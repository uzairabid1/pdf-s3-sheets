from instructions import get_instructions_data

import requests
import boto3
import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import pandas as pd
import time

import math

load_dotenv()

s3_access_key = os.getenv('s3_access_key')
s3_secret_key = os.getenv('s3_secret_key')
s3_bucket_name = os.getenv('s3_bucket_name')
s3_bucket_region = os.getenv('s3_bucket_region')

taxStatus_token_url = os.getenv('taxStatus_token_url')
taxStatus_client_id = os.getenv('taxStatus_client_id')
taxStatus_client_secret = os.getenv('taxStatus_client_secret')
taxStatus_scope = os.getenv('taxStatus_scope')
taxStatus_euid = os.getenv('taxStatus_euid')

gsheet_scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
gsheet_creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", gsheet_scope)
gsheet_client = gspread.authorize(gsheet_creds)

def upload_pdf_to_s3(pdf_url,pdf_file_name):

    pdf_content = requests.get(pdf_url).content        
    s3_client = boto3.client('s3', aws_access_key_id=s3_access_key, aws_secret_access_key=s3_secret_key)
    s3_key = pdf_file_name
    s3_client.put_object(Body=pdf_content, Bucket= s3_bucket_name, Key=s3_key, ContentType='application/pdf')
        

    s3_url = f'https://setcpro-automate-boring.s3.us-east-2.amazonaws.com/{s3_key}'    
    return s3_url



def upload_pdf_to_s3_2(pdf_content, pdf_file_name):
    s3_client = boto3.client('s3', aws_access_key_id=s3_access_key, aws_secret_access_key=s3_secret_key)
    s3_key = pdf_file_name
    s3_client.put_object(Body=pdf_content, Bucket=s3_bucket_name, Key=s3_key, ContentType='application/pdf')

    s3_url = f'https://setcpro-automate-boring.s3.us-east-2.amazonaws.com/{s3_key}'
    return s3_url

