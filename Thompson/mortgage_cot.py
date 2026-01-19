import sys
import yaml
from bedrock_access import get_chat_response
from calculations import calculate_affordability

def run_demo():
    print("--- Mortgage Affordability CoT Demo ---")
    
    # Get inputs with defaults
    try:
        try:
            val = input("Annual income (e.g., 120000): ")
            annual_income = float(val) if val else 120000.0
        except ValueError: annual_income = 120000.0

        try:
            val = input("Monthly debt (e.g., 600): ")
            monthly_debt = float(val) if val else 600.0
        except ValueError: monthly_debt = 600.0

        try:
            val = input("Home price of interest (e.g., 420000): ")
            home_price = float(val) if val else 420000.0
        except ValueError: home_price = 420000.0

        try:
            val = input("Interest rate (e.g., 6.5): ")
            rate = float(val) if val else 6.5
        except ValueError: rate = 6.5

        try:
            val = input("Mortgage term in years (e.g., 30): ")
            years = int(val) if val else 30
        except ValueError: years = 30
        
        dti_limit = 0.43
        
    except KeyboardInterrupt:
        sys.exit(0)

    # Calculate metrics using the python function
    is_affordable, monthly_payment, max_monthly_budget = calculate_affordability(
        annual_income=annual_income,
        monthly_debt=monthly_debt,
        home_price=home_price,
        rate=rate,
        year=years,
        dti_limit=dti_limit,
    )

    # Prompt Construction
    system_prompt = """You are a mortgage affordability assistant. 

Instructions:
Walk through the math step-by-step to explain *why* the system determined the affordability status.
IMPORTANT: Use plain text only for calculations. Do NOT use LaTeX formatting (e.g., no \[ or \frac).
1. Calculate monthly gross income.
2. Verify the max total debt allowed.
3. Explain the remaining budget for a mortgage.
4. Compare the estimated payment to the budget."""

    user_message = f"""User inputs:
- Annual income: ${annual_income}
- Monthly debt: ${monthly_debt}
- Home price: ${home_price}
- Interest rate: {rate}%
- Term: {years} years
- DTI limit: {dti_limit}

The system has pre-calculated the following:
- Estimated Monthly Payment: ${monthly_payment:.2f}
- Max Monthly Budget: ${max_monthly_budget:.2f}
- Affordability: {is_affordable}

Answer: Let's think step by step."""

    model_id = "amazon.nova-micro-v1:0"

    print(f"\nModel: {model_id}")
    print("\n--- Sending request to LLM (Bedrock) ---\n")
    
    # Call Bedrock
    response_text = get_chat_response(
        model_id=model_id,
        system_prompt=system_prompt,
        user_message=user_message,
        temperature=0.1
    )
    
    print("\n--- Response ---\n")
    print(response_text)


if __name__ == "__main__":
    run_demo()
