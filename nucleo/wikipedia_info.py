"""
Módulo generado automáticamente a partir de App.py original.
Importa todo lo común desde config para no repetir imports en cada módulo.
"""
from config import *


@st.cache_data(ttl=3600)
def obtener_info_wikipedia(ticker, nombre_empresa):
    """
    Obtiene información de Wikipedia usando la API oficial - CONTENIDO COMPLETO MEJORADO
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # PRIMERO: Usar la API de búsqueda de Wikipedia para encontrar la página correcta
        search_url = f"https://es.wikipedia.org/w/api.php?action=query&list=search&srsearch={nombre_empresa}&format=json&srlimit=5"
        
        search_response = requests.get(search_url, headers=headers, timeout=10)
        
        if search_response.status_code == 200:
            search_data = search_response.json()
            
            if search_data['query']['search']:
                # Tomar el primer resultado que parezca relevante
                for result in search_data['query']['search']:
                    title = result['title']
                    
                    # Verificar que el título sea relevante (contenga palabras clave de la empresa)
                    if any(keyword in title.lower() for keyword in ['inc', 'corp', 'company', 'corporation', nombre_empresa.split()[0].lower()]):
                        # Obtener el contenido COMPLETO de la página usando la API
                        content_url = f"https://es.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=true&titles={title}&format=json"
                        content_response = requests.get(content_url, headers=headers, timeout=10)
                        
                        if content_response.status_code == 200:
                            content_data = content_response.json()
                            pages = content_data['query']['pages']
                            
                            for page_id, page_data in pages.items():
                                if 'extract' in page_data and page_data['extract']:
                                    contenido = page_data['extract']
                                    
                                    # LIMPIAR EL FORMATO DE TÍTULOS
                                    contenido_limpio = limpiar_formato_wikipedia(contenido)
                                    
                                    return {
                                        'encontrado': True,
                                        'contenido': contenido_limpio,
                                        'url': f"https://es.wikipedia.org/wiki/{title.replace(' ', '_')}",
                                        'termino_busqueda': title,
                                        'fuente': 'API Wikipedia'
                                    }
        
        # SEGUNDO: Intentar con búsqueda en inglés
        search_url_english = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={nombre_empresa}&format=json&srlimit=5"
        
        search_response_english = requests.get(search_url_english, headers=headers, timeout=10)
        
        if search_response_english.status_code == 200:
            search_data_english = search_response_english.json()
            
            if search_data_english['query']['search']:
                for result in search_data_english['query']['search']:
                    title = result['title']
                    
                    if any(keyword in title.lower() for keyword in ['inc', 'corp', 'company', 'corporation', nombre_empresa.split()[0].lower()]):
                        content_url_english = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=true&titles={title}&format=json"
                        content_response_english = requests.get(content_url_english, headers=headers, timeout=10)
                        
                        if content_response_english.status_code == 200:
                            content_data_english = content_response_english.json()
                            pages_english = content_data_english['query']['pages']
                            
                            for page_id, page_data in pages_english.items():
                                if 'extract' in page_data and page_data['extract']:
                                    contenido_ingles = page_data['extract']
                                    
                                    # LIMPIAR EL FORMATO PRIMERO
                                    contenido_ingles_limpio = limpiar_formato_wikipedia(contenido_ingles)
                                    
                                    # Traducir con Gemini - CONTENIDO COMPLETO
                                    try:
                                        prompt_traduccion = f"""
                                        Traduce al español el siguiente texto sobre una empresa manteniendo un tono formal.
                                        Conserva términos técnicos y financieros sin cambios.
                                        Traduce TODO el texto completo sin omitir nada.
                                        
                                        Texto: {contenido_ingles_limpio}
                                        """
                                        
                                        response_traduccion = genai.models.generate_content(
                                            model="gemini-3.8-flash",
                                            contents=prompt_traduccion
                                        )
                                        
                                        contenido_traducido = response_traduccion.text
                                        
                                        return {
                                            'encontrado': True,
                                            'contenido': contenido_traducido,
                                            'url': f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                                            'termino_busqueda': title,
                                            'fuente': 'API Wikipedia Inglés (Traducido)'
                                        }
                                    except:
                                        # Si falla la traducción, devolver en inglés COMPLETO
                                        return {
                                            'encontrado': True,
                                            'contenido': contenido_ingles_limpio,
                                            'url': f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                                            'termino_busqueda': title,
                                            'fuente': 'API Wikipedia Inglés'
                                        }
        
        return {'encontrado': False, 'error': 'No se encontró información en Wikipedia'}
            
    except Exception as e:
        return {'encontrado': False, 'error': f'Error: {str(e)}'}


def limpiar_formato_wikipedia(texto):
    """
    Limpia el formato de markdown de Wikipedia y convierte los títulos a formato Markdown
    """
    if not texto:
        return texto
    
    lineas = texto.split('\n')
    lineas_limpias = []
    
    for linea in lineas:
        linea_limpia = linea.strip()
        if not linea_limpia:
            continue
            
        # Detectar títulos con === Título ===
        if linea_limpia.startswith('===') and linea_limpia.endswith('==='):
            # Es un título principal (### en Markdown)
            titulo = linea_limpia.replace('===', '').strip()
            if titulo:
                lineas_limpias.append(f"### {titulo}")
                
        # Detectar subtítulos con == Título ==
        elif linea_limpia.startswith('==') and linea_limpia.endswith('=='):
            # Es un subtítulo (## en Markdown)
            subtitulo = linea_limpia.replace('==', '').strip()
            if subtitulo:
                lineas_limpias.append(f"## {subtitulo}")
                
        else:
            # Texto normal
            lineas_limpias.append(linea_limpia)
    
    return '\n\n'.join(lineas_limpias)