def extract_data_keys_and_values(data):
    extracted_data = []

    for item in data.get('items', []):        
        #old data processing
        sheet = gsheet_client.open('TS-MASTER-1-JS-1').get_worksheet(0)
        try:
            data_7202_21_4b = sheet.cell(51,23).value
        except:
            data_7202_21_4b = ''
        try:
            data_7202_21_6b = sheet.cell(52,23).value
        except:
            data_7202_21_6b = ''
        try:
            data_7202_21_38 = sheet.cell(53,23).value
        except:
            data_7202_21_38 = ''
        try:
            data_7202_21_40 = sheet.cell(54,23).value
        except:
            data_7202_21_40 = ''

        old_dates = {
            "data_7202_21_4b": data_7202_21_4b,
            "data_7202_21_6b": data_7202_21_6b,
            "data_7202_21_38": data_7202_21_38,
            "data_7202_21_40": data_7202_21_40,      
        }

        
        first_name = item.get('First_Name')
        last_name= item.get('Last_Name')
        email = item.get('Email')
        print(email)
        try:
            old_data_response = requests.get(f"https://ltt.aip.global.bizopsaip.com/flow/api/flow-rest-selfauth/getTaxCaculation?Email={email}")
            tax_data = old_data_response.json()
            tax_data = tax_data['taxCaculationReturn']
            intake_date = json.loads(tax_data['calculateInput']['longText'])
            
            Child_April_1_2020_through_December_31_2020 = intake_date.get('zohoReturn','').get('Child_April_1_2020_through_December_31_2020','')
            Child_January_1_2021_through_March_31_2021 = intake_date.get('zohoReturn','').get('Child_January_1_2021_through_March_31_2021','')
            Gov_April_1_2021_through_September_30_2021 = intake_date.get('zohoReturn','').get('Gov_April_1_2021_through_September_30_2021','')
            Gov_January_1_2021_through_March_31_2021 = intake_date.get('zohoReturn','').get('Gov_January_1_2021_through_March_31_2021','')
            Gov_April_1_2020_through_December_31_2020 = intake_date.get('zohoReturn','').get('Gov_April_1_2020_through_December_31_2020','')
            Family_January_1_2021_through_March_31_2021 = intake_date.get('zohoReturn','').get('Family_January_1_2021_through_March_31_2021','')
            Family_April_1_2020_through_December_31_2020 = intake_date.get('zohoReturn','').get('Family_April_1_2020_through_December_31_2020','')
            Child_April_1_2021_through_September_30_2021 = intake_date.get('zohoReturn','').get('Child_April_1_2021_through_September_30_2021','')
            Family_April_1_2021_through_September_30_2021 = intake_date.get('zohoReturn','').get('Family_April_1_2021_through_September_30_2021','')
            clientId = intake_date.get('zohoReturn','').get('ClientId','')
            status = intake_date.get('zohoReturn','').get('Status','')

            old_intake_data = {
                "Child_April_1_2020_through_December_31_2020": Child_April_1_2020_through_December_31_2020,
                "Email": email,
                "Child_January_1_2021_through_March_31_2021": Child_January_1_2021_through_March_31_2021,
                "Gov_April_1_2021_through_September_30_2021": Gov_April_1_2021_through_September_30_2021,
                "Gov_January_1_2021_through_March_31_2021": Gov_January_1_2021_through_March_31_2021,
                "Gov_April_1_2020_through_December_31_2020": Gov_April_1_2020_through_December_31_2020,
                "Family_January_1_2021_through_March_31_2021": Family_January_1_2021_through_March_31_2021,
                "Family_April_1_2020_through_December_31_2020": Family_April_1_2020_through_December_31_2020,
                "Child_April_1_2021_through_September_30_2021": Child_April_1_2021_through_September_30_2021,
                "Family_April_1_2021_through_September_30_2021": Family_April_1_2021_through_September_30_2021,
                "First_Name": first_name,
                "Last_Name": last_name,
                "ClientId": clientId,
                "Status": status
            }

        except Exception as e:
            print(f"Error processing data for email {email}: {e}")

            try:
                df = pd.read_csv("Deals_2024_03_18-1.csv")
                print(df)
                row = df[df['Email'] == email].iloc[0]
          
                Child_April_1_2020_through_December_31_2020 = row.get('(Child) April 1, 2020, through December, 31, 2020', '')
                
                if isinstance(Child_April_1_2020_through_December_31_2020, float) and math.isnan(Child_April_1_2020_through_December_31_2020):
                    old_intake_data = {
                        "Child_April_1_2020_through_December_31_2020": "",
                        "Email": email,
                        "Child_January_1_2021_through_March_31_2021": "",
                        "Gov_April_1_2021_through_September_30_2021": "",
                        "Gov_January_1_2021_through_March_31_2021": "",
                        "Gov_April_1_2020_through_December_31_2020": "",
                        "Family_January_1_2021_through_March_31_2021": "",
                        "Family_April_1_2020_through_December_31_2020": "",
                        "Child_April_1_2021_through_September_30_2021": "",
                        "Family_April_1_2021_through_September_30_2021": "",
                        "First_Name": first_name,
                        "Last_Name": last_name,
                        "ClientId": "",
                        "Status": status
                    }   

                else:              
                    Child_April_1_2021_through_September_30_2021 = row.get('(Child) April 1, 2021, through September 30, 2021', '')
                    Child_January_1_2021_through_March_31_2021 = row.get('(Child) January 1, 2021, through March 31, 2021', '')
                    Family_April_1_2020_through_December_31_2020 = row.get('(Family) April 1, 2020, through December, 31, 2020', '')
                    Family_April_1_2021_through_September_30_2021 = row.get('(Family) April 1, 2021, through September 30, 2021', '')
                    Family_January_1_2021_through_March_31_2021 = row.get('(Family) January 1, 2021, through March 31, 2021', '')
                    Gov_April_1_2020_through_December_31_2020 = row.get('(Gov) April 1, 2020, through December, 31, 2020', '')
                    Gov_April_1_2021_through_September_30_2021 = row.get('(Gov) April 1, 2021, through September 30, 2021', '')
                    Gov_January_1_2021_through_March_31_2021 = row.get('(Gov) January 1, 2021, through March 31, 2021', '')
                    clientId = row.get('ClientId', '')
                    status = row.get('Stage', '')

                    old_intake_data = {
                        "Child_April_1_2020_through_December_31_2020": Child_April_1_2020_through_December_31_2020,
                        "Email": email,
                        "Child_January_1_2021_through_March_31_2021": Child_January_1_2021_through_March_31_2021,
                        "Gov_April_1_2021_through_September_30_2021": Gov_April_1_2021_through_September_30_2021,
                        "Gov_January_1_2021_through_March_31_2021": Gov_January_1_2021_through_March_31_2021,
                        "Gov_April_1_2020_through_December_31_2020": Gov_April_1_2020_through_December_31_2020,
                        "Family_January_1_2021_through_March_31_2021": Family_January_1_2021_through_March_31_2021,
                        "Family_April_1_2020_through_December_31_2020": Family_April_1_2020_through_December_31_2020,
                        "Child_April_1_2021_through_September_30_2021": Child_April_1_2021_through_September_30_2021,
                        "Family_April_1_2021_through_September_30_2021": Family_April_1_2021_through_September_30_2021,
                        "First_Name": first_name,
                        "Last_Name": last_name,
                        "ClientId": clientId,
                        "Status": status
                    }

            except Exception as e:
                print(f"Error reading CSV data for email {email}: {e}")
                df = pd.read_csv("Deals_2024_03_18-1.csv")
                row = df[df['Email'] == email].iloc[0]
                status = row.get('Stage', '')

                old_intake_data = {              
                    "Child_April_1_2020_through_December_31_2020": "",
                    "Email": email,
                    "Child_January_1_2021_through_March_31_2021": "",
                    "Gov_April_1_2021_through_September_30_2021": "",
                    "Gov_January_1_2021_through_March_31_2021": "",
                    "Gov_April_1_2020_through_December_31_2020": "",
                    "Family_January_1_2021_through_March_31_2021": "",
                    "Family_April_1_2020_through_December_31_2020": "",
                    "Child_April_1_2021_through_September_30_2021": "",
                    "Family_April_1_2021_through_September_30_2021": "",
                    "First_Name": first_name,
                    "Last_Name": last_name,
                    "ClientId": "",
                    "Status": status
                }

        # new data processsing
        try:
            data_new_clientId = sheet.cell(60,18).value
        except:
            data_new_clientId = ''
        try:
            data_new_status = sheet.cell(61,18).value
        except:
            data_new_status = ''
        try:
            data_new_7202_21_4b = sheet.cell(63,18).value
        except:
            data_new_7202_21_4b = ''
        try:
            data_new_7202_21_6b = sheet.cell(64,18).value
        except:
            data_new_7202_21_6b = ''
        try:
            data_new_7202_21_38b = sheet.cell(65,18).value
        except:
            data_new_7202_21_38b = ''
        try:
            data_new_7202_21_40b = sheet.cell(66,18).value
        except:
            data_new_7202_21_40b = ''

        new_intake_data = {
            "data_new_clientId": data_new_clientId,
            "data_new_status": data_new_status,
            "data_new_7202_21_4b": data_new_7202_21_4b,
            "data_new_7202_21_6b": data_new_7202_21_6b,
            "data_new_7202_21_38b": data_new_7202_21_38b,
            "data_new_7202_21_40b": data_new_7202_21_40b
        }


        data_2019_reca_list = {}
        data_2020_reca_list = {}
        data_2021_reca_list = {}
        data_variables = [
                "F8995 QUALIFIED BUSINESS INCOME DEDUCTION COMPUTER",
                "SELF EMPLOYMENT TAX DEDUCTION PER COMPUTER",
                "ADJUSTED GROSS INCOME",
                "ADJUSTED GROSS INCOME PER COMPUTER",
                "STANDARD DEDUCTION PER COMPUTER",
                "TENTATIVE TAX",
                "TOTAL CREDITS",
                "SE TAX",
                "FEDERAL INCOME TAX WITHHELD",
                "ESTIMATED TAX PAYMENTS",
                "OTHER PAYMENT CREDIT",
                "EARNED INCOME CREDIT",
                "TOTAL PAYMENTS",
                "BAL DUE/OVER PYMT USING TP FIG PER COMPUTER",
                "TOTAL QUALIFIED BUSINESS INCOME OR LOSS",
                "FILING STATUS",
                "SE INCOME PER COMPUTER",
                "Credit to your account",
                "ACCOUNT BALANCE",
                "ACCRUED INTEREST",
                "TAXABLE INCOME",
                "TAX PER RETURN",
                "SCHEDULE 8812 ADDITIONAL CHILD TAX CREDIT",
                "FORM 2439 REGULATED INVESTMENT COMPANY CREDIT",
                "FORM 4136 CREDIT FOR FEDERAL TAX ON FUELS PER COMPUTER",
                "TOTAL EDUCATION CREDIT AMOUNT PER COMPUTER",
                "HEALTH COVERAGE TX CR",
                "AMOUNT YOU OWE",
                "REFUND AMOUNT",
                "SICK FAMILY LEAVE CREDIT AFTER 3-31-21",
                "SICK FAMILY LEAVE CREDIT",
                "PREMIUM TAX CREDIT AMOUNT",
                "REFUNDABLE CREDITS PER COMPUTER",
                "SCHEDULE 8812 ADDITIONAL CHILD TAX CREDIT PER COMPUTER",
                "RECOVERY REBATE CREDIT PER COMPUTER",
                "WAGES, SALARIES, TIPS, ETC",
                "TAX-EXEMPT INTEREST",
                "QUALIFIED DIVIDENDS",
                "TOTAL IRA DISTRIBUTIONS",
                "TOTAL PENSIONS AND ANNUITIES",
                "TOTAL SOCIAL SECURITY BENEFITS",
                "TAXABLE INTEREST INCOME",
                "ORDINARY DIVIDEND INCOME",
                "TAXABLE IRA DISTRIBUTIONS",
                "TAXABLE PENSION/ANNUITY AMOUNT",
                "TAXABLE SOCIAL SECURITY BENEFITS PER COMPUTER",
                "CAPITAL GAIN OR LOSS",
                "OTHER INCOME",
                "TOTAL ADJUSTMENTS PER COMPUTER",
                "NON ITEMIZED CHARITABLE CONTRIBUTION PER COMPUTER",
                "BUSINESS INCOME OR LOSS (SCHEDULE C)",
                "CHILD AND OTHER DEPENDENT CREDIT PER COMPUTER",
                "EXCESS ADVANCE PREMIUM TAX CREDIT REPAYMENT AMOUNT",
                "SEC 965 TAX INSTALLMENT",
                "CHILD & DEPENDENT CARE CREDIT",
                "ESTIMATED TAX PENALTY",
                "APPLIED TO NEXT YEAR'S ESTIMATED TAX",
                "EARNED INCOME CREDIT NONTAXABLE COMBAT PAY",
                "MAX DEFERRED TAX PER COMPUTER",
                "EIC PRIOR YEAR EARNED INCOME"
                ]
        
        data_variables_19 = [
                "Credit to your account",
                "ACCOUNT BALANCE",
                "ACCRUED INTEREST",
                "FILING STATUS",
                "ADJUSTED GROSS INCOME",
                "TAXABLE INCOME",
                "TAX PER RETURN",
                ]
        
        for key in data_variables_19:
            data_2019_reca_list[key]=  '0'

        for key in data_variables:
            data_2020_reca_list[key] = '0'
            data_2021_reca_list[key] = '0'


        try:
            for data_val in json.loads(item.get('result', {})).get('2019_RECA', {}).get('Data', [])[0].get('Transactions', ''):
                if data_val.get('Desc', '') == 'Credit to your account':
                    amount = data_val.get('Amount', '0').replace('$', '').replace(',', '').replace('-', '0')
                    if amount.replace('.', '').isdigit():
                        data_2019_reca_list["Credit to your account"] = int(float(amount))
                    else:
                        data_2019_reca_list["Credit to your account"] = amount
        except Exception as e:
            print(f"Error processing 2020 credit: {e}")

        try:
            for data_val in item.get('result', {}).get('2020_RECA', {}).get('Data', [])[0].get('Transactions', ''):
                if data_val.get('Desc', '') == 'Credit to your account':
                    amount = data_val.get('Amount', '0').replace('$', '').replace(',', '').replace('-', '0')
                    if amount.replace('.', '').isdigit():
                        data_2020_reca_list["Credit to your account"] = int(float(amount))
                    else:
                        data_2020_reca_list["Credit to your account"] = amount
        except Exception as e:
            print(f"Error processing 2020 credit: {e}")

        try:
            for data_val in item.get('result', {}).get('2021_RECA', {}).get('Data', [])[0].get('Transactions', ''):
                if data_val.get('Desc', '') == 'Credit to your account':
                    amount = data_val.get('Amount', '0').replace('$', '').replace(',', '').replace('-', '0')
                    if amount.replace('.', '').isdigit():
                        data_2021_reca_list["Credit to your account"] = int(float(amount))
                    else:
                        data_2021_reca_list["Credit to your account"] = amount
        except Exception as e:
            print(f"Error processing 2021 credit: {e}")


        try:
            for data_val in item.get('result', {}).get('2019_RECA', {}).get('Data', [])[0].get('DataValues', ''):
                key = data_val.get('DataKey', '')
                if key in data_variables_19:
                    value = data_val.get('DataValue', '0').replace('$', '').replace(',', '').replace('-', '0')
                    if value.replace('.', '').isdigit():
                        data_2019_reca_list[key] = int(float(value))
                    else:
                        data_2019_reca_list[key] = value
        except Exception as e:
            print(f"Error processing 2020 data values: {e}")

        try:
            for data_val in item.get('result', {}).get('2020_RECA', {}).get('Data', [])[0].get('DataValues', ''):
                key = data_val.get('DataKey', '')
                if key in data_variables:
                    value = data_val.get('DataValue', '0').replace('$', '').replace(',', '').replace('-', '0')
                    if value.replace('.', '').isdigit():
                        data_2020_reca_list[key] = int(float(value))
                    else:
                        data_2020_reca_list[key] = value
        except Exception as e:
            print(f"Error processing 2020 data values: {e}")

        try:
            for data_val in item.get('result', {}).get('2021_RECA', {}).get('Data', [])[0].get('DataValues', ''):
                key = data_val.get('DataKey', '')
                if key in data_variables:
                    value = data_val.get('DataValue', '0').replace('$', '').replace(',', '').replace('-', '0')
                    if value.replace('.', '').isdigit():
                        data_2021_reca_list[key] = int(float(value))
                    else:
                        data_2021_reca_list[key] = value
        except Exception as e:
            print(f"Error processing 2021 data values: {e}")

        extracted_data.append({
            'old_intake_data': old_intake_data,
            'old_intake_dates': old_dates,
            'new_intake_data': new_intake_data,
            '2019': data_2019_reca_list,
            '2020': data_2020_reca_list,
            '2021': data_2021_reca_list
        })
        print(extracted_data)

    return extracted_data

