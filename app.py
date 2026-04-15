#python3 -m streamlit run app.py use this to run
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Personal Budget Tracker")
st.caption("Created by Ryan Turner")
st.write("Use the slider to select your monthly income.")
income = st.slider("Monthly Income ($)", min_value=0, max_value=10000, value=3000, step=100)
st.divider()

# Create tabs for the different sections like log and charts
tab1, tab2, tab3 = st.tabs(["Log Expense", "Monthly Log", "Chart"])

with tab1:
    st.write("Enter an expense below to see if it fits within your budget.")

    category = st.selectbox("Select an Expense Category", ["Housing", "Food", "Transportation", "Entertainment", "Utilities", "Other"])
    amount = st.number_input("Enter the Expense Amount", min_value=0.0, step=0.01)

    if amount > 0:
        percent = (amount / income) * 100 if income > 0 else 0
        st.write(f"You logged **${amount:.2f}** under **{category}**.")
        st.write(f"That's **{percent:.1f}%** of your monthly income.")
        if amount > 500:
            st.warning("This is a large expense, make sure it fits your budget!")
        else:
            st.success("This expense seems reasonable within your budget.")

    if 'budget_log' not in st.session_state:
        st.session_state.budget_log = []

    if st.button("Add this monthly expense to the log"):
        if amount > 0:
            st.session_state.budget_log.append({
                "Category": category,
                "Amount": amount
            })
            st.success(f"Added ${amount:.2f} to the log under {category}")
        else:
            st.warning("Please enter an amount greater than $0 before adding.")

with tab2:
    st.header("Monthly Budget Log")
    if 'budget_log' not in st.session_state or len(st.session_state.budget_log) == 0:
        st.info("No expenses logged yet. Add some in the Log Expense tab!")
    else:
        df_log = pd.DataFrame(st.session_state.budget_log)
        st.write("Here's your monthly budget log:")
        st.dataframe(df_log)

        total_spent = df_log["Amount"].sum()
        remaining = income - total_spent

        col1, col2, col3 = st.columns(3)
        col1.metric("Monthly Income", f"${income:,.2f}")
        col2.metric("Total Spent", f"${total_spent:,.2f}")
        col3.metric("Remaining", f"${remaining:,.2f}", delta=f"{'Under' if remaining >= 0 else 'Over'} budget", delta_color="normal" if remaining >= 0 else "inverse")

with tab3:
    st.header("Spending by Category")
    if 'budget_log' not in st.session_state or len(st.session_state.budget_log) == 0:
        st.info("No expenses logged yet. Add some in the Log Expense tab!")
    else:
        df_log = pd.DataFrame(st.session_state.budget_log)
        df_chart = df_log.groupby("Category")["Amount"].sum().reset_index()
        fig = px.bar(df_chart, x="Category", y="Amount", title="Monthly Expenses by Category")
        st.plotly_chart(fig)