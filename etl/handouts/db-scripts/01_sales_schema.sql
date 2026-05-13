
CREATE TABLE IF NOT EXISTS sales_data (
    customer_id int NOT NULL,
    purchase_date date,
    purchase_amount decimal(19,2),
    product_id varchar(10)
);

CREATE TABLE IF NOT EXISTS customer_spend (
    customer_id int NOT NULL,
    average_spend decimal(19,2),
    total_spend decimal(19,2)
);

CREATE TABLE IF NOT EXISTS customer_products (
    customer_id int NOT NULL,
    product_id varchar(10),
    quantity int
);

/* The following will scrub old data */

TRUNCATE TABLE sales_data;
TRUNCATE TABLE customer_spend;
TRUNCATE TABLE customer_products;