def place_data_variables(sheet_name, data_variables):

    
    sheet = gsheet_client.open(sheet_name).get_worksheet(0)

    for data in data_variables:
        row_number = 37
        for key,val in data['2020'].items():
            sheet.update_cell(row_number,13,val)
            row_number += 1
            time.sleep(0.05)
        
        row_number = 37
        for key,val in data['2021'].items():
            sheet.update_cell(row_number,14,val)
            row_number += 1
            time.sleep(0.05)

        row_number = 36
        for key,val in data['old_intake_data'].items():
            sheet.update_cell(row_number,20,val)
            row_number += 1
            time.sleep(0.05)

    credit_to_your_account_19 = data_variables[0]['2019']['Credit to your account']
    sheet.update_cell(54,15,credit_to_your_account_19)
    account_balance_19 = data_variables[0]['2019']['ACCOUNT BALANCE']
    sheet.update_cell(55,15,account_balance_19)
    accrued_interest_19 = data_variables[0]['2019']['ACCRUED INTEREST']
    sheet.update_cell(56,15,accrued_interest_19)
    time.sleep(0.3)
    filing_status_19 = data_variables[0]['2019']['FILING STATUS']
    sheet.update_cell(52,15,filing_status_19)
    taxable_income_19 = data_variables[0]['2019']['TAXABLE INCOME']
    sheet.update_cell(57,15,taxable_income_19)
    adjusted_gross_income_19 = data_variables[0]['2019']['ADJUSTED GROSS INCOME']
    sheet.update_cell(39,15,adjusted_gross_income_19)
    tax_per_return_19 = data_variables[0]['2019']['TAX PER RETURN']
    sheet.update_cell(58,15,tax_per_return_19)

    print("Data placed successfully!")

