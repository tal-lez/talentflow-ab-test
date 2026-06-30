# TalentFlow SQL Queries - Analysis Starter Pack

Once data is loaded into MySQL, use these queries to answer key business questions.

---

## Query 1: Creative Performance Overview
**Question:** Which creative has the best conversion rate?

```sql
SELECT
    c.ad_creative,
    COUNT(c.customer_id) as total_impressions,
    SUM(CASE WHEN c.clicked = TRUE THEN 1 ELSE 0 END) as clicks,
    ROUND(SUM(CASE WHEN c.clicked = TRUE THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as ctr_pct,
    SUM(CASE WHEN c.converted = TRUE THEN 1 ELSE 0 END) as conversions,
    ROUND(SUM(CASE WHEN c.converted = TRUE THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as conversion_rate_pct
FROM customers c
GROUP BY c.ad_creative
ORDER BY conversion_rate_pct DESC;
```

**What it shows:** CTR and conversion rate by creative. You should see Creative A highest (~12%), then C (~11%), then B (~10%).

---

## Query 2: Creative Performance by Company Size
**Question:** Which creative attracts which customer segments?

```sql
SELECT
    c.ad_creative,
    co.company_size,
    COUNT(c.customer_id) as customer_count,
    SUM(CASE WHEN c.converted = TRUE THEN 1 ELSE 0 END) as converted,
    ROUND(SUM(CASE WHEN c.converted = TRUE THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as conversion_pct,
    ROUND(AVG(r.arr), 2) as avg_arr
FROM customers c
JOIN companies co ON c.company_id = co.company_id
LEFT JOIN revenue r ON c.customer_id = r.customer_id
GROUP BY c.ad_creative, co.company_size
ORDER BY c.ad_creative, co.company_size;
```

**What it shows:** Which size of company converts best for each creative. You should see Creative B attracting more Enterprise customers with higher ARR.

---

## Query 3: Adoption Speed by Creative
**Question:** Which creative's customers adopt fastest?

```sql
SELECT
    c.ad_creative,
    COUNT(c.customer_id) as customers,
    ROUND(AVG(pu.time_to_first_value), 2) as avg_ttv_days,
    ROUND(AVG(pu.days_active_first_7), 2) as avg_days_active_7,
    ROUND(AVG(pu.logins_first_30), 2) as avg_logins_30,
    ROUND(SUM(CASE WHEN pu.days_active_first_30 >= 15 THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as healthy_adoption_pct
FROM customers c
JOIN product_usage pu ON c.customer_id = pu.customer_id
WHERE c.converted = TRUE
GROUP BY c.ad_creative
ORDER BY avg_ttv_days ASC;
```

**What it shows:** 
- TTV (time to first value) - should be 3-4 days for all
- Days active - shows engagement
- "Healthy adoption" = 15+ days active in first 30 days
- Creative B should show faster adoption and higher healthy adoption %

---

## Query 4: Churn Analysis by Creative
**Question:** Which creative's customers stay longest?

```sql
SELECT
    c.ad_creative,
    COUNT(c.customer_id) as converted_customers,
    SUM(CASE WHEN pu.churn_flag = 'no' THEN 1 ELSE 0 END) as still_active_90,
    SUM(CASE WHEN pu.churn_flag = 'yes' THEN 1 ELSE 0 END) as churned_90,
    ROUND(SUM(CASE WHEN pu.churn_flag = 'no' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as retention_pct_90
FROM customers c
JOIN product_usage pu ON c.customer_id = pu.customer_id
WHERE c.converted = TRUE
GROUP BY c.ad_creative
ORDER BY retention_pct_90 DESC;
```

**What it shows:** 90-day retention by creative. Creative B should have highest retention (~91%), followed by C (~88%), then A (~85%).

---

## Query 5: Churn by Company Size
**Question:** Does churn vary by company size?

```sql
SELECT
    co.company_size,
    COUNT(c.customer_id) as converted_customers,
    ROUND(SUM(CASE WHEN pu.churn_flag = 'no' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as retention_pct_90,
    ROUND(AVG(r.arr), 2) as avg_arr,
    ROUND(SUM(r.arr) / COUNT(c.customer_id), 2) as arr_per_customer
FROM customers c
JOIN companies co ON c.company_id = co.company_id
JOIN product_usage pu ON c.customer_id = pu.customer_id
LEFT JOIN revenue r ON c.customer_id = r.customer_id
WHERE c.converted = TRUE
GROUP BY co.company_size
ORDER BY retention_pct_90 DESC;
```

**What it shows:** Enterprise customers retain better (~94%) than SMB (~85%), etc.

---

## Query 6: Revenue Efficiency (CAC-like metric)
**Question:** Which creative generates the best revenue per customer?

```sql
SELECT
    c.ad_creative,
    COUNT(c.customer_id) as total_acquired,
    SUM(CASE WHEN c.converted = TRUE THEN 1 ELSE 0 END) as converted,
    ROUND(SUM(CASE WHEN c.converted = TRUE THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as conversion_pct,
    ROUND(SUM(r.arr) / COUNT(c.customer_id), 2) as avg_arr_per_acquired,
    ROUND(SUM(r.arr) / SUM(CASE WHEN c.converted = TRUE THEN 1 ELSE 0 END), 2) as avg_arr_per_converted
FROM customers c
LEFT JOIN revenue r ON c.customer_id = r.customer_id
GROUP BY c.ad_creative
ORDER BY avg_arr_per_converted DESC;
```

**What it shows:** Revenue per acquired customer and per converted customer. Shows which creative brings higher-value customers.

---

## Query 7: Advanced Segmentation - Best Customer Profile
**Question:** What's the ideal customer for each creative?

```sql
SELECT
    c.ad_creative,
    co.company_size,
    COUNT(c.customer_id) as customer_count,
    ROUND(SUM(CASE WHEN c.converted = TRUE THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as conversion_pct,
    ROUND(AVG(pu.time_to_first_value), 2) as avg_ttv,
    ROUND(SUM(CASE WHEN pu.churn_flag = 'no' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as retention_pct_90,
    ROUND(AVG(r.arr), 2) as avg_arr
FROM customers c
JOIN companies co ON c.company_id = co.company_id
JOIN product_usage pu ON c.customer_id = pu.customer_id
LEFT JOIN revenue r ON c.customer_id = r.customer_id
WHERE c.converted = TRUE
GROUP BY c.ad_creative, co.company_size
HAVING COUNT(c.customer_id) >= 50
ORDER BY c.ad_creative, retention_pct_90 DESC;
```

**What it shows:** Best-fit customer segments for each creative. Use this for your recommendation.

---

## How to Run These

1. Open MySQL Workbench
2. Create a new query tab
3. Copy & paste one query at a time
4. Click Execute (lightning bolt)
5. Review results
6. **Screenshot or export results** for your analysis

---

## Next Steps

Once you've run these queries:
1. **Document findings** — which creative wins for which segment?
2. **Statistical testing** — use Python to run t-tests and chi-square tests
3. **Visualization** — create charts showing key insights
4. **Recommendation** — write up your findings
