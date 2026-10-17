"""
Módulo de carga de datos.

Genera los archivos de salida: dataset transformado completo,
Data Mart analítico y resumen ejecutivo agregado.
"""

from pathlib import Path

import pandas as pd


def crear_carpeta(ruta: str) -> Path:
    """
    Crea una carpeta si no existe.

    Args:
        ruta: Ruta de la carpeta.

    Returns:
        Objeto Path de la carpeta creada o existente.
    """
    carpeta = Path(ruta)
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta


def guardar_csv(df: pd.DataFrame, ruta: str, nombre_archivo: str) -> None:
    """
    Guarda un DataFrame como archivo CSV.

    Args:
        df: DataFrame que se desea exportar.
        ruta: Carpeta de destino.
        nombre_archivo: Nombre del archivo CSV.
    """
    carpeta = crear_carpeta(ruta)
    archivo = carpeta / nombre_archivo

    df.to_csv(archivo, index=False, encoding="utf-8-sig")

    print(f"[CARGA] Archivo generado: {archivo}")


def crear_data_mart(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Construye un Data Mart optimizado para análisis comercial.

    Args:
        dataset: Dataset transformado completo.

    Returns:
        DataFrame con las dimensiones y métricas más relevantes.
    """
    columnas_data_mart = [
        "order_id",
        "fecha",
        "año",
        "mes",
        "nombre_mes",
        "dia",
        "dia_semana",
        "producto_id",
        "categoria",
        "subcategoria",
        "marca",
        "tienda_id",
        "ciudad",
        "region",
        "cliente_id",
        "cantidad",
        "precio_unitario",
        "venta_total",
        "categoria_venta"
    ]

    data_mart = dataset[columnas_data_mart].copy()

    print("[CARGA] Data Mart analítico creado.\n")

    return data_mart


def crear_resumen_ejecutivo(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Genera un resumen agregado por ciudad y categoría de producto.

    Args:
        dataset: Dataset transformado completo.

    Returns:
        DataFrame con métricas agregadas de negocio.
    """
    resumen = (
        dataset
        .groupby(["ciudad", "region", "categoria"], as_index=False)
        .agg(
            transacciones=("order_id", "count"),
            unidades_vendidas=("cantidad", "sum"),
            ventas_totales=("venta_total", "sum"),
            ticket_promedio=("venta_total", "mean")
        )
        .sort_values(
            by="ventas_totales",
            ascending=False
        )
    )

    resumen["participacion_ventas_pct"] = (
        resumen["ventas_totales"] / resumen["ventas_totales"].sum() * 100
    ).round(2)

    print("[CARGA] Resumen ejecutivo agregado creado.\n")

    return resumen


def cargar_datos(
    dataset: pd.DataFrame,
    ruta_salida: str
) -> dict:
    """
    Ejecuta la fase de carga y exporta todos los archivos CSV.

    Args:
        dataset: Dataset transformado completo.
        ruta_salida: Carpeta donde se guardarán los resultados.

    Returns:
        Diccionario con los DataFrames exportados.
    """
    data_mart = crear_data_mart(dataset)
    resumen_ejecutivo = crear_resumen_ejecutivo(dataset)

    guardar_csv(dataset, ruta_salida, "dataset_transformado.csv")
    guardar_csv(data_mart, ruta_salida, "data_mart.csv")
    guardar_csv(resumen_ejecutivo, ruta_salida, "resumen_ejecutivo.csv")

    return {
        "dataset_transformado": dataset,
        "data_mart": data_mart,
        "resumen_ejecutivo": resumen_ejecutivo
    }