def get_7202_20_data(data_variables):

    instructions_data =  get_instructions_data(data_variables)
    twenty_7202_Day_Overide_1 = int(instructions_data['Gov_April_1_2020_through_December_31_2020'])
    # pull the date variable from Gov_April_1_2020_through_December_3
    # AL7
    AL7 = int(twenty_7202_Day_Overide_1)
    twenty_7202_Day_Overide_2 = int(instructions_data['Child_April_1_2020_through_December_31_2020'])
    # pull the date variable from Child_April_1_2020_through_December_31_2020
    # AL8
    AL8 = int(twenty_7202_Day_Overide_2)
    twenty_7202_Day_Overide_3 = int(instructions_data['Family_April_1_2020_through_December_31_2020'])
    # pull the date variable from Family_April_1_2020_through_December_31_2020
    # = AL9
    AL9 = int(twenty_7202_Day_Overide_3)

    # this is the 2019 income variable
    twenty_7202_2019 = int(instructions_data['nineteen_ADJUSTED_GROSS_INCOME'])

    # this is the 2020 income variables
    twenty_7202_20Schedule_SE_Line_3 = int(instructions_data['twenty_SE_income_per_computer'])

    # formula =ROUND(IF(AL24>0,AL24*0.9235,AL24),0)
    # Given value of AL24
    AL24 = int(twenty_7202_20Schedule_SE_Line_3)
    # Applying the formula
    AL24result = int(round(AL24 * 0.9235 if AL24 > 0 else AL24, 0))
    # print(AL24result)

    twenty_7202_20_Line_4a = AL24result

    twenty_7202_20_Line_4b = 0
    # was AL26

    # AL27
    # =MAX(SUM(AL25,AL26),0)
    # AL25 = twenty_7202_20_Line_4a,  AL26= twenty_7202_20_Line 4b
    # Given values of AL25 and AL26
    AL25 = int(twenty_7202_20_Line_4a)
    AL26 = int(twenty_7202_20_Line_4b)

    # Applying the formula
    twenty_7202_20_Line_4c_result = max(sum([AL25, AL26]), 0)
    twenty_7202_20_Line_4c = twenty_7202_20_Line_4c_result



    twenty_7202_20_Line_5a = 0

    # AL29
    # =ROUND(AL28*0.9235,0)
    # Given value of AL28
    AL28 = int(twenty_7202_20_Line_5a)
    # Applying the formula
    twenty_7202_20_Line_5b_result = round(AL28 * 0.9235, 0)
    twenty_7202_20_Line_5b = twenty_7202_20_Line_5b_result



    # =AL27+AL29
    # Given Values of AL27 AL29
    AL27 = int(twenty_7202_20_Line_4c)
    AL29 = int(twenty_7202_20_Line_5b)
    # Adding the values
    twenty_7202_20_Line_6_result = AL27 + AL29
    twenty_7202_20_Line_6 = twenty_7202_20_Line_6_result


    Fiscal_Year_Return = True
    Sick_Leave_1 = 0
    Sick_Leave_2 = 0
    Sick_Leave_3 = 0
    AL21 = Sick_Leave_3


    # start the Column for the 7202 form

    twenty_7202_1 = twenty_7202_Day_Overide_1
    # = AJ5
    # =SUMIF($AM$7:$AM$16,"Self",$AP$7:$AP$16)
    AJ5 = int(twenty_7202_1)

    # this is working on Line 2
    # AJ6
    # =IF(AJ5>9,0,MIN(10-AJ5,SUMIF($AM$7:$AM$16,"Other",$AP$7:$AP$16)))

    if AJ5 > 9:
        twenty_7202_2_result = 0
    else:
        twenty_7202_2_result = min(10 - int(AJ5), 10)

    twenty_7202_2 = twenty_7202_2_result
    AJ6 = int(twenty_7202_2)

    # This is working on Line 3
    # AJ7
    # =IF(AJ5=0,0,IF(AL18="no",10,"View instructions"))
    # AL18 = Fiscal_Year_Return
    # This Python code will set result to 0 if AJ5 equals 0. If AJ5 is not 0, it checks the value of Fiscal_Year_Return. If Fiscal_Year_Return is False, it sets result to 10, otherwise, it sets result to "View instructions".
    twenty_7202_3 = 0 if AJ5 == 0 else (10 if Fiscal_Year_Return else "View instructions")
    AJ7 = int(twenty_7202_3)

    # working on line 4
    #AJ8
    # =MIN(AJ5,AJ7)
    # This Python code will assign the minimum value between AJ5 and AJ7 to the variable.
    twenty_7202_4 = min(AJ5, AJ7)
    AJ8 = int(twenty_7202_4)

    # working on Line 5
    # AJ9
    # =IF(AJ5=0,0,AJ7-AJ8)

    if AJ5 == 0:
        twenty_7202_5 = 0
    else:
        twenty_7202_5 = AJ7 - AJ8
    AJ9 = int(twenty_7202_5)

    # working on Line 6
    # AJ10
    # =MIN(AJ6,AJ9)

    twenty_7202_6 = min(AJ6, AJ9)
    AJ10 = twenty_7202_6

    # working on Line 7
    # AJ11
    # =MAX(AL30,AN24)
    AL30 = twenty_7202_20_Line_6
    AN24 = twenty_7202_2019

    twenty_7202_7 = max(AL30, AN24)
    AJ11 = twenty_7202_7

    # working on Line 8
    # AJ12
    # =ROUND(AJ11/260,0)
    twenty_7202_8 = int(round(AJ11 / 260, 0))
    AJ12 = twenty_7202_8

    # working on Line 9
    # AJ13
    # =MIN(AJ12,511)
    twenty_7202_9 = min(AJ12,511)
    AJ13 = twenty_7202_9

    # working on Line 10
    # AJ14
    # =ROUND(AJ13*AJ8,0)
    twenty_7202_10 = int(round(AJ13*AJ8,0))
    AJ14 = twenty_7202_10

    # working on Line 11
    # AJ15
    # =ROUND(AJ12*0.67,0)
    twenty_7202_11 = int(round(AJ12*0.67,0))
    AJ15 = twenty_7202_11

    # working on Line 12
    # AJ16
    # =MIN(AJ15,200)
    twenty_7202_12 =min(AJ15,200)
    AJ16 = twenty_7202_12

    # working on Line 13
    # AJ17
    # =AJ16*AJ10
    twenty_7202_13 =AJ16*AJ10
    AJ17 = twenty_7202_13

    # working on Line 14
    # AJ18
    # =AJ17+AJ14
    twenty_7202_14 =AJ17+AJ14
    AJ18 = twenty_7202_14

    # working on Line 15
    # AJ19
    # =AL19 = Sick_Leave_1
    twenty_7202_15 = Sick_Leave_1
    AJ19 = twenty_7202_15

    # working on Line 16
    # AJ20
    # =AL20  = Sick_Leave_2
    twenty_7202_16 = Sick_Leave_2
    AJ20 = twenty_7202_16

    # working on Line 17
    # AJ22
    # =AJ20+AJ17
    twenty_7202_17 =AJ20+AJ17
    AJ22 = twenty_7202_17

    # working on Line 18
    # AJ23
    # =MIN(AJ22,2000)
    twenty_7202_18 =min(AJ22,2000)
    AJ23 = twenty_7202_18


    # working on Line 19
    # AJ24
    # =AJ22-AJ23
    twenty_7202_19 =AJ22-AJ23
    AJ24 = twenty_7202_19

    # working on Line 20
    # AJ25
    # =AJ14+AJ19+AJ23
    twenty_7202_20 =AJ14+AJ19+AJ23
    AJ25 = twenty_7202_20

    # working on Line 21
    # AJ26
    # =MIN(AJ25,5110)
    twenty_7202_21 =min(AJ25,5110)
    AJ26 = twenty_7202_21

    # working on Line 22
    # AJ27
    # =AJ25-AJ26
    twenty_7202_22 =AJ25-AJ26
    AJ27 = twenty_7202_22

    # working on Line 23
    # AJ28
    # =AJ24+AJ27
    twenty_7202_23 =AJ24+AJ27
    AJ28 = twenty_7202_23

    # working on Line 24
    # AJ30
    # =IF((AJ18-AJ28)<=0,0,AJ18-AJ28)
    if (AJ18 - AJ28) <= 0:
        twenty_7202_24 = 0
    else:
        twenty_7202_24 = AJ18 - AJ28
    AJ30= twenty_7202_24

    # working on Line 25
    # AJ34
    # =MIN(SUMIF($AM$7:$AM$16,"Fam Leave",$AP$7:$AP$16),50)
    # AL9 = twenty_7202_Day_Overide_3
    # Take the minimum between the sum and 50
    twenty_7202_25 = min(twenty_7202_Day_Overide_3, 50)
    AJ34 = twenty_7202_25

    # working on Line 26
    # AJ26
    # =AJ11
    twenty_7202_26 =AJ11
    AJ35 = twenty_7202_26

    # working on Line 27
    # AJ36
    # =ROUND(AJ35/260,0)
    twenty_7202_27 =int(round(AJ35/260,0))
    AJ36 = twenty_7202_27

    # working on Line 28
    # AJ37
    # =ROUND(AJ36*0.67,0)
    twenty_7202_28 =int(round(AJ36*0.67,0))
    AJ37 = twenty_7202_28

    # working on Line 29
    # AJ38
    # =MIN(AJ37,200)
    twenty_7202_29 =min(AJ37,200)
    AJ38 = twenty_7202_29

    # working on Line 30
    # AJ39
    # =AJ32*AJ38
    AJ32 = AJ34

    twenty_7202_30 = AJ32*AJ38
    AJ39 = twenty_7202_30

    # working on Line 31
    # =AJ40 as the cell
    # =AL21 = new Sick_Leave_3
    twenty_7202_31 = Sick_Leave_3
    AJ40 = twenty_7202_31

    # working on Line 32
    # AJ42
    # =AJ39+AJ40
    twenty_7202_32 = AJ39+AJ40
    AJ42 = twenty_7202_32

    # working on Line 33
    # AJ43
    # =MIN(AJ42,10000)
    twenty_7202_33 =min(AJ42,10000)
    AJ43 = twenty_7202_33

    # working on Line 34
    # AJ44
    # =AJ42-AJ43
    twenty_7202_34 =AJ42-AJ43
    AJ44 = twenty_7202_34

    # working on Line 35
    # AJ46
    # =MAX(AJ39-AJ44,0)
    twenty_7202_35 =max(AJ39-AJ44,0)
    AJ46 = twenty_7202_35


    # Total 2020 Credit (enter this number on Schedule 3 Line 12b)
    # =AJ45+AJ29
    # AJ49
    Total_2020_Credit =AJ46+AJ30

    data_7202_20 = {
        "data_7202_20_1": AJ5,
        "data_7202_20_2": AJ6,
        "data_7202_20_3": AJ7,
        "data_7202_20_4": AJ8,
        "data_7202_20_5": AJ9,
        "data_7202_20_6": AJ10,
        "data_7202_20_7": AJ11,
        "data_7202_20_8": AJ12,
        "data_7202_20_9": AJ13,
        "data_7202_20_10": AJ14,
        "data_7202_20_11": AJ15,
        "data_7202_20_12": AJ16,
        "data_7202_20_13": AJ17,
        "data_7202_20_14": AJ18,
        "data_7202_20_15": AJ19,
        "data_7202_20_16": AJ20,
        "data_7202_20_17": AJ22,
        "data_7202_20_18": AJ23,
        "data_7202_20_19": AJ24,
        "data_7202_20_20": AJ25,
        "data_7202_20_21": AJ26,
        "data_7202_20_22": AJ27,
        "data_7202_20_23": AJ28,
        "data_7202_20_24": AJ30,
        "data_7202_20_25": AJ34,
        "data_7202_20_26": AJ35,
        "data_7202_20_27": AJ36,
        "data_7202_20_28": AJ37,
        "data_7202_20_29": AJ38,
        "data_7202_20_30": AJ39,
        "data_7202_20_31": AJ40,
        "data_7202_20_32": AJ42,
        "data_7202_20_33": AJ43,
        "data_7202_20_34": AJ44,
        "data_7202_20_35": AJ46,
        "data_7202_20_total_credit": Total_2020_Credit
    }  

    return data_7202_20


