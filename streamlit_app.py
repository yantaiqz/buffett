import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    # 为了演示，直接构建DataFrame。实际项目中可读取CSV。
    # 这里映射了核心股票的行业，用于第三个维度的分析
    sector_map = {
        'AAPL': 'Technology', 'IBM': 'Technology', 'HPQ': 'Technology', 'SNOW': 'Technology', 'GOOGL': 'Technology', 'VRSN': 'Technology', 'ATVI': 'Technology',
        'BAC': 'Financials', 'AXP': 'Financials', 'WFC': 'Financials', 'USB': 'Financials', 'JPM': 'Financials', 'MCO': 'Financials', 'BK': 'Financials', 'GS': 'Financials', 'C': 'Financials', 'CB': 'Financials', 'MA': 'Financials', 'V': 'Financials', 'WSC': 'Financials', 'MTB': 'Financials',
        'KO': 'Consumer Staples', 'KHC': 'Consumer Staples', 'KFT': 'Consumer Staples', 'PG': 'Consumer Staples', 'WMT': 'Consumer Staples', 'KR': 'Consumer Staples', 'COST': 'Consumer Staples', 'BUD': 'Consumer Staples',
        'G': 'Consumer Discretionary', 'WPO': 'Comm/Media', 'DPZ': 'Consumer Discretionary', 'DIS': 'Comm/Media', 'CHTR': 'Comm/Media', 'PARA': 'Comm/Media', 'VZ': 'Comm/Media',
        'CVX': 'Energy', 'OXY': 'Energy', 'XOM': 'Energy', 'COP': 'Energy', 'PSX': 'Energy',
        'BNI': 'Industrials', 'DAL': 'Industrials', 'LUV': 'Industrials', 'UAL': 'Industrials', 'AAL': 'Industrials', 'POOL': 'Consumer Discretionary',
        'DVA': 'Healthcare', 'JNJ': 'Healthcare', 'ABBV': 'Healthcare', 'MRK': 'Healthcare',
        'HRB': 'Consumer Discretionary'
    }

    # 原始数据列表 (基于之前整理的表格)
    raw_data = [
        # 2025 Q3
        ('2025 Q3', 'AAPL', 238000000, 60600, 22.7), ('2025 Q3', 'AXP', 151610700, 50300, 18.8), ('2025 Q3', 'BAC', 568334000, 29300, 11.0), ('2025 Q3', 'KO', 400000000, 26500, 9.9), ('2025 Q3', 'CVX', 122144000, 18900, 7.1), ('2025 Q3', 'OXY', 265321000, 13000, 4.9), ('2025 Q3', 'MCO', 24669778, 11000, 4.1), ('2025 Q3', 'KHC', 325634818, 10500, 3.9), ('2025 Q3', 'CB', 31330000, 8800, 3.3), ('2025 Q3', 'GOOGL', 17840000, 4300, 1.6), ('2025 Q3', 'DVA', 32160000, 4200, 1.6), ('2025 Q3', 'KR', 50000000, 2800, 1.0), ('2025 Q3', 'DPZ', 2980000, 1300, 0.5), ('2025 Q3', 'POOL', 3450000, 1100, 0.4),
        # 2024 Q4
        ('2024 Q4', 'AAPL', 300000000, 69900, 25.0), ('2024 Q4', 'AXP', 151610700, 48200, 17.3), ('2024 Q4', 'BAC', 700000000, 31500, 11.3), ('2024 Q4', 'KO', 400000000, 25200, 9.0), ('2024 Q4', 'CVX', 118600000, 18300, 6.5), ('2024 Q4', 'OXY', 255000000, 14800, 5.3), ('2024 Q4', 'KHC', 325634818, 11100, 3.9), ('2024 Q4', 'MCO', 24669778, 10600, 3.8), ('2024 Q4', 'CB', 27000000, 7600, 2.7), ('2024 Q4', 'DVA', 36095570, 4500, 1.6), ('2024 Q4', 'C', 55244797, 3500, 1.2), ('2024 Q4', 'KR', 50000000, 2700, 0.9),
        # 2023 Q4
        ('2023 Q4', 'AAPL', 905560000, 174343, 50.1), ('2023 Q4', 'BAC', 1032852006, 34776, 10.0), ('2023 Q4', 'AXP', 151610700, 28386, 8.2), ('2023 Q4', 'KO', 400000000, 23572, 6.8), ('2023 Q4', 'CVX', 126093326, 18808, 5.4), ('2023 Q4', 'OXY', 248018128, 14801, 4.3), ('2023 Q4', 'KHC', 325634818, 12045, 3.5), ('2023 Q4', 'MCO', 24669778, 9635, 2.8),
        # 2022 Q4
        ('2022 Q4', 'AAPL', 895136175, 116305, 38.9), ('2022 Q4', 'BAC', 1010100606, 33454, 11.2), ('2022 Q4', 'CVX', 162975771, 29252, 9.8), ('2022 Q4', 'KO', 400000000, 25444, 8.5), ('2022 Q4', 'AXP', 151610700, 22400, 7.5), ('2022 Q4', 'KHC', 325634818, 13256, 4.4), ('2022 Q4', 'OXY', 194351650, 12242, 4.1), ('2022 Q4', 'MCO', 24669778, 6868, 2.3), ('2022 Q4', 'ATVI', 52717075, 4035, 1.3),
        # 2021 Q4
        ('2021 Q4', 'AAPL', 887135554, 157529, 47.6), ('2021 Q4', 'BAC', 1010100606, 44939, 13.6), ('2021 Q4', 'AXP', 151610700, 24804, 7.5), ('2021 Q4', 'KO', 400000000, 23684, 7.2), ('2021 Q4', 'KHC', 325634818, 11690, 3.5), ('2021 Q4', 'MCO', 24669778, 9636, 2.9), ('2021 Q4', 'VZ', 158824575, 8253, 2.5),
        # 2020 Q4
        ('2020 Q4', 'AAPL', 887135554, 117708, 43.6), ('2020 Q4', 'BAC', 1010100606, 30606, 11.3), ('2020 Q4', 'KO', 400000000, 21936, 8.1), ('2020 Q4', 'AXP', 151610700, 18331, 6.8), ('2020 Q4', 'VZ', 146716496, 8615, 3.2), ('2020 Q4', 'KHC', 325634818, 11296, 4.2), ('2020 Q4', 'MCO', 24669778, 7160, 2.7), ('2020 Q4', 'USB', 131071284, 6105, 2.3),
        # 2019 Q4
        ('2019 Q4', 'AAPL', 245155566, 71987, 29.7), ('2019 Q4', 'BAC', 925008600, 32560, 13.5), ('2019 Q4', 'KO', 400000000, 22140, 9.2), ('2019 Q4', 'AXP', 151610700, 18874, 7.8), ('2019 Q4', 'WFC', 323212918, 17388, 7.2), ('2019 Q4', 'KHC', 325634818, 10452, 4.3), ('2019 Q4', 'JPM', 59514932, 8296, 3.4),
        # 2015 Q4
        ('2015 Q4', 'WFC', 479704270, 26076, 19.8), ('2015 Q4', 'KHC', 325634818, 23693, 17.9), ('2015 Q4', 'KO', 400000000, 17184, 13.0), ('2015 Q4', 'IBM', 81033450, 11150, 8.4), ('2015 Q4', 'AXP', 151610700, 10544, 8.0), ('2015 Q4', 'PSX', 61487210, 4906, 3.7), ('2015 Q4', 'PG', 52793078, 4191, 3.2),
        # 2010 Q4
        ('2010 Q4', 'KO', 200000000, 13154, 25.0), ('2010 Q4', 'WFC', 342623800, 10617, 20.2), ('2010 Q4', 'AXP', 151610700, 6507, 12.4), ('2010 Q4', 'PG', 76056000, 4892, 9.3), ('2010 Q4', 'KFT', 105214580, 3315, 6.3), ('2010 Q4', 'JNJ', 42620000, 2636, 5.0),
        # 2005 Q4
        ('2005 Q4', 'AXP', 151610700, 7818, 16.8), ('2005 Q4', 'KO', 200000000, 8064, 17.3), ('2005 Q4', 'PG', 96300000, 5573, 12.0), ('2005 Q4', 'WFC', 56448380, 3546, 7.6), ('2005 Q4', 'MCO', 48000000, 2985, 6.4), ('2005 Q4', 'WSC', 5703087, 2144, 4.6), ('2005 Q4', 'WPO', 1727765, 1308, 2.8),
        # 2000 Q4
        ('2000 Q4', 'KO', 200000000, 12188, 31.5), ('2000 Q4', 'AXP', 151610700, 8332, 21.6), ('2000 Q4', 'G', 96000000, 3456, 8.9), ('2000 Q4', 'WFC', 23733198, 2669, 6.9), ('2000 Q4', 'WSC', 5703087, 1650, 4.3), ('2000 Q4', 'WPO', 1727765, 993, 2.6)
    ]

    df = pd.DataFrame(raw_data, columns=['Quarter', 'Ticker', 'Shares', 'Value_Millions', 'Percent_Portfolio'])
    
    # 数据清洗：将 Quarter 转换为更易排序的格式 (YYYY-MM-DD approx)
    def parse_quarter(q_str):
        year, q = q_str.split(' ')
        if q == 'Q1': return f"{year}-03-31"
        if q == 'Q2': return f"{year}-06-30"
        if q == 'Q3': return f"{year}-09-30"
        if q == 'Q4': return f"{year}-12-31"
    
    df['Date'] = pd.to_datetime(df['Quarter'].apply(parse_quarter))
    df['Value_Billions'] = df['Value_Millions'] / 1000  # 转换为十亿美元
    df['Sector'] = df['Ticker'].map(sector_map).fillna('Others')
    
    # 排序
    df = df.sort_values(by=['Date', 'Value_Billions'], ascending=[True, False])
    return df

