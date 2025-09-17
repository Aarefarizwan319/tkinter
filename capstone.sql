CREATE TABLE IF NOT EXISTS Salesman (
  Salesman_id TEXT PRIMARY KEY,
  name TEXT,
  city TEXT,
  Comission REAL
);

-- Insert sample data into the Salesman table
INSERT INTO Salesman (Salesman_id, name, city, Comission) VALUES
  ('5001', 'James Hoog', 'New York', 0.15),
  ('5002', 'Nail Knite', 'Paris', 0.13),
  ('5005', 'Pit Alex', 'London', 0.11),
  ('5006', 'Mc Lyon', 'Paris', 0.14),
  ('5007', 'Paul Adam', 'Rome', 0.13),
  ('5003', 'Lauson Hen', 'San Jose', 0.12);

-- Create the Customer table if it does not exist
CREATE TABLE IF NOT EXISTS Customer (
  customer_id TEXT,
  cust_name TEXT PRIMARY KEY,
  city TEXT,
  grade INTEGER,
  Salesman_id TEXT,
  FOREIGN KEY (Salesman_id) REFERENCES Salesman(Salesman_id)
);

-- Insert sample data into the Customer table
INSERT INTO Customer (customer_id, cust_name, city, grade, Salesman_id) VALUES
  ('3002', 'nick rimando', 'new york', 100, '5001'),
  ('3007', 'brad davis', 'new york', 200, '5001'),
  ('3005', 'graham zusi', 'california', 200, '5002'),
  ('3008', 'julian green', 'london', 300, '5002'),
  ('3004', 'fabian johnson', 'paris', 300, '5006'),
  ('3009', 'geoff cameron', 'berlin', 100, '5003'),
  ('3003', 'jozy altidor', 'moscow', 200, '5007'),
  ('3001', 'brad guzan', 'london', NULL, '5005');

-- Create the Orders table if it does not exist
CREATE TABLE IF NOT EXISTS Orders (
  ord_no TEXT PRIMARY KEY,
  purch_amt REAL,
  ord_date TEXT,
  customer_id TEXT,
  Salesman_id TEXT,
  FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
  FOREIGN KEY (Salesman_id) REFERENCES Salesman(Salesman_id)
);

-- Insert sample data into the Orders table
INSERT INTO Orders (ord_no, purch_amt, ord_date, customer_id, Salesman_id) VALUES
  ('70001', 150.5, '2012-10-05', '3005', '5002'),
  ('70009', 270.65, '2012-09-10', '3001', '5001'),
  ('70002', 65.26, '2012-10-05', '3002', '5003'),
  ('70004', 110.5, '2012-08-17', '3009', '5007'),
  ('70007', 948.5, '2012-09-10', '3005', '5005'),
  ('70005', 2400.6, '2012-07-27', '3007', '5006');

-- Linking customers to their salesmen
SELECT Customer.cust_name, Salesman.name
FROM Customer
JOIN Salesman ON Customer.salesman_id = Salesman.salesman_id;

-- Fetching orders where customer's city does not match salesman's city
SELECT Orders.ord_no, Customer.cust_name, Orders.customer_id, Orders.salesman_id
FROM Orders
JOIN Customer ON Orders.customer_id = Customer.customer_id
JOIN Salesman ON Orders.salesman_id = Salesman.salesman_id
WHERE Customer.city <> Salesman.city;

-- Fetching all orders with customer names
SELECT Orders.ord_no, Customer.cust_name
FROM Orders
JOIN Customer ON Orders.customer_id = Customer.customer_id;


SELECT cust_name AS "Customer", grade AS "Grade"
FROM Customer
WHERE grade IS NOT NULL;


SELECT Customer.cust_name AS "Customer",
Customer.city AS "City",
Salesman.name AS "Salesman",
Salesman.Comission 
FROM Customer
JOIN Salesman ON Customer.salesman_id = Salesman.salesman_id
WHERE Salesman.Comission BETWEEN 0.12 AND 0.14;

-- Calculating commissions for orders where customer grade is 200 or more
SELECT Orders.ord_no, Customer.cust_name, Salesman.comission AS "Commission",
Orders.purch_amt * Salesman.comission AS "Comission"
FROM Orders
JOIN Salesman ON Orders.salesman_id = Salesman.salesman_id
JOIN Customer ON Orders.customer_id = Customer.customer_id
WHERE Customer.grade >= 200;

-- Orders on a specific date
SELECT *
FROM Customer
JOIN Orders ON Customer.customer_id = Orders.customer_id
WHERE Orders.ord_date = '2012-10-05';
