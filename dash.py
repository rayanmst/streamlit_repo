# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 15:01:19 2021

@author: rayan
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import string

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
    
st.write("## Funcionários com Silva e com Ana nos nomes")
silvas = 0
silvasdf = pd.DataFrame(columns=df.columns)
anas = 0
anasdf = pd.DataFrame(columns=df.columns)
for _,line in df.iterrows():
    nome_sep = line['NOME_FUNCIONARIO'].split(" ")
    if string.capwords(nome_sep[0]) == 'Ana':
        anasdf.loc[anasdf.shape[0]]=(line)
        anas = anas + 1
    for name in nome_sep[1:]:
        if string.capwords(name) == 'Silva':
            silvasdf.loc[silvasdf.shape[0]]=(line)
            silvas = silvas + 1
st.write("Existem", len(silvasdf.index), "funcionários com o sobrenome Silva do total de", len(df.index) ,"funcionários")
lista_silva = st.expander("Clique para ver a lista com os funcionários de sobrenome Silva")
with lista_silva:
    st.dataframe(silvasdf)
st.write("Existem", len(anasdf.index), "funcionárias com o nome Ana do total de", len(df.index) ,"funcionários")
lista_ana = st.expander("Clique para ver a lista com as funcionárias de nome Ana")
with lista_ana:
    st.dataframe(anasdf)
## Número de cargos existentes

st.write("## **Número de funcionários por cargo**")
funcPcargos = df['CARGO'].value_counts()
funcdf = pd.DataFrame({'CARGO':funcPcargos.index, 'NUMERO_FUNCIONARIOS':funcPcargos.values})
cargos = st.expander("Existem " + str(df['ID_CARGO'].nunique())+ " cargos distintos no documento. Clique para detalhes: ")
with cargos:
    st.dataframe(funcdf)

## Cargas horárias
journey = df.JORNADA.value_counts()
journey_pct = journey/len(df.index)
journeydf = pd.DataFrame({'JORNADA':journey.index,'TOTAL_FUNCIONARIOS':journey.values,'%_FUNCIONARIOS':journey_pct.values*100})
explode = [0.1,0,0,0,0,0.8]


st.write("## **Cargas horárias**")
    
fig1,ax1=plt.subplots(figsize=(8,8))
ax1.pie(journey_pct.values,explode = explode, autopct='%1.2f%%',shadow=True, radius=3, pctdistance=1.08)
ax1.legend(journey.index, loc="lower right",bbox_to_anchor=(1.2,0))
ax1.set_title('Porcentagem de trabalhadores por carga horária',fontweight='bold', size = 18)
ax1.axis('equal')
ploted = st.expander('Existem {:.2%} trabalhadores com carga horária de 40 horas.'.format(journey_pct[0]))
with ploted:
    st.pyplot(fig1)
    
jornadas = st.expander('Clique aqui para mais detalhes sobre as jornadas de trabalho')
with jornadas:
    st.dataframe(journeydf)

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