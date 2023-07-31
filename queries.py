# Aggregate financial data for the banking industry
# Calculate the total quarterly net income for the banking industry over the last four decades.
bank_income_query = """SELECT att.variable_name,
       ts.date,
       ts.value
FROM cybersyn.financial_fred_timeseries AS ts
JOIN cybersyn.financial_fred_attributes AS att ON (ts.variable = att.variable)
WHERE att.variable_name = 'Income and Expense: Net Income (Loss) Attributable to Bank, Not seasonally adjusted, Quarterly, USD'
  AND ts.date >= '1984-01-01';
"""

# FDIC deposit exposure
# Determine which banks have the highest percentage of uninsured deposits.
fdic_exposure_query = """WITH big_banks AS (
    SELECT id_rssd
    FROM cybersyn.financial_institution_timeseries
    WHERE variable = 'ASSET'
      AND value > 1E10
)
SELECT name,
       1 - value AS pct_uninsured,
       ts.date,
       ent.is_active
FROM cybersyn.financial_institution_timeseries AS ts
INNER JOIN cybersyn.financial_institution_attributes AS att ON (ts.variable = att.variable)
INNER JOIN cybersyn.financial_institution_entities AS ent ON (ts.id_rssd = ent.id_rssd)
INNER JOIN big_banks ON (big_banks.id_rssd = ts.id_rssd)
  AND att.variable_name = '% Insured (Estimated)'
  AND att.frequency = 'Quarterly'
"""

# Credit card company complaints
credit_card_complaints_query = """
SELECT company,
       date_received AS date,
       credit_card_complaint
FROM cybersyn.financial_cfpb_complaint
WHERE product ILIKE '%card%'
  AND date_received >= '2012-01-01'
"""

# Evaluate central bank interest rate policies
# Compare and contrast interest rate policies for major global economies
central_bank_interest_rates_query = """
SELECT TO_DATE(ts.date) AS date,
       ts.variable_name,
       ts.value
FROM cybersyn.financial_fred_timeseries AS ts
JOIN cybersyn.financial_fred_attributes AS att
    ON (att.variable = ts.variable)
WHERE variable_group IN ('Bank of Brazil Selic Interest Rate Target',
                         'Bank of Canada Overnight Lending Rate',
                         'Bank of England Official Bank Rate',
                         'Bank of Japan Policy-Rate Balance Rate',
                         'Bank of Mexico Official Overnight Target Rate',
                         'ECB Main Refinancing Operations Rate: Fixed Rate Tenders for Euro Area',
                         'Federal Funds Effective Rate');
"""


queries_dict = {
    "FDIC Exposure": {
        "description": "FDIC deposit exposure. Can be used to determine which banks have the highest percentage of uninsured deposits.",
        "query": fdic_exposure_query,
    },
    "Credit Card Complaints": {
        "description": " Credit card company complaints. Can be used to count credit card complaints by month by company",
        "query": bank_income_query,
    },
    "Central Bank Interest Rates": {
        "description": "Evaluate central bank interest rate policies. Can be used to compare and contrast interest rate policies for major global economies",
        "query": central_bank_interest_rates_query,
    },
    "Bank Income": {
        "description": "Aggregate financial data for the banking industry",
        "query": bank_income_query,
    },
}

