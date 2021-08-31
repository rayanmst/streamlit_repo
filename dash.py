# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 15:01:19 2021

@author: rayan
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('arquivo-desafio.csv', sep = ';')

df['NOME_FUNCIONARIO'] = df['NOME_FUNCIONARIO'].str.capitalize()
df['CARGO'] = df['CARGO'].str.capitalize()
df['NOME_SITUAÇÃO'] = df['NOME_FUNCIONARIO'] + ' - ' + df['SITUAÇÃO']
df['DATA_DESLIGAMENTO'] = df['DATA_DESLIGAMENTO'].fillna('Atualmente')

st.title("Lista de funcionários")

st.dataframe(df)

## Número de cargos existentes

st.title("Número de funcionários por cargo")
st.text("Existem " + str(df['ID_CARGO'].nunique())+ " cargos distintos no documento")

st.dataframe(df['CARGO'].value_counts())

## Cargas horárias
journey = df.JORNADA.value_counts()
journey = journey/len(df.index)
explode = [0.1,0,0,0,0,0.8]


st.title("Cargas horárias")
st.text('Existem {:.2%} trabalhadores com carga horária de 40 horas.'.format(journey[0]))

fig1,ax1=plt.subplots(figsize=(8,8))
ax1.pie(journey.values,explode = explode, autopct='%1.1f%%',radius=3, pctdistance=1.08)
ax1.legend(journey.index, loc="lower right",bbox_to_anchor=(1.2,0))
ax1.set_title('Porcentagem de trabalhadores por carga horária',fontweight='bold', size = 18)
ax1.axis('equal')
st.pyplot(fig1)

## Encontrando a pessoa que tem data de admissão 15/06/2012 e data de desligamento 04/12/2012
st.title('Funcionários com data de admissão 15/06/2012 e data de desligamento 04/12/2012')
for _,line in df.iterrows():
    if line['DATA_ADMISSAO'] == '2012-06-15' and line['DATA_DESLIGAMENTO'] == '2012-12-04':
        st.text('Funcionário(a):' + line['NOME_FUNCIONARIO'] + '\nData de admissão: 15/06/2012\nData de desligamento: 04/12/2012\n')
        #print('Funcionário(a):', line['NOME_FUNCIONARIO'], '\nData de admissão: 15/06/2012\nData de desligamento: 04/12/2012\n')
        

## Removendo funcionários com categoria não preenchida
df.dropna(subset = ["CATEGORIA"], inplace=True)


## Funcionários que podem se aposentar por tempo de serviço
mask = df['SITUAÇÃO'] == 'Ativo'
ativos = df[mask]
st.title("Funcionários ativos\n")
st.dataframe(ativos)


## Encontrando funcionários com possibilidade de se aposentar
from datetime import date
today = date.today()

st.title("Funcionários com mais de 30 anos de serviço:")
aptos = pd.DataFrame({'NOME_FUNCIONARIO':[],'ANOS_TRABALHO':[]})

for _,line in ativos.iterrows():
    admissao = date.fromisoformat(line['DATA_ADMISSAO'])
    tempo = round((today-admissao).days/365)
    if tempo >= 30:
        aptos.loc[aptos.shape[0]] = [line['NOME_FUNCIONARIO'],str(tempo)]
    
st.dataframe(aptos)
## Exportando para csv o dataframe tratado
df.to_csv('desafio-tratado-Rayan.csv', sep=';', index = False)