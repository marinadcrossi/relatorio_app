#data_loaders.py


import pandas as pd
import streamlit as st


#@st.cache_data
def load_bolsas(path):
    df = pd.read_excel(path, sheet_name="bolsas", engine="openpyxl")
    df["Dates"] = pd.to_datetime(df["Dates"])
    return df

#@st.cache_data
def load_cambio(path):
    df = pd.read_excel(path, sheet_name='moedas', engine="openpyxl")
    df["Dates"] = pd.to_datetime(df["Dates"])
    return df

#@st.cache_data
def load_commodities_usd(path):
    df = pd.read_excel(path, sheet_name='commodities_usd', engine="openpyxl")
    df["Dates"] = pd.to_datetime(df["Dates"])
    return df

#@st.cache_data
def load_commodities_brl(path):
    df = pd.read_excel(path, sheet_name='commodities_brl', engine="openpyxl")
    df["Dates"] = pd.to_datetime(df["Dates"])
    return df

#@st.cache_data
def load_implicitas(path):
    df = pd.read_excel(path, sheet_name='implicitas', engine="openpyxl")
    df["Dates"] = pd.to_datetime(df["Dates"])
    return df

#@st.cache_data
def load_nominal(path):
    df = pd.read_excel(path, sheet_name='nominal', engine="openpyxl")
    df["Dates"] = pd.to_datetime(df["Dates"])
    return df

#@st.cache_data
def load_real(path):
    df = pd.read_excel(path, sheet_name='real', engine="openpyxl")
    df["Dates"] = pd.to_datetime(df["Dates"])
    return df
