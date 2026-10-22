# Índice — versión refactorizada

Esta es la versión mejorada de tu app original (`App.py`, 11,842 líneas en un
solo archivo). El comportamiento y el diseño visual son los mismos que ya
tenías; lo que cambió es **cómo está organizado el código por dentro**.

## Qué se hizo

### 1. Se eliminaron las funciones duplicadas
Tu archivo original definía varias funciones **más de una vez** (Python
usaba silenciosamente solo la última definición, y las anteriores quedaban
como código muerto, ocupando espacio y generando confusión):

- `calcular_metricas_riesgo_avanzadas` (3 veces)
- `calcular_indicadores_tecnicos` (2 veces)
- `obtener_rating_analistas` (2 veces)
- `obtener_info_wikipedia` (2 veces)
- `obtener_datos_macro` (2 veces)
- `generar_analisis_riesgo_ia` (2 veces)

Ahora cada una existe **una sola vez**, con la versión que realmente se
estaba usando.

También se quitó una línea de prueba que había quedado al final
(`"🔥 ESTE ES UN TEST..."`) y que se mostraba siempre, en cualquier sección.

### 2. Se dividió el archivo en un proyecto modular
Esto es lo que probablemente le causaba fallas intermitentes a la app según
te comentó tu maestro: un script de casi 12,000 líneas es más lento de
analizar y recargar, y cualquier error de sintaxis en cualquier parte del
archivo tira TODA la app.

Estructura nueva:

```
Indice/
├── App.py                        # orquestador (52 líneas) — decide qué vista mostrar
├── config.py                     # imports, API keys, CSS, configuración de página
├── requirements.txt
├── .env.example                  # plantilla de tus llaves (AP, AP1, AP2, AP3)
├── nucleo/                       # funciones reutilizables (sin pantallas)
│   ├── datos.py                  # descarga de datos (yfinance, S&P 500, paralelo)
│   ├── tecnico.py                 # indicadores técnicos y tendencias
│   ├── riesgo.py                  # métricas de riesgo, gráficas, análisis IA de riesgo
│   ├── scoring.py                 # scoring fundamental y reporte descargable
│   ├── wikipedia_info.py          # info corporativa de Wikipedia
│   ├── ratings.py                 # rating de analistas
│   ├── interfaz.py                # buscador + botones de navegación
│   └── footer.py                  # reporte, historial, favoritos, aviso legal
└── vistas/                        # una función por cada botón/sección
    ├── informacion.py, inicio.py, variacion_precio.py
    ├── fundamentales.py            # ahora solo arma las 2 pestañas...
    ├── educacion_financiera.py     # ...la pestaña de educación vive aparte (era enorme)
    ├── noticias.py, riesgo.py, comparacion.py, tecnico.py
    ├── analisis_ia.py, screener.py, macro.py, mercados_globales.py
```

Cada archivo ahora tiene entre 20 y ~1,200 líneas (antes: 11,842 en uno
solo). El más grande que queda es `educacion_financiera.py` (contenido
educativo estático de las 82 métricas) — si más adelante quieres, se puede
dividir por categoría, pero no era código con lógica compleja, así que no
representa el mismo riesgo.

### 3. Optimizaciones de velocidad
Al deduplicar, algunas funciones se habían quedado sin el `@st.cache_data`
que tenía su versión descartada (justo la que hacía las llamadas costosas a
Yahoo Finance). Se restauró en:

- `calcular_metricas_riesgo_avanzadas` → caché de 2 horas (descarga histórico
  de hasta 5 años, dos veces, cada vez que se llama).
- `calcular_indicadores_tecnicos` → caché de 1 hora.
- `obtener_rating_analistas` → caché corto de 5 minutos (para no perder
  frescura, pero evitando pedir lo mismo varias veces seguidas).

El resto de tus cachés (`obtener_datos_accion`, `obtener_info_completa`,
Wikipedia, macro, screener, etc.) ya estaban bien puestos y se conservaron
igual.

## Cómo correrla

```bash
pip install -r requirements.txt
cp .env.example .env      # y coloca ahí tus llaves reales
streamlit run App.py
```

