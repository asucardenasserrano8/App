"""
Manejo amable de errores: traduce errores técnicos a mensajes claros en
español, y NUNCA deja ver llaves de API en pantalla.
"""
import re

from config import *

# Patrones de llaves/credenciales que no deben mostrarse nunca en la app
# (ni siquiera dentro del "Detalle técnico"): una llave visible en una
# captura de pantalla o en un chat equivale a una llave filtrada.
_PATRONES_LLAVES = [
    (re.compile(r"api_key:[^\s'\"\\\]]+"), "api_key:[oculta]"),
    (re.compile(r"AIza[0-9A-Za-z_\-]{20,}"), "[llave oculta]"),
    (re.compile(r"AQ\.[0-9A-Za-z_\-]{20,}"), "[llave oculta]"),
]


def ocultar_llaves(texto):
    """Reemplaza cualquier llave de API que aparezca dentro de un texto."""
    texto = str(texto)
    for patron, reemplazo in _PATRONES_LLAVES:
        texto = patron.sub(reemplazo, texto)
    return texto


def mensaje_amigable(excepcion, contexto=""):
    """Traduce errores técnicos comunes (de red, de APIs, de datos faltantes)
    a un mensaje claro en español. Si no reconoce el tipo de error, da un
    mensaje genérico pero amable en vez de mostrar la excepción cruda."""
    texto = str(excepcion).lower()
    prefijo = f" en {contexto}" if contexto else ""

    # Proyecto/llave suspendidos por Google (ej. porque la llave se filtró).
    # Va ANTES del caso de "api_key" porque ese texto también contiene "api_key".
    if "consumer_suspended" in texto or "has been suspended" in texto:
        return ("🚫 Google suspendió el proyecto al que pertenece tu llave de Gemini "
                "(suele pasar cuando una llave se filtra públicamente). Crea una llave "
                "nueva en un PROYECTO NUEVO desde aistudio.google.com, ponla en la "
                "línea AP= de tu .env y reinicia la app.")
    if "permission denied" in texto or "permissiondenied" in texto or "403" in texto:
        return ("🔒 Google rechazó la petición (permiso denegado). Revisa que tu llave "
                "de Gemini esté activa y que pertenezca a un proyecto sin restricciones.")
    if "timeout" in texto or "timed out" in texto or "read timed out" in texto:
        return "⏱️ La fuente de datos tardó demasiado en responder. Intenta de nuevo en unos segundos."
    if "connection" in texto or "connexion" in texto or "max retries" in texto:
        return "🌐 No se pudo conectar con la fuente de datos. Revisa tu conexión a internet."
    if "429" in texto or "rate limit" in texto or "too many requests" in texto or "quota" in texto:
        return "🚦 Se alcanzó el límite de peticiones de una fuente de datos gratuita. Espera un momento y vuelve a intentar."
    if "api_key" in texto or ("api key" in texto and "valid" in texto) or "unauthorized" in texto or "401" in texto:
        return "🔑 Hay un problema con una llave de API (puede faltar, estar mal escrita, o haber expirado). Revisa tu archivo .env."
    if "404" in texto or "not found" in texto:
        return "🔎 No encontramos ese dato en la fuente consultada. Puede que el símbolo esté mal escrito o no esté disponible ahí."
    if isinstance(excepcion, KeyError):
        return "📭 Los datos que llegaron no traían la información esperada — puede que este símbolo no la tenga disponible."
    if "empty" in texto or "no data" in texto or "no hay datos" in texto:
        return "📭 No encontramos datos para este símbolo en el rango solicitado."
    return f"⚠️ Ocurrió un problema{prefijo}. Intenta de nuevo en unos momentos."


def mostrar_error_amigable(excepcion, contexto=""):
    """Muestra el error de forma amigable en la interfaz, y deja el detalle
    técnico (con las llaves ocultas) dentro de un expander plegado."""
    st.error(mensaje_amigable(excepcion, contexto))
    with st.expander("Detalle técnico"):
        st.code(ocultar_llaves(f"{type(excepcion).__name__}: {excepcion}"))
