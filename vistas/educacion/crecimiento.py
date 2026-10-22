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


def mostrar_crecimiento(stonk, ticker, info, nombre, descripcion, start_date, end_date):
            st.subheader("📈 CRECIMIENTO - 8 Métricas")
            
            metricas = {
                "Sales Growth 5Y": {
                    "definicion": "**Crecimiento de Ventas 5 Años** - Tasa crecimiento anual compuesto",
                    "calculacion": "(Ventas año actual ÷ Ventas año base)^(1/5) - 1",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **<5%**: Crecimiento lento (madurez)
                    - **5-15%**: Crecimiento moderado
                    - **>15%**: Crecimiento rápido
                    - **Negativo**: Contracción
                    
                    **Ventajas:**
                    - Muestra tendencia de largo plazo
                    - Menos volátil que anual
                    - Buen indicador de momentum
                    
                    **Desventajas:**
                    - Puede enmascarar cambios recientes
                    - Sensible al año base elegido
                    - No considera adquisiciones orgánicas vs inorgánicas
                    
                    **¿Para qué sirve?**
                    - Evaluar trayectoria histórica
                    - Comparar con expectativas futuras
                    - Análisis de madurez del negocio
                    """,
                    "ejemplo": "Ventas crecieron de $200M a $400M en 5 años → 15% CAGR"
                },
                
                "EPS Growth 5Y": {
                    "definicion": "**Crecimiento EPS 5 Años** - Tasa crecimiento ganancias por acción",
                    "calculacion": "(EPS año actual ÷ EPS año base)^(1/5) - 1",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Consistente >10%**: Empresa growth de calidad
                    - **Volátil**: Resultados inconsistentes
                    - **Decreciente**: Posible saturación o problemas
                    
                    **Ventajas:**
                    - Enfocado en valor por acción
                    - Considera efecto de recompras
                    - Mejor que crecimiento de beneficio neto
                    
                    **Desventajas:**
                    - Puede ser afectado por eventos extraordinarios
                    - Sensible a cambios en número de acciones
                    - No considera calidad de ganancias
                    
                    **¿Para qué sirve?**
                    - Evaluar creación de valor histórico
                    - Calcular PEG ratio
                    - Proyectar crecimiento futuro
                    """,
                    "ejemplo": "EPS creció de $2 a $4 en 5 años → 15% CAGR"
                },
                
                "Sales Growth Q/Q": {
                    "definicion": "**Crecimiento Ventas Trimestral** - Cambio vs trimestre anterior",
                    "calculacion": "(Ventas Q actual - Ventas Q anterior) ÷ Ventas Q anterior × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Positivo**: Momentum positivo
                    - **Negativo**: Desaceleración
                    - **Aceleración**: Crecimiento cada vez más rápido
                    - **Desaceleración**: Pérdida de momentum
                    
                    **Ventajas:**
                    - Muestra momentum reciente
                    - Sensible a cambios en el negocio
                    - Útil para trading
                    
                    **Desventajas:**
                    - Muy volátil
                    - Sensible a estacionalidad
                    - Puede estar distorsionado por eventos únicos
                    
                    **¿Para qué sirve?**
                    - Evaluar performance reciente
                    - Identificar cambios en tendencia
                    - Timing de decisiones de inversión
                    """,
                    "ejemplo": "Ventas Q1 $250M, Q2 $275M → Crecimiento 10%"
                },
                
                "EPS Growth Q/Q": {
                    "definicion": "**Crecimiento EPS Trimestral** - Cambio ganancias vs trimestre anterior",
                    "calculacion": "(EPS Q actual - EPS Q anterior) ÷ EPS Q anterior × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Beat estimates**: Supera expectativas (positivo)
                    - **Miss estimates**: No alcanza expectativas (negativo)
                    - **Guide higher**: Aumenta guidance (muy positivo)
                    
                    **Ventajas:**
                    - Muestra momentum reciente de ganancias
                    - Muy seguido por el mercado
                    - Bueno para estrategias de earnings
                    
                    **Desventajas:**
                    - Extremadamente volátil
                    - Sensible a estacionalidad
                    - Las estimaciones pueden ser erróneas
                    
                    **¿Para qué sirve?**
                    - Evaluar resultados trimestrales
                    - Identificar sorpresas de ganancias
                    - Trading alrededor de earnings
                    """,
                    "ejemplo": "EPS Q1 $1.20, Q2 $1.35 → Crecimiento 12.5%"
                },
                
                "Sales Growth Y/Y": {
                    "definicion": "**Crecimiento Ventas Interanual** - Cambio vs mismo periodo año anterior",
                    "calculacion": "(Ventas periodo actual - Ventas mismo periodo año anterior) ÷ Ventas año anterior × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Elimina estacionalidad**: Mejor comparación que Q/Q
                    - **Tendencia real**: Muestra crecimiento subyacente
                    - **Comparable**: Mismo periodo estacional
                    
                    **Ventajas:**
                    - Elimina efecto estacional
                    - Mejor indicador de tendencia
                    - Ampliamente utilizado
                    
                    **Desventajas:**
                    - Puede enmascarar cambios recientes
                    - Menos frecuente que Q/Q
                    - Sensible a eventos únicos anuales
                    
                    **¿Para qué sirve?**
                    - Evaluar crecimiento real
                    - Comparar performance anual
                    - Análisis de tendencias fundamentales
                    """,
                    "ejemplo": "Ventas Q2 2024 $300M, Q2 2023 $250M → Crecimiento 20%"
                },
                
                "EPS Growth Y/Y": {
                    "definicion": "**Crecimiento EPS Interanual** - Cambio ganancias vs mismo periodo año anterior",
                    "calculacion": "(EPS periodo actual - EPS mismo periodo año anterior) ÷ EPS año anterior × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Crecimiento orgánico**: Mejora en operaciones
                    - **Decrecimiento**: Problemas operativos o comparación difícil
                    - **Consistencia**: Crecimiento sostenido es positivo
                    
                    **Ventajas:**
                    - Elimina estacionalidad
                    - Mejor indicador de tendencia de ganancias
                    - Menos volátil que Q/Q
                    
                    **Desventajas:**
                    - Puede estar afectado por eventos únicos
                    - No considera cambios recientes
                    - Sensible a base de comparación
                    
                    **¿Para qué sirve?**
                    - Evaluar crecimiento real de ganancias
                    - Comparar con expectativas
                    - Análisis de calidad de crecimiento
                    """,
                    "ejemplo": "EPS Q2 2024 $1.50, Q2 2023 $1.25 → Crecimiento 20%"
                },
                
                "Revenue Growth (ttm)": {
                    "definicion": "**Crecimiento de Ingresos últimos 12 meses** - Cambio vs mismo periodo anterior",
                    "calculacion": "(Ventas ttm - Ventas ttm año anterior) ÷ Ventas ttm año anterior × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Muestra tendencia**: Crecimiento en los últimos 12 meses
                    - **Menos volátil**: Que trimestral
                    - **Visión actualizada**: Pero con perspectiva
                    
                    **Ventajas:**
                    - Combina actualidad con estabilidad
                    - Menos volátil que trimestral
                    - Bueno para análisis fundamental
                    
                    **Desventajas:**
                    - Puede enmascarar cambios recientes
                    - Menos frecuente que trimestral
                    - Sensible a eventos pasados
                    
                    **¿Para qué sirve?**
                    - Evaluar crecimiento reciente con perspectiva
                    - Comparar con competidores
                    - Análisis de momentum fundamental
                    """,
                    "ejemplo": "Ventas ttm $1.2B, ttm año anterior $1.0B → Crecimiento 20%"
                },
                
                "EPS Growth (ttm)": {
                    "definicion": "**Crecimiento EPS últimos 12 meses** - Cambio ganancias vs mismo periodo anterior",
                    "calculacion": "(EPS ttm - EPS ttm año anterior) ÷ EPS ttm año anterior × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Crecimiento sostenido**: Positivo para valoración
                    - **Volátil**: Resultados inconsistentes
                    - **Decreciente**: Posibles problemas
                    
                    **Ventajas:**
                    - Visión actualizada con perspectiva
                    - Menos volátil que trimestral
                    - Bueno para análisis de valoración
                    
                    **Desventajas:**
                    - Puede estar afectado por eventos pasados
                    - Menos frecuente que trimestral
                    - Sensible a base de comparación
                    
                    **¿Para qué sirve?**
                    - Evaluar crecimiento reciente de ganancias
                    - Calcular ratios de crecimiento
                    - Análisis fundamental para inversión
                    """,
                    "ejemplo": "EPS ttm $5.00, ttm año anterior $4.00 → Crecimiento 25%"
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