## Qué NO cambió

- Ninguna funcionalidad, texto, ni estilo visual (CSS) se modificó.
- Los nombres de las variables de entorno (`AP`, `AP1`, `AP2`, `AP3`) son
  los mismos que ya usabas.
- El flujo de botones y secciones es idéntico al original.

## Mejoras de la segunda ronda (caché, carga, fuentes de datos, búsqueda)

### 3) Revisión de cachés
Se agregó `@st.cache_data` a 4 funciones que hacían llamadas costosas (descargas
de Yahoo Finance o a Gemini) sin ningún caché:
- `generar_analisis_riesgo_ia` (Gemini) — 1 hora.
- `crear_grafica_drawdown_mejorada` y `crear_grafica_distribucion_retornos`
  (descargan histórico de precios) — 1 hora.
- `cargar_sp500_paralelo` (Screener: 20 descargas en paralelo) — 30 min.

`obtener_datos_macro()` se quedó sin caché a propósito: no hace ninguna
llamada de red, son **datos de ejemplo fijos** (mira el comentario
`# Datos macroeconómicos simulados` en `nucleo/datos.py`) — no vienen de
ninguna API real todavía. Es una mejora aparte para cuando quieras conectarla
a una fuente real (dejarlo anotado aquí para no olvidarlo).

También encontramos que `cargar_sp500_paralelo()` en realidad solo trae **20
acciones fijas** (las más grandes), no las 500 del índice real — es una
limitación de la app original, no algo que haya cambiado el refactor, pero
vale la pena saberlo si el Screener se siente "incompleto".

### 4) Cargar solo lo necesario por sección
`folium`, `geopy` (`Nominatim`) y `pycountry` solo los usa `vistas/macro.py`
— y ese archivo YA los importaba de forma local (dentro de la función, no al
inicio del archivo). El problema era que `config.py` los volvía a importar
de forma **global**, así que toda sección pagaba ese costo aunque no los
usara. Se quitaron de `config.py`; ahora solo se cargan cuando realmente
entras a Panorama Macro.

Sobre "evitar recalcular al cambiar de pestaña": esto ya lo resuelve el
propio `@st.cache_data` de Streamlit — el caché no se borra al cambiar de
sección, así que si vuelves a una pestaña con el mismo ticker, no se vuelve
a pedir el dato a Yahoo Finance/Finviz/FMP. Por eso el punto 3 (revisar que
todo esté bien cacheado) es, en la práctica, lo que resuelve este punto.

### 1) Depender menos de Finviz
Se agregó `nucleo/fmp.py`, que trae las métricas fundamentales desde
**Financial Modeling Prep** (API real, la llave que ya tenías configurada
como `AP2`/`FMP`, usada hasta ahora solo en Mercados Globales).

Nuevo orden de prioridad en "Métricas Fundamentales Principales":
**FMP → Finviz (scraping) → Yahoo Finance**. Antes era Finviz primero y
Yahoo Finance como único respaldo. Si no tienes configurada la llave de FMP
(`AP2` en tu `.env`), la app simplemente sigue con Finviz y Yahoo Finance
como antes — no se rompe nada si no la tienes.

### 2) Mejor búsqueda de tickers (sin base de datos propia)
Se agregó `buscar_sugerencias_ticker()` en `nucleo/datos.py`, que consulta
**en vivo** el buscador público de Yahoo Finance (no es una base de datos
que mantengamos nosotros). Ahora, si escribes algo que no es un ticker
exacto, la barra de búsqueda te muestra sugerencias reales para elegir —y
si de plano no existe ese símbolo, el mensaje de error es más claro
("No encontramos ningún símbolo llamado...") en vez del error técnico de
antes.

### 📊 Panorama Macro: de datos de ejemplo a datos reales
`obtener_datos_macro()` devolvía un diccionario **fijo**, escrito a mano
(el propio código lo decía: "Datos macroeconómicos simulados"). Se
reemplazó por `nucleo/macro_real.py`, con datos reales de dos fuentes que
**no requieren ninguna llave de API nueva**:
- **FRED** (Reserva Federal de St. Louis) para inflación (CPI interanual),
  desempleo, crecimiento del PIB, tasa de la Fed y confianza del
  consumidor — descarga pública en CSV, sin registro.
