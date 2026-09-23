/*==============================================================================
Database : MFInvestmentDB Project : Mutual Fund Investment Analytics
Dashboard Author : Vishal Surwase

Description: Creates the complete database schema for the Mutual Fund
Investment Analytics project.

Tables: 1. FundMaster 2. NAVHistory 3. Transactions
==============================================================================*/

IF DB_ID(ΓÇÿMFInvestmentDBΓÇÖ) IS NULL BEGIN CREATE DATABASE MFInvestmentDB;
END GO

USE MFInvestmentDB; GO

/==============================================================================
Table : FundMaster Purpose: Stores master information for all tracked
mutual funds.
==============================================================================/
IF OBJECT_ID(ΓÇÿdbo.FundMasterΓÇÖ,ΓÇÿUΓÇÖ) IS NOT NULL DROP TABLE
dbo.FundMaster; GO

CREATE TABLE dbo.FundMaster ( FundID INT IDENTITY(1,1) NOT NULL,
SchemeCode INT NOT NULL, FundName VARCHAR(250) NOT NULL, AMC VARCHAR(50)
NOT NULL, FundCategory VARCHAR(50) NOT NULL, ISINGrowth VARCHAR(20)
NULL, ISINReinvestment VARCHAR(20) NULL, ConfiguredSIPDay TINYINT NOT
NULL, AlertThreshold DECIMAL(5,2) NOT NULL, IsActive BIT NOT NULL
CONSTRAINT DF_FundMaster_IsActive DEFAULT (1), CreatedDate DATETIME NOT
NULL CONSTRAINT DF_FundMaster_CreatedDate DEFAULT (GETDATE()),
LastUpdated DATETIME NULL,

    CONSTRAINT PK_FundMaster PRIMARY KEY CLUSTERED (FundID),
    CONSTRAINT UQ_FundMaster_SchemeCode UNIQUE (SchemeCode)

); GO

/==============================================================================
Table : NAVHistory Purpose: Stores historical NAV values for tracked
mutual funds.
==============================================================================/
IF OBJECT_ID(ΓÇÿdbo.NAVHistoryΓÇÖ,ΓÇÿUΓÇÖ) IS NOT NULL DROP TABLE
dbo.NAVHistory; GO

CREATE TABLE dbo.NAVHistory ( NAVID INT IDENTITY(1,1) NOT NULL, FundID
INT NOT NULL, NAVDate DATE NOT NULL, NAV DECIMAL(18,4) NOT NULL,
CreatedDate DATETIME NOT NULL CONSTRAINT DF_NAVHistory_CreatedDate
DEFAULT(GETDATE()),

    CONSTRAINT PK_NAVHistory PRIMARY KEY CLUSTERED (NAVID),
    CONSTRAINT UQ_NAVHistory_Fund_Date UNIQUE (FundID,NAVDate),
    CONSTRAINT FK_NAVHistory_FundMaster
        FOREIGN KEY(FundID)
        REFERENCES dbo.FundMaster(FundID)

); GO

/==============================================================================
Table : Transactions Purpose: Stores mutual fund BUY/SELL transactions.
==============================================================================/
IF OBJECT_ID(ΓÇÿdbo.TransactionsΓÇÖ,ΓÇÿUΓÇÖ) IS NOT NULL DROP TABLE
dbo.Transactions; GO

CREATE TABLE dbo.Transactions ( TransactionID INT IDENTITY(1,1) NOT
NULL, FundID INT NOT NULL, TransactionDate DATE NOT NULL,
TransactionType VARCHAR(20) NOT NULL, Amount DECIMAL(12,2) NOT NULL, NAV
DECIMAL(18,4) NOT NULL, Units DECIMAL(18,6) NOT NULL, CreatedDate
DATETIME NOT NULL CONSTRAINT DF_Transactions_CreatedDate
DEFAULT(GETDATE()),

    CONSTRAINT PK_Transactions PRIMARY KEY CLUSTERED (TransactionID),
    CONSTRAINT FK_Transactions_FundMaster
        FOREIGN KEY(FundID)
        REFERENCES dbo.FundMaster(FundID)

); GO

/==============================================================================
Helpful Indexes
==============================================================================/
CREATE INDEX IX_NAVHistory_FundID ON dbo.NAVHistory(FundID); CREATE
INDEX IX_NAVHistory_NAVDate ON dbo.NAVHistory(NAVDate); CREATE INDEX
IX_Transactions_FundID ON dbo.Transactions(FundID); CREATE INDEX
IX_Transactions_TransactionDate ON dbo.Transactions(TransactionDate); GO

/==============================================================================
Verification Queries
==============================================================================/
SELECT * FROM dbo.FundMaster; SELECT * FROM dbo.NAVHistory; SELECT *
FROM dbo.Transactions; GO
