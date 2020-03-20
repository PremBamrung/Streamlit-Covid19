import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px 
import plotly.graph_objs as go
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
    df3["Active"]=df3.Confirmed-df3.Dead-df3.Recovered
    return df3

st.title('Dashboard Covid19')


# st.header("Loading data")
df=load_data()

features=["Confirmed","Dead","Recovered","Active"]



mode=st.sidebar.selectbox("Mode",["Overview","Flourish","About"])


if mode=="Overview":

    st.write("This is an experimental dashboard to showcase the evolution of Covid-19 around the world.")

    if st.checkbox("Show raw data"):
        nb_head = st.slider('Number of rows to show',min_value=5,max_value=1000)
        st.write(df.head(nb_head))



    st.header("Global")

    carotte=df.groupby('Date')[features].sum()



    fig = go.Figure()
    fig.add_trace(go.Scatter(x=carotte.index, y=carotte.Confirmed,
                    mode='lines+markers',
                    name='Confirmed'))
    fig.add_trace(go.Scatter(x=carotte.index, y=carotte.Dead,
                    mode='lines+markers',
                    name='Dead'))

    fig.add_trace(go.Scatter(x=carotte.index, y=carotte.Recovered,
                    mode='lines+markers',
                    name='Recovered'))            
    
    fig.add_trace(go.Scatter(x=carotte.index, y=carotte.Active,
                    mode='lines+markers',
                    name='Active'))    

    st.plotly_chart(fig)

    toto=df[df.Date=="2020-03-19"].groupby("Country/Region")[features].sum().sort_values("Confirmed",ascending=False)
    toto=toto.head(20)
    # fig=px.bar(toto,x=toto.index,y="Confirmed",orientation="v",color=toto.index)
    fig=go.Figure(data=[
        go.Bar(name="Active",x=toto.index,y=toto.Active),
        go.Bar(name="Dead",x=toto.index,y=toto.Dead),
        go.Bar(name="Recovered",x=toto.index,y=toto.Recovered),
    ])

    fig.update_layout(
    yaxis_title="Cases",
    xaxis_title="Country",
    showlegend=True,
    barmode='stack')
    st.plotly_chart(fig)



    st.header("Evolution by country/region")

    selected_country=st.selectbox("Choose your country",sorted(df["Country/Region"].unique()))
    country=df[(df["Country/Region"]==selected_country)]
    country=country.groupby("Date")[features].sum()

    fig=go.Figure()
    fig.add_scatter(x=country.index,y=country["Confirmed"],name="Confirmed")
    fig.add_scatter(x=country.index,y=country["Dead"],name="Dead")
    fig.add_scatter(x=country.index,y=country["Active"],name="Active")
    fig.add_scatter(x=country.index,y=country["Recovered"],name="Recovered")

    fig.update_layout(
        title=f"Evolution of cases for {selected_country}",
        xaxis_title="Time",
        yaxis_title="Population")
    st.plotly_chart(fig)





    df_last=df.groupby("Date")[features].sum().tail(1)


    st.header(f"Total Confirmed : {df_last.Confirmed[0]}")

    toto=df[df.Date=="2020-03-19"].groupby("Country/Region")[features].sum().sort_values("Confirmed",ascending=False)
    toto=toto.head(15)
    fig=px.bar(toto,y=toto.index,x="Confirmed",orientation="h",color=toto.index).update_yaxes(categoryorder="total ascending")
    fig.update_layout(
    xaxis_title="Confirmed Cases",
    yaxis_title="Country",
    showlegend=False)
    st.plotly_chart(fig)




    st.header(f"Total Death : {df_last.Dead[0]} ({round((df_last.Dead[0]/df_last.Confirmed[0])*100,2)} %)")

    toto=df[df.Date=="2020-03-19"].groupby("Country/Region")[features].sum().sort_values("Dead",ascending=False)
    toto=toto.head(15)
    fig=px.bar(toto,y=toto.index,x="Dead",orientation="h",color=toto.index).update_yaxes(categoryorder="total ascending")
    fig.update_layout(
    xaxis_title="Dead Cases",
    yaxis_title="Country",
    showlegend=False)
    st.plotly_chart(fig)




    st.header(f"Total Recovered : {df_last.Recovered[0]} ({round((df_last.Recovered[0]/df_last.Confirmed[0])*100,2)} %)")

    toto=df[df.Date=="2020-03-19"].groupby("Country/Region")[features].sum().sort_values("Recovered",ascending=False)
    toto=toto.head(15)
    fig=px.bar(toto,y=toto.index,x="Recovered",orientation="h",color=toto.index).update_yaxes(categoryorder="total ascending")
    fig.update_layout(
    xaxis_title="Recovered Cases",
    yaxis_title="Country",
    showlegend=False)
    st.plotly_chart(fig)




    st.header(f"Total Active : {df_last.Active[0]} ({round((df_last.Active[0]/df_last.Confirmed[0])*100,2)} %)")

    toto=df[df.Date=="2020-03-19"].groupby("Country/Region")[features].sum().sort_values("Active",ascending=False)
    toto=toto.head(15)
    fig=px.bar(toto,y=toto.index,x="Active",orientation="h",color=toto.index).update_yaxes(categoryorder="total ascending")
    fig.update_layout(
    xaxis_title="Active Cases",
    yaxis_title="Country",
    showlegend=False)
    st.plotly_chart(fig)



    st.header(f"DataFrame")
    kiwi= df[df.Date=="2020-03-19"].groupby("Country/Region")[features].sum()
    kiwi["Recovery Rate"]=round(kiwi.Recovered/kiwi.Confirmed,2)
    kiwi["Death Rate"]=round(kiwi.Dead/kiwi.Confirmed,2)
    kiwi["Death Rate"]=kiwi["Death Rate"].map(lambda n: '{:.2%}'.format(n))
    kiwi["Recovery Rate"]=kiwi["Recovery Rate"].map(lambda n: '{:.2%}'.format(n))
    st.dataframe(kiwi.style.highlight_max(axis=0))





