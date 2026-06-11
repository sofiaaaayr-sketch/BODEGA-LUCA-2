import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Bodega Luca", page_icon="📦", layout="wide")

# Cargar archivos
inventario = pd.read_csv("inventario.csv")
ventas = pd.read_csv("ventas.csv")

st.title("📦 BODEGA LUCA")

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
        st.metric("📦 Productos", len(inventario))

    with col2:
        st.metric("📋 Stock Total", int(inventario["Stock"].sum()))

    with col3:
        if len(ventas) > 0:
            st.metric("💰 Ingresos", f"S/ {ventas['Total'].sum():.2f}")
        else:
            st.metric("💰 Ingresos", "S/ 0.00")

    st.subheader("⚠️ Productos con stock bajo")

    stock_bajo = inventario[inventario["Stock"] < 5]

    if len(stock_bajo) > 0:
        st.dataframe(stock_bajo)
    else:
        st.success("No hay productos con stock bajo")

# INVENTARIO
elif menu == "📦 Inventario":

    st.header("📦 Inventario")

    categoria = st.selectbox(
        "Filtrar categoría",
        ["Todas"] + list(inventario["Categoría"].unique())
    )

    if categoria == "Todas":
        tabla = inventario
    else:
        tabla = inventario[inventario["Categoría"] == categoria]

    st.dataframe(tabla, use_container_width=True)

# BUSCAR
elif menu == "🔍 Buscar Producto":

    st.header("🔍 Buscar Producto")

    buscar = st.text_input("Ingrese nombre del producto")

    if buscar:
        resultado = inventario[
            inventario["Producto"].str.contains(
                buscar,
                case=False,
                na=False
            )
        ]

        st.dataframe(resultado)

# REGISTRAR VENTA
elif menu == "💰 Registrar Venta":

    st.header("💰 Registrar Venta")

    producto = st.selectbox(
        "Producto",
        inventario["Producto"]
    )

    cantidad = st.number_input(
        "Cantidad",
        min_value=1,
        step=1
    )

    if st.button("Registrar Venta"):

        fila = inventario[inventario["Producto"] == producto]

        stock_actual = int(fila["Stock"].values[0])
        precio = float(fila["Precio"].values[0])
        codigo = fila["Código"].values[0]

        if cantidad > stock_actual:
            st.error("Stock insuficiente")

        else:

            nuevo_stock = stock_actual - cantidad

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
                "Fecha": [datetime.now().strftime("%d/%m/%Y %H:%M")],
                "Código": [codigo],
                "Producto": [producto],
                "Cantidad": [cantidad],
                "Total": [total]
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
                f"Venta registrada. Total: S/ {total:.2f}"
            )

# HISTORIAL
elif menu == "📅 Historial de Ventas":

    st.header("📅 Historial de Ventas")

    if len(ventas) > 0:
        st.dataframe(ventas, use_container_width=True)
    else:
        st.info("Aún no hay ventas registradas")

# ACERCA
elif menu == "ℹ️ Acerca del Sistema":

    st.header("ℹ️ Acerca del Sistema")

    st.write("""
    Sistema web desarrollado para la gestión de inventario
    y ventas de la Bodega Luca.

    Funciones:
    - Control de inventario
    - Registro de ventas
    - Historial de ventas
    - Búsqueda de productos
    - Control de stock
    """)
