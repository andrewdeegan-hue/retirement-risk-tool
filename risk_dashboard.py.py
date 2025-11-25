import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sequence of Returns Risk",
    page_icon="📉",
    layout="wide"
)

# --- DATA ---
# Hardcoded S&P 500 Real Returns (Inflation Adjusted)
# This allows the script to run without needing an external CSV file.
data = [
  {'year': 1928, 'return': 0.4549}, {'year': 1929, 'return': -0.0883}, {'year': 1930, 'return': -0.2001},
  {'year': 1931, 'return': -0.3807}, {'year': 1932, 'return': 0.0182}, {'year': 1933, 'return': 0.4885},
  {'year': 1934, 'return': -0.0266}, {'year': 1935, 'return': 0.4249}, {'year': 1936, 'return': 0.3006},
  {'year': 1937, 'return': -0.3713}, {'year': 1938, 'return': 0.3298}, {'year': 1939, 'return': -0.0110},
  {'year': 1940, 'return': -0.1131}, {'year': 1941, 'return': -0.2062}, {'year': 1942, 'return': 0.1235},
  {'year': 1943, 'return': 0.2285}, {'year': 1944, 'return': 0.1764}, {'year': 1945, 'return': 0.3392},
  {'year': 1946, 'return': -0.1982}, {'year': 1947, 'return': -0.0333}, {'year': 1948, 'return': 0.0274},
  {'year': 1949, 'return': 0.2036}, {'year': 1950, 'return': 0.2435}, {'year': 1951, 'return': 0.1542},
  {'year': 1952, 'return': 0.1739}, {'year': 1953, 'return': -0.0163}, {'year': 1954, 'return': 0.5362},
  {'year': 1955, 'return': 0.3096}, {'year': 1956, 'return': 0.0354}, {'year': 1957, 'return': -0.1349},
  {'year': 1958, 'return': 0.4137}, {'year': 1959, 'return': 0.1037}, {'year': 1960, 'return': -0.0125},
  {'year': 1961, 'return': 0.2605}, {'year': 1962, 'return': -0.0991}, {'year': 1963, 'return': 0.2109},
  {'year': 1964, 'return': 0.1524}, {'year': 1965, 'return': 0.1026}, {'year': 1966, 'return': -0.1272},
  {'year': 1967, 'return': 0.2015}, {'year': 1968, 'return': 0.0582}, {'year': 1969, 'return': -0.1360},
  {'year': 1970, 'return': -0.0190}, {'year': 1971, 'return': 0.1061}, {'year': 1972, 'return': 0.1484},
  {'year': 1973, 'return': -0.2117}, {'year': 1974, 'return': -0.3404}, {'year': 1975, 'return': 0.2811},
  {'year': 1976, 'return': 0.1809}, {'year': 1977, 'return': -0.1282}, {'year': 1978, 'return': -0.0230},
  {'year': 1979, 'return': 0.0461}, {'year': 1980, 'return': 0.1708}, {'year': 1981, 'return': -0.1251},
  {'year': 1982, 'return': 0.1652}, {'year': 1983, 'return': 0.1822}, {'year': 1984, 'return': 0.0226},
  {'year': 1985, 'return': 0.2737}, {'year': 1986, 'return': 0.1741}, {'year': 1987, 'return': 0.0083},
  {'year': 1988, 'return': 0.1205}, {'year': 1989, 'return': 0.2646}, {'year': 1990, 'return': -0.0927},
  {'year': 1991, 'return': 0.2699}, {'year': 1992, 'return': 0.0459}, {'year': 1993, 'return': 0.0718},
  {'year': 1994, 'return': -0.0135}, {'year': 1995, 'return': 0.3456}, {'year': 1996, 'return': 0.1917},
  {'year': 1997, 'return': 0.3113}, {'year': 1998, 'return': 0.2696}, {'year': 1999, 'return': 0.1827},
  {'year': 2000, 'return': -0.1224}, {'year': 2001, 'return': -0.1332}, {'year': 2002, 'return': -0.2384},
  {'year': 2003, 'return': 0.2649}, {'year': 2004, 'return': 0.0738}, {'year': 2005, 'return': 0.0142},
  {'year': 2006, 'return': 0.1306}, {'year': 2007, 'return': 0.0139}, {'year': 2008, 'return': -0.3711},
  {'year': 2009, 'return': 0.2325}, {'year': 2010, 'return': 0.1348}, {'year': 2011, 'return': -0.0094},
  {'year': 2012, 'return': 0.1396}, {'year': 2013, 'return': 0.3069}, {'year': 2014, 'return': 0.1287},
  {'year': 2015, 'return': 0.0065}, {'year': 2016, 'return': 0.0984}, {'year': 2017, 'return': 0.1925},
  {'year': 2018, 'return': -0.0655}, {'year': 2019, 'return': 0.2882}, {'year': 2020, 'return': 0.1644},
  {'year': 2021, 'return': 0.2002}, {'year': 2022, 'return': -0.2301}, {'year': 2023, 'return': 0.2197}
]

