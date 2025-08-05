# modules/cambio.py
import streamlit as st
import pandas as pd
from data_loaders import load_cambio


def cambio_page():
    st.title("Câmbio")
    st.markdown("---")
    df = load_cambio("base.xlsx")
    df_plot = df.rename(columns={"Dates": "Date"})
    numeric_cols = [c for c in df_plot.columns if c != "Date"]
    series = st.selectbox("Moedas", numeric_cols)

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
    st.subheader("Moedas")
    st.markdown("Currency/USD")
    st.vega_lite_chart(df_plot, spec, use_container_width=True)

    # Transformação em índice (Dez/24 = 100)
    df_idx = df_plot.set_index("Date").copy()
    monthly = df_idx.resample("M").last()
    base_dec24 = monthly.loc["2024-12-31"]
    df_idx = df_idx.div(base_dec24) * 100
    df_indexed = df_idx.reset_index()

    st.subheader("Moedas: Peers")
    st.markdown("###### Dez/24=100: Currency/USD")
    all_currencies = [c for c in df_indexed.columns if c != "Date"]
    chosen = st.multiselect("Quais moedas?", all_currencies, default=all_currencies)
    df_sel = df_indexed[["Date"] + chosen]
    df_long_sel = df_sel.melt(id_vars="Date", var_name="Currency", value_name="Index")

    spec_zoom = {
        "mark": {"type": "line"},
        "encoding": {
            "x": {"field": "Date", "type": "temporal",
                  "axis": {"grid": True, "gridColor": "#e0e0e0", "gridOpacity": 1}},
            "y": {"field": "Index", "type": "quantitative",
                  "axis": {"grid": True, "gridColor": "#e0e0e0", "gridOpacity": 1}},
            "color": {"field": "Currency", "type": "nominal"}
        },
        "selection": {"grid": {"type": "interval", "bind": "scales"}}
    }
    st.vega_lite_chart(df_long_sel, spec_zoom, use_container_width=True)
