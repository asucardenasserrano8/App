"""
Módulo generado automáticamente a partir de App.py original.
Importa todo lo común desde config para no repetir imports en cada módulo.
"""
from config import *
from nucleo.errores import mostrar_error_amigable


@st.cache_data(ttl=3600, show_spinner=False)  # 1 hora: evita recalcular los mismos indicadores
def calcular_indicadores_tecnicos(data):
    if data.empty:
        return data
    
    # Crear una copia para no modificar el original
    data_tech = data.copy()
    
    # Asegurarnos de que tenemos la columna Close
    if 'Close' not in data_tech.columns:
        st.error("No se encuentra la columna 'Close' en los datos")
        return data_tech
    
    try:
        # RSI
        delta = data_tech['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data_tech['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp12 = data_tech['Close'].ewm(span=12, adjust=False).mean()
        exp26 = data_tech['Close'].ewm(span=26, adjust=False).mean()
        data_tech['MACD'] = exp12 - exp26
        data_tech['MACD_Signal'] = data_tech['MACD'].ewm(span=9, adjust=False).mean()
        data_tech['MACD_Histogram'] = data_tech['MACD'] - data_tech['MACD_Signal']
        
        # Bandas de Bollinger
        data_tech['BB_Middle'] = data_tech['Close'].rolling(window=20).mean()
        bb_std = data_tech['Close'].rolling(window=20).std()
        data_tech['BB_Upper'] = data_tech['BB_Middle'] + (bb_std * 2)
        data_tech['BB_Lower'] = data_tech['BB_Middle'] - (bb_std * 2)
        
        # Medias Móviles
        data_tech['SMA_20'] = data_tech['Close'].rolling(window=20).mean()
        data_tech['SMA_50'] = data_tech['Close'].rolling(window=50).mean()
        data_tech['SMA_200'] = data_tech['Close'].rolling(window=200).mean()
        
        return data_tech
        
    except Exception as e:
        mostrar_error_amigable(e, "el cálculo de indicadores técnicos")
        return data_tech


def analizar_tendencias(data):
    if data.empty or 'Close' not in data.columns:
        return {"tendencia": "No disponible", "confianza": 0, "detalles": {}}
    
    try:
        # Calcular medias móviles
        data['SMA_20'] = data['Close'].rolling(window=20).mean()
        data['SMA_50'] = data['Close'].rolling(window=50).mean()
        data['SMA_200'] = data['Close'].rolling(window=200).mean()
        
        # Obtener últimos valores
        precio_actual = data['Close'].iloc[-1]
        sma_20 = data['SMA_20'].iloc[-1]
        sma_50 = data['SMA_50'].iloc[-1]
        sma_200 = data['SMA_200'].iloc[-1]
        
        # Calcular RSI para momentum
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        rsi_actual = rsi.iloc[-1]
        
        # Análisis de tendencia
        tendencia_alcista = 0
        tendencia_bajista = 0
        
        # 1. Análisis de medias móviles (40%)
        if precio_actual > sma_20 > sma_50 > sma_200:
            tendencia_alcista += 40
        elif precio_actual < sma_20 < sma_50 < sma_200:
            tendencia_bajista += 40
        
        # 2. Posición respecto a medias (30%)
        if precio_actual > sma_20:
            tendencia_alcista += 15
        else:
            tendencia_bajista += 15
            
        if precio_actual > sma_50:
            tendencia_alcista += 10
        else:
            tendencia_bajista += 10
            
        if precio_actual > sma_200:
            tendencia_alcista += 5
        else:
            tendencia_bajista += 5
        
        # 3. Momentum RSI (30%)
        if rsi_actual > 50:
            tendencia_alcista += 30
        else:
            tendencia_bajista += 30
        
        # Determinar tendencia principal
        if tendencia_alcista > tendencia_bajista:
            tendencia = "ALCISTA"
            confianza = min(100, tendencia_alcista)
        elif tendencia_bajista > tendencia_alcista:
            tendencia = "BAJISTA"
            confianza = min(100, tendencia_bajista)
        else:
            tendencia = "LATERAL"
            confianza = 50
        
        detalles = {
            "precio_actual": precio_actual,
            "sma_20": sma_20,
            "sma_50": sma_50,
            "sma_200": sma_200,
            "rsi": rsi_actual,
            "puntos_alcista": tendencia_alcista,
            "puntos_bajista": tendencia_bajista
        }
        
        return {
            "tendencia": tendencia,
            "confianza": confianza,
            "detalles": detalles
        }
        
    except Exception as e:
        return {"tendencia": "Error en análisis", "confianza": 0, "detalles": {}}
