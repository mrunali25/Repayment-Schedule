import streamlit as st
import pandas as pd
from utils.utils import *  # This now also includes check_interest_rate_consistency
from utils.getinfo import *
from utils.basic import *

# Assume 'create_repayment_schedule_with_crr' is a function similar to 'create_repayment_schedule_table'
# but with logic to handle the Capital Repayment Receivable events.
# from your_repayment_module import create_repayment_schedule_with_crr

# Function to calculate difference and display results
def calculate_difference(actual_df, calculated_df):
    difference, difference_sum = repayment_schedule_difference(actual_df, calculated_df)
    st.write("Difference in Closing Balance:")
    st.write(difference)
    st.write("Total Difference:", difference_sum)

def main():
    st.title("Repayment Schedule Difference Checker")

    # User selection for type of repayment schedule
    schedule_type = st.radio(
        "Choose the type of repayment schedule you want to upload:",
        ('Normal Repayment Schedule', 'Repayment Schedule with CRR')
    )

    # File upload
    uploaded_file = st.file_uploader("Upload XLSX file", type=['xlsx'])

    if uploaded_file is not None:
        

        # Create a calculated repayment schedule based on the user's choice
        if schedule_type == 'Normal Repayment Schedule':
            # Read uploaded file into DataFrame
            actual_df = pd.read_excel(uploaded_file)
            OPBAL = st.selectbox('Opening Balance', actual_df.columns)
            CLBAL= st.selectbox('Closing Balance', actual_df.columns)
            Installment=st.selectbox('Installment Amount', actual_df.columns)
            Interest=st.selectbox('Interest Amount', actual_df.columns)
            Pricipal=st.selectbox('Principal Amount', actual_df.columns)
            # Get interest and principle EMI from the actual repayment schedule
            monthly_IR, annual_IR = IR_from_repayment_schedule(actual_df)
            principle, emi = principal_emi_from_repayment_schedule(actual_df)

            # Display interest rates, principal, and EMI
            st.write("Monthly Interest Rate:", monthly_IR)
            st.write("Annual Interest Rate:", annual_IR)
            st.write("Principle:", principle)
            st.write("EMI:", emi)
            # Perform interest rate consistency check only for normal repayment schedules
            consistent, message = check_interest_rate_consistency(uploaded_file)
            if consistent:
                st.markdown(f'<span style="color:green;">✔️</span> {message}', unsafe_allow_html=True)
            else:
                st.markdown(f'<span style="color:red;">❌</span> {message}', unsafe_allow_html=True)

            # Calculate EMI table for normal schedules
            calculated_df = create_repayment_schedule_table(principle, monthly_IR, emi)
            st.write("Calculated EMI Table:")
        else:  # 'Repayment Schedule with CRR'
            actual_df = pd.read_excel(uploaded_file)
            # Calculate EMI table with CRR adjustments
            calculated_df = create_repayment_schedule_with_crr(actual_df)
            st.write("Calculated Repayment Schedule with CRR:")

        # Display the calculated repayment schedule
        st.write(calculated_df)

        # Calculate and display the difference between actual and calculated schedules
        calculate_difference(actual_df, calculated_df)

if __name__ == "__main__":
    main()


