"""
Módulo generado automáticamente a partir de App.py original.
Importa todo lo común desde config para no repetir imports en cada módulo.
"""
from config import *


@st.cache_data(ttl=300, show_spinner=False)  # 5 min: acelera sin perder frescura (cambia seguido)
def obtener_rating_analistas(ticker):
    """Rating de analistas - sin caching extenso porque cambia frecuentemente"""
    try:
        ticker_obj = yf.Ticker(ticker)
        info = ticker_obj.info
        
        ratings = {
            'recommendationMean': info.get('recommendationMean', 'N/A'),
            'recommendationKey': info.get('recommendationKey', 'N/A'),
            'targetMeanPrice': info.get('targetMeanPrice', 'N/A'), 
            'numberOfAnalystOpinions': info.get('numberOfAnalystOpinions', 'N/A')
        }
        return ratings
    except:
        return {}
