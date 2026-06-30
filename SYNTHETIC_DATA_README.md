# TalentFlow Synthetic Data Generator

## Quick Start

**Goal:** Generate 10,000 synthetic customer records for A/B testing ad creatives.

**Time estimate:** 5-10 minutes to run

**Output:** 4 CSV files ready for SQL analysis

---

## What to Do

### Step 1: Run the Script
```bash
python talentflow_synthetic_data_generator.py
```

This will:
- Generate 10,000 companies and customers
- Create realistic adoption patterns (first 90 days)
- Assign ad creatives (A, B, C) with built-in performance differences
- Calculate revenue and retention metrics

### Step 2: You'll Get 4 CSV Files
```
companies.csv          (10,000 rows)
customers.csv          (10,000 rows)
product_usage.csv      (10,000 rows)
revenue.csv            (10,000 rows)
```

### Step 3: Load into SQL Database
```sql
-- Create tables
CREATE TABLE companies (
    company_id INT PRIMARY KEY,
    company_size VARCHAR(20),
    employee_count INT,
    monthly_hiring_volume INT,
    industry VARCHAR(50),
    region VARCHAR(50)
);

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    company_id INT,
    ad_creative CHAR(1),
    clicked BOOLEAN,
    converted BOOLEAN,
    signup_date DATE,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE product_usage (
    customer_id INT PRIMARY KEY,
    days_active_first_7 INT,
    days_active_first_30 INT,
    days_active_first_90 INT,
    time_to_first_value INT,
    logins_first_30 INT,
    jobs_posted INT,
    candidates_viewed INT,
    churn_flag VARCHAR(3),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE revenue (
    customer_id INT PRIMARY KEY,
    arr DECIMAL(10,2),
    days_to_first_job_posting INT,
    net_revenue_retention_90 DECIMAL(5,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Load data
LOAD DATA INFILE 'companies.csv' INTO TABLE companies ...;
LOAD DATA INFILE 'customers.csv' INTO TABLE customers ...;
LOAD DATA INFILE 'product_usage.csv' INTO TABLE product_usage ...;
LOAD DATA INFILE 'revenue.csv' INTO TABLE revenue ...;
```

---

## What the Data Represents

### Companies Table
- **company_size**: Micro (1-50), SMB (50-500), Mid-market (500-5k), Enterprise (5k+)
- **Distribution**: 30% Micro, 40% SMB, 20% Mid-market, 10% Enterprise
- **hiring_volume**: Varies by size (1-3 for Micro, up to 20-50+ for Enterprise)

### Customers Table
- **ad_creative**: A ("Hire Faster"), B ("Hire Better"), C ("Scale Your Hiring")
- **clicked**: Whether the ad was clicked (15% CTR)
- **converted**: Whether they signed up (varies by creative: 10-12%)
- **signup_date**: Randomly distributed over 30-day campaign

### Product Usage Table (First 90 Days)
- **time_to_first_value**: How fast they reached first value (3-4 days)
- **days_active**: Engagement across 7, 30, 90 days
- **logins_first_30**: How many times they logged in
- **jobs_posted / candidates_viewed**: Platform usage signal
- **churn_flag**: Did they churn by day 90? (Varies by size: 15% Micro, 6% Enterprise)

### Revenue Table
- **arr**: Annual recurring revenue (varies by company size: $2k-$200k)
- **days_to_first_job_posting**: How quickly they started using the product
- **net_revenue_retention_90**: Did they expand, contract, or churn?

---

## Built-In Performance Differences

The script encodes realistic performance patterns for each creative:

| Creative | Name | Conv Rate | TTV (days) | 90-Day Churn |
|----------|------|-----------|-----------|--------------|
| A | Hire Faster | 12% | 4 | 15% |
| B | Hire Better | 10% | 3 | 9% |
| C | Scale Your Hiring | 11% | 4 | 12% |

**Your analysis should discover:** Creative B attracts higher-value customers and retains them better, despite lower conversion rate.

---

## Next Steps (After Data Generation)

1. **SQL Analysis** — Segment by creative, company size, adoption speed
2. **Statistical Testing** — T-tests on adoption, chi-square on conversion
3. **Visualization** — Create charts showing findings
4. **Recommendation** — Which creative to scale and where?

---

## Questions?

The script is heavily commented. Read through the code to understand:
- How company size distribution is created
- How adoption patterns differ by creative
- How churn is calculated based on company size

This is intentional — part of your portfolio is the code itself!
