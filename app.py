
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("Personal Budget Tracker")
st.write("enter an expense below to see if it will fit within your budget")

#First Widget

category = st.selectbox("Select an Expense Category", ["Housing", "Food", "Transportation", "Entertainment", "Utilities", "Other"])

#Second Wideget
amount = st.number_input("Enter the Expense Amount", min_value=0.0, step=0.01)

# Widget 3: slider for monthly income
income = st.slider("Monthly Income ($)", min_value=0, max_value=10000, value=3000, step=100)

#Output that reflects expense

if amount > 0:
    percent = (amount / income) * 100 if income > 0 else 0
    st.write(f"You logged **${amount:.2f}** under **{category}**.")
    st.write(f"That's **{percent:.1f}%** of your monthly income.")
    if amount > 500:
        st.warning("⚠️ This is a large expense — make sure it fits your budget!")
    else:
        st.success("This expense seems reasonable within your budget.")