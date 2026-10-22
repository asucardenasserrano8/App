"""
Módulo generado a partir de la mejora acordada: reemplazar los datos
macroeconómicos de ejemplo (fijos) por datos reales.

Fuentes usadas, y por qué:
- FRED (Federal Reserve Economic Data, del Banco de la Reserva Federal de
  St. Louis) para los indicadores macro de EUA (inflación, desempleo, PIB,
  tasa de la Fed, confianza del consumidor). Se usa su descarga pública de
  CSV, que NO requiere llave de API — así esta mejora funciona para ti sin
  que tengas que tramitar nada nuevo.
- Yahoo Finance (ya lo usas en toda la app) para índices bursátiles,
  materias primas y divisas — tampoco necesita llave.
"""
from config import *


# Series de FRED (identificadores oficiales, estables desde hace décadas)
_SERIES_FRED = {
    "CPI": "CPIAUCSL",           # Índice de Precios al Consumidor (para calcular inflación interanual)
    "Desempleo": "UNRATE",       # Tasa de desempleo (ya viene en %)
    "PIB": "A191RL1Q225SBEA",    # Crecimiento del PIB real, trimestral anualizado (ya en %)
    "Fed": "FEDFUNDS",           # Tasa de fondos federales efectiva (ya en %)
    "Confianza": "UMCSENT",      # Índice de confianza del consumidor (Universidad de Michigan)
}


def _valor_fred(serie_id, calcular_variacion_anual=False):
    """Descarga una serie de FRED (sin llave) y devuelve su valor más
    reciente ya formateado. Si algo falla (sin internet, FRED caído, etc.),
    devuelve None y quien llama debe mostrar 'no disponible' en vez de
    inventar un número."""
    try:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={serie_id}"
        df = pd.read_csv(url)
        df = df.dropna()
        if df.empty:
            return None
        columna_valor = df.columns[-1]
        if calcular_variacion_anual:
            # CPI viene como índice (ej. 314.2), no como % — calculamos la
            # inflación interanual comparando contra el mismo mes del año pasado
            if len(df) < 13:
                return None
            valor_actual = float(df[columna_valor].iloc[-1])
            valor_hace_un_anio = float(df[columna_valor].iloc[-13])
            return (valor_actual / valor_hace_un_anio - 1) * 100
        return float(df[columna_valor].iloc[-1])
    except Exception:
        return None


@st.cache_data(ttl=43200, show_spinner=False)  # 12 horas: estos datos se publican mensual/trimestralmente
def obtener_indicadores_economicos_reales():
    """Indicadores macro reales de EUA, vía FRED (sin llave de API)."""
    inflacion = _valor_fred(_SERIES_FRED["CPI"], calcular_variacion_anual=True)
    desempleo = _valor_fred(_SERIES_FRED["Desempleo"])
    pib = _valor_fred(_SERIES_FRED["PIB"])
    tasa_fed = _valor_fred(_SERIES_FRED["Fed"])
    confianza = _valor_fred(_SERIES_FRED["Confianza"])

    return {
        "Inflación (CPI, interanual)": f"{inflacion:.1f}%" if inflacion is not None else "No disponible",
        "Tasa de Desempleo": f"{desempleo:.1f}%" if desempleo is not None else "No disponible",
        "Crecimiento PIB (trimestral anualizado)": f"{pib:+.1f}%" if pib is not None else "No disponible",
        "Tasa de Interés Fed": f"{tasa_fed:.2f}%" if tasa_fed is not None else "No disponible",
        "Confianza del Consumidor": f"{confianza:.1f}" if confianza is not None else "No disponible",
    }


@st.cache_data(ttl=3600, show_spinner=False)
def obtener_mercados_globales_macro():
    """Variación % de este año (YTD) para los índices que muestra el
    Panorama Macro, vía Yahoo Finance (sin llave de API)."""
    indices = {
        "S&P 500": "^GSPC",
        "NASDAQ": "^IXIC",
        "Dow Jones": "^DJI",
        "Euro Stoxx 50": "^STOXX50E",
        "Nikkei 225": "^N225",
    }
    resultado = {}
    for nombre, simbolo in indices.items():
        try:
            hist = yf.Ticker(simbolo).history(period="ytd")
            if not hist.empty and len(hist) > 1:
                cambio = (hist["Close"].iloc[-1] / hist["Close"].iloc[0] - 1) * 100
                resultado[nombre] = f"{cambio:+.1f}% YTD"
            else:
                resultado[nombre] = "No disponible"
        except Exception:
            resultado[nombre] = "No disponible"
    return resultado


@st.cache_data(ttl=1800, show_spinner=False)
def obtener_materias_primas_macro():
    """Precio más reciente de materias primas clave, vía Yahoo Finance."""
    simbolos = {
        "Petróleo (WTI)": "CL=F",
        "Oro": "GC=F",
        "Plata": "SI=F",
        "Cobre": "HG=F",
        "Bitcoin": "BTC-USD",
    }
    resultado = {}
    for nombre, simbolo in simbolos.items():
        try:
            hist = yf.Ticker(simbolo).history(period="5d")
            if not hist.empty:
                precio = hist["Close"].iloc[-1]
                resultado[nombre] = f"${precio:,.2f}"
            else:
                resultado[nombre] = "No disponible"
        except Exception:
            resultado[nombre] = "No disponible"
    return resultado


@st.cache_data(ttl=1800, show_spinner=False)
def obtener_divisas_macro():
    """Tipos de cambio más recientes, vía Yahoo Finance."""
    simbolos = {
        "EUR/USD": "EURUSD=X",
        "USD/JPY": "JPY=X",
        "GBP/USD": "GBPUSD=X",
        "USD/MXN": "MXN=X",
        "DXY (Índice Dólar)": "DX-Y.NYB",
    }
    resultado = {}
    for nombre, simbolo in simbolos.items():
        try:
            hist = yf.Ticker(simbolo).history(period="5d")
            if not hist.empty:
                valor = hist["Close"].iloc[-1]
                resultado[nombre] = f"{valor:.4f}" if valor < 50 else f"{valor:.2f}"
            else:
                resultado[nombre] = "No disponible"
        except Exception:
            resultado[nombre] = "No disponible"
    return resultado


def obtener_datos_macro():
    """Reemplaza los datos de ejemplo fijos que tenía la app: ahora arma el
    mismo diccionario (misma forma, para no tener que tocar la vista que lo
    muestra) pero con datos reales de FRED y Yahoo Finance."""
    return {
        "indicadores_usa": obtener_indicadores_economicos_reales(),
        "mercados_globales": obtener_mercados_globales_macro(),
        "materias_primas": obtener_materias_primas_macro(),
        "divisas": obtener_divisas_macro(),
    }
