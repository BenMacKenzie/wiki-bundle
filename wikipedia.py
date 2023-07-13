# Databricks notebook source

from pyspark.sql.functions import *

import dlt


@dlt.create_table(
  comment="Wikipedia clickstream dataset with cleaned-up datatypes / column names and quality expectations.",
  table_properties={
    "quality": "silver"
  }
)
@dlt.expect("valid_current_page", "current_page_id IS NOT NULL AND current_page_title IS NOT NULL")
@dlt.expect_or_fail("valid_count", "click_count > 0")
def clickstream_clean():
  return (
    dlt.read("clickstream_raw")
      .withColumn("current_page_id", expr("CAST(curr_id AS INT)"))
      .withColumn("click_count", expr("CAST(n AS INT)"))
      .withColumn("previous_page_id", expr("CAST(prev_id AS INT)"))
      .withColumnRenamed("curr_title", "current_page_title")
      .withColumnRenamed("prev_title", "previous_page_title")
      .select("current_page_id", "current_page_title", "click_count", "previous_page_id", "previous_page_title")
  )


@dlt.create_table(
  comment="A table of the most common (100) pages that link to the Apache Spark page.",
  table_properties={
    "quality": "gold"  
  }  
)
def top_spark_referrers():
  return (
    dlt.read("clickstream_clean")
      .filter(expr("current_page_title == 'Apache_Spark'"))
      .withColumnRenamed("previous_page_title", "referrer")
      .sort(desc("click_count"))
      .select("referrer", "click_count")
  )


@dlt.create_table(
  comment="A list of the top 500 pages by number of clicks.",
  table_properties={
    "quality": "gold"  
  }  
)
def top_pages():
  return (
    dlt.read("clickstream_clean")
      .groupBy("current_page_title")
      .agg(sum("click_count").alias("total_clicks"))
      .sort(desc("total_clicks"))
  )