def get_sch_3_20_data(data_variables):
    twenty_schd3_7 = 0
    

    twenty_schd3_12b = get_7202_20_data(data_variables)['data_7202_20_total_credit']

    twenty_schd3_12f = twenty_schd3_12b

    twenty_schd3_13 = twenty_schd3_12f + twenty_schd3_7

    data_sch_3_20 = {
            "data_sch_3_20_7": twenty_schd3_7,
            "data_sch_3_20_12b" : twenty_schd3_12b,
            "data_sch_3_20_12f" : twenty_schd3_12f,
            "data_sch_3_20_13" : twenty_schd3_13
    }

    return data_sch_3_20


def get_1040_20_data(data_variables):
    # line 1
    #AB35
    # =Instructions!M72 = twenty_wages_salaries_tips_etc
    instructions_data = get_instructions_data(data_variables)

    sch_3_data = get_sch_3_20_data(data_variables)

    twenty1040_1 = int(instructions_data['twenty_wages_salaries_tips_etc'])

    #2a
    #=Instructions!M73 =twenty_tax_exempt_interest
    #
    twenty1040_2a = int(instructions_data['twenty_tax_exempt_interest'])

    # =Instructions!M78
    twenty1040_2b = int(instructions_data['twenty_taxable_interest_income'])

    #
    twenty1040_3a = int(instructions_data['twenty_qualified_dividends'])

    twenty1040_3b = int(instructions_data['twenty_ordinary_dividend_income'])

    twenty1040_4a = int(instructions_data['twenty_total_IRA_distributions'])
    twenty1040_4b = int(instructions_data['twenty_taxable_IRA_distributions'])

    twenty1040_5a = int(instructions_data['twenty_total_pensions_and_annuities'])
    twenty1040_5b = int(instructions_data['twenty_taxable_pension_annuity_amount'])  # Corrected variable name

    twenty1040_6a = int(instructions_data['twenty_total_social_security_benefits'])
    twenty1040_6b = int(instructions_data['twenty_taxable_social_security_benefits_per_computer'])

    twenty1040_7 = int(instructions_data['twenty_capital_gain_or_loss'])
    twenty1040_8 = int(instructions_data['twenty_other_income'])
    twenty1040_9 = twenty1040_1 + twenty1040_2b + twenty1040_3b + twenty1040_4b + twenty1040_5b + twenty1040_6b + twenty1040_7 + twenty1040_8

    twenty1040_10a = int(instructions_data['twenty_total_adjustments_per_computer'])
    twenty1040_10b = int(instructions_data['twenty_non_itemized_charitable_contribution_per_computer'])
    twenty1040_10c = twenty1040_10a + twenty1040_10b

    twenty1040_11 = abs(twenty1040_9 - twenty1040_10c)
    twenty1040_12 = int(instructions_data['twenty_standard_deduction_per_computer'])
    twenty1040_13 = int(instructions_data['twenty_business_income_or_loss_schedule_C'])
    twenty1040_14 = twenty1040_12 + twenty1040_13
    twenty1040_15 = max(0, twenty1040_11 - twenty1040_14)
    twenty1040_16 = int(instructions_data['twenty_tentative_tax'])
    twenty1040_17 = 0
    twenty1040_18 = twenty1040_16 + twenty1040_17
    twenty1040_19 = 0
    twenty1040_20 = int(sch_3_data['data_sch_3_20_7']) if 'data_sch_3_20_7' in sch_3_data else 0
    twenty1040_21 = twenty1040_19 + twenty1040_20
    # Assigns the result of the formula to twenty1040_22
    twenty1040_22 = max(twenty1040_18 - twenty1040_21, 0)
    twenty1040_23 = int(instructions_data['twenty_SE_tax'])
    twenty1040_24 = twenty1040_23 + twenty1040_22
    twenty1040_25a = 0
    twenty1040_25b = 0
    twenty1040_25c = 0
    twenty1040_25d = twenty1040_25a + twenty1040_25b + twenty1040_25c
    twenty1040_26 = 0
    twenty1040_27 = int(instructions_data['twenty_earned_income_credit']) if 'twenty_earned_income_credit' in instructions_data else 0
    twenty1040_28 = int(instructions_data['twenty_schedule_8812_additional_child_tax_credit']) if 'twenty_schedule_8812_additional_child_tax_credit' in instructions_data else 0
    twenty1040_29 = int(instructions_data['twenty_total_education_credit_amount_per_computer']) if 'twenty_total_education_credit_amount_per_computer' in instructions_data else 0
    twenty1040_30 = int(instructions_data['twenty_recovery_rebate_credit_per_computer']) if 'twenty_recovery_rebate_credit_per_computer' in instructions_data else 0
    twenty1040_31 = int(sch_3_data['data_sch_3_20_13']) if 'data_sch_3_20_13' in sch_3_data else 0

    twenty1040_32 = twenty1040_27 + twenty1040_28 + twenty1040_29 + twenty1040_30 + twenty1040_31
    twenty1040_33 = twenty1040_25d + twenty1040_32 + twenty1040_26
    twenty1040_34 = max(twenty1040_33 - twenty1040_24, 0) if twenty1040_33 > twenty1040_24 else 0
    twenty1040_35a = twenty1040_34
    twenty1040_37 = twenty1040_24 - twenty1040_33 if twenty1040_34 == 0 else 0
    twenty1040_38 = int(instructions_data['twenty_estimated_tax_penalty'])

    data_1040_20 = {
        "data_1040_20_1": twenty1040_1,
        "data_1040_20_2a": twenty1040_2a,
        "data_1040_20_2b": twenty1040_2b,
        "data_1040_20_3a": twenty1040_3a,
        "data_1040_20_3b": twenty1040_3b,
        "data_1040_20_4a": twenty1040_4a,
        "data_1040_20_4b": twenty1040_4b,
        "data_1040_20_5a": twenty1040_5a,
        "data_1040_20_5b": twenty1040_5b,
        "data_1040_20_6a": twenty1040_6a,
        "data_1040_20_6b": twenty1040_6b,
        "data_1040_20_7": twenty1040_7,
        "data_1040_20_8": twenty1040_8,
        "data_1040_20_9": twenty1040_9,
        "data_1040_20_10a": twenty1040_10a,
        "data_1040_20_10b": twenty1040_10b,
        "data_1040_20_10c": twenty1040_10c,
        "data_1040_20_11": twenty1040_11,
        "data_1040_20_12": twenty1040_12,
        "data_1040_20_13": twenty1040_13,
        "data_1040_20_14": twenty1040_14,
        "data_1040_20_15": twenty1040_15,
        "data_1040_20_16": twenty1040_16,
        "data_1040_20_17": twenty1040_17,
        "data_1040_20_18": twenty1040_18,
        "data_1040_20_19": twenty1040_19,
        "data_1040_20_20": twenty1040_20,
        "data_1040_20_21": twenty1040_21,
        "data_1040_20_22": twenty1040_22,
        "data_1040_20_23": twenty1040_23,
        "data_1040_20_24": twenty1040_24,
        "data_1040_20_25a": twenty1040_25a,
        "data_1040_20_25b": twenty1040_25b,
        "data_1040_20_25c": twenty1040_25c,
        "data_1040_20_25d": twenty1040_25d,
        "data_1040_20_26": twenty1040_26,
        "data_1040_20_27": twenty1040_27,
        "data_1040_20_28": twenty1040_28,
        "data_1040_20_29": twenty1040_29,
        "data_1040_20_30": twenty1040_30,
        "data_1040_20_31": twenty1040_31,
        "data_1040_20_32": twenty1040_32,
        "data_1040_20_33": twenty1040_33,
        "data_1040_20_34": twenty1040_34,
        "data_1040_20_35a": twenty1040_35a,
        "data_1040_20_37": twenty1040_37,
        "data_1040_20_38": twenty1040_38,
    }

    return data_1040_20

