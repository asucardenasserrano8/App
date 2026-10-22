"""
Ayudante único para pedirle texto a Gemini desde cualquier sección.

- Guarda en memoria de la sesión las respuestas que SÍ salieron bien, para no
  gastar cuota pidiendo lo mismo en cada recarga de la página.
- Los fallos no se guardan por mucho tiempo (solo unos segundos, para no
  repetir una petición que acaba de fallar): así, en cuanto arregles la llave,
  el análisis vuelve a funcionar sin esperar.
- Los errores se muestran en español y sin enseñar nunca la llave de API.
"""
import hashlib

from config import *
from nucleo.errores import mensaje_amigable, ocultar_llaves

_SEGUNDOS_ESPERA_TRAS_FALLO = 45
MODELO_IA = "gemini-3.8-flash"


def generar_texto_ia(prompt, contexto="el análisis con IA"):
    """Devuelve (texto, error). Si todo sale bien, error es None; si falla,
    texto es None y error trae un mensaje claro en español."""
    cache = st.session_state.setdefault("_ia_cache", {})
    clave = hashlib.md5(prompt.encode("utf-8")).hexdigest()
    guardado = cache.get(clave)
    if guardado:
        texto, error, detalle, momento = guardado
        if texto:
            return texto, None
        if time.time() - momento < _SEGUNDOS_ESPERA_TRAS_FALLO:
            st.session_state["_ia_ultimo_detalle"] = detalle
            return None, error

    try:
        modelo = genai.GenerativeModel(MODELO_IA)
        respuesta = modelo.generate_content(prompt)
        texto = getattr(respuesta, "text", None)
        if not texto or not texto.strip():
            raise ValueError("Gemini respondió sin texto utilizable (empty response)")
        cache[clave] = (texto, None, None, time.time())
        return texto, None
    except Exception as e:
        error = mensaje_amigable(e, contexto)
        detalle = ocultar_llaves(f"{type(e).__name__}: {e}")
        cache[clave] = (None, error, detalle, time.time())
        st.session_state["_ia_ultimo_detalle"] = detalle
        return None, error


def mostrar_analisis_ia(titulo, prompt, contexto="el análisis con IA"):
    """Genera y muestra un análisis con IA dentro de la sección actual.
    Si no se puede generar, avisa claramente (con el detalle técnico
    escondido en un expander) en vez de dejar un hueco en la página."""
    st.markdown(f"#### 🤖 {titulo}")
    with st.spinner("Generando análisis con IA..."):
        texto, error = generar_texto_ia(prompt, contexto)
    if texto:
        st.markdown(texto)
        st.caption("Generado con IA (Gemini). Es informativo y no constituye asesoría financiera.")
    else:
        st.warning(error)
        detalle = st.session_state.get("_ia_ultimo_detalle")
        if detalle:
            with st.expander("Detalle técnico"):
                st.code(detalle)
    return texto
