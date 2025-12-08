# Berkshire Hathaway Portfolio Evolution (2000-2025)



![Python](https://img.shields.io/badge/Python-3.8%2B-blue)



![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-green)



![Plotly](https://img.shields.io/badge/Plotly-5.0%2B-orange)

**中文名称：伯克希尔・哈撒韦投资组合 25 年演变可视化分析**

## 🔍 项目简介

A professional interactive visualization tool for Warren Buffett's Berkshire Hathaway investment portfolio (2000-2025). Track the evolution of top holdings, sector allocation shifts, and individual stock performance with real-time bilingual (English / 中文) support.

专业的沃伦・巴菲特伯克希尔・哈撒韦投资组合交互式可视化工具（2000-2025），支持实时跟踪核心持仓演变、行业配置变迁、个股表现分析，提供中英文双语切换功能。

### 核心价值



* 📊 25 年投资数据全量覆盖（2000Q4-2025Q3），还原巴菲特投资策略变迁

* 🌐 中英文双语界面，适配全球用户需求

* 🎯 多维度筛选（时间范围、行业分类、个股高亮），精准定位投资趋势

* 📈 动态图表可视化（面积图、柱状图、折线图），直观呈现数据洞察

## 🚀 核心功能

### 1. 投资组合构成分析（Portfolio Composition）



* 实时查看股票持仓价值变化趋势（按时间 / 行业筛选）

* 持仓占比相对变化可视化，识别核心重仓股变迁

* 个股高亮功能，快速对比目标股票与其他持仓表现

### 2. 个股深度分析（Stock Deep Dive）



* 单只股票市值历史追踪（十亿美元级数据）

* 持股数量变化趋势分析（百万股级数据）

* 多股对比工具，支持自定义选择标的（默认含可口可乐 KO 作为基准）

### 3. 行业配置变迁（Sector Shift）



* 行业持仓价值构成动态演变

* 最新季度行业配置占比饼图（支持时间范围筛选）

* 识别巴菲特长期行业配置战略调整

### 4. 公司参考手册（Company Reference）



* 全量持仓公司中英文名称对照

* 真实企业 Logo 展示（基于 Google Favicon API）

* 行业分类标注，快速建立投资组合行业认知

## 📋 快速开始

### 1. 环境准备



```
\# 克隆仓库（如需）

git clone https://github.com/your-username/berkshire-portfolio.git

cd berkshire-portfolio

\# 安装依赖

pip install streamlit pandas plotly
```

### 2. 运行项目



```
streamlit run app.py
```

自动打开浏览器访问 `http://localhost:8501`，即可使用完整功能。

### 3. 基础操作指南



1. **语言切换**：侧边栏顶部选择「English / 中文」，界面实时同步翻译

2. **时间筛选**：拖动时间滑块选择目标时间段（默认全量 25 年数据）

3. **行业筛选**：勾选目标行业，仅显示该行业下的持仓数据

4. **个股高亮**：在「Highlight Specific Stocks」中选择标的，图表中自动突出显示

5. **Tab 切换**：通过 4 个功能标签页（组合构成 / 个股分析 / 行业变迁 / 公司参考）切换分析维度

## 📊 数据说明

### 数据来源

基于 Berkshire Hathaway 13F Filings（美国证监会 SEC 季度持仓备案文件），筛选核心重仓股数据进行清洗整理。

数据维度包括：



* 时间维度：季度级数据（2000Q4-2025Q3）

* 股票维度：代码（Ticker）、中英文全名、行业分类、企业 Logo

* 指标维度：持股数量（百万股）、持仓市值（十亿美元）、组合占比（%）

### 核心覆盖标的（部分）



| 股票代码 | 英文名称                  | 中文名称   | 行业分类                   |
| ---- | --------------------- | ------ | ---------------------- |
| AAPL | Apple Inc.            | 苹果公司   | 科技（Technology）         |
| KO   | The Coca-Cola Company | 可口可乐公司 | 必选消费（Consumer Staples） |
| BAC  | Bank of America       | 美国银行   | 金融（Financials）         |
| AXP  | American Express      | 美国运通公司 | 金融（Financials）         |
| OXY  | Occidental Petroleum  | 西方石油公司 | 能源（Energy）             |

## 🌐 技术栈



* **前端框架**：Streamlit（快速构建数据可视化 Web 应用）

* **数据处理**：Pandas（数据清洗、筛选、聚合）

* **可视化库**：Plotly（交互式图表生成，支持响应式布局）

* **其他**：Google Favicon API（企业 Logo 获取）、Session State（双语状态管理）

## 🎨 界面特性



* 硅谷极简风格设计，专注数据可读性

* 响应式布局，适配桌面 / 平板设备

* 中文字体优化（Microsoft YaHei），英文优化（Helvetica Neue）

* 图表交互功能（悬停显示详情、缩放、下载）

## 📌 注意事项



1. 数据为核心重仓股筛选结果，非伯克希尔全部持仓（完整 13F 文件含更多标的）

2. 2025Q3 数据为预测值，基于历史趋势及公开信息估算

3. Logo 加载依赖网络连接，部分地区可能需要科学上网

4. 建议使用 Chrome/Firefox 浏览器以获得最佳交互体验

## 🤝 贡献指南

欢迎提交 Issue 或 Pull Request 优化项目：



* 数据补充：新增更多历史季度数据或修正现有数据

* 功能优化：增加财务指标计算、估值分析等高级功能

* 体验改进：优化界面设计、添加更多语言支持

## 📞 联系我们

如需商业合作、数据定制或功能咨询，可通过以下方式联系：



* GitHub：[your-username](https://github.com/your-username)

* Email：your-email@example.com



***

**SEO 关键词**：Warren Buffett, Berkshire Hathaway, 巴菲特投资组合，伯克希尔持仓分析，股票可视化工具，投资策略变迁，行业配置分析，双语数据工具

**License**：MIT License（开源自由使用，保留署名）

> （注：文档部分内容可能由 AI 生成）
