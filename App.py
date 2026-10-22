"""
App.py — Orquestador principal de Índice.

Antes: un solo archivo de 11,842 líneas con funciones duplicadas.
Ahora: este archivo solo decide qué vista mostrar; toda la lógica vive en
nucleo/ (funciones reutilizables) y vistas/ (una función por sección).
"""
import streamlit as st

import config  # ejecuta st.set_page_config y carga de API keys al importarse
from config import inicializar_estado, aplicar_tema
from nucleo.interfaz import render_barra_principal
from nucleo.footer import mostrar_footer
from vistas import (
    informacion, inicio, variacion_precio, fundamentales, noticias,
    riesgo, comparacion, tecnico, analisis_ia, screener, macro,
    mercados_globales,
)

inicializar_estado()
aplicar_tema()

stonk, ticker, info, nombre, descripcion, start_date, end_date = render_barra_principal()
ARGS = (stonk, ticker, info, nombre, descripcion, start_date, end_date)

seccion = st.session_state.seccion_actual

if seccion == "info":
    informacion.mostrar_seccion_informacion(*ARGS)
elif seccion == "inicio":
    inicio.mostrar_seccion_inicio(*ARGS)
elif seccion == "datos":
    variacion_precio.mostrar_seccion_variacion_precio(*ARGS)
elif seccion == "fundamentales":
    fundamentales.mostrar_seccion_fundamentales(*ARGS)
elif seccion == "noticias":
    noticias.mostrar_seccion_noticias(*ARGS)
elif seccion == "riesgo":
    riesgo.mostrar_seccion_riesgo(*ARGS)
elif seccion == "comparar":
    comparacion.mostrar_seccion_comparacion(*ARGS)
elif seccion == "tecnico":
    tecnico.mostrar_seccion_tecnico(*ARGS)
elif seccion == "ia":
    analisis_ia.mostrar_seccion_analisis_ia(*ARGS)
elif seccion == "screener":
    screener.mostrar_seccion_screener(*ARGS)
elif seccion == "macro":
    macro.mostrar_seccion_macro(*ARGS)
elif seccion == "global":
    mercados_globales.mostrar_seccion_mercados_globales(*ARGS)

st.caption(
    "⚠️ Proyecto académico con fines educativos. La información proviene de Yahoo Finance "
    "y puede tener retrasos o errores. Los análisis con IA son generados automáticamente "
    "y no constituyen asesoría financiera ni recomendación de inversión."
)

mostrar_footer(stonk, info, nombre)
