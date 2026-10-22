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


def mostrar_datos_corporativos(stonk, ticker, info, nombre, descripcion, start_date, end_date):
            st.subheader("🏢 DATOS CORPORATIVOS - 8 Métricas")
            
            metricas = {
                "Shares Out": {
                    "definicion": "**Acciones en Circulación** - Número total de acciones emitidas",
                    "calculacion": "Acciones comunes emitidas - Acciones en tesorería",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Creciente**: Dilución (emisiones)
                    - **Decreciente**: Recompra de acciones
                    - **Estable**: Política conservadora
                    
                    **Ventajas:**
                    - Base para cálculo por acción
                    - Muestra política de capital
                    - Afecta valoración
                    
                    **Desventajas:**
                    - No considera clases diferentes
                    - Puede incluir acciones restringidas
                    - No muestra float real
                    
                    **¿Para qué sirve?**
                    - Calcular market cap
                    - Evaluar políticas de capital
                    - Analizar dilución/recompra
                    """,
                    "ejemplo": "10 millones de acciones en circulación"
                },
                
                "Float": {
                    "definicion": "**Acciones Flotantes** - Acciones disponibles para trading público",
                    "calculacion": "Shares Out - Acciones restringidas (insiders, control)",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Float pequeño**: Alta volatilidad posible
                    - **Float grande**: Más liquidez
                    - **Float vs Shares Out**: Grado de control insider
                    
                    **Ventajas:**
                    - Mejor indicador de liquidez real
                    - Muestra concentración de propiedad
                    - Útil para análisis técnico
                    
                    **Desventajas:**
                    - Los datos pueden ser estimados
                    - Puede cambiar con el tiempo
                    - No considera bloqueos regulatorios
                    
                    **¿Para qué sirve?**
                    - Evaluar liquidez real
                    - Analizar riesgo de manipulación
                    - Gestión de tamaño de posición
                    """,
                    "ejemplo": "Shares Out 10M, Float 8M → 80% disponible para trading"
                },
                
                "Insider Own": {
                    "definicion": "**Propiedad Insider** - % acciones poseídas por directivos y consejo",
                    "calculacion": "Acciones de insiders ÷ Shares Out × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Alto (>10%)**: Alineación con accionistas
                    - **Bajo (<5%)**: Posible falta de alineación
                    - **Muy alto (>30%)**: Control concentrado
                    
                    **Ventajas:**
                    - Mide alineación de intereses
                    - Buen predictor de performance
                    - Refleja confianza del management
                    
                    **Desventajas:**
                    - No considera tipos de acciones
                    - Puede incluir holdings pasivos
                    - Datos con retraso
                    
                    **¿Para qué sirve?**
                    - Evaluar gobierno corporativo
                    - Analizar alineación de intereses
                    - Detectar posibles conflictos
                    """,
                    "ejemplo": "Insiders poseen 15% de las acciones → buena alineación"
                },
                
                "Insider Trans": {
                    "definicion": "**Transacciones Insider** - Compras y ventas de directivos",
                    "calculacion": "Net buying/selling de insiders en período",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Net buying**: Confianza en el futuro
                    - **Net selling**: Puede ser normal (diversificación) o preocupante
                    - **Patrones**: Compras consistentes son muy positivas
                    
                    **Ventajas:**
                    - Información privilegiada (legal)
                    - Muy seguido por el mercado
                    - Buen predictor de performance
                    
                    **Desventajas:**
                    - Las ventas pueden ser por razones personales
                    - Datos con retraso (form 4)
                    - Puede ser manipulado con timing
                    
                    **¿Para qué sirve?**
                    - Confirmar tesis de inversión
                    - Detectar posibles problemas
                    - Señales de confianza del management
                    """,
                    "ejemplo": "CEO compró 50,000 acciones → señal muy positiva"
                },
                
                "Inst Own": {
                    "definicion": "**Propiedad Institucional** - % acciones poseídas por fondos e instituciones",
                    "calculacion": "Acciones de instituciones ÷ Shares Out × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Alto (>60%)**: Aprobación institucional
                    - **Bajo (<30%)**: Poco seguimiento institucional
                    - **Creciente**: Mayor interés profesional
                    
                    **Ventajas:**
                    - Mapeo de interés profesional
                    - Indica calidad de la empresa
                    - Refleja liquidez institucional
                    
                    **Desventajas:**
                    - Instituciones pueden ser wrong
                    - Datos trimestrales con retraso
                    - No diferencia entre tipos de instituciones
                    
                    **¿Para qué sirve?**
                    - Evaluar calidad de la empresa
                    - Analizar seguimiento profesional
                    - Detectar cambios en percepción
                    """,
                    "ejemplo": "70% propiedad institucional → buena aprobación profesional"
                },
                
                "Inst Trans": {
                    "definicion": "**Transacciones Institucionales** - Compras/ventas de fondos",
                    "calculacion": "Net buying/selling de instituciones en período",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Net buying**: Aprobación profesional
                    - **Net selling**: Preocupación profesional
                    - **Cambios bruscos**: Señales fuertes
                    - **Calidad instituciones**: Importa quién compra/vende
                    
                    **Ventajas:**
                    - Muestra sentiment profesional
                    - Datos de gestores sofisticados
                    - Puede anticipar movimientos
                    
                    **Desventajas:**
                    - Datos con retraso (13F trimestral)
                    - Agregado, no detalle por institución
                    - Puede ser momentum following
                    
                    **¿Para qué sirve?**
                    - Confirmar tesis de inversión
                    - Seguir smart money
                    - Detectar cambios en percepción profesional
                    """,
                    "ejemplo": "Fondos value reconocidos comprando → señal positiva"
                },
                
                "Short Float": {
                    "definicion": "**Short Interest** - % acciones vendidas en corto",
                    "calculacion": "Acciones vendidas en corto ÷ Float × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Bajo (<5%)**: Poco pesimismo
                    - **Moderado (5-10%)**: Escepticismo normal
                    - **Alto (10-20%)**: Significativo pesimismo
                    - **Muy alto (>20%)**: Posible short squeeze
                    
                    **Ventajas:**
                    - Mapeo de sentiment negativo
                    - Identifica posibles squeezes
                    - Refleja controversia
                    
                    **Desventajas:**
                    - Los shorts pueden tener razón
                    - Datos con retraso (semanal/biweekly)
                    - No considera timing de shorts
                    
                    **¿Para qué sirve?**
                    - Evaluar controversia sobre la acción
                    - Identificar oportunidades de squeeze
                    - Analizar riesgo de covering rallies
                    """,
                    "ejemplo": "Short Float 25% → alto pesimismo, posible squeeze"
                },
                
                "Short Ratio": {
                    "definicion": "**Días para Cubrir** - Tiempo para cubrir posiciones cortas",
                    "calculacion": "Acciones vendidas en corto ÷ Volumen promedio diario",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **<3 días**: Bajo riesgo de squeeze
                    - **3-7 días**: Riesgo moderado
                    - **>7 días**: Alto riesgo de squeeze
                    - **>10 días**: Riesgo muy alto
                    
                    **Ventajas:**
                    - Mejor que Short Float solo
                    - Considera liquidez
                    - Buen predictor de squeeze potential
                    
                    **Desventajas:**
                    - Basado en volumen histórico
                    - Puede cambiar rápidamente
                    - No considera convicción de shorts
                    
                    **¿Para qué sirve?**
                    - Evaluar riesgo de short squeeze
                    - Analizar dinámica de covering
                    - Gestión de riesgo en posiciones cortas
                    """,
                    "ejemplo": "Short Ratio 12 días → alto riesgo de squeeze"
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

