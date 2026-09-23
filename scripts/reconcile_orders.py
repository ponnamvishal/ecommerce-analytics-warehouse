from pathlib import Path

import duckdb

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "warehouse.duckdb"

con = duckdb.connect(DB_PATH)

print("\n========== ECOMMERCE WAREHOUSE VALIDATION ==========\n")


# =====================================================
# 1. ROW COUNT VALIDATION
# =====================================================

raw_orders = con.execute("""
    SELECT COUNT(*)
    FROM raw.orders
""").fetchone()[0]

staging_orders = con.execute("""
    SELECT COUNT(*)
    FROM staging.stg_orders
""").fetchone()[0]

order_item_rows = con.execute("""
    SELECT COUNT(*)
    FROM staging.stg_order_items
""").fetchone()[0]

itemized_orders = con.execute("""
    SELECT COUNT(DISTINCT order_id)
    FROM staging.stg_order_items
""").fetchone()[0]

orders_without_items = raw_orders - itemized_orders


# =====================================================
# 2. REVENUE VALIDATION
# =====================================================

item_revenue = con.execute("""
    SELECT COALESCE(SUM(price), 0)
    FROM staging.stg_order_items
""").fetchone()[0]

item_freight = con.execute("""
    SELECT COALESCE(SUM(freight_value), 0)
    FROM staging.stg_order_items
""").fetchone()[0]

item_total_revenue = item_revenue + item_freight

mart_product_revenue = con.execute("""
    SELECT COALESCE(SUM(product_revenue), 0)
    FROM marts.mart_daily_sales
""").fetchone()[0]

mart_total_revenue = con.execute("""
    SELECT COALESCE(SUM(total_revenue), 0)
    FROM marts.mart_daily_sales
""").fetchone()[0]


# =====================================================
# 3. PAYMENT VALIDATION
# =====================================================

payment_value = con.execute("""
    SELECT COALESCE(SUM(payment_value), 0)
    FROM staging.stg_order_payments
""").fetchone()[0]


# =====================================================
# 4. AUDIT VALIDATION
# =====================================================

audit_exception_count = con.execute("""
    SELECT COUNT(*)
    FROM audits.audit_orders_without_items
""").fetchone()[0]


# =====================================================
# 5. DIFFERENCES
# =====================================================

order_count_difference = raw_orders - staging_orders

product_revenue_difference = (
    item_revenue - mart_product_revenue
)

total_revenue_difference = (
    item_total_revenue - mart_total_revenue
)

payment_vs_product_revenue = (
    payment_value - item_revenue
)


# =====================================================
# 6. VALIDATION FLAGS
# =====================================================

orders_match = order_count_difference == 0

product_revenue_match = (
    abs(product_revenue_difference) < 0.01
)

total_revenue_match = (
    abs(total_revenue_difference) < 0.01
)


# =====================================================
# 7. SUMMARY
# =====================================================

print("ROW COUNTS")
print("-" * 50)

print(f"Raw orders:                  {raw_orders:,}")
print(f"Staging orders:              {staging_orders:,}")
print(f"Order item rows:             {order_item_rows:,}")
print(f"Orders with items:           {itemized_orders:,}")
print(f"Orders without items:        {orders_without_items:,}")


print("\nREVENUE")
print("-" * 50)

print(f"Product revenue:             BRL {item_revenue:,.2f}")
print(f"Freight revenue:             BRL {item_freight:,.2f}")
print(f"Total item revenue:          BRL {item_total_revenue:,.2f}")

print(f"Mart product revenue:        BRL {mart_product_revenue:,.2f}")
print(f"Mart total revenue:          BRL {mart_total_revenue:,.2f}")

print(
    f"Product revenue difference:  "
    f"BRL {product_revenue_difference:,.2f}"
)

print(
    f"Total revenue difference:    "
    f"BRL {total_revenue_difference:,.2f}"
)


print("\nPAYMENTS")
print("-" * 50)

print(f"Payment value:               BRL {payment_value:,.2f}")

print(
    f"Payment vs product revenue:  "
    f"BRL {payment_vs_product_revenue:,.2f}"
)


print("\nDATA QUALITY AUDIT")
print("-" * 50)

print(
    f"Unexpected orders without items: "
    f"{audit_exception_count:,}"
)


print("\nVALIDATION")
print("-" * 50)

print(
    f"Raw -> Staging orders:        "
    f"{'PASS' if orders_match else 'FAIL'}"
)

print(
    f"Product revenue reconcile:    "
    f"{'PASS' if product_revenue_match else 'FAIL'}"
)

print(
    f"Total revenue reconcile:      "
    f"{'PASS' if total_revenue_match else 'FAIL'}"
)

print(
    f"Audit exceptions:             "
    f"{audit_exception_count:,}"
)


print("\n=====================================================\n")

con.close()