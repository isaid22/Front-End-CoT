import numpy_financial as npf

def calculate_affordability(
    annual_income: float,
    monthly_debt: float,
    home_price: float,
    down_payment_percent: float = 20.0,
    rate: float = 6.5,
    year: int = 30,
    dti_limit: float = 0.43,
    property_tax_rate: float = 1.2,
    home_insurance_rate: float = 0.5,
):
    """
    Calculates mortgage affordability based on user inputs.

    Returns:
        A tuple containing:
        - is_affordable (str): "affordable" or "not affordable"
        - monthly_payment (float): The estimated monthly PITI payment.
        - max_monthly_budget (float): The maximum monthly payment the user can afford based on DTI.
    """
    # 1. Calculate loan amount
    down_payment = home_price * (down_payment_percent / 100)
    loan_amount = home_price - down_payment

    # 2. Calculate monthly Principal & Interest (P&I)
    monthly_rate = (rate / 100) / 12
    n_payments = year * 12
    principal_and_interest = -npf.pmt(monthly_rate, n_payments, loan_amount)

    # 3. Calculate monthly Taxes & Insurance (T&I)
    property_tax = (home_price * (property_tax_rate / 100)) / 12
    home_insurance = (home_price * (home_insurance_rate / 100)) / 12
    
    # 4. Total estimated monthly payment (PITI)
    total_monthly_payment = principal_and_interest + property_tax + home_insurance

    # 5. Calculate max affordable payment based on DTI
    monthly_gross_income = annual_income / 12
    max_total_debt = monthly_gross_income * dti_limit
    max_monthly_budget_for_mortgage = max_total_debt - monthly_debt

    # 6. Determine affordability
    is_affordable_bool = total_monthly_payment <= max_monthly_budget_for_mortgage
    affordability_status = "affordable" if is_affordable_bool else "not affordable"

    return affordability_status, total_monthly_payment, max_monthly_budget_for_mortgage
