"""
Módulo generado automáticamente a partir de App.py original.
Importa todo lo común desde config para no repetir imports en cada módulo.
"""
from config import *

from nucleo.datos import *
from nucleo.tecnico import *
from nucleo.riesgo import *
from nucleo.scoring import *
from nucleo.wikipedia_info import *
from nucleo.ratings import *


def mostrar_seccion_macro(stonk, ticker, info, nombre, descripcion, start_date, end_date):
    st.header("🌍 Panorama Macroeconómico Global")
    
    st.markdown("""
    **Contexto macroeconómico actual** que puede afectar tus inversiones.
    Los indicadores económicos influyen en los mercados bursátiles y en las decisiones de los inversores.
    """)

    # CONFIGURACIÓN DE SESIÓN HTTP OPTIMIZADA
    def crear_session_optimizada():
        """Crea una sesión HTTP optimizada con timeouts y reintentos"""
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        session = requests.Session()
        
        # Configurar reintentos
        retry_strategy = Retry(
            total=2,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=10)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session

    # FUNCIONES AUXILIARES
    def mostrar_indicadores_en_columnas(indicadores_dict):
        """Muestra indicadores organizados en columnas"""
        cols = st.columns(2)
        current_col = 0
        
        for indicador, valor in indicadores_dict.items():
            if "---" in valor or "**" in indicador:
                # Es un separador o título
                st.markdown(f"**{indicador}**")
                continue
                
            with cols[current_col]:
                color_borde, color_texto = determinar_colores_indicador(indicador, valor)
                    
                st.markdown(f"""
                <div style='padding: 12px; margin: 8px 0; border-radius: 8px; border-left: 4px solid {color_borde}; background-color: #1e1e1e; border: 1px solid #444;'>
                    <strong style='color: #ffffff; font-size: 13px;'>{indicador}</strong><br>
                    <span style='color: {color_texto}; font-weight: bold; font-size: 14px;'>{valor}</span>
                </div>
                """, unsafe_allow_html=True)
            
            current_col = (current_col + 1) % 2

    def determinar_colores_indicador(indicador, valor):
        """Determina colores apropiados para cada tipo de indicador"""
        indicador_lower = indicador.lower()
        
        # Indicadores donde alto es malo
        if any(x in indicador_lower for x in ['inflación', 'desempleo', 'interés', 'déficit', 'deuda', 'pobreza', 'corrupción', 'riesgo', 'emisiones', 'mortalidad', 'contaminación', 'desnutrición', 'analfabetismo']):
            try:
                valor_limpio = ''.join(c for c in str(valor) if c.isdigit() or c == '.' or c == '-')
                if valor_limpio:
                    valor_num = float(valor_limpio)
                    if valor_num > 10:
                        return "#ff4444", "#ff6666"  # Rojo - Muy malo
                    elif valor_num > 5:
                        return "#ffaa00", "#ffbb33"  # Naranja - Malo
                    else:
                        return "#4CAF50", "#66bb6a"  # Verde - Bueno
            except:
                pass
            return "#2196F3", "#64b5f6"  # Azul - Neutral
        
        # Indicadores donde alto es bueno
        elif any(x in indicador_lower for x in ['crecimiento', 'confianza', 'producción', 'ventas', 'consumo', 'inversión', 'salarios', 'productividad', 'innovación', 'competitividad', 'facilidad', 'esperanza', 'alfabetización', 'matrícula', 'acceso', 'calidad']):
            try:
                valor_limpio = ''.join(c for c in str(valor) if c.isdigit() or c == '.' or c == '-')
                if valor_limpio:
                    valor_num = float(valor_limpio)
                    if valor_num > 5:
                        return "#4CAF50", "#66bb6a"  # Verde - Muy bueno
                    elif valor_num > 0:
                        return "#ffaa00", "#ffbb33"  # Naranja - Regular
                    else:
                        return "#ff4444", "#ff6666"  # Rojo - Malo
            except:
                pass
            return "#2196F3", "#64b5f6"  # Azul - Neutral
        
        # Indicadores de igualdad (Gini)
        elif 'gini' in indicador_lower:
            try:
                valor_limpio = ''.join(c for c in str(valor) if c.isdigit() or c == '.' or c == '-')
                if valor_limpio:
                    valor_num = float(valor_limpio)
                    if valor_num > 0.4:
                        return "#ff4444", "#ff6666"  # Rojo - Alta desigualdad
                    elif valor_num > 0.3:
                        return "#ffaa00", "#ffbb33"  # Naranja - Media desigualdad
                    else:
                        return "#4CAF50", "#66bb6a"  # Verde - Baja desigualdad
            except:
                pass
        
        return "#2196F3", "#64b5f6"  # Azul por defecto

    # FUNCIONES OPTIMIZADAS CON CACHING PARA WORLD BANK
    @st.cache_data(ttl=43200, show_spinner=False)  # 12 horas - países cambian muy poco
    def buscar_codigo_pais_world_bank_optimizado(nombre_pais):
        """Versión optimizada con caching para búsqueda de países"""
        try:
            session = crear_session_optimizada()
            url = f"http://api.worldbank.org/v2/country?format=json&per_page=300"
            response = session.get(url, timeout=8)
            
            if response.status_code == 200:
                data = response.json()
                if len(data) > 1:
                    # Buscar el país por nombre (búsqueda flexible)
                    nombre_buscar = nombre_pais.lower().strip()
                    for pais in data[1]:
                        nombre_pais_wb = pais['name'].lower()
                        
                        # Búsqueda exacta o parcial
                        if (nombre_buscar == nombre_pais_wb or 
                            nombre_buscar in nombre_pais_wb or 
                            nombre_pais_wb in nombre_buscar):
                            return pais['id']
                    
                    # Si no se encuentra, intentar con pycountry para nombres alternativos
                    try:
                        import pycountry
                        pais_pycountry = pycountry.countries.search_fuzzy(nombre_pais)
                        if pais_pycountry:
                            nombre_oficial = pais_pycountry[0].name
                            # Buscar nuevamente con el nombre oficial
                            for pais in data[1]:
                                if nombre_oficial.lower() == pais['name'].lower():
                                    return pais['id']
                    except:
                        pass
            return None
        except Exception as e:
            return None

    def obtener_datos_world_bank_optimizado(pais_codigo, indicadores):
        """Versión optimizada con sesión HTTP reutilizable"""
        try:
            session = crear_session_optimizada()
            datos = {}
            
            # Obtener datos en paralelo (secuencial pero optimizado)
            for indicador in indicadores:
                try:
                    url = f"http://api.worldbank.org/v2/country/{pais_codigo}/indicator/{indicador}?format=json"
                    response = session.get(url, timeout=8)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if len(data) > 1 and data[1]:
                            # Ordenar por año y obtener el más reciente
                            datos_ordenados = sorted(data[1], key=lambda x: x['date'], reverse=True)
                            for dato in datos_ordenados:
                                if dato['value'] is not None:
                                    datos[indicador] = {
                                        'valor': dato['value'],
                                        'año': dato['date'],
                                        'nombre': dato['indicator']['value']
                                    }
                                    break
                except Exception as e:
                    continue
            
            return datos
        except Exception as e:
            return {}

    @st.cache_data(ttl=86400, show_spinner=False)  # 24 horas - datos macro cambian lentamente
    def obtener_datos_pais_world_bank_optimizado(nombre_pais):
        """Versión principal optimizada con caching extensivo pero con TODOS los indicadores originales"""
        try:
            # Buscar código del país (ya cacheados)
            pais_codigo = buscar_codigo_pais_world_bank_optimizado(nombre_pais)
            
            if not pais_codigo:
                return {
                    "nombre": nombre_pais.title(),
                    "poblacion": "País no encontrado",
                    "pib_per_capita": "N/A",
                    "pib_nominal": "N/A",
                    "indicadores": {
                        "Error": f"No se pudo encontrar '{nombre_pais}' en la base de datos del World Bank",
                        "Sugerencia": "Intenta con el nombre en inglés o verifica la ortografía"
                    }
                }
            
            # INDICADORES COMPLETOS DEL WORLD BANK - CON MÁS INDICADORES SOCIALES Y AMBIENTALES
            indicadores_wb = {
                # Población y demografía
                'SP.POP.TOTL': 'Población total',
                'SP.POP.GROW': 'Crecimiento poblacional anual %',
                'SP.DYN.LE00.IN': 'Esperanza de vida al nacer',
                'SP.DYN.LE00.FE.IN': 'Esperanza de vida mujeres',
                'SP.DYN.LE00.MA.IN': 'Esperanza de vida hombres',
                'SP.URB.TOTL.IN.ZS': 'Población urbana %',
                'SP.URB.GROW': 'Crecimiento población urbana %',
                'SM.POP.NETM': 'Migración neta',
                'SP.POP.0014.TO.ZS': 'Población 0-14 años %',
                'SP.POP.1564.TO.ZS': 'Población 15-64 años %',
                'SP.POP.65UP.TO.ZS': 'Población 65+ años %',
                
                # Economía y PIB
                'NY.GDP.MKTP.CD': 'PIB nominal (US$)',
                'NY.GDP.MKTP.KD.ZG': 'Crecimiento del PIB anual %',
                'NY.GDP.PCAP.CD': 'PIB per cápita (US$)',
                'NY.GDP.PCAP.PP.CD': 'PIB per cápita PPA (US$)',
                'NY.GDP.MKTP.KD': 'PIB real (US$ constantes)',
                
                # Inflación y precios
                'FP.CPI.TOTL.ZG': 'Inflación anual %',
                'FP.CPI.TOTL': 'Índice de precios al consumidor',
                
                # Empleo
                'SL.UEM.TOTL.ZS': 'Tasa de desempleo %',
                'SL.TLF.TOTL.IN': 'Fuerza laboral total',
                'SL.EMP.TOTL.SP.ZS': 'Empleo total',
                'SL.EMP.1524.SP.ZS': 'Desempleo juvenil %',
                
                # Comercio exterior
                'NE.EXP.GNFS.CD': 'Exportaciones de bienes y servicios (US$)',
                'NE.IMP.GNFS.CD': 'Importaciones de bienes y servicios (US$)',
                'NE.RSB.GNFS.CD': 'Balanza comercial (US$)',
                'NE.EXP.GNFS.ZS': 'Exportaciones % PIB',
                'NE.IMP.GNFS.ZS': 'Importaciones % PIB',
                
                # Finanzas públicas
                'GC.DOD.TOTL.GD.ZS': 'Deuda pública % PIB',
                'GC.REV.XGRT.GD.ZS': 'Ingresos del gobierno % PIB',
                'GC.XPN.TOTL.GD.ZS': 'Gasto del gobierno % PIB',
                'GC.BAL.CASH.GD.ZS': 'Balance fiscal % PIB',
                
                # SALUD - MÁS INDICADORES
                'SH.XPD.CHEX.GD.ZS': 'Gasto en salud % PIB',
                'SH.XPD.CHEX.PC.CD': 'Gasto en salud per cápita (US$)',
                'SH.DYN.MORT': 'Tasa de mortalidad menores de 5 años',
                'SH.DYN.MORT.FE': 'Mortalidad menores de 5 años (mujeres)',
                'SH.DYN.MORT.MA': 'Mortalidad menores de 5 años (hombres)',
                'SH.DYN.AIDS.ZS': 'Prevalencia de VIH %',
                'SH.STA.OWGH.ZS': 'Obesidad adulta %',
                'SH.STA.OWGH.FE.ZS': 'Obesidad adulta mujeres %',
                'SH.STA.OWGH.MA.ZS': 'Obesidad adulta hombres %',
                'SH.STA.MMRT': 'Tasa mortalidad materna',
                'SH.STA.BRTW.ZS': 'Partos atendidos por personal calificado %',
                'SH.IMM.MEAS': 'Vacunación contra sarampión %',
                'SH.TBS.INCD': 'Incidencia de tuberculosis',
                'SH.MED.BEDS.ZS': 'Camas de hospital por 1000 habitantes',
                'SH.MED.PHYS.ZS': 'Médicos por 1000 habitantes',
                
                # EDUCACIÓN - MÁS INDICADORES
                'SE.XPD.TOTL.GD.ZS': 'Gasto en educación % PIB',
                'SE.XPD.PRIM.ZS': 'Gasto educación primaria %',
                'SE.XPD.SECO.ZS': 'Gasto educación secundaria %',
                'SE.XPD.TERT.ZS': 'Gasto educación terciaria %',
                'SE.ADT.LITR.ZS': 'Tasa de alfabetización adultos %',
                'SE.ADT.1524.LT.FE.ZS': 'Alfabetización jóvenes mujeres %',
                'SE.ADT.1524.LT.MA.ZS': 'Alfabetización jóvenes hombres %',
                'SE.PRM.ENRR': 'Tasa de matrícula primaria',
                'SE.SEC.ENRR': 'Tasa de matrícula secundaria',
                'SE.TER.ENRR': 'Tasa de matrícula terciaria',
                'SE.PRM.CMPT.ZS': 'Tasa finalización primaria %',
                'SE.SEC.CMPT.LO.ZS': 'Tasa finalización secundaria %',
                'SE.PRM.PRSL.ZS': 'Tasa repetición primaria %',
                
                # POBREZA Y DESIGUALDAD - MÁS INDICADORES
                'SI.POV.DDAY': 'Pobreza $3.20/día % población',
                'SI.POV.UMIC': 'Pobreza $5.50/día % población',
                'SI.POV.GINI': 'Coeficiente Gini',
                'SI.POV.NAHC': 'Pobreza nacional %',
                'SI.POV.NAHC.FE': 'Pobreza nacional mujeres %',
                'SI.POV.NAHC.MA': 'Pobreza nacional hombres %',
                'SI.DST.02.20': 'Participación ingreso 20% más rico',
                'SI.DST.FRST.20': 'Participación ingreso 20% más pobre',
                'SI.DST.05TH.20': 'Participación ingreso quintil 5',
                
                # PROTECCIÓN SOCIAL
                'per_sa_allsa.cov_pop_tot': 'Cobertura protección social %',
                'per_lm_alllm.cov_pop_tot': 'Cobertura desempleo %',
                
                # INFRAESTRUCTURA
                'EG.ELC.ACCS.ZS': 'Acceso a electricidad % población',
                'EG.ELC.ACCS.RU.ZS': 'Acceso electricidad rural %',
                'EG.ELC.ACCS.UR.ZS': 'Acceso electricidad urbana %',
                'IT.NET.USER.ZS': 'Usuarios de internet % población',
                'IS.RRS.TOTL.KM': 'Red ferroviaria total (km)',
                'IS.ROD.GOOD.MT': 'Red caminos pavimentados %',
                'EG.NSF.ACCS.ZS': 'Acceso a servicios sanitarios %',
                'SH.H2O.SAFE.ZS': 'Acceso a agua potable %',
                'SH.STA.ACSN': 'Acceso a saneamiento %',
                
                # MEDIO AMBIENTE - MÁS INDICADORES
                'EN.ATM.CO2E.PC': 'Emisiones CO2 per cápita',
                'EN.ATM.CO2E.KT': 'Emisiones CO2 totales (kt)',
                'EN.ATM.CO2E.GF.KT': 'Emisiones CO2 combustible (kt)',
                'EN.ATM.GHGO.KT.CE': 'Emisiones gases efecto invernadero',
                'EN.ATM.METH.KT.CE': 'Emisiones metano',
                'EN.ATM.NOXE.KT.CE': 'Emisiones óxido nitroso',
                'EN.ATM.PM25.MC.M3': 'Contaminación PM2.5',
                'AG.LND.FRST.ZS': 'Área forestal % territorio',
                'AG.LND.FRST.K2': 'Área forestal (km²)',
                'ER.H2O.FWTL.ZS': 'Estrés hídrico %',
                'ER.GDP.FWTL.M3.KD': 'Productividad agua (US$/m³)',
                'AG.CON.FERT.ZS': 'Uso de fertilizantes (kg/ha)',
                'AG.CON.FERT.PT.ZS': 'Uso fertilizantes fosfatados',
                'AG.LND.AGRI.ZS': 'Tierra agrícola %',
                'AG.LND.ARBL.ZS': 'Tierra cultivable %',
                'ER.LND.PTLD.ZS': 'Tierra degradada %',
                'ER.PTD.TOTL.ZS': 'Especies amenazadas %',
                'ER.MRN.PTMR.ZS': 'Especies marinas amenazadas',
                'EN.CLC.MDAT.ZS': 'Cobertura áreas protegidas %',
                'EN.MAM.THRD.NO': 'Especies mamíferos amenazadas',
                'EN.BIR.THRD.NO': 'Especies aves amenazadas',
                'AG.PRD.CREL.MT': 'Producción cereales (ton)',
                'ER.H2O.INTR.PC': 'Recursos hídricos internos per cápita',
                
                # ENERGÍA - NUEVOS INDICADORES
                'EG.USE.COMM.FO.ZS': 'Uso energía combustibles fósiles %',
                'EG.USE.CRNW.ZS': 'Uso energía renovable %',
                'EG.ELC.RNEW.ZS': 'Electricidad renovable %',
                'EG.FEC.RNEW.ZS': 'Energía renovable consumo final %',
                'EG.ELC.NUCL.ZS': 'Electricidad nuclear %',
                'EG.ELC.HYRO.ZS': 'Electricidad hidroeléctrica %',
                
                # CALIDAD DEL AIRE
                'EN.ATM.PM25.MC.M3': 'Concentración PM2.5 (μg/m³)',
                'EN.ATM.NOXE.PC': 'Emisiones NOx per cápita',
                
                # RESIDUOS
                'EN.POP.SLUM.UR.ZS': 'Población en barrios marginales %',
                'EN.POP.SLUM.UR.ZS.1': 'Acceso mejorado a agua urbana %',
                
                # Negocios y competitividad
                'IC.BUS.EASE.XQ': 'Facilidad para hacer negocios',
                'IC.TAX.TOTL.CP.ZS': 'Carga tributaria total %',
                'IC.FRM.CORR.ZS': 'Empresas que experimentan soborno %',
                'IC.REG.COST.PC.ZS': 'Costo registrar empresa % ingreso per cápita',
                
                # GÉNERO E INCLUSIÓN
                'SG.GEN.PARL.ZS': 'Mujeres en parlamento %',
                'SG.VAW.REAS.ZS': 'Mujeres que justifican violencia doméstica %',
                'SG.DMK.SRCR.FN.ZS': 'Mujeres cuenta bancaria %',
                'SL.TLF.CACT.FE.ZS': 'Participación fuerza laboral mujeres %'
            }
            
            # Obtener TODOS los indicadores
            datos_wb = obtener_datos_world_bank_optimizado(pais_codigo, list(indicadores_wb.keys()))
            
            # Obtener nombre oficial del país
            nombre_oficial = nombre_pais.title()
            for pais_info in datos_wb.values():
                if 'nombre' in pais_info:
                    if ' - ' in pais_info['nombre']:
                        nombre_oficial = pais_info['nombre'].split(' - ')[-1]
                        break
            
            # Procesar y formatear los datos
            indicadores_formateados = {}
            
            # Información básica del país
            poblacion = datos_wb.get('SP.POP.TOTL', {}).get('valor', 'N/A')
            pib_nominal = datos_wb.get('NY.GDP.MKTP.CD', {}).get('valor', 'N/A')
            pib_per_capita = datos_wb.get('NY.GDP.PCAP.CD', {}).get('valor', 'N/A')
            pib_ppa = datos_wb.get('NY.GDP.PCAP.PP.CD', {}).get('valor', 'N/A')
            
            # Formatear valores grandes
            def formatear_numero_grande(valor):
                if isinstance(valor, (int, float)):
                    if valor > 1e12:
                        return f"{valor/1e12:.2f}T"
                    elif valor > 1e9:
                        return f"{valor/1e9:.2f}B"
                    elif valor > 1e6:
                        return f"{valor/1e6:.2f}M"
                    else:
                        return f"{valor:,.0f}"
                return str(valor)
            
            def formatear_moneda(valor):
                if isinstance(valor, (int, float)):
                    if valor > 1e12:
                        return f"${valor/1e12:.2f}T"
                    elif valor > 1e9:
                        return f"${valor/1e9:.2f}B"
                    elif valor > 1e6:
                        return f"${valor/1e6:.2f}M"
                    else:
                        return f"${valor:,.0f}"
                return str(valor)
            
            poblacion_str = formatear_numero_grande(poblacion)
            pib_nominal_str = formatear_moneda(pib_nominal)
            pib_per_capita_str = formatear_moneda(pib_per_capita)
            pib_ppa_str = formatear_moneda(pib_ppa)
            
            # Construir diccionario de indicadores
            for codigo, nombre in indicadores_wb.items():
                if codigo in datos_wb:
                    dato = datos_wb[codigo]
                    valor = dato['valor']
                    año = dato['año']
                    
                    # Formatear valores según el tipo de indicador
                    if isinstance(valor, (int, float)):
                        if 'US$' in nombre or codigo in ['NY.GDP.MKTP.CD', 'NY.GDP.PCAP.CD', 'NY.GDP.PCAP.PP.CD', 'NE.EXP.GNFS.CD', 'NE.IMP.GNFS.CD']:
                            valor_str = formatear_moneda(valor)
                        elif any(x in nombre for x in ['%', 'tasa', 'crecimiento', 'ratio']):
                            valor_str = f"{valor:.2f}%"
                        elif 'coeficiente' in nombre.lower() or 'índice' in nombre.lower():
                            valor_str = f"{valor:.3f}"
                        else:
                            valor_str = formatear_numero_grande(valor)
                    else:
                        valor_str = str(valor)
                    
                    indicadores_formateados[f"{nombre} ({año})"] = valor_str
            
            return {
                "nombre": nombre_oficial,
                "poblacion": poblacion_str,
                "pib_per_capita": pib_per_capita_str,
                "pib_nominal": pib_nominal_str,
                "pib_ppa": pib_ppa_str,
                "codigo": pais_codigo,
                "indicadores": indicadores_formateados
            }
            
        except Exception as e:
            return {
                "nombre": nombre_pais.title(),
                "poblacion": "Error en consulta",
                "pib_per_capita": "Error en consulta",
                "pib_nominal": "Error en consulta",
                "pib_ppa": "Error en consulta",
                "indicadores": {
                    "Error": f"No se pudieron obtener datos: {str(e)}",
                    "Recomendación": "Intenta nuevamente en unos momentos"
                }
            }

    # Inicializar session_state para el país seleccionado
    if 'pais_seleccionado_macro' not in st.session_state:
        st.session_state.pais_seleccionado_macro = None
    
    # BUSCADOR Y MAPA
    st.subheader("🔍 Buscar y Seleccionar País")
    
    # Buscador de países
    col_buscador, col_limpiar = st.columns([3, 1])
    with col_buscador:
        pais_buscador = st.text_input(
            "Escribe el nombre de cualquier país del mundo:",
            placeholder="Ej: United States, Germany, Japan, Brazil, Mexico, Argentina, Spain, France, China, India...",
            key="buscador_paises_macro"
        )
    with col_limpiar:
        if st.session_state.pais_seleccionado_macro:
            if st.button("🗑️ Limpiar selección", use_container_width=True):
                st.session_state.pais_seleccionado_macro = None
                st.rerun()
    
    # Mapa interactivo con Folium
    try:
        from streamlit_folium import st_folium
        import folium
        from geopy.geocoders import Nominatim
        
        st.subheader("🗺️ Mapa Mundial Interactivo - Selecciona cualquier país")
        
        # Crear mapa global centrado
        m = folium.Map(location=[20, 0], zoom_start=2)
        
        # Mostrar mapa en Streamlit y capturar clic
        mapa_datos = st_folium(m, width=700, height=400, returned_objects=["last_clicked"])
        
        # Detectar clic en el mapa
        if mapa_datos and mapa_datos.get("last_clicked") is not None:
            lat = mapa_datos["last_clicked"]["lat"]
            lon = mapa_datos["last_clicked"]["lng"]
            
            try:
                geolocator = Nominatim(user_agent="macro_app")
                location = geolocator.reverse((lat, lon), language="en", exactly_one=True, timeout=5)
                
                if location and 'address' in location.raw and 'country' in location.raw['address']:
                    pais_click = location.raw['address']['country']
                    st.session_state.pais_seleccionado_macro = pais_click
                    st.success(f"🌍 País seleccionado desde el mapa: **{pais_click}**")
                    
            except Exception as e:
                st.warning("⚠️ No se pudo identificar el país. Intenta hacer clic más cerca del centro del país.")
                
    except ImportError:
        st.info("""
        **💡 Mapa no disponible** 
        Para usar el mapa interactivo, instala: 
        `pip install streamlit-folium folium geopy`
        """)
    
    # Determinar qué país mostrar (del buscador O del mapa)
    pais_actual = None
    if pais_buscador and pais_buscador.strip():
        pais_actual = pais_buscador.strip()
        st.session_state.pais_seleccionado_macro = pais_actual
    elif st.session_state.pais_seleccionado_macro:
        pais_actual = st.session_state.pais_seleccionado_macro
    
    # Indicador del país seleccionado
    if pais_actual:
        st.success(f"**País seleccionado:** {pais_actual}")
    else:
        st.info("💡 **Escribe el nombre de un país en el buscador o haz clic en el mapa**")
    
    # MOSTRAR INFORMACIÓN DEL PAÍS SELECCIONADO
    st.markdown("---")
    
    if pais_actual:
        # Mostrar vista específica del país usando la función optimizada
        with st.spinner(f"📊 Cargando datos económicos de {pais_actual}..."):
            datos_pais = obtener_datos_pais_world_bank_optimizado(pais_actual)
        
        st.header(f"📊 Información Económica Completa de {datos_pais['nombre']}")
        
        # Mostrar código del país si se encontró
        if datos_pais.get('codigo'):
            st.caption(f"**World Bank Group:** {datos_pais['codigo']}")
        
        # Métricas principales
        st.subheader("📈 Métricas Principales")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Población", datos_pais.get('poblacion', 'N/A'))
        with col2:
            st.metric("💰 PIB Per Cápita", datos_pais.get('pib_per_capita', 'N/A'))
        with col3:
            st.metric("🌍 PIB Nominal", datos_pais.get('pib_nominal', 'N/A'))
        with col4:
            st.metric("⚖️ PIB PPA", datos_pais.get('pib_ppa', 'N/A'))
        
        # Indicadores económicos del país
        st.subheader("📊 Indicadores Económicos del World Bank Group")
        indicadores = datos_pais.get("indicadores", {})
        
        if indicadores and len(indicadores) > 2:
            # Crear pestañas para diferentes categorías de indicadores
            tab_principales, tab_economia, tab_social, tab_ambiente = st.tabs([
                "🎯 Principales", 
                "💰 Economía", 
                "👥 Social",
                "🌱 Ambiente"
            ])
            
            with tab_principales:
                st.subheader("📈 Indicadores Principales")
                indicadores_principales = {
                    k: v for k, v in indicadores.items() 
                    if any(x in k.lower() for x in ['pib', 'crecimiento', 'inflación', 'desempleo', 'población'])
                }
                if indicadores_principales:
                    mostrar_indicadores_en_columnas(indicadores_principales)
                else:
                    st.info("No hay indicadores principales disponibles")
            
            with tab_economia:
                st.subheader("💰 Indicadores Económicos")
                indicadores_economia = {
                    k: v for k, v in indicadores.items() 
                    if any(x in k.lower() for x in ['exportaciones', 'importaciones', 'balanza', 'deuda', 'gasto', 'ingresos', 'comercio', 'fiscal', 'tributaria'])
                }
                if indicadores_economia:
                    mostrar_indicadores_en_columnas(indicadores_economia)
                else:
                    st.info("No hay indicadores económicos disponibles")
            
            with tab_social:
                st.subheader("👥 Indicadores Sociales")
                indicadores_social = {
                    k: v for k, v in indicadores.items() 
                    if any(x in k.lower() for x in [
                        'esperanza', 'salud', 'educación', 'pobreza', 'gini', 'alfabetización', 'mortalidad', 
                        'obesidad', 'vacunación', 'tuberculosis', 'médicos', 'matrícula', 'género', 'mujeres',
                        'protección social', 'desempleo juvenil', 'camas hospital'
                    ])
                }
                if indicadores_social:
                    mostrar_indicadores_en_columnas(indicadores_social)
                else:
                    st.info("No hay indicadores sociales disponibles")
            
            with tab_ambiente:
                st.subheader("🌱 Indicadores Ambientales")
                indicadores_ambiente = {
                    k: v for k, v in indicadores.items() 
                    if any(x in k.lower() for x in [
                        'emisiones', 'forestal', 'electricidad', 'internet', 'agua', 'medio ambiente', 'co2',
                        'energía', 'renovable', 'contaminación', 'áreas protegidas', 'especies', 'residuos',
                        'calidad del aire', 'estrés hídrico', 'fertilizantes', 'metano', 'nuclear', 'hidroeléctrica'
                    ])
                }
                if indicadores_ambiente:
                    mostrar_indicadores_en_columnas(indicadores_ambiente)
                else:
                    st.info("No hay indicadores ambientales disponibles")
            
            # Botones de control
            col_act1, col_act2, col_act3 = st.columns(3)
            with col_act1:
                if st.button("🔄 Actualizar Datos", use_container_width=True, type="primary"):
                    st.cache_data.clear()
                    st.rerun()
            with col_act2:
                if st.button("📥 Exportar Datos", use_container_width=True):
                    st.info("Función de exportación en desarrollo")
            with col_act3:
                st.info("**Fuente:** World Bank Group")
                
        else:
            st.warning("""
            **No se pudieron obtener datos específicos para este país.**
            
            Posibles razones:
            - El país puede no estar en la base de datos del World Bank Group
            - Problemas temporales de conexión con la API
            - El país no tiene datos disponibles para los indicadores solicitados
            
            **Solución:** Intenta con otro país o verifica el nombre.
            """)
                
    else:
        # Vista cuando no hay país seleccionado
        st.info("🌍 **Selecciona un país usando el buscador o el mapa para ver sus datos económicos**")
        
        st.markdown("""
        ### 💡 Cómo usar esta sección:
        
        1. **🔍 Buscar país**: Escribe el nombre de cualquier país
        2. **🗺️ Mapa interactivo**: Haz clic en cualquier país del mapa mundial
        3. **📊 Datos oficiales**: Obtén información económica verificada del World Bank Group
        
        ### 📈 Información disponible:
        - **Métricas principales**: Población, PIB, PIB per cápita
        - **Indicadores económicos**: Crecimiento, inflación, desempleo
        - **Comercio exterior**: Exportaciones, importaciones, balanza comercial
        - **Finanzas públicas**: Deuda pública, gasto gubernamental
        - **Indicadores sociales**: Salud, educación, pobreza, desigualdad, género
        - **Medio ambiente**: Emisiones, energía renovable, áreas protegidas, calidad del aire
        
        ### 🚀 **Optimizaciones implementadas:**
        - **Caching de 24 horas** para datos que cambian lentamente
        - **Sesiones HTTP optimizadas** con reintentos automáticos
        - **Timeouts configurados** para evitar bloqueos
        - **80+ indicadores reales** del World Bank
        """)
    
    # INFORMACIÓN SOBRE LA FUENTE
    st.markdown("---")
    st.success("""
    **🌐 Fuente de Datos: World Bank Group**
    
    - **📊 Datos oficiales** de gobiernos e instituciones internacionales
    - **🕐 Actualizaciones periódicas** según disponibilidad de cada indicador
    - **🌍 Cobertura global** de más de 200 países y territorios
    - **📈 Series históricas** desde 1960 para muchos indicadores
    - **🎯 Metodología consistente** entre países y años
    
    **🚀 Optimizado para rendimiento:**
    - Cache de 24 horas para datos macroeconómicos
    - Conexiones HTTP optimizadas con reintentos
    - Timeouts para respuestas rápidas
    - **80+ indicadores reales** sin datos simulados
    
    **Nota:** Algunos indicadores pueden tener datos con 1-2 años de retraso debido a los procesos de recolección y verificación.
    """)
