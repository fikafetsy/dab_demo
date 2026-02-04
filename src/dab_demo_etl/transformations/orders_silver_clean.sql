CREATE OR REFRESH STREAMING TABLE silver_orders_clean(
  CONSTRAINT valid_customer_id EXPECT (customer_id IS NOT NULL) ON VIOLATION FAIL UPDATE,
  CONSTRAINT valid_order_id EXPECT (order_id IS NOT NULL) ON VIOLATION FAIL UPDATE,
  CONSTRAINT valid_order_status EXPECT (order_status IN ('Pending', 'Shipped')),
  CONSTRAINT valid_payment_method EXPECT (payment_method IN ('Credit Card', 'Debit Card'))
)
COMMENT "Cleaned orders data"
TBLPROPERTIES ("quality" = "silver")
AS
SELECT
  order_id,
  customer_id,
  CAST(order_timestamp AS TIMESTAMP) AS order_timestamp,
  payment_method,
  items,
  order_status
FROM STREAM(${source_catalog}.bronze.bronze_orders);