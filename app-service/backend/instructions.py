
# Instructions is a copy of the instructions sheet in the google doc.
# This page contains all the data to merge into the calculations. 
def get_instructions_data(data_variables):
    nineteen_ADJUSTED_GROSS_INCOME = int(data_variables[0]['2019']['ADJUSTED GROSS INCOME'])
    # Check if the variable is null, if so, assign it a default value of 0
    if nineteen_ADJUSTED_GROSS_INCOME is None:
        nineteen_ADJUSTED_GROSS_INCOME = 0

    nineteen_FILING_STATUS = data_variables[0]['2019']['FILING STATUS']
    # Check if the variable is null, if so, assign it a default value of 0
    if nineteen_FILING_STATUS is None:
        nineteen_FILING_STATUS = ''

    nineteen_credit_to_your_account = int(data_variables[0]['2019']['Credit to your account'])
    # Check if the variable is null, if so, assign it a default value of 0
    if nineteen_credit_to_your_account is None:
        nineteen_credit_to_your_account = 0

    nineteen_account_balance = int(data_variables[0]['2019']['ACCOUNT BALANCE'])
    # Check if the variable is null, if so, assign it a default value of 0
    if nineteen_account_balance is None:
        nineteen_account_balance = 0

    nineteen_accrued_interest = int(data_variables[0]['2019']['ACCRUED INTEREST'])
    # Check if the variable is null, if so, assign it a default value of 0
    if nineteen_accrued_interest is None:
        nineteen_accrued_interest = 0

    nineteen_taxable_income = int(data_variables[0]['2019']['TAXABLE INCOME'])
    # Check if the variable is null, if so, assign it a default value of 0
    if nineteen_taxable_income is None:
        nineteen_taxable_income = 0

    nineteen_tax_per_return = int(data_variables[0]['2019']['TAX PER RETURN'])
    # Check if the variable is null, if so, assign it a default value of 0
    if nineteen_tax_per_return is None:
        nineteen_tax_per_return = 0



    #Data variable for 2020 
    twenty_qualified_business_income_deduction_computer = int(data_variables[0]['2020']['F8995 QUALIFIED BUSINESS INCOME DEDUCTION COMPUTER'])
    if twenty_qualified_business_income_deduction_computer is None:
        twenty_qualified_business_income_deduction_computer = 0

    twenty_self_employment_tax_deduction_per_computer = int(data_variables[0]['2020']['SELF EMPLOYMENT TAX DEDUCTION PER COMPUTER'])
    if twenty_self_employment_tax_deduction_per_computer is None:
        twenty_self_employment_tax_deduction_per_computer = 0

    twenty_adjusted_gross_income = int(data_variables[0]['2020']['ADJUSTED GROSS INCOME'])
    if twenty_adjusted_gross_income is None:
        twenty_adjusted_gross_income = 0

    twenty_adjusted_gross_income_per_computer = int(data_variables[0]['2020']['ADJUSTED GROSS INCOME PER COMPUTER'])
    if twenty_adjusted_gross_income_per_computer is None:
        twenty_adjusted_gross_income_per_computer = 0

    twenty_standard_deduction_per_computer = int(data_variables[0]['2020']['STANDARD DEDUCTION PER COMPUTER'])
    if twenty_standard_deduction_per_computer is None:
        twenty_standard_deduction_per_computer = 0

    twenty_tentative_tax = int(data_variables[0]['2020']['TENTATIVE TAX'])
    if twenty_tentative_tax is None:
        twenty_tentative_tax = 0

    twenty_total_credits = int(data_variables[0]['2020']['TOTAL CREDITS'])
    if twenty_total_credits is None:
        twenty_total_credits = 0

    twenty_SE_tax = int(data_variables[0]['2020']['SE TAX'])
    if twenty_SE_tax is None:
        twenty_SE_tax = 0

    twenty_federal_income_tax_withheld = int(data_variables[0]['2020']['FEDERAL INCOME TAX WITHHELD'])
    if twenty_federal_income_tax_withheld is None:
        twenty_federal_income_tax_withheld = 0

    twenty_estimated_tax_payments = int(data_variables[0]['2020']['ESTIMATED TAX PAYMENTS'])
    if twenty_estimated_tax_payments is None:
        twenty_estimated_tax_payments = 0

    twenty_other_payment_credit = int(data_variables[0]['2020']['OTHER PAYMENT CREDIT'])
    if twenty_other_payment_credit is None:
        twenty_other_payment_credit = 0

    twenty_earned_income_credit = int(data_variables[0]['2020']['EARNED INCOME CREDIT'])
    if twenty_earned_income_credit is None:
        twenty_earned_income_credit = 0

    twenty_total_payments = int(data_variables[0]['2020']['TOTAL PAYMENTS'])
    if twenty_total_payments is None:
        twenty_total_payments = 0

    twenty_balance_due_overpayment_using_TP_figure_per_computer = int(data_variables[0]['2020']['BAL DUE/OVER PYMT USING TP FIG PER COMPUTER'])
    if twenty_balance_due_overpayment_using_TP_figure_per_computer is None:
        twenty_balance_due_overpayment_using_TP_figure_per_computer = 0

    twenty_total_qualified_business_income_or_loss = int(data_variables[0]['2020']['TOTAL QUALIFIED BUSINESS INCOME OR LOSS'])
    if twenty_total_qualified_business_income_or_loss is None:
        twenty_total_qualified_business_income_or_loss = 0

    twenty_filing_status = data_variables[0]['2020']['FILING STATUS']
    if twenty_filing_status is None:
        twenty_filing_status = ''

    twenty_SE_income_per_computer = int(data_variables[0]['2020']['SE INCOME PER COMPUTER'])
    if twenty_SE_income_per_computer is None:
        twenty_SE_income_per_computer = 0

    twenty_credit_to_your_account = int(data_variables[0]['2020']['Credit to your account'])
    if twenty_credit_to_your_account is None:
        twenty_credit_to_your_account = 0

    twenty_account_balance = int(data_variables[0]['2020']['ACCOUNT BALANCE'])
    if twenty_account_balance is None:
        twenty_account_balance = 0

    twenty_accrued_interest = int(data_variables[0]['2020']['ACCRUED INTEREST'])
    if twenty_accrued_interest is None:
        twenty_accrued_interest = 0

    twenty_taxable_income = int(data_variables[0]['2020']['TAXABLE INCOME'])
    if twenty_taxable_income is None:
        twenty_taxable_income = 0

    twenty_tax_per_return = int(data_variables[0]['2020']['TAX PER RETURN'])
    if twenty_tax_per_return is None:
        twenty_tax_per_return = 0

    twenty_schedule_8812_additional_child_tax_credit = int(data_variables[0]['2020']['SCHEDULE 8812 ADDITIONAL CHILD TAX CREDIT'])
    if twenty_schedule_8812_additional_child_tax_credit is None:
        twenty_schedule_8812_additional_child_tax_credit = 0

    twenty_form_2439_regulated_investment_company_credit = int(data_variables[0]['2020']['FORM 2439 REGULATED INVESTMENT COMPANY CREDIT'])
    if twenty_form_2439_regulated_investment_company_credit is None:
        twenty_form_2439_regulated_investment_company_credit = 0

    twenty_form_4136_credit_for_federal_tax_on_fuels_per_computer = int(data_variables[0]['2020']['FORM 4136 CREDIT FOR FEDERAL TAX ON FUELS PER COMPUTER'])
    if twenty_form_4136_credit_for_federal_tax_on_fuels_per_computer is None:
        twenty_form_4136_credit_for_federal_tax_on_fuels_per_computer = 0

    twenty_total_education_credit_amount_per_computer = int(data_variables[0]['2020']['TOTAL EDUCATION CREDIT AMOUNT PER COMPUTER'])
    if twenty_total_education_credit_amount_per_computer is None:
        twenty_total_education_credit_amount_per_computer = 0

    twenty_health_coverage_TX_credit_F8885 = int(data_variables[0]['2020']['HEALTH COVERAGE TX CR'])
    if twenty_health_coverage_TX_credit_F8885 is None:
        twenty_health_coverage_TX_credit_F8885 = 0

    twenty_amount_you_owe = int(data_variables[0]['2020']['AMOUNT YOU OWE'])
    if twenty_amount_you_owe is None:
        twenty_amount_you_owe = 0

    twenty_refund_amount = int(data_variables[0]['2020']['REFUND AMOUNT'])
    if twenty_refund_amount is None:
        twenty_refund_amount = 0

    twenty_sick_family_leave_credit_after_3_31_21 = int(data_variables[0]['2020']['SICK FAMILY LEAVE CREDIT AFTER 3-31-21'])
    if twenty_sick_family_leave_credit_after_3_31_21 is None:
        twenty_sick_family_leave_credit_after_3_31_21 = 0

    twenty_wages_salaries_tips_etc = int(data_variables[0]['2020']['WAGES, SALARIES, TIPS, ETC'])
    if twenty_wages_salaries_tips_etc is None:
        twenty_wages_salaries_tips_etc = 0

    twenty_tax_exempt_interest = int(data_variables[0]['2020']['TAX-EXEMPT INTEREST'])
    if twenty_tax_exempt_interest is None:
        twenty_tax_exempt_interest = 0

    twenty_qualified_dividends = int(data_variables[0]['2020']['QUALIFIED DIVIDENDS'])
    if twenty_qualified_dividends is None:
        twenty_qualified_dividends = 0

    twenty_total_IRA_distributions = int(data_variables[0]['2020']['TOTAL IRA DISTRIBUTIONS'])
    if twenty_total_IRA_distributions is None:
        twenty_total_IRA_distributions = 0

    twenty_total_pensions_and_annuities = int(data_variables[0]['2020']['TOTAL PENSIONS AND ANNUITIES'])
    if twenty_total_pensions_and_annuities is None:
        twenty_total_pensions_and_annuities = 0

    twenty_total_social_security_benefits = int(data_variables[0]['2020']['TOTAL SOCIAL SECURITY BENEFITS'])
    if twenty_total_social_security_benefits is None:
        twenty_total_social_security_benefits = 0

    twenty_taxable_interest_income = int(data_variables[0]['2020']['TAXABLE INTEREST INCOME'])
    if twenty_taxable_interest_income is None:
        twenty_taxable_interest_income = 0

    twenty_ordinary_dividend_income = int(data_variables[0]['2020']['ORDINARY DIVIDEND INCOME'])
    if twenty_ordinary_dividend_income is None:
        twenty_ordinary_dividend_income = 0

    twenty_taxable_IRA_distributions = int(data_variables[0]['2020']['TAXABLE IRA DISTRIBUTIONS'])
    if twenty_taxable_IRA_distributions is None:
        twenty_taxable_IRA_distributions = 0

    twenty_taxable_pension_annuity_amount = int(data_variables[0]['2020']['TAXABLE PENSION/ANNUITY AMOUNT'])
    if twenty_taxable_pension_annuity_amount is None:
        twenty_taxable_pension_annuity_amount = 0

    twenty_taxable_social_security_benefits_per_computer = int(data_variables[0]['2020']['TAXABLE SOCIAL SECURITY BENEFITS PER COMPUTER'])
    if twenty_taxable_social_security_benefits_per_computer is None:
        twenty_taxable_social_security_benefits_per_computer = 0

    twenty_capital_gain_or_loss = int(data_variables[0]['2020']['CAPITAL GAIN OR LOSS'])
    if twenty_capital_gain_or_loss is None:
        twenty_capital_gain_or_loss = 0

    twenty_other_income = int(data_variables[0]['2020']['OTHER INCOME'])
    if twenty_other_income is None:
        twenty_other_income = 0

    twenty_total_adjustments_per_computer = int(data_variables[0]['2020']['TOTAL ADJUSTMENTS PER COMPUTER'])
    if twenty_total_adjustments_per_computer is None:
        twenty_total_adjustments_per_computer = 0

    twenty_non_itemized_charitable_contribution_per_computer = int(data_variables[0]['2020']['NON ITEMIZED CHARITABLE CONTRIBUTION PER COMPUTER'])
    if twenty_non_itemized_charitable_contribution_per_computer is None:
        twenty_non_itemized_charitable_contribution_per_computer = 0

    twenty_business_income_or_loss_schedule_C = int(data_variables[0]['2020']['BUSINESS INCOME OR LOSS (SCHEDULE C)'])
    if twenty_business_income_or_loss_schedule_C is None:
        twenty_business_income_or_loss_schedule_C = 0

    twenty_child_and_other_dependent_credit_per_computer = int(data_variables[0]['2020']['CHILD AND OTHER DEPENDENT CREDIT PER COMPUTER'])
    if twenty_child_and_other_dependent_credit_per_computer is None:
        twenty_child_and_other_dependent_credit_per_computer = 0

    twenty_excess_advance_premium_tax_credit_repayment_amount = int(data_variables[0]['2020']['EXCESS ADVANCE PREMIUM TAX CREDIT REPAYMENT AMOUNT'])
    if twenty_excess_advance_premium_tax_credit_repayment_amount is None:
        twenty_excess_advance_premium_tax_credit_repayment_amount = 0

    twenty_sec_965_tax_installment = int(data_variables[0]['2020']['SEC 965 TAX INSTALLMENT'])
    if twenty_sec_965_tax_installment is None:
        twenty_sec_965_tax_installment = 0

    twenty_child_dependent_care_credit = int(data_variables[0]['2020']['CHILD & DEPENDENT CARE CREDIT'])
    if twenty_child_dependent_care_credit is None:
        twenty_child_dependent_care_credit = 0

    twenty_estimated_tax_penalty = int(data_variables[0]['2020']['ESTIMATED TAX PENALTY'])
    if twenty_estimated_tax_penalty is None:
        twenty_estimated_tax_penalty = 0

    twenty_applied_to_next_years_estimated_tax = int(data_variables[0]['2020']['APPLIED TO NEXT YEAR\'S ESTIMATED TAX'])
    if twenty_applied_to_next_years_estimated_tax is None:
        twenty_applied_to_next_years_estimated_tax = 0

    twenty_earned_income_credit_nontaxable_combat_pay = int(data_variables[0]['2020']['EARNED INCOME CREDIT NONTAXABLE COMBAT PAY'])
    if twenty_earned_income_credit_nontaxable_combat_pay is None:
        twenty_earned_income_credit_nontaxable_combat_pay = 0

    twenty_max_deferred_tax_per_computer = int(data_variables[0]['2020']['MAX DEFERRED TAX PER COMPUTER'])
    if twenty_max_deferred_tax_per_computer is None:
        twenty_max_deferred_tax_per_computer = 0

    twenty_EIC_prior_year_earned_income = int(data_variables[0]['2020']['EIC PRIOR YEAR EARNED INCOME'])
    if twenty_EIC_prior_year_earned_income is None:
        twenty_EIC_prior_year_earned_income = 0

            

    # Data for 2021 
    twenty_twenty_one_qualified_business_income_deduction_computer = int(data_variables[0]['2021']['F8995 QUALIFIED BUSINESS INCOME DEDUCTION COMPUTER'])
    if twenty_twenty_one_qualified_business_income_deduction_computer is None:
        twenty_twenty_one_qualified_business_income_deduction_computer = 0

    twenty_twenty_one_self_employment_tax_deduction_per_computer = int(data_variables[0]['2021']['SELF EMPLOYMENT TAX DEDUCTION PER COMPUTER'])
    if twenty_twenty_one_self_employment_tax_deduction_per_computer is None:
        twenty_twenty_one_self_employment_tax_deduction_per_computer = 0

    twenty_twenty_one_adjusted_gross_income = int(data_variables[0]['2021']['ADJUSTED GROSS INCOME'])
    if twenty_twenty_one_adjusted_gross_income is None:
        twenty_twenty_one_adjusted_gross_income = 0

    twenty_twenty_one_adjusted_gross_income_per_computer = int(data_variables[0]['2021']['ADJUSTED GROSS INCOME PER COMPUTER'])
    if twenty_twenty_one_adjusted_gross_income_per_computer is None:
        twenty_twenty_one_adjusted_gross_income_per_computer = 0

    twenty_twenty_one_standard_deduction_per_computer = int(data_variables[0]['2021']['STANDARD DEDUCTION PER COMPUTER'])
    if twenty_twenty_one_standard_deduction_per_computer is None:
        twenty_twenty_one_standard_deduction_per_computer = 0

    twenty_twenty_one_tentative_tax = int(data_variables[0]['2021']['TENTATIVE TAX'])
    if twenty_twenty_one_tentative_tax is None:
        twenty_twenty_one_tentative_tax = 0

    twenty_twenty_one_total_credits = int(data_variables[0]['2021']['TOTAL CREDITS'])
    if twenty_twenty_one_total_credits is None:
        twenty_twenty_one_total_credits = 0

    twenty_twenty_one_SE_tax = int(data_variables[0]['2021']['SE TAX'])
    if twenty_twenty_one_SE_tax is None:
        twenty_twenty_one_SE_tax = 0

    twenty_twenty_one_federal_income_tax_withheld = int(data_variables[0]['2021']['FEDERAL INCOME TAX WITHHELD'])
    if twenty_twenty_one_federal_income_tax_withheld is None:
        twenty_twenty_one_federal_income_tax_withheld = 0

    twenty_twenty_one_estimated_tax_payments = int(data_variables[0]['2021']['ESTIMATED TAX PAYMENTS'])
    if twenty_twenty_one_estimated_tax_payments is None:
        twenty_twenty_one_estimated_tax_payments = 0

    twenty_twenty_one_other_payment_credit = int(data_variables[0]['2021']['OTHER PAYMENT CREDIT'])
    if twenty_twenty_one_other_payment_credit is None:
        twenty_twenty_one_other_payment_credit = 0

    twenty_twenty_one_earned_income_credit = int(data_variables[0]['2021']['EARNED INCOME CREDIT'])
    if twenty_twenty_one_earned_income_credit is None:
        twenty_twenty_one_earned_income_credit = 0

    twenty_twenty_one_total_payments = int(data_variables[0]['2021']['TOTAL PAYMENTS'])
    if twenty_twenty_one_total_payments is None:
        twenty_twenty_one_total_payments = 0

    twenty_twenty_one_balance_due_overpayment_using_TP_figure_per_computer = int(data_variables[0]['2021']['BAL DUE/OVER PYMT USING TP FIG PER COMPUTER'])
    if twenty_twenty_one_balance_due_overpayment_using_TP_figure_per_computer is None:
        twenty_twenty_one_balance_due_overpayment_using_TP_figure_per_computer = 0

    twenty_twenty_one_total_qualified_business_income_or_loss = int(data_variables[0]['2021']['TOTAL QUALIFIED BUSINESS INCOME OR LOSS'])
    if twenty_twenty_one_total_qualified_business_income_or_loss is None:
        twenty_twenty_one_total_qualified_business_income_or_loss = 0

    twenty_twenty_one_filing_status = data_variables[0]['2021']['FILING STATUS']
    if twenty_twenty_one_filing_status is None:
        twenty_twenty_one_filing_status = ''

    twenty_twenty_one_SE_income_per_computer = int(data_variables[0]['2021']['SE INCOME PER COMPUTER'])
    if twenty_twenty_one_SE_income_per_computer is None:
        twenty_twenty_one_SE_income_per_computer = 0

    twenty_twenty_one_credit_to_your_account = int(data_variables[0]['2021']['Credit to your account'])
    if twenty_twenty_one_credit_to_your_account is None:
        twenty_twenty_one_credit_to_your_account = 0

    twenty_twenty_one_account_balance = int(data_variables[0]['2021']['ACCOUNT BALANCE'])
    if twenty_twenty_one_account_balance is None:
        twenty_twenty_one_account_balance = 0

    twenty_twenty_one_accrued_interest = int(data_variables[0]['2021']['ACCRUED INTEREST'])
    if twenty_twenty_one_accrued_interest is None:
        twenty_twenty_one_accrued_interest = 0

    twenty_twenty_one_taxable_income = int(data_variables[0]['2021']['TAXABLE INCOME'])
    if twenty_twenty_one_taxable_income is None:
        twenty_twenty_one_taxable_income = 0

    twenty_twenty_one_tax_per_return = int(data_variables[0]['2021']['TAX PER RETURN'])
    if twenty_twenty_one_tax_per_return is None:
        twenty_twenty_one_tax_per_return = 0

    twenty_twenty_one_schedule_8812_additional_child_tax_credit = int(data_variables[0]['2021']['SCHEDULE 8812 ADDITIONAL CHILD TAX CREDIT'])
    if twenty_twenty_one_schedule_8812_additional_child_tax_credit is None:
        twenty_twenty_one_schedule_8812_additional_child_tax_credit = 0

    twenty_twenty_one_form_2439_regulated_investment_company_credit = int(data_variables[0]['2021']['FORM 2439 REGULATED INVESTMENT COMPANY CREDIT'])
    if twenty_twenty_one_form_2439_regulated_investment_company_credit is None:
        twenty_twenty_one_form_2439_regulated_investment_company_credit = 0

    twenty_twenty_one_form_4136_credit_for_federal_tax_on_fuels_per_computer = int(data_variables[0]['2021']['FORM 4136 CREDIT FOR FEDERAL TAX ON FUELS PER COMPUTER'])
    if twenty_twenty_one_form_4136_credit_for_federal_tax_on_fuels_per_computer is None:
        twenty_twenty_one_form_4136_credit_for_federal_tax_on_fuels_per_computer = 0

    twenty_twenty_one_total_education_credit_amount_per_computer = int(data_variables[0]['2021']['TOTAL EDUCATION CREDIT AMOUNT PER COMPUTER'])
    if twenty_twenty_one_total_education_credit_amount_per_computer is None:
        twenty_twenty_one_total_education_credit_amount_per_computer = 0

    twenty_twenty_one_health_coverage_TX_credit_F8885 = int(data_variables[0]['2021']['HEALTH COVERAGE TX CR'])
    if twenty_twenty_one_health_coverage_TX_credit_F8885 is None:
        twenty_twenty_one_health_coverage_TX_credit_F8885 = 0

    twenty_twenty_one_amount_you_owe = int(data_variables[0]['2021']['AMOUNT YOU OWE'])
    if twenty_twenty_one_amount_you_owe is None:
        twenty_twenty_one_amount_you_owe = 0

    twenty_twenty_one_refund_amount = int(data_variables[0]['2021']['REFUND AMOUNT'])
    if twenty_twenty_one_refund_amount is None:
        twenty_twenty_one_refund_amount = 0

    twenty_twenty_one_wages_salaries_tips_etc = int(data_variables[0]['2021']['WAGES, SALARIES, TIPS, ETC'])
    if twenty_twenty_one_wages_salaries_tips_etc is None:
        twenty_twenty_one_wages_salaries_tips_etc = 0

    twenty_twenty_one_tax_exempt_interest = int(data_variables[0]['2021']['TAX-EXEMPT INTEREST'])
    if twenty_twenty_one_tax_exempt_interest is None:
        twenty_twenty_one_tax_exempt_interest = 0

    twenty_twenty_one_qualified_dividends = int(data_variables[0]['2021']['QUALIFIED DIVIDENDS'])
    if twenty_twenty_one_qualified_dividends is None:
        twenty_twenty_one_qualified_dividends = 0

    twenty_twenty_one_total_IRA_distributions = int(data_variables[0]['2021']['TOTAL IRA DISTRIBUTIONS'])
    if twenty_twenty_one_total_IRA_distributions is None:
        twenty_twenty_one_total_IRA_distributions = 0

    twenty_twenty_one_total_pensions_and_annuities = int(data_variables[0]['2021']['TOTAL PENSIONS AND ANNUITIES'])
    if twenty_twenty_one_total_pensions_and_annuities is None:
        twenty_twenty_one_total_pensions_and_annuities = 0

    twenty_twenty_one_total_social_security_benefits = int(data_variables[0]['2021']['TOTAL SOCIAL SECURITY BENEFITS'])
    if twenty_twenty_one_total_social_security_benefits is None:
        twenty_twenty_one_total_social_security_benefits = 0

    twenty_twenty_one_taxable_interest_income = int(data_variables[0]['2021']['TAXABLE INTEREST INCOME'])
    if twenty_twenty_one_taxable_interest_income is None:
        twenty_twenty_one_taxable_interest_income = 0

    twenty_twenty_one_ordinary_dividend_income = int(data_variables[0]['2021']['ORDINARY DIVIDEND INCOME'])
    if twenty_twenty_one_ordinary_dividend_income is None:
        twenty_twenty_one_ordinary_dividend_income = 0

    twenty_twenty_one_taxable_IRA_distributions = int(data_variables[0]['2021']['TAXABLE IRA DISTRIBUTIONS'])
    if twenty_twenty_one_taxable_IRA_distributions is None:
        twenty_twenty_one_taxable_IRA_distributions = 0

    twenty_twenty_one_taxable_pension_annuity_amount = int(data_variables[0]['2021']['TAXABLE PENSION/ANNUITY AMOUNT'])
    if twenty_twenty_one_taxable_pension_annuity_amount is None:
        twenty_twenty_one_taxable_pension_annuity_amount = 0

    twenty_twenty_one_taxable_social_security_benefits_per_computer = int(data_variables[0]['2021']['TAXABLE SOCIAL SECURITY BENEFITS PER COMPUTER'])
    if twenty_twenty_one_taxable_social_security_benefits_per_computer is None:
        twenty_twenty_one_taxable_social_security_benefits_per_computer = 0

    twenty_twenty_one_capital_gain_or_loss = int(data_variables[0]['2021']['CAPITAL GAIN OR LOSS'])
    if twenty_twenty_one_capital_gain_or_loss is None:
        twenty_twenty_one_capital_gain_or_loss = 0

    twenty_twenty_one_other_income = int(data_variables[0]['2021']['OTHER INCOME'])
    if twenty_twenty_one_other_income is None:
        twenty_twenty_one_other_income = 0

    twenty_twenty_one_total_adjustments_per_computer = int(data_variables[0]['2021']['TOTAL ADJUSTMENTS PER COMPUTER'])
    if twenty_twenty_one_total_adjustments_per_computer is None:
        twenty_twenty_one_total_adjustments_per_computer = 0

    twenty_twenty_one_non_itemized_charitable_contribution_per_computer = int(data_variables[0]['2021']['NON ITEMIZED CHARITABLE CONTRIBUTION PER COMPUTER'])
    if twenty_twenty_one_non_itemized_charitable_contribution_per_computer is None:
        twenty_twenty_one_non_itemized_charitable_contribution_per_computer = 0

    twenty_twenty_one_business_income_or_loss_schedule_C = int(data_variables[0]['2021']['BUSINESS INCOME OR LOSS (SCHEDULE C)'])
    if twenty_twenty_one_business_income_or_loss_schedule_C is None:
        twenty_twenty_one_business_income_or_loss_schedule_C = 0

    twenty_twenty_one_child_and_other_dependent_credit_per_computer = int(data_variables[0]['2021']['CHILD AND OTHER DEPENDENT CREDIT PER COMPUTER'])
    if twenty_twenty_one_child_and_other_dependent_credit_per_computer is None:
        twenty_twenty_one_child_and_other_dependent_credit_per_computer = 0

    twenty_twenty_one_excess_advance_premium_tax_credit_repayment_amount = int(data_variables[0]['2021']['EXCESS ADVANCE PREMIUM TAX CREDIT REPAYMENT AMOUNT'])
    if twenty_twenty_one_excess_advance_premium_tax_credit_repayment_amount is None:
        twenty_twenty_one_excess_advance_premium_tax_credit_repayment_amount = 0

    twenty_twenty_one_sec_965_tax_installment = int(data_variables[0]['2021']['SEC 965 TAX INSTALLMENT'])
    if twenty_twenty_one_sec_965_tax_installment is None:
        twenty_twenty_one_sec_965_tax_installment = 0

    twenty_twenty_one_child_dependent_care_credit = int(data_variables[0]['2021']['CHILD & DEPENDENT CARE CREDIT'])
    if twenty_twenty_one_child_dependent_care_credit is None:
        twenty_twenty_one_child_dependent_care_credit = 0

    twenty_twenty_one_estimated_tax_penalty = int(data_variables[0]['2021']['ESTIMATED TAX PENALTY'])
    if twenty_twenty_one_estimated_tax_penalty is None:
        twenty_twenty_one_estimated_tax_penalty = 0

    twenty_twenty_one_applied_to_next_years_estimated_tax = int(data_variables[0]['2021']['APPLIED TO NEXT YEAR\'S ESTIMATED TAX'])
    if twenty_twenty_one_applied_to_next_years_estimated_tax is None:
        twenty_twenty_one_applied_to_next_years_estimated_tax = 0

    twenty_twenty_one_earned_income_credit_nontaxable_combat_pay = int(data_variables[0]['2021']['EARNED INCOME CREDIT NONTAXABLE COMBAT PAY'])
    if twenty_twenty_one_earned_income_credit_nontaxable_combat_pay is None:
        twenty_twenty_one_earned_income_credit_nontaxable_combat_pay = 0

    twenty_twenty_one_max_deferred_tax_per_computer = int(data_variables[0]['2021']['MAX DEFERRED TAX PER COMPUTER'])
    if twenty_twenty_one_max_deferred_tax_per_computer is None:
        twenty_twenty_one_max_deferred_tax_per_computer = 0

    twenty_twenty_one_EIC_prior_year_earned_income = int(data_variables[0]['2021']['EIC PRIOR YEAR EARNED INCOME'])
    if twenty_twenty_one_EIC_prior_year_earned_income is None:
        twenty_twenty_one_EIC_prior_year_earned_income = 0



    # Data from Zoho
    Child_April_1_2020_through_December_31_2020 = data_variables[0]['old_intake_data'].get("Child_April_1_2020_through_December_31_2020", 0)
    if Child_April_1_2020_through_December_31_2020 == '' or Child_April_1_2020_through_December_31_2020 == '-':
        Child_April_1_2020_through_December_31_2020 = 0
    else:
        Child_April_1_2020_through_December_31_2020 = int(Child_April_1_2020_through_December_31_2020)

    Email = data_variables[0]['old_intake_data'].get("Email", "")
    if Email is None:
        Email = ""

    Child_January_1_2021_through_March_31_2021 = data_variables[0]['old_intake_data'].get("Child_January_1_2021_through_March_31_2021", 0)
    if Child_January_1_2021_through_March_31_2021 == '' or Child_January_1_2021_through_March_31_2021 == '-':
        Child_January_1_2021_through_March_31_2021 = 0
    else:
        Child_January_1_2021_through_March_31_2021 = int(Child_January_1_2021_through_March_31_2021)

    Gov_April_1_2021_through_September_30_2021 = data_variables[0]['old_intake_data'].get("Gov_April_1_2021_through_September_30_2021", 0)
    if Gov_April_1_2021_through_September_30_2021 == '' or Gov_April_1_2021_through_September_30_2021 == '-':
        Gov_April_1_2021_through_September_30_2021 = 0
    else:
        Gov_April_1_2021_through_September_30_2021 = int(Gov_April_1_2021_through_September_30_2021)

    Gov_January_1_2021_through_March_31_2021 = data_variables[0]['old_intake_data'].get("Gov_January_1_2021_through_March_31_2021", 0)
    if Gov_January_1_2021_through_March_31_2021 == '' or Gov_January_1_2021_through_March_31_2021 == '-':
        Gov_January_1_2021_through_March_31_2021 = 0
    else:
        Gov_January_1_2021_through_March_31_2021 = int(Gov_January_1_2021_through_March_31_2021)

    Gov_April_1_2020_through_December_31_2020 = data_variables[0]['old_intake_data'].get("Gov_April_1_2020_through_December_31_2020", 0)
    if Gov_April_1_2020_through_December_31_2020 == '' or Gov_April_1_2020_through_December_31_2020 == '-':
        Gov_April_1_2020_through_December_31_2020 = 0
    else:
        Gov_April_1_2020_through_December_31_2020 = int(Gov_April_1_2020_through_December_31_2020)

    Family_January_1_2021_through_March_31_2021 = data_variables[0]['old_intake_data'].get("Family_January_1_2021_through_March_31_2021", 0)
    if Family_January_1_2021_through_March_31_2021 == '' or Family_January_1_2021_through_March_31_2021 == '-':
        Family_January_1_2021_through_March_31_2021 = 0
    else:
        Family_January_1_2021_through_March_31_2021 = int(Family_January_1_2021_through_March_31_2021)

    Family_April_1_2020_through_December_31_2020 = data_variables[0]['old_intake_data'].get("Family_April_1_2020_through_December_31_2020", 0)
    if Family_April_1_2020_through_December_31_2020 == '' or Family_April_1_2020_through_December_31_2020 == '-':
        Family_April_1_2020_through_December_31_2020 = 0
    else:
        Family_April_1_2020_through_December_31_2020 = int(Family_April_1_2020_through_December_31_2020)

    Child_April_1_2021_through_September_30_2021 = data_variables[0]['old_intake_data'].get("Child_April_1_2021_through_September_30_2021", 0)
    if Child_April_1_2021_through_September_30_2021 == '' or Child_April_1_2021_through_September_30_2021 == '-':
        Child_April_1_2021_through_September_30_2021 = 0
    else:
        Child_April_1_2021_through_September_30_2021 = int(Child_April_1_2021_through_September_30_2021)

    Family_April_1_2021_through_September_30_2021 = data_variables[0]['old_intake_data'].get("Family_April_1_2021_through_September_30_2021", 0)
    if Family_April_1_2021_through_September_30_2021 == '' or Family_April_1_2021_through_September_30_2021 == '-':
        Family_April_1_2021_through_September_30_2021 = 0
    else:
        Family_April_1_2021_through_September_30_2021 = int(Family_April_1_2021_through_September_30_2021)

    First_Name = data_variables[0]['old_intake_data'].get("First_Name", "")
    if First_Name is None:
        First_Name = ""

    Last_Name = data_variables[0]['old_intake_data'].get("Last_Name", "")
    if Last_Name is None:
        Last_Name = ""

    ClientId = data_variables[0]['old_intake_data'].get("ClientId", "")
    if ClientId is None:
        ClientId = ""

    Status = data_variables[0]['old_intake_data'].get("Status", "")
    if Status is None:
        Status = ""

    Zoho_21_7202_4b	= "01/04 01/05 01/06 01/07 01/08 01/09 01/10 01/11 01/12 01/13"
    # Assuming Gov_April_1_2020_through_December_31_2020 holds a numeric value

    if Gov_April_1_2020_through_December_31_2020 == 0:
        Zoho_21_7202_4b = ""
    elif Gov_April_1_2020_through_December_31_2020 == 1:
        Zoho_21_7202_4b = "01/04"
    elif Gov_April_1_2020_through_December_31_2020 == 2:
        Zoho_21_7202_4b = "01/04 01/05"
    elif Gov_April_1_2020_through_December_31_2020 == 3:
        Zoho_21_7202_4b = "01/04 01/05 01/06"
    elif Gov_April_1_2020_through_December_31_2020 == 4:
        Zoho_21_7202_4b = "01/04 01/05 01/06 01/07"
    elif Gov_April_1_2020_through_December_31_2020 == 5:
        Zoho_21_7202_4b = "01/04 01/05 01/06 01/07 01/08"
    elif Gov_April_1_2020_through_December_31_2020 == 6:
        Zoho_21_7202_4b = "01/04 01/05 01/06 01/07 01/08 01/09"
    elif Gov_April_1_2020_through_December_31_2020 == 7:
        Zoho_21_7202_4b = "01/04 01/05 01/06 01/07 01/08 01/09 01/10"
    elif Gov_April_1_2020_through_December_31_2020 == 8:
        Zoho_21_7202_4b = "01/04 01/05 01/06 01/07 01/08 01/09 01/10 01/11"
    elif Gov_April_1_2020_through_December_31_2020 == 9:
        Zoho_21_7202_4b = "01/04 01/05 01/06 01/07 01/08 01/09 01/10 01/11 01/12"
    elif Gov_April_1_2020_through_December_31_2020 == 10:
        Zoho_21_7202_4b = "01/04 01/05 01/06 01/07 01/08 01/09 01/10 01/11 01/12 01/13"
    else:
        Zoho_21_7202_4b = ""  # handle cases where Gov_April_1_2020_through_December_31_2020 is out of range

    print(Zoho_21_7202_4b)


    # this checks the variable Child_January_1_2021_through_March_31_2021 to then update Zoho_21_7202_6b
    Zoho_21_7202_6b	= "01/14 01/15 01/16 01/17 01/18 01/19 01/20 01/21 01/22 01/23"

    if Child_January_1_2021_through_March_31_2021 == 0:
        Zoho_21_7202_6b = ""
    elif Child_January_1_2021_through_March_31_2021 == 1:
        Zoho_21_7202_6b = "01/14"
    elif Child_January_1_2021_through_March_31_2021 == 2:
        Zoho_21_7202_6b = "01/14 01/15"
    elif Child_January_1_2021_through_March_31_2021 == 3:
        Zoho_21_7202_6b = "01/14 01/15 01/16"
    elif Child_January_1_2021_through_March_31_2021 == 4:
        Zoho_21_7202_6b = "01/14 01/15 01/16 01/17"
    elif Child_January_1_2021_through_March_31_2021 == 5:
        Zoho_21_7202_6b = "01/14 01/15 01/16 01/17 01/18"
    elif Child_January_1_2021_through_March_31_2021 == 6:
        Zoho_21_7202_6b = "01/14 01/15 01/16 01/17 01/18 01/19"
    elif Child_January_1_2021_through_March_31_2021 == 7:
        Zoho_21_7202_6b = "01/14 01/15 01/16 01/17 01/18 01/19 01/20"
    elif Child_January_1_2021_through_March_31_2021 == 8:
        Zoho_21_7202_6b = "01/14 01/15 01/16 01/17 01/18 01/19 01/20 01/21"
    elif Child_January_1_2021_through_March_31_2021 == 9:
        Zoho_21_7202_6b = "01/14 01/15 01/16 01/17 01/18 01/19 01/20 01/21 01/22"
    elif Child_January_1_2021_through_March_31_2021 == 10:
        Zoho_21_7202_6b = "01/14 01/15 01/16 01/17 01/18 01/19 01/20 01/21 01/22 01/23"
    else:
        Zoho_21_7202_6b = ""  # handle cases where Child_January_1_2021_through_March_31_2021 is out of range

    print(Zoho_21_7202_6b)


    Zoho_21_7202_38b =	"04/01 04/02 04/03 04/04 04/05 04/06/ 04/07 04/08 04/09 04/10"
    if Gov_April_1_2021_through_September_30_2021 == 0:
        Zoho_21_7202_5b = ""
    elif Gov_April_1_2021_through_September_30_2021 == 1:
        Zoho_21_7202_5b = "04/01"
    elif Gov_April_1_2021_through_September_30_2021 == 2:
        Zoho_21_7202_5b = "04/01 04/02"
    elif Gov_April_1_2021_through_September_30_2021 == 3:
        Zoho_21_7202_5b = "04/01 04/02 04/03"
    elif Gov_April_1_2021_through_September_30_2021 == 4:
        Zoho_21_7202_5b = "04/01 04/02 04/03 04/04"
    elif Gov_April_1_2021_through_September_30_2021 == 5:
        Zoho_21_7202_5b = "04/01 04/02 04/03 04/04 04/05"
    elif Gov_April_1_2021_through_September_30_2021 == 6:
        Zoho_21_7202_5b = "04/01 04/02 04/03 04/04 04/05 04/06"
    elif Gov_April_1_2021_through_September_30_2021 == 7:
        Zoho_21_7202_5b = "04/01 04/02 04/03 04/04 04/05 04/06 04/07"
    elif Gov_April_1_2021_through_September_30_2021 == 8:
        Zoho_21_7202_5b = "04/01 04/02 04/03 04/04 04/05 04/06 04/07 04/08"
    elif Gov_April_1_2021_through_September_30_2021 == 9:
        Zoho_21_7202_5b = "04/01 04/02 04/03 04/04 04/05 04/06 04/07 04/08 04/09"
    elif Gov_April_1_2021_through_September_30_2021 == 10:
        Zoho_21_7202_5b = "04/01 04/02 04/03 04/04 04/05 04/06 04/07 04/08 04/09 04/10"
    else:
        Zoho_21_7202_5b = ""  # handle cases where Gov_April_1_2021_through_September_30_2021 is out of range

    print(Zoho_21_7202_5b)

    Zoho_21_7202_40b =	"04/11 04/12 04/13 04/14 04/15 04/16/ 04/17 04/18 04/19 04/20"
    # Assuming Child_April_1_2021_through_September_30_2021 holds a numeric value
    Child_April_1_2021_through_September_30_2021 = 4  # Example value

    if Child_April_1_2021_through_September_30_2021 == 0:
        Zoho_21_7202_6b = ""
    elif Child_April_1_2021_through_September_30_2021 == 1:
        Zoho_21_7202_6b = "04/11"
    elif Child_April_1_2021_through_September_30_2021 == 2:
        Zoho_21_7202_6b = "04/11 04/12"
    elif Child_April_1_2021_through_September_30_2021 == 3:
        Zoho_21_7202_6b = "04/11 04/12 04/13"
    elif Child_April_1_2021_through_September_30_2021 == 4:
        Zoho_21_7202_6b = "04/11 04/12 04/13 04/14"
    elif Child_April_1_2021_through_September_30_2021 == 5:
        Zoho_21_7202_6b = "04/11 04/12 04/13 04/14 04/15"
    elif Child_April_1_2021_through_September_30_2021 == 6:
        Zoho_21_7202_6b = "04/11 04/12 04/13 04/14 04/15 04/16"
    elif Child_April_1_2021_through_September_30_2021 == 7:
        Zoho_21_7202_6b = "04/11 04/12 04/13 04/14 04/15 04/16 04/17"
    elif Child_April_1_2021_through_September_30_2021 == 8:
        Zoho_21_7202_6b = "04/11 04/12 04/13 04/14 04/15 04/16 04/17 04/18"
    elif Child_April_1_2021_through_September_30_2021 == 9:
        Zoho_21_7202_6b = "04/11 04/12 04/13 04/14 04/15 04/16 04/17 04/18 04/19"
    elif Child_April_1_2021_through_September_30_2021 == 10:
        Zoho_21_7202_6b = "04/11 04/12 04/13 04/14 04/15 04/16 04/17 04/18 04/19 04/20"
    else:
        Zoho_21_7202_6b = ""  # handle cases where Child_April_1_2021_through_September_30_2021 is out of range

    print(Zoho_21_7202_6b)



    #Data from Xano
    # ClientId = data_variables[0]['new_intake_data']['ClientId']
    # if ClientId is None:
    #     ClientId = ""

    # Status = 0
    # if Status is None:
    #     Status = ""

    # Dates = 0
    # if Dates is None:
    #     Dates = ""

    # S1_Q1_Selfemployed = 0
    # if S1_Q1_Selfemployed is None:
    #     S1_Q1_Selfemployed = 0

    # S1_Q2_Filed1040_tax = 0
    # if S1_Q2_Filed1040_tax is None:
    #     S1_Q2_Filed1040_tax = 0

    # S1_Q3_Affected = 0
    # if S1_Q3_Affected is None:
    #     S1_Q3_Affected = 0

    # First_Name = 0
    # if First_Name is None:
    #     First_Name = ""

    # Last_Name = 0
    # if Last_Name is None:
    #     Last_Name = ""

    # Email = 0
    # if Email is None:
    #     Email = ""

    # Phone = 0
    # if Phone is None:
    #     Phone = ""

    # S2_Q1 = 0
    # if S2_Q1 is None:
    #     S2_Q1 = 0

    # S2_Q2 = 0
    # if S2_Q2 is None:
    #     S2_Q2 = 0

    # S2_Q3 = 0
    # if S2_Q3 is None:
    #     S2_Q3 = 0

    # S3_Q1 = 0
    # if S3_Q1 is None:
    #     S3_Q1 = 0

    # S3_Q1_D1 = 0
    # if S3_Q1_D1 is None:
    #     S3_Q1_D1 = 0

    # S3_Q1_D3 = 0
    # if S3_Q1_D3 is None:
    #     S3_Q1_D3 = 0

    # S3_Q1_D4 = 0
    # if S3_Q1_D4 is None:
    #     S3_Q1_D4 = 0

    # S3_Q1_D5 = 0
    # if S3_Q1_D5 is None:
    #     S3_Q1_D5 = 0

    # S3_Q1_D6 = 0
    # if S3_Q1_D6 is None:
    #     S3_Q1_D6 = 0

    # S3_Q1_D7 = 0
    # if S3_Q1_D7 is None:
    #     S3_Q1_D7 = 0

    # S3_Q1_D8 = 0
    # if S3_Q1_D8 is None:
    #     S3_Q1_D8 = 0

    # S3_Q1_D9 = 0
    # if S3_Q1_D9 is None:
    #     S3_Q1_D9 = 0

    # S3_Q1_D10 = 0
    # if S3_Q1_D10 is None:
    #     S3_Q1_D10 = 0

    # S3_Q2 = 0
    # if S3_Q2 is None:
    #     S3_Q2 = 0

    # S3_Q2_D1 = 0
    # if S3_Q2_D1 is None:
    #     S3_Q2_D1 = 0

    # S3_Q2_D2 = 0
    # if S3_Q2_D2 is None:
    #     S3_Q2_D2 = 0

    # S3_Q2_D3 = 0
    # if S3_Q2_D3 is None:
    #     S3_Q2_D3 = 0

    # S3_Q2_D4 = 0
    # if S3_Q2_D4 is None:
    #     S3_Q2_D4 = 0

    # S3_Q2_D5 = 0
    # if S3_Q2_D5 is None:
    #     S3_Q2_D5 = 0

    # S3_Q2_D6 = 0
    # if S3_Q2_D6 is None:
    #     S3_Q2_D6 = 0

    # S3_Q2_D7 = 0
    # if S3_Q2_D7 is None:
    #     S3_Q2_D7 = 0

    # S3_Q2_D8 = 0
    # if S3_Q2_D8 is None:
    #     S3_Q2_D8 = 0

    # S3_Q2_D9 = 0
    # if S3_Q2_D9 is None:
    #     S3_Q2_D9 = 0

    # S3_Q2_D10 = 0
    # if S3_Q2_D10 is None:
    #     S3_Q2_D10 = 0

    # S4_Q1 = 0
    # if S4_Q1 is None:
    #     S4_Q1 = 0

    # S4_Q2 = 0
    # if S4_Q2 is None:
    #     S4_Q2 = 0

    # S4_Q2_D1 = 0
    # if S4_Q2_D1 is None:
    #     S4_Q2_D1 = 0

    # S4_Q2_D2 = 0
    # if S4_Q2_D2 is None:
    #     S4_Q2_D2 = 0

    # S4_Q2_D3 = 0
    # if S4_Q2_D3 is None:
    #     S4_Q2_D3 = 0

    # S4_Q2_D4 = 0
    # if S4_Q2_D4 is None:
    #     S4_Q2_D4 = 0

    # S4_Q2_D5 = 0
    # if S4_Q2_D5 is None:
    #     S4_Q2_D5 = 0

    # S4_Q2_D6 = 0
    # if S4_Q2_D6 is None:
    #     S4_Q2_D6 = 0

    # S4_Q2_D7 = 0
    # if S4_Q2_D7 is None:
    #     S4_Q2_D7 = 0

    # S4_Q2_D8 = 0
    # if S4_Q2_D8 is None:
    #     S4_Q2_D8 = 0

    # S4_Q2_D9 = 0
    # if S4_Q2_D9 is None:
    #     S4_Q2_D9 = 0

    # S4_Q2_D10 = 0
    # if S4_Q2_D10 is None:
    #     S4_Q2_D10 = 0

    # S4_Q3 = 0
    # if S4_Q3 is None:
    #     S4_Q3 = 0

    # S4_Q3_D1 = 0
    # if S4_Q3_D1 is None:
    #     S4_Q3_D1 = 0

    # S4_Q3_D2 = 0
    # if S4_Q3_D2 is None:
    #     S4_Q3_D2 = 0

    # S4_Q3_D3 = 0
    # if S4_Q3_D3 is None:
    #     S4_Q3_D3 = 0

    # S4_Q3_D4 = 0
    # if S4_Q3_D4 is None:
    #     S4_Q3_D4 = 0

    # S4_Q3_D5 = 0
    # if S4_Q3_D5 is None:
    #     S4_Q3_D5 = 0

    # S4_Q3_D6 = 0
    # if S4_Q3_D6 is None:
    #     S4_Q3_D6 = 0

    # S4_Q3_D7 = 0
    # if S4_Q3_D7 is None:
    #     S4_Q3_D7 = 0

    # S4_Q3_D8 = 0
    # if S4_Q3_D8 is None:
    #     S4_Q3_D8 = 0

    # S4_Q3_D9 = 0
    # if S4_Q3_D9 is None:
    #     S4_Q3_D9 = 0

    # S4_Q3_D10 = 0
    # if S4_Q3_D10 is None:
    #     S4_Q3_D10 = 0

    # S5_Q1 = 0
    # if S5_Q1 is None:
    #     S5_Q1 = 0

    # S3_Q1_D2 = 0
    # if S3_Q1_D2 is None:
    #     S3_Q1_D2 = 0

    # # Concatenate the date values stored in S3_Q1_D1, S3_Q1_D2, ..., S3_Q1_D10
    # New_Intake_Dates_21_7202_4b = str(S3_Q1_D1) + " " + str(S3_Q1_D2) + " " + str(S3_Q1_D3) + " " + str(S3_Q1_D4) + " " + str(S3_Q1_D5) + " " + str(S3_Q1_D6) + " " + str(S3_Q1_D7) + " " + str(S3_Q1_D8) + " " + str(S3_Q1_D9) + " " + str(S3_Q1_D1)

    # # Check if New_Intake_Dates_21_7202_4b is an empty string
    # if not New_Intake_Dates_21_7202_4b:
    #     print("New_Intake_Dates_21_7202_4b is empty")
    # else:
    #     print("New_Intake_Dates_21_7202_4b is not empty")

    # # Concatenate the date values stored in S3_Q2_D1, S3_Q2_D2, ..., S3_Q2_D10
    # New_Intake_Dates_21_7202_6b = str(S3_Q2_D1) + " " + str(S3_Q2_D2) + " " + str(S3_Q2_D3) + " " + str(S3_Q2_D4) + " " + str(S3_Q2_D5) + " " + str(S3_Q2_D6) + " " + str(S3_Q2_D7) + " " + str(S3_Q2_D8) + " " + str(S3_Q2_D9) + " " + str(S3_Q2_D1)

    # # Check if New_Intake_Dates_21_7202_6b is None
    # if New_Intake_Dates_21_7202_6b is None:
    #     New_Intake_Dates_21_7202_6b = 0

    # # print(New_Intake_Dates_21_7202_6b)
        
    # # Concatenate the date values stored in S4_Q2_D1, S4_Q2_D2, ..., S4_Q2_D10
    # New_Intake_Dates_21_7202_38b = str(S4_Q2_D1) + " " + str(S4_Q2_D2) + " " + str(S4_Q2_D3) + " " + str(S4_Q2_D4) + " " + str(S4_Q2_D5) + " " + str(S4_Q2_D6) + " " + str(S4_Q2_D7) + " " + str(S4_Q2_D8) + " " + str(S4_Q2_D9) + " " + str(S4_Q2_D1)

    # # Check if New_Intake_Dates_21_7202_38b is None
    # if New_Intake_Dates_21_7202_38b is None:
    #     New_Intake_Dates_21_7202_38b = 0

    # # print(New_Intake_Dates_21_7202_38b)
        
    # # Concatenate the date values stored in S4_Q3_D1, S4_Q3_D2, ..., S4_Q3_D10
    # New_Intake_Dates_21_7202_40b = str(S4_Q3_D1) + " " + str(S4_Q3_D2) + " " + str(S4_Q3_D3) + " " + str(S4_Q3_D4) + " " + str(S4_Q3_D5) + " " + str(S4_Q3_D6) + " " + str(S4_Q3_D7) + " " + str(S4_Q3_D8) + " " + str(S4_Q3_D9) + " " + str(S4_Q3_D1)

    # # Check if New_Intake_Dates_21_7202_40b is None
    # if New_Intake_Dates_21_7202_40b is None:
    #     New_Intake_Dates_21_7202_40b = 0


    instructions_data = {
        'nineteen_ADJUSTED_GROSS_INCOME': nineteen_ADJUSTED_GROSS_INCOME,
        'nineteen_FILING_STATUS': nineteen_FILING_STATUS,
        'nineteen_credit_to_your_account': nineteen_credit_to_your_account,
        'nineteen_account_balance': nineteen_account_balance,
        'nineteen_accrued_interest': nineteen_accrued_interest,
        'nineteen_taxable_income': nineteen_taxable_income,
        'nineteen_tax_per_return': nineteen_tax_per_return,
        'twenty_qualified_business_income_deduction_computer': twenty_qualified_business_income_deduction_computer,
        'twenty_self_employment_tax_deduction_per_computer': twenty_self_employment_tax_deduction_per_computer,
        'twenty_adjusted_gross_income': twenty_adjusted_gross_income,
        'twenty_adjusted_gross_income_per_computer': twenty_adjusted_gross_income_per_computer,
        'twenty_standard_deduction_per_computer': twenty_standard_deduction_per_computer,
        'twenty_tentative_tax': twenty_tentative_tax,
        'twenty_total_credits': twenty_total_credits,
        'twenty_SE_tax': twenty_SE_tax,
        'twenty_federal_income_tax_withheld': twenty_federal_income_tax_withheld,
        'twenty_estimated_tax_payments': twenty_estimated_tax_payments,
        'twenty_other_payment_credit': twenty_other_payment_credit,
        'twenty_earned_income_credit': twenty_earned_income_credit,
        'twenty_total_payments': twenty_total_payments,
        'twenty_balance_due_overpayment_using_TP_figure_per_computer': twenty_balance_due_overpayment_using_TP_figure_per_computer,
        'twenty_total_qualified_business_income_or_loss': twenty_total_qualified_business_income_or_loss,
        'twenty_filing_status': twenty_filing_status,
        'twenty_SE_income_per_computer': twenty_SE_income_per_computer,
        'twenty_credit_to_your_account': twenty_credit_to_your_account,
        'twenty_account_balance': twenty_account_balance,
        'twenty_accrued_interest': twenty_accrued_interest,
        'twenty_taxable_income': twenty_taxable_income,
        'twenty_tax_per_return': twenty_tax_per_return,
        'twenty_schedule_8812_additional_child_tax_credit': twenty_schedule_8812_additional_child_tax_credit,
        'twenty_form_2439_regulated_investment_company_credit': twenty_form_2439_regulated_investment_company_credit,
        'twenty_form_4136_credit_for_federal_tax_on_fuels_per_computer': twenty_form_4136_credit_for_federal_tax_on_fuels_per_computer,
        'twenty_total_education_credit_amount_per_computer': twenty_total_education_credit_amount_per_computer,
        'twenty_health_coverage_TX_credit_F8885': twenty_health_coverage_TX_credit_F8885,
        'twenty_amount_you_owe': twenty_amount_you_owe,
        'twenty_refund_amount': twenty_refund_amount,
        'twenty_sick_family_leave_credit_after_3_31_21': twenty_sick_family_leave_credit_after_3_31_21,
        'twenty_wages_salaries_tips_etc': twenty_wages_salaries_tips_etc,
        'twenty_tax_exempt_interest': twenty_tax_exempt_interest,
        'twenty_qualified_dividends': twenty_qualified_dividends,
        'twenty_total_IRA_distributions': twenty_total_IRA_distributions,
        'twenty_total_pensions_and_annuities': twenty_total_pensions_and_annuities,
        'twenty_total_social_security_benefits': twenty_total_social_security_benefits,
        'twenty_taxable_interest_income': twenty_taxable_interest_income,
        'twenty_ordinary_dividend_income': twenty_ordinary_dividend_income,
        'twenty_taxable_IRA_distributions': twenty_taxable_IRA_distributions,
        'twenty_taxable_pension_annuity_amount': twenty_taxable_pension_annuity_amount,
        'twenty_taxable_social_security_benefits_per_computer': twenty_taxable_social_security_benefits_per_computer,
        'twenty_capital_gain_or_loss': twenty_capital_gain_or_loss,
        'twenty_other_income': twenty_other_income,
        'twenty_total_adjustments_per_computer': twenty_total_adjustments_per_computer,
        'twenty_non_itemized_charitable_contribution_per_computer': twenty_non_itemized_charitable_contribution_per_computer,
        'twenty_business_income_or_loss_schedule_C': twenty_business_income_or_loss_schedule_C,
        'twenty_child_and_other_dependent_credit_per_computer': twenty_child_and_other_dependent_credit_per_computer,
        'twenty_excess_advance_premium_tax_credit_repayment_amount': twenty_excess_advance_premium_tax_credit_repayment_amount,
        'twenty_sec_965_tax_installment': twenty_sec_965_tax_installment,
        'twenty_child_dependent_care_credit': twenty_child_dependent_care_credit,
        'twenty_estimated_tax_penalty': twenty_estimated_tax_penalty,
        'twenty_applied_to_next_years_estimated_tax': twenty_applied_to_next_years_estimated_tax,
        'twenty_earned_income_credit_nontaxable_combat_pay': twenty_earned_income_credit_nontaxable_combat_pay,
        'twenty_max_deferred_tax_per_computer': twenty_max_deferred_tax_per_computer,
        'twenty_EIC_prior_year_earned_income': twenty_EIC_prior_year_earned_income,   
        'twenty_twenty_one_qualified_business_income_deduction_computer': twenty_twenty_one_qualified_business_income_deduction_computer,
        'twenty_twenty_one_self_employment_tax_deduction_per_computer': twenty_twenty_one_self_employment_tax_deduction_per_computer,
        'twenty_twenty_one_adjusted_gross_income': twenty_twenty_one_adjusted_gross_income,
        'twenty_twenty_one_adjusted_gross_income_per_computer': twenty_twenty_one_adjusted_gross_income_per_computer,
        'twenty_twenty_one_standard_deduction_per_computer': twenty_twenty_one_standard_deduction_per_computer,
        'twenty_twenty_one_tentative_tax': twenty_twenty_one_tentative_tax,
        'twenty_twenty_one_total_credits': twenty_twenty_one_total_credits,
        'twenty_twenty_one_SE_tax': twenty_twenty_one_SE_tax,
        'twenty_twenty_one_federal_income_tax_withheld': twenty_twenty_one_federal_income_tax_withheld,
        'twenty_twenty_one_estimated_tax_payments': twenty_twenty_one_estimated_tax_payments,
        'twenty_twenty_one_other_payment_credit': twenty_twenty_one_other_payment_credit,
        'twenty_twenty_one_earned_income_credit': twenty_twenty_one_earned_income_credit,
        'twenty_twenty_one_total_payments': twenty_twenty_one_total_payments,
        'twenty_twenty_one_balance_due_overpayment_using_TP_figure_per_computer': twenty_twenty_one_balance_due_overpayment_using_TP_figure_per_computer,
        'twenty_twenty_one_total_qualified_business_income_or_loss': twenty_twenty_one_total_qualified_business_income_or_loss,
        'twenty_twenty_one_filing_status': twenty_twenty_one_filing_status,
        'twenty_twenty_one_SE_income_per_computer': twenty_twenty_one_SE_income_per_computer,
        'twenty_twenty_one_credit_to_your_account': twenty_twenty_one_credit_to_your_account,
        'twenty_twenty_one_account_balance': twenty_twenty_one_account_balance,
        'twenty_twenty_one_accrued_interest': twenty_twenty_one_accrued_interest,
        'twenty_twenty_one_taxable_income': twenty_twenty_one_taxable_income,
        'twenty_twenty_one_tax_per_return': twenty_twenty_one_tax_per_return,
        'twenty_twenty_one_schedule_8812_additional_child_tax_credit': twenty_twenty_one_schedule_8812_additional_child_tax_credit,
        'twenty_twenty_one_form_2439_regulated_investment_company_credit': twenty_twenty_one_form_2439_regulated_investment_company_credit,
        'twenty_twenty_one_form_4136_credit_for_federal_tax_on_fuels_per_computer': twenty_twenty_one_form_4136_credit_for_federal_tax_on_fuels_per_computer,
        'twenty_twenty_one_total_education_credit_amount_per_computer': twenty_twenty_one_total_education_credit_amount_per_computer,
        'twenty_twenty_one_health_coverage_TX_credit_F8885': twenty_twenty_one_health_coverage_TX_credit_F8885,
        'twenty_twenty_one_amount_you_owe': twenty_twenty_one_amount_you_owe,
        'twenty_twenty_one_refund_amount': twenty_twenty_one_refund_amount,
        'twenty_twenty_one_wages_salaries_tips_etc': twenty_twenty_one_wages_salaries_tips_etc,
        'twenty_twenty_one_tax_exempt_interest': twenty_twenty_one_tax_exempt_interest,
        'twenty_twenty_one_qualified_dividends': twenty_twenty_one_qualified_dividends,
        'twenty_twenty_one_total_IRA_distributions': twenty_twenty_one_total_IRA_distributions,
        'twenty_twenty_one_total_pensions_and_annuities': twenty_twenty_one_total_pensions_and_annuities,
        'twenty_twenty_one_total_social_security_benefits': twenty_twenty_one_total_social_security_benefits,
        'twenty_twenty_one_taxable_interest_income': twenty_twenty_one_taxable_interest_income,
        'twenty_twenty_one_ordinary_dividend_income': twenty_twenty_one_ordinary_dividend_income,
        'twenty_twenty_one_taxable_IRA_distributions': twenty_twenty_one_taxable_IRA_distributions,
        'twenty_twenty_one_taxable_pension_annuity_amount': twenty_twenty_one_taxable_pension_annuity_amount,
        'twenty_twenty_one_taxable_social_security_benefits_per_computer': twenty_twenty_one_taxable_social_security_benefits_per_computer,
        'twenty_twenty_one_capital_gain_or_loss': twenty_twenty_one_capital_gain_or_loss,
        'twenty_twenty_one_other_income': twenty_twenty_one_other_income,
        'twenty_twenty_one_total_adjustments_per_computer': twenty_twenty_one_total_adjustments_per_computer,
        'twenty_twenty_one_non_itemized_charitable_contribution_per_computer': twenty_twenty_one_non_itemized_charitable_contribution_per_computer,
        'twenty_twenty_one_business_income_or_loss_schedule_C': twenty_twenty_one_business_income_or_loss_schedule_C,
        'twenty_twenty_one_child_and_other_dependent_credit_per_computer': twenty_twenty_one_child_and_other_dependent_credit_per_computer,
        'twenty_twenty_one_excess_advance_premium_tax_credit_repayment_amount': twenty_twenty_one_excess_advance_premium_tax_credit_repayment_amount,
        'twenty_twenty_one_sec_965_tax_installment': twenty_twenty_one_sec_965_tax_installment,
        'twenty_twenty_one_child_dependent_care_credit': twenty_twenty_one_child_dependent_care_credit,
        'twenty_twenty_one_estimated_tax_penalty': twenty_twenty_one_estimated_tax_penalty,
        'twenty_twenty_one_applied_to_next_years_estimated_tax': twenty_twenty_one_applied_to_next_years_estimated_tax,
        'twenty_twenty_one_earned_income_credit_nontaxable_combat_pay': twenty_twenty_one_earned_income_credit_nontaxable_combat_pay,
        'twenty_twenty_one_max_deferred_tax_per_computer': twenty_twenty_one_max_deferred_tax_per_computer,
        'twenty_twenty_one_EIC_prior_year_earned_income': twenty_twenty_one_EIC_prior_year_earned_income,       
        'Child_April_1_2020_through_December_31_2020': Child_April_1_2020_through_December_31_2020,
        'Email': Email,
        'Child_January_1_2021_through_March_31_2021': Child_January_1_2021_through_March_31_2021,
        'Gov_April_1_2021_through_September_30_2021': Gov_April_1_2021_through_September_30_2021,
        'Gov_January_1_2021_through_March_31_2021': Gov_January_1_2021_through_March_31_2021,
        'Gov_April_1_2020_through_December_31_2020': Gov_April_1_2020_through_December_31_2020,
        'Family_January_1_2021_through_March_31_2021': Family_January_1_2021_through_March_31_2021,
        'Family_April_1_2020_through_December_31_2020': Family_April_1_2020_through_December_31_2020,
        'Child_April_1_2021_through_September_30_2021': Child_April_1_2021_through_September_30_2021,
        'Family_April_1_2021_through_September_30_2021': Family_April_1_2021_through_September_30_2021,
        'First_Name': First_Name,
        'Last_Name': Last_Name,
        'ClientId': ClientId,
        'Status': Status
        }


    return instructions_data
    # print(New_Intake_Dates_21_7202_40b)


