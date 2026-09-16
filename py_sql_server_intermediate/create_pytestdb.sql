/* ============================================================================
   PyTestDb — Intermediate SQL Server schema, seed data, and stored procedures
   ============================================================================
   This script is the SECOND step in the SQL Server series. The basics folder
   (`py_sql_server_basics`) created a single wide table (`dbo.PyTestTable`)
   that exercised every data type family. Here we build a small, REALISTIC
   relational schema so the intermediate lesson can teach real-world SQL:

       Customers  ──< Orders ──< OrderItems >── Products

   It is IDEMPOTENT: you can run it any number of times and it always ends in
   the same state. It drops the tables (and procedures) if they exist, then
   recreates them and seeds them with stable, predictable data.

   How to run it:
     - In SSMS: open this file and press F5 (Execute) against the `master`
       database — the script creates `PyTestDb` if it does not exist.
     - From the command line:
         sqlcmd -S localhost -E -i create_pytestdb.sql

   Docs:
     - CREATE TABLE:  https://learn.microsoft.com/sql/t-sql/statements/create-table-transact-sql
     - FOREIGN KEY:   https://learn.microsoft.com/sql/relational-databases/tables/primary-and-foreign-key-constraints
     - CREATE PROC:   https://learn.microsoft.com/sql/t-sql/statements/create-procedure-transact-sql
   ============================================================================ */

-- ---------------------------------------------------------------------------
-- 1. Make sure the database exists
-- ---------------------------------------------------------------------------
-- `IF DB_ID(...) IS NULL` checks whether the database already exists. If it
-- does not, we CREATE it. This makes the whole script safe to re-run.
IF DB_ID('PyTestDb') IS NULL
BEGIN
    CREATE DATABASE PyTestDb;
END;
GO

-- Switch context to PyTestDb so every statement below runs inside it.
USE PyTestDb;
GO

-- ---------------------------------------------------------------------------
-- 2. Drop existing objects (idempotency)
-- ---------------------------------------------------------------------------
-- We drop child tables before parent tables so FOREIGN KEY constraints never
-- block us. OrderItems references Orders and Products, so it goes first.
IF OBJECT_ID('dbo.OrderItems', 'U') IS NOT NULL DROP TABLE dbo.OrderItems;
IF OBJECT_ID('dbo.Orders',     'U') IS NOT NULL DROP TABLE dbo.Orders;
IF OBJECT_ID('dbo.Products',   'U') IS NOT NULL DROP TABLE dbo.Products;
IF OBJECT_ID('dbo.Customers',  'U') IS NOT NULL DROP TABLE dbo.Customers;

-- Drop the stored procedures too, so re-running always starts clean.
IF OBJECT_ID('dbo.usp_PlaceOrder',     'P') IS NOT NULL DROP PROCEDURE dbo.usp_PlaceOrder;
IF OBJECT_ID('dbo.usp_GetOrderDetails','P') IS NOT NULL DROP PROCEDURE dbo.usp_GetOrderDetails;
GO

-- ---------------------------------------------------------------------------
-- 3. Create the tables
-- ---------------------------------------------------------------------------

-- Customers: the "who" of the store.
CREATE TABLE dbo.Customers
(
    CustomerId  INT           IDENTITY(1,1) PRIMARY KEY,
    FirstName   NVARCHAR(50)  NOT NULL,
    LastName    NVARCHAR(50)  NOT NULL,
    Email       NVARCHAR(100) NOT NULL UNIQUE,
    City        NVARCHAR(50)  NOT NULL,
    CreatedDate DATE          NOT NULL DEFAULT CAST(GETDATE() AS DATE)
);

-- Products: the "what" we sell.
CREATE TABLE dbo.Products
(
    ProductId   INT            IDENTITY(1,1) PRIMARY KEY,
    ProductName NVARCHAR(100)  NOT NULL,
    Category    NVARCHAR(50)   NOT NULL,
    UnitPrice   DECIMAL(10,2)  NOT NULL,
    UnitsInStock INT           NOT NULL DEFAULT 0
);

-- Orders: the "when / who" of a purchase. One customer can have many orders.
CREATE TABLE dbo.Orders
(
    OrderId     INT          IDENTITY(1,1) PRIMARY KEY,
    CustomerId  INT          NOT NULL REFERENCES dbo.Customers(CustomerId),
    OrderDate   DATE         NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    Status      NVARCHAR(20) NOT NULL DEFAULT 'Pending'
);

-- OrderItems: the line items inside an order (the "how many / at what price").
CREATE TABLE dbo.OrderItems
(
    OrderItemId INT           IDENTITY(1,1) PRIMARY KEY,
    OrderId     INT           NOT NULL REFERENCES dbo.Orders(OrderId),
    ProductId   INT           NOT NULL REFERENCES dbo.Products(ProductId),
    Quantity    INT           NOT NULL CHECK (Quantity > 0),
    UnitPrice   DECIMAL(10,2) NOT NULL
);
GO

