
-- CREATE OR REFRESH STREAMING TABLE silver_customers_clean (
--   CONSTRAINT valid_customer_id   EXPECT (customer_id IS NOT NULL) ON VIOLATION FAIL UPDATE,
--   CONSTRAINT valid_customer_name EXPECT (customer_name IS NOT NULL) ON VIOLATION DROP ROW,
--   CONSTRAINT valid_telephone     EXPECT (LENGTH(telephone) >= 10),
--   CONSTRAINT valid_email         EXPECT (email IS NOT NULL),
--   CONSTRAINT valid_date_of_birth EXPECT (date_of_birth >= '1920-01-01')
-- )
-- COMMENT 'Cleaned customers data'
-- TBLPROPERTIES ('quality' = 'silver')
-- AS
-- SELECT
--   customer_id,
--   customer_name,
--   CAST(date_of_birth AS DATE) AS date_of_birth,
--   telephone,
--   email,
--   CAST(created_date AS DATE) AS created_date
-- FROM STREAM(customers_dev.bronze.bronze_customers);


-- CREATE OR REFRESH STREAMING TABLE customers_dev.silver.silver_customers
-- COMMENT 'SCD Type 1 customers data'
-- TBLPROPERTIES ('quality' = 'silver');

-- APPLY CHANGES INTO customers_dev.silver.silver_customers
-- FROM STREAM(LIVE.silver_customers_clean)
-- KEYS (customer_id)
-- SEQUENCE BY created_date
-- STORED AS SCD TYPE 1;


CREATE OR REFRESH STREAMING TABLE silver_customers_clean (
  CONSTRAINT valid_customer_id   EXPECT (customer_id IS NOT NULL) ON VIOLATION FAIL UPDATE,
  CONSTRAINT valid_customer_name EXPECT (customer_name IS NOT NULL) ON VIOLATION DROP ROW,
  CONSTRAINT valid_telephone     EXPECT (LENGTH(telephone) >= 10),
  CONSTRAINT valid_email         EXPECT (email IS NOT NULL),
  CONSTRAINT valid_date_of_birth EXPECT (date_of_birth >= '1920-01-01')
)
COMMENT 'Cleaned customers data'
TBLPROPERTIES ('quality' = 'silver')
AS
SELECT
  customer_id,
  customer_name,
  CAST(date_of_birth AS DATE) AS date_of_birth,
  telephone,
  email,
  CAST(created_date AS DATE) AS created_date
FROM STREAM(${source_catalog}.bronze.bronze_customers);

CREATE OR REFRESH STREAMING TABLE silver_customers
COMMENT 'SCD Type 1 customers data'
TBLPROPERTIES ('quality' = 'silver');

APPLY CHANGES INTO silver_customers
FROM STREAM(silver_customers_clean)
KEYS (customer_id)
SEQUENCE BY created_date
STORED AS SCD TYPE 1;
