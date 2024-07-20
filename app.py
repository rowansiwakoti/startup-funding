import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='Indian Startup Analysis')

df = pd.read_csv('startup_cleaned.csv')

df['date'] = pd.to_datetime(df['date'])

df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

print(type(df.info()))

def load_startup_details(startup):
    st.markdown(f"<h3 style='text-align: center; text-decoration: underline'>{startup} Analysis</h3>", unsafe_allow_html=True)
    details = df[df['startup'] == startup][['date','vertical','subvertical', 'investors', 'amount']]
    st.dataframe(details)

def load_overall_analysis():
    st.markdown(f"<h3 style='text-align: center; text-decoration: underline'>Overall Analysis</h3>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # total invested amount
        total = round(df['amount'].sum())
        st.metric('Total', str(total) + ' Cr')
    with col2:
        # max funding amount
        max_funding = round(df.groupby('startup')['amount'].max().sort_values().tail(1).values[0])
        st.metric('Max Funding', str(max_funding) + ' Cr')
    with col3:
        avg_funding = round(df.groupby('startup')['amount'].sum().mean())
        st.metric('Average Funding', str(avg_funding) + ' Cr')
    with col4:
        no_startups = df['startup'].nunique()
        st.metric('Total Startups', no_startups)

    st.markdown(f"<h4>Monthly Graph</h4>", unsafe_allow_html=True)
    selected_option = st.selectbox('Select Type', ['Total Funding', 'Number of Startups'])

    if selected_option == 'Total Funding':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

        fig1, ax1 = plt.subplots()
        ax1.plot(temp_df['x_axis'], temp_df['amount'])
        st.pyplot(fig1)
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
        temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

        fig1, ax1 = plt.subplots()
        ax1.plot(temp_df['x_axis'], temp_df['amount'])
        st.pyplot(fig1)

    st.markdown(f"<h4>Top 5 Investement Sectors</h4>", unsafe_allow_html=True)
    
    top5_verticals = df.groupby('vertical')['amount'].max().sort_values(ascending=False).head(5)
    fig1, ax1 = plt.subplots()
    ax1.pie(top5_verticals, labels=top5_verticals.index, autopct="%0.01f%%")
    st.pyplot(fig1)


def load_investor_details(investor):
    # st.subheader(investor + ' Investment Analysis:')
    st.markdown(f"<h3 style='text-align: center; text-decoration: underline'>{investor} Investment Analysis</h3>", unsafe_allow_html=True)


    # Load the most recent 5 invesments of the investor
    last_5 = df[df['investors'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'subvertical', 'city', 'round', 'amount']]
    # st.subheader('Five Most Recent Investments')
    st.markdown(f"<h4>Five Most Recent Investments</h4>", unsafe_allow_html=True)
    st.dataframe(last_5)


    # Biggest investments
    big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
    # st.subheader('Five Biggest Investments')
    st.markdown(f"<h4>Five Biggest Investments</h4>", unsafe_allow_html=True)

    fig, ax = plt.subplots()
    ax.bar(big_series.index, big_series.values)
    st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        # st.subheader('Sectors Invested In')
        st.markdown(f"<h4>Sectors Invested In</h4>", unsafe_allow_html=True)

        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)
    
    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        # st.subheader('City Invested In')
        st.markdown(f"<h4>City Invested In</h4>", unsafe_allow_html=True)

        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)
    

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    # st.subheader('Year on Year Investments')
    st.markdown(f"<h4>Year on Year Investments</h4>", unsafe_allow_html=True)

    fig1, ax1 = plt.subplots()
    ax1.plot(year_series.index, year_series.values)
    st.pyplot(fig1)

st.sidebar.subheader('Indian Startup Funding Analysis')

option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()
elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select Startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:
        load_startup_details(selected_startup)
else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)




