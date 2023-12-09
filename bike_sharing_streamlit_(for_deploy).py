import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='dark')
import streamlit as st

df = pd.read_csv(r'C:\Users\TUKIYEM\Downloads\Upload\day.csv')
df_day_copy = df.copy()

Season_Map = {1:'Spring',
              2:'Summer',
              3:'Fall',
              4:'Winter'}

Day_Map = {0:'Sunday',
           1:'Monday',
           2:'Tuesday',
           3:'Wednesday',
           4:'Thursday',
           5:'Friday',
           6:'Saturday'}

df_day_copy['weekday'] = df_day_copy['weekday'].map(Day_Map)
df_day_copy['season'] = df_day_copy['season'].map(Season_Map)

df_day_copy['dteday'] = pd.to_datetime(df_day_copy['dteday'])
df_day_copy['dteday'] = df_day_copy.rename(columns={'dteday':'date'}, inplace=True)


def db_daily_days(df):
  daily_days = df_day_copy.resample(rule='D', on='date').agg({'season':'nunique',
                                                               'weekday':'nunique',
                                                               'cnt':'sum'}).reset_index()
  daily_days.rename({'season':'Season',
                      'weekday':'Day',
                      'cnt':'Total_Users'}, inplace=True)
  return daily_days


def db_weather_condition(df):
  weather_condition = df_day_copy.groupby('season').agg({'temp':'mean',
                                                         'atemp':'mean',
                                                         'hum':'mean',
                                                         'windspeed':'mean'}).reset_index()
  weather_condition.rename({'weathersit':'Weather_Sit',
                            'temp':'Temperature',
                            'atemp':'Temperature_Feeling',
                            'hum':'Humidity',
                            'windspeed':'WindSpeed'}, inplace=True)
  return weather_condition


def db_users(df):
  users_percentage = df_day_copy.filter(['date','season','weekday','casual','registered','cnt'], axis='columns')
  users_percentage = users_percentage.assign(casual_p = (users_percentage['casual']/users_percentage['cnt']).round(2)*100)
  users_percentage = users_percentage.assign(registered_p = (users_percentage['registered']/users_percentage['cnt']).round(2)*100)
  users_percentage.rename({'date':'Date',
                           'season':'Season',
                           'weekday':'Day',
                           'casual':'Casual',
                           'registered':'Registered',
                           'cnt':'Total_Users',
                           'casual_p':'Percentage_Casual_Users',
                           'registered_p':'Percentage_Registered_Users'})
  return users_percentage


def db_sum_users(df):
  sum_users_all = df_day_copy.filter(['date','weekday','season','cnt'])
  return sum_users_all

min_date = df_day_copy['date'].min()
max_date = df_day_copy['date'].max()

with st.sidebar:
    start_date, end_date = st.date_input(label='Date',min_value=min_date,
                                         max_value=max_date,
                                         value=[min_date, max_date])

df_dashb = df_day_copy[(df_day_copy['date'] >= str(start_date)) & (df_day_copy['date'] <= str(end_date))]

df_dashb_daily_days = db_daily_days(df_dashb)
df_dashb_weather_condition = db_weather_condition(df_dashb)
df_dashb_users = db_users(df_dashb)
df_dashb_sum_users = db_sum_users(df_dashb)

st.header('Dicoding Dashboard by Burhan, Bike Sharing Report')

st.subheader('Daily Report')

tab1, tab2, tab3, tab4 = st.tabs(['Users','Weather Influence','Days vs Weather','Summary'])

with tab1:
  st.header('Users')
  col1, col2 = st.columns(2)
  with col1:
    Total_Customer = df_dashb_users.cnt.sum()
    st.metric('Total Customer', value=Total_Customer)
  with col2:
    Counted_Date = df_dashb.date.count()
    st.metric('Total Counted Day', value=Counted_Date)

with tab2:
  st.header('Weather Influence')
  df_dashb_weather_condition = pd.DataFrame(df_dashb_weather_condition)
  colA,colB = st.columns(2)
  with colA:
      fig1,ax1 = plt.subplots(figsize=(13,10))
      sns.barplot(x=df_dashb_weather_condition['season'], y=df_dashb_weather_condition['temp'], width=0.6)
      plt.gca().spines[['top', 'right']].set_visible(False)
      ax1 = sns.barplot(x=df_dashb_weather_condition['season'],y=df_dashb_weather_condition['temp'], color='blue', width=0.6)
      ax1.bar_label(ax1.containers[0])
      st.subheader('Temperature')
      st.pyplot(fig1)
      fig2,ax2 = plt.subplots(figsize=(13,10))
      sns.barplot(x=df_dashb_weather_condition['season'], y=df_dashb_weather_condition['atemp'], width=0.6)
      plt.gca().spines[['top', 'right']].set_visible(False)
      ax2 = sns.barplot(x=df_dashb_weather_condition['season'],y=df_dashb_weather_condition['atemp'], color='blue', width=0.6)
      ax2.bar_label(ax2.containers[0])
      st.subheader('Feeling Temperature')
      st.pyplot(fig2)
  with colB:
      fig3,ax3 = plt.subplots(figsize=(13,10))
      sns.barplot(x=df_dashb_weather_condition['season'], y=df_dashb_weather_condition['hum'], width=0.6)
      plt.gca().spines[['top', 'right']].set_visible(False)
      ax3 = sns.barplot(x=df_dashb_weather_condition['season'],y=df_dashb_weather_condition['hum'], color='blue', width=0.6)
      ax3.bar_label(ax3.containers[0])
      st.subheader('Humidity')
      st.pyplot(fig3)  
      fig4,ax4 = plt.subplots(figsize=(13,10))
      sns.barplot(x=df_dashb_weather_condition['season'], y=df_dashb_weather_condition['windspeed'], width=0.6)
      plt.gca().spines[['top', 'right']].set_visible(False)
      ax1 = sns.barplot(x=df_dashb_weather_condition['season'],y=df_dashb_weather_condition['windspeed'], color='blue', width=0.6)
      ax4.bar_label(ax4.containers[0])
      st.subheader('Wind Speed')
      st.pyplot(fig4)
    
