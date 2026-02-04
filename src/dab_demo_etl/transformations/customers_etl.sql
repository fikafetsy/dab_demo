
-- create or refresh streaming table customers_dev.bronze.bronze_customers
-- comment 'raw customer data'
-- tblproperties ('quality' = 'bronze')
-- as
-- select *,
--   _metadata.file_path as input_file_path,
--   current_timestamp as ingestion_timestamp
-- from cloud_files(
--   '/Volumes/customers_dev/landing/source_customers/',
--   'json',
--    map('cloudFiles.inferColumnTypes','true')
-- );


CREATE OR REFRESH STREAMING TABLE bronze_customers
COMMENT 'raw customer data'
TBLPROPERTIES ('quality' = 'bronze')
AS
SELECT *,
  _metadata.file_path AS input_file_path,
  current_timestamp() AS ingestion_timestamp
FROM cloud_files(
  '${source_path}',
  'json',
  map(
    'cloudFiles.inferColumnTypes','true')
);

