"""
Módulo generado automáticamente al dividir educacion_financiera.py por
categoría (antes eran ~2,700 líneas en un solo archivo).
"""
from config import *

from nucleo.datos import *
from nucleo.tecnico import *
from nucleo.riesgo import *
from nucleo.scoring import *
from nucleo.wikipedia_info import *
from nucleo.ratings import *


def mostrar_indicadores_tecnicos_edu(stonk, ticker, info, nombre, descripcion, start_date, end_date):
            st.subheader("📊 INDICADORES TÉCNICOS - 10 Métricas")
            
            metricas = {
                "Beta": {
                    "definicion": "**Volatilidad vs Mercado** - Sensibilidad de la acción vs benchmark",
                    "calculacion": "Covarianza(Acción, Mercado) ÷ Varianza(Mercado)",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **<0.8**: Defensivo (menos volátil que mercado)
                    - **0.8-1.2**: Neutral (similar volatilidad)
                    - **>1.2**: Agresivo (más volátil que mercado)
                    - **Negativo**: Se mueve en dirección opuesta (raro)
                    
                    **Ventajas:**
                    - Mide riesgo sistemático
                    - Útil para construcción de carteras
                    - Base para modelo CAPM
                    
                    **Desventajas:**
                    - Basado en datos históricos
                    - Asume distribuciones normales
                    - Puede cambiar con el tiempo
                    
                    **¿Para qué sirve?**
                    - Evaluar riesgo vs recompensa esperada
                    - Construcción de carteras diversificadas
                    - Cálculo de costo de capital
                    """,
                    "ejemplo": "Beta 1.5: si mercado ±10%, acción ±15% en promedio"
                },
                
                "RSI (14)": {
                    "definicion": "**Índice de Fuerza Relativa** - Oscilador de momentum",
                    "calculacion": "100 - (100 ÷ (1 + (Ganancia promedio ÷ Pérdida promedio)))",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **>70**: Sobrecomprado (posible corrección)
                    - **<30**: Sobrevendido (posible rebote)
                    - **50**: Neutral
                    - **Divergencias**: Señales fuertes
                    
                    **Ventajas:**
                    - Identifica condiciones extremas
                    - Fácil de interpretar
                    - Ampliamente seguido
                    
                    **Desventajas:**
                    - Puede dar señales prematuras en tendencias fuertes
                    - Menos efectivo en mercados laterales
                    - Parámetro dependiente (14 períodos típico)
                    
                    **¿Para qué sirve?**
                    - Identificar puntos de entrada/salida
                    - Confirmar momentum
                    - Detectar posibles reversiones
                    """,
                    "ejemplo": "RSI 75 → condición sobrecomprada, posible corrección"
                },
                
                "Volatility": {
                    "definicion": "**Volatilidad** - Desviación estándar de rendimientos",
                    "calculacion": "Desviación estándar(rendimientos diarios) × √252",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **<20%**: Baja volatilidad (estable)
                    - **20-40%**: Volatilidad media
                    - **>40%**: Alta volatilidad (riesgosa)
                    - **>80%**: Extremadamente volátil
                    
                    **Ventajas:**
                    - Mide riesgo total
                    - Base para muchos modelos
                    - Fácil de comparar
                    
                    **Desventajas:**
                    - Asume distribuciones normales
                    - No diferencia entre riesgo arriba/abajo
                    - Basado en histórico
                    
                    **¿Para qué sirve?**
                    - Evaluar riesgo de la inversión
                    - Dimensionar posiciones
                    - Comparar con rendimiento esperado
                    """,
                    "ejemplo": "Volatilidad 30% → movimientos típicos de ±30% anuales"
                },
                
                "ATR": {
                    "definicion": "**Average True Range** - Volatilidad basada en rangos de trading",
                    "calculacion": "Media móvil de True Range (máx(alto-bajo, |alto-cierre anterior|, |bajo-cierre anterior|))",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Alto**: Alta volatilidad intradía
                    - **Bajo**: Baja volatilidad intradía
                    - **Creciente**: Aumento volatilidad
                    - **Decreciente**: Disminución volatilidad
                    
                    **Ventajas:**
                    - Considera gaps de precios
                    - Mejor que volatilidad basada solo en cierres
                    - Útil para stops y targets
                    
                    **Desventajas:**
                    - No direccional
                    - Depende del período elegido
                    - Menos conocido que volatilidad estándar
                    
                    **¿Para qué sirve?**
                    - Colocar stops loss dinámicos
                    - Evaluar condiciones de trading
                    - Gestión de riesgo intradía
                    """,
                    "ejemplo": "ATR $2.50 → movimiento intradía típico de $2.50"
                },
                
                "SMA 20": {
                    "definicion": "**Media Móvil Simple 20 días** - Tendencia corto plazo",
                    "calculacion": "Suma últimos 20 cierres ÷ 20",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Precio > SMA**: Tendencia alcista
                    - **Precio < SMA**: Tendencia bajista
                    - **Cruces**: Posibles cambios de tendencia
                    - **Soporte/Resistencia**: Niveles importantes
                    
                    **Ventajas:**
                    - Suaviza el ruido
                    - Fácil de calcular e interpretar
                    - Ampliamente usado
                    
                    **Desventajas:**
                    - Retraso (lagging indicator)
                    - Menos efectivo en mercados laterales
                    - Parámetro dependiente
                    
                    **¿Para qué sirve?**
                    - Identificar tendencias
                    - Señales de compra/venta
                    - Niveles de soporte/resistencia
                    """,
                    "ejemplo": "Precio $105, SMA20 $100 → tendencia alcista corto plazo"
                },
                
                "SMA 50": {
                    "definicion": "**Media Móvil Simple 50 días** - Tendencia medio plazo",
                    "calculacion": "Suma últimos 50 cierres ÷ 50",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Tendencia intermedia**: Más suave que SMA20
                    - **Cruces con SMA20**: Señales de momentum
                    - **Soporte/Resistencia**: Niveles más fuertes
                    
                    **Ventajas:**
                    - Menos ruido que SMA20
                    - Mejor para tendencias intermedias
                    - Menos señales falsas
                    
                    **Desventajas:**
                    - Más retraso que SMA20
                    - Puede perder movimientos rápidos
                    - Parámetro fijo
                    
                    **¿Para qué sirve?**
                    - Confirmar tendencias
                    - Filtrar señales de corto plazo
                    - Análisis de momentum intermedio
                    """,
                    "ejemplo": "SMA20 > SMA50 → momentum alcista confirmado"
                },
                
                "SMA 200": {
                    "definicion": "**Media Móvil Simple 200 días** - Tendencia largo plazo",
                    "calculacion": "Suma últimos 200 cierres ÷ 200",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Tendencia principal**: Bull market vs Bear market
                    - **Soporte/Resistencia mayor**: Nivel muy importante
                    - **Golden Cross/Death Cross**: Señales mayores
                    
                    **Ventajas:**
                    - Define tendencia principal
                    - Muy seguido por instituciones
                    - Señales fuertes y confiables
                    
                    **Desventajas:**
                    - Mucho retraso
                    - Puede perder grandes movimientos
                    - Menos útil para trading corto
                    
                    **¿Para qué sirve?**
                    - Determinar tendencia principal
                    - Señales de inversión (no trading)
                    - Análisis de largo plazo
                    """,
                    "ejemplo": "Precio > SMA200 → tendencia alcista principal"
                },
                
                "Volume": {
                    "definicion": "**Volumen** - Acciones negociadas en el período",
                    "calculacion": "Número total de acciones negociadas",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Alto volumen**: Confirmación de movimiento
                    - **Bajo volumen**: Falta de convicción
                    - **Volume spikes**: Eventos importantes
                    - **Divergencias**: Señales de debilidad
                    
                    **Ventajas:**
                    - Confirma price action
                    - Indica interés institucional
                    - Detecta acumulación/distribución
                    
                    **Desventajas:**
                    - No da señales por sí solo
                    - Puede ser manipulado en acciones pequeñas
                    - Varía por liquidez de la acción
                    
                    **¿Para qué sirve?**
                    - Confirmar rupturas de soporte/resistencia
                    - Detectar interés institucional
                    - Identificar posibles reversiones
                    """,
                    "ejemplo": "Ruptura con alto volumen → señal más confiable"
                },
                
                "Avg Volume": {
                    "definicion": "**Volumen Promedio** - Volumen medio histórico",
                    "calculacion": "Media volumen últimos 20-30 días",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Volume > Avg**: Interés inusual
                    - **Volume < Avg**: Poco interés
                    - **Cambios en avg volume**: Cambio en liquidez/perfil
                    
                    **Ventajas:**
                    - Proporciona contexto
                    - Detecta anomalías
                    - Útil para screening
                    
                    **Desventajas:**
                    - Basado en histórico
                    - Puede cambiar estructuralmente
                    - No considera eventos conocidos
                    
                    **¿Para qué sirve?**
                    - Evaluar liquidez relativa
                    - Detectar interés inusual
                    - Filtrar acciones por liquidez
                    """,
                    "ejemplo": "Volume actual 2M, Avg Volume 1M → interés inusual"
                },
                
                "Rel Volume": {
                    "definicion": "**Volumen Relativo** - Volumen actual vs promedio",
                    "calculacion": "Volume actual ÷ Avg Volume",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **<0.5**: Muy bajo volumen
                    - **0.5-1.5**: Volumen normal
                    - **1.5-3.0**: Alto volumen
                    - **>3.0**: Volumen muy alto
                    
                    **Ventajas:**
                    - Normalizado y comparable
                    - Fácil de interpretar
                    - Bueno para screening
                    
                    **Desventajas:**
                    - Depende del período de avg volume
                    - Puede dar falsas señales en eventos conocidos
                    - No considera dirección del movimiento
                    
                    **¿Para qué sirve?**
                    - Identificar acciones con volumen inusual
                    - Detectar acumulación/distribución
                    - Screening para oportunidades
                    """,
                    "ejemplo": "Rel Volume 2.5 → volumen 2.5x el normal, interés inusual"
                }
            }
            
            for metrica, detalles in metricas.items():
                with st.expander(f"**{metrica}**"):
                    st.write(f"**📖 DEFINICIÓN:** {detalles['definicion']}")
                    st.write(f"**🧮 CÁLCULO:** {detalles['calculacion']}")
                    st.markdown("**📊 INTERPRETACIÓN DETALLADA:**")
                    st.write(detalles['interpretacion'])
                    if 'ejemplo' in detalles:
                        st.info(f"**🔢 EJEMPLO:** {detalles['ejemplo']}")

