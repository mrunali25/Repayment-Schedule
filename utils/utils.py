import pandas as pd 
import numpy as np 
from utils.basic_calculations import *

def create_repayment_schedule_table(principle, monthly_IR, emi):
    # Initialize an empty list to store rows
    rows = []
    
    # Append first row manually
    rows.append({'MONTHS': 0, 'OPBAL': 0, 'FLOW AMT': -round(principle, 2), 'CAPITAL': -round(principle, 2), 'REVENUE': 0, 'CLBAL': round(principle, 2)})
    
    # Loop until CLBAL is less than 10
    while rows[-1]['CLBAL'] >= 10:
        # Calculate values for the next row
        revenue = round(rows[-1]['CLBAL'] * monthly_IR, 2)
        capital = round(emi - revenue, 2)
        clbal = round(rows[-1]['CLBAL'] - capital, 2)

        # Append row to list of rows
        rows.append({'MONTHS': rows[-1]['MONTHS'],
                     'OPBAL': rows[-1]['CLBAL'],
                     'FLOW AMT': round(emi, 2),
                     'CAPITAL': capital,
                     'REVENUE': revenue,
                     'CLBAL': clbal})
    
    # Create DataFrame from list of rows
    df = pd.DataFrame(rows)
    
    return df  


def repayment_schedule_difference(df1,df2):
    difference=abs(df1['CLBAL']-df2['CLBAL'])
    difference_sum=np.sum(difference)
    return difference,difference_sum

def calculate_emi_amount(principal, interest_rate, loan_tenure):
  """
  Calculates the EMI (Equated Monthly Installment) for a loan.

  Args:
      principal: The principal loan amount (float).
      interest_rate: The annual interest rate (float).
      loan_tenure: The loan tenure in months (int).

  Returns:
      The EMI amount (float).
  """

  # Convert annual interest rate to monthly interest rate
  monthly_interest_rate = annual_to_monthly_IR(interest_rate)

  # Calculate the EMI
  emi = (principal * monthly_interest_rate * ((1 + monthly_interest_rate) ** loan_tenure)) / (((1 + monthly_interest_rate) ** loan_tenure) - 1)

  return emi

def check_interest_rate_consistency(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Calculate the interest rate starting from the second row to skip the first row
    df['Calculated_Monthly_IR'] = (df['REVENUE'] / df['OPBAL']).round(6)
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

