CREATE STREAMING TABLE silver_orders
AS
SELECT
  order_id,
  customer_id,
  order_timestamp,
  payment_method,
  order_status,
  item.item_id AS item_id,
  item.name AS item_name,
  item.price AS item_price,
  item.quantity AS item_quantity,
  item.category AS item_category
FROM (
  SELECT
    order_id,
    customer_id,
    order_timestamp,
    payment_method,
    order_status,
    explode(items) AS item
  FROM STREAM(${source_catalog}.silver.silver_orders_clean)
);
