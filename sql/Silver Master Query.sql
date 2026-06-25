-- ─────────────────────────────────────────────
-- The Silver Master Query
-- Silver transformation does 4 things:
-- 1. JOIN all 4 tables into one master employee table
-- 2. Clean nulls
-- 3. Add derived columns (RiskLevel, AttritionFlag)
-- 4. Save as Delta table
-- ─────────────────────────────────────────────

SELECT 
    -- From employees table
    e.EmployeeID,	
    e.Name,	
    e.Age,	
    e.Gender,	
    e.MaritalStatus,	
    e.Education,	
    e.EducationField,	
    e.Department,	
    e.JobRole,	
    e.JobLevel,
    e.MonthlyIncome,	
    e.YearsAtCompany,
    e.NumCompaniesWorked,
    e.DistanceFromHome,
    e.Attrition,
    
    -- From performance table 
    p.OverTime, 
    p.PerformanceRating, 
    p.YearsSinceLastPromotion,
    p.TrainingTimesLastYear, 
    p.YearsInCurrentRole, 
    p.TotalWorkingYears,

    -- From satisfaction table
    s.JobSatisfaction,
    s.WorkLifeBalance,
    s.RelationshipSatisfaction,
    s.EnvironmentSatisfaction,
    s.JobInvolvement,
    s.StockOptionLevel,

    -- From attendance table
    a.AvgHoursPerDay, 
    a.AvgLaptopActiveHours,
    a.LeaveDaysTaken, 
    a.AbsentDaysLastYear, 
    a.BusinessTravelFrequency,

    -- Derived columns
    -- 1. AttritionFlag → Attrition Yes=1, No=0
    CASE 
        WHEN e.Attrition = 'Yes' THEN 1
        ELSE 0
    END AS AttritionFlag,

    -- 2. RiskLevel → High/Medium/Low (you already wrote this!)
    CASE 
        WHEN s.JobSatisfaction = 1 OR s.WorkLifeBalance = 1 THEN 'High Risk'
        WHEN s.JobSatisfaction = 2 OR s.WorkLifeBalance = 2 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS RiskLevel,

    -- 3. SalaryBand → 'Below 50K', '50K-100K', '100K-200K', 'Above 200K'
    CASE 
        WHEN e.MonthlyIncome < 50000 THEN 'Below 50K'
        WHEN e.MonthlyIncome >= 50000 AND e.MonthlyIncome <= 100000 THEN '50K-100K'
        WHEN e.MonthlyIncome > 100000 AND e.MonthlyIncome <= 200000 THEN '100K-200K'
        WHEN e.MonthlyIncome > 200000 THEN 'Above 200K'
    END AS SalaryBand

FROM employees e 
INNER JOIN performance p 
ON e.EmployeeID = p.EmployeeID
INNER JOIN satisfaction s 
ON e.EmployeeID = s.EmployeeID 
INNER JOIN attendance a 
ON e.EmployeeID = a.EmployeeID ; 
