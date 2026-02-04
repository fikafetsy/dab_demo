CREATE OR REFRESH MATERIALIZED VIEW ${orders_catalog}.gold.gold_customer_order_summary AS
SELECT
  c.customer_id,
  c.customer_name,
  c.date_of_birth,
  c.telephone,
  c.email,
  a.address_line_1,
  a.city,
  a.state,
  a.postcode,
  COUNT(DISTINCT o.order_id) AS total_orders,
  SUM(o.item_quantity) AS total_items_ordered,
  SUM(o.item_quantity * o.item_price) AS total_order_amount
FROM ${customers_catalog}.${silver_schema}.silver_customers c
JOIN ${addresses_catalog}.${silver_schema}.silver_addresses a
  ON c.customer_id = a.customer_id
JOIN ${orders_catalog}.${silver_schema}.silver_orders o
  ON c.customer_id = o.customer_id
WHERE a.__END_AT IS NULL
GROUP BY
  c.customer_id, c.customer_name, c.date_of_birth, c.telephone, c.email,
  a.address_line_1, a.city, a.state, a.postcode;


-- FROM customers_dev.silver.silver_customers c
-- JOIN addresses_dev.silver.silver_addresses a
--   ON c.customer_id = a.customer_id
-- JOIN orders_dev.silver.silver_orders o
--   ON c.customer_id = o.customer_id
-- WHERE a.__END_AT IS NULL
-- GROUP BY
--   c.customer_id, c.customer_name, c.date_of_birth, c.telephone, c.email,
--   a.address_line_1, a.city, a.state, a.postcode;
