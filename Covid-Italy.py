"""
Dashboard for data exploration about the Covid-19 epidemic in Italy
Author: Marco Lardera (larderamarco@hotmail.com)
"""

import datetime
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

plt.rcParams ["figure.figsize"]=[16,8]
sns.set_style ("darkgrid")

source_naz="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"
source_reg="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv"

df_naz=pd.read_csv (source_naz, sep=",")
df_reg=pd.read_csv (source_reg, sep=",")

#Cleaning operations
df_naz.drop (["stato","note_it","note_en"], axis=1, inplace=True)
df_reg.drop (["stato","codice_regione","lat","long","note_it","note_en"], axis=1, inplace=True)
df_reg.sort_values (["denominazione_regione","data"], inplace=True)
df_reg.reset_index (drop=True, inplace=True)
df_naz ["crescita"]=df_naz ["totale_casi"]/df_naz ["totale_casi"].shift (1)
df_reg ["crescita"]=df_reg ["totale_casi"]/df_reg ["totale_casi"].shift (1)
df_naz.replace (np.nan, 0, inplace=True)
df_reg.replace ([np.nan,np.inf], 0, inplace=True)

#Workaround for hiding the Streamlit menu
hide_menu_style = "<style>#MainMenu {visibility: hidden;}</style>"
st.markdown (hide_menu_style, unsafe_allow_html=True)

#*** SIDEBAR START ***

st.sidebar.title ("Overview nazionale")
st.sidebar.text ("")

totale_casi=df_naz.iloc[-1]["totale_casi"]
tamponi=df_naz.iloc[-1]["tamponi"]
totale_positivi=df_naz.iloc[-1]["totale_positivi"]
deceduti=df_naz.iloc[-1]["deceduti"]
dimessi_guariti=df_naz.iloc[-1]["dimessi_guariti"]
nuovi_positivi=df_naz.iloc[-1]["nuovi_positivi"]
crescita=(df_naz.iloc[-1]["crescita"]*100)-100

st.sidebar.markdown (f"**Casi totali:** {totale_casi}")
st.sidebar.markdown (f"**Tamponi:** {tamponi}")
st.sidebar.markdown (f"**Totale positivi:** {totale_positivi}")
st.sidebar.markdown (f"**Deceduti:** {deceduti}")
st.sidebar.markdown (f"**Guariti:** {dimessi_guariti}")

st.sidebar.text ("")
st.sidebar.markdown (f"Oggi **{nuovi_positivi}** nuovi casi (**+{crescita.round(2)}%**)")

#*** SIDEBAR END ***

image=Image.open ("covid19.jpg")
st.image (image, use_column_width=True)

st.title ("COVID-19 - Dati italiani")

data=df_naz.iloc[-1]["data"].replace ("T", " ")
data_format=datetime.datetime.strptime (data, "%Y-%m-%d %H:%M:%S").strftime ("%d/%m/%Y ore %H:%M:%S")
st.markdown (f"*Ultimo aggiornamento: {data_format}*")

if st.checkbox ("Mostra i dataset completi"):
	st.subheader (f"Dataset nazionale ([Fonte]({source_naz}))")
	st.dataframe (df_naz)
	st.subheader (f"Dataset suddiviso per regioni ([Fonte]({source_reg}))")
	st.dataframe (df_reg)

options=["Italia",
"Abruzzo",
"Basilicata",
"P.A. Bolzano",
"Calabria",
"Campania",
"Emilia-Romagna",
"Friuli Venezia Giulia",
"Lazio",
"Liguria",
"Lombardia",
"Marche",
"Molise",
"Piemonte",
"Puglia",
"Sardegna",
"Sicilia",
"Toscana",
"P.A. Trento",
"Umbria",
"Valle d'Aosta",
"Veneto"]

select=st.selectbox ("Regione", options)

#*** REGION OVERVIEW START***

if select != "Italia":

	totale_casi_reg=df_reg [df_reg["denominazione_regione"]==select]["totale_casi"].iloc[-1]
	tamponi_reg=df_reg [df_reg["denominazione_regione"]==select]["tamponi"].iloc[-1]
	totale_positivi_reg=df_reg [df_reg["denominazione_regione"]==select]["totale_positivi"].iloc[-1]
	deceduti_reg=df_reg [df_reg["denominazione_regione"]==select]["deceduti"].iloc[-1]
	dimessi_guariti_reg=df_reg [df_reg["denominazione_regione"]==select]["dimessi_guariti"].iloc[-1]
	
	st.header (f"Overview {select}")
	st.info (f"""
		**Casi totali:** {totale_casi_reg}
		\n\n**Tamponi:** {tamponi_reg}
		\n\n**Totale positivi:** {totale_positivi_reg}
		\n\n**Deceduti:** {deceduti_reg}
		\n\n**Guariti:** {dimessi_guariti_reg}""")

