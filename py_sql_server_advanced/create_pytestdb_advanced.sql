/* ============================================================================
   PyTestDb — Advanced SQL Server schema, seed data, indexes, views, trigger
   ============================================================================
   This script is the THIRD step in the SQL Server series. The intermediate
   folder (`py_sql_server_intermediate`) built a small, realistic relational
   store schema:

       Customers  ──< Orders ──< OrderItems >── Products

   Here we recreate that same schema and seed data, then ADD the objects an
   advanced lesson needs to teach performance, schema, and integration:

       • Indexes   — so the "indexes" and "query tuning" sections can show
                     the difference an index makes (SET STATISTICS TIME, IO).
       • Views     — so the "views" section has real views to query/update.
       • A trigger — so the "transactions & isolation" section can show an
                     audit log being written automatically.

   It is IDEMPOTENT: you can run it any number of times and it always ends in
   the same state. It drops the tables (and views, trigger, indexes) if they
   exist, then recreates them and seeds them with stable, predictable data.

   How to run it:
     - In SSMS: open this file and press F5 (Execute) against the `master`
       database — the script creates `PyTestDb` if it does not exist.
     - From the command line:
         sqlcmd -S localhost -E -i create_pytestdb_advanced.sql

   Docs:
     - CREATE TABLE:  https://learn.microsoft.com/sql/t-sql/statements/create-table-transact-sql
     - CREATE INDEX:  https://learn.microsoft.com/sql/t-sql/statements/create-index-transact-sql
     - CREATE VIEW:   https://learn.microsoft.com/sql/t-sql/statements/create-view-transact-sql
     - CREATE TRIGGER:https://learn.microsoft.com/sql/t-sql/statements/create-trigger-transact-sql
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
-- Views, the trigger, and the audit table must be dropped before the tables
-- they depend on.
IF OBJECT_ID('dbo.v_ProductSales',   'V') IS NOT NULL DROP VIEW  dbo.v_ProductSales;
IF OBJECT_ID('dbo.v_CustomerOrders', 'V') IS NOT NULL DROP VIEW  dbo.v_CustomerOrders;
IF OBJECT_ID('dbo.trg_Orders_Audit', 'TR') IS NOT NULL DROP TRIGGER dbo.trg_Orders_Audit;
IF OBJECT_ID('dbo.OrderStatusAudit', 'U') IS NOT NULL DROP TABLE dbo.OrderStatusAudit;
-- Tables written by the pandas sections (8 & 9) via to_sql — drop them too
-- so re-running setup always starts clean.
IF OBJECT_ID('dbo.TopProductsByCategory', 'U') IS NOT NULL DROP TABLE dbo.TopProductsByCategory;
IF OBJECT_ID('dbo.OrderStatusSummary',    'U') IS NOT NULL DROP TABLE dbo.OrderStatusSummary;
IF OBJECT_ID('dbo.OrderItems', 'U') IS NOT NULL DROP TABLE dbo.OrderItems;
IF OBJECT_ID('dbo.Orders',     'U') IS NOT NULL DROP TABLE dbo.Orders;
IF OBJECT_ID('dbo.Products',   'U') IS NOT NULL DROP TABLE dbo.Products;
IF OBJECT_ID('dbo.Customers',  'U') IS NOT NULL DROP TABLE dbo.Customers;
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
-- every JOIN / window-function / view example deterministic — the lesson
-- always knows which rows exist. We turn it OFF again right after each insert.
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
-- 5. Indexes
-- ---------------------------------------------------------------------------
-- An index is a sorted copy of a column (or columns) that lets SQL Server
-- find rows without scanning the whole table. The "indexes" and "query
-- tuning" sections run the SAME query with and without these to show the
-- difference in logical reads and elapsed time.

-- A simple index on the foreign key Orders.CustomerId. Every JOIN from
-- Customers -> Orders can now seek straight to that customer's orders.
CREATE INDEX IX_Orders_CustomerId ON dbo.Orders(CustomerId);

-- A "covering" index on OrderItems. It covers the columns the sales query
-- needs (OrderId, ProductId, Quantity, UnitPrice), so SQL Server can answer
-- the query entirely from the index without touching the table at all.
CREATE INDEX IX_OrderItems_OrderId_Product
    ON dbo.OrderItems(OrderId, ProductId)
    INCLUDE (Quantity, UnitPrice);
GO

-- ---------------------------------------------------------------------------
-- 6. Views
-- ---------------------------------------------------------------------------
-- A view is a saved SELECT statement you can query like a table. It does not
-- store data — it runs the underlying query each time you SELECT from it.

-- v_CustomerOrders: a convenient "customer + order" summary. The "views"
-- section queries this instead of writing the JOIN every time.
CREATE VIEW dbo.v_CustomerOrders AS
SELECT o.OrderId,
       o.OrderDate,
       o.Status,
       c.FirstName,
       c.LastName,
       c.City
FROM dbo.Orders o
JOIN dbo.Customers c ON c.CustomerId = o.CustomerId;
GO

-- v_ProductSales: an aggregated sales view. The "views" section also shows
-- how to UPDATE through a simple view (one that maps to a single table).
CREATE VIEW dbo.v_ProductSales AS
SELECT p.ProductId,
       p.ProductName,
       p.Category,
       SUM(oi.Quantity)              AS TotalSold,
       SUM(oi.Quantity * oi.UnitPrice) AS TotalRevenue
FROM dbo.Products p
LEFT JOIN dbo.OrderItems oi ON oi.ProductId = p.ProductId
GROUP BY p.ProductId, p.ProductName, p.Category;
GO

-- ---------------------------------------------------------------------------
-- 7. Trigger (audit log)
-- ---------------------------------------------------------------------------
-- A trigger is SQL that runs automatically when a table changes. This one
-- writes a row to an audit table every time an order's Status changes, so
-- the "transactions & isolation" section can show the audit trail being
-- written automatically inside the same transaction.

-- The audit table (created here, dropped with the trigger above).
CREATE TABLE dbo.OrderStatusAudit
(
    AuditId    INT           IDENTITY(1,1) PRIMARY KEY,
    OrderId    INT           NOT NULL,
    OldStatus  NVARCHAR(20)  NULL,
    NewStatus  NVARCHAR(20)  NOT NULL,
    ChangedAt  DATETIME2(3)  NOT NULL DEFAULT SYSDATETIME()
);
GO

-- The trigger fires AFTER an UPDATE to dbo.Orders and logs every changed row.
CREATE TRIGGER dbo.trg_Orders_Audit
ON dbo.Orders
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO dbo.OrderStatusAudit (OrderId, OldStatus, NewStatus)
    SELECT i.OrderId, d.Status, i.Status
    FROM INSERTED i
    JOIN DELETED d ON d.OrderId = i.OrderId
    WHERE ISNULL(d.Status, '') <> ISNULL(i.Status, '');
END;
GO

-- ---------------------------------------------------------------------------
-- 8. Quick sanity check
-- ---------------------------------------------------------------------------
-- A tiny verification query so you can confirm the seed loaded correctly.
-- (Note: `RowCount` is a reserved keyword, so we alias it `TotalRows`.)
SELECT 'Customers' AS TableName, COUNT(*) AS TotalRows FROM dbo.Customers
UNION ALL SELECT 'Products',  COUNT(*) FROM dbo.Products
UNION ALL SELECT 'Orders',    COUNT(*) FROM dbo.Orders
UNION ALL SELECT 'OrderItems',COUNT(*) FROM dbo.OrderItems;
GO