 
-- Day -4 Task 4: SQL Exploratory Data Analysis (EDA)
-- Customer Churn Analysis

---1. What percentage of customers have churned overall?
use [ ChurnDB];
WITH TotalCustomers AS (
    SELECT
        COUNT(*) AS Total_Customers
    FROM [dbo].[vw_ChurnData]
),
ChurnedCustomers AS (
    SELECT
        COUNT(*) AS Churned_Customers
    FROM [dbo].[vw_ChurnData]
    WHERE Churn = 1
)
SELECT
    CAST(
        100.0 * Churned_Customers / Total_Customers
        AS DECIMAL(10,2)
    ) AS Churn_Percentage
FROM TotalCustomers AS TC
CROSS JOIN ChurnedCustomers AS CC;

-- Insight:
-- Overall, 26.54% of customers have churned, indicating a considerable level of customer attrition.

--- 2. Which contract type (month-to-month, one year, two year) has the highest churn rate?

WITH cte_1 AS(
SELECT 
   Contract,
   COUNT(Contract) as Churned_Customers
   FROM [dbo].[vw_ChurnData]
   WHERE Churn = 1
   GROUP BY Contract),
cte_2 AS(
SELECT
  Contract,
  COUNT(*) AS Total_Customers
FROM [dbo].[vw_ChurnData]
GROUP BY  Contract),
cte_3 AS(
SELECT
   t1.Contract,
   Churned_Customers,
   Total_Customers
 FROM cte_1 as t1
 JOIN cte_2 as t2
ON t1.Contract = t2.Contract)
SELECT
   Contract,
   CAST(100.0 * Churned_Customers/Total_Customers AS DECIMAL(10,2)) AS Churn_Rate
FROM cte_3;

-- Insight:
-- Month-to-month customers have the highest churn rate at 42.71%.
-- Two-year contract customers have the lowest churn rate at 2.83%.
-- This shows that customers with longer contracts are less likely to leave the company.

---3. Do customers with higher MonthlyCharges churn more?

SELECT
   Churn,
   CAST(AVG(MonthlyCharges) AS DECIMAL(10,2)) AS Avg_Monthly_Charges 
FROM [dbo].[vw_ChurnData]
GROUP BY Churn

-- Insight:
-- Churned customers have higher monthly charges (74.44) compared to non-churned customers (61.27).
-- The difference is around 13, indicating that customers with higher monthly charges are more likely to churn.

---4. Does tenure (how long they've been a customer) relate to churn?

SELECT
    Churn,
    CAST(AVG(Tenure) AS DECIMAL(10,2)) AS Avg_Tenure
FROM [dbo].[vw_ChurnData]
GROUP BY Churn;

-- Insight:
-- There is a clear difference in the average tenure of churned and non-churned customers.
-- Non-churned customers stay for about 37 months, while churned customers stay for about 17 months.
-- This shows that customers who stay longer are less likely to churn.

---5. Does Gender Impact Churn?

SELECT
    gender,
    COUNT(*) AS Total_Customers,
    CAST(
        100.0 * SUM(CASE WHEN Churn = 1 THEN 1 ELSE 0 END) / COUNT(*)
        AS DECIMAL(10,2)
    ) AS Churn_Rate
FROM [dbo].[vw_ChurnData]
GROUP BY gender;

-- Insight:
-- There is very little difference in churn rates between male (26.16%) and female (26.92%) customers.
-- This shows that gender does not have a major impact on customer churn.

---6. Does payment method affect churn?

WITH cte_1 AS (
    SELECT
        PaymentMethod,
        COUNT(*) AS NumberofCustomerinpaymenttype
    FROM [dbo].[vw_ChurnData]
    GROUP BY PaymentMethod
),
cte_2 AS (
    SELECT
        PaymentMethod,
        COUNT(*) AS Churncustomers
    FROM [dbo].[vw_ChurnData]
    WHERE Churn = 1
    GROUP BY PaymentMethod
)
SELECT
    t1.PaymentMethod,
    NumberofCustomerinpaymenttype,
    CAST(100.0 * Churncustomers/NumberofCustomerinpaymenttype AS DECIMAL(10,2)) AS ChurnRate
FROM cte_1 AS t1
JOIN cte_2 AS t2
    ON t1.PaymentMethod = t2.PaymentMethod

-- Insight:
-- Electronic check customers have the highest churn rate at 45.29%.
-- Credit card customers have the lowest churn rate at 15.24%.
-- This shows that customers using electronic checks are more likely to churn.

 ---7. Does having TechSupport affect churn?
   SELECT
    TechSupport,
    COUNT(*) AS TotalCustomers,
    SUM(CASE WHEN Churn = 1 THEN 1 ELSE 0 END) AS ChurnedCustomers,
    CAST(
    100.0 * SUM(CASE WHEN Churn = 1 THEN 1 ELSE 0 END) / COUNT(*) AS DECIMAL(10,2)) AS ChurnRate
FROM [dbo].[vw_ChurnData]
GROUP BY TechSupport;

-- Insight:
-- Customers without tech support have a higher churn rate of 41.64%.
-- Customers with tech support have a lower churn rate of 15.17%.
-- This shows that customers with tech support are less likely to churn.