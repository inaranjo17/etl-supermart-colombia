"""
Módulo de extracción de datos.

Se encarga de leer los archivos CSV de entrada, validar su existencia
y estructura básica, y reportar estadísticas iniciales de carga.
"""

import pandas as pd


def extraer_csv(ruta: str, nombre_fuente: str) -> pd.DataFrame:
    """
    Lee un archivo CSV y realiza validaciones básicas de carga.

    Args:
        ruta: Ruta relativa del archivo CSV.
        nombre_fuente: Nombre descriptivo de la fuente de datos.

    Returns:
        DataFrame con los datos cargados.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si el archivo tiene un formato incorrecto.
    """
    try:
        df = pd.read_csv(ruta)
    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Error: no se encontró el archivo '{ruta}' ({nombre_fuente})."
        ) from error

    except pd.errors.ParserError as error:
        raise ValueError(
            f"Error: el archivo '{ruta}' tiene un formato CSV inválido."
        ) from error

    except UnicodeDecodeError as error:
        raise ValueError(
            f"Error: no fue posible decodificar el archivo '{ruta}'."
        ) from error

    if df.empty:
        raise ValueError(
            f"Error: el archivo '{ruta}' no contiene registros."
        )

    print(f"[EXTRACCIÓN] {nombre_fuente}: {len(df)} registros cargados desde '{ruta}'.")

    return df


def extraer_datos(ruta_ventas: str, ruta_productos: str, ruta_tiendas: str) -> dict:
    """
    Extrae los tres conjuntos de datos del proyecto.

    Args:
        ruta_ventas: Ruta del archivo de ventas crudas.
        ruta_productos: Ruta del archivo de productos.
        ruta_tiendas: Ruta del archivo de tiendas.

    Returns:
        Diccionario con los DataFrames de ventas, productos y tiendas.
    """
    ventas = extraer_csv(ruta_ventas, "Ventas crudas")
    productos = extraer_csv(ruta_productos, "Productos")
    tiendas = extraer_csv(ruta_tiendas, "Tiendas")

    print("\n[EXTRACCIÓN] Resumen inicial de fuentes:")
    print(f"- Ventas: {ventas.shape[0]} filas y {ventas.shape[1]} columnas.")
    print(f"- Productos: {productos.shape[0]} filas y {productos.shape[1]} columnas.")
    print(f"- Tiendas: {tiendas.shape[0]} filas y {tiendas.shape[1]} columnas.\n")

    return {
        "ventas": ventas,
        "productos": productos,
        "tiendas": tiendas,
    }