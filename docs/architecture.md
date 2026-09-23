# Warehouse Architecture

## Overview

This project implements an end-to-end e-commerce analytics warehouse using Python, DuckDB, dbt, SQL, and Power BI.

The implemented data flow is:

```text
Raw Olist CSV Data
        |
        v
Python Data Loading
        |
        v
DuckDB Raw Layer
        |
        v
dbt Staging Models
        |
        v
Intermediate Transformation
        |
        v
Analytics Marts
        |
        +------> Data Quality Audits
        |
        v
Power BI
```

The architecture separates ingestion, transformation, business logic, validation, and reporting.

## 1. Raw Layer

The source data is the Brazilian E-Commerce Public Dataset by Olist.

The raw CSV files are loaded into DuckDB under the `raw` schema using:

```text
scripts/load_raw.py
```

The loading process creates these raw tables:

- `customers`
- `geolocation`
- `order_items`
- `order_payments`
- `reviews`
- `orders`
- `products`
- `sellers`
- `category_translation`

The raw layer preserves the source data before analytical transformations are applied.

## 2. Staging Layer

The staging layer is implemented with dbt models under:

```text
ecommerce_analytics/models/staging/
```

The staging models standardize the raw source tables and provide consistent inputs for downstream transformations.

The staging layer contains models for the major source entities, including customers, orders, order items, payments, reviews, products, sellers, geolocation, and category translation.

## 3. Intermediate Layer

The intermediate transformation is implemented through:

```text
int_order_items_enriched
```

This model operates at the **order-item grain**.

It combines order-item records with related order, customer, product, seller, and category information.

The model also calculates:

```text
item_total_including_freight = price + freight
```

Keeping the order-item grain explicit prevents downstream aggregations from unintentionally mixing different levels of detail.

## 4. Analytics Marts

The warehouse contains three primary analytical marts.

### Customer Summary

Model:

```text
mart_customer_summary
```

Grain:

```text
One row per customer_unique_id
```

It provides customer-level measures including:

- Total orders
- Delivered orders
- Total items
- Product revenue
- Freight
- Total revenue
- Average order value
- First order date
- Last order date
- Customer lifetime days

### Daily Sales

Model:

```text
mart_daily_sales
```

Grain:

```text
One row per purchase date
```

It provides:

- Total orders
- Total items
- Product revenue
- Freight
- Total revenue
- Average order value

### Product Performance

Model:

```text
mart_product_performance
```

Grain:

```text
One row per product
```

It provides:

- Total orders
- Items sold
- Product revenue
- Freight
- Total revenue
- Average item price
- Average freight value
- Product attributes
- Category attributes

## 5. Revenue Definitions

The warehouse keeps the major financial measures explicitly defined.

| Measure | Definition |
|---|---|
| Product revenue | Item price only |
| Freight revenue | Freight value |
| Total revenue | Item price + freight value |
| Payment value | Recorded customer payment amount |

Payment value is maintained as a separate measure and is not treated as a direct reconciliation target for product revenue.

## 6. Data Quality and Audit Layer

The project uses both dbt tests and custom validation scripts.

The audit model:

```text
audit_orders_without_items
```

identifies orders without associated order-item records when their status is not expected to lack item records.

The current audit identifies:

- 2 invoiced orders
- 1 shipped order

These records are retained and surfaced as data-quality exceptions rather than deleted.

Additional reconciliation checks validate:

- Raw to staging order counts
- Staging to mart product revenue
- Staging to mart total revenue
- Orders without item records
- Payment values
- Data-quality exceptions

## 7. Reporting Layer

Power BI consumes the analytical warehouse outputs for business-facing reporting.

The final dashboard focuses on:

- Sales performance
- Customer analysis
- Product performance
- Revenue trends
- KPI monitoring

The Power BI project is stored under:

```text
power bi/Ecommerce_Customer_Revenue_Analytics_Final.pbix
```

The reporting layer is kept separate from the warehouse transformation logic so that business reporting is built on tested analytical models rather than directly on raw source data.

## 8. End-to-End Model Flow

The implemented architecture can be summarized as:

```text
CSV Sources
   |
   v
scripts/load_raw.py
   |
   v
DuckDB raw.*
   |
   v
dbt staging
   |
   v
int_order_items_enriched
   |
   +-------------------+
   |         |         |
   v         v         v
Customer   Daily    Product
Summary    Sales    Performance
   |         |         |
   +---------+---------+
             |
             v
          Power BI

Separate validation path:
dbt tests + reconciliation scripts + audit model
```

This separation provides traceability from source data through transformations, analytical outputs, validation, and business reporting.
