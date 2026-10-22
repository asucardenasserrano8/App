"""
Módulo generado automáticamente a partir de App.py original.
Importa todo lo común desde config para no repetir imports en cada módulo.
"""
from config import *


@st.cache_data(ttl=86400, show_spinner=False)  # 24 horas: la composición del índice cambia pocas veces al año
def obtener_lista_sp500_actual():
    """Lista ACTUAL de las 500 empresas del S&P 500, tomada de Wikipedia
    (se actualiza sola cada vez que hay cambios reales en el índice —
    fusiones, adquisiciones, altas y bajas). Devuelve None si no se pudo
    obtener (sin internet, cambió el formato de la página, etc.), y quien
    llama debe usar una lista de respaldo en ese caso."""
    try:
        # Wikipedia a veces rechaza peticiones que no se identifican como
        # un navegador real (pd.read_html por sí solo no manda ese
        # encabezado) — por eso se descarga con requests primero.
        respuesta = requests.get(
            "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
            headers={"User-Agent": "Mozilla/5.0 (compatible; IndiceApp/1.0)"},
            timeout=10,
        )
        respuesta.raise_for_status()
        tablas = pd.read_html(io.StringIO(respuesta.text))
        simbolos = tablas[0]["Symbol"].tolist()
        # yfinance usa guion en vez de punto para acciones de doble clase (ej. BRK.B -> BRK-B)
        simbolos = [str(s).replace(".", "-") for s in simbolos]
        # Verificación mínima de sanidad: si Wikipedia cambió su formato y
        # esto viene corto o vacío, mejor no arriesgarse a una lista mala
        if len(simbolos) < 400:
            return None
        return simbolos
    except Exception:
        return None


@st.cache_data(ttl=3600, show_spinner=False, max_entries=200)
def buscar_sugerencias_ticker(consulta):
    """Autocompletado de tickers EN VIVO, sin mantener ninguna base de datos
    propia de nombres de empresas: usa el buscador público de Yahoo Finance.
    Devuelve una lista de tuplas (símbolo, nombre, tipo) con las mejores
    coincidencias para lo que el usuario escribió."""
    if not consulta or len(consulta.strip()) < 2:
        return []
    try:
        resp = requests.get(
            "https://query1.finance.yahoo.com/v1/finance/search",
            params={"q": consulta, "quotesCount": 6, "newsCount": 0},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=5,
        )
        if resp.status_code != 200:
            return []
        quotes = resp.json().get("quotes", [])
        sugerencias = []
        for q in quotes:
            simbolo = q.get("symbol")
            nombre = q.get("shortname") or q.get("longname") or simbolo
            tipo = q.get("quoteType", "")
            if simbolo:
                sugerencias.append((simbolo, nombre, tipo))
        return sugerencias
    except Exception:
        return []


@st.cache_data(ttl=1800, show_spinner=False, max_entries=200)
def obtener_datos_accion_optimizado(ticker):
    """Obtiene datos de acciones optimizado para paralelismo"""
    try:
        data = yf.download(ticker, period="6mo", progress=False, interval="1d")
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        return data
    except:
        return pd.DataFrame()


@st.cache_data(ttl=3600, show_spinner=False, max_entries=100)
def obtener_info_completa_optimizada(ticker):
    """Obtiene información completa optimizada"""
    try:
        return yf.Ticker(ticker).info
    except:
        return {}


@st.cache_data(ttl=3600, show_spinner=False, max_entries=100)  # 1 hora, sin spinner, 100 entradas
def obtener_datos_accion(ticker):
    """Obtiene datos de acciones con caching extendido"""
    try:
        data = yf.download(ticker, period="1y", progress=False, interval="1d")
        # yfinance reciente devuelve columnas MultiIndex (ej. ('Close','MSFT'))
        # incluso para una sola acción; las aplanamos a 'Close', 'Open', etc.
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        return data
    except:
        return pd.DataFrame()


@st.cache_data(ttl=7200, show_spinner=False, max_entries=50)  # 2 horas para info que cambia poco
def obtener_info_completa(ticker):
    """Obtiene información completa con caching extendido"""
    try:
        return yf.Ticker(ticker).info
    except:
        return {}


@st.cache_data(ttl=300, show_spinner=False, max_entries=20)  # 5 minutos para datos en tiempo real
def obtener_datos_tiempo_real(ticker):
    """Datos en tiempo real con caching corto"""
    try:
        ticker_obj = yf.Ticker(ticker)
        info = ticker_obj.info
        hist = ticker_obj.history(period="2d")
        
        if not hist.empty and len(hist) >= 2:
            current = hist['Close'].iloc[-1]
            previous = hist['Close'].iloc[-2] 
            change = ((current - previous) / previous) * 100
            
            return {
                'precio_actual': current,
                'cambio_porcentaje': change,
                'volumen': hist['Volume'].iloc[-1] if 'Volume' in hist.columns else 0
            }
    except:
        return None

# Nota: aquí vivían antes `precalcular_datos_screener()` (sin argumentos),
# `obtener_datos_sp500_completo()`, `cargar_accion_paralelo`,
# `cargar_sp500_paralelo`, `buscar_simbolos_sp500_rapido` y
# `aplicar_filtros_rapidos`. Se eliminaron porque eran código muerto: nada
# en la app los llamaba (el Screener real usa su propia versión, definida
# dentro de vistas/screener.py). Una de ellas (`cargar_sp500_paralelo`)
# era justamente la que traía la lista fija de solo 20 acciones que
# generaba confusión — por eso el Screener real nunca estuvo limitado a 20,
# aunque lo pareciera.
