USE PyTestDb;
GO

IF OBJECT_ID('dbo.PyTestTable', 'U') IS NOT NULL
    DROP TABLE dbo.PyTestTable;
GO

CREATE TABLE dbo.PyTestTable
(
    -- Identity / row version (auto-managed)
    Id                  INT             IDENTITY(1,1) PRIMARY KEY,
    ColRowVersion       ROWVERSION                      NOT NULL,   -- auto-generated

    -- Exact numerics
    ColBigInt           BIGINT,
    ColInt              INT,
    ColSmallInt         SMALLINT,
    ColTinyInt          TINYINT,
    ColBit              BIT,
    ColDecimal          DECIMAL(18,4),
    ColNumeric          NUMERIC(10,2),
    ColMoney            MONEY,
    ColSmallMoney       SMALLMONEY,

    -- Approximate numerics
    ColFloat            FLOAT,
    ColReal             REAL,

    -- Date / time
    ColDate             DATE,
    ColTime             TIME(7),
    ColDateTime         DATETIME,
    ColDateTime2        DATETIME2(7),
    ColDateTimeOffset   DATETIMEOFFSET(7),
    ColSmallDateTime    SMALLDATETIME,

    -- Non-Unicode character strings
    ColChar             CHAR(10),
    ColVarChar          VARCHAR(100),
    ColVarCharMax       VARCHAR(MAX),

    -- Unicode character strings
    ColNChar            NCHAR(10),
    ColNVarChar         NVARCHAR(100),
    ColNVarCharMax      NVARCHAR(MAX),

    -- Binary strings
    ColBinary           BINARY(16),
    ColVarBinary        VARBINARY(100),
    ColVarBinaryMax     VARBINARY(MAX),

    -- Other / specialized
    ColUniqueIdentifier UNIQUEIDENTIFIER,
    ColXml              XML,
    ColSqlVariant       SQL_VARIANT,
    ColHierarchyId      HIERARCHYID,
    ColGeography        GEOGRAPHY,
    ColGeometry         GEOMETRY
);
GO
