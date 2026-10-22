"""
Módulo generado automáticamente a partir de App.py original.
Importa todo lo común desde config para no repetir imports en cada módulo.
"""
from config import *


def _pct_fmp(x):
    try:
        return f"{float(x) * 100:.2f}%"
    except (TypeError, ValueError):
        return None


def _num_fmp(x, decimales=2):
    try:
        return f"{float(x):.{decimales}f}"
    except (TypeError, ValueError):
        return None


def _grande_fmp(x):
    try:
        x = float(x)
        for unidad, div in [("T", 1e12), ("B", 1e9), ("M", 1e6), ("K", 1e3)]:
            if abs(x) >= div:
                return f"{x / div:.2f}{unidad}"
        return f"{x:.2f}"
    except (TypeError, ValueError):
        return None


@st.cache_data(ttl=21600, show_spinner=False)  # 6 horas: son datos que cambian poco (trimestrales)
def obtener_metricas_fmp(ticker):
    """Métricas fundamentales desde Financial Modeling Prep.

    Esta es ahora la FUENTE PRINCIPAL de 'Métricas Fundamentales Principales'
    (antes era Finviz, vía scraping). Si FMP no tiene la llave configurada, o
    la petición falla, devuelve un diccionario vacío y quien llama sigue con
    Finviz y luego Yahoo Finance como respaldo — la app no se detiene.
    """
    if not FMP:
        return {}

    ratios, metricas, cotizacion = {}, {}, {}
    try:
        r = requests.get(
            f"https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker}?apikey={FMP}",
            timeout=8,
        )
        if r.status_code == 200 and r.json():
            ratios = r.json()[0]
    except Exception:
        pass

    try:
        r = requests.get(
            f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{ticker}?apikey={FMP}",
            timeout=8,
        )
        if r.status_code == 200 and r.json():
            metricas = r.json()[0]
    except Exception:
        pass

    try:
        r = requests.get(
            f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={FMP}",
            timeout=8,
        )
        if r.status_code == 200 and r.json():
            cotizacion = r.json()[0]
    except Exception:
        pass

    if not (ratios or metricas or cotizacion):
        return {}

    campos = {
        "Market Cap": _grande_fmp(cotizacion.get("marketCap")),
        "P/E": _num_fmp(cotizacion.get("pe") or ratios.get("peRatioTTM")),
        "PEG": _num_fmp(ratios.get("pegRatioTTM")),
        "P/FCF": _num_fmp(ratios.get("priceToFreeCashFlowsRatioTTM")),
        "EV/EBITDA": _num_fmp(metricas.get("evToEbitdaTTM")),
        "EV/SALES": _num_fmp(metricas.get("evToSalesTTM")),
        "Gross Margin": _pct_fmp(ratios.get("grossProfitMarginTTM")),
        "Oper. Margin": _pct_fmp(ratios.get("operatingProfitMarginTTM")),
        "Profit Margin": _pct_fmp(ratios.get("netProfitMarginTTM")),
        "Cash/Share": _num_fmp(metricas.get("cashPerShareTTM")),
        "Debt/Eq": _num_fmp(ratios.get("debtEquityRatioTTM")),
        "ROA": _pct_fmp(ratios.get("returnOnAssetsTTM")),
        "ROE": _pct_fmp(ratios.get("returnOnEquityTTM")),
        "Beta": _num_fmp(cotizacion.get("beta")),
        "Volume": _grande_fmp(cotizacion.get("volume")),
    }
    # Solo devolvemos las que sí vinieron con un valor real
    return {k: v for k, v in campos.items() if v is not None}
