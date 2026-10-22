"""
Módulo generado automáticamente a partir de App.py original.
Importa todo lo común desde config para no repetir imports en cada módulo.
"""
from config import *

from nucleo.ratings import obtener_rating_analistas
from nucleo.datos import buscar_sugerencias_ticker


def render_barra_principal():
    """Buscador, historial, y botones de navegación entre secciones.
    Devuelve las variables que todas las vistas necesitan.
    """
    # Botón para alternar tema (arriba de todo, siempre visible)
    col_titulo, col_tema = st.columns([5, 1])
    with col_tema:
        if st.session_state.tema == "claro":
            if st.button("🌙 Modo oscuro", use_container_width=True):
                st.session_state.tema = "oscuro"
                st.rerun()
        else:
            if st.button("☀️ Modo claro", use_container_width=True):
                st.session_state.tema = "claro"
                st.rerun()

    if "stonk_input" not in st.session_state:
        st.session_state.stonk_input = "MSFT"

    # Si en la corrida anterior el usuario eligió una sugerencia, la
    # aplicamos ANTES de crear la caja de texto (Streamlit no permite
    # cambiar el valor de un widget después de haberlo instanciado en la
    # misma corrida — por eso esto va antes del st.text_input de abajo).
    if "stonk_pendiente" in st.session_state:
        st.session_state.stonk_input = st.session_state.pop("stonk_pendiente")

    stonk = st.text_input("Ingrese el nombre del símbolo de la acción", key="stonk_input")

    # Autocompletado EN VIVO (sin base de datos propia): mientras escribes,
    # se consulta el buscador público de Yahoo Finance y se muestran las
    # mejores coincidencias por si el símbolo exacto no lo tienes memorizado.
    if stonk:
        sugerencias = buscar_sugerencias_ticker(stonk)
        coincide_exacto = any(s.upper() == stonk.upper() for s, _, _ in sugerencias)
        if sugerencias and not coincide_exacto:
            opciones = [f"{s} — {n}" for s, n, _ in sugerencias]
            st.caption("¿Buscabas alguna de estas?")
            elegido = st.radio(
                "Sugerencias", opciones, index=None,
                label_visibility="collapsed", key="sugerencias_ticker",
            )
            if elegido:
                nuevo_simbolo = elegido.split(" — ")[0]
                if nuevo_simbolo != st.session_state.stonk_input:
                    st.session_state.stonk_pendiente = nuevo_simbolo
                    st.rerun()

    # Agregar a historial de búsquedas
    if stonk and stonk not in st.session_state.historial_busquedas:
        st.session_state.historial_busquedas.append(stonk)
        if len(st.session_state.historial_busquedas) > 10:
            st.session_state.historial_busquedas.pop(0)

    end_date = datetime.today()
    start_date = end_date - timedelta(days=5 * 365)

    # Yahoo finanzas trae los datos del Ticker
    try:
        ticker = yf.Ticker(stonk)
        info = ticker.info
        if not info or info.get("longName") is None:
            raise ValueError("símbolo no encontrado")
        nombre = info.get("longName", "Ese nombre no existe")
        descripcion = info.get("longBusinessSummary", "No hay datos")
    except Exception:
        st.error(
            f"❌ No encontramos ningún símbolo llamado **{stonk}**. "
            "Revisa que esté bien escrito, o elige una de las sugerencias de arriba."
        )
        st.stop()

    # BOTONES MEJORADOS CON NUEVA DISTRIBUCIÓN
    st.write("### 📊 Selecciona qué información quieres ver:")

    # Primera fila: 5 botones
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("🏠 Inicio", use_container_width=True, key="btn_inicio", 
                    type="primary" if st.session_state.seccion_actual == "inicio" else "secondary"):
            st.session_state.seccion_actual = "inicio"
            st.rerun()

    with col2:
        if st.button("🏢 Información", use_container_width=True, key="btn_info", 
                    type="primary" if st.session_state.seccion_actual == "info" else "secondary"):
            st.session_state.seccion_actual = "info"
            st.rerun()

    with col3:    
        if st.button("📈 Variación del precio", use_container_width=True, key="btn_datos", 
                    type="primary" if st.session_state.seccion_actual == "datos" else "secondary"):
            st.session_state.seccion_actual = "datos"
            st.rerun()

    with col4:
        if st.button("💰 Datos fundamentales", use_container_width=True, key="btn_fundamentales", 
                    type="primary" if st.session_state.seccion_actual == "fundamentales" else "secondary"):
            st.session_state.seccion_actual = "fundamentales"
            st.rerun()

    with col5:
        if st.button("📊 Análisis técnico", use_container_width=True, key="btn_tecnico", 
                    type="primary" if st.session_state.seccion_actual == "tecnico" else "secondary"):
            st.session_state.seccion_actual = "tecnico"
            st.rerun()

    # Segunda fila: 4 botones
    col6, col7, col8, col9 = st.columns(4)

    with col6:
        if st.button("🤖 Análisis IA", use_container_width=True, key="btn_ia", 
                    type="primary" if st.session_state.seccion_actual == "ia" else "secondary"):
            st.session_state.seccion_actual = "ia"
            st.rerun()

    with col7:
        if st.button("⚠️ Análisis De Riesgos", use_container_width=True, key="btn_riesgo", 
                    type="primary" if st.session_state.seccion_actual == "riesgo" else "secondary"):
            st.session_state.seccion_actual = "riesgo"
            st.rerun()

    with col8:
        if st.button("📊 Comparación", use_container_width=True, key="btn_comparar", 
                    type="primary" if st.session_state.seccion_actual == "comparar" else "secondary"):
            st.session_state.seccion_actual = "comparar"
            st.rerun()

    with col9:
        if st.button("📰 Noticias", use_container_width=True, key="btn_noticias", 
                    type="primary" if st.session_state.seccion_actual == "noticias" else "secondary"):
            st.session_state.seccion_actual = "noticias"
            st.rerun()

    col10, col11, col12 = st.columns(3)

    with col10:
        if st.button("🔍 Buscador", use_container_width=True, key="btn_screener", 
                    type="primary" if st.session_state.seccion_actual == "screener" else "secondary"):
            st.session_state.seccion_actual = "screener"
            st.rerun()

    # En la sección de botones (después del botón de Macroeconomía), agrega:
    with col11:
        if st.button("🌍 Macroeconomía", use_container_width=True, key="btn_macro", 
                    type="primary" if st.session_state.seccion_actual == "macro" else "secondary"):
            st.session_state.seccion_actual = "macro"
            st.rerun()

    # Agrega un décimo botón para Mercados Globales
    with col12:
        if st.button("📈 Mercados Globales", use_container_width=True, key="btn_global", 
                    type="primary" if st.session_state.seccion_actual == "global" else "secondary"):
            st.session_state.seccion_actual = "global"
            st.rerun()

    # Línea separadora
    st.markdown("---")

    return stonk, ticker, info, nombre, descripcion, start_date, end_date
