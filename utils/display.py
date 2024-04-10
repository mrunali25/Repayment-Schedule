
import numpy as np 
import pandas as pd 
import streamlit as st 
from .basic import *
from .getinfo import *


def repayment_schedule_difference(actual_df, calculated_df):
    difference = abs(actual_df['Closing Balance'] - calculated_df['Closing Balance'])
    difference_sum = np.sum(difference)
    return difference, difference_sum


# Function to calculate difference and display results
def calculate_difference(actual_df, calculated_df):
    difference, difference_sum = repayment_schedule_difference(actual_df, calculated_df)
    st.write("Difference in Closing Balance:")
    st.write(difference)
    st.write("Total Difference:", difference_sum)

def display_interest_and_principle_emi(actual_df):
    """
    Displays the monthly and annual interest rates, principle, and EMI from the actual repayment schedule.

    Args:
        actual_df (DataFrame): DataFrame containing the actual repayment schedule.
    """
    monthly_IR, annual_IR = IR_from_repayment_schedule(actual_df)
    principle, emi = principal_emi_from_repayment_schedule(actual_df)
    # Display interest rates, principal, and EMI
    st.write("Monthly Interest Rate:", monthly_IR)
    st.write("Annual Interest Rate:", annual_IR)
    st.write("Principle:", principle)
    st.write("EMI:", emi)


def check_interest_rate_consistency(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Calculate the interest rate starting from the second row to skip the first row
    df['Calculated_Monthly_IR'] = (df['Interest Amount'] / df['Opening Balance']).round(6)
    calculated_IRs = df['Calculated_Monthly_IR'].iloc[1:]  # Skipping the first row

    # Check if all calculated monthly interest rates from the second row onwards are the same
    if calculated_IRs.nunique() == 1:
        # Interest rate is consistent
        return True, "Interest rate is the same throughout rows."
    else:
        # Since all rates should be the same, checking for actual inconsistency
        # Find the first row index where the difference occurs, considering the skipped row
        first_diff_index = calculated_IRs.diff().ne(0).idxmax()  # Finding first non-zero diff
        if first_diff_index is not pd.NaT:
            # If an actual difference is found, report the row number
            return False, f"Interest rate is not consistent. Check row {first_diff_index + 1} for the first discrepancy."
        else:
            # If no actual difference found, report as consistent
            return True, "Interest rate is the same throughout after skipping the first row."


