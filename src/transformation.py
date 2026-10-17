"""
Módulo de transformación y control de calidad.

Incluye limpieza de fechas, tratamiento de valores nulos, validación
de duplicados, cálculo de métricas, enriquecimiento con dimensiones
y verificación de integridad referencial.
"""

import pandas as pd
import numpy as np


def limpiar_ventas(ventas: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Limpia y normaliza el DataFrame de ventas.

    Args:
        ventas: DataFrame original de ventas.

    Returns:
        Tupla con el DataFrame limpio y un diccionario de métricas
        de calidad de datos.
    """
    df = ventas.copy()
    metricas_calidad = {}

    metricas_calidad["registros_originales"] = len(df)
    metricas_calidad["cliente_id_nulos"] = int(df["cliente_id"].isna().sum())
    metricas_calidad["order_id_duplicados"] = int(df["order_id"].duplicated().sum())

    # Normalización de fechas con formatos mixtos.
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce", format="mixed")

    fechas_invalidas = df["fecha"].isna().sum()
    metricas_calidad["fechas_invalidas"] = int(fechas_invalidas)

    # Se eliminan registros sin fecha válida.
    df = df.dropna(subset=["fecha"])

    # Los clientes sin identificación se asignan a una categoría estándar.
    df["cliente_id"] = df["cliente_id"].fillna("CLIENTE_DESCONOCIDO")

    # Validación de duplicados por identificador de orden.
    df = df.drop_duplicates(subset=["order_id"], keep="first")

    # Conversión y validación de campos numéricos.
    df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")
    df["precio_unitario"] = pd.to_numeric(df["precio_unitario"], errors="coerce")

    registros_invalidos = df[
        (df["cantidad"] <= 0)
        | (df["precio_unitario"] <= 0)
        | df["cantidad"].isna()
        | df["precio_unitario"].isna()
    ]

    metricas_calidad["registros_con_valores_invalidos"] = len(registros_invalidos)

    # Se eliminan registros que incumplen reglas de negocio.
    df = df[
        (df["cantidad"] > 0)
        & (df["precio_unitario"] > 0)
        & df["cantidad"].notna()
        & df["precio_unitario"].notna()
    ]

    metricas_calidad["registros_finales"] = len(df)

    print("[TRANSFORMACIÓN] Limpieza de ventas completada.")
    print(f"- Fechas inválidas eliminadas: {metricas_calidad['fechas_invalidas']}")
    print(f"- Clientes nulos asignados a 'CLIENTE_DESCONOCIDO': {metricas_calidad['cliente_id_nulos']}")
    print(f"- Órdenes duplicadas eliminadas: {metricas_calidad['order_id_duplicados']}")
    print(f"- Registros con cantidades o precios inválidos: {metricas_calidad['registros_con_valores_invalidos']}")
    print(f"- Registros finales después de la limpieza: {metricas_calidad['registros_finales']}\n")

    return df, metricas_calidad


def calcular_metricas(ventas: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula la venta total y la categoría de venta.

    Args:
        ventas: DataFrame de ventas limpio.

    Returns:
        DataFrame con las columnas 'venta_total' y 'categoria_venta'.
    """
    df = ventas.copy()

    df["venta_total"] = df["cantidad"] * df["precio_unitario"]

    df["categoria_venta"] = np.select(
        condlist=[
            df["venta_total"] < 20,
            df["venta_total"] < 50
        ],
        choicelist=[
            "Baja",
            "Media"
        ],
        default="Alta"
    )

    print("[TRANSFORMACIÓN] Métricas calculadas: venta_total y categoria_venta.")

    return df


def validar_integridad_referencial(
    ventas: pd.DataFrame,
    productos: pd.DataFrame,
    tiendas: pd.DataFrame
) -> pd.DataFrame:
    """
    Valida que los productos y tiendas de las ventas existan en sus catálogos.

    Args:
        ventas: DataFrame de ventas con métricas calculadas.
        productos: Catálogo de productos.
        tiendas: Catálogo de tiendas.

    Returns:
        DataFrame únicamente con registros referencialmente válidos.
    """
    productos_validos = set(productos["producto_id"])
    tiendas_validas = set(tiendas["tienda_id"])

    antes = len(ventas)

    df = ventas[
        ventas["producto_id"].isin(productos_validos)
        & ventas["tienda_id"].isin(tiendas_validas)
    ]

    eliminados = antes - len(df)

    print("[CALIDAD] Validación de integridad referencial completada.")
    print(f"- Registros eliminados por producto o tienda inexistente: {eliminados}\n")

    return df


def enriquecer_datos(
    ventas: pd.DataFrame,
    productos: pd.DataFrame,
    tiendas: pd.DataFrame
) -> pd.DataFrame:
    """
    Enriquece las ventas con información de productos, tiendas y tiempo.

    Args:
        ventas: DataFrame de ventas validado.
        productos: Catálogo de productos.
        tiendas: Catálogo de tiendas.

    Returns:
        DataFrame analítico completo.
    """
    df = ventas.merge(
        productos,
        on="producto_id",
        how="left",
        validate="many_to_one"
    )

    df = df.merge(
        tiendas,
        on="tienda_id",
        how="left",
        validate="many_to_one"
    )

    df["año"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month
    df["nombre_mes"] = df["fecha"].dt.strftime("%B")
    df["dia"] = df["fecha"].dt.day
    df["dia_semana"] = df["fecha"].dt.day_name()

    print("[TRANSFORMACIÓN] Datos enriquecidos con productos, tiendas y dimensiones temporales.\n")

    return df


def transformar_datos(
    ventas: pd.DataFrame,
    productos: pd.DataFrame,
    tiendas: pd.DataFrame
) -> tuple[pd.DataFrame, dict]:
    """
    Ejecuta el proceso completo de transformación.

    Args:
        ventas: DataFrame de ventas crudas.
        productos: Catálogo de productos.
        tiendas: Catálogo de tiendas.

    Returns:
        Tupla con el dataset analítico final y las métricas de calidad.
    """
    ventas_limpias, metricas_calidad = limpiar_ventas(ventas)
    ventas_con_metricas = calcular_metricas(ventas_limpias)
    ventas_validadas = validar_integridad_referencial(
        ventas_con_metricas,
        productos,
        tiendas
    )
    dataset_final = enriquecer_datos(ventas_validadas, productos, tiendas)

    return dataset_final, metricas_calidad