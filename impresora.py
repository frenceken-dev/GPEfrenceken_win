# impresora.py

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.utils import simpleSplit
from tkinter import messagebox
import webbrowser, platform, subprocess, pathlib
import os

class ImpresorPDF:
    @staticmethod
    def generar_pdf(titulo, datos, columnas, nombre_archivo, logo_path=None):
        if nombre_archivo == 'historial_costos_producto_especifico':
            ruta_pdf = f"historial_costo/{nombre_archivo}.pdf"
        
        elif nombre_archivo == 'historial_costos_producto_todos':
            ruta_pdf = f"historial_costo/{nombre_archivo}.pdf"
        
        else:
            ruta_pdf = f"historial_ganancias/{nombre_archivo}.pdf"

        def header_footer(canvas, doc):
            # Header con logo
            if logo_path and os.path.exists(logo_path):
                logo = Image(logo_path, width=90, height=40)
                logo.drawOn(canvas, 50, letter[1] - 70)

            # Footer con número de página
            canvas.saveState()
            canvas.setFont("Helvetica", 10)
            canvas.drawCentredString(letter[0] / 2.0, 30, f"Página {doc.page}")
            canvas.restoreState()

        # Crear el documento con márgenes ajustados
        doc = SimpleDocTemplate(
            ruta_pdf,
            pagesize=letter,
            leftMargin=30,
            rightMargin=30,
            topMargin=100,
            bottomMargin=50
        )

        styles = getSampleStyleSheet()
        story = []

        # Título
        titulo_pdf = Paragraph(f"{titulo}", styles["Heading1"])
        story.append(titulo_pdf)
        story.append(Spacer(1, 12))

        # Estilo para las celdas de la tabla
        estilo_celda = ParagraphStyle(
            name="Celda",
            fontName="Helvetica",
            fontSize=8,
            leading=9,
            alignment=TA_LEFT
        )

        # Preparar los datos para la tabla
        tabla_datos = []

        # Agregar encabezados
        tabla_datos.append([Paragraph(col, estilo_celda) for col in columnas])

        # Agregar datos
        for fila in datos:
            fila_formateada = []
            for valor in fila:
                if valor is None:
                    valor = ""
                # Convertir el valor a Paragraph para manejar texto largo
                fila_formateada.append(Paragraph(str(valor), estilo_celda))
            tabla_datos.append(fila_formateada)

        # Calcular los anchos de las columnas
        def calcular_anchos_columnas(tabla_datos):
            anchos = [0] * len(columnas)
            for fila in tabla_datos:
                for i, celda in enumerate(fila):
                    # Obtener el ancho requerido para el texto
                    texto = celda.getPlainText() if hasattr(celda, 'getPlainText') else str(celda)
                    ancho_texto = len(texto) * 4  # Factor aproximado para el ancho de los caracteres
                    if ancho_texto > anchos[i]:
                        anchos[i] = ancho_texto

            # Asegurar un ancho mínimo
            anchos = [max(ancho, 60) for ancho in anchos]

            # Ajustar los anchos para que no excedan el ancho de la página
            ancho_total = sum(anchos)
            ancho_disponible = letter[0] - 100  # Restar márgenes izquierdo y derecho

            if ancho_total > ancho_disponible:
                factor = ancho_disponible / ancho_total
                anchos = [ancho * factor for ancho in anchos]

            return anchos

        col_widths = calcular_anchos_columnas(tabla_datos)

        # Crear la tabla
        tabla = Table(tabla_datos, colWidths=col_widths, repeatRows=1)
        tabla.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Alinear texto a la parte superior
        ]))

        story.append(tabla)

        # Generar el PDF
        doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)

        # Abrir el PDF automáticamente
        if os.path.exists(ruta_pdf):
            try:
                if platform.system() == "Darwin":
                    subprocess.run(["open", ruta_pdf])
                else:
                    webbrowser.open(ruta_pdf)
            except Exception:
                # fallback universal
                webbrowser.open(pathlib.Path(ruta_pdf).absolute().as_uri())
        else:
            messagebox.showerror("⚠️ Error", "No se pudo generar el PDF.")

        return ruta_pdf
    