import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import requests
import base64

# -----------------------------------------------------------------------------
# 新增：将图片URL转换为Base64编码的函数
# -----------------------------------------------------------------------------
def get_base64_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return base64.b64encode(response.content).decode('utf-8')
    except:
        # 若获取失败，使用默认占位符的Base64（30x30蓝色方块）
        default_png = base64.b64encode(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x1e\x00\x00\x00\x1e\x08\x06\x00\x00\x00\x7f\x7b\xfa\x5a\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00\x19tEXtSoftware\x00Adobe ImageReady\x00\x00\x00\x00IDATx\x9c\xec\xdd\x07\x00\x00\x00\x02\x00\x01\x8d\x1f\x10\x00\x00\x00\x00IEND\xaeB`\x82').decode('utf-8')
        return default_png

# -----------------------------------------------------------------------------
# 1. 配置页面 (Silicon Valley Minimalist Style)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Berkshire Portfolio | 2000-2025",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS（新增：调整图例区域的样式）
st.markdown("""
<style>
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    h1 {font-family: 'Helvetica Neue', sans-serif; font-weight: 700; letter-spacing: -1px;}
    h2 {font-family: 'Helvetica Neue', sans-serif; font-weight: 600; letter-spacing: -0.5px; color: #333;}
    .stMetric {background-color: #f9f9f9; padding: 10px; border-radius: 5px; border: 1px solid #eee;}
    
    /* 优化表格中 Logo 的显示 */
    table img {
        border-radius: 5px;
        vertical-align: middle;
        margin-right: 8px;
        width: 30px;
        height: 30px;
    }
    .ref-ticker-col {font-weight: bold; color: #3498DB;}
    
    /* 自定义图例的容器样式（若使用HTML图例） */
    .custom-legend {
        position: absolute;
        top: 20px;
        right: 20px;
        background: white;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
        z-index: 100;
    }
    .legend-item {
        display: flex;
        align-items: center;
        margin-bottom: 5px;
    }
    .legend-item img {
        width: 20px;
        height: 20px;
        margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 数据准备 (内置全量清洗后的数据)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    # 核心映射数据：新增全名映射
    full_name_map = {
        'AAPL': 'Apple Inc.', 'AXP': 'American Express Company', 'BAC': 'Bank of America Corporation', 
        'KO': 'The Coca-Cola Company', 'CVX': 'Chevron Corporation', 'OXY': 'Occidental Petroleum Corporation', 
        'MCO': 'Moody\'s Corporation', 'KHC': 'The Kraft Heinz Company', 'CB': 'Chubb Limited', 
        'GOOGL': 'Alphabet Inc. (Google)', 'DVA': 'DaVita Inc.', 'KR': 'The Kroger Co.', 
        'DPZ': 'Domino\'s Pizza, Inc.', 'POOL': 'Pool Corporation', 'IBM': 'International Business Machines Corp.',
        'WFC': 'Wells Fargo & Company', 'PG': 'The Procter & Gamble Company', 'VZ': 'Verizon Communications Inc.',
        'USB': 'U.S. Bancorp', 'JPM': 'JPMorgan Chase & Co.', 'C': 'Citigroup Inc.', 
        'V': 'Visa Inc.', 'MA': 'Mastercard Incorporated', 'AMZN': 'Amazon.com, Inc.', 
        'ATVI': 'Activision Blizzard', 'HPQ': 'HP Inc.', 'PARA': 'Paramount Global', 
        'WPO': 'The Washington Post Company', 'G': 'The Gillette Company', 'COP': 'ConocoPhillips',
        'KFT': 'Kraft Foods', 'WSC': 'Wesco Financial', 'BNI': 'BNSF Railway Co.', 'PSX': 'Phillips 66',
        'TSM': 'Taiwan Semiconductor (TSM)', 'UNH': 'UnitedHealth Group', 'JNJ': 'Johnson & Johnson',
        'SNOW': 'Snowflake Inc.', 'VRSN': 'VeriSign Inc.', 'BK': 'Bank of New York Mellon Corporation',
        'WMT': 'Walmart Inc.', 'COST': 'Costco Wholesale Corporation', 'BUD': 'Anheuser-Busch InBev SA/NV',
        'DIS': 'The Walt Disney Company', 'CHTR': 'Charter Communications Inc.', 'XOM': 'Exxon Mobil Corporation',
        'DAL': 'Delta Air Lines Inc.', 'LUV': 'Southwest Airlines Co.', 'UAL': 'United Airlines Holdings Inc.',
        'AAL': 'American Airlines Group Inc.', 'ABBV': 'AbbVie Inc.', 'MRK': 'Merck & Co. Inc.',
        'HRB': 'H&R Block Inc.', 'MTB': 'M&T Bank Corporation'
    }
    
    # 行业映射
    sector_map = {
        'AAPL': 'Technology', 'IBM': 'Technology', 'HPQ': 'Technology', 'SNOW': 'Technology', 'GOOGL': 'Technology', 'VRSN': 'Technology', 'ATVI': 'Technology', 'TSM': 'Technology',
        'BAC': 'Financials', 'AXP': 'Financials', 'WFC': 'Financials', 'USB': 'Financials', 'C': 'Financials', 'JPM': 'Financials', 'MCO': 'Financials', 'BK': 'Financials', 'CB': 'Financials', 'MA': 'Financials', 'V': 'Financials', 'WSC': 'Financials', 'MTB': 'Financials',
        'KO': 'Consumer Staples', 'KHC': 'Consumer Staples', 'KFT': 'Consumer Staples', 'PG': 'Consumer Staples', 'WMT': 'Consumer Staples', 'KR': 'Consumer Staples', 'COST': 'Consumer Staples', 'BUD': 'Consumer Staples',
        'G': 'Consumer Discretionary', 'WPO': 'Comm/Media', 'DPZ': 'Consumer Discretionary', 'DIS': 'Comm/Media', 'CHTR': 'Comm/Media', 'PARA': 'Comm/Media', 'VZ': 'Comm/Media', 'POOL': 'Consumer Discretionary', 'HRB': 'Consumer Discretionary',
        'CVX': 'Energy', 'OXY': 'Energy', 'XOM': 'Energy', 'COP': 'Energy', 'PSX': 'Energy',
        'BNI': 'Industrials', 'DAL': 'Industrials', 'LUV': 'Industrials', 'UAL': 'Industrials', 'AAL': 'Industrials',
        'DVA': 'Healthcare', 'JNJ': 'Healthcare', 'ABBV': 'Healthcare', 'MRK': 'Healthcare', 'UNH': 'Healthcare',
    }

    # 使用Google Favicon API获取logo URL，并转换为Base64
    def get_google_logo_info(ticker):
        domain_map = {
            'AAPL': 'apple.com', 'AXP': 'americanexpress.com', 'BAC': 'bankofamerica.com', 'KO': 'coca-colacompany.com', 
            'CVX': 'chevron.com', 'OXY': 'oxy.com', 'MCO': 'moodys.com', 'KHC': 'kraftheinzcompany.com', 'CB': 'chubb.com', 
            'GOOGL': 'google.com', 'DVA': 'davita.com', 'KR': 'kroger.com', 'DPZ': 'dominos.com', 'POOL': 'poolcorp.com', 
            'IBM': 'ibm.com', 'WFC': 'wellsfargo.com', 'PG': 'pg.com', 'VZ': 'verizon.com', 'USB': 'usbank.com', 
            'JPM': 'jpmorganchase.com', 'C': 'citi.com', 'V': 'visa.com', 'MA': 'mastercard.com', 'AMZN': 'amazon.com', 
            'ATVI': 'activisionblizzard.com', 'HPQ': 'hp.com', 'PARA': 'paramount.com', 'WPO': 'washingtonpost.com', 
            'G': 'gillette.com', 'COP': 'conocophillips.com', 'KFT': 'kraftfoods.com', 'WSC': 'wesco.com', 
            'BNI': 'bnsf.com', 'PSX': 'phillips66.com', 'TSM': 'tsmc.com', 'UNH': 'unitedhealthgroup.com', 
            'JNJ': 'jnj.com', 'SNOW': 'snowflake.com', 'VRSN': 'verisign.com', 'BK': 'bnymellon.com', 
            'WMT': 'walmart.com', 'COST': 'costco.com', 'BUD': 'ab-inbev.com', 'DIS': 'disney.com', 
            'CHTR': 'charter.com', 'XOM': 'exxonmobil.com', 'DAL': 'delta.com', 'LUV': 'southwest.com', 
            'UAL': 'united.com', 'AAL': 'aa.com', 'ABBV': 'abbvie.com', 'MRK': 'merck.com', 
            'HRB': 'hrblock.com', 'MTB': 'mtb.com'
        }
        domain = domain_map.get(ticker, 'google.com')
        size = 30
        url = f"https://www.google.com/s2/favicons?domain={domain}&sz={size}"
        b64 = get_base64_from_url(url)
        return url, b64  # 返回URL和Base64编码
    
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
    
    # 数据清洗和映射
    def parse_quarter(q_str):
        year, q = q_str.split(' ')
        if q == 'Q1': return f"{year}-03-31"
        if q == 'Q2': return f"{year}-06-30"
        if q == 'Q3': return f"{year}-09-30"
        if q == 'Q4': return f"{year}-12-31"
    
    df['Date'] = pd.to_datetime(df['Quarter'].apply(parse_quarter))
    df['Sector'] = df['Ticker'].map(sector_map).fillna('Others')
    df['Full_Name'] = df['Ticker'].map(full_name_map).fillna(df['Ticker'])
    
    # 获取Logo的URL和Base64编码
    logo_info = df['Ticker'].apply(get_google_logo_info)
    df['Logo_URL'] = [x[0] for x in logo_info]
    df['Logo_B64'] = [x[1] for x in logo_info]
    
    # 构建Logo的HTML标签
    df['Logo_HTML'] = df['Logo_URL'].apply(lambda url: f'<img src="{url}" alt="logo" width="30" height="30">')
    
    # 标注列：用于图表图例和悬停信息 (使用全名+代码)
    df['Logo_Name'] = df.apply(lambda row: f"{row['Full_Name']} ({row['Ticker']})", axis=1)
    
    df = df.sort_values(by=['Date', 'Value_Billions'], ascending=[True, False])
    return df, full_name_map, sector_map

df, full_name_map, sector_map = load_data()

def add_custom_legend(fig, df, chart_type="area"):
    """
    为Plotly图表添加带Logo的自定义图例
    :param fig: Plotly图表对象
    :param df: 数据DataFrame
    :param chart_type: 图表类型（area/bar）
    :return: 处理后的图表对象
    """
    # 隐藏原生图例
    fig.update_layout(showlegend=False)
    
    # 获取唯一的Logo_Name和对应的颜色、Base64编码
    unique_names = df['Logo_Name'].unique()
    color_map = {}
    b64_map = {}
    
    # 提取Plotly自动分配的颜色（按Logo_Name排序）
    if chart_type == "area":
        for i, name in enumerate(unique_names):
            if i < len(fig.data):
                color_map[name] = fig.data[i].fillcolor if hasattr(fig.data[i], 'fillcolor') else fig.data[i].line.color
    else:  # bar
        for i, name in enumerate(unique_names):
            if i < len(fig.data):
                color_map[name] = fig.data[i].marker.color
    
    # 提取Base64编码
    for name in unique_names:
        b64_map[name] = df[df['Logo_Name'] == name]['Logo_B64'].iloc[0]
    
    # 自定义图例的位置和大小（右侧，从上到下排列）
    legend_x = 1.02  # 图例在图表右侧（paper坐标系，1为图表右边界）
    legend_y_start = 0.95  # 图例顶部起始位置（paper坐标系，1为图表上边界）
    item_height = 0.04  # 每个图例项的高度（paper坐标系）
    logo_size_ratio = 0.02  # Logo的大小（相对图表的比例，0-1）
    
    for i, name in enumerate(unique_names):
        y_pos = legend_y_start - i * item_height
        if y_pos < 0:
            break  # 超出图表底部则停止
        
        # 1. 添加Logo图片（Base64编码）
        fig.add_layout_image(
            dict(
                source=f"data:image/png;base64,{b64_map[name]}",
                x=legend_x,
                y=y_pos,
                xref="paper",
                yref="paper",
                sizex=logo_size_ratio,
                sizey=logo_size_ratio,
                xanchor="left",
                yanchor="middle"
            )
        )
        
        # 2. 添加颜色方块（模拟图例的颜色标识）
        # 颜色方块的大小适配item_height
        rect_width = 0.015  # 颜色方块的宽度（paper坐标系）
        rect_height = item_height * 0.6  # 颜色方块的高度（paper坐标系）
        fig.add_shape(
            type="rect",
            x0=legend_x + logo_size_ratio + 0.005,  # Logo右侧偏移一点
            y0=y_pos - rect_height/2,
            x1=legend_x + logo_size_ratio + 0.005 + rect_width,
            y1=y_pos + rect_height/2,
            xref="paper",
            yref="paper",
            fillcolor=color_map.get(name, '#000000'),
            line_width=0
        )
        
        # 3. 添加文本标签
        text_x = legend_x + logo_size_ratio + 0.005 + rect_width + 0.005  # 颜色方块右侧偏移一点
        fig.add_annotation(
            x=text_x,
            y=y_pos,
            text=name,
            xref="paper",
            yref="paper",
            xanchor="left",
            yanchor="middle",
            font=dict(size=10),
            showarrow=False
        )
    
    # 调整图表右侧边距，为自定义图例留出空间（根据图例项数量动态调整）
    legend_count = min(len(unique_names), int(0.95/item_height))  # 实际显示的图例项数
    right_margin = 150 + legend_count * 10  # 基础边距+按项数增加
    fig.update_layout(margin=dict(right=right_margin))
    
    return fig


# -----------------------------------------------------------------------------
# 4. Sidebar 控制区（保持不变）
# -----------------------------------------------------------------------------
st.sidebar.header("⚙️ Controls")

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

all_sectors = sorted(df['Sector'].unique())
selected_sectors = st.sidebar.multiselect("🏷️ Filter by Sector", all_sectors, default=all_sectors)

all_full_names = sorted([name for name in df['Full_Name'].unique() if pd.notna(name)])
selected_full_names = st.sidebar.multiselect("🔍 Highlight Specific Stocks", all_full_names, default=[])

# -----------------------------------------------------------------------------
# 5. 数据筛选应用（保持不变）
# -----------------------------------------------------------------------------
filtered_df = df[df['Sector'].isin(selected_sectors)]
filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]
highlighted_df = filtered_df[filtered_df['Full_Name'].isin(selected_full_names)] if selected_full_names else None

# -----------------------------------------------------------------------------
# 6. 主内容区（保持不变）
# -----------------------------------------------------------------------------
st.title("Berkshire Hathaway Portfolio Evolution")
st.caption("A 25-year interactive visualization of Warren Buffett's investment strategy (2000-2025).")

if not filtered_df.empty:
    latest_date_filtered = filtered_df['Date'].max()
    latest_data_filtered = filtered_df[filtered_df['Date'] == latest_date_filtered]
    
    if not latest_data_filtered.empty:
        top_holding = latest_data_filtered.sort_values(by='Value_Billions', ascending=False).iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Start Period", start_date.strftime("%Y Q%q"))
        with col2:
            st.metric("End Period", end_date.strftime("%Y Q%q"))
        with col3:
            st.metric("Top Holding (Filtered)", top_holding['Logo_Name'], f"{top_holding['Percent_Portfolio']}%")
        with col4:
            top_sector_value = latest_data_filtered.groupby('Sector')['Value_Billions'].sum()
            if not top_sector_value.empty:
                top_sector = top_sector_value.idxmax()
                top_sector_percent = top_sector_value.max() / top_sector_value.sum() * 100
                st.metric("Top Sector", top_sector, f"{top_sector_percent:.1f}%")
            else:
                st.metric("Top Sector", "N/A", "0%")
    else:
        st.warning("No data found for the latest selected period. Adjust filters.")
        st.stop()
else:
    st.warning("No data found for the selected time and sector filters.")
    st.stop()

st.markdown("---")

# -----------------------------------------------------------------------------
# 7. 可视化 Tab 页（修改Tab1的图表，添加自定义图例）
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📊 Portfolio Composition", "📈 Stock Deep Dive", "🧩 Sector Shift", "📘 Company Reference"])

# --- Tab 1: 组合构成 (Macro) ---
with tab1:
    st.subheader("Evolution of Top Holdings (Value & Proportion)")
    
    # Area Chart（添加自定义图例）
    fig_area = px.area(
        filtered_df, 
        x="Date", 
        y="Value_Billions", 
        color="Logo_Name",
        title="Portfolio Value by Stock (Filtered by Time & Sector)",
        labels={"Value_Billions": "Value ($ Billions)"},
        template="plotly_white",
        hover_data={"Date": "|%Y-%m-%d"}
    )
    fig_area.update_layout(showlegend=False, height=600)  # 增加高度以容纳图例
    fig_area = add_custom_legend(fig_area, filtered_df, chart_type="area")
    st.plotly_chart(fig_area, use_container_width=True)
    
    st.subheader("Proportional Changes Over Time")
    
    # Bar Chart（添加自定义图例）
    fig_bar = px.bar(
        filtered_df, 
        x="Quarter", 
        y="Percent_Portfolio", 
        color="Logo_Name",
        title="Relative Portfolio Weight % (Filtered by Time & Sector)",
        barmode="relative",
        template="plotly_white"
    )
    fig_bar.update_layout(xaxis={'categoryorder':'category ascending'}, height=600, showlegend=False)
    fig_bar = add_custom_legend(fig_bar, filtered_df, chart_type="bar")
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Tab 2: 单个股票深度分析 (Micro) ---
with tab2:
    st.subheader("Single Stock Analysis")
    
    stock_options_filtered = sorted([name for name in filtered_df['Full_Name'].unique() if pd.notna(name)])
    if stock_options_filtered:
        target_full_name = st.selectbox("Select a Company to Analyze", stock_options_filtered, index=0)
        
        stock_data = filtered_df[filtered_df['Full_Name'] == target_full_name].sort_values('Date')
        
        c1, c2 = st.columns(2)
        
        with c1:
            fig_stock_val = px.line(
                stock_data, x='Date', y='Value_Billions', markers=True,
                title=f"{target_full_name}: Market Value History ($B)",
                color_discrete_sequence=['#2E86C1']
            )
            fig_stock_val.update_yaxes(rangemode="tozero")
            st.plotly_chart(fig_stock_val, use_container_width=True)
            
        with c2:
            fig_stock_share = px.line(
                stock_data, x='Date', y='Shares_Millions', markers=True,
                title=f"{target_full_name}: Shares Held History (Millions)",
                color_discrete_sequence=['#E74C3C']
            )
            fig_stock_share.update_yaxes(rangemode="tozero")
            st.plotly_chart(fig_stock_share, use_container_width=True)
            
        st.divider()
        st.subheader("Comparison Tool")
        logo_name_options = filtered_df['Logo_Name'].unique()
        default_compare = [filtered_df[filtered_df['Full_Name'] == target_full_name]['Logo_Name'].iloc[0]] if not filtered_df[filtered_df['Full_Name'] == target_full_name].empty else []
        if 'The Coca-Cola Company (KO)' in logo_name_options:
            default_compare.append('The Coca-Cola Company (KO)')
        compare_stocks_names = st.multiselect("Compare Holdings (Value)", logo_name_options, default=default_compare[:2])
        if compare_stocks_names:
            compare_data = filtered_df[filtered_df['Logo_Name'].isin(compare_stocks_names)]
            fig_compare = px.line(
                compare_data, x="Date", y="Value_Billions", color="Logo_Name",
                title="Holdings Value Comparison (Filtered)", markers=True
            )
            st.plotly_chart(fig_compare, use_container_width=True)
    else:
        st.info("No stocks available for analysis with current filters.")

# --- Tab 3: 行业变迁 (Trends) ---
with tab3:
    st.subheader("Strategic Shift by Sector")
    
    sector_data = filtered_df.groupby(['Date', 'Quarter', 'Sector'])['Value_Billions'].sum().reset_index()
    
    fig_sector = px.area(
        sector_data, x="Date", y="Value_Billions", color="Sector",
        title="Portfolio Value Composition by Sector (Filtered)",
        template="plotly_white",
    )
    st.plotly_chart(fig_sector, use_container_width=True)
    
    latest_sector_data = sector_data[sector_data['Date'] == latest_date_filtered]
    if not latest_sector_data.empty:
        fig_pie = px.pie(
            latest_sector_data, values='Value_Billions', names='Sector',
            title=f"Sector Allocation ({latest_date_filtered.strftime('%Y Q%q')}) (Filtered)",
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No sector data available for the latest period with current filters.")

# --- Tab 4: 公司参考 (Reference) ---
with tab4:
    st.subheader("📘 Company Reference (Full Name & Real Logo)")
    
    ref_df = filtered_df[['Ticker', 'Full_Name', 'Sector', 'Logo_HTML']].drop_duplicates(subset=['Ticker']).sort_values('Sector')
    
    ref_df['Logo & Name'] = ref_df.apply(
        lambda row: f"{row['Logo_HTML']} <span class='ref-ticker-col'>{row['Ticker']}</span>: {row['Full_Name']}", axis=1
    )
    
    final_ref_df = ref_df[['Logo & Name', 'Sector']]
    
    st.markdown("以下是筛选后的数据中出现的公司及其信息：", unsafe_allow_html=True)
    st.write(final_ref_df.to_html(escape=False, index=False), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("Designed with Streamlit & Plotly | Data based on Berkshire Hathaway 13F Filings (Top Holdings Only)")
