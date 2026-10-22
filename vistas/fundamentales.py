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
from nucleo.fmp import *
from nucleo.ia import mostrar_analisis_ia
from nucleo.errores import mostrar_error_amigable


from vistas.educacion_financiera import mostrar_educacion_financiera


def mostrar_seccion_fundamentales(stonk, ticker, info, nombre, descripcion, start_date, end_date):
    st.header(f"💰 Datos Fundamentales Completos - {nombre}")
    
    # Pestañas para Fundamentales
    tab1, tab2 = st.tabs(["📊 Análisis Fundamental", "🎓 Educación Financiera"])

    with tab1:
        # FUNCIONES PARA EXTRACCIÓN DE DATOS FUNDAMENTALES
        def extraer_tabla_finviz(ticker):
            url = f"https://finviz.com/quote.ashx?t={ticker}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extraer TODOS los datos de la tabla snapshot de Finviz
                    tabla_snapshot = soup.find('table', class_='snapshot-table2')
                    
                    if tabla_snapshot:
                        datos = {}
                        
                        # Extraer en el formato exacto de Finviz (pares clave-valor)
                        filas = tabla_snapshot.find_all('tr')
                        
                        for fila in filas:
                            celdas = fila.find_all('td')
                            for i in range(0, len(celdas) - 1, 2):
                                if i + 1 < len(celdas):
                                    clave = celdas[i].get_text(strip=True)
                                    valor = celdas[i + 1].get_text(strip=True)
                                    if clave and valor:
                                        datos[clave] = valor
                        
                        return datos
                    else:
                        return {}
                else:
                    return {}
                    
            except Exception as e:
                return {}

        # FUNCIÓN PARA CALCULAR SKEWNESS Y KURTOSIS
        def calcular_skewness_kurtosis(returns):
            """
            Calcula skewness y kurtosis de una serie de retornos
            """
            try:
                n = len(returns)
                if n < 4:
                    return 0, 0
                
                mean = np.mean(returns)
                std = np.std(returns)
                
                if std == 0:
                    return 0, 0
                
                # Skewness
                skew = np.sum((returns - mean) ** 3) / (n * std ** 3)
                
                # Kurtosis (Fisher's definition, excess kurtosis)
                kurt = np.sum((returns - mean) ** 4) / (n * std ** 4) - 3
                
                return skew, kurt
                
            except Exception as e:
                return 0, 0

        # FUNCIONES PARA CÁLCULOS DE RIESGO AVANZADOS
        def calcular_metricas_riesgo_avanzadas(ticker_symbol, periodo_años=5):
            """
            Calcula métricas avanzadas de riesgo MEJORADAS para una acción
            """
            try:
                # Descargar datos históricos
                end_date = datetime.today()
                start_date = end_date - timedelta(days=periodo_años * 365)
                
                # Datos de la acción
                stock_data = yf.download(ticker_symbol, start=start_date, end=end_date, interval='1d')
                if stock_data.empty or len(stock_data) == 0:
                    return None
                    
                # Datos del mercado (S&P500 como benchmark)
                market_data = yf.download('^GSPC', start=start_date, end=end_date, interval='1d')
                if market_data.empty or len(market_data) == 0:
                    return None
                
                # Asegurarnos de que tenemos columnas de cierre
                if 'Close' not in stock_data.columns or 'Close' not in market_data.columns:
                    return None
                
                # Calcular rendimientos diarios - manejar MultiIndex
                if isinstance(stock_data.columns, pd.MultiIndex):
                    stock_close = stock_data[('Close', ticker_symbol)]
                else:
                    stock_close = stock_data['Close']
                    
                if isinstance(market_data.columns, pd.MultiIndex):
                    market_close = market_data[('Close', '^GSPC')]
                else:
                    market_close = market_data['Close']
                
                stock_returns = stock_close.pct_change().dropna()
                market_returns = market_close.pct_change().dropna()
                
                # Alinear las fechas
                common_dates = stock_returns.index.intersection(market_returns.index)
                if len(common_dates) == 0:
                    return None
                    
                stock_returns = stock_returns.loc[common_dates]
                market_returns = market_returns.loc[common_dates]
                
                if len(stock_returns) < 30:  # Mínimo de datos
                    return None
                
                # Convertir a arrays numpy para evitar problemas con Series
                stock_returns_array = stock_returns.values
                market_returns_array = market_returns.values
                
                # 1. CALCULAR BETA
                covariance = np.cov(stock_returns_array, market_returns_array)[0, 1]
                market_variance = np.var(market_returns_array)
                beta = covariance / market_variance if market_variance != 0 else 0
                
                # 2. CALCULAR ALPHA
                stock_total_return = (stock_close.iloc[-1] / stock_close.iloc[0] - 1)
                market_total_return = (market_close.iloc[-1] / market_close.iloc[0] - 1)
                alpha = stock_total_return - (beta * market_total_return)
                
                # 3. CALCULAR SHARPE RATIO
                risk_free_rate = 0.02 / 252  # Tasa diaria
                excess_returns = stock_returns_array - risk_free_rate
                sharpe_ratio = (np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252) 
                              if np.std(excess_returns) != 0 else 0)
                
                # 4. CALCULAR SORTINO RATIO
                downside_returns = stock_returns_array[stock_returns_array < 0]
                downside_std = np.std(downside_returns) if len(downside_returns) > 0 else 0
                sortino_ratio = (np.mean(excess_returns) / downside_std * np.sqrt(252) 
                               if downside_std != 0 else 0)
                
                # 5. CALCULAR TREYNOR RATIO
                treynor_ratio = (stock_total_return - 0.02) / beta if beta != 0 else 0
                
                # 6. CALCULAR INFORMATION RATIO
                active_returns = stock_returns_array - market_returns_array
                tracking_error = np.std(active_returns) * np.sqrt(252) if len(active_returns) > 0 else 0
                information_ratio = (stock_total_return - market_total_return) / tracking_error if tracking_error != 0 else 0
                
                # 7. CALCULAR VALUE AT RISK (VaR)
                var_95 = np.percentile(stock_returns_array, 5)
                var_95_annual = var_95 * np.sqrt(252)
                var_99 = np.percentile(stock_returns_array, 1)
                var_99_annual = var_99 * np.sqrt(252)
                
                # 8. CALCULAR EXPECTED SHORTFALL (CVaR)
                cvar_95 = stock_returns_array[stock_returns_array <= var_95].mean()
                cvar_95_annual = cvar_95 * np.sqrt(252) if not np.isnan(cvar_95) else 0
                
                # 9. CALCULAR DRAWDOWN MÁXIMO
                cumulative_returns = (1 + stock_returns).cumprod()
                rolling_max = cumulative_returns.expanding().max()
                drawdown = (cumulative_returns - rolling_max) / rolling_max
                max_drawdown = drawdown.min()
                
                # Calcular duración del drawdown máximo
                max_dd_idx = drawdown.idxmin()
                max_dd_start = drawdown[drawdown == 0].last_valid_index()
                if max_dd_start is not None:
                    max_dd_duration = (max_dd_idx - max_dd_start).days
                else:
                    max_dd_duration = 0
                
                # 10. CALCULAR VOLATILIDAD ANUALIZADA
                volatility_annual = np.std(stock_returns_array) * np.sqrt(252)
                
                # 11. CALCULAR CORRELACIONES CON MÚLTIPLES ÍNDICES 
                correlation_sp500 = np.corrcoef(stock_returns_array, market_returns_array)[0, 1]
                
                # 12. CALCULAR MÁXIMO GANANCIA/PÉRDIDA CONSECUTIVA 
                positive_streak = 0
                negative_streak = 0
                max_positive_streak = 0
                max_negative_streak = 0
                
                for ret in stock_returns_array:
                    if ret > 0:
                        positive_streak += 1
                        negative_streak = 0
                        max_positive_streak = max(max_positive_streak, positive_streak)
                    elif ret < 0:
                        negative_streak += 1
                        positive_streak = 0
                        max_negative_streak = max(max_negative_streak, negative_streak)
                
                # 13. CALCULAR SKEWNESS Y KURTOSIS
                skewness, kurtosis = calcular_skewness_kurtosis(stock_returns_array)
                
                # 14. CALCULAR PROBABILIDAD DE PÉRDIDA
                prob_loss = np.mean(stock_returns_array < 0) * 100
                
                return {
                    # Métricas básicas
                    'Beta': round(beta, 4),
                    'Alpha': round(alpha, 4),
                    'Sharpe Ratio': round(sharpe_ratio, 4),
                    'Sortino Ratio': round(sortino_ratio, 4),
                    'Treynor Ratio': round(treynor_ratio, 4),
                    'Information Ratio': round(information_ratio, 4),
                    
                    # Métricas de riesgo
                    'VaR 95% Diario': round(var_95, 4),
                    'VaR 95% Anual': round(var_95_annual, 4),
                    'VaR 99% Diario': round(var_99, 4),
                    'VaR 99% Anual': round(var_99_annual, 4),
                    'Expected Shortfall 95%': round(cvar_95_annual, 4),
                    'Drawdown Máximo': round(max_drawdown, 4),
                    'Duración Drawdown (días)': max_dd_duration,
                    'Volatilidad Anual': round(volatility_annual, 4),
                    
                    # Correlaciones
                    'Correlación S&P500': round(correlation_sp500, 4),
                    
                    # Estadísticas avanzadas
                    'Máxima Ganancia Consecutiva': max_positive_streak,
                    'Máxima Pérdida Consecutiva': max_negative_streak,
                    'Skewness': round(skewness, 4),
                    'Kurtosis': round(kurtosis, 4),
                    'Probabilidad de Pérdida (%)': round(prob_loss, 2),
                    
                    # Rendimientos
                    'Rendimiento Total': round(stock_total_return, 4),
                    'Rendimiento Mercado': round(market_total_return, 4),
                    'Días Analizados': len(stock_returns),
                    'Período': f"{periodo_años} años"
                }
                
            except Exception as e:
                mostrar_error_amigable(e, "el cálculo de métricas de riesgo")
                return None

        def crear_grafica_drawdown_mejorada(ticker_symbol, periodo_años=5):
            """
            Crea gráfica de drawdown MEJORADA para visualizar pérdidas máximas
            """
            try:
                # Descargar datos
                end_date = datetime.today()
                start_date = end_date - timedelta(days=periodo_años * 365)
                
                stock_data = yf.download(ticker_symbol, start=start_date, end=end_date, interval='1d')
                if stock_data.empty:
                    return None
                
                # Manejar MultiIndex columns
                if isinstance(stock_data.columns, pd.MultiIndex):
                    stock_close = stock_data[('Close', ticker_symbol)]
                else:
                    stock_close = stock_data['Close']
                
                # Calcular drawdown
                returns = stock_close.pct_change().dropna()
                cumulative_returns = (1 + returns).cumprod()
                rolling_max = cumulative_returns.expanding().max()
                drawdown = (cumulative_returns - rolling_max) / rolling_max
                
                # Crear gráfica
                fig = go.Figure()
                
                # Área de drawdown
                fig.add_trace(go.Scatter(
                    x=drawdown.index,
                    y=drawdown * 100,
                    fill='tozeroy',
                    fillcolor='rgba(255, 0, 0, 0.3)',
                    line=dict(color='red', width=2),
                    name='Drawdown',
                    hovertemplate='<b>Drawdown</b><br>Fecha: %{x}<br>Drawdown: %{y:.2f}%<extra></extra>'
                ))
                
                # Línea de máximo anterior
                fig.add_hline(y=0, line_dash="dash", line_color="green", annotation_text="Máximo Anterior")
                
                # Encontrar los 3 mayores drawdowns
                drawdown_sorted = drawdown.sort_values()
                top_drawdowns = drawdown_sorted.head(3)
                
                # Anotar los mayores drawdowns
                for i, (fecha, valor) in enumerate(top_drawdowns.items()):
                    fig.add_annotation(
                        x=fecha,
                        y=valor * 100,
                        text=f"DD {i+1}: {valor*100:.1f}%",
                        showarrow=True,
                        arrowhead=2,
                        bgcolor="red",
                        font=dict(color="white", size=10),
                        yshift=10 if i == 0 else (-20 if i == 1 else 30)
                    )
                
                fig.update_layout(
                    title=f'Análisis de Drawdown - {ticker_symbol}',
                    xaxis_title='Fecha',
                    yaxis_title='Drawdown (%)',
                    height=500,
                    showlegend=True,
                    hovermode='x unified'
                )
                
                return fig
                
            except Exception as e:
                mostrar_error_amigable(e, "la gráfica de drawdown")
                return None

        def crear_grafica_distribucion_retornos(ticker_symbol, periodo_años=5):
            """
            Crea gráfica de distribución de retornos
            """
            try:
                # Descargar datos
                end_date = datetime.today()
                start_date = end_date - timedelta(days=periodo_años * 365)
                
                stock_data = yf.download(ticker_symbol, start=start_date, end=end_date, interval='1d')
                if stock_data.empty:
                    return None
                
                # Manejar MultiIndex columns
                if isinstance(stock_data.columns, pd.MultiIndex):
                    stock_close = stock_data[('Close', ticker_symbol)]
                else:
                    stock_close = stock_data['Close']
                
                # Calcular retornos
                returns = stock_close.pct_change().dropna() * 100  # En porcentaje
                
                # Crear histograma con curva normal
                fig = go.Figure()
                
                # Histograma
                fig.add_trace(go.Histogram(
                    x=returns,
                    nbinsx=50,
                    name='Frecuencia',
                    opacity=0.7,
                    marker_color='lightblue'
                ))
                
                # Calcular distribución normal (aproximación)
                if len(returns) > 0:
                    x_norm = np.linspace(returns.min(), returns.max(), 100)
                    # Aproximación manual de distribución normal
                    mean = np.mean(returns)
                    std = np.std(returns)
                    if std > 0:
                        y_norm = (1/(std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_norm - mean)/std) ** 2)
                        y_norm = y_norm * len(returns) * (returns.max() - returns.min()) / 50  # Escalar
                        
                        # Curva normal
                        fig.add_trace(go.Scatter(
                            x=x_norm,
                            y=y_norm,
                            mode='lines',
                            name='Distribución Normal',
                            line=dict(color='red', width=2)
                        ))
                
                # Línea en cero
                fig.add_vline(x=0, line_dash="dash", line_color="green")
                
                fig.update_layout(
                    title=f'Distribución de Retornos Diarios - {ticker_symbol}',
                    xaxis_title='Retorno Diario (%)',
                    yaxis_title='Frecuencia',
                    height=400,
                    showlegend=True
                )
                
                return fig
                
            except Exception as e:
                mostrar_error_amigable(e, "la gráfica de distribución de retornos")
                return None

        # Mostrar spinner mientras se cargan los datos
        with st.spinner('Cargando datos fundamentales y calculando métricas de riesgo avanzadas...'):
            datos_finviz = extraer_tabla_finviz(stonk)
            # Fuente principal: FMP (API real). Si no trae nada (sin llave,
            # límite alcanzado, o el ticker no aplica), seguimos con Finviz
            # y, si tampoco, con Yahoo Finance — ver buscar_metrica más abajo.
            datos_fmp = obtener_metricas_fmp(stonk)
            metricas_riesgo = calcular_metricas_riesgo_avanzadas(stonk)
            
