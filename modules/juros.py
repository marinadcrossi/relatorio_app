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
import datetime



def juros_page():
    st.title("Juros")
    st.markdown("---")
    st.write("Página em desenvolvimento..")

    cal=Calendar.load('ANBIMA')

    #Colocar aqui a data de referência para puxar a curva
    refdate = datetime.datetime(2025, 5, 2)
    df = get_contracts(refdate)

    di1 = df.loc[(df["Mercadoria"] == "DI1") & (df["PUAtual"] != 100_000)].copy()
    di1["Maturity"] = di1["Vencimento"].map(cal.following)
    di1["DU"] = di1.apply(lambda x: cal.bizdays(x["DataRef"], x["Maturity"]), axis=1)
    di1["Rate"] = (100_000 / di1["PUAtual"]) ** (252 / di1["DU"]) - 1
    curve = di1[["Maturity", "Rate"]].sort_values("Maturity")

    # ------------------------------------------------------------------
    # 2. Altair chart with interactive scales
    # ------------------------------------------------------------------
    spec = (
        alt.Chart(curve)
        .mark_line(point=True, color="#06333B")
        .encode(
            x=alt.X("Maturity:T", title="Maturity date"),
            y=alt.Y("Rate:Q", title="Rate"),
        )
        .properties(height=400)
        .interactive(bind_y=False)  # pan/zoom on x; keep y fixed (or omit for both)
    )

    st.altair_chart(spec, use_container_width=True)

    st.caption("Pan / scroll to zoom; double-click to reset.")