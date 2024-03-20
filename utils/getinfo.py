import numpy as np
import pandas as pd

def IR_from_repayment_schedule(dataframe):
    """
    Calculate monthly and annual interest rates from the repayment schedule dataframe.

    Args:
    dataframe (pandas DataFrame): Repayment schedule dataframe.

    Returns:
    tuple: A tuple containing monthly interest rate and annual interest rate.
    """
    df = dataframe
    # Round the intermediate calculation to 9 decimal places as you did
    monthly_IR = df.loc[1, 'Interest Amount'] / df.loc[0, 'Closing Balance']
    monthly_IR_str = "{:.9f}".format(monthly_IR).rstrip('0').rstrip('.')
    monthly_IR = float(monthly_IR_str)

    # Now, round the annual interest rate to 6 decimal places
    annual_IR = monthly_IR * 12
    annual_IR = round(annual_IR,6)
    
    return monthly_IR, annual_IR

   
def principal_emi_from_repayment_schedule(dataframe):
        """
        Extract principal amount and EMI from the repayment schedule dataframe.

        Args:
        dataframe (pandas DataFrame): Repayment schedule dataframe.

        Returns:
        tuple: A tuple containing principal amount and EMI.
        """
        df = dataframe
        principle = df.loc[0, 'Closing Balance']
        emi = df.loc[1, 'Installment Amount']
        return principle, emi


