"""
educacion_financiera.py — Orquestador de la pestaña de Educación Financiera.

Antes: ~2,700 líneas en un solo archivo con las 9 categorías mezcladas.
Ahora: cada categoría vive en su propio archivo bajo vistas/educacion/, y
este archivo solo decide cuál mostrar según lo que el usuario elija.
"""
from config import *

from vistas.educacion.valoracion_mercado import mostrar_valoracion_mercado
from vistas.educacion.rentabilidad_margenes import mostrar_rentabilidad_margenes
from vistas.educacion.deuda_liquidez import mostrar_deuda_liquidez
from vistas.educacion.eficiencia_operativa import mostrar_eficiencia_operativa
from vistas.educacion.crecimiento import mostrar_crecimiento
from vistas.educacion.indicadores_tecnicos_edu import mostrar_indicadores_tecnicos_edu
from vistas.educacion.datos_corporativos import mostrar_datos_corporativos
from vistas.educacion.riesgo_avanzado_edu import mostrar_riesgo_avanzado_edu
from vistas.educacion.consejos_inversion import mostrar_consejos_inversion


def mostrar_educacion_financiera(stonk, ticker, info, nombre, descripcion, start_date, end_date):
    st.header("🎓 Educación Financiera - Guía Completa de 82 Métricas")
    st.write("**Explicación DETALLADA de cada métrica: qué es, para qué sirve, ventajas y desventajas**")

    categorias = [
        "💰 VALORACIÓN Y MERCADO (18 métricas)",
        "📈 RENTABILIDAD Y MÁRGENES (16 métricas)",
        "🏦 DEUDA Y LIQUIDEZ (12 métricas)",
        "📊 EFICIENCIA OPERATIVA (10 métricas)",
        "📈 CRECIMIENTO (8 métricas)",
        "📊 INDICADORES TÉCNICOS (10 métricas)",
        "🏢 DATOS CORPORATIVOS (8 métricas)",
        "⚡ MÉTRICAS AVANZADAS DE RIESGO",
        "💡 CONSEJOS PRÁCTICOS DE INVERSIÓN"
    ]

    categoria = st.selectbox("Selecciona la categoría:", categorias)

    st.markdown("---")

    args = (stonk, ticker, info, nombre, descripcion, start_date, end_date)

    if categoria == "💰 VALORACIÓN Y MERCADO (18 métricas)":
        mostrar_valoracion_mercado(*args)
    elif categoria == "📈 RENTABILIDAD Y MÁRGENES (16 métricas)":
        mostrar_rentabilidad_margenes(*args)
    elif categoria == "🏦 DEUDA Y LIQUIDEZ (12 métricas)":
        mostrar_deuda_liquidez(*args)
    elif categoria == "📊 EFICIENCIA OPERATIVA (10 métricas)":
        mostrar_eficiencia_operativa(*args)
    elif categoria == "📈 CRECIMIENTO (8 métricas)":
        mostrar_crecimiento(*args)
    elif categoria == "📊 INDICADORES TÉCNICOS (10 métricas)":
        mostrar_indicadores_tecnicos_edu(*args)
    elif categoria == "🏢 DATOS CORPORATIVOS (8 métricas)":
        mostrar_datos_corporativos(*args)
    elif categoria == "⚡ MÉTRICAS AVANZADAS DE RIESGO":
        mostrar_riesgo_avanzado_edu(*args)
    else:
        mostrar_consejos_inversion(*args)
