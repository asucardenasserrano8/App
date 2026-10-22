# App.py
import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
import time
import google.generativeai as genai
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import numpy as np
import io
import base64
import random
from dotenv import load_dotenv
import os
import concurrent.futures
from threading import Lock

# yfinance (desde hace algunas versiones) devuelve columnas "MultiIndex"
# (ej. ('Close', 'MSFT')) incluso al pedir una sola acción. Eso rompe cosas
# como el cálculo de Bandas de Bollinger ("Cannot set a DataFrame with
# multiple columns to the single column BB_Upper") y puede causar datos
# inconsistentes en varias secciones. Se corrige UNA vez aquí, envolviendo
# yf.download para toda la app, en vez de tener que arreglarlo en cada
# una de las ~20 llamadas repartidas en distintos archivos.
_yf_download_original = yf.download


def _yf_download_columnas_planas(*args, **kwargs):
    datos = _yf_download_original(*args, **kwargs)
    if hasattr(datos, "columns") and isinstance(datos.columns, pd.MultiIndex):
        datos.columns = datos.columns.get_level_values(0)
    return datos


yf.download = _yf_download_columnas_planas

# Cargar variables de entorno
load_dotenv()

# Configuración de la página (debe ser lo primero)
st.set_page_config(page_title="Análisis de Acciones", layout="wide")

GOOGLE_KEY = os.getenv("AP") or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if GOOGLE_KEY:
    genai.configure(api_key=GOOGLE_KEY)
else:
    # No se detuvo la app: las secciones que no usan IA siguen funcionando.
    # Solo se avisa aquí, una vez, para que sea fácil de detectar el motivo real.
    st.sidebar.warning(
        "⚠️ No se encontró la llave de Gemini (variable AP en tu .env). "
        "El Análisis IA y la traducción de la descripción no van a funcionar "
        "hasta que la agregues."
    )

currencyapi = os.getenv("AP1")

FMP = os.getenv("AP2") #Financial Modeling Prep

AlphaVantage = os.getenv("AP3")

# CSS personalizado mejorado — estilos que se ven igual de bien en ambos temas
_CSS_BASE = """
<style>
    /* Indicadores de métricas */
    .metric-positive { color: #28a745; font-weight: bold; }
    .metric-negative { color: #dc3545; font-weight: bold; }
    .metric-neutral { color: #ffc107; font-weight: bold; }

    /* Tarjetas de información */
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px; border-radius: 10px; color: white; margin: 10px 0;
    }
    .concept-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px; border-radius: 10px; color: white; margin: 10px 0;
        border-left: 5px solid #ff6b6b;
    }
    .macro-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 15px; border-radius: 10px; color: white; margin: 5px 0;
    }
    .ia-analysis {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px; border-radius: 10px; color: white; margin: 10px 0;
        border-left: 5px solid #28a745;
    }
    .ia-recommendation {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 15px; border-radius: 8px; color: white; margin: 8px 0;
        border-left: 4px solid #ff6b6b;
    }
</style>
"""

# Estilos de los botones y del fondo general — estos SÍ cambian según el tema
_CSS_TEMA_CLARO = """
<style>
    .stButton > button {
        border: 2px solid #cccccc; background-color: white; color: black;
        transition: all 0.3s ease;
    }
    .stButton > button:hover { border-color: #adb5bd; background-color: #f8f9fa; }
    .stButton > button.selected {
        border: 3px solid #28a745 !important; background-color: #d4edda !important;
        color: #155724 !important; font-weight: bold;
        box-shadow: 0 2px 4px rgba(40, 167, 69, 0.3);
    }
</style>
"""

_CSS_TEMA_OSCURO = """
<style>
    .stApp { background-color: #0e1117; color: #e6e6e6; }
    [data-testid="stSidebar"] { background-color: #161a23; }
    .stButton > button {
        border: 2px solid #3a3f4b; background-color: #1c1f26; color: #e6e6e6;
        transition: all 0.3s ease;
    }
    .stButton > button:hover { border-color: #667eea; background-color: #262b36; }
    .stButton > button.selected {
        border: 3px solid #28a745 !important; background-color: #1d3a26 !important;
        color: #a3f7bf !important; font-weight: bold;
        box-shadow: 0 2px 4px rgba(40, 167, 69, 0.3);
    }
    [data-testid="stMetric"] { background-color: #1c1f26; padding: 10px; border-radius: 8px; }
    .stDataFrame { filter: none; }
</style>
"""


def aplicar_tema():
    """Inyecta el CSS según el tema elegido (claro por defecto). Se llama en
    cada corrida desde App.py — no puede ir suelta a nivel de módulo porque
    config.py solo se importa (y ejecuta) una vez por sesión, y el tema
    puede cambiar en cualquier momento."""
    st.markdown(_CSS_BASE, unsafe_allow_html=True)
    if st.session_state.get("tema") == "oscuro":
        st.markdown(_CSS_TEMA_OSCURO, unsafe_allow_html=True)
    else:
        st.markdown(_CSS_TEMA_CLARO, unsafe_allow_html=True)

# Inicialización de session_state

# (nota: st.set_page_config ya se ejecutó arriba, al importar este módulo,
#  tal como exige Streamlit: debe ser el primer comando st.* de la app)


def inicializar_estado():
    if 'seccion_actual' not in st.session_state:
        st.session_state.seccion_actual = "inicio"

    if 'favoritas' not in st.session_state:
        st.session_state.favoritas = ["AAPL", "MSFT", "GOOGL", "TSLA", "AMZN"]

    if 'portafolio' not in st.session_state:
        st.session_state.portafolio = {}

    if 'historial_busquedas' not in st.session_state:
        st.session_state.historial_busquedas = []

    if 'cache_lock' not in st.session_state:
        st.session_state.cache_lock = Lock()

    if 'tema' not in st.session_state:
        st.session_state.tema = "claro"
