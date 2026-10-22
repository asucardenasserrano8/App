"""
Módulo generado automáticamente a partir de App.py original.
Importa todo lo común desde config para no repetir imports en cada módulo.
"""
from config import *

from nucleo.datos import obtener_datos_accion
from nucleo.scoring import calcular_scoring_fundamental, generar_reporte_texto
from nucleo.errores import mostrar_error_amigable
from nucleo.exportar import generar_reporte_pdf, generar_reporte_excel


def mostrar_footer(stonk, info, nombre):
    """Reporte descargable, historial, favoritos y aviso legal (se muestra
    siempre, sin importar la sección activa).
    """
    # BOTONES ADICIONALES EN EL FOOTER
    st.markdown("---")
    st.write("**📥 Descargar Reporte:**")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Generar reporte de texto
        if st.button("📄 Texto (.txt)", use_container_width=True):
            try:
                with st.spinner("Generando reporte..."):
                    datos = obtener_datos_accion(stonk)

                    # Verificar que tenemos datos
                    if datos.empty:
                        st.error("No se pudieron obtener datos para generar el reporte")
                    else:
                        scoring, metricas = calcular_scoring_fundamental(info)
                        reporte_texto = generar_reporte_texto(stonk, info, datos, scoring, metricas)

                        # Mostrar preview del reporte
                        with st.expander("📋 Vista Previa del Reporte"):
                            st.text(reporte_texto)

                        # Botón de descarga
                        st.download_button(
                            label="📥 Descargar (TXT)",
                            data=reporte_texto,
                            file_name=f"reporte_{stonk}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
            except Exception as e:
                mostrar_error_amigable(e, "la generación del reporte")

    with col2:
        # Generar reporte en PDF, con gráfica y formato profesional
        if st.button("🧾 PDF", use_container_width=True):
            try:
                with st.spinner("Generando PDF..."):
                    datos = obtener_datos_accion(stonk)
                    if datos.empty:
                        st.error("No se pudieron obtener datos para generar el reporte")
                    else:
                        scoring, metricas = calcular_scoring_fundamental(info)
                        pdf_buffer = generar_reporte_pdf(stonk, info, datos, scoring, metricas, nombre)
                        st.download_button(
                            label="📥 Descargar (PDF)",
                            data=pdf_buffer,
                            file_name=f"reporte_{stonk}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                        )
            except Exception as e:
                mostrar_error_amigable(e, "la generación del PDF")

    with col3:
        # Generar reporte en Excel, con gráfica nativa editable
        if st.button("📊 Excel", use_container_width=True):
            try:
                with st.spinner("Generando Excel..."):
                    datos = obtener_datos_accion(stonk)
                    if datos.empty:
                        st.error("No se pudieron obtener datos para generar el reporte")
                    else:
                        scoring, metricas = calcular_scoring_fundamental(info)
                        excel_buffer = generar_reporte_excel(stonk, info, datos, scoring, metricas, nombre)
                        st.download_button(
                            label="📥 Descargar (XLSX)",
                            data=excel_buffer,
                            file_name=f"reporte_{stonk}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True,
                        )
            except Exception as e:
                mostrar_error_amigable(e, "la generación del Excel")

    with col4:
        # Historial de búsquedas
        if st.session_state.historial_busquedas:
            with st.popover("🔍 Historial Búsquedas", use_container_width=True):
                st.write("**Búsquedas recientes:**")
                for busqueda in reversed(st.session_state.historial_busquedas):
                    if st.button(f"📌 {busqueda}", key=f"hist_{busqueda}", use_container_width=True):
                        st.session_state.seccion_actual = "info"
                        st.rerun()
        else:
            with st.popover("🔍 Historial Búsquedas", use_container_width=True):
                st.info("No hay búsquedas recientes")

    # FAVORITOS RÁPIDOS
    if st.session_state.favoritas:
        st.markdown("---")
        st.write("⭐ **Favoritos Rápidos:**")
        cols_fav = st.columns(len(st.session_state.favoritas))

        for i, favorita in enumerate(st.session_state.favoritas):
            with cols_fav[i]:
                if st.button(f"📈 {favorita}", use_container_width=True, key=f"fav_{favorita}"):
                    st.session_state.seccion_actual = "info"

    # --- DISCLAIMER FINAL ---
    st.markdown("""
    ---
    <p style='text-align: center; font-size: 13px; color: gray;'>
    © 2025 Todos los derechos reservados. Desarrollado por <strong>Jesús Alberto Cárdenas Serrano.</strong>
    <br><em>Esta aplicación es con fines educativos. No constituye asesoramiento financiero.</em>
    </p>
    """, unsafe_allow_html=True)
