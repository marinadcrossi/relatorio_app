# modules/commodities.py
import streamlit as st
import pandas as pd
from data_loaders import load_commodities_usd
from data_loaders import load_commodities_brl

def commodities_page():
    st.title("Commodities")
    st.markdown("---")
    # Carrega dados USD e BRL
    df_usd = load_commodities_usd("base.xlsx")
    df_brl = load_commodities_brl("base.xlsx")

    # Padroniza coluna de data
    df_usd = df_usd.rename(columns={"Dates": "Date"})
    df_brl = df_brl.rename(columns={"Dates": "Date"})

    # Cria abas
    tab_usd, tab_brl = st.tabs(["USD", "BRL"])

    with tab_usd:
        st.subheader("Commodities em USD")
        numeric_usd = [c for c in df_usd.columns if c != "Date"]
        series_usd = st.selectbox("Commodities (USD)", numeric_usd, key="usd_series")

        # especificação Vega-Lite para série única
        spec_usd = {
            "mark": {"type": "line", "color": "#06333B"},
            "encoding": {
                "x": {"field": "Date", "type": "temporal", "title": "Date", "axis": {"grid": True}},
                "y": {"field": series_usd, "type": "quantitative", "title": series_usd, "axis": {"grid": True}}
            },
            "selection": {"grid": {"type": "interval", "bind": "scales"}}
        }
        st.vega_lite_chart(df_usd, spec_usd, use_container_width=True)

        # Comparativo em índice (Dez/24 = 100)
        df_idx_u = df_usd.set_index("Date").resample("M").last()
        base_u = df_idx_u.loc["2024-12-31"]
        df_idx_u = df_idx_u.div(base_u) * 100
        df_idx_u = df_idx_u.reset_index()
        st.subheader("Comparativo USD (Dez/24 = 100)")
        all_u = [c for c in df_idx_u.columns if c != "Date"]
        chosen_u = st.multiselect("Quais séries? (USD)", all_u, default=all_u, key="idx_usd")
        df_long_u = df_idx_u.melt(id_vars="Date", var_name="Commodity", value_name="Índice")[lambda d: d.Commodity.isin(chosen_u)]
        spec_idx_u = {
            "mark": {"type": "line"},
            "encoding": {
                "x": {"field": "Date", "type": "temporal", "axis": {"grid": True}},
                "y": {"field": "Índice", "type": "quantitative", "axis": {"grid": True}},
                "color": {"field": "Commodity", "type": "nominal"}
            },
            "selection": {"grid": {"type": "interval", "bind": "scales"}}
        }
        st.vega_lite_chart(df_long_u, spec_idx_u, use_container_width=True)

    with tab_brl:
        st.subheader("Commodities em BRL")
        numeric_brl = [c for c in df_brl.columns if c != "Date"]
        series_brl = st.selectbox("Commodities (BRL)", numeric_brl, key="brl_series")

        # especificação Vega-Lite para série única
        spec_brl = {
            "mark": {"type": "line", "color": "#06333B"},
            "encoding": {
                "x": {"field": "Date", "type": "temporal", "title": "Date", "axis": {"grid": True}},
                "y": {"field": series_brl, "type": "quantitative", "title": series_brl, "axis": {"grid": True}}
            },
            "selection": {"grid": {"type": "interval", "bind": "scales"}}
        }
        st.vega_lite_chart(df_brl, spec_brl, use_container_width=True)

        # Comparativo em índice (Dez/24 = 100)
        df_idx_b = df_brl.set_index("Date").resample("M").last()
        base_b = df_idx_b.loc["2024-12-31"]
        df_idx_b = df_idx_b.div(base_b) * 100
        df_idx_b = df_idx_b.reset_index()
        st.subheader("Comparativo BRL (Dez/24 = 100)")
        all_b = [c for c in df_idx_b.columns if c != "Date"]
        chosen_b = st.multiselect("Quais séries? (BRL)", all_b, default=all_b, key="idx_brl")
        df_long_b = df_idx_b.melt(id_vars="Date", var_name="Commodity", value_name="Índice")[lambda d: d.Commodity.isin(chosen_b)]
        spec_idx_b = {
            "mark": {"type": "line"},
            "encoding": {
                "x": {"field": "Date", "type": "temporal", "axis": {"grid": True}},
                "y": {"field": "Índice", "type": "quantitative", "axis": {"grid": True}},
                "color": {"field": "Commodity", "type": "nominal"}
            },
            "selection": {"grid": {"type": "interval", "bind": "scales"}}
        }
        st.vega_lite_chart(df_long_b, spec_idx_b, use_container_width=True)
