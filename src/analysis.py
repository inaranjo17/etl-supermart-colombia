"""
Módulo de análisis, visualización y reporte ejecutivo.

Genera gráficos ejecutivos y un reporte textual con métricas
principales, líderes comerciales e indicadores de calidad.
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def configurar_estilo_visual() -> None:
    """Configura el estilo visual de las gráficas."""
    sns.set_theme(style="whitegrid")
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.titleweight"] = "bold"


def graficar_ventas_por_ciudad(dataset: pd.DataFrame, ruta_salida: str) -> None:
    """Genera y guarda el gráfico de ventas totales por ciudad."""
    ventas_ciudad = (
        dataset
        .groupby("ciudad", as_index=False)["venta_total"]
        .sum()
        .sort_values("venta_total", ascending=False)
    )

    plt.figure()
    ax = sns.barplot(
        data=ventas_ciudad,
        x="ciudad",
        y="venta_total",
        palette="viridis",
        hue="ciudad",
        legend=False
    )

    ax.set_title("Ventas totales por ciudad")
    ax.set_xlabel("Ciudad")
    ax.set_ylabel("Ventas totales ($)")

    for contenedor in ax.containers:
        ax.bar_label(contenedor, fmt="%.2f")

    plt.tight_layout()
    plt.savefig(f"{ruta_salida}/ventas_por_ciudad.png", dpi=300)
    plt.close()

    print("[ANÁLISIS] Gráfico generado: ventas_por_ciudad.png")


def graficar_ventas_por_categoria(dataset: pd.DataFrame, ruta_salida: str) -> None:
    """Genera y guarda el gráfico circular de ventas por categoría."""
    ventas_categoria = (
        dataset
        .groupby("categoria")["venta_total"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure()
    plt.pie(
        ventas_categoria,
        labels=ventas_categoria.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=sns.color_palette("viridis", len(ventas_categoria))
    )

    plt.title("Distribución de ventas por categoría")
    plt.tight_layout()
    plt.savefig(f"{ruta_salida}/ventas_por_categoria.png", dpi=300)
    plt.close()

    print("[ANÁLISIS] Gráfico generado: ventas_por_categoria.png")


def graficar_transacciones_por_dia(dataset: pd.DataFrame, ruta_salida: str) -> None:
    """Genera y guarda el gráfico de transacciones por día de la semana."""
    orden_dias = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    transacciones = (
        dataset
        .groupby("dia_semana")["order_id"]
        .count()
        .reindex(orden_dias)
        .fillna(0)
    )

    plt.figure()
    ax = sns.barplot(
        x=transacciones.index,
        y=transacciones.values,
        palette="crest",
        hue=transacciones.index,
        legend=False
    )

    ax.set_title("Transacciones por día de la semana")
    ax.set_xlabel("Día de la semana")
    ax.set_ylabel("Número de transacciones")
    plt.xticks(rotation=30)

    for contenedor in ax.containers:
        ax.bar_label(contenedor)

    plt.tight_layout()
    plt.savefig(f"{ruta_salida}/transacciones_dia_semana.png", dpi=300)
    plt.close()

    print("[ANÁLISIS] Gráfico generado: transacciones_dia_semana.png")


def graficar_distribucion_ventas(dataset: pd.DataFrame, ruta_salida: str) -> None:
    """Genera y guarda el histograma de montos de venta."""
    plt.figure()
    ax = sns.histplot(
        data=dataset,
        x="venta_total",
        bins=10,
        kde=True,
        color="#2a9d8f"
    )

    ax.set_title("Distribución de montos de venta")
    ax.set_xlabel("Monto de venta ($)")
    ax.set_ylabel("Frecuencia")

    plt.tight_layout()
    plt.savefig(f"{ruta_salida}/distribucion_ventas.png", dpi=300)
    plt.close()

    print("[ANÁLISIS] Gráfico generado: distribucion_ventas.png")


def generar_visualizaciones(dataset: pd.DataFrame, ruta_salida: str) -> None:
    """
    Genera todas las visualizaciones requeridas.

    Args:
        dataset: Dataset transformado completo.
        ruta_salida: Carpeta donde se guardarán las imágenes.
    """
    Path(ruta_salida).mkdir(parents=True, exist_ok=True)
    configurar_estilo_visual()

    graficar_ventas_por_ciudad(dataset, ruta_salida)
    graficar_ventas_por_categoria(dataset, ruta_salida)
    graficar_transacciones_por_dia(dataset, ruta_salida)
    graficar_distribucion_ventas(dataset, ruta_salida)


def generar_reporte_ejecutivo(
    dataset: pd.DataFrame,
    metricas_calidad: dict,
    ruta_reporte: str
) -> None:
    """
    Genera el reporte ejecutivo en formato TXT.

    Args:
        dataset: Dataset transformado completo.
        metricas_calidad: Métricas obtenidas durante la limpieza.
        ruta_reporte: Ruta del archivo TXT a generar.
    """
    Path(ruta_reporte).parent.mkdir(parents=True, exist_ok=True)

    ventas_totales = dataset["venta_total"].sum()
    transacciones = dataset["order_id"].nunique()
    ticket_promedio = dataset["venta_total"].mean()

    ciudad_lider = (
        dataset
        .groupby("ciudad")["venta_total"]
        .sum()
        .idxmax()
    )

    categoria_lider = (
        dataset
        .groupby("categoria")["venta_total"]
        .sum()
        .idxmax()
    )

    tienda_lider = (
        dataset
        .groupby(["tienda_id", "ciudad"])["venta_total"]
        .sum()
        .idxmax()
    )

    reporte = f"""REPORTE EJECUTIVO
