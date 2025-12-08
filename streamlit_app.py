import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. 多语言配置
# -----------------------------------------------------------------------------
# 语言字典 - 包含所有需要翻译的文本
LANG = {
    "English": {
        "page_title": "Berkshire Portfolio | 2000-2025",
        "title": "Berkshire Hathaway Portfolio Evolution",
        "caption": "A 25-year interactive visualization of Warren Buffett's investment strategy (2000-2025).",
        "sidebar_header": "⚙️ Controls",
        "time_slider": "⏳ Select Time Period",
        "sector_filter": "🏷️ Filter by Sector",
        "stock_filter": "🔍 Highlight Specific Stocks",
        "start_period": "Start Period",
        "end_period": "End Period",
        "top_holding": "Top Holding (Filtered)",
        "top_sector": "Top Sector",
        "warning_no_latest_data": "No data found for the latest selected period. Adjust filters.",
        "warning_no_data": "No data found for the selected time and sector filters.",
        "tab1_title": "📊 Portfolio Composition",
        "tab2_title": "📈 Stock Deep Dive",
        "tab3_title": "🧩 Sector Shift",
        "tab4_title": "📘 Company Reference",
        "tab1_sub1": "Evolution of Top Holdings (Value & Proportion)",
        "tab1_chart1_title": "Portfolio Value by Stock (Filtered by Time & Sector)",
        "tab1_chart1_yaxis": "Value ($ Billions)",
        "tab1_sub2": "Proportional Changes Over Time",
        "tab1_chart2_title": "Relative Portfolio Weight % (Filtered by Time & Sector)",
        "tab2_sub1": "Single Stock Analysis",
        "tab2_select_company": "Select a Company to Analyze",
        "tab2_no_stocks": "No stocks available for analysis with current filters.",
        "tab2_chart1_title": "{name}: Market Value History ($B)",
        "tab2_chart2_title": "{name}: Shares Held History (Millions)",
        "tab2_divider": "Comparison Tool",
        "tab2_compare_label": "Compare Holdings (Value)",
        "tab2_compare_title": "Holdings Value Comparison (Filtered)",
        "tab3_sub1": "Strategic Shift by Sector",
        "tab3_chart1_title": "Portfolio Value Composition by Sector (Filtered)",
        "tab3_chart2_title": "Sector Allocation ({date}) (Filtered)",
        "tab3_no_sector_data": "No sector data available for the latest period with current filters.",
        "tab4_sub1": "📘 Company Reference (Full Name & Real Logo)",
        "tab4_description": "Below are the companies appearing in the filtered data with their information:",
        "col_logo_name": "Logo & Name",
        "col_sector": "Sector",
        "footer": "Designed with Streamlit & Plotly | Data based on Berkshire Hathaway 13F Filings (Top Holdings Only)"
    },
    "中文": {
        "page_title": "伯克希尔投资组合 | 2000-2025",
        "title": "伯克希尔·哈撒韦投资组合演变",
        "caption": "巴菲特25年投资策略的交互式可视化分析 (2000-2025)",
        "sidebar_header": "⚙️ 控制面板",
        "time_slider": "⏳ 选择时间范围",
        "sector_filter": "🏷️ 按行业筛选",
        "stock_filter": "🔍 高亮特定股票",
        "start_period": "开始时间",
        "end_period": "结束时间",
        "top_holding": "最大持仓 (已筛选)",
        "top_sector": "主要行业",
        "warning_no_latest_data": "所选最新时间段无数据，请调整筛选条件。",
        "warning_no_data": "所选时间和行业筛选条件下无数据。",
        "tab1_title": "📊 投资组合构成",
        "tab2_title": "📈 个股深度分析",
        "tab3_title": "🧩 行业变迁",
        "tab4_title": "📘 公司参考",
        "tab1_sub1": "主要持仓演变 (价值与占比)",
        "tab1_chart1_title": "股票持仓价值 (按时间和行业筛选)",
        "tab1_chart1_yaxis": "价值 (十亿美元)",
        "tab1_sub2": "持仓占比变化趋势",
        "tab1_chart2_title": "持仓权重占比 % (按时间和行业筛选)",
        "tab2_sub1": "个股分析",
        "tab2_select_company": "选择要分析的公司",
        "tab2_no_stocks": "当前筛选条件下无可分析的股票。",
        "tab2_chart1_title": "{name}: 市值历史 (十亿美元)",
        "tab2_chart2_title": "{name}: 持股数量历史 (百万股)",
        "tab2_divider": "对比分析工具",
        "tab2_compare_label": "对比持仓价值",
        "tab2_compare_title": "持仓价值对比 (已筛选)",
        "tab3_sub1": "行业配置战略变迁",
        "tab3_chart1_title": "行业持仓价值构成 (已筛选)",
        "tab3_chart2_title": "行业配置占比 ({date}) (已筛选)",
        "tab3_no_sector_data": "当前筛选条件下最新时间段无行业数据。",
        "tab4_sub1": "📘 公司参考 (全名与真实Logo)",
        "tab4_description": "以下是筛选后的数据中出现的公司及其信息：",
        "col_logo_name": "Logo & 名称",
        "col_sector": "行业",
        "footer": "使用 Streamlit & Plotly 制作 | 数据基于伯克希尔·哈撒韦 13F 备案文件 (仅主要持仓)"
    }
}

