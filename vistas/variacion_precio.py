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


def mostrar_seccion_variacion_precio(stonk, ticker, info, nombre, descripcion, start_date, end_date):
    st.header(f"📊 Variación del Precio y Gráfica de Velas de {nombre}")
    
    # MÉTRICAS DE PRECIO
    st.subheader(f"📊 Métricas de Precio - Período Actual")
    
    try:
        # Descargar datos de yfinance (por defecto 5 años para las métricas iniciales)
        start_date_default = end_date - timedelta(days=5 * 365)
        with st.spinner("📊 Cargando histórico de precios..."):
            data = yf.download(stonk, start=start_date_default.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), interval='1d')
        
        if data.empty:
            st.warning("No se encontraron datos para este símbolo")
        else:
            # Organizar datos
            data = data.reset_index()
            
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in data.columns.values]
            
            data.columns = [col.replace(f'_{stonk}', '') for col in data.columns]
            
            # MÉTRICAS VISUALES
            if 'Close' in data.columns:
                precio_actual = data['Close'].iloc[-1]
                precio_inicial = data['Close'].iloc[0]
                variacion_total = ((precio_actual - precio_inicial) / precio_inicial) * 100
                
                # Calcular variación del último día
                if len(data) > 1:
                    precio_anterior = data['Close'].iloc[-2]
                    variacion_diaria = ((precio_actual - precio_anterior) / precio_anterior) * 100
                else:
                    variacion_diaria = 0
                
                # Calcular máximo y mínimo del período
                precio_maximo = data['Close'].max()
                precio_minimo = data['Close'].min()
                
                # Calcular volatilidad (desviación estándar de los retornos diarios)
                retornos_diarios = data['Close'].pct_change().dropna()
                volatilidad = retornos_diarios.std() * 100  # En porcentaje
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Precio Inicial", f"${precio_inicial:.2f}")
                    st.metric("Precio Mínimo", f"${precio_minimo:.2f}")
                with col2:
                    st.metric("Precio Actual", f"${precio_actual:.2f}", f"{variacion_diaria:.2f}%")
                    st.metric("Precio Máximo", f"${precio_maximo:.2f}")
                with col3:
                    st.metric("Variación Total", f"{variacion_total:.2f}%")
                    st.metric("Volatilidad Anual", f"{volatilidad:.2f}%")
                with col4:
                    st.metric("Período", "5 Años")
                    st.metric("Días Analizados", len(data))
            
            # Selector de período
            st.subheader("📅 Selecciona el período de análisis")
            
            periodo_opciones = {
                "1 Mes": 30,
                "3 Meses": 90,
                "6 Meses": 180,
                "1 Año": 365,
                "3 Años": 3 * 365,
                "5 Años": 5 * 365,
                "Máximo": None  # Para datos máximos disponibles
            }
            
            periodo_seleccionado = st.selectbox(
                "Período:",
                options=list(periodo_opciones.keys()),
                index=5,  # 5 Años por defecto
                key="selector_periodo"
            )
            
            # Calcular fecha de inicio según el período seleccionado
            if periodo_opciones[periodo_seleccionado] is None:
                # Para período máximo, usar una fecha muy antigua
                start_date = datetime(2000, 1, 1)
                periodo_texto = "Máximo"
            else:
                start_date = end_date - timedelta(days=periodo_opciones[periodo_seleccionado])
                periodo_texto = periodo_seleccionado
            
            # Descargar datos de yfinance
            data_periodo = yf.download(stonk, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), interval='1d')
            
            if not data_periodo.empty:
                data_periodo = data_periodo.reset_index()
                if isinstance(data_periodo.columns, pd.MultiIndex):
                    data_periodo.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in data_periodo.columns.values]
                data_periodo.columns = [col.replace(f'_{stonk}', '') for col in data_periodo.columns]
            
            # Línea separadora entre métricas y gráfica
            st.markdown("---")
            
            # GRÁFICA DE VELAS
            st.subheader(f"📈 Gráfica de Velas - Período: {periodo_texto}")
            
            # Función para obtener nombres de columnas dinámicamente
            def get_column_name(data, prefix):
                for col in data.columns:
                    if col.startswith(prefix):
                        return col
                return None
            
            if not data_periodo.empty:
                # Obtener los nombres dinámicos de las columnas
                open_col = get_column_name(data_periodo, 'Open')
                high_col = get_column_name(data_periodo, 'High') 
                low_col = get_column_name(data_periodo, 'Low')
                close_col = get_column_name(data_periodo, 'Close')
                date_col = get_column_name(data_periodo, 'Date')
                
                # Gráfica de velas
                if all(col is not None for col in [open_col, high_col, low_col, close_col, date_col]):
                    fig = go.Figure(data=[go.Candlestick(
                        x=data_periodo[date_col],
                        open=data_periodo[open_col],
                        high=data_periodo[high_col],
                        low=data_periodo[low_col],
                        close=data_periodo[close_col],
                        increasing_line_color='green',
                        decreasing_line_color='red',
                        name=stonk
                    )])
                    
                    fig.update_layout(
                        title=f'Gráfica de velas de {stonk}',
                        xaxis_title='Fecha',
                        yaxis_title='Precio (USD)',
                        xaxis_rangeslider_visible=False,
                        height=600
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                else:
                    st.warning("No se pudieron cargar los datos para la gráfica de velas")
            
                # DETECTOR DE TENDENCIAS (NUEVO)
                st.markdown("---")
                st.subheader("🔍 Detector de Tendencias")
                
                # Analizar tendencias
                analisis_tendencia = analizar_tendencias(data_periodo)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if analisis_tendencia["tendencia"] == "ALCISTA":
                        st.success(f"📈 Tendencia: {analisis_tendencia['tendencia']}")
                    elif analisis_tendencia["tendencia"] == "BAJISTA":
                        st.error(f"📉 Tendencia: {analisis_tendencia['tendencia']}")
                    else:
                        st.warning(f"➡️ Tendencia: {analisis_tendencia['tendencia']}")
                    
                    st.metric("Confianza", f"{analisis_tendencia['confianza']}%")
                
                with col2:
                    if 'detalles' in analisis_tendencia:
                        detalles = analisis_tendencia['detalles']
                        if 'precio_actual' in detalles:
                            st.metric("Precio Actual", f"${detalles['precio_actual']:.2f}")
                        if 'rsi' in detalles:
                            rsi_color = "green" if detalles['rsi'] < 30 else "red" if detalles['rsi'] > 70 else "orange"
                            st.metric("RSI", f"{detalles['rsi']:.1f}")
                
                with col3:
                    if 'detalles' in analisis_tendencia:
                        detalles = analisis_tendencia['detalles']
                        if all(key in detalles for key in ['sma_20', 'sma_50', 'sma_200']):
                            st.write("**Medias Móviles:**")
                            st.write(f"SMA 20: ${detalles['sma_20']:.2f}")
                            st.write(f"SMA 50: ${detalles['sma_50']:.2f}")
                            st.write(f"SMA 200: ${detalles['sma_200']:.2f}")
                
                # Explicación de la tendencia
                with st.expander("📖 Explicación del Análisis de Tendencia"):
                    st.write("""
                    **Cómo se determina la tendencia:**
                    - **Medias Móviles (40%):** Analiza la posición del precio respecto a las medias de 20, 50 y 200 días
                    - **Posición Precio/Medias (30%):** Evalúa si el precio está por encima o debajo de las medias clave
                    - **Momentum RSI (30%):** Considera si el RSI indica fuerza compradora o vendedora
                    
                    **Interpretación:**
                    - 🟢 **ALCISTA:** Precio por encima de medias, RSI >50, medias alineadas ascendente
                    - 🔴 **BAJISTA:** Precio por debajo de medias, RSI <50, medias alineadas descendente  
                    - 🟡 **LATERAL:** Señales mixtas o sin dirección clara
                    """)
                
                # Línea separadora entre gráfica y tabla
                st.markdown("---")
                
                # TABLA DE DATOS HISTÓRICOS
                st.subheader(f"📋 Datos Históricos Del Período: {periodo_texto}")
                
                # Mostrar información resumida sobre los datos
                st.write(f"**Total de registros:** {len(data_periodo)} días")
                if date_col:
                    st.write(f"**Período:** {data_periodo[date_col].iloc[0].strftime('%d/%m/%Y')} - {data_periodo[date_col].iloc[-1].strftime('%d/%m/%Y')}")
                
                # Agregar las medias móviles (SMA 20, 50 y 200) a la tabla. Se
                # calculan sobre el historial MÁS LARGO que tengamos (los 5 años
                # descargados arriba, o el propio período si es más largo), no
                # solo sobre las filas del período elegido: si no, con un período
                # corto (ej. 1 mes) la SMA 200 saldría vacía porque necesita 200
                # días previos para poder calcularse.
                tabla_historica = data_periodo.copy()
                fuente_sma = data if len(data) >= len(data_periodo) else data_periodo
                fecha_fuente = get_column_name(fuente_sma, 'Date')
                cierre_fuente = get_column_name(fuente_sma, 'Close')
                if date_col and fecha_fuente and cierre_fuente:
                    serie_cierre = fuente_sma.set_index(fecha_fuente)[cierre_fuente]
                    serie_cierre = serie_cierre[~serie_cierre.index.duplicated(keep='last')]
                    for ventana in (20, 50, 200):
                        sma = serie_cierre.rolling(ventana).mean()
                        tabla_historica[f'SMA_{ventana}'] = tabla_historica[date_col].map(sma).round(2)

                st.dataframe(tabla_historica, use_container_width=True)
            
    except Exception as e:
        mostrar_error_amigable(e, "la gráfica de variación del precio")
