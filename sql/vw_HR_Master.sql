CREATE OR ALTER VIEW Gold_Layer_DB.vw_HR_Master AS
SELECT
    s.EmployeeID,
    s.Name,
    s.Age,
    s.Gender,
    s.MaritalStatus,
    s.Education,
    s.EducationField,
    s.Department,
    s.JobRole,
    s.JobLevel,
    s.MonthlyIncome,
    s.YearsAtCompany,
    s.NumCompaniesWorked,
    s.DistanceFromHome,
    s.Attrition,
    s.OverTime,
    s.PerformanceRating,
    s.YearsSinceLastPromotion,
    s.TrainingTimesLastYear,
    s.YearsInCurrentRole,
    s.TotalWorkingYears,
    s.JobSatisfaction,
    s.WorkLifeBalance,
    s.RelationshipSatisfaction,
    s.EnvironmentSatisfaction,
    s.JobInvolvement,
    s.StockOptionLevel,
    s.AvgHoursPerDay,
    s.LeaveDaysTaken,
    s.AbsentDaysLastYear,
    s.BusinessTravelFrequency,
    s.AttritionFlag,
    s.RiskLevel,
    s.SalaryBand,

    -- RiskScore recalculated inline
    (
        CASE WHEN s.OverTime = 'Yes' THEN 25 ELSE 0 END
        + CASE WHEN s.JobSatisfaction = 1 THEN 20
               WHEN s.JobSatisfaction = 2 THEN 10
               ELSE 0 END
        + CASE WHEN s.WorkLifeBalance = 1 THEN 20
               WHEN s.WorkLifeBalance = 2 THEN 10
               ELSE 0 END
        + CASE WHEN s.YearsSinceLastPromotion >= 4 THEN 20
               WHEN s.YearsSinceLastPromotion >= 2 THEN 10
               ELSE 0 END
        + CASE WHEN s.EnvironmentSatisfaction = 1 THEN 15
               WHEN s.EnvironmentSatisfaction = 2 THEN 8
               ELSE 0 END
    ) AS RiskScore,

    -- ML columns from predictions table
    m.Cluster,
    m.ClusterName,
    m.ML_Risk_Score_Pct,
    m.ML_Attrition_Probability,
    m.ML_Predicted_Attrition,

    -- AI Columns from Notebook
    ai.AI_Risk_Card,
    ai.Generated_At

FROM TechNova_HR_Lakehouse.dbo.silver_master_employees s
LEFT JOIN TechNova_HR_Lakehouse.dbo.ml_attrition_predictions m
    ON s.EmployeeID = m.EmployeeID
LEFT JOIN dbo.vw_AI_Risk_Cards ai
    ON s.EmployeeID = ai.EmployeeID;

