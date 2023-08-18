# Databricks notebook source
# 
# Wikipedia Clickstream
# An example Delta Live Tables pipeline that ingests wikipedia click stream data and builds some simple summary tables.
#
#   Source: February 2015 English Wikipedia Clickstream in JSON
#   More information of the columns can be found at: https://meta.wikimedia.org/wiki/Research:Wikipedia_clickstream
#

import dlt

json_path = "/databricks-datasets/wikipedia-datasets/data-001/clickstream/raw-uncompressed-json/2015_2_clickstream.json"

@dlt.create_table(
  comment="The raw wikipedia click stream dataset, ingested from /databricks-datasets.",
  table_properties={
    "quality": "bronze"
  }
)
def clickstream_raw():          
  df = spark.read.option("inferSchema", "true").json(json_path)
  return df