- **Yahoo Finance** (ya la usas en toda la app) para los índices bursátiles
  (variación real del año, no inventada), materias primas y divisas.

Si alguna fuente falla momentáneamente (sin internet, la fuente caída),
esa métrica muestra "No disponible" en vez de inventar un número — igual
que en el resto de la app.

### 🔍 Screener: por qué "solo cargaban 20" y cómo se corrigió
Buena noticia: el Screener real (`vistas/screener.py`) **ya intentaba
escanear hasta ~500 acciones**, no 20 — ese límite de 20 vivía en un grupo
de funciones que nunca se usaban (código muerto heredado de una versión
anterior de la app, en `nucleo/datos.py`). Se eliminó ese código muerto
para que no vuelva a generar confusión.

El problema real de fondo era otro: la carga de esas ~500 acciones se hacía
**una por una, sin caché**, con dos llamadas de red cada una — hasta 1,000
peticiones seguidas a Yahoo Finance. Eso es lento y, sobre todo, hace que
Yahoo empiece a rechazar peticiones a la mitad del proceso, dejando cargar
solo un puñado de acciones antes de fallar.

Se corrigió con tres cambios en `vistas/screener.py`:
1. Se quitaron los símbolos repetidos de la lista (varios aparecían 2-3
   veces en distintas categorías).
2. Cada ticker individual ahora tiene su propio caché de 1 hora — una
   segunda búsqueda es casi instantánea.
3. La precarga ahora es **en paralelo** (10 acciones a la vez) en vez de
   secuencial, con una barra de progreso que también muestra cuántas se
   cargaron con éxito.

Aun así, ten en cuenta que Yahoo Finance puede limitar temporalmente si
haces varias búsquedas completas seguidas en poco tiempo — es una
limitación de la fuente de datos gratuita, no del código.

### 🌍 Se quitó el "Resumen en Tiempo Real" de Panorama Macro
A petición tuya: ya no se muestran ahí "Indicadores de Estados Unidos",
"Índices Bursátiles", "Materias Primas" ni "Divisas" — esa sección se quedó
tal cual estaba antes de esa mejora (con el mapa). El código que trae esos
datos reales (`nucleo/macro_real.py`) se dejó intacto por si más adelante
quieres usarlo en otra parte de la app; simplemente ya no se llama desde
Panorama Macro.

### 🔍 Screener: por qué decía "488" y por qué solo 269 cargaban bien
Encontramos la causa exacta: la lista fija tenía **tickers que ya no
existen** — empresas que se fusionaron, fueron compradas, o cambiaron de
símbolo. Por ejemplo: `ATVI` (Activision, comprada por Microsoft en 2023),
`KSU` (Kansas City Southern, fusionada con Canadian Pacific en 2021), `ABC`
(AmerisourceBergen, ahora cotiza como `COR`), `PXD` (Pioneer Natural
Resources, comprada por ExxonMobil en 2024), entre otros. Esos nunca iban a
cargar, sin importar qué tan bien optimizado estuviera el código — Yahoo
Finance simplemente no tiene datos vigentes para ellos.

En vez de ir corrigiendo la lista a mano cada vez que una empresa se
fusiona o cambia de símbolo (y que se vuelva a quedar vieja en unos meses),
se agregó `obtener_lista_sp500_actual()`: trae la lista **real y actual**
del S&P 500 desde Wikipedia (se actualiza sola conforme cambia el índice
de verdad). Si por algún motivo no se puede obtener (sin internet, cambió
el formato de la página), el Screener sigue funcionando con la lista fija
de respaldo — nunca se queda sin funcionar.

Con esto, el número de acciones debería acercarse más a las 500 reales, y
el porcentaje de éxito debería subir bastante (aunque seguirá sin ser
100% — Yahoo Finance a veces limita peticiones si hay muchas seguidas, y
eso no depende del código).


