import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. 配置页面 (Silicon Valley Minimalist Style)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Berkshire Portfolio | 2000-2025",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS以实现更干净的界面
st.markdown("""
<style>
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    h1 {font-family: 'Helvetica Neue', sans-serif; font-weight: 700; letter-spacing: -1px;}
    h2 {font-family: 'Helvetica Neue', sans-serif; font-weight: 600; letter-spacing: -0.5px; color: #333;}
    .stMetric {background-color: #f9f9f9; padding: 10px; border-radius: 5px; border: 1px solid #eee;}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 数据准备 (内置全量清洗后的数据)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    # 行业映射
    sector_map = {
        'AAPL': 'Technology', 'IBM': 'Technology', 'HPQ': 'Technology', 'SNOW': 'Technology', 'GOOGL': 'Technology', 'VRSN': 'Technology', 'ATVI': 'Technology',
        'BAC': 'Financials', 'AXP': 'Financials', 'WFC': 'Financials', 'USB': 'Financials', 'C': 'Financials', 'JPM': 'Financials', 'MCO': 'Financials', 'BK': 'Financials', 'CB': 'Financials', 'MA': 'Financials', 'V': 'Financials', 'WSC': 'Financials', 'MTB': 'Financials',
        'KO': 'Consumer Staples', 'KHC': 'Consumer Staples', 'KFT': 'Consumer Staples', 'PG': 'Consumer Staples', 'WMT': 'Consumer Staples', 'KR': 'Consumer Staples', 'COST': 'Consumer Staples', 'BUD': 'Consumer Staples',
        'G': 'Consumer Discretionary', 'WPO': 'Comm/Media', 'DPZ': 'Consumer Discretionary', 'DIS': 'Comm/Media', 'CHTR': 'Comm/Media', 'PARA': 'Comm/Media', 'VZ': 'Comm/Media',
        'CVX': 'Energy', 'OXY': 'Energy', 'XOM': 'Energy', 'COP': 'Energy', 'PSX': 'Energy',
        'BNI': 'Industrials', 'DAL': 'Industrials', 'LUV': 'Industrials', 'UAL': 'Industrials', 'AAL': 'Industrials', 'POOL': 'Consumer Discretionary',
        'DVA': 'Healthcare', 'JNJ': 'Healthcare', 'ABBV': 'Healthcare', 'MRK': 'Healthcare',
        'HRB': 'Consumer Discretionary'
    }

    # 原始数据列表 (使用简化值，单位为十亿，以便在代码中减少字符数)
    # 格式: ('Quarter', 'Ticker', Shares (M), Value ($B), 'Percent')
    raw_data = [
        ('2025 Q3', 'AAPL', 238.0, 60.6, 22.7), ('2025 Q3', 'AXP', 151.6, 50.3, 18.8), ('2025 Q3', 'BAC', 568.3, 29.3, 11.0), ('2025 Q3', 'KO', 400.0, 26.5, 9.9), ('2025 Q3', 'CVX', 122.1, 18.9, 7.1), ('2025 Q3', 'OXY', 265.3, 13.0, 4.9), ('2025 Q3', 'MCO', 24.7, 11.0, 4.1), ('2025 Q3', 'KHC', 325.6, 10.5, 3.9), ('2025 Q3', 'CB', 31.3, 8.8, 3.3), ('2025 Q3', 'GOOGL', 17.8, 4.3, 1.6), ('2025 Q3', 'DVA', 32.2, 4.2, 1.6), ('2025 Q3', 'KR', 50.0, 2.8, 1.0), ('2025 Q3', 'DPZ', 3.0, 1.3, 0.5), ('2025 Q3', 'POOL', 3.5, 1.1, 0.4),
        ('2024 Q4', 'AAPL', 300.0, 69.9, 25.0), ('2024 Q4', 'AXP', 151.6, 48.2, 17.3), ('2024 Q4', 'BAC', 700.0, 31.5, 11.3), ('2024 Q4', 'KO', 400.0, 25.2, 9.0), ('2024 Q4', 'CVX', 118.6, 18.3, 6.5), ('2024 Q4', 'OXY', 255.0, 14.8, 5.3), ('2024 Q4', 'KHC', 325.6, 11.1, 3.9), ('2024 Q4', 'MCO', 24.7, 10.6, 3.8), ('2024 Q4', 'CB', 27.0, 7.6, 2.7), ('2024 Q4', 'DVA', 36.1, 4.5, 1.6), ('2024 Q4', 'C', 55.2, 3.5, 1.2), ('2024 Q4', 'KR', 50.0, 2.7, 0.9),
        ('2023 Q4', 'AAPL', 905.6, 174.3, 50.1), ('2023 Q4', 'BAC', 1032.9, 34.8, 10.0), ('2023 Q4', 'AXP', 151.6, 28.4, 8.2), ('2023 Q4', 'KO', 400.0, 23.6, 6.8), ('2023 Q4', 'CVX', 126.1, 18.8, 5.4), ('2023 Q4', 'OXY', 248.0, 14.8, 4.3), ('2023 Q4', 'KHC', 325.6, 12.0, 3.5), ('2023 Q4', 'MCO', 24.7, 9.6, 2.8),
        ('2022 Q4', 'AAPL', 895.1, 116.3, 38.9), ('2022 Q4', 'BAC', 1010.1, 33.5, 11.2), ('2022 Q4', 'CVX', 163.0, 29.3, 9.8), ('2022 Q4', 'KO', 400.0, 25.4, 8.5), ('2022 Q4', 'AXP', 151.6, 22.4, 7.5), ('2022 Q4', 'KHC', 325.6, 13.3, 4.4), ('2022 Q4', 'OXY', 194.4, 12.2, 4.1), ('2022 Q4', 'MCO', 24.7, 6.9, 2.3),
        ('2021 Q4', 'AAPL', 887.1, 157.5, 47.6), ('2021 Q4', 'BAC', 1010.1, 44.9, 13.6), ('2021 Q4', 'AXP', 151.6, 24.8, 7.5), ('2021 Q4', 'KO', 400.0, 23.7, 7.2), ('2021 Q4', 'KHC', 325.6, 11.7, 3.5), ('2021 Q4', 'MCO', 24.7, 9.6, 2.9), ('2021 Q4', 'VZ', 158.8, 8.3, 2.5),
        ('2020 Q4', 'AAPL', 887.1, 117.7, 43.6), ('2020 Q4', 'BAC', 1010.1, 30.6, 11.3), ('2020 Q4', 'KO', 400.0, 21.9, 8.1), ('2020 Q4', 'AXP', 151.6, 18.3, 6.8), ('2020 Q4', 'VZ', 146.7, 8.6, 3.2), ('2020 Q4', 'KHC', 325.6, 11.3, 4.2), ('2020 Q4', 'MCO', 24.7, 7.2, 2.7), ('2020 Q4', 'USB', 131.1, 6.1, 2.3),
        ('2019 Q4', 'AAPL', 245.2, 72.0, 29.7), ('2019 Q4', 'BAC', 925.0, 32.6, 13.5), ('2019 Q4', 'KO', 400.0, 22.1, 9.2), ('2019 Q4', 'AXP', 151.6, 18.9, 7.8), ('2019 Q4', 'WFC', 323.2, 17.4, 7.2), ('2019 Q4', 'KHC', 325.6, 10.5, 4.3), ('2019 Q4', 'JPM', 59.5, 8.3, 3.4),
        ('2015 Q4', 'WFC', 479.7, 26.1, 19.8), ('2015 Q4', 'KHC', 325.6, 23.7, 17.9), ('2015 Q4', 'KO', 400.0, 17.2, 13.0), ('2015 Q4', 'IBM', 81.0, 11.2, 8.4), ('2015 Q4', 'AXP', 151.6, 10.5, 8.0), ('2015 Q4', 'PSX', 61.5, 4.9, 3.7), ('2015 Q4', 'PG', 52.8, 4.2, 3.2),
        ('2010 Q4', 'KO', 200.0, 13.2, 25.0), ('2010 Q4', 'WFC', 342.6, 10.6, 20.2), ('2010 Q4', 'AXP', 151.6, 6.5, 12.4), ('2010 Q4', 'PG', 76.1, 4.9, 9.3), ('2010 Q4', 'KFT', 105.2, 3.3, 6.3), ('2010 Q4', 'JNJ', 42.6, 2.6, 5.0),
        ('2005 Q4', 'AXP', 151.6, 7.8, 16.8), ('2005 Q4', 'KO', 200.0, 8.1, 17.3), ('2005 Q4', 'PG', 96.3, 5.6, 12.0), ('2005 Q4', 'WFC', 56.4, 3.5, 7.6), ('2005 Q4', 'MCO', 48.0, 3.0, 6.4), ('2005 Q4', 'WSC', 5.7, 2.1, 4.6), ('2005 Q4', 'WPO', 1.7, 1.3, 2.8),
        ('2000 Q4', 'KO', 200.0, 12.2, 31.5), ('2000 Q4', 'AXP', 151.6, 8.3, 21.6), ('2000 Q4', 'G', 96.0, 3.5, 8.9), ('2000 Q4', 'WFC', 23.7, 2.7, 6.9), ('2000 Q4', 'WSC', 5.7, 1.7, 4.3), ('2000 Q4', 'WPO', 1.7, 1.0, 2.6)
    ]

    # DataFrame 初始化
    df = pd.DataFrame(raw_data, columns=['Quarter', 'Ticker', 'Shares_Millions', 'Value_Billions', 'Percent_Portfolio'])
    
    # 将季度字符串转换为日期对象
    def parse_quarter(q_str):
        year, q = q_str.split(' ')
        if q == 'Q1': return f"{year}-03-31"
        if q == 'Q2': return f"{year}-06-30"
        if q == 'Q3': return f"{year}-09-30"
        if q == 'Q4': return f"{year}-12-31"
    
    df['Date'] = pd.to_datetime(df['Quarter'].apply(parse_quarter))
    df['Sector'] = df['Ticker'].map(sector_map).fillna('Others')
    
    # 排序
    df = df.sort_values(by=['Date', 'Value_Billions'], ascending=[True, False])
    return df

df = load_data()

# -----------------------------------------------------------------------------
# 3. Sidebar 控制区
# -----------------------------------------------------------------------------
st.sidebar.header("⚙️ Controls")

# 时间线滑块 (新增部分)
min_date = df['Date'].min().to_pydatetime()
max_date = df['Date'].max().to_pydatetime()

date_range = st.sidebar.slider(
    "⏳ Select Time Period",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM"
)
start_date, end_date = date_range

# 行业筛选器 (沿用部分)
all_sectors = sorted(df['Sector'].unique())
selected_sectors = st.sidebar.multiselect("🏷️ Filter by Sector", all_sectors, default=all_sectors)

# 公司筛选器 (沿用部分)
all_tickers = sorted(df['Ticker'].unique())
selected_tickers = st.sidebar.multiselect("🔍 Highlight Specific Stocks", all_tickers, default=[])

# -----------------------------------------------------------------------------
# 4. 数据筛选应用
# -----------------------------------------------------------------------------
# 1. 行业筛选
filtered_df = df[df['Sector'].isin(selected_sectors)]

# 2. 时间筛选
filtered_df = filtered_df[
    (filtered_df['Date'] >= start_date) & 
    (filtered_df['Date'] <= end_date)
]

# -----------------------------------------------------------------------------
# 5. 主内容区
# -----------------------------------------------------------------------------
st.title("Berkshire Hathaway Portfolio Evolution")
st.caption("A 25-year interactive visualization of Warren Buffett's investment strategy (2000-2025).")

# --- Key Metrics (Top Row) ---
# 确保在筛选后仍然有数据
if not filtered_df.empty:
    latest_date_filtered = filtered_df['Date'].max()
    latest_data_filtered = filtered_df[filtered_df['Date'] == latest_date_filtered]
    top_holding = latest_data_filtered.iloc[0]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Start Period", start_date.strftime("%Y Q%q"))
    with col2:
        st.metric("End Period", end_date.strftime("%Y Q%q"))
    with col3:
        st.metric("Top Holding", top_holding['Ticker'], f"{top_holding['Percent_Portfolio']}%")
    with col4:
        st.metric("Top Sector", latest_data_filtered.groupby('Sector')['Value_Billions'].sum().idxmax())
else:
    st.warning("No data found for the selected time and sector filters.")
    st.stop()


st.markdown("---")

# -----------------------------------------------------------------------------
# 6. 可视化 Tab 页
# -----------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Portfolio Composition", "📈 Stock Deep Dive", "🧩 Sector Shift"])

# --- Tab 1: 组合构成 (Macro) ---
with tab1:
    st.subheader("Evolution of Top Holdings (Value & Proportion)")
    
    # 图表 1: 堆叠面积图 (估值绝对值)
    fig_area = px.area(
        filtered_df, 
        x="Date", 
        y="Value_Billions", 
        color="Ticker",
        title="Portfolio Value by Stock (Top Holdings Only)",
        labels={"Value_Billions": "Value ($ Billions)"},
        template="plotly_white",
        hover_data={"Date": "|%Y-%m-%d"}
    )
    fig_area.update_layout(showlegend=True, height=500)
    st.plotly_chart(fig_area, use_container_width=True)
    
    # 图表 2: 100% 堆叠条形图 (比例变化)
    st.subheader("Proportional Changes Over Time")
    fig_bar = px.bar(
        filtered_df, 
        x="Quarter", 
        y="Percent_Portfolio", 
        color="Ticker",
        title="Relative Portfolio Weight %",
        barmode="relative",
        template="plotly_white"
    )
    fig_bar.update_layout(xaxis={'categoryorder':'category ascending'}, height=500)
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Tab 2: 单个股票深度分析 (Micro) ---
with tab2:
    st.subheader("Single Stock Analysis")
    
    stock_options_filtered = sorted(filtered_df['Ticker'].unique())
    target_stock = st.selectbox("Select a Company to Analyze", stock_options_filtered, index=0)
    
    stock_data = filtered_df[filtered_df['Ticker'] == target_stock].sort_values('Date')
    
    c1, c2 = st.columns(2)
    
    with c1:
        # 持仓市值变化
        fig_stock_val = px.line(
            stock_data, x='Date', y='Value_Billions', markers=True,
            title=f"{target_stock}: Market Value History ($B)",
            color_discrete_sequence=['#2E86C1']
        )
        fig_stock_val.update_yaxes(rangemode="tozero")
        st.plotly_chart(fig_stock_val, use_container_width=True)
        
    with c2:
        # 持仓股数变化
        fig_stock_share = px.line(
            stock_data, x='Date', y='Shares_Millions', markers=True,
            title=f"{target_stock}: Shares Held History (Millions)",
            color_discrete_sequence=['#E74C3C']
        )
        fig_stock_share.update_yaxes(rangemode="tozero")
        st.plotly_chart(fig_stock_share, use_container_width=True)
        
    # 对比视图
    st.divider()
    st.subheader("Comparison Tool")
    compare_stocks = st.multiselect("Compare Holdings (Value)", stock_options_filtered, default=[target_stock])
    if compare_stocks:
        compare_data = filtered_df[filtered_df['Ticker'].isin(compare_stocks)]
        fig_compare = px.line(
            compare_data, x="Date", y="Value_Billions", color="Ticker",
            title="Holdings Value Comparison", markers=True
        )
        st.plotly_chart(fig_compare, use_container_width=True)

# --- Tab 3: 行业变迁 (Trends) ---
with tab3:
    st.subheader("Strategic Shift by Sector")
    
    # 聚合行业数据
    sector_data = filtered_df.groupby(['Date', 'Quarter', 'Sector'])['Value_Billions'].sum().reset_index()
    
    fig_sector = px.area(
        sector_data, x="Date", y="Value_Billions", color="Sector",
        title="Portfolio Value Composition by Sector",
        template="plotly_white",
    )
    st.plotly_chart(fig_sector, use_container_width=True)
    
    # 行业饼图 (最新)
    latest_sector_data = sector_data[sector_data['Date'] == latest_date_filtered]
    fig_pie = px.pie(
        latest_sector_data, values='Value_Billions', names='Sector',
        title=f"Sector Allocation ({latest_date_filtered.strftime('%Y Q%q')})",
        hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("Designed with Streamlit & Plotly | Data based on Berkshire Hathaway 13F Filings (Top Holdings Only)")