df = load_data()

# -----------------------------------------------------------------------------
# 3. Sidebar 控制区
# -----------------------------------------------------------------------------
st.sidebar.header("⚙️ Controls")

# 行业筛选器
all_sectors = sorted(df['Sector'].unique())
selected_sectors = st.sidebar.multiselect("Filter by Sector", all_sectors, default=all_sectors)

# 公司筛选器
all_tickers = sorted(df['Ticker'].unique())
selected_tickers = st.sidebar.multiselect("Highlight Specific Stocks", all_tickers, default=[])

# 过滤数据
if selected_sectors:
    filtered_df = df[df['Sector'].isin(selected_sectors)]
else:
    filtered_df = df

# -----------------------------------------------------------------------------
# 4. 主内容区
# -----------------------------------------------------------------------------

st.title("Berkshire Hathaway Portfolio Evolution")
st.caption("A 25-year interactive visualization of Warren Buffett's investment strategy (2000-2025).")

# --- Key Metrics (Top Row) ---
latest_date = df['Date'].max()
latest_data = df[df['Date'] == latest_date]
top_holding = latest_data.iloc[0]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Latest Snapshot", "2025 Q3")
with col2:
    st.metric("Top Holding", top_holding['Ticker'], f"{top_holding['Percent_Portfolio']}%")
