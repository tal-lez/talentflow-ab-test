# Loading Synthetic Data into MySQL Workbench

## Step-by-Step Guide

### Step 1: Create the Database & Tables

1. Open MySQL Workbench
2. Connect to your local MySQL server
3. Create a new query tab (File → New Query Tab, or Ctrl+T)
4. Copy & paste the entire contents of `talentflow_schema.sql`
5. Click the lightning bolt icon (Execute) to run all queries
6. You should see:
   - Database `talentflow` created
   - 4 tables created with indexes

**Check:** Look in the left sidebar under "Schemas" → you should see `talentflow` with all 4 tables.

---

### Step 2: Import CSV Files into Tables

MySQL Workbench has a built-in Table Data Import Wizard. Here's how:

#### For Each CSV File (repeat 4 times):

1. **Right-click the table** in the left sidebar (e.g., `companies`)
2. Select **"Table Data Import Wizard"**
3. **Browse** for the CSV file:
   - Navigate to: `C:\Users\tlez1\OneDrive\מסמכים\Claude\Projects\Weekly Schedule\Portfolio_Projects\`
   - Select the corresponding CSV (e.g., `companies.csv`)
4. **Click Next** through the wizard:
   - Column mapping should auto-detect correctly
   - Review the preview
   - Click "Next" until you see "Import Complete"

**Repeat for:**
- `companies.csv` → companies table
- `customers.csv` → customers table
- `product_usage.csv` → product_usage table
- `revenue.csv` → revenue table

---

### Step 3: Verify the Data Loaded Correctly

1. Create a new query tab
2. Copy & paste the **VERIFICATION QUERIES** section from `talentflow_schema.sql`
3. Run them (Execute button)

**You should see:**
- Row counts: 10,000 for each table
- Ad creative distribution (roughly equal A/B/C)
- Company size breakdown
- Conversion rates by creative (~10-12%)

**Example output:**
```
| table_name   | row_count |
|--------------|-----------|
| companies    |     10000 |
| customers    |     10000 |
| product_usage|     10000 |
| revenue      |     10000 |
```

---

## Troubleshooting

**Issue: "Table already exists" error**
- You already created the tables. Delete them first or use `DROP TABLE IF EXISTS ...;` in the schema script.

**Issue: Foreign key constraint errors during import**
- Make sure you import in this order:
  1. companies (no dependencies)
  2. customers (depends on companies)
  3. product_usage (depends on customers)
  4. revenue (depends on customers)

**Issue: CSV columns not mapping correctly**
- Make sure column headers in CSVs match the column names in the SQL schema.
- Check the first row of each CSV file matches: `company_id, company_size, employee_count, ...`

**Issue: "Access Denied" or file path errors**
- Make sure you're using the Table Data Import Wizard (not manual LOAD DATA INFILE)
- Workbench handles file permissions automatically

---

## What's Next?

Once verified, you're ready for SQL analysis! See `talentflow_sql_queries.md` for starter queries to:
- Compare creative performance by segment
- Calculate adoption speed (time to first value)
- Analyze churn patterns
- Calculate CAC efficiency
