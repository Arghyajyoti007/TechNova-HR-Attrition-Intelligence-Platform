-- ─────────────────────────────────────────────
-- SQL Warmups
-- ─────────────────────────────────────────────
SELECT * FROM employees LIMIT 1;
SELECT * FROM performance LIMIT 1;
SELECT * FROM satisfaction LIMIT 1;
SELECT * FROM attendance LIMIT 1;

-- Show all columns from employees table for the first 5 rows.
SELECT * FROM employees LIMIT 5;

-- Count how many employees are in each Department. Order by count descending.
SELECT 
    Department,
    COUNT(EmployeeID) AS TotalEmployees
FROM employees
GROUP BY Department
ORDER BY TotalEmployees DESC;

-- Calculate attrition rate percentage per Department.
-- Show Department, TotalEmployees, AttritionCount, AttritionRate.
-- Round AttritionRate to 2 decimal places.
SELECT 
    Department,
    COUNT(EmployeeID) AS TotalEmployees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS AttritionCount,
    ROUND(
        SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 
        / COUNT(EmployeeID)
    , 2) AS AttritionRate
FROM employees
GROUP BY Department
ORDER BY AttritionRate DESC;


-- Join employees and performance tables on EmployeeID.
-- Show EmployeeID, Name, Department, OverTime, PerformanceRating
-- Only for employees where Attrition = 'Yes'
SELECT 
    e.EmployeeID, 
    e.Name, e.Department, 
    p.OverTime, 
    p.PerformanceRating 
FROM employees e 
INNER JOIN performance p 
ON e.EmployeeID = p.EmployeeID
WHERE e.Attrition = 'Yes';


-- Add a new column called RiskLevel based on these rules:
-- JobSatisfaction = 1 OR WorkLifeBalance = 1 → 'High Risk'
-- JobSatisfaction = 2 OR WorkLifeBalance = 2 → 'Medium Risk'
-- Everything else → 'Low Risk'
-- Show EmployeeID, JobSatisfaction, WorkLifeBalance, RiskLevel
SELECT 
    EmployeeID, JobSatisfaction, WorkLifeBalance,
    CASE 
        WHEN JobSatisfaction = 1 OR WorkLifeBalance = 1 THEN 'High Risk'
        WHEN JobSatisfaction = 2 OR WorkLifeBalance = 2 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS RiskLevel
FROM satisfaction;
