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


def mostrar_valoracion_mercado(stonk, ticker, info, nombre, descripcion, start_date, end_date):
            st.subheader("💰 VALORACIÓN Y MERCADO - 18 Métricas")
            
            metricas = {
                "Market Cap": {
                    "definicion": "**Capitalización de mercado** - Valor total de la empresa en bolsa",
                    "calculacion": "Precio actual de la acción × Número total de acciones en circulación",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Large Cap (>$10B)**: Empresas establecidas, menos volátiles, dividendos consistentes
                    - **Mid Cap ($2B-$10B)**: Empresas en crecimiento, balance riesgo/recompensa
                    - **Small Cap (<$2B)**: Empresas pequeñas, alto crecimiento potencial, más riesgo
                    - **Mega Cap (>$200B)**: Gigantes globales como Apple, Microsoft
                    
                    **Ventajas:**
                    - Fácil de calcular y entender
                    - Buen indicador del tamaño relativo
                    - Útil para comparar empresas del mismo sector
                    
                    **Desventajas:**
                    - No considera la deuda de la empresa
                    - Puede ser engañoso si hay muchas acciones en circulación
                    - No refleja el valor intrínseco real
                    
                    **¿Para qué sirve?**
                    - Determinar el tamaño y estabilidad de la empresa
                    - Clasificar empresas por capitalización
                    - Evaluar el riesgo relativo (generalmente empresas más grandes = menos riesgo)
                    """,
                    "ejemplo": "Apple: 16,300 millones de acciones × $150 = $2.45 billones de Market Cap"
                },
                
                "P/E (Price-to-Earnings)": {
                    "definicion": "**Ratio Precio-Beneficio** - Cuánto pagan los inversores por cada dólar de ganancias",
                    "calculacion": "Precio de la acción ÷ Ganancias por acción (EPS)",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **P/E bajo (<15)**: Posiblemente subvalorada, pero investiga por qué
                    - **P/E medio (15-25)**: Rango típico para muchas empresas
                    - **P/E alto (>25)**: Altas expectativas de crecimiento o posible sobrevaloración
                    
                    **Ventajas:**
                    - Fácil de calcular y entender
                    - Ampliamente utilizado y aceptado
                    - Buen punto de partida para valoración
                    
                    **Desventajas:**
                    - No útil para empresas sin ganancias
                    - Las ganancias pueden ser manipuladas contablemente
                    - No considera el crecimiento futuro
                    - Varía mucho entre sectores
                    
                    **Sectores típicos:**
                    - Tecnología: 20-30 (alto crecimiento esperado)
                    - Utilities: 12-18 (bajo crecimiento, estables)
                    - Bancos: 8-12 (regulados, crecimiento estable)
                    - Biotech: 30+ (potencial alto crecimiento)
                    
                    **¿Para qué sirve?**
                    - Comparar empresas dentro del mismo sector
                    - Identificar posibles oportunidades de valor
                    - Evaluar si el precio está justificado por las ganancias
                    """,
                    "ejemplo": "Empresa precio $100, EPS $5 → P/E = 20 (pagas $20 por cada $1 de ganancias)"
                },
                
                "Forward P/E": {
                    "definicion": "**P/E Forward** - Ratio P/E basado en ganancias estimadas futuras",
                    "calculacion": "Precio actual ÷ EPS estimado para el próximo año",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Forward P/E < Current P/E**: Se espera crecimiento de ganancias
                    - **Forward P/E > Current P/E**: Se espera disminución de ganancias
                    - Diferencia significativa puede indicar cambios en el negocio
                    
                    **Ventajas:**
                    - Más forward-looking que el P/E tradicional
                    - Mejor para empresas en crecimiento rápido
                    - Considera las expectativas del mercado
                    
                    **Desventajas:**
                    - Depende de estimaciones (pueden ser erróneas)
                    - Sensible a revisiones de analistas
                    - Las estimaciones pueden ser demasiado optimistas o pesimistas
                    
                    **¿Para qué sirve?**
                    - Evaluar valoración basada en expectativas futuras
                    - Identificar empresas donde el crecimiento no está reflejado en el precio
                    - Comparar con el P/E histórico para ver tendencias
                    """,
                    "ejemplo": "Precio $50, EPS estimado próximo año $2.50 → Forward P/E = 20"
                },
                
                "PEG Ratio": {
                    "definicion": "**Ratio P/E sobre Crecimiento** - Relaciona el P/E con la tasa de crecimiento",
                    "calculacion": "P/E Ratio ÷ Tasa de crecimiento anual de EPS (%)",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **PEG < 1**: Posiblemente subvalorada (crecimiento > P/E)
                    - **PEG = 1**: Valoración justa
                    - **PEG > 1**: Posiblemente sobrevalorada (P/E > crecimiento)
                    
                    **Ventajas:**
                    - Considera el crecimiento futuro
                    - Mejor que solo mirar P/E para empresas growth
                    - Útil para comparar empresas con diferentes tasas de crecimiento
                    
                    **Desventajas:**
                    - Depende de estimaciones de crecimiento (inciertas)
                    - No considera el riesgo
                    - Las tasas de crecimiento pueden no ser sostenibles
                    
                    **Interpretación por sectores:**
                    - Tech growth: PEG 1.0-1.5 puede ser aceptable
                    - Value stocks: Buscar PEG < 0.8
                    - Empresas maduras: PEG cercano a 1.0
                    
                    **¿Para qué sirve?**
                    - Identificar empresas growth a precios razonables
                    - Evaluar si el premium de P/E está justificado por el crecimiento
                    - Comparar empresas con diferentes perfiles de crecimiento
                    """,
                    "ejemplo": "P/E 20, crecimiento EPS 25% anual → PEG = 0.8 (atractivo)"
                },
                
                "P/S (Price-to-Sales)": {
                    "definicion": "**Ratio Precio-Ventas** - Valoración respecto a los ingresos por ventas",
                    "calculacion": "Market Cap ÷ Ventas anuales totales",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **P/S < 1**: Considerado bajo (posible oportunidad)
                    - **P/S 1-3**: Rango típico para muchas empresas
                    - **P/S > 3**: Considerado alto (mucho crecimiento esperado)
                    
                    **Ventajas:**
                    - Útil para empresas sin ganancias o con ganancias volátiles
                    - Las ventas son más difíciles de manipular que las ganancias
                    - Bueno para startups y empresas en crecimiento
                    
                    **Desventajas:**
                    - No considera la rentabilidad
                    - Empresas con márgenes bajos pueden tener P/S engañosos
                    - No diferencia entre ventas de calidad y ventas sin profit
                    
                    **Sectores típicos:**
                    - Software: P/S 5-15 (márgenes altos esperados)
                    - Retail: P/S 0.5-1.5 (márgenes bajos)
                    - Manufacturing: P/S 1-2
                    
                    **¿Para qué sirve?**
                    - Evaluar empresas que aún no son rentables
                    - Comparar empresas dentro del mismo sector
                    - Identificar empresas con ventas crecientes pero P/S bajo
                    """,
                    "ejemplo": "Market Cap $500M, Ventas $250M → P/S = 2.0"
                },
                
                "P/B (Price-to-Book)": {
                    "definicion": "**Ratio Precio-Valor Contable** - Compara precio de mercado con valor en libros",
                    "calculacion": "Precio de la acción ÷ Valor contable por acción",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **P/B < 1**: Cotiza bajo valor contable (posible oportunidad value)
                    - **P/B = 1**: Precio igual al valor contable
                    - **P/B > 1**: Prima sobre valor contable (normal para empresas rentables)
                    
                    **Ventajas:**
                    - Bueno para empresas con muchos activos tangibles
                    - El valor contable es relativamente estable
                    - Útil para bancos y empresas financieras
                    
                    **Desventajas:**
                    - No útil para empresas de servicios o tecnología
                    - No considera activos intangibles (marca, patentes)
                    - El valor contable puede estar desactualizado
                    
                    **Sectores típicos:**
                    - Bancos: P/B 0.8-1.5
                    - Seguros: P/B 1.0-1.8
                    - Tecnología: P/B 3.0+ (muchos intangibles)
                    
                    **¿Para qué sirve?**
                    - Encontrar empresas potencialmente subvaloradas
                    - Evaluar empresas con muchos activos físicos
                    - Análisis de bancos y instituciones financieras
                    """,
                    "ejemplo": "Precio $50, Valor contable por acción $40 → P/B = 1.25"
                },
                
                "P/FCF": {
                    "definicion": "**Precio/Flujo de Caja Libre** - Valoración respecto al flujo de caja generado",
                    "calculacion": "Market Cap ÷ Flujo de Caja Libre anual",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **P/FCF < 15**: Generalmente considerado atractivo
                    - **P/FCF 15-25**: Rango razonable
                    - **P/FCF > 25**: Posiblemente sobrevalorado
                    
                    **Ventajas:**
                    - El flujo de caja es más difícil de manipular que las ganancias
                    - Mide la capacidad real de generar efectivo
                    - Buen indicador de salud financiera
                    
                    **Desventajas:**
                    - El FCF puede ser volátil entre años
                    - No considera inversiones de capital futuras
                    - Puede ser negativo en empresas en crecimiento
                    
                    **¿Para qué sirve?**
                    - Evaluar la capacidad de generar efectivo real
                    - Comparar empresas dentro del mismo sector
                    - Identificar empresas con fuerte generación de caja
                    """,
                    "ejemplo": "Market Cap $1B, FCF $100M → P/FCF = 10"
                },
                
                "P/C": {
                    "definicion": "**Precio/Efectivo** - Valoración respecto al efectivo en balance",
                    "calculacion": "Precio de la acción ÷ Efectivo por acción",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **P/C bajo**: Mucho efectivo relativo al precio (posible oportunidad)
                    - **P/C alto**: Poca reserva de efectivo relativa al precio
                    - **P/C < 5**: Generalmente considerado atractivo
                    - **P/C > 10**: Puede indicar sobrevaloración
                    
                    **Ventajas:**
                    - Mide el colchón de seguridad en efectivo
                    - Útil para identificar empresas con fuerte posición de caja
                    - El efectivo es el activo más líquido y seguro
                    - Bueno para evaluar valoración en situaciones de crisis
                    
                    **Desventajas:**
                    - No considera cómo se usa el efectivo
                    - El efectivo puede estar destinado a obligaciones específicas
                    - Puede ser temporal (venta de activos, emisión de deuda)
                    - No diferencia entre efectivo operativo y no operativo
                    
                    **Interpretación por sectores:**
                    - **Tecnología**: P/C 5-15 (normal por alto crecimiento)
                    - **Manufactura**: P/C 3-8 (menos efectivo intensivo)
                    - **Financieras**: P/C 1-3 (mucha regulación de capital)
                    - **Biotech**: P/C 10-20 (queman efectivo en desarrollo)
                    
                    **¿Para qué sirve?**
                    - Evaluar la solidez financiera a corto plazo
                    - Identificar empresas con exceso de efectivo
                    - Analizar oportunidades de recompra de acciones o dividendos
                    - Valoración en adquisiciones (empresas con mucho cash)
                    
                    **Señales de alerta:**
                    - P/C muy alto con poco crecimiento
                    - Efectivo decreciente con P/C constante
                    - Empresas que queman cash rápidamente
                    """,
                    "ejemplo": "Precio $100, Efectivo por acción $25 → P/C = 4 (atractivo)\nPrecio $50, Efectivo por acción $3 → P/C = 16.7 (elevado)"
                },

                "EV/EBITDA": {
                    "definicion": "**Enterprise Value/EBITDA** - Valor empresa completa sobre ganancias operativas",
                    "calculacion": "Enterprise Value ÷ EBITDA",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **EV/EBITDA < 8**: Posiblemente subvalorada
                    - **EV/EBITDA 8-12**: Rango típico
                    - **EV/EBITDA > 12**: Posiblemente sobrevalorada
                    
                    **Ventajas:**
                    - Considera la deuda y efectivo (mejor que P/E)
                    - Útil para comparar empresas con diferente apalancamiento
                    - Muy usado en fusiones y adquisiciones
                    
                    **Desventajas:**
                    - No considera gastos por intereses e impuestos
                    - El EBITDA puede ser engañoso en algunos casos
                    - No es GAAP (puede calcularse de diferentes formas)
                    
                    **Sectores típicos:**
                    - Telecom: 6-9
                    - Healthcare: 10-14
                    - Tech: 12-18
                    
                    **¿Para qué sirve?**
                    - Comparar empresas con diferentes estructuras de capital
                    - Análisis de M&A (fusiones y adquisiciones)
                    - Evaluar el valor operativo del negocio
                    """,
                    "ejemplo": "EV $500M, EBITDA $50M → EV/EBITDA = 10"
                },
                
                "EV/Sales": {
                    "definicion": "**Enterprise Value/Ventas** - Valor empresa completa sobre ventas",
                    "calculacion": "Enterprise Value ÷ Ventas anuales",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **EV/Sales < 1**: Bajo relativo a ventas
                    - **EV/Sales 1-3**: Rango típico
                    - **EV/Sales > 3**: Alto relativo a ventas
                    
                    **Ventajas:**
                    - Considera la estructura completa de capital
                    - Mejor que P/S para empresas con mucha deuda
                    - Útil para empresas sin ganancias
                    
                    **Desventajas:**
                    - No considera rentabilidad
                    - Las ventas no garantizan ganancias
                    - Puede variar mucho entre sectores
                    
                    **¿Para qué sirve?**
                    - Evaluar empresas en crecimiento sin ganancias
                    - Comparar empresas con diferentes niveles de deuda
                    - Análisis de startups y empresas high-growth
                    """,
                    "ejemplo": "EV $600M, Ventas $200M → EV/Sales = 3.0"
                },
                
                "EV/FCF": {
                    "definicion": "**Enterprise Value/Flujo de Caja Libre** - Valor empresa completa sobre FCF",
                    "calculacion": "Enterprise Value ÷ Flujo de Caja Libre",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **EV/FCF < 10**: Muy atractivo
                    - **EV/FCF 10-20**: Razonable
                    - **EV/FCF > 20**: Posiblemente caro
                    
                    **Ventajas:**
                    - Considera toda la estructura de capital
                    - Basado en flujo de caja real (no ganancias contables)
                    - Bueno para evaluar capacidad de pago de deuda
                    
                    **Desventajas:**
                    - El FCF puede ser volátil
                    - No considera necesidades futuras de inversión
                    - Puede ser negativo
                    
                    **¿Para qué sirve?**
                    - Evaluar el retorno sobre la inversión total
                    - Análisis de empresas con mucha deuda
                    - Comparar oportunidades de inversión
                    """,
                    "ejemplo": "EV $800M, FCF $80M → EV/FCF = 10"
                },
                
                "EPS (ttm)": {
                    "definicion": "**Ganancias por Acción últimos 12 meses** - Beneficio neto por acción",
                    "calculacion": "Beneficio Neto últimos 12 meses ÷ Acciones en circulación",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **EPS creciente**: Empresa en crecimiento
                    - **EPS estable**: Empresa madura
                    - **EPS decreciente**: Posibles problemas
                    
                    **Ventajas:**
                    - Fácil de entender
                    - Directamente relacionado con el precio (P/E)
                    - Buen indicador de salud financiera
                    
                    **Desventajas:**
                    - Puede ser manipulado contablemente
                    - No considera el flujo de caja
                    - Puede variar por eventos extraordinarios
                    
                    **¿Para qué sirve?**
                    - Calcular el P/E ratio
                    - Evaluar la rentabilidad por acción
                    - Seguir la trayectoria de ganancias
                    """,
                    "ejemplo": "Beneficio $100M, 10M acciones → EPS = $10"
                },
                
                "EPS next Y": {
                    "definicion": "**EPS Próximo Año** - Estimación de ganancias para el próximo año",
                    "calculacion": "Estimación de Beneficio Neto próximo año ÷ Acciones estimadas",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **EPS next Y > EPS actual**: Crecimiento esperado
                    - **EPS next Y < EPS actual**: Decrecimiento esperado
                    - **Gran diferencia**: Cambios significativos en el negocio
                    
                    **Ventajas:**
                    - Proporciona visión futura
                    - Útil para calcular Forward P/E
                    - Refleja expectativas del mercado
                    
                    **Desventajas:**
                    - Basado en estimaciones (inciertas)
                    - Puede ser demasiado optimista/pesimista
                    - Sensible a revisiones
                    
                    **¿Para qué sirve?**
                    - Evaluar expectativas de crecimiento
                    - Identificar posibles sorpresas de ganancias
                    - Planificar estrategias de inversión
                    """,
                    "ejemplo": "EPS actual $5, EPS next Y estimado $6 → 20% crecimiento esperado"
                },
                
                "EPS next Q": {
                    "definicion": "**EPS Próximo Trimestre** - Estimación para el próximo trimestre",
                    "calculacion": "Estimación Beneficio Neto próximo trimestre ÷ Acciones",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Beat estimates**: Supera estimaciones (positivo)
                    - **Miss estimates**: No alcanza estimaciones (negativo)
                    - **Guide higher**: Aumenta guidance (muy positivo)
                    
                    **Ventajas:**
                    - Proporciona visión a corto plazo
                    - Útil para trading alrededor de earnings
                    - Indica momentum operativo
                    
                    **Desventajas:**
                    - Muy volátil entre trimestres
                    - Sensible a estacionalidad
                    - Las estimaciones pueden ser erróneas
                    
                    **¿Para qué sirve?**
                    - Anticipar resultados trimestrales
                    - Evaluar momentum del negocio
                    - Timing de entrada/salida de posiciones
                    """,
                    "ejemplo": "Estimación Q1: $1.25 por acción"
                },
                
                "EPS this Y": {
                    "definicion": "**EPS Este Año** - Ganancias actuales vs año anterior",
                    "calculacion": "EPS año actual ÷ EPS año anterior - 1",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Positivo**: Crecimiento interanual
                    - **Negativo**: Decrecimiento interanual
                    - **Alto**: Fuerte crecimiento
                    
                    **Ventajas:**
                    - Muestra tendencia anual
                    - Menos volátil que trimestral
                    - Buen indicador de dirección
                    
                    **Desventajas:**
                    - Puede estar influido por eventos únicos
                    - No considera factores estacionales
                    - Puede enmascarar problemas trimestrales
                    
                    **¿Para qué sirve?**
                    - Evaluar performance anual
                    - Comparar con guidance de la empresa
                    - Análisis de tendencias a medio plazo
                    """,
                    "ejemplo": "EPS 2023: $4.50, EPS 2024: $5.00 → Crecimiento 11%"
                },
                
                "EPS next 5Y": {
                    "definicion": "**Crecimiento EPS Próximos 5 Años** - Tasa crecimiento anual estimada",
                    "calculacion": "Estimación crecimiento anual compuesto próximo 5 años",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **<5%**: Crecimiento lento (empresa madura)
                    - **5-15%**: Crecimiento moderado
                    - **>15%**: Crecimiento rápido (empresa growth)
                    
                    **Ventajas:**
                    - Proporciona perspectiva a largo plazo
                    - Útil para modelos de descuento de flujos
                    - Refleja expectativas de crecimiento sostenido
                    
                    **Desventajas:**
                    - Muy especulativo a 5 años vista
                    - Las estimaciones suelen ser optimistas
                    - Difícil de predecir con precisión
                    
                    **¿Para qué sirve?**
                    - Calcular PEG ratio
                    - Evaluar potencial de crecimiento a largo plazo
                    - Comparar empresas dentro del mismo sector
                    """,
                    "ejemplo": "Crecimiento EPS estimado 12% anual próximos 5 años"
                },
                
                "EPS past 5Y": {
                    "definicion": "**Crecimiento EPS 5 Años** - Tasa crecimiento histórico anual",
                    "calculacion": "Tasa crecimiento anual compuesto últimos 5 años",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Consistente**: Crecimiento estable (buena gestión)
                    - **Volátil**: Resultados irregulares (riesgo)
                    - **Decreciente**: Posible madurez/saturación
                    
                    **Ventajas:**
                    - Basado en datos reales (no estimaciones)
                    - Muestra capacidad histórica de crecimiento
                    - Buen indicador de calidad de gestión
                    
                    **Desventajas:**
                    - El pasado no garantiza futuro
                    - Puede estar influido por ciclos económicos
                    - No considera cambios recientes en el negocio
                    
                    **¿Para qué sirve?**
                    - Evaluar track record de la empresa
                    - Comparar con estimaciones futuras
                    - Análisis de consistencia en resultados
                    """,
                    "ejemplo": "EPS creció de $2 a $4 en 5 años → 15% crecimiento anual"
                },
                
                "Book Value/Share": {
                    "definicion": "**Valor Contable por Acción** - Valor patrimonial por acción",
                    "calculacion": "Patrimonio Neto ÷ Acciones en circulación",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Creciente**: Empresa acumulando valor
                    - **Decreciente**: Pérdidas o recompras de acciones
                    - **Estable**: Empresa madura
                    
                    **Ventajas:**
                    - Representa el valor en libros
                    - Relativamente estable
                    - Bueno para empresas con activos tangibles
                    
                    **Desventajas:**
                    - No refleja valor de mercado
                    - Puede no incluir activos intangibles
                    - Puede estar desactualizado
                    
                    **¿Para qué sirve?**
                    - Calcular P/B ratio
                    - Evaluar valoración relativa
                    - Análisis de empresas value
                    """,
                    "ejemplo": "Patrimonio $400M, 10M acciones → Book Value/Share = $40"
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
