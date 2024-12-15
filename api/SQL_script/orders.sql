CREATE TABLE order (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quantity INTEGER NOT NULL,
    price FLOAT NOT NULL,
    status VARCHAR(100) NOT NULL,
    payment_id VARCHAR(1000) NOT NULL,
    customer_link INTEGER NOT NULL,
    product_link INTEGER NOT NULL,
    FOREIGN KEY (customer_link) REFERENCES customer (id),
    FOREIGN KEY (product_link) REFERENCES product (id)
);