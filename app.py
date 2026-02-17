from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Load dataset
df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")


@app.route("/")
def dashboard():

    selected_chart = request.args.get("chart", "Age vs Attrition Analysis")

    # ===== Overall KPI =====
    total_emp = len(df)
    total_attrition = len(df[df["Attrition"] == "Yes"])
    attrition_rate = round((total_attrition / total_emp) * 100, 2)

    # ===== Dropdown options =====
    chart_options = [
        "Age vs Attrition Analysis",
        "Marital Status vs Attrition",
        "Job Role vs Attrition",
        "Job Involvement vs Attrition",
        "Experienced vs Attrition",
        "Distance from Home vs Attrition",
        "Years with Current Manager vs Attrition",
        "Total Working Years vs Attrition",
        "Gender vs Monthly Income",
        "Monthly Income vs Job Role"
    ]

    # ===== Graph selection =====
    if selected_chart == "Age vs Attrition Analysis":
        group_col = "Age"
        c = df.groupby(["Age", "Attrition"]).size().reset_index(name="Count")
        fig = px.bar(c, x="Age", y="Count", color="Attrition",
                     title=selected_chart, template="plotly_dark")

    elif selected_chart == "Marital Status vs Attrition":
        group_col = "MaritalStatus"
        c = df.groupby(["MaritalStatus", "Attrition"]).size().reset_index(name="Count")
        fig = px.bar(c, x="MaritalStatus", y="Count", color="Attrition",
                     barmode="group", title=selected_chart,
                     template="plotly_dark")

    elif selected_chart == "Job Role vs Attrition":
        group_col = "JobRole"
        c = df.groupby(["JobRole", "Attrition"]).size().reset_index(name="Count")
        fig = px.bar(c, x="JobRole", y="Count", color="Attrition",
                     barmode="group", title=selected_chart,
                     template="plotly_dark")
        fig.update_layout(xaxis_tickangle=-45)

    elif selected_chart == "Job Involvement vs Attrition":
        group_col = "JobInvolvement"
        c = df.groupby(["JobInvolvement", "Attrition"]).size().reset_index(name="Count")
        fig = px.bar(c, x="JobInvolvement", y="Count", color="Attrition",
                     title=selected_chart, template="plotly_dark")

    elif selected_chart == "Experienced vs Attrition":
        group_col = "YearsAtCompany"
        c = df.groupby(["YearsAtCompany", "Attrition"]).size().reset_index(name="Count")
        fig = px.bar(c, x="YearsAtCompany", y="Count", color="Attrition",
                     title=selected_chart, template="plotly_dark")

    elif selected_chart == "Distance from Home vs Attrition":
        group_col = "DistanceFromHome"
        c = df.groupby(["DistanceFromHome", "Attrition"]).size().reset_index(name="Count")
        fig = px.bar(c, x="DistanceFromHome", y="Count", color="Attrition",
                     title=selected_chart, template="plotly_dark")

    elif selected_chart == "Years with Current Manager vs Attrition":
        group_col = "YearsWithCurrManager"
        c = df.groupby(["YearsWithCurrManager", "Attrition"]).size().reset_index(name="Count")
        fig = px.bar(c, x="YearsWithCurrManager", y="Count", color="Attrition",
                     title=selected_chart, template="plotly_dark")

    elif selected_chart == "Total Working Years vs Attrition":
        group_col = "TotalWorkingYears"
        c = df.groupby(["TotalWorkingYears", "Attrition"]).size().reset_index(name="Count")
        fig = px.bar(c, x="TotalWorkingYears", y="Count", color="Attrition",
                     title=selected_chart, template="plotly_dark")

    # ===== NEW CHART 1 =====
    elif selected_chart == "Gender vs Monthly Income":
        group_col = "Gender"
        fig = px.box(
            df,
            x="Gender",
            y="MonthlyIncome",
            color="Gender",
            title=selected_chart,
            template="plotly_dark"
        )

    # ===== NEW CHART 2 =====
    elif selected_chart == "Monthly Income vs Job Role":
        group_col = "JobRole"
        fig = px.box(
            df,
            x="JobRole",
            y="MonthlyIncome",
            color="JobRole",
            title=selected_chart,
            template="plotly_dark"
        )
        fig.update_layout(xaxis_tickangle=-45)

    # ===== Dynamic Numbers =====
    top_category = df[group_col].value_counts().idxmax()

    top_attrition_category = (
        df[df["Attrition"] == "Yes"][group_col]
        .value_counts()
        .idxmax()
    )

    fig.update_layout(height=650)

    graph_html = fig.to_html(full_html=False)

    return render_template(
        "dashboard.html",
        graph_html=graph_html,
        chart_options=chart_options,
        selected_chart=selected_chart,
        total_emp=total_emp,
        total_attrition=total_attrition,
        attrition_rate=attrition_rate,
        top_category=top_category,
        top_attrition_category=top_attrition_category
    )


if __name__ == "__main__":
    app.run(debug=True)
