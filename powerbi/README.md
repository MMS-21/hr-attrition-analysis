# Power BI reporting

Original report built by Moaaz Magdy. Its pages are Landing Page, Executive Overview, Deep Dive, and Recommendations Preview.

## Model

FactEmployee has one row per employee. DimDepartment and DimJobRole connect to the fact table through unique dimension keys, using one-to-many relationships with filters flowing from dimensions to the fact table. DimEmployee holds employee attributes and connects through EmployeeNumber in the prepared workbook.

The companion DAX file documents counts, attrition proportions, income comparisons, and the overtime segment measure. Format attrition measures as percentages. Total Employees describes all employee records in the selected sample, not current active headcount. Attrition is the fraction marked as leavers in this dataset, not an annual turnover measure.

The original PBIX is withheld because it embeds source records and local metadata. Images in this public project are checked analysis charts, not screenshots of Power BI pages.
