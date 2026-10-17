<div align="center">

# 🛒 ETL Pipeline · SuperMart Colombia

### Data Pipeline para análisis comercial de ventas retail

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-Scientific%20Computing-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C?style=for-the-badge&logo=plotly&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Graphics-4C8CBF?style=for-the-badge)
![Git](https://img.shields.io/badge/Git-Version%20Control-F05032?style=for-the-badge&logo=git&logoColor=white)

**Proyecto académico de Sistemas de Información**  
**Cliente:** SuperMart Colombia  
**Empresa consultora:** EAN TechRetail Solutions  

</div>

---

## 📌 Descripción del proyecto

SuperMart Colombia cuenta con datos de ventas almacenados en archivos CSV dispersos, con formatos inconsistentes, valores nulos y falta de estructuras analíticas.

Este proyecto implementa un **pipeline ETL completo en Python**, capaz de:

- Extraer datos desde múltiples fuentes CSV.
- Limpiar, validar y estandarizar la información.
- Calcular métricas comerciales.
- Enriquecer los datos con catálogos de productos y tiendas.
- Construir un Data Mart optimizado para análisis.
- Generar visualizaciones ejecutivas automáticas.
- Producir un reporte ejecutivo con hallazgos de negocio.

El resultado es un flujo reproducible que transforma datos crudos en información accionable para la toma de decisiones.

---

## 🔄 Arquitectura del Pipeline

```text
┌─────────────────┐    ┌──────────────────────┐    ┌─────────────────┐
│    EXTRACT      │ →  │      TRANSFORM       │ →  │      LOAD       │
│                 │    │                      │    │                 │
│ -  ventas_crudas │    │ -  Limpieza de datos  │    │ -  Dataset final │
│ -  productos     │    │ -  Fechas y nulos     │    │ -  Data Mart     │
│ -  tiendas       │    │ -  Métricas de venta  │    │ -  Resumen       │
└─────────────────┘    │ -  Validaciones       │    └─────────────────┘
                       └──────────────────────┘              │
                                                             ▼
                                              ┌─────────────────────────┐
                                              │  ANALYSIS & REPORTING   │
                                              │                         │
                                              │ -  Visualizaciones       │
                                              │ -  KPIs de negocio       │
                                              │ -  Reporte ejecutivo     │
                                              └─────────────────────────┘
```

---

## ⚙️ Fases implementadas

### 1️⃣ Extracción — *Extract*

- Lectura de tres fuentes CSV con `pandas`.
- Validación de existencia y formato de los archivos.
- Manejo controlado de errores.
- Reporte de registros cargados por fuente.

**Fuentes de datos:**

| Archivo | Descripción |
|---|---|
| `ventas_crudas.csv` | Transacciones de venta realizadas por tienda |
| `productos.csv` | Catálogo de productos, categorías y marcas |
| `tiendas.csv` | Información de tiendas, ciudades, regiones y gerentes |

---

### 2️⃣ Transformación — *Transform*

El módulo de transformación aplica reglas de calidad y enriquecimiento analítico.

| Proceso | Descripción |
|---|---|
| 📅 Normalización de fechas | Unifica formatos inconsistentes como `2024-03-15` y `2024/03/16` |
| 👤 Clientes desconocidos | Reemplaza valores nulos por `CLIENTE_DESCONOCIDO` |
| 🔁 Control de duplicados | Elimina órdenes repetidas mediante `order_id` |
| 💰 Cálculo de ventas | Genera `venta_total = cantidad × precio_unitario` |
| 🏷️ Segmentación | Clasifica ventas en **Baja**, **Media** y **Alta** |
| 🔗 Integración | Une ventas con productos y tiendas |
| 📆 Dimensiones temporales | Crea año, mes, día y día de la semana |
| ✅ Calidad de datos | Valida cantidades, precios, fechas e integridad referencial |

**Categorías de venta:**

| Categoría | Rango |
|---|---|
| 🟢 Baja | Menor a $20 |
| 🟡 Media | Entre $20 y $50 |
| 🔴 Alta | Igual o mayor a $50 |

---

### 3️⃣ Carga — *Load*

El pipeline genera tres salidas analíticas:

| Archivo generado | Propósito |
|---|---|
| `dataset_transformado.csv` | Dataset completo, limpio y enriquecido |
| `data_mart.csv` | Estructura optimizada para análisis y BI |
| `resumen_ejecutivo.csv` | Métricas agregadas por ciudad, región y categoría |

---

### 4️⃣ Análisis y reportes

Se generan automáticamente:

- 📊 Ventas totales por ciudad.
- 🥧 Distribución de ventas por categoría.
- 📅 Transacciones por día de la semana.
- 📈 Distribución de montos de venta.
- 📄 Reporte ejecutivo en formato TXT.

---

## 🗂️ Estructura del proyecto

```text
etl-supermart-colombia/
│
├── 📁 data/
│   ├── 📁 input/
│   │   ├── 📄 ventas_crudas.csv
│   │   ├── 📄 productos.csv
│   │   └── 📄 tiendas.csv
│   │
│   └── 📁 output/
│       ├── 📄 dataset_transformado.csv
│       ├── 📄 data_mart.csv
│       └── 📄 resumen_ejecutivo.csv
│
├── 📁 src/
│   ├── 🐍 extraction.py
│   ├── 🐍 transformation.py
│   ├── 🐍 loading.py
│   ├── 🐍 analysis.py
│   └── 🐍 main.py
│
├── 📁 reports/
│   ├── 📁 visualizaciones/
│   │   ├── 🖼️ ventas_por_ciudad.png
│   │   ├── 🖼️ ventas_por_categoria.png
│   │   ├── 🖼️ transacciones_dia_semana.png
│   │   └── 🖼️ distribucion_ventas.png
│   │
│   └── 📄 reporte_ejecutivo.txt
│
├── 📄 README.md
├── 📄 requirements.txt
└── 🙈 .gitignore
```

---

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone [https://github.com/tu-usuario/etl-supermart-colombia.git](https://github.com/tu-usuario/etl-supermart-colombia.git)
cd etl-supermart-colombia
```

### 2. Crear y activar el entorno virtual

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar el pipeline

Desde la raíz del proyecto:

```bash
python -m src.main
```

---

## 📤 Salidas generadas

Al ejecutar el pipeline se crean automáticamente:

```text
data/output/dataset_transformado.csv
data/output/data_mart.csv
data/output/resumen_ejecutivo.csv

reports/visualizaciones/ventas_por_ciudad.png
reports/visualizaciones/ventas_por_categoria.png
reports/visualizaciones/transacciones_dia_semana.png
reports/visualizaciones/distribucion_ventas.png

reports/reporte_ejecutivo.txt
```

---

## 📊 Indicadores analizados

El pipeline calcula y reporta indicadores clave como:

- 💵 Ventas totales.
- 🧾 Número de transacciones.
- 🛍️ Unidades vendidas.
- 🎯 Ticket promedio.
- 🏙️ Ciudad con mayores ventas.
- 🏬 Tienda líder.
- 📦 Categoría de producto líder.
- 🧹 Indicadores de calidad de datos.

---

## 🧠 Hallazgos esperados

El análisis permite identificar:

- Las ciudades con mayor participación en las ventas.
- Las categorías de productos con mejor desempeño comercial.
- Los días de la semana con mayor volumen de transacciones.
- La distribución de los montos de venta.
- La calidad de los datos capturados en el punto de venta.

Estos hallazgos pueden apoyar decisiones sobre inventario, promociones, expansión comercial y mejora en la captura de datos.

---

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso en el proyecto |
|---|---|
| 🐍 Python | Lenguaje principal del pipeline |
| 🐼 pandas | Extracción, transformación y carga de datos |
| 🔢 NumPy | Cálculos y validaciones numéricas |
| 📊 Matplotlib | Generación de visualizaciones |
| 📈 Seaborn | Estilo y gráficos estadísticos |
| 🗃️ CSV | Formato de entrada y salida de datos |
| 🌿 Git / GitHub | Control de versiones y publicación del proyecto |

---

## 📈 Posibles mejoras futuras

- [ ] Automatizar la ejecución con GitHub Actions.
- [ ] Cargar el Data Mart en una base de datos SQL.
- [ ] Construir un dashboard interactivo en Power BI o Looker Studio.
- [ ] Incorporar pruebas unitarias con `pytest`.
- [ ] Agregar logging profesional con la librería `logging`.
- [ ] Parametrizar rutas y reglas de negocio mediante archivos de configuración.

---

## 👤 Autor

<div align="center">

**[Isabella Naranjo, Nicolas Varon, Nicole Daza]**  
Ingeniería de Sistemas · EAN  
Rol: **Ingeniero de Datos**  

[![GitHub](https://img.shields.io/badge/GitHub-Perfil-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/tu-usuario)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Perfil-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/tu-usuario/)

</div>

---

<div align="center">

⭐ Si este proyecto te parece útil, no olvides dejar una estrella en el repositorio.

</div>