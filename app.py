# app.py
import streamlit as st
from streamlit_option_menu import option_menu

# import your page-functions
from modules.home        import home_page
from modules.bolsas      import bolsas_page
from modules.cambio      import cambio_page
from modules.juros       import juros_page
from modules.commodities import commodities_page
from modules.implicitas  import implicitas_page


st.set_page_config(page_title="Relatório Dados de Mercado", page_icon="💹")

# --- SIDEBAR MENU ---
with st.sidebar:
    st.markdown("## Menu de Navegação")
    st.markdown("---")
    choice = option_menu(
        menu_title=None,
        options=[
            "Home",
            "Bolsas",
            "Câmbio",
            "Juros",
            "Commodities",
            "Inflação Implícita"
        ],
        icons=[
            "house",
            "graph-up",
            "currency-exchange",
            "percent",
            "bar-chart",
            "house"
        ],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important"},
            "icon":     {"font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "padding":     "8px 10px"
            },
            "nav-link-selected": {
                "background-color": "#06333B",
                "color":            "white"
            },
        }
    )

# --- PAGE DISPATCH ---
if choice == "Home":
    home_page()
elif choice == "Bolsas":
    bolsas_page()
elif choice == "Câmbio":
    cambio_page()
elif choice == "Juros":
    juros_page()
elif choice == "Commodities":
    commodities_page()
elif choice == "Inflação Implícita":
    implicitas_page()