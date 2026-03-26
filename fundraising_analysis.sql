-- ============================================================
-- Nonprofit Fundraising Analysis
-- Author: Oguz Tuncel
-- Description: SQL scripts for analysing donor behaviour,
--              campaign performance, and fundraising trends
-- ============================================================

-- ============================================================
-- 1. DATABASE SETUP
-- ============================================================

CREATE TABLE IF NOT EXISTS donors (
    donor_id        VARCHAR(10) PRIMARY KEY,
    donor_name      VARCHAR(100),
    donor_type      VARCHAR(20),
    city            VARCHAR(50),
    state           VARCHAR(10),
    email           VARCHAR(100),
    acquisition_date DATE,
    age_group       VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS donations (
    donation_id     VARCHAR(10) PRIMARY KEY,
    donor_id        VARCHAR(10) REFERENCES donors(donor_id),
    donation_date   DATE,
    amount          DECIMAL(12,2),
    campaign        VARCHAR(50),
    channel         VARCHAR(20),
    is_recurring    SMALLINT,
    status          VARCHAR(20),
    fiscal_year     VARCHAR(10),
    quarter         VARCHAR(5),
    month           VARCHAR(15),
    year            INT
);

-- ============================================================
-- 2. KPI OVERVIEW
-- ============================================================

-- Total donations, donors, and average gift
SELECT
    COUNT(DISTINCT d.donor_id)                          AS total_donors,
    COUNT(dn.donation_id)                               AS total_donations,
    SUM(dn.amount)                                      AS total_raised,
    ROUND(AVG(dn.amount), 2)                            AS avg_gift,
    ROUND(SUM(dn.amount) / COUNT(DISTINCT d.donor_id), 2) AS revenue_per_donor
FROM donors d
JOIN donations dn ON d.donor_id = dn.donor_id
WHERE dn.status = 'Completed';

-- ============================================================
-- 3. CAMPAIGN PERFORMANCE
-- ============================================================

-- Revenue and donation count by campaign
SELECT
    campaign,
    COUNT(donation_id)                          AS num_donations,
    SUM(amount)                                 AS total_raised,
    ROUND(AVG(amount), 2)                       AS avg_donation,
    ROUND(SUM(amount) * 100.0 /
          SUM(SUM(amount)) OVER (), 2)          AS pct_of_total
FROM donations
WHERE status = 'Completed'
GROUP BY campaign
ORDER BY total_raised DESC;

-- Campaign performance by year
SELECT
    campaign,
    year,
    COUNT(donation_id)  AS num_donations,
    SUM(amount)         AS total_raised
FROM donations
WHERE status = 'Completed'
GROUP BY campaign, year
ORDER BY campaign, year;

-- ============================================================
-- 4. DONOR ANALYSIS
-- ============================================================

-- Donor segmentation by type
SELECT
    d.donor_type,
    COUNT(DISTINCT d.donor_id)          AS num_donors,
    COUNT(dn.donation_id)               AS num_donations,
    SUM(dn.amount)                      AS total_raised,
    ROUND(AVG(dn.amount), 2)            AS avg_donation
FROM donors d
JOIN donations dn ON d.donor_id = dn.donor_id
WHERE dn.status = 'Completed'
GROUP BY d.donor_type
ORDER BY total_raised DESC;

-- Top 10 donors by lifetime value
SELECT
    d.donor_id,
    d.donor_name,
    d.donor_type,
    d.city,
    COUNT(dn.donation_id)       AS num_donations,
    SUM(dn.amount)              AS lifetime_value,
    MIN(dn.donation_date)       AS first_donation,
    MAX(dn.donation_date)       AS last_donation
FROM donors d
JOIN donations dn ON d.donor_id = dn.donor_id
WHERE dn.status = 'Completed'
GROUP BY d.donor_id, d.donor_name, d.donor_type, d.city
ORDER BY lifetime_value DESC
LIMIT 10;

-- Donor retention: how many donated in consecutive years
WITH donor_years AS (
    SELECT
        donor_id,
        year,
        LAG(year) OVER (PARTITION BY donor_id ORDER BY year) AS prev_year
    FROM (
        SELECT DISTINCT donor_id, year
        FROM donations
        WHERE status = 'Completed'
    ) t
)
SELECT
    year,
    COUNT(CASE WHEN year - prev_year = 1 THEN 1 END)   AS retained_donors,
    COUNT(CASE WHEN prev_year IS NULL THEN 1 END)       AS new_donors
FROM donor_years
GROUP BY year
ORDER BY year;

-- ============================================================
-- 5. CHANNEL ANALYSIS
-- ============================================================

-- Revenue by acquisition channel
SELECT
    channel,
    COUNT(donation_id)                          AS num_donations,
    SUM(amount)                                 AS total_raised,
    ROUND(AVG(amount), 2)                       AS avg_donation,
    SUM(is_recurring)                           AS recurring_count,
    ROUND(SUM(is_recurring) * 100.0 /
          COUNT(donation_id), 1)                AS pct_recurring
FROM donations
WHERE status = 'Completed'
GROUP BY channel
ORDER BY total_raised DESC;

-- ============================================================
-- 6. TREND ANALYSIS
-- ============================================================

-- Monthly donation trend
SELECT
    year,
    month,
    COUNT(donation_id)      AS num_donations,
    SUM(amount)             AS total_raised,
    ROUND(AVG(amount), 2)   AS avg_donation
FROM donations
WHERE status = 'Completed'
GROUP BY year, month
ORDER BY year, MIN(donation_date);

-- Quarter over quarter growth
WITH quarterly AS (
    SELECT
        fiscal_year,
        quarter,
        SUM(amount) AS total_raised
    FROM donations
    WHERE status = 'Completed'
    GROUP BY fiscal_year, quarter
)
SELECT
    fiscal_year,
    quarter,
    total_raised,
    LAG(total_raised) OVER (ORDER BY fiscal_year, quarter) AS prev_quarter,
    ROUND((total_raised - LAG(total_raised) OVER
          (ORDER BY fiscal_year, quarter)) * 100.0 /
          NULLIF(LAG(total_raised) OVER
          (ORDER BY fiscal_year, quarter), 0), 2)          AS qoq_growth_pct
FROM quarterly
ORDER BY fiscal_year, quarter;

-- ============================================================
-- 7. GEOGRAPHIC ANALYSIS
-- ============================================================

-- Revenue by state
SELECT
    d.state,
    COUNT(DISTINCT d.donor_id)      AS num_donors,
    COUNT(dn.donation_id)           AS num_donations,
    SUM(dn.amount)                  AS total_raised,
    ROUND(AVG(dn.amount), 2)        AS avg_donation
FROM donors d
JOIN donations dn ON d.donor_id = dn.donor_id
WHERE dn.status = 'Completed'
GROUP BY d.state
ORDER BY total_raised DESC;

-- ============================================================
-- 8. DATA QUALITY CHECKS
-- ============================================================

-- Check for failed/pending donations
SELECT
    status,
    COUNT(*)            AS count,
    SUM(amount)         AS total_amount
FROM donations
GROUP BY status;

-- Check for duplicate donations
SELECT
    donor_id,
    donation_date,
    amount,
    COUNT(*) AS duplicates
FROM donations
GROUP BY donor_id, donation_date, amount
HAVING COUNT(*) > 1;

-- Donors with no completed donations
SELECT d.donor_id, d.donor_name, d.donor_type
FROM donors d
LEFT JOIN donations dn
    ON d.donor_id = dn.donor_id
    AND dn.status = 'Completed'
WHERE dn.donation_id IS NULL;
