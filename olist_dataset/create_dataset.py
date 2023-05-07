import pandas as pd

orders = pd.read_csv("https://github.com/sarahlbe/redi/blob/main/olist_orders_dataset.csv?raw=True")
customers = pd.read_csv("https://github.com/sarahlbe/redi/blob/main/olist_customers_dataset.csv?raw=True")
orders_items = pd.read_csv("https://github.com/obreit/redi/raw/master/olist_dataset/olist_order_items_dataset.csv.zip")
reviews = pd.read_csv("https://github.com/obreit/redi/raw/master/olist_dataset/olist_order_reviews_dataset.csv.zip")

def process_orders(orders_df):
    return orders_df \
        .drop(columns=['order_approved_at', 'order_delivered_carrier_date', 'order_estimated_delivery_date', 'category_first_item_in_order']) \
        .rename(columns={'number_items_in_order': 'number_of_items', 'categories_all_items_in_order': 'categories_of_items'})

def process_customers(customers_df):
    return customers_df[['customer_id', 'customer_unique_id', 'customer_city', 'customer_state']]

def process_items(order_items_df):
    orders_cost_df = order_items_df.groupby('order_id')[['price', 'freight_value']].transform('sum')

    order_items_df[['order_price', 'order_shipping_cost']] = orders_cost_df
    order_items_df = order_items_df.drop_duplicates(subset=['order_id'], keep='first')

    return order_items_df[['order_id', 'order_price', 'order_shipping_cost']]

def process_reviews(reviews_df):
    reviews_avgs = reviews_df.groupby('order_id')['review_score'].transform('mean')

    reviews_df['avg_review_score'] = reviews_avgs
    reviews_df = reviews_df.drop_duplicates(subset=['order_id'], keep='first')

    return reviews_df[['order_id', 'avg_review_score']]

orders_enriched = process_orders(orders) \
    .merge(process_customers(customers), how='inner', on='customer_id').drop(columns=['customer_id']) \
    .merge(process_reviews(reviews), how='left', on='order_id') \
    .merge(process_items(orders_items), how='left', on='order_id') \
    [['order_id', 'order_status', 'number_of_items', 'categories_of_items', 'order_price', 'order_shipping_cost', 'avg_review_score', 'customer_city', 'customer_state', 'customer_unique_id', 'order_purchase_timestamp', 'order_delivered_customer_date']]

orders_enriched.to_csv('orders_enriched.csv.zip', index=False, compression='zip')