## Mejoras de la cuarta ronda (errores amigables, spinners, PDF/Excel)

### 10) Mensajes de error más amigables
Se agregó `nucleo/errores.py`, con `mostrar_error_amigable(excepcion, contexto)`:
traduce errores técnicos comunes (timeouts, límites de peticiones, llaves de
API inválidas, datos faltantes) a un mensaje claro en español, y deja el
detalle técnico real dentro de un expander plegado ("Detalle técnico") por
si necesitas depurar — ya no se le muestra un traceback de Python a quien
use la app. Se conectó en los 18 lugares donde antes se mostraba el error
crudo (Riesgo, Comparación, Noticias, Análisis IA, Técnico, Screener,
Fundamentales, Mercados Globales, y el reporte del footer).

### 11) Indicador de carga más consistente
Se revisaron las 12 vistas. La mayoría ya tenía `st.spinner` en sus cargas
principales; se agregó donde faltaba — Análisis Técnico y Variación del
Precio no mostraban ningún indicador mientras descargaban el histórico de
precios, y ahora sí.

### 7) Exportar a PDF y Excel con gráficas y formato profesional
Nuevo módulo `nucleo/exportar.py`, con dos botones nuevos junto al de texto
en el footer:

- **PDF** (`reportlab`): portada con el nombre de la empresa, tabla de
  resumen ejecutivo (puntuación y categoría), gráfica de precio del último
  año, tabla de métricas fundamentales con colores, y datos generales de
  la empresa — todo con el mismo morado/índigo de la marca.
- **Excel** (`openpyxl`): una hoja "Resumen" con el mismo contenido que el
  PDF pero en formato de hoja de cálculo (con colores y bordes), y una
  hoja "Histórico de Precios" con una **gráfica nativa de Excel** (de
  líneas, editable dentro de Excel — no una imagen pegada).

Ambos se probaron generándolos con datos de ejemplo y abriéndolos para
confirmar que no salen corruptos y que la gráfica sí aparece. Se agregaron
`reportlab` y `openpyxl` a `requirements.txt` — necesitas volver a correr
`pip install -r requirements.txt` para tenerlos instalados.

## Mejoras de la quinta ronda (tema, comparación múltiple, educación financiera dividida)

### 8) Modo claro/oscuro
El CSS ya no se inyecta una sola vez al importar `config.py` (así nunca se
podía cambiar después) — ahora es la función `aplicar_tema()`, que se llama
en cada corrida desde `App.py`. Arriba del buscador hay un botón
"🌙 Modo oscuro" / "☀️ Modo claro" que guarda tu elección en
`st.session_state.tema` y refresca la página al instante. El modo oscuro
ajusta el fondo, la barra lateral y los botones; las tarjetas con
degradado (`.info-card`, `.ia-analysis`, etc.) se dejaron igual porque ya
se ven bien en ambos temas.

### 9) Comparar más de un índice/moneda a la vez
En "Comparación", el selector que antes solo dejaba elegir **un** índice
ahora es un multiselect con índices (S&P500, NASDAQ, Dow Jones, Russell
2000) **y monedas** (EUR/USD, USD/JPY, USD/MXN, GBP/USD) — puedes marcar
varios y todos se agregan a la tabla y gráfica comparativa. Beta y CAPM
siguen calculándose contra un solo mercado (es lo correcto
matemáticamente), así que se usa el primero que marques; si eliges más de
uno, un aviso en pantalla te dice cuál se está usando para eso.

### 13) `educacion_financiera.py` dividido por categoría
El archivo de ~2,700 líneas ahora es 9 archivos (uno por categoría) dentro
de `vistas/educacion/`, más un orquestador (`vistas/educacion_financiera.py`,
ahora de 60 líneas) que solo decide cuál mostrar según lo que elijas en el
selector. Ningún archivo nuevo pasa de 556 líneas.

