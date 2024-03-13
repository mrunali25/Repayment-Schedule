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

    
 
    