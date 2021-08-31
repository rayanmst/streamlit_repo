# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 15:01:19 2021

@author: rayan
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.write(""" 
	# Case Intelbras - Estágio área de dados
	### Rayan M. Steinbach
""")


df = pd.read_csv('arquivo-desafio.csv', sep = ';')

df['NOME_FUNCIONARIO'] = df['NOME_FUNCIONARIO'].str.capitalize()
df['CARGO'] = df['CARGO'].str.capitalize()
df['NOME_SITUAÇÃO'] = df['NOME_FUNCIONARIO'] + ' - ' + df['SITUAÇÃO']
df['DATA_DESLIGAMENTO'] = df['DATA_DESLIGAMENTO'].fillna('Atualmente')

st.write("## **Lista de funcionários**")
expander = st.expander("Clique para visualizar a lista de funcionários. ")
with expander:
    st.dataframe(df)

## Número de cargos existentes

st.write("## **Número de funcionários por cargo**")
cargos = st.expander("Existem " + str(df['ID_CARGO'].nunique())+ " cargos distintos no documento. Clique para detalhes: ")
with cargos:
    st.dataframe(df['CARGO'].value_counts())

## Cargas horárias
journey = df.JORNADA.value_counts()
journey = journey/len(df.index)
explode = [0.1,0,0,0,0,0.8]


st.write("## **Cargas horárias**")

fig1,ax1=plt.subplots(figsize=(8,8))
ax1.pie(journey.values,explode = explode, autopct='%1.1f%%',radius=3, pctdistance=1.08)
ax1.legend(journey.index, loc="lower right",bbox_to_anchor=(1.2,0))
ax1.set_title('Porcentagem de trabalhadores por carga horária',fontweight='bold', size = 18)
ax1.axis('equal')
ploted = st.expander('Existem {:.2%} trabalhadores com carga horária de 40 horas.'.format(journey[0]))
with ploted:
    st.pyplot(fig1)

## Encontrando a pessoa que tem data de admissão 15/06/2012 e data de desligamento 04/12/2012
st.write('## **Funcionários com data de admissão 15/06/2012 e data de desligamento 04/12/2012**')
desligados = st.expander("Clique para ver os funcionários que cumprem os requisitos.")
with desligados:
    for _,line in df.iterrows():
        if line['DATA_ADMISSAO'] == '2012-06-15' and line['DATA_DESLIGAMENTO'] == '2012-12-04':
            st.text('Funcionário(a):' + line['NOME_FUNCIONARIO'] + '\nData de admissão: 15/06/2012\nData de desligamento: 04/12/2012\n')
        

## Removendo funcionários com categoria não preenchida
df.dropna(subset = ["CATEGORIA"], inplace=True)


## Funcionários que podem se aposentar por tempo de serviço
mask = df['SITUAÇÃO'] == 'Ativo'
ativos = df[mask]
st.write("## **Funcionários ativos**")
actives = st.expander("Clique para visualizar a lista de funcionários ativos.")
with actives: 
    st.dataframe(ativos)


## Encontrando funcionários com possibilidade de se aposentar
from datetime import date
today = date.today()

st.write("## **Funcionários com mais de 30 anos de serviço:**")
aptos = pd.DataFrame({'NOME_FUNCIONARIO':[],'ANOS_TRABALHO':[]})

for _,line in ativos.iterrows():
    admissao = date.fromisoformat(line['DATA_ADMISSAO'])
    tempo = round((today-admissao).days/365)
    if tempo >= 30:
        aptos.loc[aptos.shape[0]] = [line['NOME_FUNCIONARIO'],str(tempo)]

aposentarao = st.expander("Clique para visualizar a lista de funcionários aptos a se aposentar.")
with aposentarao:
    st.dataframe(aptos)