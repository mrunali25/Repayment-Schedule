import pandas as pd 
import numpy as np 
from utils.basic import * 
from datetime import datetime,timedelta
from utils.getinfo import *


def calculate_CRR_interest(closing_balance, extra_payment, interest_rate, days_in_month, last_emi_date, payment_date):
    # Calculate days remaining after the last EMI date till the payment date
    days_before_payment = (payment_date - last_emi_date).days
    
    # Calculate interest on the remaining CLBAL before extra payment
    interest_before_extra_payment = interest_rate * closing_balance * ((days_before_payment) / days_in_month)

    # Calculate interest on the remaining CLBAL after extra payment
    clbal_after_extra_payment = closing_balance - extra_payment
    interest_after_extra_payment = interest_rate * clbal_after_extra_payment * ((days_in_month - days_before_payment) / days_in_month)
    
    # Total interest for the month
    total_interest = interest_before_extra_payment + interest_after_extra_payment
    
    return total_interest

def create_repayment_schedule_table(principal, monthly_IR, emi):
    # Initialize an empty list to store rows
    rows = []
    
    # Append first row manually
    rows.append({'Opening Balance': 0, 'Installment Amount': -round(principal, 2), 'Principal Amount': -round(principal, 2), 'Interest Amount': 0, 'Closing Balance': round(principal, 2)})
    
    # Loop until CLBAL is less than 10
    while rows[-1]['Closing Balance'] >= 10:
        # Calculate values for the next row
        interest_amount = round(rows[-1]['Closing Balance'] * monthly_IR, 2)
        principal_amount = round(emi - interest_amount, 2)
        closing_balance = round(rows[-1]['Closing Balance'] - principal_amount, 2)

        # Append row to list of rows
        rows.append({'Opening Balance': rows[-1]['Closing Balance'],
                     'Installment Amount': round(emi, 2),
                     'Principal Amount': principal_amount,
                     'Interest Amount': interest_amount,
                     'Closing Balance': closing_balance})
    
    # Create DataFrame from list of rows
    df = pd.DataFrame(rows)
    
    return df  


def repayment_schedule_difference(actual_df, calculated_df):
    difference = abs(actual_df['Closing Balance'] - calculated_df['Closing Balance'])
    difference_sum = np.sum(difference)
    return difference, difference_sum




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

def calculate_interest_after_crr(opening_balance_before_crr, opening_balance_after_crr, monthly_IR, days_before_crr, days_in_month):
    interest_before_crr = (opening_balance_before_crr * monthly_IR * (days_before_crr / days_in_month))
    interest_after_crr = (opening_balance_after_crr * monthly_IR * ((days_in_month - days_before_crr) / days_in_month))
    return round(interest_before_crr + interest_after_crr, 2)

def process_installment_row(row, opening_balance, monthly_IR, days_in_month, previous_row_was_crr, crr_info):
    if previous_row_was_crr:
        # Calculate interest based on the provided formula
        interest_amount = calculate_interest_after_crr(
            crr_info['closing_balance_before_crr'], 
            crr_info['closing_balance_after_crr'], 
            monthly_IR, 
            crr_info['days_before_crr'], 
            days_in_month
        )
    else:
        # Standard interest calculation
        interest_amount = round(opening_balance * monthly_IR, 2)

    principal_amount = row['Installment Amount'] - interest_amount
    closing_balance = calculate_closing_balance(opening_balance, principal_amount)
    return principal_amount, interest_amount, closing_balance

def create_repayment_schedule_with_crr(dataframe):
    rows = []
    previous_row_was_crr = False
    crr_info = {}
    days_in_month = 30
    
    # Retrieve monthly interest rate from the repayment schedule
    monthly_IR, _ = IR_from_repayment_schedule(dataframe)

    for index, row in dataframe.iterrows():
        opening_balance = rows[-1]['Closing Balance'] if rows else 0

        if row['Transaction Type'] == 'Capital Repayment Receivable':
            previous_row_was_crr = True
            crr_info = {
                'date': row['Installment Date'],
                'amount_paid': row['Principal Amount'],
                'closing_balance_before_crr': opening_balance,
                'closing_balance_after_crr': calculate_closing_balance(opening_balance, row['Principal Amount']),
                'days_before_crr': (row['Installment Date'] - dataframe.iloc[index - 1]['Installment Date']).days if index > 0 else 0
            }
            closing_balance = crr_info['closing_balance_after_crr']
            rows.append({
                'Installment Date': row['Installment Date'],
                'Transaction Type': row['Transaction Type'],
                'Opening Balance': round(opening_balance, 0),
                'Principal Amount': row['Principal Amount'],
                'Interest Amount': 0,
                'Installment Amount': 0,
                'Closing Balance': closing_balance
            })
        else:
            principal_amount, interest_amount, closing_balance = process_installment_row(
                row, 
                opening_balance, 
                monthly_IR, 
                days_in_month, 
                previous_row_was_crr, 
                crr_info
            )
            
            # Calculate one-day interest for the opening balance
            one_day_interest = opening_balance * monthly_IR / days_in_month
            
            # Calculate the difference between calculated and provided closing balance
            closing_balance_difference = closing_balance - row['Closing Balance']
            
            # Adjust the final closing balance if the difference is less than one-day interest
            if closing_balance_difference < one_day_interest:
                closing_balance -= closing_balance_difference
            
            previous_row_was_crr = False  # Reset after processing a non-CRR row
            rows.append({
                'Installment Date': row['Installment Date'],
                'Transaction Type': row['Transaction Type'],
                'Opening Balance': round(opening_balance, 0),
                'Principal Amount': principal_amount,
                'Interest Amount': interest_amount,
                'Installment Amount': row['Installment Amount'],
                'Closing Balance': closing_balance
            })

    return pd.DataFrame(rows)