De paso se encontró y corrigió un **bug real que ya traía tu app
original**: la sección "Libros Recomendados" tenía mala indentación en el
archivo original y por eso se mostraba siempre, sin importar qué categoría
tuvieras seleccionada (Valoración, Deuda, Crecimiento, etc. — todas
terminaban mostrando también los libros recomendados al final). Ahora
solo aparece dentro de "Consejos Prácticos de Inversión", que es donde
pertenece por tema.

## Correcciones tras probar la quinta ronda

### 📊 Beta mostraba "nan" en Comparación
Cuando el cálculo manual de Beta fallaba de forma silenciosa (fechas que no
alineaban bien entre la acción y el índice/moneda elegidos), el resultado
podía ser matemáticamente "NaN" (No es un Número) en vez de un error — y
como NaN cuenta como "verdadero" para Python, se colaba como si fuera un
valor válido y aparecía literalmente como texto "nan" en la tabla. Se
corrigió en dos capas: ahora se detecta el NaN antes de aceptarlo (cae al
respaldo del Beta de Yahoo Finance), y aunque se colara alguno, la tabla ya
no lo muestra como "nan" sino como "N/A".

### 📈 El título de la gráfica CAPM tapaba los nombres
Se separó la leyenda del título (antes casi se encimaban) y se le dio más
espacio arriba a la gráfica.

### 🔍 Screener: por qué seguía sin llegar a 500
Encontramos algo importante: cuando un ticker fallaba (así fuera por un
rechazo **pasajero** de Yahoo Finance por tantas peticiones en paralelo),
ese fallo se guardaba en caché por **1 hora completa** como si el ticker no
existiera — sin distinguir entre "esta empresa ya no cotiza" y "Yahoo tuvo
un hipo justo en ese momento". Se agregó un reintento automático (con una
pequeña pausa) antes de darse por vencido con cada ticker, así que un fallo
pasajero ya no te cuesta una hora completa de caché. No vas a llegar a
100% (eso depende de Yahoo Finance, no del código), pero debería subir el
porcentaje de éxito.

### 🌍 Mercados Globales: Oro atorado en "Cargando", faltaban IBEX 35 y Shanghai Composite
Encontramos un bug real: el respaldo a Yahoo Finance en Índices, Materias
Primas, Forex y Cripto solo se activaba si **absolutamente todo** fallaba
en Financial Modeling Prep. Si FMP traía la mayoría pero fallaba solo en
un par de símbolos específicos (el plan gratuito de FMP no siempre cubre
"GCUSD" para Oro, o ciertos índices como IBEX 35 y Shanghai Composite), esos
se quedaban sin dato **para siempre** — porque como el resto sí había
funcionado, nunca se activaba el respaldo completo. Ahora Yahoo Finance
rellena automáticamente cualquier elemento faltante, venga de donde venga
la causa — se corrigió en las 4 secciones (Índices, Materias Primas,
Forex, Cripto) porque las 4 tenían exactamente el mismo patrón.

## Correcciones tras la sexta ronda de pruebas

### 📈 El título de la gráfica CAPM seguía tapando los nombres
El ajuste anterior (subir el título y bajar la leyenda) no fue suficiente.
Esta vez se movió la leyenda **debajo** de la gráfica por completo
(horizontal, centrada), separada del título — es el patrón más usado en
gráficas de Plotly justamente para evitar este tipo de choque. No pude
generar una vista previa esta vez (el entorno de prueba no tiene acceso
para descargar el navegador que se necesita para eso), así que si sigue
sin verse bien, dime y lo ajustamos de nuevo con más detalle de qué parte
sigue tapándose.

### 🔍 Screener: subir el porcentaje de acciones cargadas (274 → 384 → buscando 80-85%)
Dos cambios:
1. **Segunda pasada de reintentos.** Después de la primera pasada rápida en
   paralelo (10 a la vez), ahora hay una segunda pasada, más lenta y con
   menos peticiones simultáneas (4 a la vez), que reintenta *solo* las
   acciones que no cargaron en la primera. Menos carga simultánea significa
   menos rechazos de Yahoo Finance, así que debería rescatar una buena
   parte de esas ~100 que antes se quedaban fuera.