-- ---------------------------------------------------------------------------
-- 4. Seed data (stable, predictable Ids)
-- ---------------------------------------------------------------------------
-- We use SET IDENTITY_INSERT ON so we can control the Id values. This makes
-- every JOIN / stored-procedure example deterministic — the lesson always
-- knows which rows exist. We turn it OFF again right after each insert.
SET IDENTITY_INSERT dbo.Customers ON;
INSERT INTO dbo.Customers (CustomerId, FirstName, LastName, Email, City, CreatedDate)
VALUES
    (1, 'Alice',   'Nguyen',  'alice.nguyen@example.com',  'Seattle',  '2026-01-05'),
    (2, 'Bob',     'Smith',   'bob.smith@example.com',     'Portland', '2026-02-11'),
    (3, 'Carla',   'Garcia',  'carla.garcia@example.com',  'Austin',   '2026-03-02'),
    (4, 'David',   'Kim',     'david.kim@example.com',     'Seattle',  '2026-04-18'),
    (5, 'Elena',   'Rossi',   'elena.rossi@example.com',   'Denver',   '2026-05-27');
SET IDENTITY_INSERT dbo.Customers OFF;
GO

SET IDENTITY_INSERT dbo.Products ON;
INSERT INTO dbo.Products (ProductId, ProductName, Category, UnitPrice, UnitsInStock)
VALUES
    (1, 'Wireless Mouse',   'Electronics', 24.99,  120),
    (2, 'Mechanical Keyboard','Electronics', 89.50,  45),
    (3, 'USB-C Cable',      'Electronics', 12.75, 300),
    (4, 'Desk Lamp',        'Home Office', 34.20,  18),
    (5, 'Notebook (Pack)',  'Office',       9.99, 500),
    (6, 'Ergonomic Chair',  'Home Office', 199.00,  8);
SET IDENTITY_INSERT dbo.Products OFF;
GO

SET IDENTITY_INSERT dbo.Orders ON;
INSERT INTO dbo.Orders (OrderId, CustomerId, OrderDate, Status)
VALUES
    (1, 1, '2026-06-01', 'Shipped'),
    (2, 2, '2026-06-03', 'Pending'),
    (3, 1, '2026-06-10', 'Delivered'),
    (4, 3, '2026-06-15', 'Pending'),
    (5, 5, '2026-06-20', 'Cancelled');
SET IDENTITY_INSERT dbo.Orders OFF;
GO

SET IDENTITY_INSERT dbo.OrderItems ON;
INSERT INTO dbo.OrderItems (OrderItemId, OrderId, ProductId, Quantity, UnitPrice)
VALUES
    (1, 1, 1, 2, 24.99),
    (2, 1, 3, 1, 12.75),
    (3, 2, 2, 1, 89.50),
    (4, 3, 5, 4,  9.99),
    (5, 4, 4, 1, 34.20),
    (6, 5, 6, 1, 199.00);
SET IDENTITY_INSERT dbo.OrderItems OFF;
GO

-- ---------------------------------------------------------------------------
-- 5. Stored procedures
-- ---------------------------------------------------------------------------

-- usp_PlaceOrder: CREATE (insert) an order and its line items in ONE call.
-- It takes the customer and a list of (product, quantity) pairs, inserts the
-- order, then inserts each line item, and returns the new OrderId via an
-- OUTPUT parameter. This is the "Create via stored procedure" half of CRUD.
CREATE PROCEDURE dbo.usp_PlaceOrder
    @CustomerId INT,
    @ProductId  INT,
    @Quantity   INT,
    @OrderId    INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- Insert the order header.
    INSERT INTO dbo.Orders (CustomerId, OrderDate, Status)
    VALUES (@CustomerId, CAST(GETDATE() AS DATE), 'Pending');

    -- Capture the new identity value.
    SET @OrderId = SCOPE_IDENTITY();

    -- Insert the line item, using the product's current price.
    INSERT INTO dbo.OrderItems (OrderId, ProductId, Quantity, UnitPrice)
    SELECT @OrderId, @ProductId, @Quantity, UnitPrice
    FROM dbo.Products
    WHERE ProductId = @ProductId;
END;
GO

-- usp_GetOrderDetails: READ an order and its line items.
-- Takes an OrderId as INPUT, returns the customer + order header as a result
-- set, and returns the order total via an OUTPUT parameter.
CREATE PROCEDURE dbo.usp_GetOrderDetails
    @OrderId INT,
    @Total   DECIMAL(10,2) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- Header + customer info.
    SELECT o.OrderId, o.OrderDate, o.Status,
           c.FirstName, c.LastName, c.Email
    FROM dbo.Orders o
    JOIN dbo.Customers c ON c.CustomerId = o.CustomerId
    WHERE o.OrderId = @OrderId;

    -- Line items.
    SELECT oi.ProductId, p.ProductName, oi.Quantity, oi.UnitPrice
    FROM dbo.OrderItems oi
    JOIN dbo.Products p ON p.ProductId = oi.ProductId
    WHERE oi.OrderId = @OrderId;

    -- Compute the total into the OUTPUT parameter.
    SELECT @Total = SUM(Quantity * UnitPrice)
    FROM dbo.OrderItems
    WHERE OrderId = @OrderId;
END;
GO

-- ---------------------------------------------------------------------------
-- 6. Quick sanity check
-- ---------------------------------------------------------------------------
-- A tiny verification query so you can confirm the seed loaded correctly.
-- (Note: `RowCount` is a reserved keyword, so we alias it `TotalRows`.)
SELECT 'Customers' AS TableName, COUNT(*) AS TotalRows FROM dbo.Customers
UNION ALL SELECT 'Products',  COUNT(*) FROM dbo.Products
UNION ALL SELECT 'Orders',    COUNT(*) FROM dbo.Orders
UNION ALL SELECT 'OrderItems',COUNT(*) FROM dbo.OrderItems;
GO