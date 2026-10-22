"""
Módulo generado automáticamente a partir de App.py original.
Importa todo lo común desde config para no repetir imports en cada módulo.
"""
from config import *


def calcular_scoring_fundamental(info):
    score = 0
    max_score = 100
    metricas = {}
    
    # P/E Ratio (15 puntos)
    pe = info.get('trailingPE', 0)
    if pe and pe > 0:
        if pe < 15:
            score += 15
            metricas['P/E'] = '🟢 Excelente'
        elif pe < 25:
            score += 10
            metricas['P/E'] = '🟡 Bueno'
        else:
            score += 5
            metricas['P/E'] = '🔴 Alto'
    
    # ROE (15 puntos)
    roe = info.get('returnOnEquity', 0)
    if roe and roe > 0:
        if roe > 0.15:
            score += 15
            metricas['ROE'] = '🟢 Excelente'
        elif roe > 0.08:
            score += 10
            metricas['ROE'] = '🟡 Bueno'
        else:
            score += 5
            metricas['ROE'] = '🔴 Bajo'
    
    # Deuda/Equity (15 puntos)
    deuda_eq = info.get('debtToEquity', 0)
    if deuda_eq and deuda_eq > 0:
        if deuda_eq < 0.5:
            score += 15
            metricas['Deuda/Equity'] = '🟢 Excelente'
        elif deuda_eq < 1.0:
            score += 10
            metricas['Deuda/Equity'] = '🟡 Bueno'
        else:
            score += 5
            metricas['Deuda/Equity'] = '🔴 Alto'
    
    # Margen Beneficio (15 puntos)
    margen = info.get('profitMargins', 0)
    if margen and margen > 0:
        if margen > 0.2:
            score += 15
            metricas['Margen Beneficio'] = '🟢 Excelente'
        elif margen > 0.1:
            score += 10
            metricas['Margen Beneficio'] = '🟡 Bueno'
        else:
            score += 5
            metricas['Margen Beneficio'] = '🔴 Bajo'
    
    # Crecimiento Ingresos (20 puntos)
    crecimiento = info.get('revenueGrowth', 0)
    if crecimiento and crecimiento > 0:
        if crecimiento > 0.15:
            score += 20
            metricas['Crecimiento Ingresos'] = '🟢 Excelente'
        elif crecimiento > 0.08:
            score += 15
            metricas['Crecimiento Ingresos'] = '🟡 Bueno'
        else:
            score += 8
            metricas['Crecimiento Ingresos'] = '🔴 Bajo'
    
    # Rating Analistas (20 puntos)
    rating_mean = info.get('recommendationMean', 3)
    if rating_mean and rating_mean > 0:
        if rating_mean < 2:
            score += 20
            metricas['Rating Analistas'] = '🟢 Fuerte Compra'
        elif rating_mean < 3:
            score += 15
            metricas['Rating Analistas'] = '🟡 Compra'
        else:
            score += 8
            metricas['Rating Analistas'] = '🔴 Neutral/Venta'
    
    return min(score, max_score), metricas


def generar_reporte_texto(ticker, info, datos, scoring, metricas):
    try:
        # Información básica
        nombre = info.get('longName', 'N/A')
        sector = info.get('sector', 'N/A')
        industria = info.get('industry', 'N/A')
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Construir el reporte paso a paso
        reporte = f"REPORTE DE ANÁLISIS: {ticker}\n"
        reporte += f"Generado: {fecha_actual}\n\n"
        
        reporte += "INFORMACIÓN BÁSICA:\n"
        reporte += f"- Nombre: {nombre}\n"
        reporte += f"- Sector: {sector}\n"
        reporte += f"- Industria: {industria}\n\n"
        
        reporte += f"SCORING FUNDAMENTAL: {scoring}/100\n\n"
        
        reporte += "MÉTRICAS:\n"
        for metrica, valor in metricas.items():
            reporte += f"- {metrica}: {valor}\n"
        
        # Datos de precio con verificación robusta
        if not datos.empty and 'Close' in datos.columns and len(datos) > 0:
            try:
                precio_actual_val = float(datos['Close'].iloc[-1])
                precio_min_val = float(datos['Close'].min())
                precio_max_val = float(datos['Close'].max())
                
                reporte += "\nDATOS DE PRECIO:\n"
                reporte += f"- Precio Actual: ${precio_actual_val:.2f}\n"
                reporte += f"- Precio Mínimo (1 año): ${precio_min_val:.2f}\n"
                reporte += f"- Precio Máximo (1 año): ${precio_max_val:.2f}\n"
            except (ValueError, IndexError, KeyError) as e:
                reporte += f"\nERROR en datos de precio: {str(e)}\n"
        else:
            reporte += "\nDATOS DE PRECIO: No disponibles\n"
        
        return reporte
        
    except Exception as e:
        return f"Error generando reporte: {str(e)}"
