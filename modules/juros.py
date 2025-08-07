# modules/juros.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
    refdate=datetime.datetime(2025,5,2)
    #Puxar os contratos
    df=get_contracts(refdate)
    di1 = df[(df['Mercadoria'] == 'DI1') & (df['PUAtual'] != 100000.0)].copy()
    print(di1)

    #Criando a curva de juros
    MARKET_CALENDAR = cal
    di1['Maturity'] = di1['Vencimento'].map(MARKET_CALENDAR.following)
    di1['DU'] = di1.apply(lambda x: MARKET_CALENDAR.bizdays(x['DataRef'], x['Maturity']), axis=1)
    di1['Rate'] = (100000 / di1['PUAtual'])**(252 / di1['DU']) - 1
    di1_curve = di1[['DataRef', 'Maturity', 'DU', 'Rate']]

    di1_curve.plot(x='Maturity', y='Rate', figsize=(20,6), style='-o',
                ylabel='Rate', xlabel='Date', title='DI1 Curve - 2021-11-01')
    plt.show()