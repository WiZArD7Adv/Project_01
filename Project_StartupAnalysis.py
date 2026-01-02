import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv(
    r"C:\Users\binit\PyCharmMiscProject\Startup_App\startup_cleaned.csv"
)
df['date'] = pd.to_datetime(df['date'])
st.set_page_config(layout='wide',page_title='StartUp Analysis')
df['year']=df['date'].dt.year
df['month_name'] = df['date'].dt.month_name()

def delete_spaces_1(l):
    return [i.strip() for i in l]

def delete_spaces(L):
    return [i.strip() for i in L]

def investor_data(l, name):
    for i in l:
        if i == name:
            return True
    return False


def investor_details(investor_name):
    st.title(investor_name)



    def investor_data(l, name):
        for i in l:
            if i == name:
                return True
        return False




    investor_df = df[df['investors'].str.split(',').apply(lambda x: delete_spaces(x)).apply(lambda l: investor_data(l,investor_name))]
    st.subheader("Recent Investment")
    st.dataframe(investor_df[['date','startup','vertical','city','round','amount']].head(5))
    col1,col2=st.columns(2)
    with col1:
        st.subheader('Biggest investments')
        startup_amt = investor_df.groupby('startup')['amount'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots()
        ax.bar(startup_amt.index, startup_amt.values, color='blue')
        ax.set_xlabel("startups")
        ax.set_ylabel("amount in cr Rupees")
        st.pyplot(fig)
    with col2:
        st.subheader('Sector Invested In')
        vertical_amt = investor_df.groupby('vertical')['amount'].sum().sort_values(ascending=False)
        fig1, ax = plt.subplots()
        ax.pie(vertical_amt,labels=vertical_amt.index,autopct="%0.01f%%")
        st.pyplot(fig1)

    s1,s2=st.columns(2)
    with s1:
        st.subheader('Round Invested In')
        round_amt = investor_df.groupby('round')['amount'].sum().sort_values(ascending=False)
        fig2, ax = plt.subplots()
        ax.pie(round_amt, labels=round_amt.index, autopct="%0.01f%%")
        st.pyplot(fig2)

    with s2:
        st.subheader('City Invested In')
        city_amt = investor_df.groupby('city')['amount'].sum().sort_values(ascending=False)
        fig3, ax = plt.subplots()
        ax.pie(city_amt,labels= city_amt.index,autopct="%0.01f%%" )
        st.pyplot(fig3)

    st.subheader('Year Invested In')
    year_amt = investor_df.groupby('year')['amount'].sum().sort_values(ascending=False)
    fig4, ax = plt.subplots()
    ax.plot(year_amt.index, year_amt.values)
    st.pyplot(fig4)

def overall_analysis():
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.metric("Total",str(round(df['amount'].sum()))+' CR')

    with c2:
        st.metric("Max", str(round(df.groupby('startup')['amount'].sum().sort_values(ascending=False).iloc[0])) + ' CR')
    with c3:
        st.metric("Avg", str(round(df.groupby('startup')['amount'].sum().mean())) + ' CR')
    with c4:
        st.metric('Total Funded Startups',str(round(df['startup'].unique().shape[0])))

    st.subheader("MoM Analysis")
    x = st.selectbox("Select",['Total','Count'])
    if x == 'Total':
        month_year_amt = df.groupby(['month_name', 'year'])['amount'].sum()
        month_year_amt = month_year_amt.reset_index()
        month_year_amt['month_year'] = month_year_amt['month_name'].astype('str') + ' ' + month_year_amt['year'].astype(
            'str')
        month_year_amt.drop(columns=['month_name', 'year'], inplace=True)
        month_year_amt.set_index('month_year', inplace=True)
        fig5, ax = plt.subplots()
        ax.plot(month_year_amt.index, month_year_amt.values)
        st.pyplot(fig5)



    if x == 'Count':
        month_year_count=df.groupby(['month_name','year']).size()
        month_year_count = month_year_count.reset_index()
        month_year_count['month_year'] = month_year_count['month_name'].astype('str') + ' ' + month_year_count['year'].astype(
            'str')
        month_year_count.drop(columns=['month_name', 'year'], inplace=True)
        month_year_count.set_index('month_year', inplace=True)
        fig6, ax = plt.subplots()
        ax.plot(month_year_count.index, month_year_count.values)
        st.pyplot(fig6)


    st.subheader("Sector-Amount Analysis")
    fig7, ax = plt.subplots()
    ax.pie(df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10), labels=df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10).index, autopct="%0.01f%%")
    st.pyplot(fig7)

    st.subheader("Sector-Count Analysis")
    fig8, ax = plt.subplots()
    ax.pie(df.groupby('vertical').size().sort_values(ascending=False).head(10),
           labels=df.groupby('vertical').size().sort_values(ascending=False).head(10).index,
           autopct="%0.01f%%")
    st.pyplot(fig8)

    st.subheader('Types of Funding')
    st.dataframe(pd.Series(np.unique(df.groupby('round').size().index)))

    st.subheader("Top Cities for Investments")
    fig9, ax = plt.subplots()
    ax.pie(df.groupby('city').size().sort_values(ascending=False).head(10), labels=df.groupby('city').size().sort_values(ascending=False).head(10).index, autopct="%0.01f%%")
    st.pyplot(fig9)

    st.subheader("Top10 Startups Overall")
    fig10, ax = plt.subplots()
    ax.pie(df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10),labels=df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10).index,autopct="%0.01f%%")
    st.pyplot(fig10)

    st.subheader("Top startups Year Wise")
    D = {'year': [2015, 2016, 2017, 2018, 2019, 2020],
         'startup': [df[df['year'] == 2015].groupby('startup')['amount'].sum().sort_values(ascending=False).index[0],
                     df[df['year'] == 2016].groupby('startup')['amount'].sum().sort_values(ascending=False).index[0],
                     df[df['year'] == 2017].groupby('startup')['amount'].sum().sort_values(ascending=False).index[0],
                     df[df['year'] == 2018].groupby('startup')['amount'].sum().sort_values(ascending=False).index[0],
                     df[df['year'] == 2019].groupby('startup')['amount'].sum().sort_values(ascending=False).index[0],
                     df[df['year'] == 2020].groupby('startup')['amount'].sum().sort_values(ascending=False).index[0]]}
    year_wise=pd.DataFrame(D)
    st.dataframe(year_wise)

    amt_invested = []

    for i in delete_spaces_1(np.sort(np.unique(df['investors'].str.split(",").sum()))):
        investor_df = df[
            df['investors'].str.split(',').apply(lambda x: delete_spaces(x)).apply(lambda l: investor_data(l, i))]
        amt_invested.append(investor_df['amount'].sum())

    top_investor = pd.DataFrame({
        'Investor': delete_spaces_1(np.sort(np.unique(df['investors'].str.split(",").sum()))),
        "Amount_Invested": amt_invested
    }).sort_values('Amount_Invested', ascending=False).head(10)

    fig11,ax = plt.subplots()
    ax.bar(top_investor['Investor'], top_investor['Amount_Invested'])
    st.pyplot(fig11)

