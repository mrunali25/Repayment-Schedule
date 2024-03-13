import streamlit as st
import pandas as pd
from utils.utils import *  # This now also includes check_interest_rate_consistency
from utils.getinfo import *

# Function to calculate difference and display results
def calculate_difference(actual_df, calculated_df):
    difference, difference_sum = repayment_schedule_difference(actual_df, calculated_df)
    st.write("Difference in CLBAL:")
    st.write(difference)
    st.write("Total Difference:", difference_sum)

def main():
    st.title("EMI Calculation Difference Checker")

    # File upload
    uploaded_file = st.file_uploader("Upload XLSX file", type=['xlsx'])

    if uploaded_file is not None:
        # Read uploaded file into DataFrame
        actual_df = pd.read_excel(uploaded_file)

        # Check interest rate consistency
        consistent, message = check_interest_rate_consistency(uploaded_file)

        # Display the results based on consistency check
        if consistent:
            # Display a green right tick and message if interest rates are consistent
            st.markdown(f'<span style="color:green;">✔️</span> {message}', unsafe_allow_html=True)
        else:
            # Display a warning message and indicate the row where interest rates differ
            st.markdown(f'<span style="color:red;">❌</span> {message}', unsafe_allow_html=True)

        # Get interest and principle EMI
        monthly_IR, annual_IR = IR_from_repayment_schedule(actual_df)
        principle, emi = principal_emi_from_repayment_schedule(actual_df)

        st.write("Monthly Interest Rate:", monthly_IR)
        st.write("Annual Interest Rate:", annual_IR)
        st.write("Principle:", principle)
        st.write("EMI:", emi)

        # Calculate EMI table
        calculated_df = create_repayment_schedule_table(principle, monthly_IR, emi)

        st.write("Calculated EMI Table:")
        st.write(calculated_df)

        # Calculate difference
        calculate_difference(actual_df, calculated_df)

if __name__ == "__main__":
    main()
