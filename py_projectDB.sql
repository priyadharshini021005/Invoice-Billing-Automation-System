CREATE DATABASE invoice_billing_system;
USE invoice_billing_system;
drop database invoice_billing_system ;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'Admin'
);

CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(100),
    address VARCHAR(255)
);

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2),
    stock INT,
    gst DECIMAL(5,2)
);

CREATE TABLE invoices (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    invoice_date DATE,
    subtotal DECIMAL(10,2),
    gst_amount DECIMAL(10,2),
    discount DECIMAL(10,2),
    grand_total DECIMAL(10,2),
    payment_mode VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE invoice_items(
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2),
    total DECIMAL(10,2),
    FOREIGN KEY(invoice_id) REFERENCES invoices(invoice_id),
    FOREIGN KEY(product_id) REFERENCES products(product_id)
);

SHOW TABLES;

INSERT INTO users (username, password, role)
VALUES ('admin', 'admin123', 'Admin');

INSERT INTO customers (customer_name, phone, email, address)
VALUES
('Rahul', '9876543210', 'rahul@gmail.com', 'Chennai'),
('Priya', '9876501234', 'priya@gmail.com', 'Coimbatore'),
('Arun', '9876512345', 'arun@gmail.com', 'Madurai');

INSERT INTO products
(product_name, category, price, stock, gst)
VALUES
('Laptop', 'Electronics', 55000.00, 20, 18),
('Wireless Mouse', 'Electronics', 750.00, 100, 18),
('Keyboard', 'Electronics', 1200.00, 80, 18),
('USB Pendrive 64GB', 'Accessories', 650.00, 50, 18),
('External Hard Disk 1TB', 'Storage', 4500.00, 25, 18),
('Printer', 'Electronics', 8500.00, 15, 18),
('A4 Paper Bundle', 'Stationery', 250.00, 200, 12),
('Calculator', 'Stationery', 450.00, 60, 12),
('Office Chair', 'Furniture', 3500.00, 10, 18),
('Computer Table', 'Furniture', 5500.00, 8, 18);

SELECT * FROM users;

SELECT * FROM customers;

SELECT customer_id, customer_name, phone, email, address
FROM customers
ORDER BY customer_id DESC;

SELECT * FROM products;

DESC products;
CREATE TABLE bills(
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    bill_date DATE,
    payment_method VARCHAR(30),
    subtotal DECIMAL(10,2),
    gst_amount DECIMAL(10,2),
    discount DECIMAL(10,2),
    grand_total DECIMAL(10,2),
    FOREIGN KEY(customer_id)
    REFERENCES customers(customer_id)
);


CREATE TABLE bill_items(
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    bill_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2),
    gst DECIMAL(10,2),
    total DECIMAL(10,2),
    FOREIGN KEY(bill_id)
    REFERENCES bills(bill_id),
    FOREIGN KEY(product_id)
    REFERENCES products(product_id)
);



