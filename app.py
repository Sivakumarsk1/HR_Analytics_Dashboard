from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

app = Flask(__name__)

df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")


@app.route("/")
def dashboard():

    # ===== FILTERS =====
    department = request.args.get("department", "All")
    gender = request.args.get("gender", "All")

    filtered_df = df.copy()

    if department != "All":
        filtered_df = filtered_df[filtered_df["Department"] == department]

    if gender != "All":
        filtered_df = filtered_df[filtered_df["Gender"] == gender]

    departments = ["All"] + sorted(df["Department"].unique())
    genders = ["All"] + sorted(df["Gender"].unique())

    # ===== KPI =====
    total_emp = len(filtered_df)
    total_attrition = len(filtered_df[filtered_df["Attrition"] == "Yes"])
    attrition_rate = round((total_attrition / total_emp) * 100, 2)

    # ===== CHART 1: Job Role vs Attrition =====
    c1 = filtered_df.groupby(["JobRole", "Attrition"]).size().reset_index(name="Count")
    fig1 = px.bar(c1, x="JobRole", y="Count", color="Attrition",
                  barmode="group", template="plotly_dark",
                  title="Job Role vs Attrition")
    fig1.update_layout(xaxis_tickangle=-45, height=400)

    # ===== CHART 2: Age vs Attrition =====
    c2 = filtered_df.groupby(["Age", "Attrition"]).size().reset_index(name="Count")
    fig2 = px.bar(c2, x="Age", y="Count", color="Attrition",
                  template="plotly_dark",
                  title="Age vs Attrition", height=400)

    # ===== CHART 3: Marital Status =====
    c3 = filtered_df.groupby(["MaritalStatus", "Attrition"]).size().reset_index(name="Count")
    fig3 = px.bar(c3, x="MaritalStatus", y="Count", color="Attrition",
                  barmode="group",
                  template="plotly_dark",
                  title="Marital Status vs Attrition",
                  height=400)

    # ===== CHART 4: Income vs Job Role =====
    fig4 = px.box(filtered_df, x="JobRole", y="MonthlyIncome",
                  color="JobRole",
                  template="plotly_dark",
                  title="Monthly Income vs Job Role")
    fig4.update_layout(xaxis_tickangle=-45, height=400)

    # ===== AI INSIGHT BOX =====
    top_attrition_role = (
        filtered_df[filtered_df["Attrition"] == "Yes"]["JobRole"]
        .value_counts()
        .idxmax()
    )

    insight = f"""
    Attrition rate is {attrition_rate}%.
    Highest attrition is seen in '{top_attrition_role}' role.
    Younger employees and lower experience groups show higher risk.
    """

    return render_template(
        "dashboard.html",
        total_emp=total_emp,
        total_attrition=total_attrition,
        attrition_rate=attrition_rate,
        departments=departments,
        genders=genders,
        selected_dept=department,
        selected_gender=gender,
        chart1=fig1.to_html(full_html=False),
        chart2=fig2.to_html(full_html=False),
        chart3=fig3.to_html(full_html=False),
        chart4=fig4.to_html(full_html=False),
        insight=insight
    )


if __name__ == "__main__":
    app.run(debug=True)