def Startup_Analysis(startup):
    st.header(startup)

    startup_df = df[df['startup'] == startup]
    st.metric('Total Invested', str(round(startup_df['amount'].sum()))+" Cr")
    st.subheader("Investors List")
    st.dataframe(pd.DataFrame(np.unique(startup_df['investors'].str.split(',').sum())))

    st.subheader("Industries")
    st.dataframe(startup_df['vertical'].drop_duplicates(keep='first').reset_index().drop(columns='index'))

    st.subheader("Subndustries")
    st.dataframe(startup_df['subvertical'].drop_duplicates(keep='first').reset_index().drop(columns='index'))

    st.subheader("Cities")
    st.dataframe(startup_df['city'].drop_duplicates(keep='first').reset_index().drop(columns='index'))











st.sidebar.header("Startup Analysis")
A = st.sidebar.selectbox("Select",["Overall Analysis","Startup","Investor"])
if A == "Overall Analysis":
    st.header("Overall Analysis")
    overall_analysis()

elif A == "Startup":

    selected_startup = st.sidebar.selectbox("Select Startup",sorted(df['startup'].unique()))
    btn1 = st.sidebar.button("Get Startup Details")
    if btn1:
        Startup_Analysis(selected_startup)


elif A == "Investor":


    selected_investor = st.sidebar.selectbox("Select Investor",delete_spaces_1(np.sort(np.unique(df['investors'].str.split(",").sum()))))
    btn2 = st.sidebar.button("Get Investors Details")
    if btn2:
        investor_details(selected_investor)




