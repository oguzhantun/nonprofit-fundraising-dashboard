# Nonprofit Fundraising Dashboard

**End-to-end data analysis project simulating a real-world fundraising reporting solution for a not-for-profit organisation.**

Built to demonstrate skills in SQL, Python (Pandas, Matplotlib, Seaborn), and Power BI — covering the full analytics lifecycle from data preparation through to executive-ready insights.

---

## Project Overview

This project replicates the type of work delivered during a Data Analyst contract at a not-for-profit organisation, where the goal was to replace fragmented third-party reporting tools with a trusted, in-house Power BI solution — resulting in approximately 20% reduction in reporting costs.

The dataset is synthetic but realistic, comprising **500 donors** and **2,000 donations** across 3 years (2022–2024), covering multiple campaigns, acquisition channels, and geographic regions across Australia.

---

## Key Metrics

| Metric | Value |
|---|---|
| Total Donors | 500 |
| Total Donations | 1,838 completed |
| Total Raised | $11.7M |
| Average Gift | $6,367 |
| Recurring Rate | 35.7% |
| Campaigns | 8 |
| Channels | 7 |
| Years Covered | 2022 – 2024 |

---

## Analysis Included

**SQL**
- KPI overview — total raised, average gift, revenue per donor
- Campaign performance with percentage contribution
- Donor segmentation by type (Individual, Corporate, Foundation, Government)
- Top 10 donors by lifetime value
- Donor retention analysis using window functions (LAG)
- Channel analysis with recurring donation rates
- Quarter-over-quarter growth
- Geographic analysis by state
- Data quality checks — duplicates, failed donations, missing records

**Python EDA**
- Campaign revenue and average gift comparison
- Monthly fundraising trend (2022–2024)
- Donor type breakdown — revenue share and count
- Acquisition channel performance
- Revenue by state (geographic breakdown)
- Year-over-year campaign revenue comparison
- Donor retention — new vs returning donors

**Power BI**
- Executive summary page with KPI cards
- Campaign performance page
- Donor segmentation page
- Trend analysis page with slicers by year, campaign, and channel

---

## Sample Charts

### Monthly Fundraising Trend
![Monthly Trend](02_monthly_trend.png)

### Campaign Performance
![Campaign Performance](01_campaign_performance.png)

### Donor Retention
![Donor Retention](07_retention.png)

### Year-over-Year Revenue
![YoY Comparison](06_yoy_campaign.png)

---

## Tools Used

| Tool | Purpose |
|---|---|
| Python (Pandas, NumPy) | Data manipulation and analysis |
| Matplotlib / Seaborn | Data visualisation |
| SQL (PostgreSQL syntax) | Data querying and transformation |
| Microsoft Power BI | Executive dashboard delivery |
| DAX | KPI measures and calculated columns |
| Git / GitHub | Version control and portfolio |

---

## How to Run

Clone the repository and install dependencies:

    pip install pandas numpy matplotlib seaborn

Then run:

    python fundraising_eda.py

For SQL — load donors.csv and donations.csv into any SQL database (PostgreSQL, SQLite, or SQL Server) and run fundraising_analysis.sql.

---

## Key Insights

1. **Youth Education** and **Community Health** are the top-performing campaigns, together accounting for over 35% of total revenue
2. **Online** and **Recurring** channels deliver the highest volume — recurring donors represent 35.7% of all donations
3. **Corporate and Foundation donors** make up only 25% of the donor base but contribute disproportionately to total revenue
4. **VIC and NSW** are the strongest geographic markets, contributing approximately 50% of total funds raised
5. Donor retention improved year-over-year, with returning donors increasing from 2022 to 2024

---

## About

**Oguz Tuncel** — Data Analyst | Power BI Developer

- LinkedIn: https://linkedin.com/in/oguztuncel
- Email: ogzhantuncell@gmail.com
- Melbourne, VIC, Australia

---

*This project uses synthetic data generated for portfolio purposes. No real donor or organisational data is included.*
