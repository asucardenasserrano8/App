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


def mostrar_seccion_riesgo(stonk, ticker, info, nombre, descripcion, start_date, end_date):
    st.header(f"⚠️ Análisis de Riesgo Avanzado De {nombre}")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; padding: 20px; border-radius: 10px; margin: 15px 0;'>
    <h4 style='color: white;'>🔍 EVALUACIÓN COMPLETA DE RIESGOS</h4>
    <p>Análisis profesional de los diferentes tipos de riesgo que afectan a esta inversión</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Obtener métricas de riesgo
    with st.spinner('Calculando métricas avanzadas de riesgo...'):
        metricas_riesgo = calcular_metricas_riesgo_avanzadas(stonk, periodo_años=5)
    
    if metricas_riesgo:
        # =============================================
        # 1. RESUMEN EJECUTIVO DE RIESGO
        # =============================================
        st.subheader("📊 Resumen Ejecutivo de Riesgo")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Clasificación de riesgo general
            score_riesgo = 0
            if metricas_riesgo['Drawdown Máximo'] > 0.4:
                score_riesgo += 3
            elif metricas_riesgo['Drawdown Máximo'] > 0.25:
                score_riesgo += 2
            elif metricas_riesgo['Drawdown Máximo'] > 0.15:
                score_riesgo += 1
                
            if metricas_riesgo['Volatilidad Anual'] > 0.5:
                score_riesgo += 3
            elif metricas_riesgo['Volatilidad Anual'] > 0.3:
                score_riesgo += 2
            elif metricas_riesgo['Volatilidad Anual'] > 0.2:
                score_riesgo += 1
                
            if metricas_riesgo['Beta'] > 1.5:
                score_riesgo += 2
            elif metricas_riesgo['Beta'] > 1.2:
                score_riesgo += 1
            
            if score_riesgo >= 5:
                riesgo_color = "red"
                riesgo_texto = "ALTO RIESGO"
                riesgo_icono = "🔴"
            elif score_riesgo >= 3:
                riesgo_color = "orange"
                riesgo_texto = "RIESGO MODERADO-ALTO"
                riesgo_icono = "🟡"
            elif score_riesgo >= 1:
                riesgo_color = "blue"
                riesgo_texto = "RIESGO MODERADO"
                riesgo_icono = "🔵"
            else:
                riesgo_color = "green"
                riesgo_texto = "BAJO RIESGO"
                riesgo_icono = "🟢"
                
            st.metric("Nivel de Riesgo General", f"{riesgo_icono} {riesgo_texto}")
        
        with col2:
            st.metric("Drawdown Máximo Histórico", f"{metricas_riesgo['Drawdown Máximo']:.1%}")
        
        with col3:
            st.metric("Volatilidad Anual", f"{metricas_riesgo['Volatilidad Anual']:.1%}")
        
        with col4:
            st.metric("Beta vs Mercado", f"{metricas_riesgo['Beta']:.2f}")
        
        # =============================================
        # 2. MÉTRICAS CUANTITATIVAS DE RIESGO
        # =============================================
        st.subheader("📈 Métricas Cuantitativas de Riesgo")

        # Pre-procesar valores para display
        sortino_val = metricas_riesgo.get('Sortino Ratio', 0)
        sortino_display = f"{sortino_val:.2f}" if abs(sortino_val) > 0.01 else f"{sortino_val:.4f}"

        var_val = metricas_riesgo.get('VaR 95% Anual', 0)
        var_display = f"{abs(var_val):.1%}" if abs(var_val) > 0.001 else "< 0.1%"

        skewness_val = metricas_riesgo.get('Skewness', 0)
        skewness_display = f"{skewness_val:.2f}" if abs(skewness_val) > 0.01 else f"{skewness_val:.4f}"

        max_perdida_val = metricas_riesgo.get('Máxima Pérdida Consecutiva', 0)
        max_perdida_display = f"{max_perdida_val} días" if max_perdida_val > 0 else "0 días"

        # Primera fila de métricas
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Sharpe Ratio", f"{metricas_riesgo['Sharpe Ratio']:.2f}",
                    help="Rendimiento por unidad de riesgo total")

        with col2:
            st.metric("Sortino Ratio", sortino_display,
                    help="Rendimiento por unidad de riesgo bajista")

        with col3:
            st.metric("VaR 95% (Anual)", var_display,
                    help="Pérdida máxima esperada en condiciones normales")

        with col4:
            st.metric("Alpha", f"{metricas_riesgo['Alpha']:.2%}",
                    help="Rendimiento excedente sobre el esperado")

        # Segunda fila de métricas
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Correlación S&P500", f"{metricas_riesgo['Correlación S&P500']:.2f}",
                    help="Grado de relación con el mercado")

        with col2:
            st.metric("Probabilidad Pérdida", f"{metricas_riesgo['Probabilidad de Pérdida (%)']:.1f}%",
                    help="% de días con rendimientos negativos")

        with col3:
            st.metric("Máxima Pérdida Consecutiva", max_perdida_display,
                    help="Racha máxima de días negativos")

        with col4:
            st.metric("Skewness", skewness_display,
                    help="Asimetría de la distribución de retornos")
        
        # =============================================
        # 3. ANÁLISIS GRÁFICO DE RIESGO
        # =============================================
        st.subheader("📊 Visualización de Riesgos")
        
        col_grafica1, col_grafica2 = st.columns(2)
        
        with col_grafica1:
            # Gráfica de Drawdown
            st.markdown("**📉 Análisis de Drawdown**")
            grafica_drawdown = crear_grafica_drawdown_mejorada(stonk)
            if grafica_drawdown:
                st.plotly_chart(grafica_drawdown, use_container_width=True)
                st.caption("Evolución histórica de las caídas desde máximos. Áreas rojas indican períodos de pérdidas.")
        
        with col_grafica2:
            # Gráfica de Distribución
            st.markdown("**📊 Distribución de Retornos**")
            grafica_distribucion = crear_grafica_distribucion_retornos(stonk)
            if grafica_distribucion:
                st.plotly_chart(grafica_distribucion, use_container_width=True)
                st.caption("Distribución de ganancias/pérdidas diarias. Línea roja = distribución normal teórica.")
        

        # =============================================
        # 4. COMPARATIVA CON EL MERCADO
        # =============================================
        st.subheader("📈 Comparativa de Riesgo vs Mercado")
        
        col_comp1, col_comp2, col_comp3 = st.columns(3)
        
        with col_comp1:
            vol_vs_mercado = (metricas_riesgo['Volatilidad Anual'] - 0.15) * 100  # 15% volatilidad promedio mercado
            st.metric("Volatilidad vs Mercado", 
                     f"{metricas_riesgo['Volatilidad Anual']:.1%}",
                     f"{vol_vs_mercado:+.1f}%")
        
        with col_comp2:
            beta_interpretacion = "Más volátil" if metricas_riesgo['Beta'] > 1 else "Menos volátil"
            st.metric("Beta vs Mercado", 
                     f"{metricas_riesgo['Beta']:.2f}",
                     beta_interpretacion)
        
        with col_comp3:
            sharpe_mercado = 0.6  # Sharpe promedio mercado
            sharpe_diff = metricas_riesgo['Sharpe Ratio'] - sharpe_mercado
            st.metric("Sharpe vs Mercado", 
                     f"{metricas_riesgo['Sharpe Ratio']:.2f}",
                     f"{sharpe_diff:+.2f}")
        
        # =============================================
        # 5. ALERTAS Y SEÑALES DE RIESGO
        # =============================================
        st.subheader("🚨 Alertas de Riesgo Activas")
        
        alertas = []
        
        # Verificar condiciones de riesgo
        if metricas_riesgo['Drawdown Máximo'] < -0.25:
            alertas.append("🔴 **ALTA ALERTA**: Drawdown histórico > 25%")
        elif metricas_riesgo['Drawdown Máximo'] < -0.15:
            alertas.append("🟡 **ALERTA MODERADA**: Drawdown histórico > 15%")
            
        if metricas_riesgo['Volatilidad Anual'] > 0.40:
            alertas.append("🔴 **ALTA VOLATILIDAD**: > 40% anual")
        elif metricas_riesgo['Volatilidad Anual'] > 0.25:
            alertas.append("🟡 **VOLATILIDAD ELEVADA**: > 25% anual")
            
        if metricas_riesgo['Probabilidad de Pérdida (%)'] > 55:
            alertas.append("🔴 **ALTA FRECUENCIA PÉRDIDAS**: > 55% de días negativos")
        elif metricas_riesgo['Probabilidad de Pérdida (%)'] > 50:
            alertas.append("🟡 **FRECUENCIA PÉRDIDAS ELEVADA**: > 50% de días negativos")
            
        if metricas_riesgo.get('VaR 95% Anual', 0) < -0.30:
            alertas.append("🔴 **VAR EXTREMO**: Pérdida esperada > 30%")
            
        if metricas_riesgo['Beta'] > 1.5:
            alertas.append("🟡 **BETA ALTO**: > 1.5 - Muy sensible al mercado")
        
        if alertas:
            for alerta in alertas:
                st.warning(alerta)
        else:
            st.success("✅ **SIN ALERTAS CRÍTICAS**: Perfil de riesgo dentro de parámetros normales")
        
        # =============================================
        # 6. HISTORIAL DE ESTRESES
        # =============================================
        st.subheader("📅 Historial de Eventos de Estrés")
        
        # Simulación de eventos de estrés (en una app real esto vendría de datos históricos)
        eventos_estres = [
            {"fecha": "2020-03", "evento": "COVID-19", "impacto": "Mercado global -40%"},
            {"fecha": "2022-01", "evento": "Subida tasas Fed", "impacto": "Tech -30%"},
            {"fecha": "2023-03", "evento": "Crisis bancaria", "impacto": "Bancos -25%"}
        ]
        
        for evento in eventos_estres:
            col_fecha, col_evento, col_impacto = st.columns([1, 2, 2])
            with col_fecha:
                st.write(f"**{evento['fecha']}**")
            with col_evento:
                st.write(evento['evento'])
            with col_impacto:
                st.write(evento['impacto'])

        # =============================================
        # 7. ANÁLISIS CUALITATIVO CON IA
        # =============================================
        st.subheader("🤖 Análisis Cualitativo de Riesgo")
        
        with st.spinner('Generando análisis cualitativo con IA...'):
            analisis_ia = generar_analisis_riesgo_ia(stonk, metricas_riesgo, nombre)
            
            if analisis_ia:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px;'>
                <h4 style='color: white;'>ANÁLISIS DE RIESGO POR IA</h4>
                """, unsafe_allow_html=True)
                st.write(analisis_ia)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("""
                **Análisis Cualitativo de Riesgos:**
                
                Basado en las métricas calculadas, aquí tienes un análisis de los riesgos:
                
                **🔴 Riesgos Principales Identificados:**
                - **Drawdown del {:.1f}%**: Indica que históricamente ha tenido caídas significativas
                - **Volatilidad del {:.1f}%**: Sugiere movimientos de precio considerables
                - **Beta de {:.2f}**: {} volatilidad que el mercado
                
                **🟡 Factores a Considerar:**
                - Sharpe Ratio de {:.2f}: {}
                - Probabilidad de pérdida: {:.1f}% de los días
                - Correlación con mercado: {:.2f}
                """.format(
                    metricas_riesgo['Drawdown Máximo'] * 100,
                    metricas_riesgo['Volatilidad Anual'] * 100,
                    metricas_riesgo['Beta'],
                    "Mayor" if metricas_riesgo['Beta'] > 1 else "Menor",
                    metricas_riesgo['Sharpe Ratio'],
                    "Rendimiento ajustado al riesgo positivo" if metricas_riesgo['Sharpe Ratio'] > 0 else "Rendimiento ajustado al riesgo negativo",
                    metricas_riesgo['Probabilidad de Pérdida (%)'],
                    metricas_riesgo['Correlación S&P500']
                ))
        
        # =============================================
        # 8. TIPOS DE RIESGO DETALLADOS
        # =============================================
        st.subheader("🎯 Tipos de Riesgo Específicos")
        
        # Crear pestañas para diferentes tipos de riesgo
        tab1, tab2, tab3, tab4 = st.tabs(["📉 Riesgo de Mercado", "🏦 Riesgo Financiero", "📊 Riesgo Operativo", "🌍 Riesgo Sectorial"])
        
        with tab1:
            st.markdown("""
            **📉 RIESGO DE MERCADO (Sistemático)**
            
            *No diversificable - Afecta a todo el mercado*
            
            **Métricas clave para {}:**
            - **Beta: {:.2f}** - {} sensibilidad a movimientos del mercado
            - **Volatilidad: {:.1f}%** - Nivel de fluctuación de precios
            - **Correlación S&P500: {:.2f}** - Grado de sincronización con el mercado
            - **VaR 95%: {:.1f}%** - Pérdida máxima esperada en condiciones normales
            
            **🔍 Impacto:** {}
            """.format(
                stonk,
                metricas_riesgo['Beta'],
                "Alta" if metricas_riesgo['Beta'] > 1.2 else "Moderada" if metricas_riesgo['Beta'] > 0.8 else "Baja",
                metricas_riesgo['Volatilidad Anual'] * 100,
                metricas_riesgo['Correlación S&P500'],
                metricas_riesgo.get('VaR 95% Anual', 0) * 100,
                "Alta exposición a riesgos de mercado" if metricas_riesgo['Beta'] > 1.2 else "Exposición moderada" if metricas_riesgo['Beta'] > 0.8 else "Baja exposición"
            ))
            
        with tab2:
            # Obtener información financiera para riesgo financiero
            deuda_equity = info.get('debtToEquity', 0)
            current_ratio = info.get('currentRatio', 0)
            interest_coverage = info.get('earningsBeforeInterestAndTaxes', 0) / max(info.get('interestExpense', 1), 1)
            
            st.markdown("""
            **🏦 RIESGO FINANCIERO**
            
            *Relacionado con la estructura de capital y solvencia*
            
            **Métricas clave:**
            - **Deuda/Equity: {:.2f}** - {}
            - **Current Ratio: {:.2f}** - {}
            - **Cobertura de Intereses: {:.1f}x** - {}
            
            **🔍 Evaluación:** {}
            """.format(
                deuda_equity,
                "Alto apalancamiento" if deuda_equity > 2 else "Apalancamiento moderado" if deuda_equity > 1 else "Bajo apalancamiento",
                current_ratio,
                "Buena liquidez" if current_ratio > 1.5 else "Liquidez adecuada" if current_ratio > 1 else "Posibles problemas de liquidez",
                interest_coverage,
                "Cobertura sólida" if interest_coverage > 5 else "Cobertura adecuada" if interest_coverage > 2 else "Cobertura insuficiente",
                "Perfil financiero conservador" if deuda_equity < 1 and current_ratio > 1.5 else "Perfil financiero moderado" if deuda_equity < 2 and current_ratio > 1 else "Perfil financiero agresivo"
            ))
            
        with tab3:
            st.markdown("""
            **📊 RIESGO OPERATIVO**
            
            *Relacionado con las operaciones del negocio*
            
            **Indicadores clave:**
            - **Margen Operativo: {}** - Eficiencia operativa
            - **ROE: {}** - Rentabilidad sobre el capital
            - **Crecimiento Ingresos: {}** - Dinamismo del negocio
            
            **🔍 Factores a monitorear:**
            • Gestión de costos y eficiencia operativa
            • Capacidad de generación de flujo de caja
            • Inversiones en investigación y desarrollo
            • Eficiencia del management
            """.format(
                f"{info.get('operatingMargins', 0)*100:.1f}%" if info.get('operatingMargins') else "N/A",
                f"{info.get('returnOnEquity', 0)*100:.1f}%" if info.get('returnOnEquity') else "N/A",
                f"{info.get('revenueGrowth', 0)*100:.1f}%" if info.get('revenueGrowth') else "N/A"
            ))
            
        with tab4:
            sector = info.get('sector', 'N/A')
            industria = info.get('industry', 'N/A')
            
            st.markdown("""
            **🌍 RIESGO SECTORIAL**
            
            *Riesgos específicos del sector industrial*
            
            **Contexto sectorial:**
            - **Sector:** {}
            - **Industria:** {}
            
            **🔍 Riesgos sectoriales típicos:**
            • Cambios regulatorios del sector
            • Ciclos económicos específicos
            • Disrupción tecnológica
            • Competencia intensiva
            • Dependencia de materias primas
            """.format(sector, industria))
        
        # =============================================
        # 9. RECOMENDACIONES DE GESTIÓN DE RIESGO
        # =============================================
        st.subheader("🛡️ Estrategias de Mitigación de Riesgo")
        
        col_rec1, col_rec2 = st.columns(2)
        
        with col_rec1:
            st.markdown("""
            **✅ PARA RIESGO MODERADO-BAJO:**
            
            • **Diversificación básica**: 15-20 acciones diferentes
            • **Horizonte medio**: 3-5 años de inversión
            • **Monitoreo trimestral**: Revisión periódica
            • **Stop-loss del 15%**: Protección básica
            """)
            
        with col_rec2:
            st.markdown("""
            **⚠️ PARA RIESGO MODERADO-ALTO:**
            
            • **Diversificación amplia**: 25+ acciones
            • **Stop-loss del 10%**: Protección más estricta
            • **Posicionamiento reducido**: Menor exposición
            • **Monitoreo mensual**: Seguimiento cercano
            • **Hedging consideración**: Opciones de protección
            """)
    
        # =============================================
        # 10. PANEL DE CONTROL DE RIESGO
        # =============================================
        st.markdown("---")
        col_ctrl1, col_ctrl2 = st.columns(2)
        
        with col_ctrl1:
            if st.button("🔄 Recalcular Métricas", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
                
        with col_ctrl2:
            # Exportar datos de riesgo
            csv_riesgo = pd.DataFrame([metricas_riesgo]).to_csv(index=False)
            st.download_button(
                label="📥 Exportar Reporte Riesgo",
                data=csv_riesgo,
                file_name=f"riesgo_{stonk}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    else:
        st.error("""
        ❌ No se pudieron calcular las métricas de riesgo para esta acción.
        
        **Posibles causas:**
        • Datos históricos insuficientes
        • Símbolo no válido o no cotizado
        • Problemas de conexión con las fuentes de datos
        
        **Sugerencias:**
        • Verifica que el símbolo sea correcto
        • Intenta con una acción más líquida y conocida
        • Espera unos minutos e intenta nuevamente
        """)
        
        if st.button("🔄 Intentar nuevamente", use_container_width=True):
            st.rerun()

    # =============================================
    # INFORMACIÓN EDUCATIVA SOBRE RIESGOS
    # =============================================
    with st.expander("📚 Guía Educativa: Entendiendo los Riesgos de Inversión", expanded=False):
        st.markdown("""
        ## 🎓 Guía Completa de Análisis de Riesgo
        
        ### 📉 ¿Qué es el Riesgo en Inversiones?
        
        El riesgo es la **posibilidad de perder dinero** en una inversión. Todas las inversiones conllevan algún nivel de riesgo, y generalmente:
        - **Mayor riesgo potencial = Mayor rendimiento potencial**
        - **Menor riesgo potencial = Menor rendimiento potencial**
        
        ### 🎯 Tipos Principales de Riesgo
        
        **1. Riesgo de Mercado (Sistemático)**
        - Afecta a TODO el mercado
        - No se puede eliminar con diversificación
        - Ejemplos: Recesiones, crisis geopolíticas, pandemias
        
        **2. Riesgo Específico (No Sistemático)**
        - Afecta a UNA empresa o sector específico
        - SÍ se puede reducir con diversificación
        - Ejemplos: Mala gestión, problemas legales, huelgas
        
        **3. Riesgo de Liquidez**
        - No poder vender rápidamente sin afectar el precio
        - Común en acciones de baja capitalización
        
        **4. Riesgo de Tasa de Interés**
        - Las subidas de tasas afectan negativamente a las acciones
        
        ### 📊 Métricas Clave Explicadas
        
        **• Volatilidad:** Mide cuánto fluctúa el precio
        - Alta volatilidad = Precio muy variable
        - Baja volatilidad = Precio más estable
        
        **• Drawdown Máximo:** Mayor caída histórica desde un pico
        - Drawdown 25% = Cayó 25% desde su máximo histórico
        - Importante para entender el "peor escenario"
        
        **• Beta:** Sensibilidad vs mercado
        - Beta 1.0 = Se mueve igual que el mercado
        - Beta 1.5 = 50% más volátil que el mercado
        - Beta 0.8 = 20% menos volátil que el mercado
        
        **• Sharpe Ratio:** Rendimiento por unidad de riesgo
        - >1.0 = Buen rendimiento ajustado al riesgo
        - <0 = Mal rendimiento ajustado al riesgo
        
        **• Value at Risk (VaR):** Pérdida máxima esperada
        - VaR 95% = 5% probabilidad de perder más de X%
        - Ayuda a dimensionar posibles pérdidas
        
        ### 🛡️ Estrategias de Gestión de Riesgo
        
        1. **Diversificación:** No poner todos los huevos en una canasta
        2. **Asset Allocation:** Distribuir entre diferentes tipos de activos
        3. **Stop-Loss:** Límites automáticos de pérdida
        4. **Hedging:** Usar instrumentos de protección
        5. **Dollar-Cost Averaging:** Invertir cantidades fijas periódicamente
        
        ### 💡 Consejos Prácticos
        
        - **Conoce tu tolerancia al riesgo** antes de invertir
        - **Diversifica siempre**, incluso en buenas oportunidades
        - **Establece límites de pérdida** antes de comprar
        - **Mantén perspectiva a largo plazo**
        - **Revisa periódicamente** tu exposición al riesgo
        """)
