import math
import argparse


def nominal_interest_rate_calc(loan_interest):
    return loan_interest / (12 * 100)


def annuity_payment_calc(loan_principal_, loan_interest, period):
    nominal_interest = nominal_interest_rate_calc(loan_interest)
    return loan_principal_ * (nominal_interest * (math.pow(1 + nominal_interest, period))) / (
                math.pow(1 + nominal_interest, period) - 1)


def period_calc(annuity_payment_, loan_interest, loan_principal_):
    nominal_interest = nominal_interest_rate_calc(loan_interest)
    return math.log(annuity_payment_ / (annuity_payment_ - nominal_interest * loan_principal_), 1 + nominal_interest)


def loan_principal_calc(annuity_payment_, loan_interest, period):
    nominal_interest = nominal_interest_rate_calc(loan_interest)
    return annuity_payment_ / ((nominal_interest * (math.pow(1 + nominal_interest, period))) / (
                math.pow(1 + nominal_interest, period) - 1))


def differentiated_payment_calc(loan_principal_, period, loan_interest, month):
    nominal_interest = nominal_interest_rate_calc(loan_interest)
    return (loan_principal_ / period) + nominal_interest * (loan_principal_ - (
            (loan_principal_ * (month - 1)) / period))


parser = argparse.ArgumentParser(description="Loan Calculator")
parser.add_argument("--type", choices=["diff", "annuity"], type=str)
parser.add_argument("--payment", type=float)
parser.add_argument("--principal", type=float)
parser.add_argument("--periods", type=float)
parser.add_argument("--interest", type=float)
args = parser.parse_args()
argument = [args.principal, args.interest, args.periods, args.payment]
type_choice = args.type

if type_choice == "annuity":
    if argument[3] is None:
        if argument[0] is None or argument[1] is None or argument[2] is None:
            print("Incorrect parameters")
        else:
            annuity_payment = math.ceil(annuity_payment_calc(argument[0], argument[1], argument[2]))
            overpayment = math.ceil(annuity_payment * argument[2] - argument[0])
            print(f"Your annuity payment = {annuity_payment}!")
            print(f"Overpayment = {overpayment}")
    elif argument[2] is None:
        if argument[0] is None or argument[1] is None or argument[3] is None:
            print("Incorrect parameters")
        else:
            month_count = math.ceil(period_calc(argument[3], argument[1], argument[0]))
            overpayment = math.ceil(month_count * argument[3] - argument[0])
            if month_count < 12:
                month_count = math.ceil(month_count / 12)
                print(f"It will take {month_count} months to repay this loan!")
            elif month_count % 12 == 0:
                month_count = math.ceil(month_count / 12)
                print(f"It will take {month_count} years to repay this loan!")
            elif month_count % 12 != 0:
                month_count = math.ceil(month_count % 12)
                year_count = math.ceil(month_count / 12)
                print(f"It will take {year_count} years {month_count} months to repay this loan!")
            print(f"Overpayment = {overpayment}")
    elif argument[0] is None:
        if argument[1] is None or argument[2] is None or argument[3] is None:
            print("Incorrect parameters")
        else:
            loan_principal = math.floor(loan_principal_calc(argument[3], argument[1], argument[2]))
            overpayment = math.ceil(argument[2] * argument[3] - loan_principal)
            print(f"Your loan principal = {loan_principal}!")
            print(f"Overpayment = {overpayment}")
if type_choice == "diff":
    if argument[0] is None or argument[1] is None or argument[2] is None:
        print("Incorrect parameters")
    else:
        differentiated_payment_sum = 0
        for months in range(1, int(argument[2]) + 1):
            differentiated_payment = math.ceil(differentiated_payment_calc(
                argument[0], argument[2], argument[1], months))
            print(f"Month {months}: payment is {differentiated_payment}")
            differentiated_payment_sum += differentiated_payment
        overpayment = math.ceil(differentiated_payment_sum - argument[0])
        print(f"Overpayment = {overpayment}")
