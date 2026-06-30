-- ============================================================================
-- TalentFlow Database Schema
-- A/B Testing Ad Creative Performance
-- ============================================================================

-- Create Database (optional - run if you want a dedicated database)
CREATE DATABASE IF NOT EXISTS talentflow;
USE talentflow;

-- ============================================================================
-- TABLE 1: COMPANIES
-- ============================================================================
CREATE TABLE IF NOT EXISTS companies (
    company_id INT PRIMARY KEY,
    company_size VARCHAR(20) NOT NULL,
    employee_count INT NOT NULL,
    monthly_hiring_volume INT NOT NULL,
    industry VARCHAR(50),
    region VARCHAR(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create index on company_size for faster queries
CREATE INDEX IF NOT EXISTS idx_company_size ON companies(company_size);

-- ============================================================================
-- TABLE 2: CUSTOMERS
-- ============================================================================
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    company_id INT NOT NULL,
    ad_creative CHAR(1) NOT NULL,
    clicked BOOLEAN,
    converted BOOLEAN,
    signup_date DATE,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_ad_creative ON customers(ad_creative);
CREATE INDEX IF NOT EXISTS idx_converted ON customers(converted);
CREATE INDEX IF NOT EXISTS idx_company_id ON customers(company_id);

-- ============================================================================
-- TABLE 3: PRODUCT_USAGE
-- ============================================================================
CREATE TABLE IF NOT EXISTS product_usage (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_churn_flag ON product_usage(churn_flag);
CREATE INDEX IF NOT EXISTS idx_time_to_first_value ON product_usage(time_to_first_value);

-- ============================================================================
-- TABLE 4: REVENUE
-- ============================================================================
CREATE TABLE IF NOT EXISTS revenue (
    customer_id INT PRIMARY KEY,
    arr DECIMAL(10, 2),
    days_to_first_job_posting INT,
    net_revenue_retention_90 DECIMAL(5, 2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create index on arr for financial queries
CREATE INDEX IF NOT EXISTS idx_arr ON revenue(arr);

-- ============================================================================
-- VERIFICATION QUERIES (Run these after loading data)
-- ============================================================================

-- Check row counts
SELECT
    'companies' as table_name, COUNT(*) as row_count FROM companies
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'product_usage', COUNT(*) FROM product_usage
UNION ALL
SELECT 'revenue', COUNT(*) FROM revenue;

-- Check ad creative distribution
SELECT ad_creative, COUNT(*) as count, ROUND(COUNT(*) / 10000 * 100, 1) as pct
FROM customers
GROUP BY ad_creative
ORDER BY ad_creative;

-- Check company size distribution
SELECT company_size, COUNT(*) as count
FROM companies
GROUP BY company_size
ORDER BY count DESC;

-- Check conversion rate by creative
SELECT
    ad_creative,
    COUNT(*) as total_customers,
    SUM(CASE WHEN converted = TRUE THEN 1 ELSE 0 END) as converted_count,
    ROUND(SUM(CASE WHEN converted = TRUE THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) as conversion_pct
FROM customers
GROUP BY ad_creative
ORDER BY ad_creative;
