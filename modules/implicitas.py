import streamlit as st
import pandas as pd
from data_loaders import load_implicitas


def implicitas_page():
    st.title("Inflação implícita")
    st.markdown("---")
    df = load_implicitas("Acompanhamento de Implícitas.xlsx.")
    df_plot = df.rename(columns={"Dates": "Date"})
    numeric_cols = [c for c in df_plot.columns if c != "Date"]
    series = st.selectbox("Prazo", numeric_cols)

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
    st.subheader("Inflação Implícita")
    st.vega_lite_chart(df_plot, spec, use_container_width=True)