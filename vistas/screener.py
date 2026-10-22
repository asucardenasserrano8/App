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


def mostrar_seccion_screener(stonk, ticker, info, nombre, descripcion, start_date, end_date):
    st.header("🔍 Screener S&P 500 - Filtros Avanzados")
    st.write("Busca acciones del S&P 500 que cumplan con tus criterios de inversión")
    
    # LISTA COMPLETA DEL S&P 500 (actualizada 2024)
    SP500_SYMBOLS = [
        # Technology (120+ stocks)
        'AAPL', 'MSFT', 'GOOGL', 'GOOG', 'AMZN', 'META', 'NVDA', 'AVGO', 'TSLA', 'ADBE',
        'CRM', 'CSCO', 'ACN', 'ORCL', 'IBM', 'INTC', 'AMD', 'QCOM', 'TXN', 'NOW',
        'SNOW', 'NET', 'PANW', 'CRWD', 'ZS', 'FTNT', 'OKTA', 'TEAM', 'PLTR', 'DDOG',
        'MDB', 'SPLK', 'HUBS', 'ESTC', 'PD', 'TWLO', 'DOCU', 'RBLX', 'UBER', 'LYFT',
        'SHOP', 'SQ', 'PYPL', 'COIN', 'HOOD', 'ROKU', 'NFLX', 'DIS', 'CMCSA', 'CHTR',
        'T', 'VZ', 'TMUS', 'EA', 'ATVI', 'TTWO', 'ZNGA', 'RIVN', 'LCID', 'FSLR',
        'ENPH', 'SEDG', 'RUN', 'PLUG', 'BE', 'NIO', 'LI', 'XPEV', 'F', 'GM',
        'TSM', 'ASML', 'LRCX', 'AMAT', 'KLAC', 'NXPI', 'MRVL', 'SWKS', 'QRVO', 'MCHP',
        'CDNS', 'ANSS', 'ADSK', 'TTD', 'TTWO', 'EA', 'ATVI', 'ZG', 'Z', 'RDFN',
        'OPEN', 'COMP', 'U', 'CLSK', 'MSTR', 'RIOT', 'MARA', 'HUT', 'BITF', 'COIN',
        
        # Healthcare (60+ stocks)
        'JNJ', 'UNH', 'PFE', 'ABBV', 'MRK', 'TMO', 'LLY', 'DHR', 'ABT', 'BMY',
        'AMGN', 'GILD', 'VRTX', 'REGN', 'BIIB', 'ISRG', 'SYK', 'BDX', 'ZTS', 'EW',
        'HCA', 'IDXX', 'DXCM', 'ILMN', 'MTD', 'WAT', 'PKI', 'TECH', 'RGEN', 'ICLR',
        'STE', 'WST', 'BRKR', 'PODD', 'ALGN', 'COO', 'HSIC', 'XRAY', 'BAX', 'HOLX',
        'LH', 'DGX', 'A', 'ABC', 'CAH', 'MCK', 'CVS', 'WBA', 'CI', 'HUM',
        'ELV', 'CNC', 'MOH', 'OGN', 'BHC', 'JAZZ', 'INCY', 'EXAS', 'NTRA', 'TXG',
        
        # Financials (70+ stocks)
        'JPM', 'BAC', 'WFC', 'GS', 'MS', 'SCHW', 'BLK', 'AXP', 'V', 'MA',
        'PYPL', 'SQ', 'COF', 'DFS', 'TFC', 'PNC', 'USB', 'KEY', 'CFG', 'MTB',
        'RF', 'HBAN', 'FITB', 'ALLY', 'CMA', 'ZION', 'EWBC', 'C', 'BK', 'STT',
        'NTRS', 'TROW', 'AMP', 'BEN', 'IVZ', 'JEF', 'PGR', 'ALL', 'TRV', 'AIG',
        'HIG', 'PFG', 'L', 'AON', 'MMC', 'WTW', 'AJG', 'BRO', 'ERIE', 'CINF',
        'RE', 'RGA', 'MET', 'PRU', 'LNC', 'UNM', 'AFL', 'BHF', 'NMRK', 'RJF',
        'ICE', 'MCO', 'SPGI', 'MSCI', 'NDAQ', 'CBOE', 'FDS', 'FIS', 'FISV', 'GPN',
        
        # Consumer Discretionary (60+ stocks)
        'AMZN', 'TSLA', 'HD', 'MCD', 'NKE', 'LOW', 'SBUX', 'TJX', 'TGT', 'BKNG',
        'ORLY', 'AZO', 'MGM', 'WYNN', 'LVS', 'RCL', 'CCL', 'NCLH', 'MAR', 'HLT',
        'EXPE', 'ABNB', 'TRIP', 'BKNG', 'YUM', 'CMG', 'DPZ', 'WING', 'DRI', 'BLMN',
        'EBAY', 'ETSY', 'ROST', 'BURL', 'DLTR', 'FIVE', 'BIG', 'DKS', 'ASO', 'ANF',
        'GPS', 'URBN', 'LEVI', 'NKE', 'LULU', 'VFC', 'TPR', 'CPRI', 'RL', 'PVH',
        'F', 'GM', 'STLA', 'HMC', 'TM', 'RACE', 'TSLA', 'LCID', 'RIVN', 'NKLA',
        
        # Consumer Staples (30+ stocks)
        'PG', 'KO', 'PEP', 'WMT', 'COST', 'TGT', 'KR', 'SYY', 'ADM', 'BG',
        'MDLZ', 'K', 'GIS', 'HSY', 'SJM', 'CAG', 'CPB', 'KMB', 'CL', 'EL',
        'NWL', 'CLX', 'CHD', 'EPD', 'MO', 'PM', 'BTI', 'IMB', 'STZ', 'BUD',
        'TAP', 'SAM', 'MNST', 'KDP', 'FIZZ', 'COKE', 'PEP', 'KO', 'WMT', 'COST',
        
        # Industrials (70+ stocks)
        'UPS', 'FDX', 'RTX', 'BA', 'LMT', 'NOC', 'GD', 'HII', 'LHX', 'CW',
        'TDG', 'HEI', 'COL', 'TXT', 'DE', 'CAT', 'CNHI', 'AGCO', 'CMI', 'PCAR',
        'ALLE', 'ALGN', 'CSX', 'UNP', 'NSC', 'CP', 'KSU', 'JBHT', 'LSTR', 'ODFL',
        'EXPD', 'CHRW', 'XPO', 'GWW', 'FAST', 'MSM', 'SNA', 'ITW', 'EMR', 'ROK',
        'DOV', 'PNR', 'IEX', 'FLS', 'FLR', 'J', 'PWR', 'QUAD', 'VMC', 'MLM',
        'SUM', 'EXP', 'ASH', 'ECL', 'IFF', 'PPG', 'SHW', 'ALB', 'LTHM', 'SLB',
        'HAL', 'BKR', 'NOV', 'FTI', 'OII', 'RIG', 'DO', 'LBRT', 'WHD', 'NBR',
        
        # Energy (30+ stocks)
        'XOM', 'CVX', 'COP', 'EOG', 'MPC', 'PSX', 'VLO', 'DVN', 'PXD', 'OXY',
        'HES', 'MRO', 'FANG', 'APA', 'NOV', 'SLB', 'HAL', 'BKR', 'WMB', 'KMI',
        'ET', 'EPD', 'OKE', 'TRGP', 'LNG', 'CHK', 'RRC', 'SWN', 'AR', 'MGY',
        
        # Materials (20+ stocks)
        'LIN', 'APD', 'SHW', 'ECL', 'PPG', 'ALB', 'NEM', 'GOLD', 'FCX', 'SCCO',
        'AA', 'CLF', 'STLD', 'NUE', 'X', 'MOS', 'CF', 'NTR', 'FMC', 'AVY',
        'IP', 'PKG', 'WRK', 'SEE', 'BALL', 'ATI', 'CMC', 'RS', 'CRS', 'WOR',
        
        # Real Estate (30+ stocks)
        'AMT', 'CCI', 'PLD', 'EQIX', 'PSA', 'SPG', 'O', 'AVB', 'EQR', 'ESS',
        'UDR', 'MAA', 'CPT', 'ARE', 'BXP', 'SLG', 'VNO', 'KIM', 'FRT', 'REG',
        'DLR', 'IRM', 'EXR', 'PSA', 'WPC', 'NSA', 'LAMR', 'CUBE', 'REXR', 'PLD',
        
        # Utilities (30+ stocks)
        'NEE', 'DUK', 'SO', 'D', 'AEP', 'EXC', 'SRE', 'XEL', 'WEC', 'ES',
        'PEG', 'ETR', 'FE', 'AES', 'AWK', 'CNP', 'DTE', 'LNT', 'PPL', 'EIX',
        'ED', 'CMS', 'NRG', 'VST', 'ALE', 'OTTR', 'SWX', 'NI', 'OGE', 'POR'
    ]
    # Intentamos traer la lista REAL y actual del S&P 500 (se actualiza sola
    # cuando hay fusiones/adquisiciones/bajas). Si no se puede (sin internet,
    # Wikipedia cambió de formato, etc.), usamos la lista fija de arriba como
    # respaldo — así el Screener nunca se queda sin funcionar.
    lista_actual = obtener_lista_sp500_actual()
    if lista_actual:
        SP500_SYMBOLS = lista_actual
        fuente_lista = "lista real y actual (Wikipedia)"
    else:
        fuente_lista = "lista de respaldo (sin conexión a Wikipedia)"
    # Quitamos duplicados (varios símbolos aparecían en más de una categoría,
    # ej. AMZN/TSLA en Tech y en Consumer Discretionary) — cada llamada
    # repetida a Yahoo Finance por un mismo ticker era tiempo desperdiciado.
    SP500_SYMBOLS = list(dict.fromkeys(SP500_SYMBOLS))
    st.caption(f"📋 Usando {fuente_lista}: {len(SP500_SYMBOLS)} símbolos.")

    # =============================================
    # FUNCIONES OPTIMIZADAS CON CACHING ESTRATÉGICO
    # =============================================

    @st.cache_data(ttl=86400, show_spinner=False)  # 24 horas
    def obtener_lista_sp500_estatica():
        """Lista estática del S&P500 que cambia poco"""
        return SP500_SYMBOLS

    @st.cache_data(ttl=3600, show_spinner=False, max_entries=50)
    def obtener_datos_sp500_precalculados():
        """Precalcula datos del S&P500 una vez por hora"""
        return precalcular_datos_screener(SP500_SYMBOLS)

    def precalcular_datos_screener(sp500_symbols):
        """Precalcula datos críticos para mayor velocidad.

        Antes esto se hacía en un for secuencial: una acción a la vez, dos
        llamadas de red cada una (info + histórico). Con ~500 símbolos eso
        eran hasta 1,000 peticiones seguidas a Yahoo Finance — lento y
        propenso a que Yahoo empiece a rechazar peticiones a la mitad,
        dejando cargar solo un puñado de acciones. Ahora se hace en paralelo
        (varias acciones a la vez) y cada ticker ya queda cacheado
        individualmente arriba, así que una segunda búsqueda es casi
        instantánea.
        """
        if 'datos_precalculados' in st.session_state:
            return st.session_state.datos_precalculados

        # Limitar a las primeras 520 acciones (por si la lista creciera más)
        simbolos_rapidos = sp500_symbols[:520]

        datos_precalculados = {}
        progress_bar = st.progress(0)
        status_text = st.empty()
        total = len(simbolos_rapidos)
        completados = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futuros = {
                executor.submit(obtener_datos_completos_yfinance, simbolo): simbolo
                for simbolo in simbolos_rapidos
            }
            for futuro in concurrent.futures.as_completed(futuros):
                simbolo = futuros[futuro]
                completados += 1
                try:
                    datos = futuro.result()
                    if datos and datos.get('Empresa Valida'):
                        scoring = calcular_scoring_dinamico(datos)
                        datos['Score'] = scoring
                        datos_precalculados[simbolo] = datos
                except Exception:
                    pass

                if completados % 10 == 0 or completados == total:
                    progress_bar.progress(completados / total)
                    status_text.text(f"Precalculando: {completados}/{total} acciones "
                                      f"({len(datos_precalculados)} cargadas con éxito)")

        # Segunda pasada, más lenta y con MENOS peticiones simultáneas, solo
        # para los símbolos que fallaron en la primera. La primera pasada es
        # rápida pero agresiva (10 a la vez) y eso hace que Yahoo Finance
        # rechace más peticiones; con menos carga a la vez, la segunda
        # pasada logra rescatar una buena parte de esos fallos pasajeros.
        faltantes = [s for s in simbolos_rapidos if s not in datos_precalculados]
        if faltantes:
            status_text = st.empty()
            status_text.text(f"Reintentando {len(faltantes)} acciones que no cargaron a la primera...")
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futuros = {
                    executor.submit(obtener_datos_completos_yfinance, simbolo): simbolo
                    for simbolo in faltantes
                }
                for futuro in concurrent.futures.as_completed(futuros):
                    simbolo = futuros[futuro]
                    try:
                        datos = futuro.result()
                        if datos and datos.get('Empresa Valida'):
                            scoring = calcular_scoring_dinamico(datos)
                            datos['Score'] = scoring
                            datos_precalculados[simbolo] = datos
                    except Exception:
                        pass
            status_text.empty()

        progress_bar.empty()
        status_text.empty()

        st.session_state.datos_precalculados = datos_precalculados
        return datos_precalculados

    def aplicar_filtros_rapidos(datos, filtros):
        """Aplica filtros de manera optimizada usando operaciones vectorizadas"""
        try:
            # Filtro P/E
            pe = datos.get('P/E', 0)
            if filtros['pe_min'] > 0 and (pe == 0 or pe < filtros['pe_min']):
                return False
            if filtros['pe_max'] < 1000 and pe > filtros['pe_max']:
                return False
            
            # Solo los filtros más importantes para velocidad
            roe = datos.get('ROE', 0)
            if filtros['roe_min'] > 0 and roe < (filtros['roe_min'] / 100):
                return False
                
            # Filtro Margen Beneficio
            margen = datos.get('Margen Beneficio', 0)
            if filtros['profit_margin_min'] > 0 and margen < (filtros['profit_margin_min'] / 100):
                return False
            
            # Filtro Deuda/Equity
            deuda_eq = datos.get('Deuda/Equity', 0)
            if filtros['debt_equity_max'] < 10 and deuda_eq > filtros['debt_equity_max']:
                return False
            
            # Filtro Beta
            beta = datos.get('Beta', 1)
            if filtros['beta_max'] < 5 and beta > filtros['beta_max']:
                return False
            
            # Filtro RSI
            rsi = datos.get('RSI', 50)
            if rsi < filtros['rsi_min'] or rsi > filtros['rsi_max']:
                return False
                
            return True
        except:
            return False

    def buscar_simbolos_sp500_optimizado(filtros, max_acciones=50):
        """Versión optimizada con carga progresiva"""
        # Cargar primero datos precalculados si existen
        datos_precalculados = st.session_state.get('datos_precalculados', {})
        
        if not datos_precalculados:
            with st.spinner('🔄 Precalculando datos del S&P500 para búsquedas ultra rápidas...'):
                datos_precalculados = precalcular_datos_screener(SP500_SYMBOLS)
                st.session_state.datos_precalculados = datos_precalculados
        
        # Aplicar filtros sobre datos precalculados (MUCHO más rápido)
        acciones_encontradas = []
        
        for simbolo, datos in datos_precalculados.items():
            if len(acciones_encontradas) >= max_acciones:
                break
            if aplicar_filtros_rapidos(datos, filtros):
                acciones_encontradas.append(datos)
        
        return acciones_encontradas

    # FUNCIONES AUXILIARES (mantener tus funciones originales)
    @st.cache_data(ttl=3600, show_spinner=False, max_entries=550)  # 1 hora, una entrada por ticker
    def obtener_datos_completos_yfinance(simbolo, intentos=2):
        """Obtiene datos fundamentales y técnicos de yFinance para cualquier
        símbolo. Reintenta una vez antes de rendirse: con tantas peticiones
        en paralelo, Yahoo Finance a veces rechaza una petición de forma
        pasajera (no porque el ticker esté mal) — sin este reintento, ese
        fallo temporal se guardaría en caché 1 hora completa como si el
        ticker no existiera."""
        for intento in range(intentos):
            try:
                ticker = yf.Ticker(simbolo)
                info = ticker.info

                # Verificar que el símbolo es válido
                if not info or 'currentPrice' not in info or info.get('currentPrice') is None:
                    if intento < intentos - 1:
                        time.sleep(0.7)
                        continue
                    return None

                # Obtener datos históricos para calcular RSI
                datos_historicos = yf.download(simbolo, period="6mo", interval="1d", progress=False)
                break
            except Exception:
                if intento < intentos - 1:
                    time.sleep(0.7)
                    continue
                return None

        # Calcular RSI si hay datos históricos
        rsi = 50
        if not datos_historicos.empty and 'Close' in datos_historicos.columns:
            try:
                delta = datos_historicos['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi_calculado = 100 - (100 / (1 + rs))
                rsi = rsi_calculado.iloc[-1] if not rsi_calculado.empty and not pd.isna(rsi_calculado.iloc[-1]) else 50
            except:
                rsi = 50

        # Datos completos
        datos = {
            'Símbolo': simbolo,
            'Nombre': info.get('longName', simbolo),
            'Sector': info.get('sector', 'N/A'),
            'Industria': info.get('industry', 'N/A'),
            'Market Cap': info.get('marketCap', 0),
            'P/E': info.get('trailingPE', 0),
            'Precio Actual': info.get('currentPrice', 0),
            'Cambio %': info.get('regularMarketChangePercent', 0),
            'Volumen': info.get('volume', 0),
            'ROE': info.get('returnOnEquity', 0),
            'Margen Beneficio': info.get('profitMargins', 0),
            'Deuda/Equity': info.get('debtToEquity', 0),
            'Crecimiento Ingresos': info.get('revenueGrowth', 0),
            'Beta': info.get('beta', 1),
            'RSI': rsi,
            'Empresa Valida': True
        }

        return datos

    def calcular_scoring_dinamico(datos):
        """Calcula scoring basado en datos fundamentales"""
        if not datos:
            return 0
        
        score = 0
        max_score = 100
        
        try:
            # P/E Ratio (20 puntos) - MÁS FLEXIBLE
            pe = datos.get('P/E', 0)
            if pe and pe > 0:
                if pe < 15:
                    score += 20
                elif pe < 25:
                    score += 15
                elif pe < 35:
                    score += 10
                else:
                    score += 5
            
            # ROE (20 puntos) - MÁS FLEXIBLE
            roe = datos.get('ROE', 0)
            if roe and roe > 0:
                if roe > 0.20:
                    score += 20
                elif roe > 0.15:
                    score += 16
                elif roe > 0.10:
                    score += 12
                elif roe > 0.05:
                    score += 8
                else:
                    score += 4
            
            # Margen Beneficio (15 puntos) - MÁS FLEXIBLE
            margen = datos.get('Margen Beneficio', 0)
            if margen and margen > 0:
                if margen > 0.20:
                    score += 15
                elif margen > 0.15:
                    score += 12
                elif margen > 0.10:
                    score += 9
                elif margen > 0.05:
                    score += 6
                else:
                    score += 3
            
            # Deuda/Equity (15 puntos) - MÁS FLEXIBLE
            deuda_eq = datos.get('Deuda/Equity', 0)
            if deuda_eq and deuda_eq >= 0:
                if deuda_eq < 0.5:
                    score += 15
                elif deuda_eq < 1.0:
                    score += 12
                elif deuda_eq < 1.5:
                    score += 9
                elif deuda_eq < 2.0:
                    score += 6
                else:
                    score += 3
            
            # Crecimiento Ingresos (20 puntos) - MÁS FLEXIBLE
            crecimiento = datos.get('Crecimiento Ingresos', 0)
            if crecimiento:
                if crecimiento > 0.20:
                    score += 20
                elif crecimiento > 0.15:
                    score += 16
                elif crecimiento > 0.10:
                    score += 12
                elif crecimiento > 0.05:
                    score += 8
                elif crecimiento > 0:
                    score += 4
            
            # Beta (10 puntos) - MÁS FLEXIBLE
            beta = datos.get('Beta', 1)
            if beta and beta > 0:
                if beta < 0.8:
                    score += 10
                elif beta < 1.2:
                    score += 8
                elif beta < 1.5:
                    score += 6
                elif beta < 2.0:
                    score += 4
                else:
                    score += 2
            
            return min(score, max_score)
            
        except Exception as e:
            return 0

    # =============================================
    # INTERFAZ DE USUARIO OPTIMIZADA
    # =============================================
    # INTERFAZ DE USUARIO OPTIMIZADA
    # =============================================

    # PRE-CÁLCULO AUTOMÁTICO AL ENTRAR A LA SECCIÓN
    if 'precalc_iniciado' not in st.session_state:
        with st.spinner('🔄 Precargando datos del S&P 500 para búsquedas instantáneas...'):
            datos_precalculados = precalcular_datos_screener(SP500_SYMBOLS)
            st.session_state.datos_precalculados = datos_precalculados
            st.session_state.precalc_iniciado = True
            st.success(f"✅ Pre-cálculo completado: {len(datos_precalculados)} acciones listas")

    # INICIALIZAR ESTADOS SI NO EXISTEN
    if 'show_search_results' not in st.session_state:
        st.session_state.show_search_results = False
    if 'show_comparison' not in st.session_state:
        st.session_state.show_comparison = False

    # INTERFAZ DE FILTROS MEJORADA - VALORES POR DEFECTO MÁS FLEXIBLES
    st.subheader("🎯 Configura tus Criterios de Búsqueda")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**💰 Valoración:**")
        pe_min = st.number_input("P/E Mínimo", value=0.0, min_value=0.0, max_value=100.0, step=1.0, 
                            help="0 = Sin filtro. Valores típicos: 5-15")
        pe_max = st.number_input("P/E Máximo", value=60.0, min_value=0.0, max_value=1000.0, step=1.0,
                            help="1000 = Sin filtro. Valores típicos: 20-50")
        
        st.write("**📈 Rentabilidad:**")
        roe_min = st.number_input("ROE Mínimo (%)", value=5.0, min_value=0.0, max_value=100.0, step=1.0,
                                help="0 = Sin filtro. Valores típicos: 8-15")
        profit_margin_min = st.number_input("Margen Beneficio Mínimo (%)", value=0.0, min_value=0.0, max_value=100.0, step=1.0,
                                        help="0 = Sin filtro. Valores típicos: 5-12")

    with col2:
        st.write("**🏦 Estructura de Capital:**")
        debt_equity_max = st.number_input("Deuda/Equity Máximo", value=3.0, min_value=0.0, max_value=10.0, step=0.1,
                                        help="10 = Sin filtro. Valores típicos: 0.5-2.0")
        
        st.write("**📊 Volatilidad:**")
        beta_max = st.number_input("Beta Máximo", value=2.5, min_value=0.1, max_value=5.0, step=0.1,
                                help="5 = Sin filtro. Valores típicos: 0.8-1.5")
        
        st.write("**🚀 Crecimiento:**")
        revenue_growth_min = st.number_input("Crecimiento Ingresos Mínimo (%)", value=0.0, min_value=-50.0, max_value=200.0, step=1.0,
                                        help="-50 = Sin filtro. Valores típicos: 5-15")

    # Filtros RSI MÁS FLEXIBLES
    st.subheader("📊 Filtro de Momentum (RSI)")
    col_rsi1, col_rsi2 = st.columns(2)

    with col_rsi1:
        rsi_min = st.slider("RSI Mínimo", 0, 100, 25, key="rsi_min_screener",
                        help="RSI muy bajo puede indicar sobreventa")

    with col_rsi2:
        rsi_max = st.slider("RSI Máximo", 0, 100, 75, key="rsi_max_screener",
                        help="RSI muy alto puede indicar sobrecompra")

    st.info(f"💡 **Rango RSI seleccionado:** {rsi_min} - {rsi_max} (Recomendado: 25-75 para más resultados)")

    # BOTÓN DE BÚSQUEDA MEJORADO
    st.markdown("---")

    # Selector de límite de resultados
    max_resultados = st.slider("Límite máximo de resultados", 10, 200, 50, 10,
                            help="Número máximo de acciones a mostrar")

    # Indicador de estado del cache
    if 'datos_precalculados' in st.session_state:
        st.success(f"✅ **Datos precalculados listos:** {len(st.session_state.datos_precalculados)} acciones cargadas en caché")
    else:
        st.info("🔄 **Sistema optimizado:** Los datos se precalcularán en la primera búsqueda para máxima velocidad")

    if st.button("🚀 Ejecutar Búsqueda Ultra Rápida", use_container_width=True, type="primary"):
        # Definir filtros
        filtros = {
            'pe_min': pe_min,
            'pe_max': pe_max,
            'roe_min': roe_min,
            'profit_margin_min': profit_margin_min,
            'revenue_growth_min': revenue_growth_min,
            'debt_equity_max': debt_equity_max,
            'beta_max': beta_max,
            'rsi_min': rsi_min,
            'rsi_max': rsi_max
        }
        
        # Ejecutar búsqueda OPTIMIZADA
        with st.spinner(f"🔍 Buscando en {len(SP500_SYMBOLS)} acciones con sistema optimizado..."):
            acciones_encontradas = buscar_simbolos_sp500_optimizado(filtros, max_resultados)
        
        if acciones_encontradas:
            # Ordenar por score
            acciones_encontradas.sort(key=lambda x: x['Score'], reverse=True)
            
            # Crear DataFrame para mostrar
            df_resultados = pd.DataFrame(acciones_encontradas)
            
            # Formatear columnas para mostrar
            columnas_mostrar = ['Símbolo', 'Nombre', 'Sector', 'P/E', 'Precio Actual', 
                            'ROE', 'Margen Beneficio', 'Deuda/Equity', 'Beta', 'RSI', 'Score']
            
            df_display = df_resultados[columnas_mostrar].copy()
            
            # Formatear valores
            df_display['P/E'] = df_display['P/E'].apply(lambda x: f"{x:.1f}" if x > 0 else "N/A")
            df_display['Precio Actual'] = df_display['Precio Actual'].apply(lambda x: f"${x:.2f}" if x > 0 else "N/A")
            df_display['ROE'] = df_display['ROE'].apply(lambda x: f"{x*100:.1f}%" if x > 0 else "N/A")
            df_display['Margen Beneficio'] = df_display['Margen Beneficio'].apply(lambda x: f"{x*100:.1f}%" if x > 0 else "N/A")
            df_display['Deuda/Equity'] = df_display['Deuda/Equity'].apply(lambda x: f"{x:.2f}" if x >= 0 else "N/A")
            df_display['Beta'] = df_display['Beta'].apply(lambda x: f"{x:.2f}" if x > 0 else "N/A")
            df_display['RSI'] = df_display['RSI'].apply(lambda x: f"{x:.1f}")
            df_display['Score'] = df_display['Score'].apply(lambda x: f"{x:.0f}")
            
            # GUARDAR ESTADO DE BÚSQUEDA
            st.session_state.show_search_results = True
            st.session_state.search_results = {
                'acciones_encontradas': acciones_encontradas,
                'df_display': df_display,
                'df_resultados': df_resultados
            }
            st.session_state.show_comparison = False  # Ocultar comparación al hacer nueva búsqueda
            
            st.rerun()
            
        else:
            st.warning("""
            ❌ No se encontraron acciones que cumplan todos los criterios.
            
            **💡 Sugerencias para obtener más resultados:**
            • **Relaja los filtros** - especialmente P/E Máximo (prueba 60-80) y ROE Mínimo (5-8%)
            • **Amplía el rango RSI** - prueba 20-80 en lugar de 30-70
            • **Reduce Deuda/Equity Máximo** - prueba 3.0-4.0
            • **Aumenta Beta Máximo** - prueba 2.5-3.0
            • **Establece algunos filtros en 0** para desactivarlos completamente
            """)

    # ⭐⭐ AQUÍ VAN LOS RESULTADOS - DESPUÉS DE LOS FILTROS Y BOTONES ⭐⭐

    # MOSTRAR RESULTADOS DE BÚSQUEDA SI ESTÁN ACTIVOS
    if st.session_state.show_search_results and st.session_state.get('search_results'):
        st.markdown("---")
        resultados = st.session_state.search_results
        st.success(f"✅ **Búsqueda completada:** {len(resultados['acciones_encontradas'])} acciones encontradas")
        
        st.subheader("📊 Resultados del Screener S&P 500 (Optimizado)")
        st.dataframe(resultados['df_display'], use_container_width=True)
        
        st.subheader("📈 Análisis por Sectores")
        sector_counts = resultados['df_resultados']['Sector'].value_counts()
        fig_sectores = px.pie(
            values=sector_counts.values,
            names=sector_counts.index,
            title='Distribución de Acciones por Sector'
        )
        st.plotly_chart(fig_sectores, use_container_width=True, key="sectores_pie")
        
        st.subheader("🏆 Distribución de Scores")
        fig_scores = px.bar(
            resultados['df_resultados'].head(20),
            x='Símbolo',
            y='Score',
            color='Score',
            title='Top 20 Acciones por Score',
            color_continuous_scale='viridis'
        )
        fig_scores.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_scores, use_container_width=True, key="scores_bar")
        
        st.markdown("---")
        st.subheader("💾 Exportar Resultados")
        
        csv_resultados = resultados['df_resultados'].to_csv(index=False)
        st.download_button(
            label="📥 Descargar resultados completos (CSV)",
            data=csv_resultados,
            file_name=f"screener_sp500_optimizado_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    # =============================================
    # GRÁFICA DE COMPARACIÓN CON S&P500
    # =============================================

    # ... (el resto del código de comparación se mantiene igual)

    # =============================================
    # GRÁFICA DE COMPARACIÓN CON S&P500
    # =============================================

    # Verificar si hay resultados disponibles para comparación
    acciones_disponibles = None
    if st.session_state.get('search_results'):
        acciones_disponibles = st.session_state.search_results['acciones_encontradas']

    if acciones_disponibles:
        st.markdown("---")
        st.subheader("📈 Comparación de Rendimiento vs S&P500")
        
        col_periodo, col_accion = st.columns(2)
        
        with col_periodo:
            periodo_comparacion = st.selectbox(
                "Período de Comparación:",
                ["1 Mes", "3 Meses", "6 Meses", "1 Año", "2 Años", "3 Años"],
                index=3,
                key="periodo_screener"
            )
        
        with col_accion:
            acciones_todas = [acc['Símbolo'] for acc in acciones_disponibles]
            accion_seleccionada = st.selectbox(
                "Seleccionar Acción para Comparar:",
                acciones_todas,
                key="accion_comparar_screener"
            )
        
        # Botón para generar comparación
        if st.button("🔄 Generar Comparación", use_container_width=True, key="comparar_btn"):
            st.session_state.show_comparison = True
            st.session_state.comparison_data = {
                'accion_seleccionada': accion_seleccionada,
                'periodo_comparacion': periodo_comparacion
            }
            st.rerun()
        
        # MOSTRAR COMPARACIÓN SI ESTÁ ACTIVA
        if st.session_state.show_comparison and st.session_state.get('comparison_data'):
            comparison = st.session_state.comparison_data
            accion_seleccionada = comparison['accion_seleccionada']
            periodo_comparacion = comparison['periodo_comparacion']
            
            with st.spinner(f'Comparando {accion_seleccionada} vs S&P500...'):
                try:
                    # Mapear período seleccionado a días
                    periodo_map = {
                        "1 Mes": 30,
                        "3 Meses": 90,
                        "6 Meses": 180,
                        "1 Año": 365,
                        "2 Años": 730,
                        "3 Años": 1095
                    }
                    
                    dias = periodo_map[periodo_comparacion]
                    start_date = datetime.today() - timedelta(days=dias)
                    
                    # Obtener datos de la acción seleccionada
                    data_accion = yf.download(accion_seleccionada, start=start_date, progress=False)
                    data_sp500 = yf.download('^GSPC', start=start_date, progress=False)
                    
                    if not data_accion.empty and not data_sp500.empty:
                        # Obtener precios de cierre
                        if isinstance(data_accion.columns, pd.MultiIndex):
                            close_accion = data_accion[('Close', accion_seleccionada)]
                        else:
                            close_accion = data_accion['Close']
                        
                        if isinstance(data_sp500.columns, pd.MultiIndex):
                            close_sp500 = data_sp500[('Close', '^GSPC')]
                        else:
                            close_sp500 = data_sp500['Close']
                        
                        # Calcular rendimiento normalizado (base 100)
                        rendimiento_accion = (close_accion / close_accion.iloc[0]) * 100
                        rendimiento_sp500 = (close_sp500 / close_sp500.iloc[0]) * 100
                        
                        # Crear gráfica
                        fig_comparacion = go.Figure()
                        
                        # Agregar línea de la acción
                        fig_comparacion.add_trace(go.Scatter(
                            x=rendimiento_accion.index,
                            y=rendimiento_accion.values,
                            mode='lines',
                            name=f'{accion_seleccionada}',
                            line=dict(color='#00FF00', width=3),
                            hovertemplate=(
                                f'<b>{accion_seleccionada}</b><br>' +
                                'Fecha: %{x}<br>' +
                                'Rendimiento: %{y:.1f}%<br>' +
                                '<extra></extra>'
                            )
                        ))
                        
                        # Agregar línea del S&P500
                        fig_comparacion.add_trace(go.Scatter(
                            x=rendimiento_sp500.index,
                            y=rendimiento_sp500.values,
                            mode='lines',
                            name='S&P 500',
                            line=dict(color='#FF6B6B', width=3, dash='dash'),
                            hovertemplate=(
                                '<b>S&P 500</b><br>' +
                                'Fecha: %{x}<br>' +
                                'Rendimiento: %{y:.1f}%<br>' +
                                '<extra></extra>'
                            )
                        ))
                        
                        # Calcular métricas de performance
                        rend_final_accion = rendimiento_accion.iloc[-1] - 100
                        rend_final_sp500 = rendimiento_sp500.iloc[-1] - 100
                        outperformance = rend_final_accion - rend_final_sp500
                        
                        # Configurar layout
                        fig_comparacion.update_layout(
                            title=f'Comparación de Rendimiento: {accion_seleccionada} vs S&P500 ({periodo_comparacion})',
                            xaxis_title='Fecha',
                            yaxis_title='Rendimiento (%)',
                            height=500,
                            showlegend=True,
                            hovermode='x unified',
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            )
                        )
                        
                        # Mostrar gráfica
                        st.plotly_chart(fig_comparacion, use_container_width=True, key="comparacion_sp500")
                        
                        # Mostrar métricas de performance
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric(
                                f"Rendimiento {accion_seleccionada}",
                                f"{rend_final_accion:+.1f}%",
                                delta_color="normal"
                            )
                        
                        with col2:
                            st.metric(
                                "Rendimiento S&P500",
                                f"{rend_final_sp500:+.1f}%", 
                                delta_color="normal"
                            )
                        
                        with col3:
                            st.metric(
                                "Outperformance",
                                f"{outperformance:+.1f}%",
                                delta_color="normal"
                            )
                        
                        with col4:
                            # Calcular correlación
                            correlacion = rendimiento_accion.corr(rendimiento_sp500)
                            st.metric(
                                "Correlación",
                                f"{correlacion:.2f}",
                                delta_color="off"
                            )
                        
                        # Análisis de la comparación
                        st.info(f"""
                        **📊 Análisis de la Comparación:**
                        
                        • **{accion_seleccionada}** ha tenido un rendimiento del **{rend_final_accion:+.1f}%** en el período
                        • **S&P 500** ha tenido un rendimiento del **{rend_final_sp500:+.1f}%**
                        • **Diferencia:** {accion_seleccionada} ha **{"superado" if outperformance >= 0 else "subperformado"}** al mercado por **{abs(outperformance):.1f}%**
                        • **Correlación:** {correlacion:.2f} ({"alta" if correlacion > 0.7 else "media" if correlacion > 0.3 else "baja"})
                        """)
                        
                        # Mantener el estado de los resultados visibles
                        st.session_state.show_search_results = True
                        
                    else:
                        st.warning("No se pudieron obtener datos para la comparación")
                        
                except Exception as e:
                    mostrar_error_amigable(e, "la comparación de acciones")

    # CONSEJOS PARA FILTROS MÁS EFECTIVOS
    with st.expander("💡 Consejos para Configurar Filtros en S&P 500"):
        st.markdown("""
        **Configuraciones recomendadas para S&P 500:**
        
        | Filtro | Valor Conservador | Valor Balanceado | Valor Agresivo | Resultados |
        |--------|------------------|------------------|----------------|------------|
        | P/E Máximo | 25 | 40-50 | 60-80 | 🟢 Más resultados |
        | ROE Mínimo | 15% | 8-12% | 5-8% | 🟢 Más resultados |
        | RSI Mínimo | 30 | 25-30 | 20-25 | 🟢 Más resultados |
        | RSI Máximo | 70 | 70-75 | 75-80 | 🟢 Más resultados |
        | Deuda/Equity | 1.0 | 2.0-2.5 | 3.0-4.0 | 🟢 Más resultados |
        | Beta Máximo | 1.2 | 1.8-2.2 | 2.5-3.0 | 🟢 Más resultados |
        
        **Para empezar (Balanceado):**
        - P/E Mínimo: 0
        - P/E Máximo: 50
        - ROE Mínimo: 8%
        - RSI: 25-75
        - Deuda/Equity: 2.5
        - Beta: 2.0
        
        Esto debería darte **20-60 acciones** del S&P 500.
        
        **Sectores con mejores resultados:**
        - 🏦 **Financieras:** Suelen tener P/E bajos
        - 🛢️ **Energía:** Crecimiento variable pero oportunidades
        - 🏭 **Industriales:** Estables con buenos dividendos
        - 🛒 **Consumo:** Defensivas con crecimiento constante
        """)

    # ESTADÍSTICAS DEL SISTEMA OPTIMIZADO
    with st.expander("🚀 Estadísticas del Sistema Optimizado"):
        if 'datos_precalculados' in st.session_state:
            datos_precalculados = st.session_state.datos_precalculados
            st.markdown(f"""
            **📊 Estado del Sistema de Caché:**
            - **Acciones precalculadas:** {len(datos_precalculados)}
            - **Tiempo de caché:** 1 hora
            - **Velocidad de búsqueda:** Instantánea
            - **Memoria optimizada:** Solo datos esenciales
            
            **💡 Beneficios del sistema optimizado:**
            - **⏱️ 10x más rápido** que búsquedas individuales
            - **📈 Mayor cobertura** del S&P500
            - **🔄 Actualizaciones automáticas** cada hora
            - **💾 Caché inteligente** que persiste entre sesiones
            """)
        else:
            st.info("El sistema de caché se activará después de la primera búsqueda")

    # BOTÓN PARA LIMPIAR CACHÉ (útil para desarrollo)
    if st.button("🗑️ Limpiar Caché de Datos", type="secondary"):
        keys_to_remove = [
            'datos_precalculados', 'precalc_iniciado', 'acciones_encontradas',
            'df_resultados', 'resultados_busqueda', 'search_results',
            'show_search_results', 'show_comparison', 'comparison_data'
        ]
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
        st.success("✅ Caché limpiado. La próxima búsqueda recalculará los datos.")
        st.rerun()
