# modules/bolsas.py
import streamlit as st
import pandas as pd
from data_loaders import load_bolsas

def bolsas_page():
    st.title("Bolsas")
    st.markdown("---")
    df = load_bolsas("base.xlsx")
    df_plot = df.rename(columns={"Dates": "Date"})
    numeric_cols = [c for c in df_plot.columns if c != "Date"]
    series = st.selectbox("Bolsas", numeric_cols)

    spec = {
        "mark": {"type": "line", "color": "#06333B"},
        "encoding": {
            "x": {"field": "Date", "type": "temporal", "title": "Date",
                  "axis": {"grid": True, "gridColor": "#e0e0e0", "gridOpacity": 1}},
            "y": {"field": series, "type": "quantitative", "title": series,
                  "axis": {"grid": True, "gridColor": "#e0e0e0", "gridOpacity": 1}}
        },
        "selection": {"grid": {"type": "interval", "bind": "scales"}}
    }
    st.subheader("Bolsas")
    st.vega_lite_chart(df_plot, spec, use_container_width=True)

    # Gráfico comparativo usando índices (Dez/24 = 100)
    df_idx = df_plot.set_index("Date").copy()
    monthly = df_idx.resample("M").last()
    base_dec24 = monthly.loc["2024-12-31"]
    df_idx = df_idx.div(base_dec24) * 100
    df_indexed = df_idx.reset_index()

    st.subheader("Bolsas: Comparação")
    st.markdown("###### Dez/24 = 100")
    all_series = [c for c in df_indexed.columns if c != "Date"]
    chosen = st.multiselect("Quais bolsas?", all_series, default=all_series)
    df_sel = df_indexed[["Date"] + chosen]
    df_long_sel = df_sel.melt(id_vars="Date", var_name="Bolsa", value_name="Índice")

    spec_index = {
        "mark": {"type": "line"},
        "encoding": {
            "x": {"field": "Date", "type": "temporal",
                  "axis": {"grid": True, "gridColor": "#e0e0e0", "gridOpacity": 1}},
            "y": {"field": "Índice", "type": "quantitative",
                  "axis": {"grid": True, "gridColor": "#e0e0e0", "gridOpacity": 1}},
            "color": {"field": "Bolsa", "type": "nominal"}
        },
        "selection": {"grid": {"type": "interval", "bind": "scales"}}
    }
    st.vega_lite_chart(df_long_sel, spec_index, use_container_width=True)