df_hist = pd.DataFrame(data)
GEO_MEAN = 0.067 # Long term geometric mean

# --- CUSTOM CSS FOR PURPLE THEME ---
st.markdown("""
    <style>
    .stApp {
        background-color: #F8FAFC;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 2px solid #E9D5FF;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .st-emotion-cache-1wivap2 {
        color: #6B21A8; 
    }
    h1, h2, h3 {
        color: #581C87 !important;
    }
    .highlight-card {
        background-color: #F3E8FF;
        border: 1px solid #D8B4FE;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: #581C87;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("⚙️ Parameters")
    
    initial_wealth = st.number_input(
        "Initial Portfolio ($)", 
        value=1000000, 
        step=50000,
        format="%d"
    )
    
    withdrawal_rate = st.slider(
        "Annual Withdrawal Rate (%)", 
        min_value=2.0, 
        max_value=8.0, 
        value=4.0, 
        step=0.1
    )
    
    duration = st.slider(
        "Duration (Years)", 
        min_value=15, 
        max_value=60, 
        value=25, 
        step=5
    )
    
    annual_income = initial_wealth * (withdrawal_rate / 100)
    st.info(f"**Annual Income:** ${annual_income:,.0f} (Inflation Adjusted)")
    
    st.markdown("---")
    st.markdown("### How to read this tool")
    st.markdown("""
    * **Dashed Line:** What happens if you get the "average" return every year.
    * **Colored Lines:** What actually happened in history depending on start year.
    """)

# --- CALCULATIONS ---
@st.cache_data
def run_simulation(wealth, rate, yrs):
    w_amount = wealth * (rate / 100)
    
    # 1. Average Path
    avg_path = []
    curr = wealth
    for i in range(yrs + 1):
        avg_path.append(curr)
        curr = curr * (1 + GEO_MEAN) - w_amount
        if curr < 0: curr = 0
        
    # 2. Historical Paths
    outcomes = []
    valid_starts = len(df_hist) - yrs
    
    for i in range(valid_starts):
        start_year = df_hist.iloc[i]['year']
        path = []
        curr = wealth
        failed = False
        
        for j in range(yrs + 1):
            path.append(curr)
            if j < yrs:
                ret = df_hist.iloc[i + j]['return']
                curr = curr * (1 + ret) - w_amount
                if curr < 0: 
                    curr = 0
                    failed = True
        
        outcomes.append({
            'start_year': start_year,
            'end_year': start_year + yrs,
            'terminal_wealth': curr,
            'failed': failed,
            'path': path
        })
        
    df_outcomes = pd.DataFrame(outcomes)
    
    # Find Median, Best, Worst
    sorted_outcomes = df_outcomes.sort_values('terminal_wealth')
    median_idx = len(sorted_outcomes) // 2
    
    stats = {
        'avg_path': avg_path,
        'outcomes': outcomes,
        'median_scen': sorted_outcomes.iloc[median_idx],
        'worst_scen': sorted_outcomes.iloc[0],
        'best_scen': sorted_outcomes.iloc[-1],
        'failure_rate': (df_outcomes['failed'].sum() / len(df_outcomes)) * 100,
        'median_terminal': sorted_outcomes.iloc[median_idx]['terminal_wealth'],
        'avg_terminal': avg_path[-1]
    }
    
    return stats

res = run_simulation(initial_wealth, withdrawal_rate, duration)

# --- MAIN CONTENT ---
st.title("Sequence of Returns Risk Analyzer")
st.markdown("""
This dashboard demonstrates why using an "Average Return" assumption is dangerous for retirement planning. 
Even if the long-term average is positive, the **order** of returns matters.
""")

# Key Insight Box
st.markdown(f"""
<div class="highlight-card">
    <h3>ℹ️ Risk of Ruin</h3>
    <p>The typical (median) retiree actually finished <b>better</b> (${res['median_terminal']:,.0f}) than the long-term average model predicted (${res['avg_terminal']:,.0f}).</p>
    <hr style="border-color: #D8B4FE;">
    <p><b>However, this creates a false sense of security.</b> Despite good typical returns, <b>{res['failure_rate']:.1f}%</b> of retirees still ran out of money completely due to bad timing (Sequence Risk).</p>
</div>
""", unsafe_allow_html=True)

# Metrics Row
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Historical Failure Rate", f"{res['failure_rate']:.1f}%", help="Percentage of periods that ran out of money")
with c2:
    st.metric("Median Ending Wealth", f"${res['median_terminal']:,.0f}", help="The 'typical' outcome")
with c3:
    st.metric("Average 'Illusion' End", f"${res['avg_terminal']:,.0f}", help="If returns were a constant 6.7%")

# Tabs for Charts
tab1, tab2 = st.tabs(["📈 Portfolio Trajectories", "📊 Outcomes by Start Year"])

with tab1:
    # Prepare Data for Plotly
    years = list(range(duration + 1))
    
    fig = go.Figure()
    
    # Average Line (Dashed)
    fig.add_trace(go.Scatter(
        x=years, y=res['avg_path'],
        mode='lines',
        name='Assumed Average (6.7%)',
        line=dict(color='gray', width=3, dash='dash')
    ))
    
    # Best Case
    fig.add_trace(go.Scatter(
        x=years, y=res['best_scen']['path'],
        mode='lines',
        name=f"Best Start ({res['best_scen']['start_year']})",
        line=dict(color='#10B981', width=1),
        opacity=0.6
    ))
    
    # Worst Case
    fig.add_trace(go.Scatter(
        x=years, y=res['worst_scen']['path'],
        mode='lines',
        name=f"Worst Start ({res['worst_scen']['start_year']})",
        line=dict(color='#EF4444', width=3)
    ))
    
    # Median Case
    fig.add_trace(go.Scatter(
        x=years, y=res['median_scen']['path'],
        mode='lines',
        name='Median Historical',
        line=dict(color='#9333EA', width=4)
    ))
    
    fig.update_layout(
        title=f"Portfolio Trajectory: Real Values over {duration} Years",
        xaxis_title="Years into Retirement",
        yaxis_title="Portfolio Value ($)",
        template="plotly_white",
        height=500,
        hovermode="x unified"
    )
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Bar Chart for Outcomes
    df_bar = pd.DataFrame(res['outcomes'])
    
    # Color logic
    colors = []
    for val in df_bar['terminal_wealth']:
        if val == 0:
            colors.append('#EF4444') # Red (Fail)
        elif val < initial_wealth:
            colors.append('#F59E0B') # Amber (Loss)
        else:
            colors.append('#9333EA') # Purple (Gain)
            
    fig_bar = go.Figure(data=[go.Bar(
        x=df_bar['start_year'],
        y=df_bar['terminal_wealth'],
        marker_color=colors
    )])
    
    fig_bar.update_layout(
        title=f"Ending Wealth by Start Year (Duration: {duration} Years)",
        xaxis_title="Start Year",
        yaxis_title="Ending Wealth ($)",
        template="plotly_white",
        height=500
    )
    
    # Add Initial Wealth Line
    fig_bar.add_hline(y=initial_wealth, line_dash="dash", line_color="gray", annotation_text="Initial Principal")
    
    st.plotly_chart(fig_bar, use_container_width=True)