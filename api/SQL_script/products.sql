CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name VARCHAR(100) NOT NULL,
    current_price FLOAT NOT NULL,
    previous_price FLOAT NOT NULL,
    in_stock INTEGER NOT NULL,
    product_picture VARCHAR(1000) NOT NULL,
    flash_sale BOOLEAN DEFAULT FALSE,
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP
);