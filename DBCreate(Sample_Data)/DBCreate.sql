SET SQL_SAFE_UPDATES = 0;
-- drop database if exists CreateDB;
create database CreateDB;
use CreateDB;


DROP TABLE IF EXISTS order_history;
DROP TABLE IF EXISTS mileage_history;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS shopping_malls;

-- 쇼핑몰 정보 테이블
CREATE TABLE shopping_malls (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    entry_date DATE,
    contact_number VARCHAR(20),
    accumulated_platform_fee DECIMAL(10, 2)
);

-- 상품 정보 테이블
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    price DECIMAL(10, 2),
    mall_id INT,
    FOREIGN KEY (mall_id) REFERENCES shopping_malls(id)
);

-- 외래 키 관계 설정
ALTER TABLE products
ADD FOREIGN KEY (mall_id) REFERENCES shopping_malls(id);


-- 고객 정보 테이블
CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_Login_id VARCHAR(255),
    pass_W VARCHAR(255),
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(255),
    address VARCHAR(255),
    total_purchase_amount DECIMAL(10, 2),
    total_mileage DECIMAL(10, 2),
    entryD DATE
);

-- 주문 정보 테이블
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    customer_id INT,
    order_date DATE,
    order_amount DECIMAL(10, 2),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- 주문 히스토리 정보 테이블
CREATE TABLE order_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    order_id INT,
    order_date DATE,
    order_amount DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- 마일리지 히스토리 정보 테이블
CREATE TABLE mileage_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT,
    date DATE,
    used_mileage DECIMAL(10, 2),
    remaining_mileage DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

INSERT INTO shopping_malls (name, entry_date, contact_number, accumulated_platform_fee)
VALUES
    ('안산몰', '2021-05-13', '010-1234-5678', 0),
    ('인천샵', '2023-12-05', '010-4321-5678', 0),
    ('네오샵', '2015-03-20', '010-5678-1234', 0),
    ('상록샵', '2022-07-21', '010-7890-1234', 0);

-- 상품 정보 예시 데이터 삽입
INSERT INTO products (name, price, mall_id)
VALUES
    ('ProductA', 50.00, 1),
    ('ProductB', 30.00, 1),
    ('ProductC', 25.00, 2),
    ('ProductD', 40.00, 2),
    ('ProductE', 60.00, 3),
    ('ProductF', 35.00, 3),
	('ProductG', 55.00, 4),
    ('ProductH', 80.00, 4);


-- 고객 정보 예시 데이터 삽입
INSERT INTO customers (user_Login_id, pass_W, name, email, phone, address, total_purchase_amount, total_mileage,entryD)
VALUES
    ('qkqkhih', '1234', '김우혁', 'qkqkhih@naver.com', '010-0000-0000', '인천 서구', 0, 0,'2022-01-01'),
    ('user1', '1234', '홍길동', 'user@ansan.ac.kr', '010-1234-5678', '경기도 안산시 상록구', 0, 0,'2021-05-03'),
    ('user2', '1234', '김디비', 'user2@ansan.ac.kr', '010-5678-1234', '서울 강남구', 0, 0,'2020-03-11');

-- 주문 정보 예시 데이터 삽입
INSERT INTO orders (product_id, customer_id, order_date, order_amount)
VALUES
    (1, 1, '2022-01-05', 100.00),
    (2, 1, '2023-02-10', 60.00),
    (3, 2, '2022-03-15', 25.00),
    (4, 2, '2022-03-18', 40.00),
    (5, 3, '2022-04-01', 120.00),
    (6, 3, '2022-04-05', 70.00),
	(7, 3, '2023-10-01', 110.00);
    
-- 주문 히스토리 예시 데이터 삽입
INSERT INTO order_history (customer_id, order_id, order_date, order_amount)
VALUES
    (1, 1, '2022-01-05', 100.00),
    (1, 2, '2022-02-10', 60.00),
    (2, 3, '2022-03-15', 25.00),
    (2, 4, '2022-03-18', 40.00),
    (3, 5, '2022-04-01', 120.00),
    (3, 6, '2022-04-05', 70.00);

-- 마일리지 히스토리 예시 데이터 삽입
INSERT INTO mileage_history (customer_id, date, used_mileage, remaining_mileage)
VALUES
    (1, '2022-01-07', 20.00, 80.00),
    (2, '2022-03-20', 10.00, 30.00),
    (3, '2022-04-10', 50.00, 20.00);

-- A.1 ~ A.2
call CalculatePlatformFee(NULL);

-- B.3 ~ B.7
CALL CalculateSalesAndProfitsByMall('안산몰');
CALL CalculateSalesAndProfitsByMall('인천샵');
CALL CalculateSalesAndProfitsByMall('네오샵');
CALL CalculateSalesAndProfitsByMall('상록샵');

-- C.8 ~ C.10
CALL GetMonthlyInfo('qkqkhih');
CALL GetMonthlyInfo('user1');
CALL GetMonthlyInfo('user2');
