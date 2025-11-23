import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

class AdvancedDEIPlatform:
    def __init__(self):
        # Initialize without OpenAI for now
        pass
        
    def load_industry_data(self):
        """Load comprehensive IT industry DEI data"""
        np.random.seed(42)
        companies = ['TechMahindra', 'Infosys', 'TCS', 'Wipro', 'HCL', 'Accenture', 'Capgemini', 'Cognizant']
        
        data = []
        for company in companies:
            base_score = np.random.normal(0.65, 0.15)
            data.append({
                'company': company,
                'gender_diversity': max(0.15, min(0.85, base_score)),
                'leadership_diversity': max(0.1, min(0.7, base_score - 0.15)),
                'pay_equity_score': max(0.6, min(0.98, base_score + 0.1)),
                'inclusion_survey_score': max(3.0, min(5.0, (base_score * 5) + 2)),
                'retention_rate_diverse': max(0.7, min(0.95, base_score + 0.2)),
                'promotion_rate_diverse': max(0.08, min(0.25, base_score * 0.3)),
                'employees': np.random.choice([5000, 250000, 600000, 200000, 220000, 50000, 300000, 350000]),
                'revenue_cr': np.random.uniform(500, 250000),
                'dei_budget_pct': np.random.uniform(0.1, 2.5),
                'region': 'India'
            })
        return pd.DataFrame(data)

def display_dashboard(df):
    st.header("📊 Industry DEI Dashboard")
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_gender = df['gender_diversity'].mean()
        st.metric("Gender Diversity", f"{avg_gender:.1%}", 
                 delta=f"{(avg_gender - 0.3)*100:.1f}% vs target")
        
    with col2:
        avg_pay = df['pay_equity_score'].mean()
        st.metric("Pay Equity", f"{avg_pay:.1%}", 
                 delta=f"{(avg_pay - 0.85)*100:.1f}% vs target")
        
    with col3:
        avg_inclusion = df['inclusion_survey_score'].mean()
        st.metric("Inclusion Score", f"{avg_inclusion:.1f}/5.0")
        
    with col4:
        avg_retention = df['retention_rate_diverse'].mean()
        st.metric("Diverse Retention", f"{avg_retention:.1%}")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.box(df, y='gender_diversity', title='Gender Diversity Distribution')
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.scatter(df, x='dei_budget_pct', y='inclusion_survey_score',
                        size='employees', color='company', hover_name='company',
                        title='DEI Budget vs Inclusion Score')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        fig = px.bar(df.sort_values('pay_equity_score'), 
                    x='company', y='pay_equity_score',
                    title='Pay Equity by Company')
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation heatmap
        corr_data = df[['gender_diversity', 'leadership_diversity', 'pay_equity_score', 
                       'inclusion_survey_score', 'retention_rate_diverse']].corr()
        fig = px.imshow(corr_data, text_auto=True, aspect="auto",
                       title='DEI Metrics Correlation Matrix')
        st.plotly_chart(fig, use_container_width=True)

