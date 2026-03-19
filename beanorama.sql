CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer VARCHAR(100),
    category VARCHAR(100),
    item VARCHAR(100),
    size VARCHAR(50),
    quantity INT,
    total DECIMAL(10,2)
);
