-- Create dataset (if not already exists)
CREATE SCHEMA IF NOT EXISTS `dbt-hackathon-genai.dbt_vlakhmapurkar`
OPTIONS(location="US");

-- Create raw customers table
CREATE OR REPLACE TABLE `dbt-hackathon-genai.dbt_vlakhmapurkar.customers` (
  customer_id INT64,
  first_name STRING,
  last_name STRING,
  email STRING,
  signup_date DATE
);

-- Create raw orders table
CREATE OR REPLACE TABLE `dbt-hackathon-genai.dbt_vlakhmapurkar.orders` (
  order_id INT64,
  customer_id INT64,
  order_date DATE,
  total_amount NUMERIC
);

-- Create raw products table
CREATE OR REPLACE TABLE `dbt-hackathon-genai.dbt_vlakhmapurkar.products` (
  product_id INT64,
  product_name STRING,
  category STRING,
  price NUMERIC
);

-- (Optional) Insert some sample data for testing
INSERT INTO `dbt-hackathon-genai.dbt_vlakhmapurkar.customers`
(customer_id, first_name, last_name, email, signup_date)
VALUES
(1, "Alice", "Smith", "alice@example.com", DATE("2024-01-01")),
(2, "Bob", "Jones", "bob@example.com", DATE("2024-02-15"));

INSERT INTO `dbt-hackathon-genai.dbt_vlakhmapurkar.orders`
(order_id, customer_id, order_date, total_amount)
VALUES
(101, 1, DATE("2024-03-01"), 250.00),
(102, 2, DATE("2024-03-05"), 125.50);

INSERT INTO `dbt-hackathon-genai.dbt_vlakhmapurkar.products`
(product_id, product_name, category, price)
VALUES
(1001, "Laptop", "Electronics", 999.99),
(1002, "Headphones", "Electronics", 199.99);
