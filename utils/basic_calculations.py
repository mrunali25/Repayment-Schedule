import numpy as np 
import pandas as pd 

def monthly_to_annual_IR(interest_rate):
    """
    Convert monthly interest rate to annual interest rate.

    Args:
    interest_rate (float): Monthly interest rate expressed as a decimal (e.g., 0.1 for 10%).

    Returns:
    float: Annual interest rate expressed as a decimal.
    """
    annual_IR = interest_rate * 12
    return round(annual_IR,6)

def annual_to_monthly_IR(interest_rate):
    """
    Convert annual interest rate to monthly interest rate.

    Args:
    interest_rate (float): Annual interest rate expressed as a decimal (e.g., 0.1 for 10%).

    Returns:
    float: Monthly interest rate expressed as a decimal.
    """
    monthly_IR = interest_rate / 12
    return round(monthly_IR,6)

    
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
    

def calculate_closing_balance(opening_balance, principal_amount):
    return round(opening_balance - principal_amount, 2)    