def display_benchmarking(df):
    st.header("🏆 Advanced Company Benchmarking")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_company = st.selectbox("Select Company", df['company'].tolist())
        benchmark_companies = st.multiselect("Compare With", 
                                           df['company'].tolist(),
                                           default=['TCS', 'Infosys'])
        
        company_data = df[df['company'] == selected_company].iloc[0]
        
    with col2:
        st.subheader(f"DEI Scorecard: {selected_company}")
        
        # Progress bars for key metrics
        metrics = [
            ('Gender Diversity', company_data['gender_diversity'], 0.4),
            ('Leadership Diversity', company_data['leadership_diversity'], 0.3),
            ('Pay Equity', company_data['pay_equity_score'], 0.9),
            ('Inclusion', company_data['inclusion_survey_score']/5, 0.8)
        ]
        
        for metric, value, target in metrics:
            col_a, col_b, col_c = st.columns([2, 5, 1])
            with col_a:
                st.write(metric)
            with col_b:
                st.progress(value, text=f"{value:.1%}")
            with col_c:
                delta = value - target
                st.metric("", f"{delta:+.1%}", delta_color="inverse" if delta < 0 else "normal")
    
    # Radar Chart
    categories = ['Gender Diversity', 'Leadership Diversity', 'Pay Equity', 
                 'Inclusion', 'Retention', 'Promotion Rate']
    
    company_values = [
        company_data['gender_diversity'] * 100,
        company_data['leadership_diversity'] * 100,
        company_data['pay_equity_score'] * 100,
        (company_data['inclusion_survey_score']/5) * 100,
        company_data['retention_rate_diverse'] * 100,
        company_data['promotion_rate_diverse'] * 100
    ]
    
    fig = go.Figure()
    
    # Add selected company
    fig.add_trace(go.Scatterpolar(
        r=company_values,
        theta=categories,
        fill='toself',
        name=selected_company
    ))
    
    # Add benchmark companies
    for bench_company in benchmark_companies:
        if bench_company != selected_company:
            bench_data = df[df['company'] == bench_company].iloc[0]
            bench_values = [
                bench_data['gender_diversity'] * 100,
                bench_data['leadership_diversity'] * 100,
                bench_data['pay_equity_score'] * 100,
                (bench_data['inclusion_survey_score']/5) * 100,
                bench_data['retention_rate_diverse'] * 100,
                bench_data['promotion_rate_diverse'] * 100
            ]
            fig.add_trace(go.Scatterpolar(
                r=bench_values,
                theta=categories,
                fill='toself',
                name=bench_company
            ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title="DEI Performance Radar Chart"
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_ai_analysis(df):
    st.header("🤖 Strategic Analysis")
    
    analysis_type = st.selectbox("Analysis Type", [
        "Industry Trend Analysis",
        "Inclusion Barrier Detection", 
        "Best Practice Identification",
        "ROI & Business Impact",
        "Regulatory Compliance Risk"
    ])
    
    selected_companies = st.multiselect("Focus Companies", 
                                      df['company'].tolist(),
                                      default=df['company'].tolist()[:3])
    
    if st.button("🚀 Generate Analysis", type="primary"):
        with st.spinner("Analyzing DEI patterns and generating insights..."):
            # Simulated analysis (replace with real AI later)
            insights = {
                "Industry Trend Analysis": """
                **Key Insights:**
                1. Indian IT industry shows 28% average gender diversity, lagging behind global benchmarks
                2. Companies with higher leadership diversity show 23% better innovation metrics
                3. Pay equity gaps persist despite public commitments to DEI
                
                **Recommendations:**
                • Implement structured mentorship programs
                • Set transparent diversity targets
                • Conduct regular pay equity audits
                """,
                "Inclusion Barrier Detection": """
                **Key Barriers Identified:**
                1. Unconscious bias in promotion processes
                2. Lack of psychological safety in teams
                3. Remote work inclusion challenges
                
                **Solutions:**
                • Implement bias detection in performance reviews
                • Create inclusion metrics for managers
                • Develop hybrid work guidelines
                """
            }
            
            ai_response = insights.get(analysis_type, "Analysis complete. Please select a specific analysis type.")
            
        st.success("Analysis Complete!")
        
        st.subheader("📈 Strategic Insights")
        st.info(ai_response)
        
        # Additional visualization
        if "Trend" in analysis_type:
            display_trend_analysis(df, selected_companies)
        elif "Barrier" in analysis_type:
            display_barrier_analysis(df, selected_companies)

def display_trend_analysis(df, companies):
    st.subheader("Trend Analysis Visualization")
    
    # Simulate trend data
    months = pd.date_range('2023-01-01', periods=12, freq='M')
    trend_data = []
    
    for company in companies:
        base_val = df[df['company'] == company]['gender_diversity'].iloc[0]
        for i, month in enumerate(months):
            trend_data.append({
                'month': month,
                'company': company,
                'diversity_score': base_val + (i * 0.02) + np.random.normal(0, 0.01),
                'inclusion_score': df[df['company'] == company]['inclusion_survey_score'].iloc[0] + (i * 0.1)
            })
    
    trend_df = pd.DataFrame(trend_data)
    fig = px.line(trend_df, x='month', y='diversity_score', color='company',
                 title='Gender Diversity Trends (Simulated)')
    st.plotly_chart(fig, use_container_width=True)

def display_interventions(df):
    st.header("🔄 Intervention Strategies")
    
    col1, col2 = st.columns(2)
    
    with col1:
        company_size = st.selectbox("Organization Size", 
            ["Startup (<500 employees)", "Growth Stage (500-5,000)", "Enterprise (5,000-50,000)", "Large Enterprise (>50,000)"])
        
        primary_focus = st.selectbox("Primary Focus Area",
            ["Recruitment & Hiring", "Retention & Advancement", "Inclusive Culture", "Pay Equity", "Leadership Diversity"])
        
        budget = st.slider("Annual DEI Budget (₹ Lakhs)", 5, 500, 50, 5)
        
    with col2:
        timeline = st.select_slider("Implementation Timeline",
            ["Quick Wins (3-6 months)", "Medium Term (6-18 months)", "Long Term (18-36 months)"])
        
        maturity = st.radio("Current DEI Maturity",
            ["Beginning", "Developing", "Maturing", "Advanced"])
        
        industry_challenges = st.multiselect("Specific Challenges",
            ["Unconscious Bias", "Pipeline Issues", "Inclusion Measurement", "Leadership Buy-in", "Remote Work Inclusion"])
    
    if st.button("🎯 Generate Customized Strategy", type="primary"):
        with st.spinner("Designing your customized DEI strategy..."):
            # Simulated strategy generation
            strategy = f"""
            **Customized DEI Strategy for {company_size}**
            
            **Focus Area:** {primary_focus}
            **Budget:** ₹{budget} lakhs annually
            **Timeline:** {timeline}
            
            **Implementation Plan:**
            1. **Assessment Phase** (Months 1-2): Comprehensive DEI audit and stakeholder interviews
            2. **Foundation Phase** (Months 3-6): Policy development and leadership training
            3. **Implementation Phase** (Months 7-18): Program rollout and capability building
            4. **Scaling Phase** (Months 19-36): Culture integration and optimization
            
            **Key Initiatives:**
            • Mentorship and sponsorship programs
            • Bias-free recruitment processes
            • Inclusive leadership development
            • Regular pay equity analysis
            
            **Success Metrics:**
            • Increase diverse hiring by 25% within 12 months
            • Improve inclusion survey scores by 15 points
            • Reduce attrition of diverse employees by 20%
            """
        
        st.success("Custom DEI Strategy Generated!")
        
        tabs = st.tabs(["Strategy Overview", "Implementation Plan", "Success Metrics", "Business Case"])
        
        with tabs[0]:
            st.subheader("Strategy Overview")
            st.write(strategy)
        
        with tabs[1]:
            st.subheader("Implementation Timeline")
            phases = {
                "Phase 1: Foundation (Months 1-3)": ["Assessment", "Stakeholder Alignment", "Goal Setting"],
                "Phase 2: Implementation (Months 4-12)": ["Program Rollout", "Training", "Policy Updates"],
                "Phase 3: Scaling (Months 13-24)": ["Expansion", "Optimization", "Culture Integration"]
            }
            
            for phase, activities in phases.items():
                with st.expander(phase):
                    for activity in activities:
                        st.checkbox(activity)
        
        with tabs[2]:
            st.subheader("Success Metrics Dashboard")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Diversity Hiring", "+25%", "Year 1 Target")
            with col2:
                st.metric("Inclusion Score", "+15 pts", "Survey Improvement")
            with col3:
                st.metric("Retention", "-12%", "Attrition Reduction")
        
        with tabs[3]:
            st.subheader("Business Impact Analysis")
            st.metric("Estimated ROI", "₹2.5-4.0 Cr", "+185% return")
            st.metric("Productivity Gain", "12-18%", "Inclusive teams")
            st.metric("Innovation Impact", "+27%", "Diverse perspectives")

def display_impact_simulator():
    st.header("📈 DEI Impact Simulator")
    
    st.info("Simulate the business impact of different DEI initiatives")
    
    col1, col2 = st.columns(2)
    
    with col1:
        diversity_increase = st.slider("Increase in Gender Diversity (%)", 5, 50, 15)
        inclusion_score = st.slider("Improvement in Inclusion Score", 5, 30, 12)
        retention_improvement = st.slider("Retention Improvement (%)", 3, 20, 8)
        
    with col2:
        budget_allocation = st.slider("Annual DEI Budget (₹ Lakhs)", 10, 200, 50)
        employee_count = st.number_input("Total Employees", 100, 100000, 5000)
        time_horizon = st.selectbox("Time Horizon", ["1 Year", "2 Years", "3 Years"])
    
    if st.button("Calculate Business Impact"):
        # Simulate impact calculations
        base_salary = 12  # lakhs average
        hiring_cost = 0.3 * base_salary  # 30% of annual salary
        turnover_cost = 1.5 * base_salary  # 150% of annual salary
        
        # Calculate benefits
        reduced_turnover = employee_count * (retention_improvement/100) * turnover_cost
        hiring_savings = employee_count * (diversity_increase/100) * hiring_cost
        productivity_gain = employee_count * (inclusion_score/100) * base_salary * 0.15
        
        total_benefits = reduced_turnover + hiring_savings + productivity_gain
        roi = ((total_benefits - (budget_allocation * 100000)) / (budget_allocation * 100000)) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Benefits", f"₹{total_benefits/10000000:.1f} Cr")
        with col2:
            st.metric("ROI", f"{roi:.0f}%")
        with col3:
            st.metric("Payback Period", "14 months")
        
        # Impact visualization
        impact_data = pd.DataFrame({
            'Category': ['Reduced Turnover', 'Hiring Savings', 'Productivity Gain', 'DEI Investment'],
            'Amount': [reduced_turnover, hiring_savings, productivity_gain, budget_allocation * 100000]
        })
        
        fig = px.bar(impact_data, x='Category', y='Amount', 
                    title='DEI Investment vs Return Analysis')
        st.plotly_chart(fig, use_container_width=True)

def main():
    st.set_page_config(page_title="DEI Intelligence Platform", layout="wide")
    
    st.title("🎯 AI-Powered DEI Intelligence Platform")
    st.subheader("Measuring & Optimizing Workplace Inclusion Across India's IT Industry")
    
    # Initialize platform
    platform = AdvancedDEIPlatform()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox("Choose Module", 
        ["🏠 Dashboard", "📊 Benchmarking", "🤖 AI Analysis", "🔄 Interventions", "📈 Impact Simulator"])
    
    # Load data
    df = platform.load_industry_data()
    
    if app_mode == "🏠 Dashboard":
        display_dashboard(df)
    elif app_mode == "📊 Benchmarking":
        display_benchmarking(df)
    elif app_mode == "🤖 AI Analysis":
        display_ai_analysis(df)
    elif app_mode == "🔄 Interventions":
        display_interventions(df)
    elif app_mode == "📈 Impact Simulator":
        display_impact_simulator()

if __name__ == "__main__":
    main()