2. **La lista de "488" en vez de "500".** Encontramos que la descarga de la
   lista real desde Wikipedia probablemente estaba fallando silenciosamente
   y cayendo a la lista fija de respaldo (~488 símbolos) — Wikipedia a veces
   rechaza peticiones que no se identifican como un navegador real. Se
   corrigió agregando ese encabezado. Ahora, arriba del Screener, vas a ver
   un aviso tipo "📋 Usando lista real y actual (Wikipedia): 503 símbolos"
   (o el aviso de respaldo, si por algún motivo tu conexión no puede llegar
   a Wikipedia) — así sabes exactamente cuál se está usando sin adivinar.

## Correcciones tras la séptima ronda de pruebas

### 🌍 IBEX 35 y Shanghai Composite mostraban "$nan" / "+nan%"
El respaldo a Yahoo Finance ya se estaba activando bien (por eso decía
"Yahoo Finance" abajo), pero para estos dos mercados extranjeros a veces
Yahoo trae una fila con el precio en blanco (NaN) para el día más
reciente. Como matemáticamente NaN es "un número" para Python, se colaba
sin que saltara ningún error y terminaba mostrándose como texto literal
"$nan" / "+nan%".

Se agregó `_precio_y_cambio_yf()`, una función compartida que descarta esas
filas vacías y, si con 2 días no junta 2 valores reales, reintenta con una
ventana de 5 días antes de rendirse. Se aplicó por igual en Índices,
Materias Primas, Forex y Cripto — los 4 lugares donde existía el mismo
riesgo, aunque solo se hubiera notado en estos dos por ahora.

## Correcciones tras la octava ronda de pruebas

### 🤖 "Análisis de Mercados en Tiempo Real" no mostraba el texto
El título y el recuadro morado sí aparecían, pero el texto del análisis se
escribía por separado con `st.write()`, **fuera** de ese recuadro — el
código "abría" el div morado en una llamada a `st.markdown()` y lo
"cerraba" en otra, con el texto en medio; Streamlit no garantiza que eso
quede anidado correctamente, así que el texto podía terminar sin
mostrarse. Se corrigió armando todo el recuadro (título + texto) en una
sola llamada. De paso, se agregó un respaldo por si Gemini alguna vez
responde vacío (bloqueo por filtros de seguridad, límite alcanzado, etc.):
ahora siempre se ve algo dentro del recuadro, aunque sea un aviso de que
el análisis con IA no está disponible en ese momento — nunca un espacio
en blanco.

## Novena ronda: análisis con IA, errores sin llaves y tablas

### 🔑 Error `CONSUMER_SUSPENDED` (Gemini)
No es un bug de la app: Google suspendió el **proyecto** de Google Cloud donde
estaba la llave (por una filtración pública). Cualquier llave nueva creada
*dentro del mismo proyecto* da el mismo error (se reconoce porque en el error
sigue saliendo el mismo número `projects/...`). Hay que crear la llave en un
**proyecto nuevo** en aistudio.google.com y ponerla en `AP=` del `.env`.

### 🙈 Las llaves ya no se muestran en pantalla
`nucleo/errores.py` ahora oculta cualquier llave (`api_key:...`, `AIza...`,
`AQ....`) en todos los mensajes y en los "Detalle técnico". Además, el error
de proyecto suspendido tiene su propio mensaje claro en español.

### 🤖 Un solo ayudante para Gemini (`nucleo/ia.py`)
Todas las secciones nuevas usan `generar_texto_ia()` / `mostrar_analisis_ia()`:
guarda en la sesión las respuestas que sí salieron bien (no gasta cuota en
cada recarga) y no repite un fallo reciente durante 45 segundos; en cuanto la
llave funcione, el análisis vuelve a salir solo.

### Cambios por sección
1. **Inicio**: al pedir el análisis de una empresa, la página se desliza
   automáticamente hasta "ANÁLISIS IA". El error ya no muestra la llave.
2. **Información**: si la traducción falla, ahora se ve la descripción
   original en inglés y el motivo (antes quedaba vacío).
