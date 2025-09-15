-- Case 1:
SELECT *
FROM Customers
WHERE city = 'New York' OR grade > 100;

-- Case 2:
SELECT *
FROM Customers
WHERE city = 'New York' AND grade > 100;
