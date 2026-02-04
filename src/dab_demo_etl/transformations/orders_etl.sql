CREATE OR REFRESH STREAMING TABLE bronze_orders
COMMENT "Raw orders data ingested from the source system"
TBLPROPERTIES ("quality" = "bronze")
AS
SELECT *,
  _metadata.file_path AS input_file_path,
  CURRENT_TIMESTAMP AS ingestion_timestamp
FROM cloud_files(
  '${source_path}',
  'json',
  map("cloudFiles.inferColumnTypes", "true")
);