# -----------------------------------------------------------------------------
# 2. 配置页面 (Silicon Valley Minimalist Style)
# -----------------------------------------------------------------------------
# 先设置页面配置（必须在开头）
st.set_page_config(
    page_title="Berkshire Portfolio | 2000-2025",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 在侧边栏顶部添加语言选择器
st.sidebar.selectbox(
    "🌐 Language / 语言",
    options=["English", "中文"],
    key="language",
    index=0
)

# 获取当前语言设置
lang = st.session_state.get("language", "English")
t = LANG[lang]

# 自定义CSS以实现更干净的界面
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
    
    /* 中文字体优化 */
    body {font-family: 'Microsoft YaHei', 'Helvetica Neue', sans-serif;}
    [data-testid="stMarkdownContainer"] p {font-size: 16px; line-height: 1.6;}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. 数据准备 (内置全量清洗后的数据)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    # 核心映射数据：新增全名映射（中英文）
    full_name_map = {
        'AAPL': {'en': 'Apple Inc.', 'zh': '苹果公司'},
        'AXP': {'en': 'American Express Company', 'zh': '美国运通公司'},
        'BAC': {'en': 'Bank of America Corporation', 'zh': '美国银行'},
        'KO': {'en': 'The Coca-Cola Company', 'zh': '可口可乐公司'},
        'CVX': {'en': 'Chevron Corporation', 'zh': '雪佛龙公司'},
        'OXY': {'en': 'Occidental Petroleum Corporation', 'zh': '西方石油公司'},
        'MCO': {'en': 'Moody\'s Corporation', 'zh': '穆迪公司'},
        'KHC': {'en': 'The Kraft Heinz Company', 'zh': '卡夫亨氏公司'},
        'CB': {'en': 'Chubb Limited', 'zh': '丘博保险'},
        'GOOGL': {'en': 'Alphabet Inc. (Google)', 'zh': '字母表公司 (谷歌)'},
        'DVA': {'en': 'DaVita Inc.', 'zh': '达维塔公司'},
        'KR': {'en': 'The Kroger Co.', 'zh': '克罗格公司'},
        'DPZ': {'en': 'Domino\'s Pizza, Inc.', 'zh': '达美乐披萨'},
        'POOL': {'en': 'Pool Corporation', 'zh': '普尔公司'},
        'IBM': {'en': 'International Business Machines Corp.', 'zh': 'IBM公司'},
        'WFC': {'en': 'Wells Fargo & Company', 'zh': '富国银行'},
        'PG': {'en': 'The Procter & Gamble Company', 'zh': '宝洁公司'},
        'VZ': {'en': 'Verizon Communications Inc.', 'zh': '威瑞森通信'},
        'USB': {'en': 'U.S. Bancorp', 'zh': '美国合众银行'},
        'JPM': {'en': 'JPMorgan Chase & Co.', 'zh': '摩根大通'},
        'C': {'en': 'Citigroup Inc.', 'zh': '花旗集团'},
        'V': {'en': 'Visa Inc.', 'zh': '维萨公司'},
        'MA': {'en': 'Mastercard Incorporated', 'zh': '万事达卡公司'},
        'AMZN': {'en': 'Amazon.com, Inc.', 'zh': '亚马逊公司'},
        'ATVI': {'en': 'Activision Blizzard', 'zh': '动视暴雪'},
        'HPQ': {'en': 'HP Inc.', 'zh': '惠普公司'},
        'PARA': {'en': 'Paramount Global', 'zh': '派拉蒙全球'},
        'WPO': {'en': 'The Washington Post Company', 'zh': '华盛顿邮报公司'},
        'G': {'en': 'The Gillette Company', 'zh': '吉列公司'},
        'COP': {'en': 'ConocoPhillips', 'zh': '康菲石油公司'},
        'KFT': {'en': 'Kraft Foods', 'zh': '卡夫食品'},
        'WSC': {'en': 'Wesco Financial', 'zh': '韦斯科金融公司'},
        'BNI': {'en': 'BNSF Railway Co.', 'zh': 'BNSF铁路公司'},
        'PSX': {'en': 'Phillips 66', 'zh': '菲利普斯66公司'},
        'TSM': {'en': 'Taiwan Semiconductor (TSM)', 'zh': '台积电'},
        'UNH': {'en': 'UnitedHealth Group', 'zh': '联合健康集团'},
        'JNJ': {'en': 'Johnson & Johnson', 'zh': '强生公司'},
        'SNOW': {'en': 'Snowflake Inc.', 'zh': '雪花公司'},
        'VRSN': {'en': 'VeriSign Inc.', 'zh': '威瑞信公司'},
        'BK': {'en': 'Bank of New York Mellon Corporation', 'zh': '纽约梅隆银行'},
        'WMT': {'en': 'Walmart Inc.', 'zh': '沃尔玛公司'},
        'COST': {'en': 'Costco Wholesale Corporation', 'zh': '开市客公司'},
        'BUD': {'en': 'Anheuser-Busch InBev SA/NV', 'zh': '百威英博'},
        'DIS': {'en': 'The Walt Disney Company', 'zh': '迪士尼公司'},
        'CHTR': {'en': 'Charter Communications Inc.', 'zh': '特许通信公司'},
        'XOM': {'en': 'Exxon Mobil Corporation', 'zh': '埃克森美孚公司'},
        'DAL': {'en': 'Delta Air Lines Inc.', 'zh': '达美航空公司'},
        'LUV': {'en': 'Southwest Airlines Co.', 'zh': '西南航空公司'},
        'UAL': {'en': 'United Airlines Holdings Inc.', 'zh': '联合航空控股公司'},
        'AAL': {'en': 'American Airlines Group Inc.', 'zh': '美国航空集团'},
        'ABBV': {'en': 'AbbVie Inc.', 'zh': '艾伯维公司'},
        'MRK': {'en': 'Merck & Co. Inc.', 'zh': '默克公司'},
        'HRB': {'en': 'H&R Block Inc.', 'zh': 'H&R布洛克公司'},
        'MTB': {'en': 'M&T Bank Corporation', 'zh': 'M&T银行'}
    }
    
    # 行业映射（中英文）
    sector_map = {
        'Technology': {'en': 'Technology', 'zh': '科技'},
        'Financials': {'en': 'Financials', 'zh': '金融'},
        'Consumer Staples': {'en': 'Consumer Staples', 'zh': '必选消费'},
        'Consumer Discretionary': {'en': 'Consumer Discretionary', 'zh': '可选消费'},
        'Comm/Media': {'en': 'Comm/Media', 'zh': '通信/媒体'},
        'Energy': {'en': 'Energy', 'zh': '能源'},
        'Industrials': {'en': 'Industrials', 'zh': '工业'},
        'Healthcare': {'en': 'Healthcare', 'zh': '医疗健康'},
        'Others': {'en': 'Others', 'zh': '其他'}
    }
    
    # 股票行业映射
    ticker_sector_map = {
        'AAPL': 'Technology', 'IBM': 'Technology', 'HPQ': 'Technology', 'SNOW': 'Technology', 'GOOGL': 'Technology', 'VRSN': 'Technology', 'ATVI': 'Technology', 'TSM': 'Technology',
        'BAC': 'Financials', 'AXP': 'Financials', 'WFC': 'Financials', 'USB': 'Financials', 'C': 'Financials', 'JPM': 'Financials', 'MCO': 'Financials', 'BK': 'Financials', 'CB': 'Financials', 'MA': 'Financials', 'V': 'Financials', 'WSC': 'Financials', 'MTB': 'Financials',
        'KO': 'Consumer Staples', 'KHC': 'Consumer Staples', 'KFT': 'Consumer Staples', 'PG': 'Consumer Staples', 'WMT': 'Consumer Staples', 'KR': 'Consumer Staples', 'COST': 'Consumer Staples', 'BUD': 'Consumer Staples',
        'G': 'Consumer Discretionary', 'WPO': 'Comm/Media', 'DPZ': 'Consumer Discretionary', 'DIS': 'Comm/Media', 'CHTR': 'Comm/Media', 'PARA': 'Comm/Media', 'VZ': 'Comm/Media', 'POOL': 'Consumer Discretionary', 'HRB': 'Consumer Discretionary',
        'CVX': 'Energy', 'OXY': 'Energy', 'XOM': 'Energy', 'COP': 'Energy', 'PSX': 'Energy',
        'BNI': 'Industrials', 'DAL': 'Industrials', 'LUV': 'Industrials', 'UAL': 'Industrials', 'AAL': 'Industrials',
        'DVA': 'Healthcare', 'JNJ': 'Healthcare', 'ABBV': 'Healthcare', 'MRK': 'Healthcare', 'UNH': 'Healthcare',
    }

    # 使用Google Favicon API获取logo URL
    def get_google_logo_url(ticker):
        domain_map = {
            'AAPL': 'apple.com', 'AXP': 'americanexpress.com', 'BAC': 'bankofamerica.com',
            'KO': 'coca-colacompany.com', 'CVX': 'chevron.com', 'OXY': 'oxy.com',
            'MCO': 'moodys.com', 'KHC': 'kraftheinzcompany.com', 'CB': 'chubb.com',
            'GOOGL': 'google.com', 'DVA': 'davita.com', 'KR': 'kroger.com',
            'DPZ': 'dominos.com', 'POOL': 'poolcorp.com', 'IBM': 'ibm.com',
            'WFC': 'wellsfargo.com', 'PG': 'pg.com', 'VZ': 'verizon.com',
            'USB': 'usbank.com', 'JPM': 'jpmorganchase.com', 'C': 'citi.com',
            'V': 'visa.com', 'MA': 'mastercard.com', 'AMZN': 'amazon.com',
            'ATVI': 'activisionblizzard.com', 'HPQ': 'hp.com', 'PARA': 'paramount.com',
            'WPO': 'washingtonpost.com', 'G': 'gillette.com', 'COP': 'conocophillips.com',
            'KFT': 'kraftfoods.com', 'WSC': 'wesco.com', 'BNI': 'bnsf.com',
            'PSX': 'phillips66.com', 'TSM': 'tsmc.com', 'UNH': 'unitedhealthgroup.com',
            'JNJ': 'jnj.com', 'SNOW': 'snowflake.com', 'VRSN': 'verisign.com',
            'BK': 'bnymellon.com', 'WMT': 'walmart.com', 'COST': 'costco.com',
            'BUD': 'ab-inbev.com', 'DIS': 'disney.com', 'CHTR': 'charter.com',
            'XOM': 'exxonmobil.com', 'DAL': 'delta.com', 'LUV': 'southwest.com',
            'UAL': 'united.com', 'AAL': 'aa.com', 'ABBV': 'abbvie.com',
            'MRK': 'merck.com', 'HRB': 'hrblock.com', 'MTB': 'mtb.com'
        }
        domain = domain_map.get(ticker, 'google.com')
        size = 30
        return f"https://www.google.com/s2/favicons?domain={domain}&sz={size}"
    
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
    
    # 根据语言获取行业名称
    def get_sector_name(ticker):
        sector_key = ticker_sector_map.get(ticker, 'Others')
        return sector_map[sector_key]
    
    df['Sector_En'] = df['Ticker'].apply(lambda x: get_sector_name(x)['en'])
    df['Sector_Zh'] = df['Ticker'].apply(lambda x: get_sector_name(x)['zh'])
    
    # 根据语言获取公司全名
    def get_company_name(ticker, lang):
        lang_key = 'en' if lang == 'English' else 'zh'
        return full_name_map.get(ticker, {}).get(lang_key, ticker)
    
    # 临时存储，后续根据当前语言选择
    df['Full_Name_En'] = df['Ticker'].apply(lambda x: get_company_name(x, 'English'))
    df['Full_Name_Zh'] = df['Ticker'].apply(lambda x: get_company_name(x, '中文'))
    
    # 生成Logo的img标签
    df['Logo_URL'] = df['Ticker'].apply(lambda t: get_google_logo_url(t))
    df['Logo_HTML'] = df['Logo_URL'].apply(lambda url: f'<img src="{url}" alt="logo" width="30" height="30">')
    
    df = df.sort_values(by=['Date', 'Value_Billions'], ascending=[True, False])
    return df, full_name_map, sector_map, ticker_sector_map

# 加载数据
df, full_name_map, sector_map, ticker_sector_map = load_data()

# 根据当前语言更新数据列
current_lang = 'en' if lang == 'English' else 'zh'
df['Sector'] = df[f'Sector_{current_lang.capitalize()}']
df['Full_Name'] = df[f'Full_Name_{current_lang.capitalize()}']
df['Logo_Name'] = df.apply(lambda row: f"{row['Full_Name']} ({row['Ticker']})", axis=1)

# -----------------------------------------------------------------------------
# 4. Sidebar 控制区
# -----------------------------------------------------------------------------
st.sidebar.header(t["sidebar_header"])

# 时间线滑块
min_date = df['Date'].min().to_pydatetime()
max_date = df['Date'].max().to_pydatetime()

date_range = st.sidebar.slider(
    t["time_slider"],
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM"
)
start_date, end_date = date_range

# 行业筛选器 - 使用当前语言的行业名称
all_sectors = sorted(df['Sector'].unique())
selected_sectors = st.sidebar.multiselect(t["sector_filter"], all_sectors, default=all_sectors)

# 公司筛选器 - 使用当前语言的公司全名
all_full_names = sorted([name for name in df['Full_Name'].unique() if pd.notna(name)])
selected_full_names = st.sidebar.multiselect(t["stock_filter"], all_full_names, default=[])

# -----------------------------------------------------------------------------
# 5. 数据筛选应用
# -----------------------------------------------------------------------------
# 1. 行业筛选
filtered_df = df[df['Sector'].isin(selected_sectors)]

# 2. 时间筛选
filtered_df = filtered_df[
    (filtered_df['Date'] >= start_date) & 
    (filtered_df['Date'] <= end_date)
]

# 3. 选中公司筛选 (仅高亮)
highlighted_df = filtered_df[filtered_df['Full_Name'].isin(selected_full_names)] if selected_full_names else None

# -----------------------------------------------------------------------------
# 6. 主内容区
# -----------------------------------------------------------------------------
st.title(t["title"])
st.caption(t["caption"])

if not filtered_df.empty:
    latest_date_filtered = filtered_df['Date'].max()
    latest_data_filtered = filtered_df[filtered_df['Date'] == latest_date_filtered]
    
    if not latest_data_filtered.empty:
        top_holding = latest_data_filtered.sort_values(by='Value_Billions', ascending=False).iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(t["start_period"], start_date.strftime("%Y"))
        with col2:
            st.metric(t["end_period"], end_date.strftime("%Y"))
        with col3:
            st.metric(t["top_holding"], top_holding['Logo_Name'], f"{top_holding['Percent_Portfolio']}%")
        with col4:
            top_sector_value = latest_data_filtered.groupby('Sector')['Value_Billions'].sum()
            if not top_sector_value.empty:
                top_sector = top_sector_value.idxmax()
                top_sector_percent = top_sector_value.max() / top_sector_value.sum() * 100
                st.metric(t["top_sector"], top_sector, f"{top_sector_percent:.1f}%")
            else:
                st.metric(t["top_sector"], "N/A", "0%")
    else:
        st.warning(t["warning_no_latest_data"])
        st.stop()
else:
    st.warning(t["warning_no_data"])
    st.stop()

st.markdown("---")

# -----------------------------------------------------------------------------
# 7. 可视化 Tab 页
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([t["tab1_title"], t["tab2_title"], t["tab3_title"], t["tab4_title"]])

# --- Tab 1: 组合构成 (Macro) ---
with tab1:
    st.subheader(t["tab1_sub1"])
    
    fig_area = px.area(
        filtered_df, 
        x="Date", 
        y="Value_Billions", 
        color="Logo_Name",
        title=t["tab1_chart1_title"],
        labels={"Value_Billions": t["tab1_chart1_yaxis"]},
        template="plotly_white",
        hover_data={"Date": "|%Y-%m-%d"}
    )
    
    if highlighted_df is not None and not highlighted_df.empty:
        highlight_names = highlighted_df['Logo_Name'].unique()
        for trace in fig_area.data:
            if trace.name in highlight_names:
                trace.line.width = 3
                trace.fill = 'tonextx'
    fig_area.update_layout(showlegend=True, height=500)
    st.plotly_chart(fig_area, use_container_width=True)
    
    st.subheader(t["tab1_sub2"])
    fig_bar = px.bar(
        filtered_df, 
        x="Quarter", 
        y="Percent_Portfolio", 
        color="Logo_Name",
        title=t["tab1_chart2_title"],
        barmode="relative",
        template="plotly_white"
    )
    
    if highlighted_df is not None and not highlighted_df.empty:
        highlight_names = highlighted_df['Logo_Name'].unique()
        for trace in fig_bar.data:
            if trace.name in highlight_names:
                trace.marker.opacity = 1
            else:
                trace.marker.opacity = 0.5
    fig_bar.update_layout(xaxis={'categoryorder':'category ascending'}, height=500)
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Tab 2: 单个股票深度分析 (Micro) ---
with tab2:
    st.subheader(t["tab2_sub1"])
    
    stock_options_filtered = sorted([name for name in filtered_df['Full_Name'].unique() if pd.notna(name)])
    if stock_options_filtered:
        target_full_name = st.selectbox(t["tab2_select_company"], stock_options_filtered, index=0)
        
        stock_data = filtered_df[filtered_df['Full_Name'] == target_full_name].sort_values('Date')
        
        c1, c2 = st.columns(2)
        
        with c1:
            fig_stock_val = px.line(
                stock_data, x='Date', y='Value_Billions', markers=True,
                title=t["tab2_chart1_title"].format(name=target_full_name),
                color_discrete_sequence=['#2E86C1']
            )
            fig_stock_val.update_yaxes(rangemode="tozero")
            st.plotly_chart(fig_stock_val, use_container_width=True)
            
        with c2:
            fig_stock_share = px.line(
                stock_data, x='Date', y='Shares_Millions', markers=True,
                title=t["tab2_chart2_title"].format(name=target_full_name),
                color_discrete_sequence=['#E74C3C']
            )
            fig_stock_share.update_yaxes(rangemode="tozero")
            st.plotly_chart(fig_stock_share, use_container_width=True)
            
        st.divider()
        st.subheader(t["tab2_divider"])
        logo_name_options = filtered_df['Logo_Name'].unique()
        default_compare = [filtered_df[filtered_df['Full_Name'] == target_full_name]['Logo_Name'].iloc[0]] if not filtered_df[filtered_df['Full_Name'] == target_full_name].empty else []
        
        # 默认添加可口可乐作为对比
        ko_name = None
        for name in logo_name_options:
            if '(KO)' in name:
                ko_name = name
                break
        if ko_name and ko_name not in default_compare:
            default_compare.append(ko_name)
        
        compare_stocks_names = st.multiselect(t["tab2_compare_label"], logo_name_options, default=default_compare[:2])
        if compare_stocks_names:
            compare_data = filtered_df[filtered_df['Logo_Name'].isin(compare_stocks_names)]
            fig_compare = px.line(
                compare_data, x="Date", y="Value_Billions", color="Logo_Name",
                title=t["tab2_compare_title"], markers=True
            )
            st.plotly_chart(fig_compare, use_container_width=True)
    else:
        st.info(t["tab2_no_stocks"])

# --- Tab 3: 行业变迁 (Trends) ---
with tab3:
    st.subheader(t["tab3_sub1"])
    
    sector_data = filtered_df.groupby(['Date', 'Quarter', 'Sector'])['Value_Billions'].sum().reset_index()
    
    fig_sector = px.area(
        sector_data, x="Date", y="Value_Billions", color="Sector",
        title=t["tab3_chart1_title"],
        template="plotly_white",
    )
    st.plotly_chart(fig_sector, use_container_width=True)
    
    latest_sector_data = sector_data[sector_data['Date'] == latest_date_filtered]
    if not latest_sector_data.empty:
        fig_pie = px.pie(
            latest_sector_data, values='Value_Billions', names='Sector',
            title=t["tab3_chart2_title"].format(date=latest_date_filtered.strftime("%Y Q%q")),
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info(t["tab3_no_sector_data"])

# --- Tab 4: 公司参考 (Reference) ---
with tab4:
    st.subheader(t["tab4_sub1"])
    
    ref_df = filtered_df[['Ticker', 'Full_Name', 'Sector', 'Logo_HTML']].drop_duplicates(subset=['Ticker']).sort_values('Sector')
    
    # 重新构建Logo & Name列
    ref_df['Logo & Name'] = ref_df.apply(
        lambda row: f"{row['Logo_HTML']} <span class='ref-ticker-col'>{row['Ticker']}</span>: {row['Full_Name']}", axis=1
    )
    
    final_ref_df = ref_df[['Logo & Name', 'Sector']]
    final_ref_df.columns = [t["col_logo_name"], t["col_sector"]]
    
    st.markdown(t["tab4_description"], unsafe_allow_html=True)
    st.write(final_ref_df.to_html(escape=False, index=False), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(t["footer"])
