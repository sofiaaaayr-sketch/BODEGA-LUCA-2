import streamlit as st
import pandas as pd
from datetime import datetime

# CONFIGURACIÓN
st.set_page_config(
    page_title="Bodega Luca",
    page_icon="📦",
    layout="wide"
)

# ESTILOS
st.markdown("""
<style>

.stApp {
    background-color: #F3E9DB;
}

[data-testid="stSidebar"] {
    background-color: #DCC7AE;
}

h1, h2, h3 {
    color: #3D2C24 !important;
}

div[data-testid="metric-container"] {
    background-color: white;
    border: 2px solid #BFA386;
    border-radius: 15px;
    padding: 15px;
}

.stButton > button {
    background-color: #8A6B54;
    color: white;
    border-radius: 10px;
    border: none;
}

.stButton > button:hover {
    background-color: #3D2C24;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# CARGAR DATOS
inventario = pd.read_csv("inventario.csv")
ventas = pd.read_csv("ventas.csv")

# TÍTULO
st.markdown(
    """
    <h1 style='text-align:center; color:#3D2C24;'>
    📦 BODEGA LUCA
    </h1>
    """,
    unsafe_allow_html=True
)

st.caption(
    f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}"
)

# MENÚ
menu = st.sidebar.selectbox(
    "Menú",
    [
        "📊 Dashboard",
        "📦 Inventario",
        "🔍 Buscar Producto",
        "💰 Registrar Venta",
        "📅 Historial de Ventas",
        "ℹ️ Acerca del Sistema"
    ]
)

# DASHBOARD
if menu == "📊 Dashboard":

    st.header("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📦 Productos",
            len(inventario)
        )

    with col2:
        st.metric(
            "📋 Stock Total",
            int(inventario["Stock"].sum())
        )

    with col3:
        ingresos = (
            ventas["Total"].sum()
            if len(ventas) > 0
            else 0
        )

        st.metric(
            "💰 Ingresos Totales",
            f"S/ {ingresos:.2f}"
        )

    st.divider()

    st.subheader("⚠️ Productos con Stock Bajo")

    stock_bajo = inventario[
        inventario["Stock"] < 5
    ]

    if len(stock_bajo) > 0:
        st.dataframe(
            stock_bajo,
            use_container_width=True
        )
    else:
        st.success(
            "No hay productos con stock bajo."
        )

# INVENTARIO
elif menu == "📦 Inventario":

    st.header("📦 Inventario")

    categoria = st.selectbox(
        "Filtrar por categoría",
        ["Todas"] +
        list(inventario["Categoría"].unique())
    )

    if categoria == "Todas":
        tabla = inventario
    else:
        tabla = inventario[
            inventario["Categoría"] == categoria
        ]

    st.dataframe(
        tabla,
        use_container_width=True
    )

# BUSCAR PRODUCTO
elif menu == "🔍 Buscar Producto":

    st.header("🔍 Buscar Producto")

    texto = st.text_input(
        "Escribe el nombre del producto"
    )

    if texto:

        resultado = inventario[
            inventario["Producto"].str.contains(
                texto,
                case=False,
                na=False
            )
        ]

        if len(resultado) > 0:
            st.dataframe(
                resultado,
                use_container_width=True
            )
        else:
            st.warning(
                "No se encontraron productos."
            )

# REGISTRAR VENTA
elif menu == "💰 Registrar Venta":

    st.header("💰 Registrar Venta")

    producto = st.selectbox(
        "Seleccione un producto",
        inventario["Producto"]
    )

    cantidad = st.number_input(
        "Cantidad",
        min_value=1,
        step=1
    )

    if st.button("Registrar Venta"):

        fila = inventario[
            inventario["Producto"] == producto
        ]

        stock = int(fila["Stock"].values[0])
        precio = float(fila["Precio"].values[0])
        codigo = fila["Código"].values[0]

        if cantidad > stock:

            st.error(
                "Stock insuficiente."
            )

        else:

            nuevo_stock = stock - cantidad

            inventario.loc[
                inventario["Producto"] == producto,
                "Stock"
            ] = nuevo_stock

            inventario.to_csv(
                "inventario.csv",
                index=False
            )

            total = cantidad * precio

            nueva_venta = pd.DataFrame({
                "Fecha":[datetime.now().strftime("%d/%m/%Y %H:%M")],
                "Código":[codigo],
                "Producto":[producto],
                "Cantidad":[cantidad],
                "Total":[total]
            })

            ventas = pd.concat(
                [ventas, nueva_venta],
                ignore_index=True
            )

            ventas.to_csv(
                "ventas.csv",
                index=False
            )

            st.success(
                f"Venta registrada correctamente. Total: S/ {total:.2f}"
            )

# HISTORIAL
elif menu == "📅 Historial de Ventas":

    st.header("📅 Historial de Ventas")

    if len(ventas) > 0:

        st.dataframe(
            ventas,
            use_container_width=True
        )

        st.metric(
            "Ventas Registradas",
            len(ventas)
        )

    else:

        st.info(
            "No existen ventas registradas."
        )

# ACERCA
elif menu == "ℹ️ Acerca del Sistema":

    st.header("ℹ️ Acerca del Sistema")

    st.write("""
### Sistema Web de Gestión de Inventario y Ventas

Bodega Luca es una aplicación web desarrollada en Python y Streamlit para administrar productos, controlar el stock y registrar ventas.

#### Funcionalidades

- Gestión de inventario
- Búsqueda de productos
- Registro de ventas
- Historial de ventas
- Control de stock
- Dashboard de indicadores

#### Tecnologías utilizadas

- Python
- Streamlit
- Pandas
- CSV
""")
