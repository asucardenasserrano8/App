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


def mostrar_deuda_liquidez(stonk, ticker, info, nombre, descripcion, start_date, end_date):
            st.subheader("🏦 DEUDA Y LIQUIDEZ - 12 Métricas")
            
            metricas = {
                "Total Debt": {
                    "definicion": "**Deuda Total** - Suma de deuda a corto y largo plazo",
                    "calculacion": "Deuda Corto Plazo + Deuda Largo Plazo",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Deuda creciente**: Posible expansión agresiva o problemas de caja
                    - **Deuda decreciente**: Desapalancamiento, mejora financiera
                    - **Sin deuda**: Empresa conservadora (puede perder oportunidades)
                    
                    **Ventajas:**
                    - Muestra la carga total de deuda
                    - Fácil de entender
                    - Base para otros ratios de deuda
                    
                    **Desventajas:**
                    - No considera la capacidad de pago
                    - No diferencia entre tipos de deuda
                    - Puede variar por ciclos empresariales
                    
                    **¿Para qué sirve?**
                    - Evaluar el apalancamiento total
                    - Comparar con patrimonio y activos
                    - Analizar tendencias de financiación
                    """,
                    "ejemplo": "Deuda corto plazo $50M + Deuda largo plazo $150M = Total Debt $200M"
                },
                
                "Debt/Eq": {
                    "definicion": "**Ratio Deuda/Patrimonio** - Relación entre deuda total y capital propio",
                    "calculacion": "Deuda Total ÷ Patrimonio Neto",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **<0.5**: Conservador
                    - **0.5-1.0**: Moderado
                    - **>1.0**: Agresivo
                    - **>2.0**: Muy riesgoso
                    
                    **Ventajas:**
                    - Muestra estructura de capital
                    - Útil para comparar empresas del mismo sector
                    - Indica política financiera
                    
                    **Desventajas:**
                    - No considera el costo de la deuda
                    - Puede variar por valoración de patrimonio
                    - Sectores intensivos en capital pueden tener ratios altos normales
                    
                    **Sectores típicos:**
                    - Utilities: 1.0-1.5
                    - Telecom: 1.5-2.0
                    - Tech: 0.2-0.8
                    - Bancos: 3.0+ (estructura diferente)
                    
                    **¿Para qué sirve?**
                    - Evaluar riesgo financiero
                    - Comparar políticas de financiación
                    - Identificar posibles problemas de solvencia
                    """,
                    "ejemplo": "Deuda $200M, Patrimonio $250M → Debt/Eq = 0.8"
                },
                
                "LT Debt/Eq": {
                    "definicion": "**Deuda Largo Plazo/Patrimonio** - Deuda a largo plazo vs capital",
                    "calculacion": "Deuda Largo Plazo ÷ Patrimonio Neto",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Alto**: Financiación estable a largo plazo
                    - **Bajo**: Poca deuda estructural
                    - **Creciente**: Más financiación vía deuda
                    
                    **Ventajas:**
                    - Enfocado en deuda estructural
                    - Menos volátil que deuda total
                    - Mejor para análisis de largo plazo
                    
                    **Desventajas:**
                    - Ignora deuda a corto plazo
                    - No considera vencimientos
                    - Puede enmascarar problemas de liquidez
                    
                    **¿Para qué sirve?**
                    - Evaluar estructura de capital permanente
                    - Analizar financiación de proyectos largos
                    - Comparar estabilidad financiera
                    """,
                    "ejemplo": "Deuda LP $150M, Patrimonio $250M → LT Debt/Eq = 0.6"
                },
                
                "Current Ratio": {
                    "definicion": "**Ratio Corriente** - Capacidad para pagar obligaciones a corto plazo",
                    "calculacion": "Activos Corrientes ÷ Pasivos Corrientes",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **<1.0**: Posibles problemas de liquidez
                    - **1.0-1.5**: Aceptable
                    - **1.5-2.0**: Bueno
                    - **>2.0**: Excelente (pero puede indicar activos ociosos)
                    
                    **Ventajas:**
                    - Simple y ampliamente usado
                    - Buen indicador de salud a corto plazo
                    - Fácil de calcular
                    
                    **Desventajas:**
                    - No considera calidad de activos corrientes
                    - El inventario puede no ser líquido
                    - Puede variar estacionalmente
                    
                    **¿Para qué sirve?**
                    - Evaluar liquidez inmediata
                    - Detectar posibles problemas de pago
                    - Comparar con competidores del sector
                    """,
                    "ejemplo": "Activos corrientes $500k, Pasivos corrientes $300k → Current Ratio = 1.67"
                },
                
                "Quick Ratio": {
                    "definicion": "**Ratio Rápido** - Liquidez inmediata excluyendo inventario",
                    "calculacion": "(Activos Corrientes - Inventario) ÷ Pasivos Corrientes",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **<0.5**: Muy bajo
                    - **0.5-1.0**: Aceptable
                    - **>1.0**: Bueno
                    - **>1.5**: Excelente
                    
                    **Ventajas:**
                    - Más conservador que Current Ratio
                    - Excluye inventario (menos líquido)
                    - Mejor indicador de liquidez real
                    
                    **Desventajas:**
                    - Puede ser demasiado conservador
                    - No considera rotación de inventario
                    - Algunas empresas dependen del inventario
                    
                    **¿Para qué sirve?**
                    - Evaluar capacidad de pago inmediata
                    - Análisis más realista de liquidez
                    - Detectar dependencia del inventario
                    """,
                    "ejemplo": "Activos corrientes $500k, Inventario $200k, Pasivos $300k → Quick Ratio = 1.0"
                },
                
                "Cash/Share": {
                    "definicion": "**Efectivo por Acción** - Reservas de efectivo por cada acción",
                    "calculacion": "Efectivo y Equivalentes ÷ Acciones en Circulación",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Alto**: Fuertes reservas, posibles dividendos especiales o recompras
                    - **Bajo**: Poco colchón de seguridad
                    - **Creciente**: Acumulación de caja
                    
                    **Ventajas:**
                    - Muestra colchón de seguridad por acción
                    - Útil para valoración
                    - Indica capacidad para oportunidades
                    
                    **Desventajas:**
                    - No considera deuda
                    - El efectivo puede estar destinado a obligaciones
                    - Demasiado efectivo puede indicar falta de oportunidades de inversión
                    
                    **¿Para qué sirve?**
                    - Evaluar margen de seguridad
                    - Identificar posibles recompras o dividendos
                    - Valoración en adquisiciones
                    """,
                    "ejemplo": "Efectivo $100M, 10M acciones → Cash/Share = $10"
                },
                
                "Cash Flow/Share": {
                    "definicion": "**Flujo de Caja por Acción** - Flujo operativo generado por acción",
                    "calculacion": "Flujo de Caja Operativo ÷ Acciones en Circulación",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Alto**: Fuerte generación de caja por acción
                    - **Creciente**: Mejora en eficiencia operativa
                    - **> EPS**: Calidad de ganancias alta
                    
                    **Ventajas:**
                    - Basado en caja real (no ganancias contables)
                    - Mejor indicador de salud financiera
                    - Difícil de manipular
                    
                    **Desventajas:**
                    - Puede ser volátil
                    - No considera inversiones de capital
                    - Sensible a cambios en capital de trabajo
                    
                    **¿Para qué sirve?**
                    - Evaluar calidad de ganancias
                    - Calcular capacidad de pago de dividendos
                    - Comparar con EPS
                    """,
                    "ejemplo": "FCF Operativo $80M, 10M acciones → Cash Flow/Share = $8"
                },
                
                "Total Cash": {
                    "definicion": "**Efectivo Total** - Dinero disponible en caja y equivalentes",
                    "calculacion": "Efectivo + Equivalentes de Efectivo",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Alto**: Fuertes reservas líquidas
                    - **Bajo**: Dependencia de financiación externa
                    - **Óptimo**: Suficiente para operar + colchón de seguridad
                    
                    **Ventajas:**
                    - Muestra liquidez absoluta
                    - Fácil de entender
                    - Base para otros cálculos
                    
                    **Desventajas:**
                    - No considera obligaciones
                    - Puede estar en el extranjero con restricciones
                    - Demasiado efectivo puede ser ineficiente
                    
                    **¿Para qué sirve?**
                    - Evaluar solvencia a corto plazo
                    - Analizar capacidad para oportunidades
                    - Preparación para crisis
                    """,
                    "ejemplo": "Efectivo $50M + Equivalentes $30M = Total Cash $80M"
                },
                
                "Total Cash/Share": {
                    "definicion": "**Efectivo Total por Acción** - Similar a Cash/Share pero incluye equivalentes",
                    "calculacion": "Total Cash ÷ Acciones en Circulación",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Comparación con precio**: Si Cash/Share es alto vs precio, posible oportunidad
                    - **Tendencia**: Creciente es positivo
                    - **Sector**: Tech suele tener más cash que industriales
                    
                    **Ventajas:**
                    - Visión completa de liquidez por acción
                    - Útil para valoración
                    - Bueno para análisis comparativo
                    
                    **Desventajas:**
                    - No considera uso del efectivo
                    - Puede incluir efectivo restringido
                    - No diferencia entre efectivo operativo y no operativo
                    
                    **¿Para qué sirve?**
                    - Valoración relativa
                    - Identificar empresas con exceso de caja
                    - Evaluar potencial de recompra de acciones
                    """,
                    "ejemplo": "Total Cash $80M, 10M acciones → Total Cash/Share = $8"
                },
                
                "Working Capital": {
                    "definicion": "**Capital de Trabajo** - Recursos disponibles para operaciones diarias",
                    "calculacion": "Activos Corrientes - Pasivos Corrientes",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Positivo**: Capacidad para operar sin problemas
                    - **Negativo**: Posibles problemas de liquidez
                    - **Creciente**: Mejora en gestión operativa
                    
                    **Ventajas:**
                    - Muestra salud operativa a corto plazo
                    - Indica eficiencia en gestión de capital de trabajo
                    - Buen predictor de problemas financieros
                    
                    **Desventajas:**
                    - No considera calidad de activos
                    - Puede ser manipulado con timing de pagos/cobros
                    - Varía por estacionalidad
                    
                    **¿Para qué sirve?**
                    - Evaluar salud operativa a corto plazo
                    - Detectar posibles problemas de liquidez
                    - Analizar eficiencia en gestión de capital
                    """,
                    "ejemplo": "Activos corrientes $500k, Pasivos corrientes $300k → Working Capital = $200k"
                },
                
                "Interest Coverage": {
                    "definicion": "**Cobertura de Intereses** - Capacidad para pagar intereses de la deuda",
                    "calculacion": "EBIT ÷ Gastos por Intereses",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **<1.0**: No cubre intereses (muy peligroso)
                    - **1.0-1.5**: Muy justo
                    - **1.5-3.0**: Aceptable
                    - **>3.0**: Bueno
                    - **>5.0**: Excelente
                    
                    **Ventajas:**
                    - Mide capacidad de servicio de deuda
                    - Buen predictor de problemas financieros
                    - Fácil de calcular
                    
                    **Desventajas:**
                    - No considera amortización de principal
                    - Basado en EBIT (no cash flow)
                    - Puede variar con tipos de interés
                    
                    **¿Para qué sirve?**
                    - Evaluar riesgo de impago
                    - Comparar capacidad de endeudamiento
                    - Análisis de solvencia
                    """,
                    "ejemplo": "EBIT $50M, Intereses $10M → Interest Coverage = 5.0"
                },
                
                "Total Debt/EBITDA": {
                    "definicion": "**Deuda Total/EBITDA** - Años necesarios para pagar deuda con EBITDA",
                    "calculacion": "Deuda Total ÷ EBITDA",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **<3.0**: Conservador
                    - **3.0-5.0**: Moderado
                    - **5.0-7.0**: Alto
                    - **>7.0**: Muy riesgoso
                    
                    **Ventajas:**
                    - Muy usado por agencias de rating
                    - Considera capacidad operativa de generar caja
                    - Bueno para comparar entre sectores
                    
                    **Desventajas:**
                    - El EBITDA no es flujo de caja
                    - No considera inversiones de capital
                    - Puede variar con ciclo económico
                    
                    **¿Para qué sirve?**
                    - Evaluar sostenibilidad de la deuda
                    - Comparar políticas de endeudamiento
                    - Análisis de riesgo crediticio
                    """,
                    "ejemplo": "Deuda Total $200M, EBITDA $50M → Debt/EBITDA = 4.0"
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

