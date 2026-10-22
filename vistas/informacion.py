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
from nucleo.ia import generar_texto_ia


def mostrar_seccion_informacion(stonk, ticker, info, nombre, descripcion, start_date, end_date):
    st.header(f"🏢 Información de {nombre}")

    # Rating de analistas
    ratings = obtener_rating_analistas(stonk)
    if ratings:
        st.subheader("🎯 Rating de Analistas")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            reco_key = ratings.get('recommendationKey', 'N/A')
            if isinstance(reco_key, str):
                reco_display = reco_key.upper().replace("_", " ")
            else:
                reco_display = "N/A"
            
            st.metric("Recomendación", reco_display)
        
        with col2:
            target_price = ratings.get('targetMeanPrice', 'N/A')
            current_price = info.get('currentPrice', 0)
            if target_price != 'N/A' and current_price and target_price > current_price:
                st.metric("Target Price", f"${target_price:.2f}", f"+{((target_price/current_price)-1)*100:.1f}%")
            elif target_price != 'N/A':
                st.metric("Target Price", f"${target_price:.2f}")
            else:
                st.metric("Target Price", "N/A")
        
        with col3:
            st.metric("Rating Medio", f"{ratings.get('recommendationMean', 'N/A')}/5")
        
        with col4:
            st.metric("# Analistas", ratings.get('numberOfAnalystOpinions', 'N/A'))
       
    # Descripción traducida
    prompt = f"""
    Te voy a dar la descripción en inglés de una empresa que cotiza en bolsa, necesito que traduzcas la descripción a español financiero formal,
    quiero que la traducción sea lo más apegado posible a la descripción original y que me entregues el texto en exactamente 500 caracteres, te paso la
    descripción de la empresa: {descripcion}
    """
    
    # --- AQUÍ ESTÁ EL CAMBIO (Añadimos el spinner) ---
    with st.spinner("🤖 Traduciendo descripción de la empresa con IA..."):
        texto_traducido, error_traduccion = generar_texto_ia(prompt, "la traducción de la descripción")

    st.subheader("📋 Descripción de la Empresa")
    if texto_traducido:
        st.write(texto_traducido)
    else:
        # Si Gemini no puede traducir, antes no se veía NADA de la descripción.
        # Ahora se muestra el motivo y, mientras tanto, la descripción original
        # (en inglés) que ya trae Yahoo Finance.
        st.warning(f"No se pudo traducir la descripción. {error_traduccion}")
        if descripcion and descripcion != "No hay datos":
            st.write(descripcion)
            st.caption("Mostrando la descripción original en inglés.")
        else:
            st.info("Esta empresa no tiene descripción disponible en Yahoo Finance.")
        detalle = st.session_state.get("_ia_ultimo_detalle")
        if detalle:
            with st.expander("Detalle técnico"):
                st.code(detalle)
    
    # INFORMACIÓN DE WIKIPEDIA PARA CUALQUIER ACCIÓN
    st.subheader("📚 Información Corporativa")

    # Información adicional básica
    st.subheader("📊 Información Básica")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        sector = info.get("sector", "N/A")
        st.metric("Sector", sector)
        employees = info.get("fullTimeEmployees", "N/A")
        if employees != "N/A":
            st.metric("Empleados", f"{employees:,}")
        else:
            st.metric("Empleados", "N/A")
    
    with col2:
        industry = info.get("industry", "N/A")
        st.metric("Industria", industry)
        country = info.get("country", "N/A")
        st.metric("País", country)
    
    with col3:
        market_cap = info.get("marketCap", "N/A")
        if market_cap != "N/A":
            st.metric("Market Cap", f"${market_cap/1e9:.2f}B")
        else:
            st.metric("Market Cap", "N/A")
        
        currency = info.get("currency", "N/A")
        st.metric("Moneda", currency)
    
    with col4:
        pe_ratio = info.get("trailingPE", "N/A")
        if pe_ratio != "N/A":
            st.metric("P/E Ratio", f"{pe_ratio:.2f}")
        else:
            st.metric("P/E Ratio", "N/A")
        
        dividend_yield = info.get("dividendYield", "N/A")
        if dividend_yield and dividend_yield != "N/A":
            st.metric("Dividend Yield", f"{dividend_yield*100:.2f}%")
        else:
            st.metric("Dividend Yield", "N/A")
            
    # Línea separadora
    st.markdown("---")

    # INFORMACIÓN DE WIKIPEDIA (AHORA AL FINAL)
    st.subheader("📚 Información Corporativa")

    # Obtener información de Wikipedia
    with st.spinner('Buscando información en Wikipedia...'):
        info_wikipedia = obtener_info_wikipedia(stonk, nombre)

        if info_wikipedia.get('encontrado', False):
            # MOSTRAR DIRECTAMENTE CON MARKDOWN SIN EL CUADRO HTML
            st.markdown(info_wikipedia['contenido'])
            
            # Mostrar fuente
            st.caption(f"📖 Fuente: {info_wikipedia['fuente']} - [Enlace a Wikipedia]({info_wikipedia['url']})")
            
        else:
            st.info("""
            ℹ️ **Información no disponible**
                
            No se pudo encontrar información específica de esta empresa. 
            """)
