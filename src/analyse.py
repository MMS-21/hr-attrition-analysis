"""Publishable adaptation of Moaaz Magdy's original notebook workflow."""
from pathlib import Path
import argparse
import duckdb
import pandas as pd


def classify_experience(years):
    if pd.isna(years) or years < 0:
        raise ValueError("TotalWorkingYears must be a nonnegative number")
    if years < 5:
        return "Junior"
    if years <= 9:
        return "Mid"
    return "Senior"


def analyse(workbook, output):
    sheets = pd.read_excel(workbook, sheet_name=None)
    required = {
        "FactEmployee": {"EmployeeNumber", "DepartmentKey", "JobRoleKey",
                         "AttritionFlag", "MonthlyIncome", "TotalWorkingYears"},
        "DimDepartment": {"DepartmentKey", "Department"},
        "DimJobRole": {"JobRoleKey", "JobRoleName"},
    }
    for name, columns in required.items():
        if name not in sheets:
            raise ValueError(f"Missing sheet: {name}")
        sheets[name].columns = sheets[name].columns.str.strip()
        missing = columns - set(sheets[name].columns)
        if missing:
            raise ValueError(f"{name}: missing columns {sorted(missing)}")
    fact = sheets["FactEmployee"].copy()
    if fact["EmployeeNumber"].isna().any() or fact["EmployeeNumber"].duplicated().any():
        raise ValueError("Expected one row per employee")
    if not fact["AttritionFlag"].isin([0, 1]).all():
        raise ValueError("AttritionFlag must contain only 0 and 1")
    for dimension, key in [("DimDepartment", "DepartmentKey"), ("DimJobRole", "JobRoleKey")]:
        dim = sheets[dimension]
        if dim[key].isna().any() or dim[key].duplicated().any():
            raise ValueError(f"{dimension}: keys must be unique and non-null")
        if not fact[key].isin(dim[key]).all():
            raise ValueError(f"Unmatched {key} in employee data")
    fact["ExperienceLevel"] = fact["TotalWorkingYears"].apply(classify_experience)
    summary = fact.groupby("ExperienceLevel").agg(
        EmployeeCount=("EmployeeNumber", "size"),
        AttritionCount=("AttritionFlag", "sum"),
    ).reset_index()
    summary["AttritionRatePct"] = 100 * summary["AttritionCount"] / summary["EmployeeCount"]
    output.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output / "experience_summary.csv", index=False)
    query = (Path(__file__).resolve().parents[1] / "sql/attrition_by_role.sql").read_text()
    with duckdb.connect() as con:
        con.register("FactEmployee", fact)
        con.register("DimDepartment", sheets["DimDepartment"])
        con.register("DimJobRole", sheets["DimJobRole"])
        result = con.execute(query).fetchdf()
    result.to_csv(output / "attrition_by_role.csv", index=False)
    print(result.to_string(index=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--output", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    analyse(args.workbook, args.output)