#*** REGION OVERVIEW END***

st.header ("Casi totali")

if select=="Italia":
	sns.lineplot (x=df_naz.index, y="totale_casi", marker="o", data=df_naz)
	plt.xticks(df_naz.index)
	plt.yticks (fontsize=20)
	plt.title ("Andamento casi totali nazionali", fontsize=20)
	plt.xlabel ("Giorni", fontsize=20)
	plt.ylabel ("Casi", fontsize=20)
	st.pyplot ()
else:
	sns.lineplot (x=df_naz.index, y="totale_casi", marker="o", data=df_reg[df_reg["denominazione_regione"]==select])
	plt.xticks(df_naz.index)
	plt.yticks (fontsize=20)
	plt.title (f"Andamento casi totali {select}", fontsize=20)
	plt.xlabel ("Giorni", fontsize=20)
	plt.ylabel ("Casi", fontsize=20)
	st.pyplot ()

st.header ("Tamponi effettuati")

if select=="Italia":
	sns.lineplot (x=df_naz.index, y="tamponi", marker="o", data=df_naz)
	plt.xticks(df_naz.index)
	plt.yticks (fontsize=20)
	plt.title ("Andamento nazionale tamponi effettuati", fontsize=20)
	plt.xlabel ("Giorni", fontsize=20)
	plt.ylabel ("Tamponi", fontsize=20)
	st.pyplot ()
else:
	sns.lineplot (x=df_naz.index, y="tamponi", marker="o", data=df_reg[df_reg["denominazione_regione"]==select])
	plt.xticks(df_naz.index)
	plt.yticks (fontsize=20)
	plt.title (f"Andamento tamponi effettuati {select}", fontsize=20)
	plt.xlabel ("Giorni", fontsize=20)
	plt.ylabel ("Tamponi", fontsize=20)
	st.pyplot ()

st.header ("Nuovi casi giornalieri")

if select=="Italia":
	sns.lineplot (x=df_naz.index, y="nuovi_positivi", marker="o", data=df_naz)
	plt.xticks(df_naz.index)
	plt.yticks (fontsize=20)
	plt.title ("Andamento nazionale nuovi casi giornalieri", fontsize=20)
	plt.xlabel ("Giorni", fontsize=20)
	plt.ylabel ("Nuovi casi", fontsize=20)
	st.pyplot ()
else:
	sns.lineplot (x=df_naz.index, y="nuovi_positivi", marker="o", data=df_reg[df_reg["denominazione_regione"]==select])
	plt.xticks(df_naz.index)
	plt.yticks (fontsize=20)
	plt.title (f"Andamento nuovi casi giornalieri {select}", fontsize=20)
	plt.xlabel ("Giorni", fontsize=20)
	plt.ylabel ("Nuovi casi", fontsize=20)
	st.pyplot ()

st.header ("Coefficiente di crescita")

if select=="Italia":
	sns.lineplot (x=df_naz[1:].index, y="crescita", marker="o", data=df_naz[1:])
	plt.xticks(df_naz.index)
	plt.yticks (fontsize=20)
	plt.title ("Andamento nazionale coefficiente di crescita", fontsize=20)
	plt.xlabel ("Giorni", fontsize=20)
	plt.ylabel ("Coefficiente di crescita", fontsize=20)
	st.pyplot ()
else:
	sns.lineplot (x=df_naz[1:].index, y="crescita", marker="o", data=df_reg[df_reg["denominazione_regione"]==select][1:])
	plt.xticks(df_naz.index)
	plt.yticks (fontsize=20)
	plt.title (f"Andamento coefficiente di crescita {select}", fontsize=20)
	plt.xlabel ("Giorni", fontsize=20)
	plt.ylabel ("Coefficiente di crescita", fontsize=20)
	st.pyplot ()

st.header ("Casi positivi")

if select=="Italia":
	sns.lineplot (x=df_naz.index, y="totale_positivi", marker="o", data=df_naz)
	plt.xticks(df_naz.index)
	plt.yticks (fontsize=20)
	plt.title ("Andamento nazionale casi positivi", fontsize=20)
	plt.xlabel ("Giorni", fontsize=20)
	plt.ylabel ("Casi positivi", fontsize=20)
	st.pyplot ()