3. **Variación del Precio**: la tabla histórica ahora incluye `SMA_20`,
   `SMA_50` y `SMA_200`, calculadas sobre el historial largo para que la de
   200 días tenga valores aunque elijas un período corto.
4. **Datos Fundamentales**: interpretación con IA debajo de "Análisis
   Gráfico de Riesgo" (drawdown y distribución de retornos).
5. **Análisis Técnico**: interpretación con IA entre "Resumen de
   Indicadores" y "¿Qué son los Indicadores Técnicos?".
6. **Mercados Globales**: el aviso de fallo del análisis global ya es claro y
   sin llaves.

## Ideas para más adelante (acordadas, aún no implementadas)

- Portafolio de inversión (dar seguimiento a varias acciones con cantidad y precio de compra).
- Alertas de precio.
- Mover las claves de API a `st.secrets` en vez de variables de entorno, si
  vas a desplegar en Streamlit Community Cloud (recomendado antes de
  monetizar la app).
- Escribir un par de pruebas simples para `nucleo/` (son funciones puras,
  fáciles de probar sin necesidad de levantar Streamlit).

## Correcciones aplicadas después de tus pruebas

### 🔑 "Análisis IA" da error de API_KEY / la descripción de la empresa no sale
**No es un bug del código, es de configuración.** Ambas cosas usan Gemini
(`genai`), y el error `No API_KEY or ADC found` significa que la variable de
entorno `AP` está vacía. El proyecto nuevo trae su propio `.env.example` en
una carpeta distinta a tu proyecto original — necesitas:

1. Copiar tu archivo `.env` real (el que ya tenías funcionando en el
   proyecto viejo, con tus llaves verdaderas) a esta carpeta nueva, junto a
   `App.py`. O bien `cp .env.example .env` y pegar tus llaves reales ahí.
2. Verificar que el archivo se llame exactamente `.env` (sin `.txt` ni nada
   más) y esté en la misma carpeta que `App.py`.
3. Volver a correr `streamlit run App.py`.

Una vez que `AP` tenga tu llave real de Google Generative AI, tanto la
descripción traducida como el Análisis IA deberían funcionar.

### 🎨 El botón no cambia de color al hacer clic
Era un bug real (ya existía en tu app original, no lo causó la
reestructuración): Streamlit dibuja el botón con su color *antes* de
enterarse de que lo acabas de presionar, así que el que acabas de clickear
se veía "sin seleccionar" hasta tu siguiente clic. Se arregló agregando
`st.rerun()` justo después de guardar la sección elegida
(`nucleo/interfaz.py`), para que la página se refresque de inmediato con el
color correcto.

### 🏢 Métricas Fundamentales Principales en "N/A"
Esa sección depende de "leer" (hacer *scraping*) la página de Finviz, que
puede cambiar su diseño con el tiempo y dejar de encontrar ciertos datos.
Se agregó un **respaldo automático**: si Finviz no trae un dato, ahora se
completa con la información equivalente que ya tenemos de Yahoo Finance
(`vistas/fundamentales.py`, función `_fallback_yfinance`). Debería haber
muchas menos "N/A" ahora. Los pocos campos sin respaldo posible (como "LT
Debt/Eq" o "ROIC" exactos) pueden seguir en N/A si Finviz no los trae.

### 📰 "Noticias de (empresa)" mostraba noticias no relacionadas
Se agregaron dos cosas en `vistas/noticias.py`:
1. Un **filtro de relevancia**: si Finviz mezcla noticias genéricas del
   mercado, ahora se descartan los titulares que no mencionan el ticker ni
   el nombre de la empresa (siempre que queden al menos 3 relevantes; si no,
   se prefiere no perder noticias válidas).
2. Un **respaldo**: si Finviz no trae nada útil, se usan las noticias que
   Yahoo Finance ya asocia directamente a ese ticker (`yf.Ticker(...).news`).

### 📊 Comparación: Beta y Correlación
- Se **eliminó por completo** la sección "🔗 Análisis de Correlación" (matriz
  de correlación, resumen, interpretación) como pediste.
- El cálculo de **Beta** ahora tiene un respaldo: si el cálculo manual falla
  (por ejemplo, por fechas que no coinciden entre la acción y el índice), se
  usa el Beta que ya reporta Yahoo Finance para esa acción, en vez de dejarlo
  en blanco silenciosamente.
- Se quitó "Correlación" de las opciones del multiselect "Métricas
  Adicionales" (ese control nunca filtraba nada, era decorativo — quedó
  igual de decorativo pero sin la opción que ya no existe).

