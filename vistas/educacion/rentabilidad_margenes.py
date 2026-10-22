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


def mostrar_rentabilidad_margenes(stonk, ticker, info, nombre, descripcion, start_date, end_date):
            st.subheader("📈 RENTABILIDAD Y MÁRGENES - 16 Métricas")
            
            metricas = {
                "ROA (Return on Assets)": {
                    "definicion": "**Retorno sobre Activos** - Eficiencia en el uso de todos los recursos",
                    "calculacion": "Beneficio Neto ÷ Activos Totales × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **ROA < 5%**: Baja eficiencia
                    - **ROA 5-10%**: Adecuado
                    - **ROA > 10%**: Alta eficiencia
                    
                    **Ventajas:**
                    - Considera todos los recursos (no solo el capital)
                    - Menos susceptible a manipulación por apalancamiento
                    - Bueno para comparar empresas con diferentes estructuras de capital
                    
                    **Desventajas:**
                    - Los activos pueden estar valorados incorrectamente
                    - No considera el costo de capital
                    - Puede penalizar empresas con muchos activos
                    
                    **Comparativa por sectores:**
                    - Tecnología: 8-15% (pocos activos, altos retornos)
                    - Manufactura: 4-8% (activos intensivos)
                    - Retail: 3-6% (márgenes bajos, alta rotación)
                    
                    **¿Para qué sirve?**
                    - Medir la eficiencia operativa general
                    - Comparar empresas con diferentes niveles de deuda
                    - Evaluar la calidad de la gestión
                    """,
                    "ejemplo": "Beneficio $500k, Activos $10M → ROA = 5%"
                },
                
                "ROE (Return on Equity)": {
                    "definicion": "**Retorno sobre el Patrimonio** - Rentabilidad generada con el capital de los accionistas",
                    "calculacion": "Beneficio Neto ÷ Patrimonio Neto × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **ROE < 8%**: Bajo - podría no compensar el riesgo
                    - **ROE 8-15%**: Adecuado
                    - **ROE 15-20%**: Bueno
                    - **ROE > 20%**: Excelente
                    
                    **Ventajas:**
                    - Fácil de calcular y entender
                    - Buen indicador de eficiencia del capital
                    - Ampliamente utilizado
                    
                    **Desventajas:**
                    - Puede ser inflado por mucho apalancamiento (deuda)
                    - No considera el riesgo asumido
                    - Puede variar significativamente entre sectores
                    
                    **Análisis DuPont (descomposición del ROE):**
                    ROE = (Margen Neto) × (Rotación Activos) × (Apalancamiento)
                    - **Margen Neto**: Eficiencia en control de costos
                    - **Rotación**: Eficiencia uso de activos  
                    - **Apalancamiento**: Uso de deuda vs capital
                    
                    **¿Para qué sirve?**
                    - Medir la eficiencia en el uso del capital de accionistas
                    - Comparar empresas dentro del mismo sector
                    - Identificar empresas con ventajas competitivas sostenibles
                    """,
                    "ejemplo": "Beneficio $1M, Patrimonio $10M → ROE = 10%"
                },
                
                "ROI (Return on Investment)": {
                    "definicion": "**Retorno sobre la Inversión** - Eficiencia de las inversiones realizadas",
                    "calculacion": "Beneficio de la inversión ÷ Costo de la inversión × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **ROI > costo de capital**: Crea valor
                    - **ROI < costo de capital**: Destruye valor
                    - **ROI alto**: Inversiones eficientes
                    
                    **Ventajas:**
                    - Mide la eficiencia de las decisiones de inversión
                    - Útil para evaluar proyectos específicos
                    - Fácil de entender
                    
                    **Desventajas:**
                    - Puede ser difícil de calcular para inversiones complejas
                    - No considera el valor temporal del dinero
                    - Puede variar según el período medido
                    
                    **¿Para qué sirve?**
                    - Evaluar la eficiencia del capital invertido
                    - Comparar diferentes oportunidades de inversión
                    - Tomar decisiones de asignación de capital
                    """,
                    "ejemplo": "Inversión $1M, Beneficio $150k anual → ROI = 15%"
                },
                
                "Gross Margin": {
                    "definicion": "**Margen Bruto** - Porcentaje que queda después de costos directos",
                    "calculacion": "(Ventas - Costo de Bienes Vendidos) ÷ Ventas × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Margen alto**: Fuertes ventajas competitivas, poder de precios
                    - **Margen bajo**: Competencia intensa, commoditización
                    - **Margen creciente**: Mejora en eficiencia o poder de precios
                    
                    **Ventajas:**
                    - Buen indicador de ventajas competitivas
                    - Relativamente estable en el tiempo
                    - Difícil de manipular contablemente
                    
                    **Desventajas:**
                    - No considera gastos operativos
                    - Puede variar significativamente por estacionalidad
                    - Depende de la clasificación de costos
                    
                    **Rangos por industria:**
                    - Software: 80-90%
                    - Farmacéutica: 70-80%
                    - Bienes de consumo: 40-60%
                    - Retail: 20-40%
                    - Airlines: 10-20%
                    
                    **¿Para qué sirve?**
                    - Evaluar el poder de fijación de precios
                    - Medir ventajas competitivas en costos
                    - Identificar tendencias en la rentabilidad del core business
                    """,
                    "ejemplo": "Ventas $1M, Costo bienes $600k → Margen Bruto = 40%"
                },
                
                "Operating Margin": {
                    "definicion": "**Margen Operativo** - Rentabilidad del negocio principal antes de intereses e impuestos",
                    "calculacion": "Beneficio Operativo ÷ Ventas × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Margen alto**: Eficiencia operativa, control de gastos
                    - **Margen bajo**: Altos gastos operativos, ineficiencia
                    - **Margen creciente**: Mejora en gestión operativa
                    
                    **Ventajas:**
                    - Mide la eficiencia del negocio principal
                    - Excluye efectos financieros y fiscales
                    - Bueno para comparar empresas con diferente apalancamiento
                    
                    **Desventajas:**
                    - No considera la estructura de capital
                    - Puede variar por decisiones contables
                    - No refleja el beneficio final para accionistas
                    
                    **Componentes que afectan el margen operativo:**
                    - Eficiencia en producción
                    - Control de gastos generales
                    - Precios vs costos
                    - Economías de escala
                    
                    **¿Para qué sirve?**
                    - Evaluar la eficiencia operativa del negocio core
                    - Comparar empresas con diferentes estructuras financieras
                    - Identificar mejoras en gestión operativa
                    """,
                    "ejemplo": "Ventas $1M, Beneficio operativo $150k → Margen Operativo = 15%"
                },
                
                "Profit Margin": {
                    "definicion": "**Margen de Beneficio Neto** - Porcentaje final que queda para accionistas",
                    "calculacion": "Beneficio Neto ÷ Ventas × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Margen alto**: Empresa muy eficiente o con fuertes ventajas
                    - **Margen bajo**: Competencia intensa o ineficiencias
                    - **Margen creciente**: Mejoras en eficiencia o mix de productos
                    
                    **Ventajas:**
                    - Representa el resultado final para accionistas
                    - Incluye todos los costos y gastos
                    - Fácil de comparar entre empresas
                    
                    **Desventajas:**
                    - Puede ser afectado por eventos extraordinarios
                    - No diferencia entre ganancias operativas y no operativas
                    - Puede variar por decisiones fiscales
                    
                    **Rangos típicos:**
                    - Software: 20-30%
                    - Bancos: 15-25%
                    - Retail: 2-5%
                    - Airlines: 2-8%
                    
                    **¿Para qué sirve?**
                    - Evaluar la rentabilidad final del negocio
                    - Comparar eficiencia entre competidores
                    - Identificar tendencias en rentabilidad
                    """,
                    "ejemplo": "Ventas $1M, Beneficio neto $80k → Profit Margin = 8%"
                },
                
                "EBITDA": {
                    "definicion": "**Ganancias antes de Intereses, Impuestos, Depreciación y Amortización**",
                    "calculacion": "Beneficio Operativo + Depreciación + Amortización",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **EBITDA alto**: Fuerte generación operativa de caja
                    - **EBITDA creciente**: Mejora en performance operativa
                    - **EBITDA/Intereses alto**: Buena capacidad de cubrir deuda
                    
                    **Ventajas:**
                    - Elimina efectos de decisiones financieras y fiscales
                    - Buen proxy para flujo de caja operativo
                    - Útil para comparar empresas con diferentes estructuras
                    
                    **Desventajas:**
                    - No es GAAP (puede calcularse de diferentes formas)
                    - Ignora necesidades de reinversión en activos
                    - Puede ser engañoso en empresas con alta depreciación
                    
                    **¿Para qué sirve?**
                    - Evaluar performance operativa pura
                    - Calcular ratios de cobertura de deuda
                    - Análisis de empresas con diferentes políticas de depreciación
                    """,
                    "ejemplo": "Beneficio operativo $200k, Depreciación $50k → EBITDA = $250k"
                },
                
                "EBIT": {
                    "definicion": "**Ganancias antes de Intereses e Impuestos** - Resultado operativo",
                    "calculacion": "Ventas - Todos los gastos operativos (excluyendo intereses e impuestos)",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **EBIT alto**: Negocio central rentable
                    - **EBIT creciente**: Mejora en eficiencia operativa
                    - **EBIT estable**: Empresa madura y predecible
                    
                    **Ventajas:**
                    - Mide la rentabilidad del negocio principal
                    - Excluye efectos financieros y fiscales
                    - Bueno para comparar eficiencia operativa
                    
                    **Desventajas:**
                    - No considera necesidades de inversión en activos
                    - Puede variar por métodos contables
                    - No refleja el costo del capital
                    
                    **¿Para qué sirve?**
                    - Evaluar la rentabilidad operativa core
                    - Comparar empresas con diferente apalancamiento
                    - Análisis de eficiencia operativa por segmentos
                    """,
                    "ejemplo": "Ventas $1M, Gastos operativos $800k → EBIT = $200k"
                },
                
                "Net Income": {
                    "definicion": "**Beneficio Neto** - Ganancias finales después de todos los gastos",
                    "calculacion": "Ingresos Totales - Gastos Totales (incluyendo intereses e impuestos)",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Positivo y creciente**: Empresa saludable y en crecimiento
                    - **Volátil**: Resultados inconsistentes (riesgo)
                    - **Negativo**: Pérdidas (señal de alerta)
                    
                    **Ventajas:**
                    - Representa el resultado final para accionistas
                    - Incluye todos los aspectos del negocio
                    - Base para cálculo de EPS
                    
                    **Desventajas:**
                    - Puede incluir partidas extraordinarias
                    - Sensible a decisiones contables
                    - No diferencia entre ganancias recurrentes y no recurrentes
                    
                    **¿Para qué sirve?**
                    - Evaluar la rentabilidad general
                    - Calcular ratios de rentabilidad (ROE, ROA)
                    - Seguir la trayectoria de ganancias
                    """,
                    "ejemplo": "Ingresos $1.2M, Gastos $1.1M → Net Income = $100k"
                },
                
                "Income Tax": {
                    "definicion": "**Impuesto sobre la Renta** - Monto pagado en impuestos",
                    "calculacion": "Base imponible × Tasa impositiva",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Tasa efectiva baja**: Posibles beneficios fiscales o ubicación favorable
                    - **Tasa efectiva alta**: Pocos beneficios fiscales
                    - **Cambios significativos**: Cambios en legislación o estructura
                    
                    **Ventajas:**
                    - Indica la carga fiscal real
                    - Puede mostrar ventajas competitivas fiscales
                    - Útil para proyecciones futuras
                    
                    **Desventajas:**
                    - Puede ser temporal (créditos fiscales, pérdidas arrastradas)
                    - Complejo de analizar en empresas multinacionales
                    - Sensible a cambios legislativos
                    
                    **¿Para qué sirve?**
                    - Evaluar la carga fiscal efectiva
                    - Identificar ventajas fiscales sostenibles
                    - Proyectar ganancias futuras netas
                    """,
                    "ejemplo": "Beneficio antes impuestos $500k, Impuestos $100k → Tasa 20%"
                },
                
                "Dividend": {
                    "definicion": "**Dividendo** - Pago periódico a accionistas",
                    "calculacion": "Monto total distribuido ÷ Acciones en circulación",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Dividendo creciente**: Empresa con exceso de caja y confianza
                    - **Dividendo estable**: Empresa madura y predecible
                    - **Recorte de dividendo**: Posibles problemas financieros
                    
                    **Ventajas:**
                    - Proporciona income a inversores
                    - Señal de confianza del management
                    - Atractivo para inversores conservadores
                    
                    **Desventajas:**
                    - Dinero que no se reinvierte en el negocio
                    - Puede crear expectativas difíciles de mantener
                    - Empresas pueden endeudarse para pagarlos
                    
                    **¿Para qué sirve?**
                    - Evaluar política de distribución a accionistas
                    - Calcular yield y retorno total
                    - Identificar empresas income-oriented
                    """,
                    "ejemplo": "Dividendo trimestral $0.25 por acción → $1.00 anual"
                },
                
                "Dividend %": {
                    "definicion": "**Rendimiento por Dividendo** - Retorno por dividendo relativo al precio",
                    "calculacion": "Dividendo anual por acción ÷ Precio de la acción × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Yield bajo (1-3%)**: Empresas growth, poco income
                    - **Yield medio (3-6%)**: Empresas value, balance growth/income
                    - **Yield alto (>6%)**: Empresas income, posible riesgo
                    
                    **Ventajas:**
                    - Fácil de calcular y comparar
                    - Componente importante del retorno total
                    - Atractivo para inversores que buscan income
                    
                    **Desventajas:**
                    - Yield alto puede indicar problemas (precio bajo)
                    - No garantizado (puede ser recortado)
                    - Empresas pueden tener yield alto pero poco crecimiento
                    
                    **Sectores típicos:**
                    - Utilities: 3-5%
                    - REITs: 4-8%
                    - Tech: 0-2%
                    - Consumer Staples: 2-4%
                    
                    **¿Para qué sirve?**
                    - Evaluar atractivo para inversores income
                    - Comparar con alternativas de renta fija
                    - Calcular retorno total esperado
                    """,
                    "ejemplo": "Precio $100, Dividendo anual $4 → Yield = 4%"
                },
                
                "Payout Ratio": {
                    "definicion": "**Ratio de Pago** - Porcentaje de ganancias pagado como dividendo",
                    "calculacion": "Dividendo por acción ÷ EPS × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Payout bajo (<30%)**: Empresa retiene ganancias para crecimiento
                    - **Payout medio (30-60%)**: Balance entre dividendos y crecimiento
                    - **Payout alto (>60%)**: Empresa madura, poco crecimiento
                    - **Payout >100%**: Pagando más de lo que gana (insostenible)
                    
                    **Ventajas:**
                    - Indica sostenibilidad del dividendo
                    - Muestra la política de distribución vs reinversión
                    - Útil para evaluar crecimiento futuro
                    
                    **Desventajas:**
                    - Basado en ganancias que pueden ser volátiles
                    - No considera flujo de caja
                    - Puede variar significativamente entre años
                    
                    **¿Para qué sirve?**
                    - Evaluar sostenibilidad del dividendo
                    - Identificar empresas con potencial de aumento de dividendo
                    - Analizar el balance entre income y crecimiento
                    """,
                    "ejemplo": "EPS $5, Dividendo $2 → Payout Ratio = 40%"
                },
                
                "EPS Q/Q": {
                    "definicion": "**Crecimiento EPS Trimestral** - Cambio vs trimestre anterior",
                    "calculacion": "(EPS trimestre actual - EPS trimestre anterior) ÷ EPS trimestre anterior × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Positivo**: Mejora trimestral
                    - **Negativo**: Empeoramiento trimestral
                    - **Alto**: Fuerte momentum
                    - **Consistente positivo**: Trayectoria sólida
                    
                    **Ventajas:**
                    - Muestra momentum a corto plazo
                    - Útil para identificar tendencias emergentes
                    - Reacciona rápido a cambios en el negocio
                    
                    **Desventajas:**
                    - Muy volátil entre trimestres
                    - Sensible a estacionalidad
                    - Puede estar afectado por eventos únicos
                    
                    **¿Para qué sirve?**
                    - Evaluar performance trimestral
                    - Identificar cambios en momentum
                    - Timing de decisiones de inversión
                    """,
                    "ejemplo": "EPS Q1: $1.20, EPS Q2: $1.35 → Crecimiento 12.5%"
                },
                
                "Sales Q/Q": {
                    "definicion": "**Crecimiento Ventas Trimestral** - Cambio en ventas vs trimestre anterior",
                    "calculacion": "(Ventas trimestre actual - Ventas trimestre anterior) ÷ Ventas trimestre anterior × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Positivo**: Crecimiento orgánico o por adquisiciones
                    - **Negativo**: Contracción del negocio
                    - **Aceleración**: Crecimiento cada vez más rápido
                    - **Desaceleración**: Crecimiento perdiendo momentum
                    
                    **Ventajas:**
                    - Indica salud del top line
                    - Menos manipulable que las ganancias
                    - Buen indicador de demanda del producto/servicio
                    
                    **Desventajas:**
                    - No considera rentabilidad
                    - Puede estar inflado por adquisiciones
                    - Sensible a estacionalidad
                    
                    **¿Para qué sirve?**
                    - Evaluar crecimiento del negocio principal
                    - Identificar tendencias en demanda
                    - Comparar con expectativas del mercado
                    """,
                    "ejemplo": "Ventas Q1: $250M, Ventas Q2: $275M → Crecimiento 10%"
                },
                
                "Earnings Date": {
                    "definicion": "**Fecha de Resultados** - Próxima publicación de resultados trimestrales",
                    "calculacion": "Fecha calendario anunciada por la empresa",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Antes del opening/after closing**: Normal para minimizar impacto
                    - **Desviación del patrón habitual**: Posible sorpresa
                    - **Retraso inusual**: Posibles problemas
                    
                    **Ventajas:**
                    - Permite prepararse para la volatilidad
                    - Útil para estrategias de trading alrededor de earnings
                    - Indica transparencia del management
                    
                    **Desventajas:**
                    - Las fechas pueden cambiar
                    - No indica la calidad de los resultados
                    - Puede generar expectativas irreales
                    
                    **¿Para qué sirve?**
                    - Planificar timing de inversiones
                    - Gestionar riesgo alrededor de eventos
                    - Evaluar consistencia en comunicación
                    """,
                    "ejemplo": "Próximo earnings: 25 de Octubre, después del cierre"
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

