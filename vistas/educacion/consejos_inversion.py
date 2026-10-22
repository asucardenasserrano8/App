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


def mostrar_consejos_inversion(stonk, ticker, info, nombre, descripcion, start_date, end_date):
            st.subheader("💡 Consejos Prácticos de Inversión")
            st.write("**Sabiduría probada para tomar mejores decisiones**")
            
            # Consejos organizados por categoría
            categorias_consejos = {
                "🔍 Investigación y Análisis": [
                    "**Conoce el negocio**: Invierte solo en empresas que entiendas completamente",
                    "**Análisis competitivo**: Evalúa ventajas competitivas duraderas (moats)",
                    "**Sector y tendencias**: Invierte en sectores con tailwinds, no headwinds",
                    "**Calidad management**: Investiga el track record del equipo directivo",
                    "**Múltiples métricas**: Nunca bases decisiones en una sola métrica"
                ],
                "📈 Gestión de Riesgo": [
                    "**Diversificación inteligente**: No sobre-diversifiques, pero tampoco pongas todos los huevos en una canasta",
                    "**Tamaño de posición**: Nunca arriesgues más del 5% de tu cartera en una sola idea",
                    "**Stop losses mentales**: Define tu precio de venta antes de comprar",
                    "**Riesgo asimétrico**: Busca oportunidades con upside potencial > downside risk",
                    "**Liquidez**: Considera siempre cuán fácil puedes salir de la inversión"
                ],
                "⏳ Psicología y Disciplina": [
                    "**Paciencia**: El tiempo en el mercado > timing del mercado",
                    "**Control emocional**: El miedo y la codicia son tus peores enemigos",
                    "**Independencia**: Piensa por ti mismo, no sigas la manada",
                    "**Humildad**: Reconoce cuando te equivocas y ajusta",
                    "**Consistencia**: Sigue tu proceso invariablemente"
                ],
                "💰 Valoración y Timing": [
                    "**Margen de seguridad**: Compra con descuento al valor intrínseco",
                    "**Ciclos de mercado**: Entiende en qué fase del ciclo estás",
                    "**Valoración relativa**: Compara siempre con alternativas",
                    "**Catalizadores**: Identifica eventos que puedan mover el precio",
                    "**Patience**: Mejor oportunidad perdida que mala inversión"
                ],
                "📚 Educación Continua": [
                    "**Aprendizaje constante**: Los mercados evolucionan, tú también debes hacerlo",
                    "**Historia financiera**: Estudia burbujas y cracks pasados",
                    "**Mentes brillantes**: Lee a Buffett, Munger, Lynch, Graham",
                    "**Pensamiento crítico**: Cuestiona todo, especialmente tus propias ideas",
                    "**Red de conocimiento**: Rodéate de personas más inteligentes que tú"
                ]
            }
            
            for categoria, consejos in categorias_consejos.items():
                st.markdown(f"### {categoria}")
                for consejo in consejos:
                    st.write(f"• {consejo}")
                st.markdown("---")
            
            # Frases célebres de inversión
            st.markdown("### 💬 Sabiduría de los Grandes Inversores")
            frases = [
                "**Warren Buffett**: 'Sé temeroso cuando otros son codiciosos, y codicioso cuando otros son temerosos.'",
                "**Charlie Munger**: 'La inversión no es fácil. Cualquiera que crea que es fácil es un tonto.'",
                "**Peter Lynch**: 'Detrás de cada acción hay una empresa. Descubre qué está haciendo esa empresa.'",
                "**Benjamin Graham**: 'En el corto plazo, el mercado es una máquina de votación. En el largo plazo, es una máquina de ponderación.'",
                "**Philip Fisher**: 'El stock market está lleno de individuos que saben el precio de todo, pero el valor de nada.'",
                "**John Bogle**: 'No busques la aguja en el pajar. Simplemente compra el pajar.'"
            ]
            
            for frase in frases:
                st.success(frase)

            # Sección de libros recomendados
            st.markdown("---")
            st.subheader("📚 Libros Recomendados para Aprender Más")
        
            libros = {
                "Para Principiantes": [
                    "**El Inversor Inteligente** - Benjamin Graham (la biblia de la inversión value)",
                    "**Un paseo aleatorio por Wall Street** - Burton Malkiel (sobre eficiencia de mercados)",
                    "**Los ensayos de Warren Buffett** - Lawrence Cunningham (sabiduría de Buffett)",
                    "**The Little Book of Common Sense Investing** - John Bogle (inversión indexada)"
                ],
                "Para Nivel Intermedio": [
                    "**Security Analysis** - Benjamin Graham & David Dodd (análisis profundo)",
                    "**Common Stocks and Uncommon Profits** - Philip Fisher (inversión en crecimiento)", 
                    "**The Little Book of Valuation** - Aswath Damodaran (valoración)",
                    "**The Most Important Thing** - Howard Marks (gestión de riesgo)"
                ],
                "Para Avanzados": [
                    "**Value Investing: From Graham to Buffett and Beyond** - Bruce Greenwald",
                    "**Expected Returns** - Antti Ilmanen (teoría moderna de portafolios)",
                    "**The Black Swan** - Nassim Taleb (eventos extremos)",
                    "**Principles** - Ray Dalio (modelos mentales para inversión)"
                ],
                "Análisis Fundamental Específico": [
                    "**Financial Statement Analysis** - Martin Fridson (análisis de estados financieros)",
                    "**The Essays of Warren Buffett** - Lawrence Cunningham (filosofía de inversión)",
                    "**Investment Valuation** - Aswath Damodaran (valoración avanzada)",
                    "**The Intelligent Asset Allocator** - William Bernstein (asignación de activos)"
                ]
            }
        
            for nivel, lista_libros in libros.items():
                st.write(f"**{nivel}:**")
                for libro in lista_libros:
                    st.write(f"• {libro}")

            # Consejos finales mejorados
            st.markdown("---")
            st.subheader("💡 Consejos para Dominar el Análisis Fundamental")
        
            consejos = [
                "**Comienza con lo básico**: Domina primero las 10-15 métricas más importantes de cada sector",
                "**Contexto es clave**: Una métrica por sí sola no te dice mucho. Siempre compara con el sector, historial y competidores",
                "**Tendencias > Niveles absolutos**: Una métrica mejorando consistentemente es más importante que su nivel actual", 
                "**Calidad de ganancias**: Analiza si las ganancias vienen del negocio principal o de eventos extraordinarios",
                "**Flujo de caja vs Ganancias**: Las ganancias son una opinión, el flujo de caja es un hecho",
                "**Apalancamiento prudente**: Un poco de deuda puede ser bueno, demasiada puede ser peligrosa",
                "**Ventajas competitivas**: Busca empresas con márgenes estables/crecientes - indican 'moats' económicos",
                "**Management calidad**: Métricas consistentes suelen indicar buena gestión",
                "**Paciencia**: El análisis fundamental es para inversores, no para traders. Think long-term",
                "**Humildad**: Ninguna métrica es perfecta. Usa múltiples herramientas y mantén escepticismo saludable"
            ]
        
            for i, consejo in enumerate(consejos, 1):
                st.write(f"**{i}.** {consejo}")

            # Resumen final de las 82 métricas
            st.markdown("---")
            st.subheader("📋 Resumen Completo: Las 82 Métricas Fundamentales")
        
            st.write("""
            **💰 VALORACIÓN Y MERCADO (18 métricas)**
            - Market Cap, P/E, Forward P/E, PEG, P/S, P/B, P/FCF
            - EV/EBITDA, EV/Sales, EV/FCF, EPS (ttm), EPS next Y, EPS next Q
            - EPS this Y, EPS next 5Y, EPS past 5Y, Book Value/Share
        
            **📈 RENTABILIDAD Y MÁRGENES (16 métricas)**
            - ROA, ROE, ROI, Gross Margin, Oper. Margin, Profit Margin
            - EBITDA, EBIT, Net Income, Income Tax, Dividend, Dividend %
            - Payout Ratio, EPS Q/Q, Sales Q/Q, Earnings Date
        
            **🏦 DEUDA Y LIQUIDEZ (12 métricas)**
            - Total Debt, Debt/Eq, LT Debt/Eq, Total Debt/EBITDA
            - Current Ratio, Quick Ratio, Cash/Share, Cash Flow/Share
            - Total Cash, Total Cash/Share, Working Capital, Interest Coverage
        
            **📊 EFICIENCIA OPERATIVA (10 métricas)**
            - Asset Turnover, Inventory Turnover, Receivables Turnover
            - Days Inventory, Days Sales Outstanding, Payables Period
            - Cash Conversion Cycle, Fixed Asset Turnover, R&D/Sales, SG&A/Sales
        
            **📈 CRECIMIENTO (8 métricas)**
            - Sales Growth 5Y, EPS Growth 5Y, Sales Growth Q/Q, EPS Growth Q/Q
            - Sales Growth Y/Y, EPS Growth Y/Y, Revenue Growth (ttm), EPS Growth (ttm)
        
            **📊 INDICADORES TÉCNICOS (10 métricas)**
            - Beta, RSI (14), Volatility W, Volatility M, ATR
            - SMA 20, SMA 50, SMA 200, Volume, Avg Volume, Rel Volume
        
            **🏢 DATOS CORPORATIVOS (8 métricas)**
            - Shares Out, Float, Insider Own, Insider Trans
            - Inst Own, Inst Trans, Short Float, Short Ratio
            """)
        
            st.success("**🎯 TOTAL: 82 MÉTRICAS FUNDAMENTALES COMPLETAMENTE EXPLICADAS**")
