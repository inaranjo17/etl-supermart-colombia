"""
Generador automático del reporte ejecutivo en formato PDF.

Este módulo construye un reporte profesional con formato APA 7,
incorporando métricas del pipeline ETL, tablas analíticas y las
visualizaciones generadas por el sistema.
"""

from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# Rutas del proyecto
RUTA_DATASET = "data/output/dataset_transformado.csv"
RUTA_RESUMEN = "data/output/resumen_ejecutivo.csv"
RUTA_VISUALIZACIONES = "reports/visualizaciones"
RUTA_PDF = "reports/reporte_ejecutivo.pdf"

# Datos institucionales
TITULO = "Pipeline ETL para el Análisis de Ventas de SuperMart Colombia"
AUTOR = "Isabella Naranjo, Nicolas Varon, Nicole Daza"
INSTITUCION = "Universidad de La Sabana"
CURSO = "Information Systems S2G4"
DOCENTE = "Ing. Javier Daza"
FECHA = "16 de octubre de 2026"


def cargar_datos() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Carga el dataset transformado y el resumen ejecutivo."""
    dataset = pd.read_csv(RUTA_DATASET)
    resumen = pd.read_csv(RUTA_RESUMEN)

    return dataset, resumen


def crear_estilos() -> dict:
    """Define los estilos tipográficos del reporte."""
    estilos = getSampleStyleSheet()

    estilos.add(
        ParagraphStyle(
            name="TituloAPA",
            fontName="Times-Bold",
            fontSize=16,
            leading=22,
            alignment=TA_CENTER,
            spaceAfter=18,
        )
    )

    estilos.add(
        ParagraphStyle(
            name="TituloSeccion",
            fontName="Times-Bold",
            fontSize=13,
            leading=18,
            spaceBefore=16,
            spaceAfter=8,
        )
    )

    estilos.add(
        ParagraphStyle(
            name="TextoAPA",
            fontName="Times-Roman",
            fontSize=11,
            leading=17,
            alignment=TA_JUSTIFY,
            spaceAfter=10,
        )
    )

    estilos.add(
        ParagraphStyle(
            name="TituloFigura",
            fontName="Times-BoldItalic",
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            spaceBefore=6,
            spaceAfter=16,
        )
    )

    estilos.add(
        ParagraphStyle(
            name="Referencia",
            fontName="Times-Roman",
            fontSize=11,
            leading=17,
            leftIndent=0.5 * inch,
            firstLineIndent=-0.5 * inch,
            spaceAfter=10,
        )
    )

    return estilos


def agregar_portada(elementos: list, estilos: dict) -> None:
    """Agrega la portada con formato APA 7."""
    elementos.append(Spacer(1, 1.8 * inch))
    elementos.append(Paragraph(TITULO, estilos["TituloAPA"]))
    elementos.append(Spacer(1, 0.4 * inch))

    datos_portada = [
        AUTOR,
        INSTITUCION,
        CURSO,
        DOCENTE,
        FECHA,
    ]

    for dato in datos_portada:
        elementos.append(
            Paragraph(
                dato,
                ParagraphStyle(
                    name="Portada",
                    parent=estilos["TextoAPA"],
                    alignment=TA_CENTER,
                    spaceAfter=6,
                ),
            )
        )

    elementos.append(PageBreak())


def agregar_resumen_ejecutivo(
    elementos: list,
    estilos: dict,
    dataset: pd.DataFrame,
) -> None:
    """Agrega el resumen ejecutivo y los indicadores principales."""
    ventas_totales = dataset["venta_total"].sum()
    transacciones = dataset["order_id"].nunique()
    unidades = dataset["cantidad"].sum()
    ticket_promedio = dataset["venta_total"].mean()

    ciudad_lider = dataset.groupby("ciudad")["venta_total"].sum().idxmax()
    categoria_lider = dataset.groupby("categoria")["venta_total"].sum().idxmax()
    tienda_lider = dataset.groupby(["tienda_id", "ciudad"])["venta_total"].sum().idxmax()

    elementos.append(Paragraph("Resumen Ejecutivo", estilos["TituloSeccion"]))

    elementos.append(
        Paragraph(
            """
            El presente reporte presenta los resultados del pipeline ETL desarrollado para
            SuperMart Colombia. El sistema integró, limpió, validó y transformó datos de
            ventas provenientes de múltiples fuentes CSV, generando un conjunto de datos
            analítico confiable para la toma de decisiones comerciales.
            """,
            estilos["TextoAPA"],
        )
    )

    datos_kpi = [
        ["Indicador", "Valor"],
        ["Ventas totales", f"${ventas_totales:,.2f}"],
        ["Transacciones", f"{transacciones:,}"],
        ["Unidades vendidas", f"{unidades:,.0f}"],
        ["Ticket promedio", f"${ticket_promedio:,.2f}"],
        ["Ciudad líder", ciudad_lider],
        ["Categoría líder", categoria_lider],
        ["Tienda líder", f"{tienda_lider[0]} - {tienda_lider[1]}"],
    ]

    tabla_kpi = Table(datos_kpi, colWidths=[2.8 * inch, 2.8 * inch])
    tabla_kpi.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1D3557")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D5DD")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F1F5F9")]),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elementos.append(tabla_kpi)
    elementos.append(
        Paragraph(
            "Tabla 1. Indicadores principales del desempeño comercial de SuperMart Colombia.",
            estilos["TituloFigura"],
        )
    )


def agregar_analisis(
    elementos: list,
    estilos: dict,
    dataset: pd.DataFrame,
    resumen: pd.DataFrame,
) -> None:
    """Agrega el análisis comercial y las visualizaciones."""
    elementos.append(Paragraph("Análisis Comercial", estilos["TituloSeccion"]))

    elementos.append(
        Paragraph(
            """
            El análisis de los datos permite identificar el comportamiento comercial de la
            cadena por ciudad, categoría de producto y día de la semana. Las visualizaciones
            presentadas a continuación fueron generadas automáticamente por el pipeline ETL
            a partir del dataset transformado y validado.
            """,
            estilos["TextoAPA"],
        )
    )

    figuras = [
        (
            "ventas_por_ciudad.png",
            "Figura 1. Ventas totales por ciudad.",
            """
            La Figura 1 muestra las ventas totales por ciudad. Este indicador permite
            identificar los mercados con mayor aporte económico y orientar decisiones
            relacionadas con inventario, personal comercial y estrategias de expansión.
            """,
        ),
        (
            "ventas_por_categoria.png",
            "Figura 2. Distribución de ventas por categoría.",
            """
            La Figura 2 presenta la participación de cada categoría en las ventas totales.
            Este análisis facilita la identificación de líneas de producto prioritarias y
            oportunidades de optimización del portafolio comercial.
            """,
        ),
        (
            "transacciones_dia_semana.png",
            "Figura 3. Transacciones por día de la semana.",
            """
            La Figura 3 muestra la cantidad de transacciones registradas por día de la
            semana. Esta información puede apoyar la planificación de personal, promociones
            y estrategias de atención al cliente.
            """,
        ),
        (
            "distribucion_ventas.png",
            "Figura 4. Distribución de montos de venta.",
            """
            La Figura 4 presenta la distribución de los montos de venta. El histograma
            permite observar la concentración de transacciones por rango de valor y apoyar
            el diseño de estrategias de precios y promociones.
            """,
        ),
    ]

    for nombre_archivo, titulo, descripcion in figuras:
        ruta_imagen = Path(RUTA_VISUALIZACIONES) / nombre_archivo

        if ruta_imagen.exists():
            elementos.append(Paragraph(titulo, estilos["TextoAPA"]))
            elementos.append(Image(str(ruta_imagen), width=6.2 * inch, height=3.7 * inch))
            elementos.append(Paragraph(descripcion, estilos["TextoAPA"]))
            elementos.append(Spacer(1, 0.15 * inch))
        else:
            elementos.append(
                Paragraph(
                    f"No se encontró la visualización: {nombre_archivo}.",
                    estilos["TextoAPA"],
                )
            )

    elementos.append(PageBreak())

    elementos.append(Paragraph("Resumen por Ciudad y Categoría", estilos["TituloSeccion"]))

    columnas = ["Ciudad", "Región", "Categoría", "Transacciones", "Ventas totales", "Participación (%)"]
    filas = [columnas]

    for _, fila in resumen.head(10).iterrows():
        filas.append(
            [
                fila["ciudad"],
                fila["region"],
                fila["categoria"],
                f"{fila['transacciones']:,.0f}",
                f"${fila['ventas_totales']:,.2f}",
                f"{fila['participacion_ventas_pct']:.2f}%",
            ]
        )

    tabla_resumen = Table(filas, repeatRows=1)
    tabla_resumen.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1D3557")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ALIGN", (3, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D0D5DD")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F1F5F9")]),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    elementos.append(tabla_resumen)
    elementos.append(
        Paragraph(
            "Tabla 2. Resumen agregado de ventas por ciudad, región y categoría de producto.",
            estilos["TituloFigura"],
        )
    )


def agregar_calidad_y_recomendaciones(elementos: list, estilos: dict) -> None:
    """Agrega control de calidad, conclusiones y recomendaciones."""
    elementos.append(Paragraph("Control de Calidad de Datos", estilos["TituloSeccion"]))

    elementos.append(
        Paragraph(
            """
            El pipeline implementó controles de calidad orientados a garantizar la confiabilidad
            del análisis. Se normalizaron fechas inconsistentes, se asignó un identificador
            estándar a los clientes sin información, se eliminaron órdenes duplicadas y se
            validaron valores numéricos y relaciones referenciales entre las tablas de ventas,
            productos y tiendas.
            """,
            estilos["TextoAPA"],
        )
    )

    elementos.append(Paragraph("Conclusiones", estilos["TituloSeccion"]))

    elementos.append(
        Paragraph(
            """
            La implementación del pipeline ETL permitió transformar archivos CSV dispersos en
            un conjunto de datos estructurado, validado y listo para análisis. La integración
            de información comercial, geográfica y temporal facilita la identificación de
            patrones de venta y oportunidades de mejora operativa.
            """,
            estilos["TextoAPA"],
        )
    )

    elementos.append(Paragraph("Recomendaciones", estilos["TituloSeccion"]))

    recomendaciones = [
        "Fortalecer la disponibilidad de inventario en las categorías con mayor participación en ventas.",
        "Analizar los registros con clientes desconocidos para mejorar la captura de datos en punto de venta.",
        "Estandarizar los formatos de fecha y los identificadores de cliente desde las fuentes originales.",
        "Utilizar el Data Mart generado como base para tableros interactivos en Power BI o Looker Studio.",
        "Priorizar estrategias comerciales en las ciudades y tiendas con mayor desempeño económico.",
    ]

    for recomendacion in recomendaciones:
        elementos.append(
            Paragraph(
                f"• {recomendacion}",
                estilos["TextoAPA"],
            )
        )


def agregar_referencias(elementos: list, estilos: dict) -> None:
    """Agrega las referencias en formato APA 7."""
    elementos.append(PageBreak())
    elementos.append(Paragraph("Referencias", estilos["TituloSeccion"]))

    referencias = [
        "Matplotlib Development Team. (2026). <i>Matplotlib: Visualization with Python</i>. https://matplotlib.org/",
        "NumPy Developers. (2026). <i>NumPy: The fundamental package for scientific computing with Python</i>. https://numpy.org/",
        "pandas development team. (2026). <i>pandas: Powerful Python data analysis toolkit</i>. https://pandas.pydata.org/",
        "ReportLab. (2026). <i>ReportLab PDF Toolkit user guide</i>. https://docs.reportlab.com/",
        "Seaborn development team. (2026). <i>seaborn: Statistical data visualization</i>. https://seaborn.pydata.org/",
    ]

    for referencia in referencias:
        elementos.append(Paragraph(referencia, estilos["Referencia"]))


def configurar_encabezado(canvas, documento) -> None:
    """Agrega número de página en la esquina superior derecha, según APA 7."""
    canvas.saveState()
    canvas.setFont("Times-Roman", 11)
    canvas.drawRightString(letter[0] - inch, letter[1] - 0.6 * inch, str(canvas.getPageNumber()))
    canvas.restoreState()


def generar_reporte_pdf() -> None:
    """Genera el reporte ejecutivo completo en formato PDF."""
    dataset, resumen = cargar_datos()
    estilos = crear_estilos()

    Path(RUTA_PDF).parent.mkdir(parents=True, exist_ok=True)

    documento = SimpleDocTemplate(
        RUTA_PDF,
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
        title=TITULO,
        author=AUTOR,
    )

    elementos = []

    agregar_portada(elementos, estilos)
    agregar_resumen_ejecutivo(elementos, estilos, dataset)
    agregar_analisis(elementos, estilos, dataset, resumen)
    agregar_calidad_y_recomendaciones(elementos, estilos)
    agregar_referencias(elementos, estilos)

    documento.build(
        elementos,
        onFirstPage=configurar_encabezado,
        onLaterPages=configurar_encabezado,
    )

    print(f"[REPORTE] PDF generado correctamente: {RUTA_PDF}")


if __name__ == "__main__":
    generar_reporte_pdf()