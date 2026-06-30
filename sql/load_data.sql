-- Load CSV data into MySQL tables
-- Make sure CSV files are in: C:\Users\tlez1\OneDrive\מסמכים\Claude\Projects\Weekly Schedule\Portfolio_Projects\

-- Clear existing data (if needed)
DELETE FROM revenue;
DELETE FROM product_usage;
DELETE FROM customers;
DELETE FROM companies;

-- Load companies
LOAD DATA LOCAL INFILE 'C:\\Users\\tlez1\\OneDrive\\מסמכים\\Claude\\Projects\\Weekly Schedule\\Portfolio_Projects\\companies.csv'
INTO TABLE companies
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Load customers
LOAD DATA LOCAL INFILE 'C:\\Users\\tlez1\\OneDrive\\מסמכים\\Claude\\Projects\\Weekly Schedule\\Portfolio_Projects\\customers.csv'
INTO TABLE customers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Load product_usage
LOAD DATA LOCAL INFILE 'C:\\Users\\tlez1\\OneDrive\\מסמכים\\Claude\\Projects\\Weekly Schedule\\Portfolio_Projects\\product_usage.csv'
INTO TABLE product_usage
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Load revenue
LOAD DATA LOCAL INFILE 'C:\\Users\\tlez1\\OneDrive\\מסמכים\\Claude\\Projects\\Weekly Schedule\\Portfolio_Projects\\revenue.csv'
INTO TABLE revenue
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Verify the data loaded
SELECT
    'companies' as table_name, COUNT(*) as row_count FROM companies
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'product_usage', COUNT(*) FROM product_usage
UNION ALL
SELECT 'revenue', COUNT(*) FROM revenue;
