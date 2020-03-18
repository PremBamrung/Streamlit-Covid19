import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px 
import streamlit as st


@st.cache
def load_data():
    url_confirmed="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
    url_dead='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
    url_recovered='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'

    confirmed=pd.read_csv(url_confirmed)
    dead=pd.read_csv(url_dead)
    recovered=pd.read_csv(url_recovered)

    df=confirmed.melt(['Province/State',"Country/Region","Lat","Long"],var_name="Date",value_name="Confirmed")
    df1=dead.melt(['Province/State',"Country/Region","Lat","Long"],var_name="Date",value_name="Dead")
    df2=recovered.melt(['Province/State',"Country/Region","Lat","Long"],var_name="Date",value_name="Recovered")

    df["Date"]=pd.to_datetime(df['Date'])
    df1["Date"]=pd.to_datetime(df1['Date'])
    df2["Date"]=pd.to_datetime(df2['Date'])

    df3=pd.merge(df,df1,on=['Province/State',"Country/Region","Lat","Long","Date"])
    df3=pd.merge(df3,df2,on=['Province/State',"Country/Region","Lat","Long","Date"])
    return df3

st.title('Streamlit Dashboard Covid19')


st.header("Loading data")
df=load_data()
nb_head = st.slider('Number of rows to show',min_value=5,max_value=1000)
st.write(df.head(nb_head))


st.header("Over time")
carotte=df.groupby('Date')["Confirmed","Dead","Recovered"].sum()
crit = st.selectbox('Which column to show the distribution ?',["Confirmed","Dead","Recovered"])
bar=px.bar(carotte,x=carotte.index,y=crit)
st.plotly_chart(bar)


