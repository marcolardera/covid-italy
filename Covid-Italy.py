"""
Dashboard for data exploration about the Covid-19 epidemic in Italy
Author: Marco Lardera (larderamarco@hotmail.com)
"""

import datetime
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from PIL import Image

source_naz="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"
source_reg="https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv"

df_naz=pd.read_csv (source_naz, sep=",")
df_reg=pd.read_csv (source_reg, sep=",")
df_reg_ranking=df_reg [-21:].set_index ("denominazione_regione").sort_values ("totale_casi", ascending=False)

#Cleaning operations
df_naz.drop (["stato","note"], axis=1, inplace=True)
df_reg.drop (["stato","codice_regione","note"], axis=1, inplace=True)
df_reg.sort_values (["denominazione_regione","data"], inplace=True)
df_reg.reset_index (drop=True, inplace=True)
df_naz ["crescita"]=df_naz ["totale_casi"]/df_naz ["totale_casi"].shift (1)
df_reg ["crescita"]=df_reg ["totale_casi"]/df_reg ["totale_casi"].shift (1)
df_naz ["casi_per_tamponi"]=df_naz ["totale_casi"]/df_naz ["tamponi"]
df_reg ["casi_per_tamponi"]=df_reg ["totale_casi"]/df_reg ["tamponi"]
df_naz.replace (np.nan, 0, inplace=True)
df_reg.replace ([np.nan,np.inf], 0, inplace=True)
df_reg_ranking.rename (columns={"totale_casi":"Casi"}, inplace=True)

#Workaround for hiding unwanted Streamlit elements
hide_style="""<style>#MainMenu {visibility: hidden;}
			  div.block-container:nth-child(2) > div:nth-child(1) > div:nth-child(12) > div:nth-child(1) > button:nth-child(1) {display: none;}
			  </style>"""
st.markdown (hide_style, unsafe_allow_html=True)

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
variazione_positivi=df_naz.iloc[-1]["variazione_totale_positivi"]

if variazione_positivi > 0 :
	variazione_positivi=f"+{variazione_positivi}"

st.sidebar.markdown (f"**Casi totali:** {totale_casi}")
st.sidebar.markdown (f"**Tamponi:** {tamponi}")
st.sidebar.markdown (f"**Totale positivi:** {totale_positivi}")
st.sidebar.markdown (f"**Deceduti:** {deceduti}")
st.sidebar.markdown (f"**Guariti:** {dimessi_guariti}")

st.sidebar.text ("")
st.sidebar.markdown ("Oggi:")
st.sidebar.markdown (f"- **{nuovi_positivi}** nuovi casi totali (**+{crescita.round(2)}%**)")
st.sidebar.markdown (f"- **{variazione_positivi}** pazienti attualmente positivi")

st.sidebar.table (df_reg_ranking["Casi"])

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

#*** SCATTER MAP START***

st.header ("Mappa casi positivi")

map_config={"scrollZoom": False, "displayModeBar": False}
reg_map=px.scatter_geo (df_reg_ranking, lat="lat", lon="long", size="totale_positivi", 
	center={"lat": 41.9145, "lon": 12.3343},
	labels={"totale_positivi": "Casi positivi"},
	hover_data={"lat": False, "long": False},
	hover_name=df_reg_ranking.index,
	scope="europe",
	height=700,
	size_max=100,
	title="Casi attualmente positivi per regione")
reg_map.update_geos (fitbounds="locations", resolution=50)
st.plotly_chart (reg_map, use_container_width=True, config=map_config)

#*** SCATTER MAP END***

st.markdown ("---") 

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

	figure=px.line (df_naz, x="data", y="totale_casi", title="Andamento casi totali nazionali",
				labels={
				"data": "Data",
				"totale_casi": "Casi"
				})
	st.plotly_chart (figure, use_container_width=True)

else:

	figure=px.line (df_reg[df_reg["denominazione_regione"]==select], x="data", y="totale_casi", title=f"Andamento casi totali {select}",
				labels={
				"data": "Data",
				"totale_casi": "Casi"
				})
	st.plotly_chart (figure, use_container_width=True)

st.header ("Tamponi effettuati")

if select=="Italia":

	figure=px.line (df_naz, x="data", y="tamponi", title="Andamento nazionale tamponi effettuati",
				labels={
				"data": "Data",
				"tamponi": "Tamponi"
				})
	st.plotly_chart (figure, use_container_width=True)

else:

	figure=px.line (df_reg[df_reg["denominazione_regione"]==select], x="data", y="tamponi", title=f"Andamento tamponi effettuati {select}",
				labels={
				"data": "Data",
				"tamponi": "Tamponi"
				})
	st.plotly_chart (figure, use_container_width=True)

st.header ("Casi per tamponi")

if select=="Italia":

	figure=px.line (df_naz, x="data", y="casi_per_tamponi", title="Andamento nazionale casi per tamponi",
				labels={
				"data": "Data",
				"casi_per_tamponi": "Casi per tamponi"
				})
	st.plotly_chart (figure, use_container_width=True)

else:

	figure=px.line (df_reg[df_reg["denominazione_regione"]==select], x="data", y="casi_per_tamponi", title=f"Andamento casi per tamponi {select}",
				labels={
				"data": "Data",
				"casi_per_tamponi": "Casi per tamponi"
				})
	st.plotly_chart (figure, use_container_width=True)

