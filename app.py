from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# Load dataset
df = pd.read_csv("WA_Fn-UseC_-HR-Employee-Attrition.csv")


@app.route("/")
def dashboard():

    selected_chart = request.args.get("chart", "Age vs Attrition Analysis")

    # ===== KPI =====
    total_emp = len(df)
    total_attrition = len(df[df["Attrition"] == "Yes"])
    attrition_rate = round((total_attrition / total_emp) * 100, 2)

    # ===== DROPDOWN OPTIONS =====
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

    # ===== CHART LOGIC =====
    if selected_chart == "Age vs Attrition Analysis":
        c = df.groupby(["Age", "Attrition"]).size().reset_index(name="Count")
        fig = px.bar(c, x="Age", y="Count", color="Attrition",
                     title=selected_chart, template="plotly_dark")

    elif selected_chart == "Marital Status vs Attrition":
        c = df.groupby(["MaritalStatus", "Attrition"]).size().reset_index(name="Count")
        fig = px.bar(c, x="MaritalStatus", y="Count", color="Attrition",
                     barmode="group", title=selected_chart,
                     template="plotly_dark")

    elif selected_chart == "Job Role vs Attrition":
        c = df.groupby(["JobRole", "Attrition"]).size().reset_index(name="Count")
        fig = px.bar(c, x="JobRole", y="Count", color="Attrition",
                     barmode="group", title=selected_chart,
                     template="plotly_dark")
        fig.update_layout(xaxis_tickangle=-45)

    elif selected_chart == "Job Involvement vs Attrition":
        c = df.groupby(["JobInvolvement", "Attrition"]).size().reset_index(name="Count")
        fig = px.bar(c, x="JobInvolvement", y="Count", color="Attrition",
                     title=selected_chart, template="plotly_dark")

    elif selected_chart == "Experienced vs Attrition":
        c = df.groupby(["YearsAtCompany", "Attrition"]).size().reset_index(name="Count")
        fig = px.bar(c, x="YearsAtCompany", y="Count", color="Attrition",
                     title=selected_chart, template="plotly_dark")

    elif selected_chart == "Distance from Home vs Attrition":
        c = df.groupby(["DistanceFromHome", "Attrition"]).size().reset_index(name="Count")
        fig = px.bar(c, x="DistanceFromHome", y="Count", color="Attrition",
                     title=selected_chart, template="plotly_dark")

    elif selected_chart == "Years with Current Manager vs Attrition":
        c = df.groupby(["YearsWithCurrManager", "Attrition"]).size().reset_index(name="Count")
        fig = px.bar(c, x="YearsWithCurrManager", y="Count", color="Attrition",
                     title=selected_chart, template="plotly_dark")

    elif selected_chart == "Total Working Years vs Attrition":
        c = df.groupby(["TotalWorkingYears", "Attrition"]).size().reset_index(name="Count")
        fig = px.bar(c, x="TotalWorkingYears", y="Count", color="Attrition",
                     title=selected_chart, template="plotly_dark")

    elif selected_chart == "Gender vs Monthly Income":
        fig = px.box(df, x="Gender", y="MonthlyIncome",
                     color="Gender", title=selected_chart,
                     template="plotly_dark")

    elif selected_chart == "Monthly Income vs Job Role":
        fig = px.box(df, x="JobRole", y="MonthlyIncome",
                     color="JobRole", title=selected_chart,
                     template="plotly_dark")
        fig.update_layout(xaxis_tickangle=-45)

    fig.update_layout(height=650)

    # ===== Enable Download Button =====
    graph_html = fig.to_html(
        full_html=False,
        config={
            "displaylogo": False,
            "toImageButtonOptions": {
                "format": "png",
                "filename": selected_chart,
                "height": 700,
                "width": 1200,
                "scale": 2
            }
        }
    )

    return render_template(
        "dashboard.html",
        chart_options=chart_options,
        selected_chart=selected_chart,
        graph_html=graph_html,
        total_emp=total_emp,
        total_attrition=total_attrition,
        attrition_rate=attrition_rate
    )


if __name__ == "__main__":
    app.run(debug=True)
