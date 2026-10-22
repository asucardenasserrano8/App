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


def mostrar_riesgo_avanzado_edu(stonk, ticker, info, nombre, descripcion, start_date, end_date):
            st.subheader("⚡ Métricas Avanzadas de Riesgo y Rendimiento")
            st.write("**Métricas sofisticadas para análisis profesional**")
            
            metricas_avanzadas = {
                "Beta (Riesgo Sistemático)": {
                    "definicion": "Mide la volatilidad de una acción en relación con el mercado completo.",
                    "formula": "Covarianza(Acción, Mercado) / Varianza(Mercado)",
                    "interpretacion": "**<0.8**: Defensivo | **0.8-1.2**: Neutral | **>1.2**: Agresivo",
                    "uso": "Para determinar qué tan sensible es una acción a los movimientos del mercado."
                },
                "Alpha": {
                    "definicion": "Rendimiento excedente sobre lo esperado dado su nivel de riesgo (Beta).",
                    "formula": "Rendimiento Real - (Beta × Rendimiento Mercado)",
                    "interpretacion": "**Alpha > 0**: Supera expectativas | **Alpha < 0**: No alcanza expectativas",
                    "uso": "Medir la habilidad del gestor o el desempeño anormal."
                },
                "Sharpe Ratio": {
                    "definicion": "Rendimiento excedente por unidad de riesgo total.",
                    "formula": "(Rendimiento - Tasa Libre Riesgo) / Volatilidad",
                    "interpretacion": "**>1.0**: Excelente | **0.5-1.0**: Bueno | **<0.5**: Pobre",
                    "uso": "Comparar fondos o estrategias ajustando por riesgo total."
                },
                "Sortino Ratio": {
                    "definicion": "Similar a Sharpe pero solo considera riesgo bajista (desviación negativa).",
                    "formula": "(Rendimiento - Tasa Libre Riesgo) / Volatilidad Bajista",
                    "interpretacion": "**>2.0**: Excelente | **1.0-2.0**: Bueno | **<1.0**: Mejorable",
                    "uso": "Mejor métrica cuando preocupa más las pérdidas que la volatilidad general."
                },
                "Treynor Ratio": {
                    "definicion": "Rendimiento excedente por unidad de riesgo sistemático (Beta).",
                    "formula": "(Rendimiento - Tasa Libre Riesgo) / Beta",
                    "interpretacion": "Cuanto mayor mejor. Comparar con benchmark del sector.",
                    "uso": "Para carteras diversificadas donde el riesgo no sistemático es mínimo."
                },
                "Information Ratio": {
                    "definicion": "Rendimiento activo por unidad de riesgo activo (tracking error).",
                    "formula": "(Rendimiento Cartera - Rendimiento Benchmark) / Tracking Error",
                    "interpretacion": "**>0.5**: Buen gestor activo | **>0.75**: Excelente gestor",
                    "uso": "Evaluar gestión activa vs benchmark."
                }
            }
            
            for metrica, detalles in metricas_avanzadas.items():
                st.markdown(f"### {metrica}")
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.write(f"**📖 Definición**: {detalles['definicion']}")
                    st.write(f"**🧮 Fórmula**: {detalles['formula']}")
                
                with col2:
                    st.write(f"**📊 Interpretación**: {detalles['interpretacion']}")
                    st.write(f"**🎯 Uso Práctico**: {detalles['uso']}")
                
                # Ejemplos prácticos
                if "Beta" in metrica:
                    st.info("**Ejemplo**: Una acción con Beta 1.5 subirá 15% si el mercado sube 10%, pero caerá 15% si el mercado cae 10%")
                elif "Sharpe" in metrica:
                    st.info("**Ejemplo**: Sharpe 1.2 significa que por cada 1% de riesgo, genera 1.2% de rendimiento excedente")
                elif "Alpha" in metrica:
                    st.info("**Ejemplo**: Alpha 0.05 significa que superó en 5% al rendimiento esperado dado su riesgo")
                
                st.markdown("---")