with col3:
    st.metric("Top Sector", latest_data.groupby('Sector')['Value_Billions'].sum().idxmax())
with col4:
    st.metric("Cash Position (Est.)", "$380B+", "Record High")

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. 可视化 Tab 页
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
    fig_area.update_layout(showlegend=False, height=500)
    st.plotly_chart(fig_area, use_container_width=True)
    
    # 图表 2: 100% 堆叠条形图 (比例变化)
    st.subheader("Proportional Changes Over Time")
    fig_bar = px.bar(
        filtered_df, 
        x="Quarter", 
        y="Percent_Portfolio", 
        color="Ticker",
        title="Relative Portfolio Weight %",
        barmode="relative", # stack
        template="plotly_white"
    )
    fig_bar.update_layout(xaxis={'categoryorder':'category ascending'}, height=500)
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Tab 2: 单个股票深度分析 (Micro) ---
with tab2:
    st.subheader("Single Stock Analysis")
    
    stock_options = df['Ticker'].unique()
    target_stock = st.selectbox("Select a Company to Analyze", stock_options, index=list(stock_options).index('AAPL'))
    
    stock_data = df[df['Ticker'] == target_stock].sort_values('Date')
    
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
            stock_data, x='Date', y='Shares', markers=True,
            title=f"{target_stock}: Shares Held History",
            color_discrete_sequence=['#E74C3C']
        )
        fig_stock_share.update_yaxes(rangemode="tozero")
        st.plotly_chart(fig_stock_share, use_container_width=True)
        
    # 对比视图
    st.divider()
    st.subheader("Comparison Tool")
    compare_stocks = st.multiselect("Compare Holdings (Value)", all_tickers, default=['KO', 'BAC', 'AAPL'])
    if compare_stocks:
        compare_data = df[df['Ticker'].isin(compare_stocks)]
        fig_compare = px.line(
            compare_data, x="Date", y="Value_Billions", color="Ticker",
            title="Holdings Value Comparison", markers=True
        )
        st.plotly_chart(fig_compare, use_container_width=True)

# --- Tab 3: 行业变迁 (Trends) ---
with tab3:
    st.subheader("Strategic Shift by Sector")
    st.markdown("""
    * **2000-2010:** 消费 (KO, G) 与 金融 (WFC, AXP) 占主导。
    * **2011-2015:** 尝试转型科技 (IBM) 失败。
    * **2016-2023:** 科技 (AAPL) 崛起成为绝对核心。
    * **2024-2025:** 转向能源 (CVX, OXY) 与防御性现金。
    """)
    
    # 聚合行业数据
    sector_data = df.groupby(['Date', 'Quarter', 'Sector'])['Value_Billions'].sum().reset_index()
    
    fig_sector = px.area(
        sector_data, x="Date", y="Value_Billions", color="Sector",
        title="Portfolio Value Composition by Sector",
        template="plotly_white",
        color_discrete_map={
            'Technology': '#3498DB', # Blue
            'Financials': '#2ECC71', # Green
            'Consumer Staples': '#E74C3C', # Red
            'Energy': '#F1C40F', # Yellow
            'Industrials': '#95A5A6', # Grey
            'Healthcare': '#9B59B6' # Purple
        }
    )
    st.plotly_chart(fig_sector, use_container_width=True)
    
    # 行业饼图 (最新)
    latest_sector = sector_data[sector_data['Date'] == latest_date]
    fig_pie = px.pie(
        latest_sector, values='Value_Billions', names='Sector',
        title=f"Sector Allocation ({latest_date.strftime('%Y Q3')})",
        hole=0.4
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("Designed with Streamlit & Plotly | Data based on Berkshire Hathaway 13F Filings (Top Holdings Only)")