Proyecto: Pipeline ETL para análisis de ventas retail
Cliente: SuperMart Colombia
Empresa consultora: EAN TechRetail Solutions

1. RESUMEN GENERAL
--------------------------------------------------
Ventas totales: ${ventas_totales:,.2f}
Número de transacciones: {transacciones}
Ticket promedio: ${ticket_promedio:,.2f}
Unidades vendidas: {dataset['cantidad'].sum():,.0f}

2. DESEMPEÑO COMERCIAL
--------------------------------------------------
Ciudad con mayores ventas: {ciudad_lider}
Categoría líder: {categoria_lider}
Tienda líder: {tienda_lider[0]} - {tienda_lider[1]}

3. INDICADORES DE CALIDAD DE DATOS
--------------------------------------------------
Registros originales: {metricas_calidad['registros_originales']}
Registros finales válidos: {metricas_calidad['registros_finales']}
Clientes nulos corregidos: {metricas_calidad['cliente_id_nulos']}
Órdenes duplicadas eliminadas: {metricas_calidad['order_id_duplicados']}
Fechas inválidas eliminadas: {metricas_calidad['fechas_invalidas']}
Registros con valores numéricos inválidos: {metricas_calidad['registros_con_valores_invalidos']}

4. HALLAZGOS PRINCIPALES
--------------------------------------------------
- La categoría '{categoria_lider}' concentra la mayor parte de las ventas,
  por lo que representa una oportunidad para fortalecer inventario,
  promociones y estrategias comerciales.
- La ciudad de {ciudad_lider} lidera el desempeño en ventas y puede
  considerarse como referencia para replicar buenas prácticas comerciales.
- La tienda {tienda_lider[0]} de {tienda_lider[1]} presenta el mayor
  aporte económico dentro de la red de tiendas analizadas.

5. RECOMENDACIONES
--------------------------------------------------
- Priorizar disponibilidad de inventario en la categoría líder.
- Analizar el comportamiento de los clientes sin identificación para
  mejorar la captura de datos en el punto de venta.
- Estandarizar la captura de fechas y datos de cliente desde el origen.
- Utilizar el Data Mart generado como base para tableros de Power BI,
  Looker Studio u otra herramienta de visualización.

Reporte generado automáticamente por el pipeline ETL.
"""

    with open(ruta_reporte, "w", encoding="utf-8") as archivo:
        archivo.write(reporte)

    print(f"[ANÁLISIS] Reporte ejecutivo generado: {ruta_reporte}")