else:
	sns.lineplot (x=df_naz.index, y="totale_positivi", marker="o", data=df_reg[df_reg["denominazione_regione"]==select])
	plt.xticks(df_naz.index)
	plt.yticks (fontsize=20)
	plt.title (f"Andamento casi positivi {select}", fontsize=20)
	plt.xlabel ("Giorni", fontsize=20)
	plt.ylabel ("Casi positivi", fontsize=20)
	st.pyplot ()

st.info ("Nota: i *casi positivi* sono calcolati sottraendo deceduti e guariti dai casi totali")

st.header ("Decessi")

if select=="Italia":
	sns.lineplot (x=df_naz.index, y="deceduti", marker="o", data=df_naz)
	plt.xticks(df_naz.index)
	plt.yticks (fontsize=20)
	plt.title ("Andamento nazionale decessi", fontsize=20)
	plt.xlabel ("Giorni", fontsize=20)
	plt.ylabel ("Decessi", fontsize=20)
	st.pyplot ()
else:
	sns.lineplot (x=df_naz.index, y="deceduti", marker="o", data=df_reg[df_reg["denominazione_regione"]==select])
	plt.xticks(df_naz.index)
	plt.yticks (fontsize=20)
	plt.title (f"Andamento decessi {select}", fontsize=20)
	plt.xlabel ("Giorni", fontsize=20)
	plt.ylabel ("Decessi", fontsize=20)
	st.pyplot ()

st.header ("Guarigioni")

if select=="Italia":
	sns.lineplot (x=df_naz.index, y="dimessi_guariti", marker="o", data=df_naz)
	plt.xticks(df_naz.index)
	plt.yticks (fontsize=20)
	plt.title ("Andamento nazionale guarigioni", fontsize=20)
	plt.xlabel ("Giorni", fontsize=20)
	plt.ylabel ("Guariti", fontsize=20)
	st.pyplot ()
else:
	sns.lineplot (x=df_naz.index, y="dimessi_guariti", marker="o", data=df_reg[df_reg["denominazione_regione"]==select])
	plt.xticks(df_naz.index)
	plt.yticks (fontsize=20)
	plt.title (f"Andamento guarigioni {select}", fontsize=20)
	plt.xlabel ("Giorni", fontsize=20)
	plt.ylabel ("Guariti", fontsize=20)
	st.pyplot ()

st.header ("Suddivisione casi positivi")

if select=="Italia":
	isolamento=df_naz.iloc[-1]["isolamento_domiciliare"]
	ricoverati=df_naz.iloc[-1]["ricoverati_con_sintomi"]
	terapia_intensiva=df_naz.iloc[-1]["terapia_intensiva"]
	x=["Isolamento domiciliare", "Ricoverati generici", "Terapia intensiva"]
	y=[isolamento, ricoverati, terapia_intensiva]
	sns.barplot(x=x, y=y)
	plt.xticks (fontsize=20)
	plt.yticks (fontsize=20)
	plt.title ("Suddivisione nazionale casi positivi", fontsize=20)
	st.pyplot ()
else:
	isolamento=df_reg[df_reg["denominazione_regione"]==select].iloc[-1]["isolamento_domiciliare"]
	ricoverati=df_reg[df_reg["denominazione_regione"]==select].iloc[-1]["ricoverati_con_sintomi"]
	terapia_intensiva=df_reg[df_reg["denominazione_regione"]==select].iloc[-1]["terapia_intensiva"]
	x=["Isolamento domiciliare", "Ricoverati generici", "Terapia intensiva"]
	y=[isolamento, ricoverati, terapia_intensiva]
	sns.barplot(x=x, y=y)
	plt.xticks (fontsize=20)
	plt.yticks (fontsize=20)
	plt.title (f"Suddivisione casi positivi {select}", fontsize=20)
	st.pyplot ()

st.header ("Fonti")

st.markdown ("Tutti i dati sono estratti in tempo reale dal repository ufficiale della Protezione Civile **[[LINK](https://github.com/pcm-dpc/COVID-19)]**")

st.header ("Contatti")

st.markdown ("Marco Lardera - [larderamarco@hotmail.com](mailto:larderamarco@hotmail.com)")
st.markdown ("[Github Repository](https://github.com/marcolardera/covid-italy)")