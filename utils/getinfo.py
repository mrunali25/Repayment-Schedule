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
        monthly_IR = df.loc[1, 'REVENUE'] / df.loc[1, 'OPBAL']
        annual_IR = monthly_IR * 12
        return monthly_IR, round(annual_IR, 6)

   
def principal_emi_from_repayment_schedule(dataframe):
        """
        Extract principal amount and EMI from the repayment schedule dataframe.

        Args:
        dataframe (pandas DataFrame): Repayment schedule dataframe.

        Returns:
        tuple: A tuple containing principal amount and EMI.
        """
        df = dataframe
        principle = df.loc[0, 'CLBAL']
        emi = df.loc[1, 'FLOW AMT']
        return principle, emi