with tab3:
  st.header('Days vs Weather')
  col3,col4,col5 = st.columns(3)
  with col3:
    st.text('Table Count of Casual User Based on Weather and Day They Sharing')
    Casual_User = df_dashb_users.drop(['registered','registered_p'], axis='columns', inplace=False)
    Casual_User = Casual_User.groupby('season').mean('casual','cnt','casual_p').reset_index()
    Casual_User = Casual_User.sort_values(by='casual', ascending=False).head(10)
    Casual_User
  with col4:
    st.text('Table Count of Casual User Based on Weather and Day They Sharing')
    Registered_User = df_dashb_users.drop(['casual','casual_p'], axis='columns', inplace=False)
    Registered_User = Registered_User.groupby('season').mean('registered','cnt','registered_p').reset_index()
    Registered_User = Registered_User.sort_values(by='registered', ascending=False).head(10)
    Registered_User
  with col5:
    Mode_Casual_User = df_dashb_users.drop(['registered','registered_p'], axis='columns', inplace=False)
    Mode_Casual_User = Mode_Casual_User.sort_values(by='casual', ascending=False).head(10)
    Mode_Casual_User = Mode_Casual_User['season'].mode()
    st.metric('The Most Season with High Casual Customer', value=Mode_Casual_User[0])

    Mode_Registered_User = df_dashb_users.drop(['casual','casual_p'], axis='columns', inplace=False)
    Mode_Registered_User = Mode_Registered_User.sort_values(by='registered', ascending=False).head(10)
    Mode_Registered_User = Mode_Registered_User['season'].mode()
    st.metric('The Most Season with High Registered Customer', value=Mode_Registered_User[0])

with tab4:
  st.header('Summary')
  dashb_sum_users = df_dashb_sum_users.groupby('weekday').sum('cnt').reset_index()
  dashb_sum_users
  fig5,ax5 = plt.subplots(figsize=(7,4))
  sns.lineplot(x=df_dashb_sum_users['weekday'], y=df_dashb_sum_users['cnt'], errorbar=None)
  plt.gca().spines[['top', 'right']].set_visible(False)
  plt.xlabel('Days')
  plt.ylabel('Total of Users')
  plt.title('Total User each Day')
  st.pyplot(fig5)

  colC, colD = st.columns(2)
  with colC:
    dashb_sum_users_season = df_dashb_sum_users[df_dashb_sum_users['season'] == 'Fall'].groupby('weekday').sum('cnt').reset_index()
    fig6,ax6 = plt.subplots(figsize=(12,7))
    sns.barplot(x=dashb_sum_users_season['weekday'], y=dashb_sum_users_season['cnt'], width=0.6)
    plt.gca().spines[['top', 'right']].set_visible(False)
    ax6 = sns.barplot(x=dashb_sum_users_season['weekday'], y=dashb_sum_users_season['cnt'], color='blue', width=0.6)
    ax6.bar_label(ax6.containers[0])
    st.subheader('Fall')
    st.pyplot(fig6)
    dashb_sum_users_season = df_dashb_sum_users[df_dashb_sum_users['season'] == 'Summer'].groupby('weekday').sum('cnt').reset_index()
    fig7,ax7 = plt.subplots(figsize=(12,7))
    sns.barplot(x=dashb_sum_users_season['weekday'], y=dashb_sum_users_season['cnt'], width=0.6)
    plt.gca().spines[['top', 'right']].set_visible(False)
    ax7 = sns.barplot(x=dashb_sum_users_season['weekday'], y=dashb_sum_users_season['cnt'], color='blue', width=0.6)
    ax7.bar_label(ax7.containers[0])
    st.subheader('Summer')
    st.pyplot(fig7)
  with colD:
    dashb_sum_users_season = df_dashb_sum_users[df_dashb_sum_users['season'] == 'Spring'].groupby('weekday').sum('cnt').reset_index()
    fig8,ax8 = plt.subplots(figsize=(12,7))
    sns.barplot(x=dashb_sum_users_season['weekday'], y=dashb_sum_users_season['cnt'], width=0.6)
    plt.gca().spines[['top', 'right']].set_visible(False)
    ax8 = sns.barplot(x=dashb_sum_users_season['weekday'], y=dashb_sum_users_season['cnt'], color='blue', width=0.6)
    ax8.bar_label(ax8.containers[0])
    st.subheader('Spring')
    st.pyplot(fig8)
    dashb_sum_users_season = df_dashb_sum_users[df_dashb_sum_users['season'] == 'Winter'].groupby('weekday').sum('cnt').reset_index()
    fig9,ax9 = plt.subplots(figsize=(12,7))
    sns.barplot(x=dashb_sum_users_season['weekday'], y=dashb_sum_users_season['cnt'], width=0.6)
    plt.gca().spines[['top', 'right']].set_visible(False)
    ax9 = sns.barplot(x=dashb_sum_users_season['weekday'], y=dashb_sum_users_season['cnt'], color='blue', width=0.6)
    ax9.bar_label(ax9.containers[0])
    st.subheader('Winter')
    st.pyplot(fig9)