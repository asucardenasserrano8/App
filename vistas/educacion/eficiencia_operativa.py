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


def mostrar_eficiencia_operativa(stonk, ticker, info, nombre, descripcion, start_date, end_date):
            st.subheader("📊 EFICIENCIA OPERATIVA - 10 Métricas")
            
            metricas = {
                "Asset Turnover": {
                    "definicion": "**Rotación de Activos** - Eficiencia en uso de activos para generar ventas",
                    "calculacion": "Ventas ÷ Activos Totales Promedio",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Alto**: Eficiente uso de activos
                    - **Bajo**: Activos subutilizados
                    - **Creciente**: Mejora en eficiencia
                    
                    **Ventajas:**
                    - Mide eficiencia operativa general
                    - Bueno para comparar empresas del mismo sector
                    - Refleja calidad de gestión
                    
                    **Desventajas:**
                    - Varía mucho entre sectores
                    - Puede estar influido por valoración de activos
                    - No considera rentabilidad
                    
                    **Sectores típicos:**
                    - Retail: 2.0-3.0 (alta rotación)
                    - Manufacturing: 0.8-1.2
                    - Utilities: 0.3-0.5 (activos intensivos)
                    
                    **¿Para qué sirve?**
                    - Evaluar eficiencia operativa
                    - Comparar gestión entre competidores
                    - Identificar mejoras en utilización de activos
                    """,
                    "ejemplo": "Ventas $1B, Activos promedio $500M → Asset Turnover = 2.0"
                },
                
                "Inventory Turnover": {
                    "definicion": "**Rotación de Inventario** - Veces que se renueva el inventario anual",
                    "calculacion": "Costo de Ventas ÷ Inventario Promedio",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Alto**: Gestión eficiente de inventario
                    - **Bajo**: Exceso de inventario o ventas lentas
                    - **Óptimo**: Balance entre disponibilidad y costos
                    
                    **Ventajas:**
                    - Mide eficiencia en gestión de inventario
                    - Buen predictor de problemas operativos
                    - Sensible a cambios en demanda
                    
                    **Desventajas:**
                    - Varía por estacionalidad
                    - Depende del tipo de negocio
                    - Puede ser manipulado con valoración de inventario
                    
                    **Sectores típicos:**
                    - Grocery: 10-15
                    - Retail: 4-8
                    - Manufacturing: 2-4
                    
                    **¿Para qué sirve?**
                    - Evaluar eficiencia operativa
                    - Detectar problemas de ventas
                    - Optimizar niveles de inventario
                    """,
                    "ejemplo": "Costo ventas $600M, Inventario promedio $100M → Inventory Turnover = 6.0"
                },
                
                "Receivables Turnover": {
                    "definicion": "**Rotación de Cuentas por Cobrar** - Eficiencia en cobro a clientes",
                    "calculacion": "Ventas a Crédito ÷ Cuentas por Cobrar Promedio",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Alto**: Cobros rápidos (eficiente)
                    - **Bajo**: Cobros lentos (posibles problemas)
                    - **Decreciente**: Posible deterioro de calidad de clientes
                    
                    **Ventajas:**
                    - Mide eficiencia en gestión de crédito
                    - Indicador de calidad de cartera
                    - Sensible a cambios en políticas de crédito
                    
                    **Desventajas:**
                    - Necesita datos de ventas a crédito (no siempre disponibles)
                    - Puede variar por estacionalidad
                    - No considera morosidad
                    
                    **¿Para qué sirve?**
                    - Evaluar políticas de crédito
                    - Detectar problemas de cobranza
                    - Comparar con términos de pago ofrecidos
                    """,
                    "ejemplo": "Ventas crédito $400M, Cuentas cobrar promedio $50M → Receivables Turnover = 8.0"
                },
                
                "Days Inventory": {
                    "definicion": "**Días de Inventario** - Días promedio que permanece el inventario",
                    "calculacion": "365 ÷ Inventory Turnover",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Bajo**: Inventario que se mueve rápido
                    - **Alto**: Inventario lento o excesivo
                    - **Óptimo**: Balance entre disponibilidad y costos
                    
                    **Ventajas:**
                    - Más intuitivo que turnover
                    - Fácil de comparar con términos de pago
                    - Bueno para gestión operativa
                    
                    **Desventajas:**
                    - Mismo que Inventory Turnover
                    - Sensible a estacionalidad
                    - Puede variar por mix de productos
                    
                    **Sectores típicos:**
                    - Fast food: 2-5 días
                    - Retail: 30-60 días
                    - Manufacturing: 60-90 días
                    
                    **¿Para qué sirve?**
                    - Gestión de niveles de inventario
                    - Evaluar eficiencia operativa
                    - Detectar productos obsoletos
                    """,
                    "ejemplo": "Inventory Turnover 6 → Days Inventory = 61 días"
                },
                
                "Days Sales Outstanding": {
                    "definicion": "**Días de Ventas Pendientes** - Días promedio para cobrar ventas",
                    "calculacion": "365 ÷ Receivables Turnover",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Bajo**: Cobros rápidos (bueno)
                    - **Alto**: Cobros lentos (malo)
                    - **Comparar con términos**: Si DSO > términos, problemas de cobro
                    
                    **Ventajas:**
                    - Fácil de entender y gestionar
                    - Bueno para seguimiento operativo
                    - Sensible a cambios en políticas
                    
                    **Desventajas:**
                    - Puede variar por mix de clientes
                    - Sensible a estacionalidad
                    - No considera morosidad
                    
                    **¿Para qué sirve?**
                    - Evaluar eficiencia de cobranza
                    - Gestionar capital de trabajo
                    - Detectar problemas con clientes
                    """,
                    "ejemplo": "Receivables Turnover 8 → DSO = 46 días"
                },
                
                "Payables Period": {
                    "definicion": "**Período de Pago a Proveedores** - Días promedio para pagar proveedores",
                    "calculacion": "365 ÷ (Compras ÷ Cuentas por Pagar Promedio)",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Alto**: Paga lentamente (usa proveedores como financiación)
                    - **Bajo**: Paga rápidamente (puede perder descuentos)
                    - **Óptimo**: Balance entre relaciones y costos
                    
                    **Ventajas:**
                    - Mide gestión de proveedores
                    - Indica poder de negociación
                    - Afecta capital de trabajo
                    
                    **Desventajas:**
                    - Datos de compras no siempre disponibles
                    - Puede variar por relaciones estratégicas
                    - No considera descuentos por pronto pago
                    
                    **¿Para qué sirve?**
                    - Optimizar capital de trabajo
                    - Evaluar relaciones con proveedores
                    - Comparar con términos de pago
                    """,
                    "ejemplo": "Compras $300M, Cuentas pagar $50M → Payables Period = 61 días"
                },
                
                "Cash Conversion Cycle": {
                    "definicion": "**Ciclo de Conversión de Efectivo** - Días desde pago a proveedores hasta cobro de clientes",
                    "calculacion": "Days Inventory + DSO - Payables Period",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Positivo**: Necesita financiar operaciones
                    - **Negativo**: Proveedores financian operaciones (ideal)
                    - **Bajo**: Eficiente gestión de capital de trabajo
                    
                    **Ventajas:**
                    - Mide eficiencia global de capital de trabajo
                    - Buen predictor de necesidades de financiación
                    - Refleja calidad de gestión operativa
                    
                    **Desventajas:**
                    - Complejo de calcular
                    - Requiere múltiples datos
                    - Puede variar estacionalmente
                    
                    **¿Para qué sirve?**
                    - Evaluar eficiencia operativa global
                    - Gestionar necesidades de financiación
                    - Comparar con competidores
                    """,
                    "ejemplo": "DI 61 + DSO 46 - PP 61 = CCC 46 días"
                },
                
                "Fixed Asset Turnover": {
                    "definicion": "**Rotación de Activos Fijos** - Eficiencia en uso de activos fijos",
                    "calculacion": "Ventas ÷ Activos Fijos Netos Promedio",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Alto**: Uso intensivo de activos fijos
                    - **Bajo**: Activos fijos subutilizados
                    - **Creciente**: Mejora en utilización
                    
                    **Ventajas:**
                    - Enfocado en activos productivos
                    - Bueno para empresas intensivas en capital
                    - Refleja decisiones de inversión
                    
                    **Desventajas:**
                    - Sensible a métodos de depreciación
                    - Varía por antigüedad de activos
                    - No considera mantenimiento
                    
                    **Sectores típicos:**
                    - Retail: 3-5
                    - Manufacturing: 1-2
                    - Utilities: 0.3-0.6
                    
                    **¿Para qué sirve?**
                    - Evaluar eficiencia de inversiones en activos fijos
                    - Comparar utilización de capacidad
                    - Análisis de decisiones de capex
                    """,
                    "ejemplo": "Ventas $1B, Activos fijos promedio $400M → Fixed Asset Turnover = 2.5"
                },
                
                "R&D/Sales": {
                    "definicion": "**Gastos I+D/Ventas** - Porcentaje de ventas invertido en investigación",
                    "calculacion": "Gastos de I+D ÷ Ventas × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Alto**: Empresa innovadora, orientada al futuro
                    - **Bajo**: Empresa madura, poco innovación
                    - **Óptimo**: Balance entre innovación y rentabilidad
                    
                    **Ventajas:**
                    - Mide compromiso con innovación
                    - Bueno para empresas growth
                    - Indicador de ventajas competitivas futuras
                    
                    **Desventajas:**
                    - No garantiza resultados
                    - Puede ser gasto ineficiente
                    - Dificil de comparar entre sectores
                    
                    **Sectores típicos:**
                    - Biotech: 15-25%
                    - Software: 10-20%
                    - Pharma: 12-18%
                    - Industrial: 2-5%
                    
                    **¿Para qué sirve?**
                    - Evaluar estrategia de innovación
                    - Comparar con competidores
                    - Analizar sostenibilidad de ventajas competitivas
                    """,
                    "ejemplo": "I+D $50M, Ventas $500M → R&D/Sales = 10%"
                },
                
                "SG&A/Sales": {
                    "definicion": "**Gastos Generales/Ventas** - Eficiencia en gastos operativos",
                    "calculacion": "Gastos de Venta, Generales y Administrativos ÷ Ventas × 100",
                    "interpretacion": """
                    **¿Qué significa?**
                    - **Alto**: Estructura costosa, posible ineficiencia
                    - **Bajo**: Estructura lean, eficiente
                    - **Decreciente**: Mejora en eficiencia operativa
                    
                    **Ventajas:**
                    - Mide eficiencia en gastos operativos
                    - Bueno para detectar burocracia
                    - Sensible a economías de escala
                    
                    **Desventajas:**
                    - Puede incluir gastos estratégicos
                    - Varía por modelo de negocio
                    - Reducciones excesivas pueden dañar crecimiento
                    
                    **Sectores típicos:**
                    - Software: 20-30%
                    - Retail: 15-25%
                    - Manufacturing: 10-15%
                    
                    **¿Para qué sirve?**
                    - Evaluar eficiencia operativa
                    - Identificar oportunidades de mejora
                    - Comparar estructura de costos
                    """,
                    "ejemplo": "SG&A $120M, Ventas $500M → SG&A/Sales = 24%"
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