#            if datos_finviz:
            if datos_finviz or datos_fmp or info:
                st.success(f"✅ Se cargaron {len(datos_finviz)} métricas fundamentales")
                
                # FUNCIÓN INTELIGENTE PARA BUSCAR MÉTRICAS
                def _formatear_pct(x):
                    try:
                        return f"{float(x)*100:.2f}%"
                    except (TypeError, ValueError):
                        return "N/A"

                def _formatear_num(x, decimales=2):
                    try:
                        return f"{float(x):.{decimales}f}"
                    except (TypeError, ValueError):
                        return "N/A"

                def _formatear_grande(x):
                    try:
                        x = float(x)
                        for unidad, div in [("T", 1e12), ("B", 1e9), ("M", 1e6), ("K", 1e3)]:
                            if abs(x) >= div:
                                return f"{x/div:.2f}{unidad}"
                        return f"{x:.2f}"
                    except (TypeError, ValueError):
                        return "N/A"

                def _rsi_actual():
                    try:
                        precios = obtener_datos_accion(stonk)
                        precios_tech = calcular_indicadores_tecnicos(precios)
                        if not precios_tech.empty and "RSI" in precios_tech.columns:
                            return _formatear_num(precios_tech["RSI"].iloc[-1])
                        return "N/A"
                    except Exception:
                        return "N/A"

                def _valor_estado_financiero(ticker_symbol, df_attr, candidatos):
                    """Busca una fila (por nombre aproximado) en un estado financiero
                    de yfinance (balance_sheet o financials) y devuelve su valor más
                    reciente."""
                    try:
                        df = getattr(yf.Ticker(ticker_symbol), df_attr)
                        if df is None or df.empty:
                            return None
                        for candidato in candidatos:
                            for fila in df.index:
                                if candidato.lower() in str(fila).lower():
                                    valor = df.loc[fila].iloc[0]
                                    if pd.notna(valor):
                                        return float(valor)
                        return None
                    except Exception:
                        return None

                def _lt_debt_eq(ticker_symbol):
                    deuda_lp = _valor_estado_financiero(ticker_symbol, "balance_sheet", ["Long Term Debt"])
                    capital = _valor_estado_financiero(
                        ticker_symbol, "balance_sheet", ["Stockholders Equity", "Total Equity"]
                    )
                    if deuda_lp is not None and capital:
                        return _formatear_num(deuda_lp / capital)
                    return "N/A"

                def _roic(ticker_symbol):
                    # Aproximación estándar: NOPAT / Capital Invertido, con una tasa
                    # de impuesto corporativa fija (21%, tasa federal EUA) porque la
                    # tasa efectiva real no siempre está disponible por separado.
                    ebit = _valor_estado_financiero(ticker_symbol, "financials", ["EBIT", "Operating Income"])
                    capital = _valor_estado_financiero(
                        ticker_symbol, "balance_sheet", ["Stockholders Equity", "Total Equity"]
                    )
                    deuda_total = _valor_estado_financiero(ticker_symbol, "balance_sheet", ["Total Debt"]) or 0
                    efectivo = _valor_estado_financiero(
                        ticker_symbol, "balance_sheet", ["Cash And Cash Equivalents", "Cash"]
                    ) or 0
                    if ebit is None or not capital:
                        return "N/A"
                    nopat = ebit * (1 - 0.21)
                    capital_invertido = deuda_total + capital - efectivo
                    if capital_invertido > 0:
                        return _formatear_pct(nopat / capital_invertido)
                    return "N/A"

                def _fallback_yfinance(clave_metrica, info_yf):
                    # Se usa solo cuando Finviz no trae el dato (bloqueo, cambio de
                    # formato en su página, ticker no listado ahí, etc.)
                    mapa = {
                        "Market Cap": lambda: _formatear_grande(info_yf.get("marketCap")),
                        "P/E": lambda: _formatear_num(info_yf.get("trailingPE")),
                        "Forward P/E": lambda: _formatear_num(info_yf.get("forwardPE")),
                        "PEG": lambda: _formatear_num(info_yf.get("trailingPegRatio")),
                        "P/FCF": lambda: _formatear_num(
                            info_yf.get("marketCap") / info_yf.get("freeCashflow")
                            if info_yf.get("marketCap") and info_yf.get("freeCashflow")
                            else None
                        ),
                        "EV/EBITDA": lambda: _formatear_num(info_yf.get("enterpriseToEbitda")),
                        "EV/SALES": lambda: _formatear_num(info_yf.get("enterpriseToRevenue")),
                        "Income": lambda: _formatear_grande(info_yf.get("netIncomeToCommon")),
                        "Sales": lambda: _formatear_grande(info_yf.get("totalRevenue")),
                        "Gross Margin": lambda: _formatear_pct(info_yf.get("grossMargins")),
                        "Oper. Margin": lambda: _formatear_pct(info_yf.get("operatingMargins")),
                        "Profit Margin": lambda: _formatear_pct(info_yf.get("profitMargins")),
                        "Cash/Share": lambda: _formatear_num(info_yf.get("totalCashPerShare")),
                        "Debt/Eq": lambda: _formatear_num((info_yf.get("debtToEquity") or 0) / 100),
                        "ROA": lambda: _formatear_pct(info_yf.get("returnOnAssets")),
                        "ROE": lambda: _formatear_pct(info_yf.get("returnOnEquity")),
                        "LT Debt/Eq": lambda: _lt_debt_eq(stonk),
                        "ROIC": lambda: _roic(stonk),
                        "Beta": lambda: _formatear_num(info_yf.get("beta")),
                        "Volume": lambda: _formatear_grande(info_yf.get("volume") or info_yf.get("averageVolume")),
                        # Estas dos ya las calcula esta misma pantalla más abajo
                        # (métricas de riesgo e indicadores técnicos), así que las
                        # reutilizamos en vez de pedirlas de nuevo a Finviz.
                        "Volatility": lambda: (
                            _formatear_pct(metricas_riesgo.get("Volatilidad Anual"))
                            if metricas_riesgo else "N/A"
                        ),
                        "RSI": lambda: _rsi_actual(),
                    }
                    try:
                        return mapa[clave_metrica]() if clave_metrica in mapa else "N/A"
                    except Exception:
                        return "N/A"

                def buscar_metrica(datos, posibles_claves, clave_metrica=None, info_yf=None, datos_fmp=None):
                    # 1) FMP primero — es una API real, más confiable que el scraping
                    if datos_fmp and clave_metrica and datos_fmp.get(clave_metrica):
                        return datos_fmp[clave_metrica]
                    # 2) Finviz (scraping) como respaldo
                    for clave in posibles_claves:
                        if clave in datos and str(datos[clave]).strip() not in ("", "-"):
                            return datos[clave]
                    # 3) Yahoo Finance como último respaldo
                    if clave_metrica is not None and info_yf is not None:
                        valor_yf = _fallback_yfinance(clave_metrica, info_yf)
                        if valor_yf != "N/A":
                            return valor_yf
                    return "N/A"
                
                # DEFINIR LAS MÉTRICAS QUE QUEREMOS MOSTRAR
                metricas_principales = {
                    # Valoración y Mercado
                    "Market Cap": ["Market Cap", "Mkt Cap"],
                    "P/E": ["P/E", "PE", "P/E Ratio"],
                    "Forward P/E": ["Forward P/E", "Fwd P/E", "Forward PE"],
                    "PEG": ["PEG", "PEG Ratio"],
                    "P/FCF": ["P/FCF", "Price/FCF"],
                    "EV/EBITDA": ["EV/EBITDA", "Enterprise Value/EBITDA"],
                    "EV/SALES": ["EV/Sales", "Enterprise Value/Sales", "EV/S"],
                    
                    # Ingresos y Rentabilidad
                    "Income": ["Income", "Net Income"],
                    "Sales": ["Sales", "Revenue", "Sales Q/Q"],
                    "Gross Margin": ["Gross Margin", "Gross Mgn"],
                    "Oper. Margin": ["Oper. Margin", "Operating Margin", "Oper Mgn"],
                    "Profit Margin": ["Profit Margin", "Profit Mgn", "Net Margin"],
                    
                    # Efectivo y Deuda
                    "Cash/Share": ["Cash/sh", "Cash/Share", "Cash per Share"],
                    "Debt/Eq": ["Debt/Eq", "Debt/Equity", "Total Debt/Equity"],
                    "LT Debt/Eq": ["LT Debt/Eq", "Long Term Debt/Equity"],
                    
                    # Rentabilidad (MANTENEMOS ROIC)
                    "ROA": ["ROA", "Return on Assets"],
                    "ROE": ["ROE", "Return on Equity"],
                    "ROIC": ["ROI", "ROIC", "Return on Investment", "Return on Capital"],
                    
                    # Indicadores Técnicos
                    "Volatility": ["Volatility", "Volatility W", "Volatility M"],
                    "RSI": ["RSI (14)", "RSI", "Relative Strength Index"],
                    "Beta": ["Beta", "Beta"],
                    "Volume": ["Volume", "Avg Volume", "Volume Today"]
                }
                
                # =============================================
                # 1. MÉTRICAS FUNDAMENTALES PRINCIPALES
                # =============================================
                st.subheader("🏢 Métricas Fundamentales Principales")
                
                # Valoración y Mercado
                st.write("#### 💰 Valoración y Mercado")
                cols = st.columns(4)
                valoracion_keys = ["Market Cap", "P/E", "Forward P/E", "PEG", "P/FCF", "EV/EBITDA", "EV/SALES"]
                for i, key in enumerate(valoracion_keys):
                    with cols[i % 4]:
                        valor = buscar_metrica(datos_finviz, metricas_principales[key], key, info, datos_fmp)
                        st.metric(key, valor)
                
                # Ingresos y Rentabilidad
                st.write("#### 📈 Ingresos y Rentabilidad")
                cols = st.columns(4)
                ingresos_keys = ["Income", "Sales", "Gross Margin", "Oper. Margin", "Profit Margin"]
                for i, key in enumerate(ingresos_keys):
                    with cols[i % 4]:
                        valor = buscar_metrica(datos_finviz, metricas_principales[key], key, info, datos_fmp)
                        st.metric(key, valor)
                
                # Deuda y Efectivo
                st.write("#### 🏦 Deuda y Efectivo")
                cols = st.columns(4)
                deuda_keys = ["Cash/Share", "Debt/Eq", "LT Debt/Eq"]
                for i, key in enumerate(deuda_keys):
                    with cols[i % 4]:
                        valor = buscar_metrica(datos_finviz, metricas_principales[key], key, info, datos_fmp)
                        st.metric(key, valor)
                
                # Rentabilidad (CON ROIC)
                st.write("#### 📊 Rentabilidad")
                cols = st.columns(4)
                rentabilidad_keys = ["ROA", "ROE", "ROIC"]
                for i, key in enumerate(rentabilidad_keys):
                    with cols[i % 4]:
                        valor = buscar_metrica(datos_finviz, metricas_principales[key], key, info, datos_fmp)
                        st.metric(key, valor)
                
                # Indicadores Técnicos
                st.write("#### 📈 Indicadores Técnicos")
                cols = st.columns(4)
                tecnicos_keys = ["Volatility", "RSI", "Beta", "Volume"]
                for i, key in enumerate(tecnicos_keys):
                    with cols[i % 4]:
                        valor = buscar_metrica(datos_finviz, metricas_principales[key], key, info, datos_fmp)
                        st.metric(key, valor)
                
                st.markdown("---")
                
                # =============================================
                # 2. MÉTRICAS AVANZADAS DE RIESGO Y RENDIMIENTO
                # =============================================
                if metricas_riesgo:
                    st.subheader("🎯 Métricas Avanzadas de Riesgo y Rendimiento")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        # Beta con interpretación 
                        beta = metricas_riesgo['Beta']
                        if beta < 0.8:
                            interpretacion = "Defensivo"
                            color = "green"
                        elif beta < 1.2:
                            interpretacion = "Neutro"
                            color = "orange"
                        else:
                            interpretacion = "Agresivo"
                            color = "red"
                        
                        st.metric("📊 Beta (Riesgo Sistemático)", f"{beta:.4f}")
                        st.caption(f"*Interpretación: {interpretacion}*")
                        
                        # Alpha 
                        alpha = metricas_riesgo['Alpha']
                        st.metric("α Alpha", f"{alpha:.2%}")
                        st.caption("*Rendimiento vs esperado*")
                    
                    with col2:
                        # Sharpe Ratio 
                        sharpe = metricas_riesgo['Sharpe Ratio']
                        if sharpe > 1.0:
                            color_sharpe = "green"
                        elif sharpe > 0.5:
                            color_sharpe = "orange"
                        else:
                            color_sharpe = "red"
                        
                        st.metric("⚡ Sharpe Ratio", f"{sharpe:.4f}")
                        st.caption("*Rendimiento/riesgo total*")
                        
                        # Sortino Ratio 
                        sortino = metricas_riesgo['Sortino Ratio']
                        st.metric("🎯 Sortino Ratio", f"{sortino:.4f}")
                        st.caption("*Rendimiento/riesgo bajista*")
                    
                    with col3:
                        # Nuevos ratios
                        treynor = metricas_riesgo['Treynor Ratio']
                        st.metric("📈 Treynor Ratio", f"{treynor:.4f}")
                        st.caption("*Rendimiento/riesgo sistemático*")
                        
                        information = metricas_riesgo['Information Ratio']
                        st.metric("ℹ️ Information Ratio", f"{information:.4f}")
                        st.caption("*Rendimiento activo*")
                    
                    with col4:
                        # Rendimiento vs Mercado 
                        rend_stock = metricas_riesgo['Rendimiento Total']
                        rend_mercado = metricas_riesgo['Rendimiento Mercado']
                        diferencia = rend_stock - rend_mercado
                        
                        st.metric("📊 Vs S&P500", f"{diferencia:.2%}")
                        st.caption("*Exceso vs mercado*")
                        
                        # Probabilidad de pérdida
                        prob_loss = metricas_riesgo['Probabilidad de Pérdida (%)']
                        st.metric("📉 Prob. Pérdida", f"{prob_loss:.1f}%")
                        st.caption("*Frecuencia días negativos*")
                    
                    st.markdown("---")
                    
                    # =============================================
                    # 3. MÉTRICAS DE RENDIMIENTO AJUSTADO AL RIESGO
                    # =============================================
                    st.subheader("📈 Métricas de Rendimiento Ajustado al Riesgo")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        # VaR 
                        var_95 = metricas_riesgo['VaR 95% Anual']
                        var_99 = metricas_riesgo['VaR 99% Anual']
                        
                        st.metric("📉 VaR 95% Anual", f"{var_95:.2%}")
                        st.caption("*Pérdida máxima esperada*")
                        st.metric("📉 VaR 99% Anual", f"{var_99:.2%}")
                        st.caption("*Pérdida extrema esperada*")
                    
                    with col2:
                        # Drawdown 
                        max_dd = metricas_riesgo['Drawdown Máximo']
                        dd_duration = metricas_riesgo['Duración Drawdown (días)']
                        
                        st.metric("🔻 Drawdown Máximo", f"{max_dd:.2%}")
                        st.caption("*Peor pérdida histórica*")
                        st.metric("⏱️ Duración DD", f"{dd_duration} días")
                        st.caption("*Tiempo recuperación*")
                    
                    with col3:
                        # Volatilidad y Correlación
                        volatilidad = metricas_riesgo['Volatilidad Anual']
                        correlacion = metricas_riesgo['Correlación S&P500']
                        
                        st.metric("📈 Volatilidad Anual", f"{volatilidad:.2%}")
                        st.caption("*Riesgo total anualizado*")
                        st.metric("🔗 Correlación S&P500", f"{correlacion:.2%}")
                        st.caption("*Movimiento vs mercado*")
                    
                    with col4:
                        # Estadísticas avanzadas
                        cvar = metricas_riesgo['Expected Shortfall 95%']
                        skew = metricas_riesgo['Skewness']
                        
                        st.metric("💀 Expected Shortfall", f"{cvar:.2%}")
                        st.caption("*Pérdida promedio en colas*")
                        st.metric("📊 Skewness", f"{skew:.4f}")
                        st.caption("*Asimetría distribución*")
                    
                    st.markdown("---")
                    
                    # =============================================
                    # 4. ALERTAS DE RIESGO
                    # =============================================
                    st.subheader("🚨 Alertas de Riesgo")
                    
                    alertas = []
                    
                    # Verificar condiciones de riesgo
                    if metricas_riesgo['Drawdown Máximo'] < -0.20:
                        alertas.append("🔴 ALTO RIESGO: Drawdown máximo > 20%")
                    elif metricas_riesgo['Drawdown Máximo'] < -0.10:
                        alertas.append("🟡 RIESGO MODERADO: Drawdown máximo > 10%")
                    
                    if metricas_riesgo['VaR 95% Anual'] < -0.25:
                        alertas.append("🔴 ALTO RIESGO: VaR anual > 25%")
                    
                    if metricas_riesgo['Volatilidad Anual'] > 0.40:
                        alertas.append("🟡 VOLATILIDAD ALTA: > 40% anual")
                    
                    if metricas_riesgo['Probabilidad de Pérdida (%)'] > 50:
                        alertas.append("🔴 ALTA PROBABILIDAD DE PÉRDIDA: > 50%")
                    
                    if alertas:
                        for alerta in alertas:
                            st.warning(alerta)
                    else:
                        st.success("✅ Perfil de riesgo dentro de parámetros normales")
                    
                    st.markdown("---")
                    
                    # =============================================
                    # 5. ANÁLISIS GRÁFICO DE RIESGO
                    # =============================================
                    st.subheader("📈 Análisis Gráfico de Riesgo")

                    col1, col2 = st.columns(2)

                    with col1:
                        # Gráfica de drawdown 
                        st.markdown("**📉 Drawdown - Pérdidas Máximas Históricas**")
                        
                        grafica_drawdown = crear_grafica_drawdown_mejorada(stonk)
                        if grafica_drawdown:
                            st.plotly_chart(grafica_drawdown, use_container_width=True)
                            st.caption("*Visualiza las mayores caídas desde máximos históricos. Áreas rojas indican períodos de pérdidas.*")
                        else:
                            st.warning("No se pudo generar la gráfica de drawdown")

                    with col2:
                        # Gráfica de distribución de retornos
                        st.markdown("**📊 Distribución de Retornos Diarios**")
                        
                        grafica_distribucion = crear_grafica_distribucion_retornos(stonk)
                        if grafica_distribucion:
                            st.plotly_chart(grafica_distribucion, use_container_width=True)
                            st.caption("*Muestra la frecuencia y distribución de ganancias/pérdidas diarias. Línea roja = distribución normal teórica.*")
                        else:
                            st.warning("No se pudo generar la gráfica de distribución")

                    # ANÁLISIS CON IA de lo que muestran las dos gráficas
                    def _pct(valor):
                        try:
                            return f"{float(valor) * 100:.1f}%"
                        except (TypeError, ValueError):
                            return "N/D"

                    def _num(valor, decimales=2):
                        try:
                            return f"{float(valor):.{decimales}f}"
                        except (TypeError, ValueError):
                            return "N/D"

                    prompt_graficas = f"""
                    Eres un analista financiero. Explica en español, de forma clara y breve
                    (máximo 150 palabras, en 3 o 4 viñetas y una conclusión de una línea),
                    qué dicen las dos gráficas de riesgo de {nombre} ({stonk}):
                    1) la gráfica de Drawdown (caídas desde máximos históricos) y
                    2) la distribución de retornos diarios (comparada con una distribución normal).

                    Datos (período {metricas_riesgo.get('Período', 'N/D')}):
                    - Drawdown máximo: {_pct(metricas_riesgo.get('Drawdown Máximo'))}
                    - Duración del peor drawdown: {metricas_riesgo.get('Duración Drawdown (días)', 'N/D')} días
                    - Volatilidad anual: {_pct(metricas_riesgo.get('Volatilidad Anual'))}
                    - VaR 95% anual: {_pct(metricas_riesgo.get('VaR 95% Anual'))}
                    - Expected Shortfall 95%: {_pct(metricas_riesgo.get('Expected Shortfall 95%'))}
                    - Skewness (asimetría): {_num(metricas_riesgo.get('Skewness'))}
                    - Kurtosis: {_num(metricas_riesgo.get('Kurtosis'))}
                    - Probabilidad de pérdida diaria: {_num(metricas_riesgo.get('Probabilidad de Pérdida (%)'), 1)}%

                    Explica qué significa cada dato para un inversionista que no es experto, y si la
                    forma de la distribución (colas gruesas, asimetría) indica más riesgo del que
                    sugiere una distribución normal. Sé objetivo y no des recomendaciones de compra o venta.
                    """
                    mostrar_analisis_ia(
                        f"Interpretación con IA de las gráficas de riesgo de {stonk}",
                        prompt_graficas,
                        "el análisis de las gráficas de riesgo",
                    )

                    st.markdown("---")

                # =============================================
                # 6. MODELO CAPM - COSTO DE CAPITAL
                # =============================================
                st.subheader("📊 Modelo CAPM - Costo de Capital")

                # Configuración de parámetros CAPM
                col_params1, col_params2, col_params3 = st.columns(3)

                with col_params1:
                    tasa_libre_riesgo = st.number_input(
                        "Tasa Libre de Riesgo (%)", 
                        min_value=0.0, 
                        max_value=10.0, 
                        value=2.0, 
                        step=0.1,
                        help="Rendimiento de bonos gubernamentales (10 años)"
                    ) / 100

                with col_params2:
                    prima_riesgo_mercado = st.number_input(
                        "Prima de Riesgo de Mercado (%)", 
                        min_value=0.0, 
                        max_value=15.0, 
                        value=6.0, 
                        step=0.1,
                        help="Rendimiento esperado del mercado sobre tasa libre de riesgo"
                    ) / 100

                with col_params3:
                    # Obtener Beta de Yahoo Finance o usar valor por defecto
                    beta_actual = info.get('beta', 1.0)
                    beta = st.number_input(
                        "Beta (β) de la Acción", 
                        min_value=0.0, 
                        max_value=5.0, 
                        value=float(beta_actual), 
                        step=0.1,
                        help="Riesgo sistemático vs mercado"
                    )

                # Calcular CAPM
                costo_capital = tasa_libre_riesgo + beta * prima_riesgo_mercado

                # Mostrar métricas CAPM
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Tasa Libre Riesgo", 
                        f"{tasa_libre_riesgo*100:.1f}%",
                        "Rf"
                    )

                with col2:
                    st.metric(
                        "Beta (β)", 
                        f"{beta:.2f}",
                        "Riesgo Sistemático"
                    )

                with col3:
                    st.metric(
                        "Prima Riesgo Mercado", 
                        f"{prima_riesgo_mercado*100:.1f}%",
                        "E(Rm) - Rf"
                    )

                with col4:
                    st.metric(
                        "**Costo Capital (CAPM)**", 
                        f"**{costo_capital*100:.1f}%**",
                        "**E(R) = Rf + β×(Rm-Rf)**",
                        delta_color="off"
                    )

                # Gráfica del CAPM - Scatter Plot con datos históricos
                st.subheader("📈 Análisis CAPM - Datos Históricos")

                # SELECTOR DE PERÍODO PARA DATOS HISTÓRICOS
                st.markdown("**🕐 Selecciona el período de análisis:**")

                col_periodo, col_frecuencia = st.columns(2)

                with col_periodo:
                    periodo_capm = st.selectbox(
                        "Período de datos:",
                        options=["1 mes", "3 meses", "6 meses", "1 año", "2 años", "3 años", "5 años", "10 años"],
                        index=3,  # 1 año por defecto
                        key="periodo_capm"
                    )

                with col_frecuencia:
                    frecuencia_capm = st.selectbox(
                        "Frecuencia de datos:",
                        options=["Diario", "Semanal", "Mensual"],
                        index=0,  # Diario por defecto para períodos cortos
                        key="frecuencia_capm"
                    )

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

                dias_periodo = periodo_map[periodo_capm]
                intervalo = frecuencia_map[frecuencia_capm]

                # Ajustar frecuencia automáticamente para períodos muy cortos
                if dias_periodo <= 90 and frecuencia_capm == "Mensual":  # 3 meses o menos
                    st.warning("⚠️ Para períodos cortos (≤ 3 meses) se recomienda frecuencia Diaria o Semanal para mejor análisis")
                    intervalo = "1d"  # Forzar diario para períodos cortos

                st.info(f"**📊 Configuración:** {periodo_capm} | {frecuencia_capm} | {stonk} vs S&P500")

                # Obtener datos históricos según la selección
                try:
                    start_date = datetime.today() - timedelta(days=dias_periodo)
                    end_date = datetime.today()
                    
                    # Descargar datos
                    with st.spinner(f'Cargando datos {frecuencia_capm.lower()} para {periodo_capm}...'):
                        stock_data = yf.download(stonk, start=start_date, end=end_date, interval=intervalo)
                        market_data = yf.download('^GSPC', start=start_date, end=end_date, interval=intervalo)
                    
                    if not stock_data.empty and not market_data.empty:
                        # Obtener precios de cierre
                        if isinstance(stock_data.columns, pd.MultiIndex):
                            stock_close = stock_data[('Close', stonk)]
                        else:
                            stock_close = stock_data['Close']
                            
                        if isinstance(market_data.columns, pd.MultiIndex):
                            market_close = market_data[('Close', '^GSPC')]
                        else:
                            market_close = market_data['Close']
                        
                        # Calcular rendimientos
                        stock_returns = stock_close.pct_change().dropna()
                        market_returns = market_close.pct_change().dropna()
                        
                        # Alinear fechas
                        common_dates = stock_returns.index.intersection(market_returns.index)
                        stock_returns = stock_returns.loc[common_dates]
                        market_returns = market_returns.loc[common_dates]
                        
                        if len(stock_returns) > 5:  # Mínimo reducido para períodos cortos
                            # Crear scatter plot
                            fig_capm = go.Figure()
                            
                            # Determinar color de los puntos basado en la tendencia reciente
                            color_points = 'blue'
                            if len(stock_returns) > 10:
                                # Calcular tendencia reciente para colorear puntos
                                tendencia_reciente = stock_returns.tail(min(10, len(stock_returns))).mean()
                                if tendencia_reciente > 0:
                                    color_points = 'green'
                                else:
                                    color_points = 'red'
                            
                            # Puntos de datos históricos
                            fig_capm.add_trace(go.Scatter(
                                x=market_returns * 100,
                                y=stock_returns * 100,
                                mode='markers',
                                name=f'Datos {frecuencia_capm} ({len(stock_returns)} puntos)',
                                marker=dict(
                                    size=8,
                                    color=color_points,
                                    opacity=0.7,
                                    line=dict(width=1, color='darkgray')
                                ),
                                hovertemplate=(
                                    'Fecha: %{text}<br>' +
                                    'Rendimiento Mercado: %{x:.2f}%<br>' +
                                    'Rendimiento Acción: %{y:.2f}%<br>' +
                                    '<extra></extra>'
                                ),
                                text=[date.strftime('%d/%m/%Y') for date in common_dates]
                            ))
                            
                            # Calcular línea de regresión (Beta histórico)
                            if len(market_returns) > 1:
                                beta_real, intercepto = np.polyfit(market_returns, stock_returns, 1)
                                r_squared = np.corrcoef(market_returns, stock_returns)[0, 1] ** 2
                                
                                # Línea de regresión
                                x_line = np.linspace(market_returns.min(), market_returns.max(), 50)
                                y_line = intercepto + beta_real * x_line
                                
                                fig_capm.add_trace(go.Scatter(
                                    x=x_line * 100,
                                    y=y_line * 100,
                                    mode='lines',
                                    name=f'Beta Histórico = {beta_real:.2f}',
                                    line=dict(color='red', width=3, dash='dash'),
                                    hovertemplate='Beta histórico: {:.2f}<extra></extra>'.format(beta_real)
                                ))
                            
                            # Línea CAPM teórica
                            # Ajustar tasa libre de riesgo según frecuencia
                            if frecuencia_capm == "Diario":
                                rf_ajustado = tasa_libre_riesgo / 252
                            elif frecuencia_capm == "Semanal":
                                rf_ajustado = tasa_libre_riesgo / 52
                            else:  # Mensual
                                rf_ajustado = tasa_libre_riesgo / 12
                                
                            x_capm = np.linspace(market_returns.min(), market_returns.max(), 50)
                            y_capm = rf_ajustado + beta * (x_capm - rf_ajustado)
                            
                            fig_capm.add_trace(go.Scatter(
                                x=x_capm * 100,
                                y=y_capm * 100,
                                mode='lines',
                                name=f'CAPM Teórico (β = {beta:.2f})',
                                line=dict(color='blue', width=3),
                                hovertemplate='CAPM teórico<extra></extra>'
                            ))
                            
                            # Punto de rendimiento esperado actual
                            fig_capm.add_trace(go.Scatter(
                                x=[0],  # Centrado en el origen para mejor visualización
                                y=[costo_capital * 100],
                                mode='markers+text',
                                name='Rendimiento Esperado Anual',
                                marker=dict(size=12, color='orange', symbol='star', line=dict(width=2, color='darkorange')),
                                text=['ESPERADO'],
                                textposition="top center",
                                hovertemplate=f'Rendimiento esperado anual: {costo_capital*100:.1f}%<extra></extra>'
                            ))
                            
                            fig_capm.update_layout(
                                title=f'CAPM - {stonk} vs S&P500 ({periodo_capm}, {frecuencia_capm})',
                                xaxis_title='Rendimiento del Mercado (S&P500) (%)',
                                yaxis_title=f'Rendimiento de {stonk} (%)',
                                height=600,
                                showlegend=True,
                                hovermode='closest',
                                legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=1.02,
                                    xanchor="right",
                                    x=1
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
                            
                            st.plotly_chart(fig_capm, use_container_width=True)
                            
                            # Análisis de la regresión
                            st.subheader("📊 Análisis de Regresión")
                            
                            col_reg1, col_reg2, col_reg3, col_reg4 = st.columns(4)
                            
                            with col_reg1:
                                st.metric("Beta Histórico", f"{beta_real:.2f}")
                                st.caption(f"Calculado con {len(stock_returns)} puntos")
                                
                            with col_reg2:
                                st.metric("Beta Teórico", f"{beta:.2f}")
                                st.caption("Valor de Yahoo Finance")
                                
                            with col_reg3:
                                diferencia_beta = beta_real - beta
                                st.metric(
                                    "Diferencia Beta", 
                                    f"{diferencia_beta:.2f}",
                                    f"{'↑' if beta_real > beta else '↓'} histórico vs teórico"
                                )
                                st.caption("Consistencia del beta")
                                
                            with col_reg4:
                                st.metric("R² (Coef. Determinación)", f"{r_squared:.3f}")
                                st.caption("Ajuste del modelo")
                            
                            # Interpretación específica por período
                            st.markdown("---")
                            st.subheader("💡 Interpretación por Período")
                            
                            col_interp1, col_interp2 = st.columns(2)
                            
                            with col_interp1:
                                st.markdown(f"""
                                **📈 Análisis del Período {periodo_capm}:**
                                
                                • **Beta histórico**: **{beta_real:.2f}**
                                • **Puntos analizados**: **{len(stock_returns)}**
                                • **Período**: {periodo_capm}
                                • **Frecuencia**: {frecuencia_capm}
                                
                                **🎯 Significado del Beta:**
                                - **Beta > 1**: Más volátil que el mercado
                                - **Beta = 1**: Misma volatilidad  
                                - **Beta < 1**: Menos volátil
                                """)
                            
                            with col_interp2:
                                # Interpretación específica del período
                                if "mes" in periodo_capm:
                                    interpretacion_periodo = "**🔄 Análisis de Corto Plazo** - Muestra el comportamiento reciente y puede ser más volátil"
                                elif periodo_capm == "1 año":
                                    interpretacion_periodo = "**📊 Análisis de Mediano Plazo** - Balance entre estabilidad y actualidad"
                                else:
                                    interpretacion_periodo = "**📈 Análisis de Largo Plazo** - Muestra tendencias estables y comportamiento histórico"
                                
                                st.markdown(f"""
                                **🔍 Contexto del Período:**
                                
                                {interpretacion_periodo}
                                
                                **📋 Recomendaciones:**
                                - Períodos cortos: Útiles para trading
                                - Períodos largos: Mejores para inversión
                                - Combine períodos para análisis completo
                                """)
                            
                            # Recomendaciones específicas basadas en el período
                            st.markdown("---")
                            st.subheader("🎯 Recomendaciones Específicas")
                            
                            if "mes" in periodo_capm:
                                if r_squared > 0.6:
                                    st.success("""
                                    **✅ BUEN AJUSTE EN CORTO PLAZO - Para Trading:**
                                    - Relación mercado-acción consistente recientemente
                                    - Estrategias de momentum pueden ser efectivas
                                    - Monitorea cambios diarios en la relación
                                    """)
                                else:
                                    st.warning("""
                                    **🟡 AJUSTE VARIABLE EN CORTO PLAZO - Precauciones:**
                                    - La acción tiene comportamiento independiente reciente
                                    - Considera noticias y eventos específicos de la empresa
                                    - Usa stops más ajustados
                                    """)
                            else:
                                if r_squared > 0.7:
                                    st.success("""
                                    **✅ ALTO AJUSTE - Para Inversión:**
                                    - Comportamiento predecible vs mercado
                                    - Estrategias basadas en Beta son confiables
                                    - Buena para diversificación de cartera
                                    """)
                                elif r_squared > 0.4:
                                    st.info("""
                                    **🟡 AJUSTE MODERADO - Enfoque Balanceado:**
                                    - Combine análisis CAPM con otros métodos
                                    - Considere factores específicos de la empresa
                                    - Monitoree cambios en la relación
                                    """)
                                else:
                                    st.warning("""
                                    **🔴 BAJO AJUSTE - Análisis Cauteloso:**
                                    - La acción se mueve independientemente del mercado
                                    - Enfóquese en análisis fundamental y técnico
                                    - El Beta puede no ser indicador confiable
                                    """)
                        
                        else:
                            st.warning(f"⚠️ No hay suficientes datos {frecuencia_capm.lower()} para {periodo_capm}. Intenta con una frecuencia diferente.")
                            
                    else:
                        st.warning("❌ No se pudieron cargar los datos para el análisis CAPM")
                        
                except Exception as e:
                    mostrar_error_amigable(e, "el análisis CAPM")

                # Consejos para usar diferentes períodos
                st.markdown("---")
                st.subheader("💡 Consejos para Usar Diferentes Períodos")

                consejos_periodos = [
                    "**📅 1-3 meses**: Ideal para traders - muestra comportamiento reciente",
                    "**📊 6 meses - 1 año**: Balanceado - buen para swing trading",
                    "**📈 2-3 años**: Estabilidad media - recomendado para mayoría de inversores", 
                    "**🏛️ 5-10 años**: Largo plazo - muestra tendencias estables",
                    "**🔄 Combine períodos**: Use corto + largo plazo para análisis completo",
                    "**📉 Períodos cortos**: Más volátiles pero más actualizados",
                    "**📈 Períodos largos**: Más estables pero pueden omitir cambios recientes"
                ]

                for consejo in consejos_periodos:
                    st.write(f"• {consejo}")

                st.markdown("---")

                # =============================================
                # 7. SNAPSHOT FINANCIERO COMPLETO
                # =============================================
                st.subheader(f"📊 Snapshot Financiero Completo - {stonk}")
                
                # Crear una tabla de 2 columnas replicando Finviz
                num_datos = len(datos_finviz)
                mitad = (num_datos + 1) // 2
                
                # Dividir los datos en dos columnas
                items = list(datos_finviz.items())
                col1_items = items[:mitad]
                col2_items = items[mitad:]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    for clave, valor in col1_items:
                        st.markdown(f"""
                        <div style="border-bottom: 1px solid #444; padding: 10px 0;">
                            <div style="font-weight: bold; color: white; font-size: 14px; margin-bottom: 2px;">{clave}</div>
                            <div style="color: #f0f0f0; font-size: 14px; text-align: right; font-weight: 500;">{valor}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    for clave, valor in col2_items:
                        st.markdown(f"""
                        <div style="border-bottom: 1px solid #444; padding: 10px 0;">
                            <div style="font-weight: bold; color: white; font-size: 14px; margin-bottom: 2px;">{clave}</div>
                            <div style="color: #f0f0f0; font-size: 14px; text-align: right; font-weight: 500;">{valor}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # BOTÓN DE DESCARGA
                st.markdown("---")
                st.subheader("💾 Exportar Datos")
                
                # Crear DataFrame combinado con todas las métricas
                df_completo = pd.DataFrame(list(datos_finviz.items()), columns=['Métrica', 'Valor'])
                
                # Agregar métricas de riesgo si están disponibles
                if metricas_riesgo:
                    df_riesgo = pd.DataFrame(list(metricas_riesgo.items()), columns=['Métrica', 'Valor'])
                    df_completo = pd.concat([df_completo, df_riesgo], ignore_index=True)
                
                csv = df_completo.to_csv(index=False)
                
                st.download_button(
                    label="📥 Descargar datos fundamentales y de riesgo como CSV",
                    data=csv,
                    file_name=f"{stonk}_datos_completos.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                    
            else:
                st.error("""
                ❌ No se pudieron cargar los datos fundamentales. Posibles causas:
                
                • **Problemas de conexión** con Finviz
                • **Bloqueo temporal** por demasiadas solicitudes
                • **El símbolo no existe** o no está disponible
                
                💡 **Sugerencias:**
                • Verifica el símbolo (ej: AAPL, MSFT, TSLA, GOOGL)
                • Espera 1-2 minutos e intenta nuevamente  
                • Verifica directamente en [Finviz](https://finviz.com/quote.ashx?t={stonk})
                """)
                
                if st.button("🔄 Intentar nuevamente", use_container_width=True, key="reintentar_fundamentales"):
                    st.rerun()
    
    #
    with tab2:
        mostrar_educacion_financiera(stonk, ticker, info, nombre, descripcion, start_date, end_date)
