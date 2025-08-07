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

    subset = curves[curves["RefDate"].isin(chosen)]
    subset["RatePct"] = subset["Rate"] * 100      # 0.1412 → 14.12

    chart = (
    alt.Chart(subset)
    .mark_line(point=True, strokeWidth=2)
    .encode(
        x=alt.X("Maturity:T", title="Maturity date"),
        y=alt.Y("RatePct:Q",  title="Rate (%)"),
        color=alt.Color(
            "RefDate:T",
            title="Reference",
            legend=alt.Legend(format="%d-%b-%Y"),
            scale=alt.Scale(scheme="tableau10")     # ← paleta vibrante
        ),
        tooltip=[
            alt.Tooltip("RefDate:T",  title="Reference", format="%d-%b-%Y"),
            alt.Tooltip("Maturity:T", title="Maturity"),
            alt.Tooltip("RatePct:Q",  title="Rate (%)", format=".2f")
        ],
    )
    .properties(height=450)
    .interactive()
)



    st.altair_chart(chart, use_container_width=True)