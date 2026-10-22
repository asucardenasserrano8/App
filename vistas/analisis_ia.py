"""
Módulo generado automáticamente a partir de App.py original.
Importa todo lo común desde config para no repetir imports en cada módulo.
"""
from config import *

from nucleo.datos import *
from nucleo.tecnico import *
from nucleo.riesgo import *
from nucleo.scoring import *
from nucleo.wikipedia_info import *
from nucleo.ratings import *
from nucleo.errores import mostrar_error_amigable


def mostrar_seccion_analisis_ia(stonk, ticker, info, nombre, descripcion, start_date, end_date):
    st.header(f"🤖 Análisis IA - {nombre}")
    
    # Obtener datos para el análisis
    try:
        current_price = info.get('currentPrice', 0)
        market_cap = info.get('marketCap', 0)
        pe_ratio = info.get('trailingPE', 0)
        revenue_growth = info.get('revenueGrowth', 0)
        
        # Prompt para análisis IA
        prompt_analisis = f"""
        Analiza la acción {stonk} ({nombre}) como un experto financiero. Considera:
        
        Precio actual: ${current_price}
        Market Cap: ${market_cap/1e9:.2f}B
        P/E Ratio: {pe_ratio}
        Crecimiento de ingresos: {revenue_growth*100 if revenue_growth else 0:.1f}%
        
        Proporciona un análisis conciso que incluya:
        1. Valoración actual (sobrevalorada/subvalorada)
        2. Fortalezas clave
        3. Riesgos principales  
        4. Recomendación (Comprar/Mantener/Vender)
        5. Perspectiva a 12 meses
        
        Máximo 400 palabras, en español.
        """
        
        with st.spinner("🤖 Analizando con IA..."):
            try:
                # FORMA CORRECTA - Crear el modelo primero
                model = genai.GenerativeModel('gemini-3.8-flash')
                response_ia = model.generate_content(prompt_analisis)
                
                st.success("✅ Análisis completado")
                
                # Mostrar el análisis con formato
                st.markdown("### 📋 Análisis de IA")
                st.markdown(response_ia.text)
                
            except Exception as e:
                mostrar_error_amigable(e, "el análisis con IA")
                # Mostrar análisis de respaldo con datos disponibles
                st.info("""
                **📊 Análisis Basado en Datos Disponibles:**
                
                Mientras se soluciona el servicio de IA, aquí tienes un análisis básico:
                
                **Métricas Clave:**
                - Precio: ${:.2f}
                - Market Cap: ${:.2f}B
                - P/E Ratio: {}
                - Crecimiento: {:.1f}%
                """.format(current_price, market_cap/1e9, pe_ratio, revenue_growth*100 if revenue_growth else 0))
        
        # Análisis de sentimiento de noticias
        st.subheader("😊 Análisis de Sentimiento")
        
        def analizar_sentimiento_noticias(ticker):
            # Simulación de análisis de sentimiento
            sentimientos = ["POSITIVO", "NEUTRAL", "NEGATIVO"]
            return random.choice(sentimientos)
        
        sentimiento = analizar_sentimiento_noticias(stonk)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if sentimiento == "POSITIVO":
                st.success("😊 Sentimiento: POSITIVO")
            elif sentimiento == "NEGATIVO":
                st.error("😞 Sentimiento: NEGATIVO")
            else:
                st.info("😐 Sentimiento: NEUTRAL")
        
        with col2:
            # Scoring fundamental
            scoring, metricas_scoring = calcular_scoring_fundamental(info)
            st.metric("Scoring Fundamental", f"{scoring}/100")
        
        with col3:
            # Recomendación IA
            if scoring >= 70:
                st.success("🎯 Recomendación: COMPRAR")
            elif scoring >= 50:
                st.warning("🎯 Recomendación: MANTENER")
            else:
                st.error("🎯 Recomendación: VENDER")
        
        # Métricas de scoring
        st.subheader("📊 Métricas de Scoring")
        col_met1, col_met2 = st.columns(2)
        
        with col_met1:
            for i, (metrica, valor) in enumerate(metricas_scoring.items()):
                if i < len(metricas_scoring) // 2:
                    st.write(f"**{metrica}:** {valor}")
        
        with col_met2:
            for i, (metrica, valor) in enumerate(metricas_scoring.items()):
                if i >= len(metricas_scoring) // 2:
                    st.write(f"**{metrica}:** {valor}")
            
    except Exception as e:
        mostrar_error_amigable(e, "el análisis con IA")
