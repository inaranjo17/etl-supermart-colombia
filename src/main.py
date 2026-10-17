"""
Script principal del pipeline ETL.

Ejecuta las fases de extracción, transformación, carga,
análisis y generación del reporte ejecutivo.
"""

from src.extraction import extraer_datos
from src.transformation import transformar_datos
from src.loading import cargar_datos
from src.analysis import generar_visualizaciones, generar_reporte_ejecutivo
from src.generar_reporte_pdf import generar_reporte_pdf


RUTA_VENTAS = "data/input/ventas_crudas.csv"
RUTA_PRODUCTOS = "data/input/productos.csv"
RUTA_TIENDAS = "data/input/tiendas.csv"

RUTA_SALIDA_DATOS = "data/output"
RUTA_SALIDA_GRAFICAS = "reports/visualizaciones"
RUTA_REPORTE = "reports/reporte_ejecutivo.txt"


def main() -> None:
    """Ejecuta el pipeline ETL completo."""
    print("=" * 60)
    print("PIPELINE ETL - SUPERMART COLOMBIA")
    print("=" * 60)

    # Fase 1: Extracción
    datos = extraer_datos(
        ruta_ventas=RUTA_VENTAS,
        ruta_productos=RUTA_PRODUCTOS,
        ruta_tiendas=RUTA_TIENDAS
    )

    # Fase 2: Transformación
    dataset_transformado, metricas_calidad = transformar_datos(
        ventas=datos["ventas"],
        productos=datos["productos"],
        tiendas=datos["tiendas"]
    )

    # Fase 3: Carga
    resultados = cargar_datos(
        dataset=dataset_transformado,
        ruta_salida=RUTA_SALIDA_DATOS
    )

    # Fase 4: Análisis y reportes
    generar_visualizaciones(
        dataset=resultados["dataset_transformado"],
        ruta_salida=RUTA_SALIDA_GRAFICAS
    )

    generar_reporte_ejecutivo(
        dataset=resultados["dataset_transformado"],
        metricas_calidad=metricas_calidad,
        ruta_reporte=RUTA_REPORTE
    )

    generar_reporte_pdf()

    print("=" * 60)
    print("PIPELINE ETL EJECUTADO CORRECTAMENTE")
    print("=" * 60)


if __name__ == "__main__":
    main()