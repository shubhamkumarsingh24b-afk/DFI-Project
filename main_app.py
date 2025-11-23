import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Simple version without OpenAI first
class DEIPlatform:
    def load_industry_data(self):
        companies = ['TechMahindra', 'Infosys', 'TCS', 'Wipro', 'HCL', 'Accenture']
        data = []
        for company in companies:
            base = np.random.uniform(0.25, 0.4)
            data.append({
                'company': company,
                'gender_diversity': round(base, 3),
                'leadership_diversity': round(max(0.1, base - 0.15), 3),
                'pay_equity_score': round(min(0.95, base + 0.4), 3),
                'inclusion_score': round(np.random.uniform(3.5, 4.5), 1),
                'employees': np.random.choice([50000, 100000, 250000, 500000]),
                'region': 'India'
            })
        return pd.DataFrame(data)

def main():
    st.set_page_config(page_title="DEI Platform", layout="wide")
    
    st.title("🎯 DEI Intelligence Platform")
    st.subheader("Indian IT Industry Analysis")
    
    # Initialize
    platform = DEIPlatform()
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose Page", ["Dashboard", "Company Analysis", "Trends"])
    
    # Load data
    df = platform.load_industry_data()
    
    if page == "Dashboard":
        st.header("📊 Dashboard")
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_gender = df['gender_diversity'].mean()
            st.metric("Avg Gender Diversity", f"{avg_gender:.1%}")
        with col2:
            avg_pay = df['pay_equity_score'].mean()
            st.metric("Avg Pay Equity", f"{avg_pay:.1%}")
        with col3:
            avg_inc = df['inclusion_score'].mean()
            st.metric("Avg Inclusion", f"{avg_inc:.1f}/5.0")
        
        # Charts
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(df, x='company', y='gender_diversity', 
                        title='Gender Diversity by Company')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.scatter(df, x='gender_diversity', y='pay_equity_score',
                           size='employees', color='company',
                           title='Diversity vs Pay Equity')
            st.plotly_chart(fig, use_container_width=True)
            
    elif page == "Company Analysis":
        st.header("🏢 Company Analysis")
        selected_company = st.selectbox("Select Company", df['company'].tolist())
        company_data = df[df['company'] == selected_company].iloc[0]
        
        st.subheader(f"DEI Metrics for {selected_company}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Gender Diversity", f"{company_data['gender_diversity']:.1%}")
        with col2:
            st.metric("Leadership Diversity", f"{company_data['leadership_diversity']:.1%}")
        with col3:
            st.metric("Pay Equity", f"{company_data['pay_equity_score']:.1%}")
            
    elif page == "Trends":
        st.header("📈 Industry Trends")
        st.line_chart(df.set_index('company')['gender_diversity'])

if __name__ == "__main__":
    main()