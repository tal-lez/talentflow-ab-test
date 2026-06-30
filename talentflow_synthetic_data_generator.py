"""
TalentFlow Synthetic Data Generator
Portfolio Project: A/B Testing Ad Creative Performance

GOAL: Generate 10,000 synthetic customers for HR/recruitment SaaS A/B test analysis
OUTPUT: 4 CSV files (customers, companies, product_usage, revenue)

COMPANY CONTEXT:
- TalentFlow: Series B recruitment platform for mid-market to enterprise
- Campaign: 3 ad creatives tested across 10k customer acquisition
- Analysis goal: Which creative attracts best-fit, highest-value customers?

DATA STRUCTURE:
1. Companies (company_id, size, hiring_volume, employee_count)
2. Customers (customer_id, company_id, ad_creative, clicked, converted)
3. Product Usage (customer_id, adoption metrics, churn)
4. Revenue (customer_id, arr, retention signals)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# ============================================================================
# PARAMETERS & BENCHMARKS
# ============================================================================

TOTAL_CUSTOMERS = 10000
START_DATE = datetime(2026, 5, 1)  # Campaign start date

# Company size distribution
COMPANY_SIZE_DIST = {
    'Micro': {'pct': 0.30, 'emp_range': (1, 50), 'hiring_range': (1, 3)},
    'SMB': {'pct': 0.40, 'emp_range': (50, 500), 'hiring_range': (3, 8)},
    'Mid-market': {'pct': 0.20, 'emp_range': (500, 5000), 'hiring_range': (8, 25)},
    'Enterprise': {'pct': 0.10, 'emp_range': (5000, 50000), 'hiring_range': (20, 50)},
}

# Ad creative performance (conversion, adoption, churn)
CREATIVE_PARAMS = {
    'A': {'conv_rate': 0.12, 'ttv_days': 4, 'churn_90': 0.15, 'name': 'Hire Faster'},
    'B': {'conv_rate': 0.10, 'ttv_days': 3, 'churn_90': 0.09, 'name': 'Hire Better'},
    'C': {'conv_rate': 0.11, 'ttv_days': 4, 'churn_90': 0.12, 'name': 'Scale Your Hiring'},
}

# Size-specific churn rates
SIZE_CHURN = {
    'Micro': 0.15,
    'SMB': 0.15,
    'Mid-market': 0.09,
    'Enterprise': 0.06,
}

# ============================================================================
# FUNCTION 1: Generate Companies Table
# ============================================================================

def generate_companies(total_customers):
    """
    Create company records with realistic distribution across size segments.
    Returns a dataframe with company_id, size, employee_count, monthly_hiring_volume.
    """
    companies = []
    company_id = 1

    for size, params in COMPANY_SIZE_DIST.items():
        count = int(total_customers * params['pct'])
        emp_range = params['emp_range']
        hiring_range = params['hiring_range']

        for _ in range(count):
            employee_count = np.random.randint(emp_range[0], emp_range[1])
            hiring_volume = np.random.randint(hiring_range[0], hiring_range[1])

            companies.append({
                'company_id': company_id,
                'company_size': size,
                'employee_count': employee_count,
                'monthly_hiring_volume': hiring_volume,
                'industry': 'Tech',
                'region': 'US',
            })
            company_id += 1

    return pd.DataFrame(companies)


# ============================================================================
# FUNCTION 2: Generate Customers Table
# ============================================================================

def generate_customers(companies_df):
    """
    Create customer records with ad creative assignment and conversion.
    Each company is matched to customers acquired from that company.
    """
    customers = []
    customer_id = 1

    # Randomly assign creatives (A, B, C) roughly evenly
    creatives = ['A', 'B', 'C']

    for _, company in companies_df.iterrows():
        creative = random.choice(creatives)
        conv_rate = CREATIVE_PARAMS[creative]['conv_rate']

        # Each company acquires ~1 customer in this campaign (for 10k customers)
        customer_dict = {
            'customer_id': customer_id,
            'company_id': company['company_id'],
            'ad_creative': creative,
            'clicked': np.random.choice([True, False], p=[0.15, 0.85]),  # 15% CTR
            'converted': np.random.choice([True, False], p=[conv_rate, 1 - conv_rate]),
            'signup_date': START_DATE + timedelta(days=np.random.randint(0, 30)),
        }
        customers.append(customer_dict)
        customer_id += 1

    return pd.DataFrame(customers)


# ============================================================================
# FUNCTION 3: Generate Product Usage Table
# ============================================================================

def generate_product_usage(customers_df, companies_df):
    """
    Create adoption and engagement metrics for first 90 days.
    Usage patterns correlate with company size and creative.
    """
    usage_records = []

    # Merge to get company size info
    merged = customers_df.merge(companies_df, on='company_id', how='left')

    for _, row in merged.iterrows():
        customer_id = row['customer_id']
        creative = row['ad_creative']
        company_size = row['company_size']
        converted = row['converted']

        # Time to first value (TTV) - varies by creative
        ttv = max(1, np.random.normal(CREATIVE_PARAMS[creative]['ttv_days'], 1))
        ttv = int(np.clip(ttv, 1, 7))

        # Days active in first 7 days (depends on TTV and size)
        days_active_7 = np.random.randint(max(1, ttv - 1), 8) if converted else 0

        # Days active in first 30 days (adoption phase)
        if converted:
            days_active_30 = np.random.randint(days_active_7, 31)
        else:
            days_active_30 = 0

        # Days active in 90 days (varies by company size, creative)
        if converted:
            churn_prob = SIZE_CHURN[company_size]
            churned = np.random.choice([True, False], p=[churn_prob, 1 - churn_prob])
            if churned:
                days_active_90 = np.random.randint(0, days_active_30)
            else:
                days_active_90 = np.random.randint(days_active_30, 91)
        else:
            days_active_90 = 0
            churned = True

        # Logins in first 30 days (target: 8+ for healthy adoption = 2+/week)
        logins_30 = np.random.randint(0, 15) if converted else 0

        # Jobs posted, candidates viewed (depends on hiring volume)
        hiring_vol = row['monthly_hiring_volume']
        jobs_posted = np.random.poisson(hiring_vol / 2) if converted else 0
        candidates_viewed = jobs_posted * np.random.randint(5, 15) if jobs_posted > 0 else 0

        usage_records.append({
            'customer_id': customer_id,
            'days_active_first_7': days_active_7,
            'days_active_first_30': days_active_30,
            'days_active_first_90': days_active_90,
            'time_to_first_value': ttv,
            'logins_first_30': logins_30,
            'jobs_posted': jobs_posted,
            'candidates_viewed': candidates_viewed,
            'churn_flag': 'yes' if churned else 'no',
        })

    return pd.DataFrame(usage_records)


# ============================================================================
# FUNCTION 4: Generate Revenue Table
# ============================================================================

def generate_revenue(customers_df, companies_df):
    """
    Create revenue and retention metrics.
    ARR varies by company size; retention signals depend on adoption.
    """
    revenue_records = []

    merged = customers_df.merge(companies_df, on='company_id', how='left')
    merged = merged.merge(
        pd.read_csv('product_usage.csv').rename(columns={'churn_flag': 'churn'}),
        on='customer_id',
        how='left'
    )

    # Size-based ARR
    arr_by_size = {
        'Micro': (2000, 5000),
        'SMB': (5000, 15000),
        'Mid-market': (15000, 50000),
        'Enterprise': (50000, 200000),
    }

    for _, row in merged.iterrows():
        customer_id = row['customer_id']
        company_size = row['company_size']
        converted = row['converted']
        jobs_posted = row.get('jobs_posted', 0)

        # ARR
        if converted:
            arr_range = arr_by_size[company_size]
            arr = np.random.uniform(arr_range[0], arr_range[1])
        else:
            arr = 0

        # Days to first job posting (adoption signal)
        if converted and jobs_posted > 0:
            days_to_first_job = np.random.randint(1, 30)
        else:
            days_to_first_job = 999  # Never posted

        # Net revenue retention at 90 days (% of contract still active)
        if converted and row.get('churn') == 'no':
            nrr_90 = np.random.uniform(0.85, 1.20)  # Could expand or contract
        else:
            nrr_90 = 0.0  # Churned

        revenue_records.append({
            'customer_id': customer_id,
            'arr': round(arr, 2),
            'days_to_first_job_posting': days_to_first_job,
            'net_revenue_retention_90': round(nrr_90, 2),
        })

    return pd.DataFrame(revenue_records)


# ============================================================================
# MAIN: Generate All Tables
# ============================================================================

if __name__ == '__main__':
    print("🚀 Generating TalentFlow synthetic dataset...\n")

    # Step 1: Companies
    print(f"1. Generating {TOTAL_CUSTOMERS} company records...")
    companies = generate_companies(TOTAL_CUSTOMERS)
    companies.to_csv('companies.csv', index=False)
    print(f"   ✅ companies.csv ({len(companies)} rows)")

    # Step 2: Customers
    print(f"2. Generating customer records...")
    customers = generate_customers(companies)
    customers.to_csv('customers.csv', index=False)
    print(f"   ✅ customers.csv ({len(customers)} rows)")

    # Step 3: Product Usage
    print(f"3. Generating product usage metrics...")
    usage = generate_product_usage(customers, companies)
    usage.to_csv('product_usage.csv', index=False)
    print(f"   ✅ product_usage.csv ({len(usage)} rows)")

    # Step 4: Revenue
    print(f"4. Generating revenue data...")
    # Regenerate to avoid circular dependency
    revenue_records = []
    merged = customers.merge(companies, on='company_id', how='left')
    merged = merged.merge(usage, on='customer_id', how='left')

    arr_by_size = {
        'Micro': (2000, 5000),
        'SMB': (5000, 15000),
        'Mid-market': (15000, 50000),
        'Enterprise': (50000, 200000),
    }

    for _, row in merged.iterrows():
        if row['converted']:
            arr_range = arr_by_size[row['company_size']]
            arr = np.random.uniform(arr_range[0], arr_range[1])
        else:
            arr = 0

        if row['converted'] and row['jobs_posted'] > 0:
            days_to_job = np.random.randint(1, 30)
        else:
            days_to_job = 999

        if row['converted'] and row['churn_flag'] == 'no':
            nrr = np.random.uniform(0.85, 1.20)
        else:
            nrr = 0.0

        revenue_records.append({
            'customer_id': row['customer_id'],
            'arr': round(arr, 2),
            'days_to_first_job_posting': days_to_job,
            'net_revenue_retention_90': round(nrr, 2),
        })

    revenue = pd.DataFrame(revenue_records)
    revenue.to_csv('revenue.csv', index=False)
    print(f"   ✅ revenue.csv ({len(revenue)} rows)")

    print("\n📊 Dataset Summary:")
    print(f"   Total customers: {len(customers)}")
    print(f"   Conversion rate: {(customers['converted'].sum() / len(customers) * 100):.1f}%")
    print(f"   Creative A: {len(customers[customers['ad_creative'] == 'A'])} customers")
    print(f"   Creative B: {len(customers[customers['ad_creative'] == 'B'])} customers")
    print(f"   Creative C: {len(customers[customers['ad_creative'] == 'C'])} customers")
    print(f"\n✅ All files saved to current directory!")
    print(f"   Ready for SQL analysis and statistical testing.")
