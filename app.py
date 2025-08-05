# app.py
import streamlit as st

from modules.home        import home_page
from modules.bolsas      import bolsas_page
from modules.cambio      import cambio_page
#from modules.juros       import juros_page
from modules.commodities import commodities_page

st.set_page_config(page_title="Relatório Dados de Mercado", page_icon="💹")

# (opcional) login logic aqui…

PAGES = {
    "Home":      home_page,
    #"Câmbio":    cambio_page,
    #"Juros":     juros_page,
    "Bolsas":    bolsas_page,
    #"Commodities": commodities_page,
}

choice = st.sidebar.radio("🔍 Navegar para:", list(PAGES.keys()))
PAGES[choice]()