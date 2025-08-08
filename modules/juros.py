# modules/juros.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
from bcb import currency, sgs
import bizdays
from myfuncs import get_contracts
from bizdays import Calendar
import datetime as dt
from pathlib import Path
from data_loaders import load_nominal
from data_loaders import load_real


CAL = Calendar.load("ANBIMA")
DATA_FILE = Path("data/di1_curves.parquet")
START_DATE = dt.date(2025, 1, 3)                    # first Friday of 2025


def make_curve(refdate: dt.date) -> pd.DataFrame:
    df = get_contracts(refdate)

    di1 = df.loc[(df["Mercadoria"] == "DI1") &
                 (df["PUAtual"] != 100_000)].copy()

    di1["Maturity"] = di1["Vencimento"].map(CAL.following)
    di1["DU"] = di1.apply(lambda x: CAL.bizdays(x["DataRef"], x["Maturity"]),
                          axis=1)
    di1["Rate"] = (100_000 / di1["PUAtual"]) ** (252 / di1["DU"]) - 1

    di1 = di1[["DataRef", "Maturity", "Rate"]].rename(
        columns={"DataRef": "RefDate"})
    di1["RefDate"] = pd.to_datetime(di1["RefDate"]).dt.date
    return di1


@st.cache_data(show_spinner=False)
def load_curves() -> pd.DataFrame:
    """Read existing file or create it from scratch (may take a minute)."""
    if DATA_FILE.exists():
        curves = pd.read_parquet(DATA_FILE)
    else:
        curves = pd.DataFrame(columns=["RefDate", "Maturity", "Rate"])

    # ---------------------------------------------------------------
    # Append any missing Fridays up to *today*
    # ---------------------------------------------------------------
    last_saved = curves["RefDate"].max() if not curves.empty else START_DATE - dt.timedelta(days=7)
    fridays = pd.date_range(last_saved + dt.timedelta(days=7),
                            dt.date.today(),
                            freq="W-FRI")

    new_parts = []
    for ref in fridays:
        try:
            new_parts.append(make_curve(ref.date()))
        except Exception:
            #st.warning(f"Curve {ref.date()} skipped: {e}")
            pass

    if new_parts:
        curves = pd.concat([curves, *new_parts]).reset_index(drop=True)
        DATA_FILE.parent.mkdir(exist_ok=True)
        curves.to_parquet(DATA_FILE, index=False)

    return curves
    

def juros_page():
    st.title("Juros")
    st.markdown("---")

    # Carrega dados de juros nominal e real
    df_nominal = load_nominal("Acompanhamento de Implícitas.xlsx")
    df_real = load_real("Acompanhamento de Implícitas.xlsx")

    # Padroniza coluna de data
    df_nominal = df_nominal.rename(columns={"Dates": "Date"})
    df_real = df_real.rename(columns={"Dates": "Date"})


    # Cria abas
    tab_nominal, tab_real = st.tabs(["Nominal", "Real"])

    with tab_nominal:


        curves = load_curves()
        all_dates = sorted(curves["RefDate"].unique())
        default_last = all_dates[-1:]                   # show latest curve by default

        chosen = st.multiselect("Select reference dates",
                                options=all_dates,
                                default=default_last,
                                format_func=lambda d: d.strftime("%d-%b-%Y"))

        if not chosen:
            st.info("Choose at least one date.")
            return

        # antes de usar .dt, converta explicitamente
        subset = curves[curves["RefDate"].isin(chosen)].copy()

        # 1) Converte para datetime, transformando valores inválidos em NaT
        subset["RefDate"] = pd.to_datetime(subset["RefDate"], errors="coerce")

        # 2) Confere se algum valor ficou NaT (caso haja linhas sem data)
        if subset["RefDate"].isna().any():
            subset = subset.dropna(subset=["RefDate"])   # ou trate como preferir

        # 3) Agora é seguro usar .dt
        subset["RatePct"] = subset["Rate"] * 100
        subset["RefStr"]  = subset["RefDate"].dt.strftime("%d-%b-%Y")
        chart = (
        alt.Chart(subset)
        .mark_line(point=True, strokeWidth=2)
        .encode(
            x=alt.X("Maturity:T", title="Maturity date"),
            y=alt.Y("RatePct:Q",  title="Rate (%)"),
            color=alt.Color(
                "RefStr:N",
                title="Reference",
                scale=alt.Scale(scheme="set1"),     # verm., azul, verde, laranja…
                legend=alt.Legend(labelOverlap=False)
            ),
            tooltip=[
                alt.Tooltip("RefStr:N",  title="Reference"),
                alt.Tooltip("Maturity:T", title="Maturity"),
                alt.Tooltip("RatePct:Q",  title="Rate (%)", format=".2f")
            ],
        )
        .properties(height=450)
        .interactive()
        )

        st.altair_chart(chart, use_container_width=True)   # 31-Jan-2025 …

        numeric_cols = [c for c in df_nominal.columns if c != "Date"]
        chosen = st.multiselect("Quais Prazos?", numeric_cols, default=numeric_cols)
        df_nominal_sel = df_nominal[["Date"] + chosen]
        df_nominal_long = df_nominal_sel.melt(id_vars="Date", var_name="Prazo", value_name="% a.a.")
        st.write("Pré-visualização:", df_nominal_long.head(), df_nominal_long.dtypes)
        st.write("Linhas:", len(df_nominal_long))

        spec = {
            "mark": {"type": "line", "color": "#06333B"},
            "encoding": {
                "x": {"field": "Date", "type": "temporal", "title": "Date",
                    "axis": {"grid": True, "gridColor": "#e0e0e0", "gridOpacity": 1}},
                "y": {"field": "% a\\.a.", "type": "quantitative", "title": '% a.a.',
                    "axis": {"grid": True, "gridColor": "#e0e0e0", "gridOpacity": 1}}
            },
            "selection": {"grid": {"type": "interval", "bind": "scales"}}
        }
        st.subheader(f"Juros Prefixados")
        st.vega_lite_chart(df_nominal_long, spec, use_container_width=True)

    with tab_real:
        st.subheader("Taxas de juros reais")

    


   