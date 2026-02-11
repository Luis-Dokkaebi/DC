# Codigo/generar_reporte_pdf.py
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from Codigo import config

class ReportePDF:
    def __init__(self, output_path, config_data):
        self.output_path = output_path
        self.config = config_data
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=50, leftMargin=50,
            topMargin=50, bottomMargin=50
        )
        self.styles = getSampleStyleSheet()
        self.elements = []

        # Estilos personalizados
        self.styles.add(ParagraphStyle(name='CenteredTitle', parent=self.styles['Title'], alignment=1, fontSize=24, spaceAfter=20))
        self.styles.add(ParagraphStyle(name='CenteredSubTitle', parent=self.styles['Heading2'], alignment=1, fontSize=16, spaceAfter=20))
        self.styles.add(ParagraphStyle(name='HeaderLeft', parent=self.styles['Normal'], fontSize=10, textColor=colors.grey))
        self.styles.add(ParagraphStyle(name='HeaderRight', parent=self.styles['Normal'], fontSize=10, alignment=2, textColor=colors.grey))
        self.styles.add(ParagraphStyle(name='TableCell', parent=self.styles['Normal'], fontSize=10, alignment=1))
        self.styles.add(ParagraphStyle(name='PhotoLabel', parent=self.styles['Normal'], fontSize=10, alignment=1, spaceBefore=5))

    def _header_footer(self, canvas, doc):
        canvas.saveState()
        # Header
        canvas.setFont('Helvetica', 9)
        logo_path = self.config.get("logo_path", "")
        if os.path.exists(logo_path):
            try:
                canvas.drawImage(logo_path, 50, letter[1] - 50, width=50, height=30, preserveAspectRatio=True, mask='auto')
            except Exception:
                pass # Fail silently if logo is invalid

        canvas.drawString(120, letter[1] - 40, f"{self.config.get('project_name', 'PROJECT REPORT')}")
        canvas.drawRightString(letter[0] - 50, letter[1] - 40, f"Report No: {self.config.get('report_number', '001')}")

        # Footer
        canvas.line(50, 50, letter[0] - 50, 50)
        canvas.drawString(50, 35, f"{self.config.get('footer_text', 'CONFIDENTIAL')}")
        canvas.drawRightString(letter[0] - 50, 35, f"Page {doc.page}")
        canvas.restoreState()

    def create_cover_page(self):
        # Espacio vertical inicial
        self.elements.append(Spacer(1, 2*inch))

        # Logos si existen
        logo_path = self.config.get("logo_path", "")
        if os.path.exists(logo_path):
            try:
                im = RLImage(logo_path, width=2*inch, height=1*inch)
                im.hAlign = 'CENTER'
                self.elements.append(im)
                self.elements.append(Spacer(1, 0.5*inch))
            except Exception:
                pass

        # Título del Proyecto
        self.elements.append(Paragraph(self.config.get("project_name", "CONSTRUCTION PROJECT"), self.styles['CenteredTitle']))
        self.elements.append(Spacer(1, 0.5*inch))

        # Detalles
        data = [
            ["Location:", self.config.get("location", "N/A")],
            ["Contractor:", self.config.get("contractor", "N/A")],
            ["Report Number:", self.config.get("report_number", "N/A")],
            ["Date:", "Unknown"] # TODO: Add date logic
        ]

        t = Table(data, colWidths=[2*inch, 3*inch])
        t.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('ALIGN', (0,0), (0,-1), 'RIGHT'),
            ('ALIGN', (1,0), (1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TEXTCOLOR', (0,0), (0,-1), colors.darkblue),
        ]))
        self.elements.append(t)
        self.elements.append(PageBreak())

    def create_summary_table(self, conteo, etapa_actual, porcentaje):
        self.elements.append(Paragraph("Executive Summary", self.styles['Heading2']))
        self.elements.append(Spacer(1, 0.2*inch))

        self.elements.append(Paragraph(f"Current Stage Detected: <b>{etapa_actual}</b>", self.styles['Normal']))
        self.elements.append(Paragraph(f"Estimated Progress: <b>{porcentaje}%</b>", self.styles['Normal']))
        self.elements.append(Spacer(1, 0.3*inch))

        data = [["Stage / Class", "Count", "Status"]]

        # Ordenar por config.ETAPAS si es posible
        sorted_stages = sorted(config.ETAPAS.items(), key=lambda x: x[1]['orden'])

        # Mapear conteo a etapas
        for stage_name, info in sorted_stages:
            count = 0
            # Sumar conteos de clases que coincidan con la etapa
            for cls, c in conteo.items():
                if stage_name.lower() in cls.lower():
                    count += c

            status = "Pending"
            if count > 0:
                status = "Active/Completed"

            data.append([stage_name, str(count), status])

        # Agregar clases no mapeadas
        mapped_classes = [s[0].lower() for s in sorted_stages]
        others_count = 0
        for cls, c in conteo.items():
            is_mapped = False
            for mapped in mapped_classes:
                if mapped in cls.lower():
                    is_mapped = True
                    break
            if not is_mapped:
                others_count += c

        if others_count > 0:
            data.append(["Other / Unclassified", str(others_count), "Review"])

        t = Table(data, colWidths=[3*inch, 1.5*inch, 2*inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.navy),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ]))
        self.elements.append(t)
        self.elements.append(PageBreak())

    def create_photo_grid(self, resultados):
        self.elements.append(Paragraph("Detailed Photo Log", self.styles['Heading2']))
        self.elements.append(Spacer(1, 0.2*inch))

        # Grid 2x3 (2 columnas, 3 filas por página = 6 fotos)
        # Preparar datos para la tabla
        row_data = []
        table_data = []

        for i, (nombre, etiqueta, ruta) in enumerate(resultados):
            try:
                # Cargar imagen y redimensionar para el reporte
                img = RLImage(ruta, width=3*inch, height=2.25*inch)

                # Crear celda con imagen y texto
                cell_content = [
                    img,
                    Paragraph(f"<b>{etiqueta}</b>", self.styles['PhotoLabel']),
                    Paragraph(f"File: {nombre}", self.styles['PhotoLabel'])
                ]

                row_data.append(cell_content)

                if len(row_data) == 2:
                    table_data.append(row_data)
                    row_data = []
            except Exception as e:
                print(f"Error loading image {ruta}: {e}")

        # Si queda una imagen suelta
        if row_data:
            while len(row_data) < 2:
                row_data.append("") # Celda vacía
            table_data.append(row_data)

        # Crear tabla grande (podría dividirse automáticamente por reportlab, pero mejor hacerlo por chunks si es muy grande,
        # aunque reportlab maneja saltos de página en tablas grandes si se configura bien, pero con imágenes es delicado.
        # Mejor crear una tabla por cada X filas o dejar que fluya)

        t = Table(table_data, colWidths=[3.5*inch, 3.5*inch])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            # ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey), # Opcional grid
        ]))
        self.elements.append(t)

    def create_charts_section(self):
        # Insertar gráfico de barras generado previamente
        chart_path = os.path.join(config.RESULTADOS_DIR, "grafica_conteo.png")
        if os.path.exists(chart_path):
            self.elements.append(PageBreak())
            self.elements.append(Paragraph("Progress Distribution", self.styles['Heading2']))
            self.elements.append(Spacer(1, 0.2*inch))
            try:
                img = RLImage(chart_path, width=6*inch, height=4*inch)
                self.elements.append(img)
            except Exception:
                pass

    def build_pdf(self, resultados, conteo, etapa_actual, porcentaje):
        self.create_cover_page()
        self.create_summary_table(conteo, etapa_actual, porcentaje)
        self.create_charts_section()
        self.create_photo_grid(resultados)

        self.doc.build(self.elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer)
        print(f"📄 PDF Professional guardado: {self.output_path}")

def generar_pdf(resultados, conteo, etapa_actual, porcentaje):
    output_path = os.path.join(config.RESULTADOS_DIR, "reporte_resultados.pdf")
    reporte = ReportePDF(output_path, config.REPORT_CONFIG)
    reporte.build_pdf(resultados, conteo, etapa_actual, porcentaje)