st.header ("Nuovi casi giornalieri")

if select=="Italia":

	figure=px.line (df_naz, x="data", y="nuovi_positivi", title="Andamento nazionale nuovi casi giornalieri",
				labels={
				"data": "Data",
				"nuovi_positivi": "Nuovi casi"
				})
	st.plotly_chart (figure, use_container_width=True)

else:

	figure=px.line (df_reg[df_reg["denominazione_regione"]==select], x="data", y="nuovi_positivi", title=f"Andamento nuovi casi giornalieri {select}",
				labels={
				"data": "Data",
				"nuovi_positivi": "Nuovi casi"
				})
	st.plotly_chart (figure, use_container_width=True)

st.header ("Coefficiente di crescita")

if select=="Italia":

	figure=px.line (df_naz, x="data", y="crescita", title="Andamento nazionale coefficiente di crescita",
				labels={
				"data": "Data",
				"crescita": "Coefficiente di crescita"
				})
	st.plotly_chart (figure, use_container_width=True)

else:

	figure=px.line (df_reg[df_reg["denominazione_regione"]==select], x="data", y="crescita", title=f"Andamento coefficiente di crescita {select}",
				labels={
				"data": "Data",
				"crescita": "Coefficiente di crescita"
				})
	st.plotly_chart (figure, use_container_width=True)

st.header ("Casi positivi")

if select=="Italia":

	figure=px.line (df_naz, x="data", y="totale_positivi", title="Andamento nazionale casi positivi",
				labels={
				"data": "Data",
				"totale_positivi": "Casi positivi"
				})
	st.plotly_chart (figure, use_container_width=True)

else:

	figure=px.line (df_reg[df_reg["denominazione_regione"]==select], x="data", y="totale_positivi", title=f"Andamento casi positivi {select}",
				labels={
				"data": "Data",
				"totale_positivi": "Casi positivi"
				})
	st.plotly_chart (figure, use_container_width=True)

st.info ("Nota: i *casi positivi* sono calcolati sottraendo deceduti e guariti dai casi totali")

st.header ("Decessi")

if select=="Italia":

	figure=px.line (df_naz, x="data", y="deceduti", title="Andamento nazionale decessi",
				labels={
				"data": "Data",
				"deceduti": "Decessi"
				})
	st.plotly_chart (figure, use_container_width=True)

else:

	figure=px.line (df_reg[df_reg["denominazione_regione"]==select], x="data", y="deceduti", title=f"Andamento decessi {select}",
				labels={
				"data": "Data",
				"deceduti": "Decessi"
				})
	st.plotly_chart (figure, use_container_width=True)

st.header ("Guarigioni")

if select=="Italia":

	figure=px.line (df_naz, x="data", y="dimessi_guariti", title="Andamento nazionale guarigioni",
				labels={
				"data": "Data",
				"dimessi_guariti": "Guariti"
				})
	st.plotly_chart (figure, use_container_width=True)

else:

	figure=px.line (df_reg[df_reg["denominazione_regione"]==select], x="data", y="dimessi_guariti", title=f"Andamento guarigioni {select}",
				labels={
				"data": "Data",
				"dimessi_guariti": "Guariti"
				})
	st.plotly_chart (figure, use_container_width=True)

st.header ("Suddivisione casi positivi")

if select=="Italia":

	isolamento=df_naz.iloc[-1]["isolamento_domiciliare"]
	ricoverati=df_naz.iloc[-1]["ricoverati_con_sintomi"]
	terapia_intensiva=df_naz.iloc[-1]["terapia_intensiva"]
	x=["Isolamento domiciliare", "Ricoverati generici", "Terapia intensiva"]
	y=[isolamento, ricoverati, terapia_intensiva]
	df_bar=pd.DataFrame ({"x":x, "y":y})

	figure=px.bar (df_bar, x="x", y="y", labels={"x": "Tipologia", "y": "Numerosità"}, text="y", title="Suddivisione nazionale casi positivi")
	st.plotly_chart (figure, use_container_width=True)

else:

	isolamento=df_reg[df_reg["denominazione_regione"]==select].iloc[-1]["isolamento_domiciliare"]
	ricoverati=df_reg[df_reg["denominazione_regione"]==select].iloc[-1]["ricoverati_con_sintomi"]
	terapia_intensiva=df_reg[df_reg["denominazione_regione"]==select].iloc[-1]["terapia_intensiva"]
	x=["Isolamento domiciliare", "Ricoverati generici", "Terapia intensiva"]
	y=[isolamento, ricoverati, terapia_intensiva]
	df_bar=pd.DataFrame ({"x":x, "y":y})

	figure=px.bar (df_bar, x="x", y="y", labels={"x": "Tipologia", "y": "Numerosità"}, text="y", title=f"Suddivisione casi positivi {select}")
	st.plotly_chart (figure, use_container_width=True)

st.markdown ("---")

st.header ("Fonti")

st.markdown ("Tutti i dati sono estratti in tempo reale dal repository ufficiale della Protezione Civile **[[LINK](https://github.com/pcm-dpc/COVID-19)]**")

st.header ("Contatti")

st.markdown ("Marco Lardera - [larderamarco@hotmail.com](mailto:larderamarco@hotmail.com)")
st.markdown ("[Github Repository](https://github.com/marcolardera/covid-italy)")