elif mode =='Flourish':
    st.header("Evolution of confirmed cases around the world")
    flourish_confirmed="<iframe src='https://public.flourish.studio/visualisation/1627982/embed' frameborder='0' scrolling='no' style='width:100%;height:600px;'></iframe><div style='width:100%!;margin-top:4px!important;text-align:right!important;'><a class='flourish-credit' href='https://public.flourish.studio/visualisation/1627982/?utm_source=embed&utm_campaign=visualisation/1627982' target='_top' style='text-decoration:none!important'><img alt='Made with Flourish' src='https://public.flourish.studio/resources/made_with_flourish.svg' style='width:105px!important;height:16px!important;border:none!important;margin:0!important;'> </a></div>"
    st.markdown(flourish_confirmed, unsafe_allow_html=True)

    st.header("Evolution of recovered cases around the world")
    flourish_recovered="<iframe src='https://public.flourish.studio/visualisation/1628304/embed' frameborder='0' scrolling='no' style='width:100%;height:600px;'></iframe><div style='width:100%!;margin-top:4px!important;text-align:right!important;'><a class='flourish-credit' href='https://public.flourish.studio/visualisation/1628304/?utm_source=embed&utm_campaign=visualisation/1628304' target='_top' style='text-decoration:none!important'><img alt='Made with Flourish' src='https://public.flourish.studio/resources/made_with_flourish.svg' style='width:105px!important;height:16px!important;border:none!important;margin:0!important;'> </a></div>"
    st.markdown(flourish_recovered, unsafe_allow_html=True)
    
    st.header("Evolution of death cases around the world")
    flourish_death="<iframe src='https://public.flourish.studio/visualisation/1628288/embed' frameborder='0' scrolling='no' style='width:100%;height:600px;'></iframe><div style='width:100%!;margin-top:4px!important;text-align:right!important;'><a class='flourish-credit' href='https://public.flourish.studio/visualisation/1628288/?utm_source=embed&utm_campaign=visualisation/1628288' target='_top' style='text-decoration:none!important'><img alt='Made with Flourish' src='https://public.flourish.studio/resources/made_with_flourish.svg' style='width:105px!important;height:16px!important;border:none!important;margin:0!important;'> </a></div>"
    st.markdown(flourish_death, unsafe_allow_html=True)







elif mode=="About":

    st.write("""
    Hi, I'm Premchanok BAMRUNG, currently intern Data Scientist. I was working on some data for my company when I thought that it would be a cool idea to use Streamlit to showcase my Exploratory Dat Analysis. But then came the Covid 19 crisi and I thought that it would be cool to create another dashboard on my own.
    
    The idea is to use Streamlit, Heroku, the standard Data Science stack (Pandas, Numpy, Seaborn...) and Flourish to create a really cool dashboard where one can select 
    whatever to see.

    If you have any suggestion, do not hesitate to contact me.


    Contact: bamrungprem@gmail.com
    
    
     """)

