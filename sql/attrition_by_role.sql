SELECT
    d.Department,
    j.JobRoleName AS JobRole,
    COUNT(*) AS EmployeeCount,
    COUNT(CASE WHEN f.AttritionFlag = 1 THEN 1 END) AS AttritionCount,
    100.0 * COUNT(CASE WHEN f.AttritionFlag = 1 THEN 1 END)
        / NULLIF(COUNT(*), 0) AS AttritionRatePct,
    AVG(f.MonthlyIncome) AS AvgMonthlyIncome
FROM FactEmployee f
INNER JOIN DimDepartment d ON f.DepartmentKey = d.DepartmentKey
INNER JOIN DimJobRole j ON f.JobRoleKey = j.JobRoleKey
GROUP BY d.Department, j.JobRoleName
ORDER BY AttritionCount DESC;
