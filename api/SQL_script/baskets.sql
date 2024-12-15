CREATE TABLE cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quantity INTEGER NOT NULL,
    customer_link INTEGER NOT NULL,
    product_link INTEGER NOT NULL,
    FOREIGN KEY (customer_link) REFERENCES customer (id),
    FOREIGN KEY (product_link) REFERENCES product (id)
);