### 📈 "Otros datos distintos a la app original"
Si después de configurar tu `.env` (ver arriba) sigues viendo números
distintos en secciones que usan Finviz (Métricas Fundamentales) o Gemini
(Análisis IA, descripción), es casi seguro la misma causa: sin llaves, esas
fuentes fallan y el programa cae a otro dato o a "N/A". Si el número
diferente es de **precio o indicadores técnicos** (que solo usan Yahoo
Finance, sin llaves), es simplemente que el mercado se movió — no es un
error del código.

### ⚠️ "Error calculando indicadores: ...BB_Upper" / datos raros en general
Causa real encontrada: una versión más nueva de `yfinance` (la que se instaló
al hacer `pip install -r requirements.txt`) cambió su comportamiento y ahora
devuelve columnas de **doble nivel** (ej. `('Close', 'MSFT')`) incluso al
pedir una sola acción — antes no hacía eso. Eso rompía el cálculo de Bandas
de Bollinger y probablemente explicaba también los "datos distintos a la
app original" que reportaste antes.

Se corrigió en un solo lugar (`config.py`), interceptando `yf.download` para
que **siempre** aplane esas columnas antes de que el resto de la app las
use — así no hubo que tocar una por una las más de 20 llamadas repartidas en
8 archivos distintos.

### 🏢 Seguían en "N/A": LT Debt/Eq y ROIC
Ahora sí se calculan (antes se dejaban en N/A a propósito por lo frágil que
es conseguirlos). Se obtienen del balance general y estado de resultados que
ya trae Yahoo Finance:
- **LT Debt/Eq** = Deuda a Largo Plazo ÷ Capital Contable.
- **ROIC** = NOPAT ÷ Capital Invertido, usando una tasa de impuesto fija del
  21% (tasa corporativa de EUA) como aproximación, ya que la tasa efectiva
  real de cada empresa no siempre está disponible por separado.

Es una **aproximación estándar**, no un cálculo idéntico al que usa Finviz
internamente — puede diferir un poco de lo que veías antes. Si algún trimestre
no trae los datos que necesita (empresas nuevas, ciertos sectores como bancos
con estados financieros distintos), seguirá mostrando "N/A" en vez de un
número inventado.

También se agregó respaldo para:
- **Volatility** y **RSI**, calculados con datos que la propia app ya obtiene
  en esa pantalla (métricas de riesgo e indicadores técnicos), en vez de
  depender de que Finviz los traiga.
- **P/FCF**, calculado como `Market Cap / Flujo de Caja Libre` cuando Yahoo
  Finance tiene ese dato disponible.

### 🔑 El error de API_KEY seguía apareciendo después de colocar las llaves
Dos cambios en `config.py`:
1. Ahora acepta la llave bajo tres nombres distintos (`AP`, `GOOGLE_API_KEY`
   o `GEMINI_API_KEY`), por si la guardaste con otro nombre al del
   `.env.example` original.
2. Si de plano no encuentra ninguna, ahora te avisa con un mensaje claro en
   la barra lateral apenas abres la app — así sabes de inmediato si el
   problema es la llave, sin tener que llegar hasta "Análisis IA" para
   enterarte.

Si el aviso sigue apareciendo después de esto, casi siempre es una de estas
tres cosas:
- El archivo no se llama exactamente `.env` (revisa que no sea `.env.txt`).
- No está en la misma carpeta que `App.py`.
- Dejaste la app corriendo y solo recargaste el navegador — Streamlit no
  vuelve a leer el `.env` sin que reinicies el proceso (`Ctrl+C` en la
  terminal y `streamlit run App.py` de nuevo).

