import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load environment variables from .env file
load_dotenv()

hf_token = st.secrets["HF_TOKEN"]

# System prompt to simulate personal finance assistant (replaced with manual advice)
system_prompt = "You are a personal finance assistant. Provide actionable advice based on the user's spending behavior and budget."

# Function to get basic financial advice based on budget and expenses
def get_financial_advice(budget, expenses):
    # Example simple advice generation
    total_expenses = sum(expenses.values())
    remaining_budget = budget - total_expenses

    if remaining_budget > 0:
        advice = "Great job! You are within your budget. You can save the remaining amount."
    elif remaining_budget == 0:
        advice = "You have exactly used up your budget. Consider reviewing some expenses."
    else:
        advice = "You have exceeded your budget. Look for ways to reduce some expenses to stay within budget."
    
    return advice

# Customizing Streamlit theme
st.set_page_config(
    page_title="AI-Powered Personal Finance Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add custom styles
st.markdown(
    """
    <style>
    /* Background Gradient */
    .stApp {
        background: linear-gradient(to bottom right, #f8f9fa, #e0e0e0);
        color: #333;
    }
    /* Title Styling */
    h1, h2, h3, h4 {
        color: #2a2a2a;
        font-family: 'Segoe UI', sans-serif;
    }
    /* Subheader Styling */
    .stMarkdown > div > h2 {
        color: #0056b3;
    }
    /* Input Field Styling */
    .stTextInput, .stNumberInput {
        background-color: #ffffff;
        border-radius: 10px;
        border: 1px solid #ced4da;
        padding: 10px;
    }
    /* Button Styling */
    .stButton button {
        background-color: #007bff;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .stButton button:hover {
        background-color: #0056b3;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App title and description
st.title("💸 AI-Powered Personal Finance Assistant")
st.markdown(""" 
    ## Welcome to Your Personal Finance Assistant! 
    This app is designed to help you manage your budget, track expenses, and receive financial advice.  
    It's intuitive, visually appealing, and super easy to use! 🎯 
""")

# Sidebar for inputs
st.sidebar.title("💡 Quick Input")
st.sidebar.markdown("Enter your total monthly budget and expense details below.")

# Step 1: Ask for the total monthly budget
total_budget = st.sidebar.number_input(
    "Total Monthly Budget ($):",
    min_value=0.0,
    step=50.0,
    help="This is the amount you plan to spend this month.",
)

# Step 2: Collect expenses in various categories
st.sidebar.markdown("### Expense Categories")
categories = {
    "Rent": st.sidebar.number_input("Rent ($):", min_value=0.0, step=10.0),
    "Dining": st.sidebar.number_input("Dining ($):", min_value=0.0, step=10.0),
    "Education Fee": st.sidebar.number_input("Education Fee ($):", min_value=0.0, step=10.0),
    "Loan Payments": st.sidebar.number_input("Loan Payments ($):", min_value=0.0, step=10.0),
    "Utilities (Bills)": st.sidebar.number_input("Utilities ($):", min_value=0.0, step=10.0),
    "Mobile/Internet Bills": st.sidebar.number_input("Mobile/Internet Bills ($):", min_value=0.0, step=10.0),
    "Other": st.sidebar.number_input("Other Expenses ($):", min_value=0.0, step=10.0),
}

# Step 3: Calculate total expenses and remaining budget
total_expenses = sum(categories.values())
remaining_budget = total_budget - total_expenses

# Display results with interactive highlights
st.subheader("💰 Budget Summary")
st.markdown(f"**Total Budget:** <span style='color: #007bff;'>${total_budget:,.2f}</span>", unsafe_allow_html=True)
st.markdown(f"**Total Expenses:** <span style='color: #dc3545;'>${total_expenses:,.2f}</span>", unsafe_allow_html=True)
st.markdown(f"**Remaining Budget:** <span style='color: #28a745;'>${remaining_budget:,.2f}</span>", unsafe_allow_html=True)

# Provide basic financial advice
if st.button("Get Financial Advice 🧠"):
    if total_budget > 0:
        response = get_financial_advice(total_budget, categories)
        st.subheader("📝 Financial Advice")
        st.markdown(f"<div style='color: #2a2a2a; font-style: italic;'>{response}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a valid budget before requesting advice.")

# Step 4: Visualize the expenses
if total_expenses > 0:
    st.subheader("📊 Expense Distribution")
    expense_df = pd.DataFrame.from_dict(categories, orient="index", columns=["Amount"])
    
    # Bar chart
    st.bar_chart(expense_df)

    # Pie chart with enhanced design
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = plt.cm.tab10(range(len(categories)))  # Use a built-in color palette
    ax.pie(categories.values(), labels=categories.keys(), autopct="%1.1f%%", startangle=90, colors=colors)
    ax.axis("equal")
    st.pyplot(fig)

# Footer with interactive style
st.markdown(""" 
    --- 
    <div style="text-align: center; color: #2a2a2a;"> 
        Developed by <strong>Your Name</strong> | Powered by <strong>AI and Machine Learning</strong> 💡  
        Let's make personal finance management smarter together! 
    </div> 
""", unsafe_allow_html=True)
