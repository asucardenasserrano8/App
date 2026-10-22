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


def mostrar_seccion_comparacion(stonk, ticker, info, nombre, descripcion, start_date, end_date):
    st.header(f"📈 Comparar {nombre} con Otras Acciones")
    
    # INPUTS MEJORADOS PARA LAS ACCIONES A COMPARAR
    st.subheader("🔍 Selecciona las acciones para comparar")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        accion1 = st.text_input("Acción 1", value="AAPL", key="accion1")
    with col2:
        accion2 = st.text_input("Acción 2", value="GOOGL", key="accion2")
    with col3:
        accion3 = st.text_input("Acción 3", value="AMZN", key="accion3")
    with col4:
        accion4 = st.text_input("Acción 4", value="TSLA", key="accion4")
    with col5:
        # MÚLTIPLES ÍNDICES Y MONEDAS DE REFERENCIA (antes solo se podía uno)
        indices_referencia = st.multiselect(
            "Índices/Monedas de Referencia:",
            options=["S&P500", "NASDAQ", "DOW JONES", "RUSSELL 2000",
                     "EUR/USD", "USD/JPY", "USD/MXN", "GBP/USD"],
            default=["S&P500"],
            help="Puedes elegir más de uno para comparar varios a la vez",
        )
    
    # SELECTOR DE PERÍODO
    st.subheader("📅 Configuración de Análisis")
    
    col_periodo, col_metricas = st.columns(2)
    
    with col_periodo:
        periodo_opciones = {
            "1 Mes": 30,
            "3 Meses": 90,
            "6 Meses": 180,
            "1 Año": 365,
            "3 Años": 3 * 365,
            "5 Años": 5 * 365,
            "10 Años": 10 * 365
        }
        
        periodo_seleccionado = st.selectbox(
            "Período de Comparación:",
            options=list(periodo_opciones.keys()),
            index=4,  # 3 Años por defecto
            key="selector_periodo_comparacion"
        )
    
    with col_metricas:
        # MÉTRICAS ADICIONALES PARA COMPARACIÓN
        metricas_adicionales = st.multiselect(
            "Métricas Adicionales:",
            options=["Volatilidad", "Sharpe Ratio", "Drawdown Máximo", "Beta"],
            default=["Volatilidad", "Sharpe Ratio"],
            help="Selecciona métricas adicionales para comparar"
        )
    
    # MAPA DE ÍNDICES Y MONEDAS
    indices_map = {
        "S&P500": "^GSPC",
        "NASDAQ": "^IXIC", 
        "DOW JONES": "^DJI",
        "RUSSELL 2000": "^RUT",
        "EUR/USD": "EURUSD=X",
        "USD/JPY": "JPY=X",
        "USD/MXN": "MXN=X",
        "GBP/USD": "GBPUSD=X",
    }
    
    indices_symbols = [indices_map[i] for i in indices_referencia]
    # El primero de la lista se usa como referencia única para Beta y CAPM
    # (esas métricas se calculan contra UN solo mercado por definición). Los
    # demás que elijas se agregan igual a la tabla y gráfica comparativa.
    indice_symbol = indices_symbols[0] if indices_symbols else "^GSPC"
    if len(indices_symbols) > 1:
        st.caption(
            f"ℹ️ Beta y CAPM se calculan contra **{indices_referencia[0]}** "
            f"(el primero de tu selección). El resto se incluye en la "
            f"comparación de rendimiento, volatilidad y drawdown."
        )
    
    # Calcular fecha de inicio
    start_date_comparacion = end_date - timedelta(days=periodo_opciones[periodo_seleccionado])
    
    # BOTÓN PARA EJECUTAR LA COMPARACIÓN
    if st.button("🔄 Ejecutar Análisis Comparativo Avanzado", use_container_width=True):
        with st.spinner('Cargando datos y calculando métricas comparativas...'):
            # LISTA DE TODAS LAS ACCIONES A COMPARAR
            acciones_comparar = [stonk, accion1, accion2, accion3, accion4]
            acciones_comparar = [accion for accion in acciones_comparar if accion.strip()]
            
            # Agregar índices/monedas seleccionados (puede ser más de uno)
            for simbolo_indice in indices_symbols:
                if simbolo_indice not in acciones_comparar:
                    acciones_comparar.append(simbolo_indice)
            
            nombres_acciones = {}
            datos_comparacion = {}
            metricas_detalladas = {}
            datos_originales = {}  # Para guardar los datos originales para las métricas de riesgo
            
            # OBTENER NOMBRES Y DATOS DE CADA ACCIÓN
            for accion in acciones_comparar:
                if accion.strip():
                    try:
                        # Obtener nombre de la acción
                        if accion in indices_map.values():
                            # Es un índice
                            nombre_idx = [k for k, v in indices_map.items() if v == accion][0]
                            nombres_acciones[accion] = f"📊 {nombre_idx}"
                        else:
                            # Es una acción
                            ticker_temp = yf.Ticker(accion)
                            info_temp = ticker_temp.info
                            nombre_accion = info_temp.get("longName", accion)
                            nombres_acciones[accion] = nombre_accion
                        
                        # Descargar datos históricos
                        data_temp = yf.download(accion, 
                                              start=start_date_comparacion.strftime('%Y-%m-%d'), 
                                              end=end_date.strftime('%Y-%m-%d'),
                                              progress=False)
                        
                        if not data_temp.empty:
                            # Guardar datos originales para métricas de riesgo
                            datos_originales[accion] = data_temp.copy()
                            
                            # Manejar MultiIndex columns
                            if isinstance(data_temp.columns, pd.MultiIndex):
                                close_columns = [col for col in data_temp.columns if 'Close' in col]
                                if close_columns:
                                    precios = data_temp[close_columns[0]]
                                else:
                                    continue
                            else:
                                if 'Close' in data_temp.columns:
                                    precios = data_temp['Close']
                                else:
                                    continue

                            if len(precios) > 0 and not precios.isna().all():
                                # Normalizar los precios a porcentaje de cambio
                                precio_inicial = precios.iloc[0]
                                if precio_inicial > 0:
                                    datos_comparacion[accion] = (precios / precio_inicial - 1) * 100
                                    
                                    # CALCULAR MÉTRICAS ADICIONALES
                                    returns = precios.pct_change().dropna()
                                    
                                    # Función para calcular drawdown máximo
                                    def calcular_drawdown_maximo(precios):
                                        try:
                                            rolling_max = precios.expanding().max()
                                            drawdown = (precios - rolling_max) / rolling_max
                                            return drawdown.min() * 100
                                        except:
                                            return 0
                                    
                                    # Función para calcular Sharpe ratio simplificado
                                    def calcular_sharpe_simple(returns, risk_free_rate=0.02):
                                        try:
                                            if len(returns) == 0:
                                                return 0
                                            excess_returns = returns - (risk_free_rate / 252)
                                            sharpe = (excess_returns.mean() / returns.std()) * np.sqrt(252)
                                            return sharpe if not np.isnan(sharpe) else 0
                                        except:
                                            return 0
                                    
                                    metricas_accion = {
                                        'Rendimiento Total': (precios.iloc[-1] / precio_inicial - 1) * 100,
                                        'Volatilidad Anual': returns.std() * np.sqrt(252) * 100,
                                        'Drawdown Máximo': calcular_drawdown_maximo(precios),
                                        'Sharpe Ratio': calcular_sharpe_simple(returns),
                                        'Beta': None,
                                    }
                                    metricas_detalladas[accion] = metricas_accion
                                    
                            else:
                                st.warning(f"⚠️ No hay datos válidos para {accion}")
                        else:
                            st.warning(f"⚠️ No se encontraron datos para {accion}")
                                                        
                    except Exception as e:
                        mostrar_error_amigable(e, f"la carga de datos de {accion}")

            # CALCULAR BETA (con respaldo del Beta de Yahoo Finance si el cálculo manual falla)
            if indice_symbol in datos_comparacion:
                for accion in [a for a in acciones_comparar if a != indice_symbol]:
                    if accion in datos_comparacion:
                        beta_calculada = None
                        try:
                            stock_returns = datos_comparacion[accion].pct_change().dropna()
                            index_returns = datos_comparacion[indice_symbol].pct_change().dropna()

                            common_dates = stock_returns.index.intersection(index_returns.index)
                            if len(common_dates) > 5:
                                stock_returns = stock_returns.loc[common_dates]
                                index_returns = index_returns.loc[common_dates]

                                covariance = np.cov(stock_returns, index_returns)[0, 1]
                                index_variance = np.var(index_returns)
                                if index_variance != 0 and not (np.isnan(covariance) or np.isnan(index_variance)):
                                    beta_calculada = covariance / index_variance
                        except Exception:
                            beta_calculada = None

                        if beta_calculada is None or (isinstance(beta_calculada, float) and np.isnan(beta_calculada)):
                            # Respaldo: Beta que ya reporta Yahoo Finance para esta acción
                            try:
                                beta_calculada = yf.Ticker(accion).info.get('beta')
                            except Exception:
                                beta_calculada = None

                        if beta_calculada is not None and not (isinstance(beta_calculada, float) and np.isnan(beta_calculada)):
                            metricas_detalladas[accion]['Beta'] = beta_calculada

            # VERIFICAR QUE HAYA DATOS PARA COMPARAR
            if len(datos_comparacion) > 1:
                st.success(f"✅ Comparando {len([a for a in acciones_comparar if a in datos_comparacion])} instrumentos")
                
                # GUARDAR DATOS EN SESSION_STATE PARA USAR EN CAPM
                st.session_state.datos_comparacion = datos_comparacion
                st.session_state.nombres_acciones = nombres_acciones
                st.session_state.metricas_detalladas = metricas_detalladas
                st.session_state.acciones_comparar = acciones_comparar
                st.session_state.indice_symbol = indice_symbol
                st.session_state.indice_referencia = indices_referencia[0] if indices_referencia else "S&P500"
                st.session_state.comparacion_realizada = True

    # MOSTRAR RESULTADOS DE COMPARACIÓN SI EXISTEN
    if hasattr(st.session_state, 'comparacion_realizada') and st.session_state.comparacion_realizada:
        datos_comparacion = st.session_state.datos_comparacion
        nombres_acciones = st.session_state.nombres_acciones
        metricas_detalladas = st.session_state.metricas_detalladas
        acciones_comparar = st.session_state.acciones_comparar
        indice_symbol = st.session_state.indice_symbol
        indice_referencia = st.session_state.indice_referencia
        
        # GRÁFICA DE LÍNEAS COMPARATIVA
        st.subheader("📊 Gráfica de Comparación - Rendimiento Relativo")
        
        fig = go.Figure()
        
        colores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', "#ffffff", '#e377c2']
        
        for i, (accion, datos) in enumerate(datos_comparacion.items()):
            if len(datos) > 0:
                nombre_display = nombres_acciones.get(accion, accion)
                color = colores[i % len(colores)]
                
                # Configuración especial para índices
                if accion in indices_map.values():
                    line_width = 4
                    line_dash = "dash"
                    nombre_display = f"📊 {nombre_display}"
                else:
                    line_width = 3
                    line_dash = "solid"
                
                fig.add_trace(go.Scatter(
                    x=datos.index,
                    y=datos.values,
                    mode='lines',
                    name=nombre_display,
                    line=dict(
                        color=color, 
                        width=line_width,
                        dash=line_dash
                    ),
                    hovertemplate=(
                        f"<b>{nombre_display}</b><br>" +
                        "Fecha: %{x}<br>" +
                        "Rendimiento: %{y:.2f}%<br>" +
                        "<extra></extra>"
                    )
                ))
         
        if len(fig.data) > 0:
            fig.update_layout(
                title=f'Comparación de Rendimiento vs {indice_referencia} - Período: {periodo_seleccionado}',
                xaxis_title='Fecha',
                yaxis_title='Rendimiento (%)',
                height=600,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # ANÁLISIS COMPARATIVO
            st.subheader("📈 Análisis de Performance vs Índice")
            
            if indice_symbol in datos_comparacion:
                index_data = datos_comparacion[indice_symbol]
                index_final = index_data.iloc[-1] if len(index_data) > 0 else 0
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    mejor_performer = None
                    mejor_rendimiento = -float('inf')
                    
                    for accion, datos in datos_comparacion.items():
                        if accion != indice_symbol:
                            rendimiento_final = datos.iloc[-1] if len(datos) > 0 else 0
                            if rendimiento_final > mejor_rendimiento:
                                mejor_rendimiento = rendimiento_final
                                mejor_performer = accion
                    
                    if mejor_performer:
                        vs_index = mejor_rendimiento - index_final
                        st.metric(
                            "🏆 Mejor Performer", 
                            f"{nombres_acciones.get(mejor_performer, mejor_performer)}",
                            f"{vs_index:+.2f}% vs índice"
                        )
                
                with col2:
                    st.metric(
                        f"📊 Rendimiento {indice_referencia}", 
                        f"{index_final:.2f}%",
                        "Referencia mercado"
                    )
                
                with col3:
                    # Contar acciones que superaron al índice
                    acciones_superiores = 0
                    total_acciones = 0
                    
                    for accion, datos in datos_comparacion.items():
                        if accion != indice_symbol:
                            total_acciones += 1
                            rendimiento_final = datos.iloc[-1] if len(datos) > 0 else 0
                            if rendimiento_final > index_final:
                                acciones_superiores += 1
                    
                    if total_acciones > 0:
                        porcentaje_superiores = (acciones_superiores / total_acciones) * 100
                        st.metric(
                            "📈 Superan Índice", 
                            f"{acciones_superiores}/{total_acciones}",
                            f"{porcentaje_superiores:.1f}%"
                        )
                
                with col4:
                    # Volatilidad promedio vs índice
                    if indice_symbol in metricas_detalladas:
                        vol_index = metricas_detalladas[indice_symbol]['Volatilidad Anual']
                        vol_promedio = np.mean([m['Volatilidad Anual'] for a, m in metricas_detalladas.items() 
                                               if a != indice_symbol])
                        diff_vol = vol_promedio - vol_index
                        
                        st.metric(
                            "📉 Volatilidad Promedio", 
                            f"{vol_promedio:.1f}%",
                            f"{diff_vol:+.1f}% vs índice"
                        )

        # TABLA DE MÉTRICAS COMPARATIVAS
        st.subheader("📋 Métricas Comparativas Detalladas")
        
        # Crear tabla de métricas
        metricas_tabla = []
        for accion in [a for a in acciones_comparar if a in metricas_detalladas]:
            metricas = metricas_detalladas[accion]
            es_indice = accion in indices_map.values()
            
            metricas_tabla.append({
                'Instrumento': nombres_acciones.get(accion, accion),
                'Tipo': 'Índice' if es_indice else 'Acción',
                'Rendimiento (%)': f"{metricas['Rendimiento Total']:.2f}%",
                'Volatilidad (%)': f"{metricas['Volatilidad Anual']:.1f}%",
                'Sharpe Ratio': f"{metricas['Sharpe Ratio']:.2f}",
                'Drawdown Máx (%)': f"{metricas['Drawdown Máximo']:.1f}%",
                'Beta': (
                    f"{metricas['Beta']:.2f}"
                    if (not es_indice and metricas.get('Beta') is not None
                        and not (isinstance(metricas.get('Beta'), float) and np.isnan(metricas.get('Beta'))))
                    else "N/A"
                ),
            })
        
        if metricas_tabla:
            df_metricas = pd.DataFrame(metricas_tabla)
            st.dataframe(df_metricas, use_container_width=True)
            
        # ANÁLISIS DE CORRELACIÓN
        st.subheader("🎯 Análisis Riesgo-Rendimiento")
        
        # Crear gráfica de riesgo-rendimiento
        fig_scatter = go.Figure()
        
        # Definir colores según tipo de instrumento
        for accion in [a for a in acciones_comparar if a in metricas_detalladas]:
            metricas = metricas_detalladas[accion]
            es_indice = accion in indices_map.values()
            
            # Configurar propiedades según tipo
            if es_indice:
                color = 'red'
                simbolo = 'star'
                tamaño = 20
                nombre = nombres_acciones.get(accion, accion)
            else:
                color = 'blue'
                simbolo = 'circle'
                tamaño = 15
                nombre = nombres_acciones.get(accion, accion)
            
            fig_scatter.add_trace(go.Scatter(
                x=[metricas['Volatilidad Anual']],
                y=[metricas['Rendimiento Total']],
                mode='markers+text',
                name=nombre,
                marker=dict(
                    size=tamaño,
                    color=color,
                    symbol=simbolo,
                    line=dict(width=2, color='darkgray')
                ),
                text=nombre,
                textposition="top center",
                hovertemplate=(
                    f"<b>{nombre}</b><br>" +
                    "Volatilidad: %{x:.1f}%<br>" +
                    "Rendimiento: %{y:.2f}%<br>" +
                    "Sharpe: " + f"{metricas['Sharpe Ratio']:.2f}" + "<br>" +
                    "<extra></extra>"
                )
            ))
        
        # Agregar línea de eficiencia teórica
        if len([a for a in acciones_comparar if a not in indices_map.values() and a in metricas_detalladas]) > 1:
            # Calcular línea de tendencia para acciones (excluyendo índices)
            acciones_no_indices = [a for a in acciones_comparar if a not in indices_map.values() and a in metricas_detalladas]
            volatilidades = [metricas_detalladas[a]['Volatilidad Anual'] for a in acciones_no_indices]
            rendimientos = [metricas_detalladas[a]['Rendimiento Total'] for a in acciones_no_indices]
            
            if len(volatilidades) > 1:
                # Calcular línea de tendencia
                z = np.polyfit(volatilidades, rendimientos, 1)
                p = np.poly1d(z)
                
                x_line = np.linspace(min(volatilidades), max(volatilidades), 50)
                y_line = p(x_line)
                
                fig_scatter.add_trace(go.Scatter(
                    x=x_line,
                    y=y_line,
                    mode='lines',
                    name='Línea de Tendencia',
                    line=dict(color='gray', dash='dash', width=1),
                    hovertemplate="Línea de tendencia<extra></extra>"
                ))
        
        fig_scatter.update_layout(
            title='Análisis Riesgo-Rendimiento',
            xaxis_title='Volatilidad Anual (%)',
            yaxis_title='Rendimiento Total (%)',
            height=500,
            showlegend=True,
            hovermode='closest'
        )
        
        # Agregar cuadrantes de referencia
        fig_scatter.add_hline(y=0, line_dash="dot", line_color="green", 
                            annotation_text="Break Even", annotation_position="left")
        
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # INTERPRETACIÓN DEL ANÁLISIS RIESGO-RENDIMIENTO
        st.info("""
        **💡 Interpretación del Gráfico Riesgo-Rendimiento:**
        - **Arriba a la izquierda**: Alto rendimiento con bajo riesgo (Ideal)
        - **Arriba a la derecha**: Alto rendimiento con alto riesgo 
        - **Abajo a la izquierda**: Bajo rendimiento con bajo riesgo (Conservador)
        - **Abajo a la derecha**: Bajo rendimiento con alto riesgo (Evitar)
        - **Estrella roja**: Índice de referencia del mercado
        """)

        # BOTÓN DE DESCARGA
        st.markdown("---")
        st.subheader("💾 Exportar Análisis Comparativo")
        
        # Crear DataFrame para exportación
        df_export = pd.DataFrame()
        for accion, datos in datos_comparacion.items():
            temp_df = pd.DataFrame({
                'Fecha': datos.index,
                nombres_acciones.get(accion, accion): datos.values
            })
            
            if df_export.empty:
                df_export = temp_df
            else:
                df_export = pd.merge(df_export, temp_df, on='Fecha', how='outer')
        
        if not df_export.empty:
            df_export = df_export.sort_values('Fecha').reset_index(drop=True)
            
            csv_comparacion = df_export.to_csv(index=False)
            st.download_button(
                label="📥 Descargar datos de comparación como CSV",
                data=csv_comparacion,
                file_name=f"comparacion_{stonk}_vs_{indice_referencia.lower()}.csv",
                mime="text/csv",
                use_container_width=True
            )

        # =============================================
        # NUEVA SECCIÓN: ANÁLISIS CAPM COMPARATIVO
        # =============================================
        st.markdown("---")
        st.subheader("📊 Análisis CAPM Comparativo")

        # Selectores para CAPM comparativo - CON STATE MANAGEMENT
        st.markdown("**🕐 Configuración del Análisis CAPM:**")

        col_capm1, col_capm2, col_capm3 = st.columns(3)

        with col_capm1:
            # Inicializar en session_state si no existe
            if 'periodo_capm_comp' not in st.session_state:
                st.session_state.periodo_capm_comp = "1 año"
                
            periodo_capm_comp = st.selectbox(
                "Período de datos CAPM:",
                options=["1 mes", "3 meses", "6 meses", "1 año", "2 años", "3 años", "5 años", "10 años"],
                index=3,
                key="periodo_capm_comparar"
            )
            st.session_state.periodo_capm_comp = periodo_capm_comp

        with col_capm2:
            if 'frecuencia_capm_comp' not in st.session_state:
                st.session_state.frecuencia_capm_comp = "Diario"
                
            frecuencia_capm_comp = st.selectbox(
                "Frecuencia de datos CAPM:",
                options=["Diario", "Semanal", "Mensual"],
                index=0,
                key="frecuencia_capm_comparar"
            )
            st.session_state.frecuencia_capm_comp = frecuencia_capm_comp

        with col_capm3:
            if 'tasa_libre_riesgo_comp' not in st.session_state:
                st.session_state.tasa_libre_riesgo_comp = 2.0
            if 'prima_riesgo_mercado_comp' not in st.session_state:
                st.session_state.prima_riesgo_mercado_comp = 6.0
                
            tasa_libre_riesgo_comp = st.number_input(
                "Tasa Libre Riesgo (%)", 
                min_value=0.0, 
                max_value=10.0, 
                value=st.session_state.tasa_libre_riesgo_comp, 
                step=0.1,
                help="Para cálculo CAPM comparativo",
                key="tasa_libre_comp"
            ) / 100
            st.session_state.tasa_libre_riesgo_comp = tasa_libre_riesgo_comp * 100
            
            prima_riesgo_mercado_comp = st.number_input(
                "Prima Riesgo Mercado (%)", 
                min_value=0.0, 
                max_value=15.0, 
                value=st.session_state.prima_riesgo_mercado_comp, 
                step=0.1,
                help="Para cálculo CAPM comparativo",
                key="prima_riesgo_comp"
            ) / 100
            st.session_state.prima_riesgo_mercado_comp = prima_riesgo_mercado_comp * 100

        # BOTÓN PARA CALCULAR CAPM - SEPARADO DEL BOTÓN PRINCIPAL
        if st.button("🧮 Calcular CAPM Comparativo", type="secondary", use_container_width=True):
            with st.spinner('Calculando CAPM comparativo...'):
                # Mapear selecciones a parámetros
                periodo_map = {
                    "1 mes": 30,
                    "3 meses": 90,
                    "6 meses": 180,
                    "1 año": 365,
                    "2 años": 730,
                    "3 años": 1095,
                    "5 años": 1825,
                    "10 años": 3650
                }

                frecuencia_map = {
                    "Diario": "1d",
                    "Semanal": "1wk", 
                    "Mensual": "1mo"
                }

                dias_periodo_comp = periodo_map[st.session_state.periodo_capm_comp]
                intervalo_comp = frecuencia_map[st.session_state.frecuencia_capm_comp]

                # Función para calcular CAPM comparativo
                def calcular_capm_comparativo(simbolo, indice_symbol, dias_periodo, intervalo):
                    """Calcula métricas CAPM para comparación"""
                    try:
                        start_date = datetime.today() - timedelta(days=dias_periodo)
                        end_date = datetime.today()
                        
                        # Descargar datos
                        stock_data = yf.download(simbolo, start=start_date, end=end_date, interval=intervalo)
                        market_data = yf.download(indice_symbol, start=start_date, end=end_date, interval=intervalo)
                        
                        if stock_data.empty or market_data.empty:
                            return None
                        
                        # Obtener precios de cierre
                        if isinstance(stock_data.columns, pd.MultiIndex):
                            stock_close = stock_data[('Close', simbolo)]
                        else:
                            stock_close = stock_data['Close']
                            
                        if isinstance(market_data.columns, pd.MultiIndex):
                            market_close = market_data[('Close', indice_symbol)]
                        else:
                            market_close = market_data['Close']
                        
                        # Calcular rendimientos
                        stock_returns = stock_close.pct_change().dropna()
                        market_returns = market_close.pct_change().dropna()
                        
                        # Alinear fechas
                        common_dates = stock_returns.index.intersection(market_returns.index)
                        stock_returns = stock_returns.loc[common_dates]
                        market_returns = market_returns.loc[common_dates]
                        
                        if len(stock_returns) < 5:
                            return None
                        
                        # Calcular Beta histórico
                        if len(market_returns) > 1:
                            beta_real, intercepto = np.polyfit(market_returns, stock_returns, 1)
                            r_squared = np.corrcoef(market_returns, stock_returns)[0, 1] ** 2
                        else:
                            beta_real = 1.0
                            r_squared = 0
                        
                        # Calcular CAPM
                        costo_capital = st.session_state.tasa_libre_riesgo_comp/100 + beta_real * st.session_state.prima_riesgo_mercado_comp/100
                        
                        return {
                            'beta_historico': beta_real,
                            'r_squared': r_squared,
                            'costo_capital': costo_capital,
                            'puntos_datos': len(stock_returns),
                            'rendimiento_promedio': stock_returns.mean() * 100,
                            'volatilidad': stock_returns.std() * 100,
                            'stock_returns': stock_returns,
                            'market_returns': market_returns,
                            'fechas': common_dates
                        }
                        
                    except Exception as e:
                        mostrar_error_amigable(e, f"el cálculo CAPM de {simbolo}")
                        return None

                # Calcular CAPM para todas las acciones
                datos_capm_comparativo = {}
                
                for accion in [a for a in acciones_comparar if a not in indices_map.values()]:
                    if accion in datos_comparacion:  # Solo acciones con datos válidos
                        datos_capm = calcular_capm_comparativo(accion, indice_symbol, dias_periodo_comp, intervalo_comp)
                        if datos_capm:
                            datos_capm_comparativo[accion] = datos_capm

                # GUARDAR RESULTADOS CAPM EN SESSION_STATE
                st.session_state.datos_capm_comparativo = datos_capm_comparativo
                st.session_state.capm_calculado = True

        # MOSTRAR RESULTADOS CAPM SI EXISTEN
        if hasattr(st.session_state, 'capm_calculado') and st.session_state.capm_calculado:
            datos_capm_comparativo = st.session_state.datos_capm_comparativo
            
            if len(datos_capm_comparativo) > 1:
                st.success(f"✅ CAPM calculado para {len(datos_capm_comparativo)} acciones")

                # =============================================
                # GRÁFICA SCATTER PLOT CAPM COMPARATIVO
                # =============================================
                st.subheader("📈 Gráfica CAPM - Scatter Plot Comparativo")
                
                # Crear gráfica scatter plot comparativa
                fig_scatter_capm = go.Figure()
                
                colores = ["#C25327", "#4EBD38", '#45B7D1', "#912727", "#AD8C20", '#DDA0DD', "#721FAA"]
                
                # Agregar puntos de datos para cada acción
                for i, (accion, datos) in enumerate(datos_capm_comparativo.items()):
                    color = colores[i % len(colores)]
                    
                    # Agregar scatter plot con todos los puntos históricos
                    fig_scatter_capm.add_trace(go.Scatter(
                        x=datos['market_returns'] * 100,  # Rendimiento del mercado
                        y=datos['stock_returns'] * 100,   # Rendimiento de la acción
                        mode='markers',
                        name=f"{nombres_acciones.get(accion, accion)} ({len(datos['stock_returns'])} pts)",
                        marker=dict(
                            size=6,
                            color=color,
                            opacity=0.6,
                            line=dict(width=1, color='darkgray')
                        ),
                        hovertemplate=(
                            f'<b>{nombres_acciones.get(accion, accion)}</b><br>' +
                            'Fecha: %{text}<br>' +
                            'Rend. Mercado: %{x:.2f}%<br>' +
                            'Rend. Acción: %{y:.2f}%<br>' +
                            '<extra></extra>'
                        ),
                        text=[date.strftime('%d/%m/%Y') for date in datos['fechas']],
                        showlegend=True
                    ))
                    
                    # Agregar línea de regresión para cada acción
                    if len(datos['market_returns']) > 1:
                        beta_real = datos['beta_historico']
                        intercepto = np.polyfit(datos['market_returns'], datos['stock_returns'], 1)[1]
                        
                        x_line = np.linspace(datos['market_returns'].min(), datos['market_returns'].max(), 50)
                        y_line = intercepto + beta_real * x_line
                        
                        fig_scatter_capm.add_trace(go.Scatter(
                            x=x_line * 100,
                            y=y_line * 100,
                            mode='lines',
                            name=f"Regresión {nombres_acciones.get(accion, accion)} (β={beta_real:.2f})",
                            line=dict(color=color, width=2, dash='dash'),
                            showlegend=True,
                            hovertemplate=f'Beta: {beta_real:.2f}<extra></extra>'
                        ))

                # Agregar línea CAPM teórica general
                x_capm = np.linspace(-0.2, 0.2, 50)  # Rango razonable para rendimientos
                y_capm = st.session_state.tasa_libre_riesgo_comp/100/252 + 1.0 * (x_capm - st.session_state.tasa_libre_riesgo_comp/100/252)  # Beta = 1 para mercado
                
                fig_scatter_capm.add_trace(go.Scatter(
                    x=x_capm * 100,
                    y=y_capm * 100,
                    mode='lines',
                    name='Línea Mercado (β=1.0)',
                    line=dict(color='black', width=3),
                    hovertemplate='Mercado teórico<extra></extra>'
                ))

                # Línea de referencia en cero
                fig_scatter_capm.add_hline(y=0, line_dash="dot", line_color="gray", opacity=0.5)
                fig_scatter_capm.add_vline(x=0, line_dash="dot", line_color="gray", opacity=0.5)

                fig_scatter_capm.update_layout(
                    title=dict(
                        text=f'CAPM Comparativo - {st.session_state.periodo_capm_comp} ({st.session_state.frecuencia_capm_comp})',
                    ),
                    xaxis_title=f'Rendimiento del Mercado ({indice_referencia}) (%)',
                    yaxis_title='Rendimiento de las Acciones (%)',
                    height=650,
                    margin=dict(t=80, b=120),
                    showlegend=True,
                    hovermode='closest',
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=-0.18,
                        xanchor="center",
                        x=0.5
                    ),
                    xaxis=dict(
                        showgrid=True,
                        gridwidth=1,
                        gridcolor='lightgray',
                        zeroline=True,
                        zerolinewidth=2,
                        zerolinecolor='black'
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridwidth=1,
                        gridcolor='lightgray',
                        zeroline=True,
                        zerolinewidth=2,
                        zerolinecolor='black'
                    )
                )

                st.plotly_chart(fig_scatter_capm, use_container_width=True)

                # Interpretación de la gráfica scatter
                st.info("""
                **💡 Interpretación del Scatter Plot CAPM:**
                
                - **🔵 Puntos**: Cada punto representa un período (día/semana/mes) histórico
                - **📈 Eje X**: Rendimiento del mercado en ese período
                - **📈 Eje Y**: Rendimiento de la acción en ese período  
                - **📊 Líneas punteadas**: Líneas de regresión (Beta histórico de cada acción)
                - **⚫ Línea negra**: Comportamiento teórico del mercado (Beta = 1.0)
                
                **Patrones a observar:**
                - **Puntos alineados con pendiente positiva**: Acción que sigue al mercado
                - **Puntos dispersos**: Acción con comportamiento independiente
                - **Pendiente > 1**: Acción más volátil que el mercado
                - **Pendiente < 1**: Acción menos volátil que el mercado
                """)

                # =============================================
                # TABLA COMPARATIVA CAPM
                # =============================================
                st.subheader("📋 Tabla Comparativa CAPM")
                
                # Crear tabla comparativa
                tabla_comparativa = []
                for accion, datos in datos_capm_comparativo.items():
                    # Obtener Beta de Yahoo Finance para comparación
                    try:
                        ticker_temp = yf.Ticker(accion)
                        info_temp = ticker_temp.info
                        beta_yahoo = info_temp.get('beta', datos['beta_historico'])
                        diferencia_beta = datos['beta_historico'] - beta_yahoo
                    except:
                        beta_yahoo = datos['beta_historico']
                        diferencia_beta = 0
                    
                    # Determinar categoría de riesgo
                    if datos['beta_historico'] < 0.8:
                        categoria_riesgo = "🛡️ Defensiva"
                    elif datos['beta_historico'] < 1.2:
                        categoria_riesgo = "⚖️ Moderada"
                    else:
                        categoria_riesgo = "🚀 Agresiva"
                    
                    # Determinar calidad del ajuste
                    if datos['r_squared'] > 0.7:
                        calidad_ajuste = "✅ Alto"
                    elif datos['r_squared'] > 0.4:
                        calidad_ajuste = "⚠️ Moderado"
                    else:
                        calidad_ajuste = "❌ Bajo"
                    
                    tabla_comparativa.append({
                        'Acción': nombres_acciones.get(accion, accion),
                        'Beta Histórico': f"{datos['beta_historico']:.2f}",
                        'Beta Yahoo': f"{beta_yahoo:.2f}",
                        'Diferencia β': f"{diferencia_beta:+.2f}",
                        'Costo Capital': f"{datos['costo_capital']*100:.1f}%",
                        'R²': f"{datos['r_squared']:.3f}",
                        'Calidad Ajuste': calidad_ajuste,
                        'Categoría Riesgo': categoria_riesgo,
                        'Rend. Promedio': f"{datos['rendimiento_promedio']:.2f}%",
                        'Puntos Datos': datos['puntos_datos']
                    })
                
                # Mostrar tabla
                df_comparativo = pd.DataFrame(tabla_comparativa)
                st.dataframe(df_comparativo, use_container_width=True)

                # =============================================
                # ANÁLISIS COMPARATIVO
                # =============================================
                st.subheader("🎯 Análisis Comparativo CAPM")
                
                col_anal1, col_anal2 = st.columns(2)
                
                with col_anal1:
                    # Encontrar acciones con mejor relación riesgo/retorno
                    st.markdown("**🏆 Mejores Relaciones Riesgo/Retorno:**")
                    
                    # Calcular ratio Sharpe simplificado (retorno/volatilidad)
                    acciones_ratio = []
                    for accion, datos in datos_capm_comparativo.items():
                        if datos['volatilidad'] > 0:
                            ratio = abs(datos['rendimiento_promedio'] / datos['volatilidad'])
                            acciones_ratio.append((accion, ratio, datos['rendimiento_promedio']))
                    
                    # Ordenar por mejor ratio
                    acciones_ratio.sort(key=lambda x: x[1], reverse=True)
                    
                    for i, (accion, ratio, rendimiento) in enumerate(acciones_ratio[:3]):
                        st.write(f"{i+1}. **{nombres_acciones.get(accion, accion)}**")
                        st.write(f"   Ratio: {ratio:.2f} | Rendimiento: {rendimiento:.2f}%")
                
                with col_anal2:
                    # Análisis de consistencia Beta
                    st.markdown("**📊 Consistencia del Beta:**")
                    
                    acciones_consistentes = []
                    for accion, datos in datos_capm_comparativo.items():
                        try:
                            ticker_temp = yf.Ticker(accion)
                            info_temp = ticker_temp.info
                            beta_yahoo = info_temp.get('beta', datos['beta_historico'])
                            diferencia = abs(datos['beta_historico'] - beta_yahoo)
                            acciones_consistentes.append((accion, diferencia, datos['r_squared']))
                        except:
                            continue
                    
                    # Ordenar por menor diferencia (más consistentes)
                    acciones_consistentes.sort(key=lambda x: x[1])
                    
                    for i, (accion, diferencia, r2) in enumerate(acciones_consistentes[:3]):
                        st.write(f"{i+1}. **{nombres_acciones.get(accion, accion)}**")
                        st.write(f"   Dif. β: {diferencia:.2f} | R²: {r2:.3f}")

                # =============================================
                # COMPARATIVA DE BETAS
                # =============================================
                st.subheader("📈 Comparativa de Betas")
                
                fig_betas = go.Figure()
                
                colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
                
                for i, (accion, datos) in enumerate(datos_capm_comparativo.items()):
                    color = colores[i % len(colores)]
                    
                    # Obtener Beta Yahoo
                    try:
                        ticker_temp = yf.Ticker(accion)
                        info_temp = ticker_temp.info
                        beta_yahoo = info_temp.get('beta', datos['beta_historico'])
                    except:
                        beta_yahoo = datos['beta_historico']
                    
                    fig_betas.add_trace(go.Bar(
                        name=nombres_acciones.get(accion, accion),
                        x=['Beta Histórico', 'Beta Yahoo'],
                        y=[datos['beta_historico'], beta_yahoo],
                        marker_color=[color, color],
                        hovertemplate='%{x}: %{y:.2f}<extra></extra>'
                    ))
                
                fig_betas.update_layout(
                    title='Comparativa Beta Histórico vs Beta Yahoo Finance',
                    yaxis_title='Valor Beta (β)',
                    height=500,
                    showlegend=True,
                    barmode='group'
                )
                
                st.plotly_chart(fig_betas, use_container_width=True)

                # =============================================
                # RECOMENDACIONES FINALES CAPM
                # =============================================
                st.markdown("---")
                st.subheader("💡 Recomendaciones de Inversión CAPM")
                
                # Encontrar la acción con mejor perfil riesgo/retorno
                mejor_accion = None
                mejor_puntaje = -float('inf')
                
                for accion, datos in datos_capm_comparativo.items():
                    # Puntaje basado en R², rendimiento y consistencia Beta
                    puntaje = (datos['r_squared'] * 100 + 
                            min(datos['rendimiento_promedio'], 20) +  # Cap rendimiento en 20%
                            (1 - min(abs(datos['beta_historico'] - 1), 1)) * 20)  # Preferir Beta cerca de 1
                    
                    if puntaje > mejor_puntaje:
                        mejor_puntaje = puntaje
                        mejor_accion = accion
                
                if mejor_accion:
                    datos_mejor = datos_capm_comparativo[mejor_accion]
                    st.success(f"""
                    **🏅 MEJOR PERFIL CAPM: {nombres_acciones.get(mejor_accion, mejor_accion)}**
                    
                    • **Costo de capital**: {datos_mejor['costo_capital']*100:.1f}%
                    • **Beta histórico**: {datos_mejor['beta_historico']:.2f}
                    • **Calidad ajuste**: {datos_mejor['r_squared']:.3f}
                    • **Rendimiento promedio**: {datos_mejor['rendimiento_promedio']:.2f}%
                    
                    **Recomendación**: Esta acción muestra la mejor combinación de relación riesgo-retorno y consistencia con el modelo CAPM.
                    """)

                # Exportar datos CAPM
                st.markdown("---")
                st.subheader("💾 Exportar Análisis CAPM Comparativo")
                
                df_export_capm = pd.DataFrame([
                    {
                        'Acción': nombres_acciones.get(accion, accion),
                        'Beta_Historico': datos['beta_historico'],
                        'Costo_Capital_%': datos['costo_capital'] * 100,
                        'R_Cuadrado': datos['r_squared'],
                        'Rendimiento_Promedio_%': datos['rendimiento_promedio'],
                        'Volatilidad_%': datos['volatilidad'],
                        'Puntos_Datos': datos['puntos_datos'],
                        'Periodo': st.session_state.periodo_capm_comp,
                        'Frecuencia': st.session_state.frecuencia_capm_comp
                    }
                    for accion, datos in datos_capm_comparativo.items()
                ])
                
                csv_capm = df_export_capm.to_csv(index=False)
                st.download_button(
                    label="📥 Descargar datos CAPM comparativo (CSV)",
                    data=csv_capm,
                    file_name=f"capm_comparativo_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
            else:
                st.warning("No hay suficientes datos CAPM para realizar la comparación")
