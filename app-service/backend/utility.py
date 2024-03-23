from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import boto3
import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from io import BytesIO
import pandas as pd
import time
from PyPDF2 import PdfFileMerger
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

def get_7202_20_data(sheet_name):

    sheet = gsheet_client.open(sheet_name).get_worksheet(1)

    try:
        data_7202_20_1 = sheet.cell(5,36).value.strip()
    except:
        data_7202_20_1 = ''
    time.sleep(0.1)
    try:
        data_7202_20_2 = sheet.cell(6,36).value.strip()
    except:
        data_7202_20_2 = ''
    time.sleep(0.1)
    try:
        data_7202_20_3 = sheet.cell(7,36).value.strip()
    except:
        data_7202_20_3 = ''
    time.sleep(0.1)
    try:
        data_7202_20_4 = sheet.cell(8,36).value.strip()
    except:
        data_7202_20_4 = ''
    time.sleep(0.1)
    try:
        data_7202_20_5 = sheet.cell(9,36).value.strip()
    except:
        data_7202_20_5 = ''
    time.sleep(0.1)
    try:
        data_7202_20_6 = sheet.cell(10,36).value.strip()
    except:
        data_7202_20_6 = ''
    time.sleep(0.1)
    try:
        data_7202_20_7 = sheet.cell(11,36).value.strip()
    except:
        data_7202_20_7 = ''
    time.sleep(0.1)
    try:
        data_7202_20_8 = sheet.cell(12,36).value.strip()
    except:
        data_7202_20_8 = ''
    time.sleep(0.1)
    try:
        data_7202_20_9 = sheet.cell(13,36).value.strip()
    except:
        data_7202_20_9 = ''
    time.sleep(0.1)
    try:
        data_7202_20_10 = sheet.cell(14,36).value.strip()
    except:
        data_7202_20_10 = ''
    time.sleep(0.1)
    try:
        data_7202_20_11 = sheet.cell(15,36).value.strip()
    except:
        data_7202_20_11 = ''
    time.sleep(0.1)
    try:
        data_7202_20_12 = sheet.cell(16,36).value.strip()
    except:
        data_7202_20_12 = ''
    time.sleep(0.1)
    try:
        data_7202_20_13 = sheet.cell(17,36).value.strip()
    except:
        data_7202_20_13 = ''
    time.sleep(0.1)
    try:
        data_7202_20_14 = sheet.cell(18,36).value.strip()
    except:
        data_7202_20_14 = ''
    try:
        data_7202_20_15 = sheet.cell(19,36).value.strip()
    except:
        data_7202_20_15 = ''
    try:
        data_7202_20_16 = sheet.cell(20,36).value.strip()
    except:
        data_7202_20_16 = ''
    try:
        data_7202_20_17 = sheet.cell(22,36).value.strip()
    except:
        data_7202_20_17 = ''
    try:
        data_7202_20_18 = sheet.cell(23,36).value.strip()
    except:
        data_7202_20_18 = ''
    try:
        data_7202_20_19 = sheet.cell(24,36).value.strip()
    except:
        data_7202_20_19 = ''
    try:
        data_7202_20_20 = sheet.cell(25,36).value.strip()
    except:
        data_7202_20_20 = ''
    try:
        data_7202_20_21 = sheet.cell(26,36).value.strip()
    except:
        data_7202_20_21 = ''
    try:
        data_7202_20_22 = sheet.cell(27,36).value.strip()
    except:
        data_7202_20_22 = ''
    try:
        data_7202_20_23 = sheet.cell(28,36).value.strip()
    except:
        data_7202_20_23 = ''
    try:
        data_7202_20_24 = sheet.cell(29,36).value.strip()
    except:
        data_7202_20_24 = ''
    try:
        data_7202_20_25 = sheet.cell(32,36).value.strip()
    except:
        data_7202_20_25 = ''
    try:
        data_7202_20_26 = sheet.cell(35,36).value.strip()
    except:
        data_7202_20_26 = ''
    try:
        data_7202_20_27 = sheet.cell(36,36).value.strip()
    except:
        data_7202_20_27 = ''
    try:
        data_7202_20_28 = sheet.cell(37,36).value.strip()
    except:
        data_7202_20_28 = ''
    try:
        data_7202_20_29 = sheet.cell(38,36).value.strip()
    except:
        data_7202_20_29 = ''
    try:
        data_7202_20_30 = sheet.cell(39,36).value.strip()
    except:
        data_7202_20_30 = ''
    try:
        data_7202_20_31 = sheet.cell(40,36).value.strip()
    except:
        data_7202_20_31 = ''
    try:
        data_7202_20_32 = sheet.cell(42,36).value.strip()
    except:
        data_7202_20_32 = ''
    time.sleep(0.1)
    try:
        data_7202_20_33 = sheet.cell(43,36).value.strip()
    except:
        data_7202_20_33 = ''
    time.sleep(0.1)
    try:
        data_7202_20_34 = sheet.cell(44,36).value.strip()
    except:
        data_7202_20_34 = ''
    try:
        data_7202_20_35 = sheet.cell(45,36).value.strip()
    except:
        data_7202_20_35 = '' 
    time.sleep(0.1)
    try:
        data_total_2020_credit = sheet.cell(49,36).value.strip()
    except:
        data_total_2020_credit = ''

    data_7202_20 = {
        "data_7202_20_1": data_7202_20_1,
        "data_7202_20_2": data_7202_20_2,
        "data_7202_20_3": data_7202_20_3,
        "data_7202_20_4": data_7202_20_4,
        "data_7202_20_5": data_7202_20_5,
        "data_7202_20_6": data_7202_20_6,
        "data_7202_20_7": data_7202_20_7,
        "data_7202_20_8": data_7202_20_8,
        "data_7202_20_9": data_7202_20_9,
        "data_7202_20_10": data_7202_20_10,
        "data_7202_20_11": data_7202_20_11,
        "data_7202_20_12": data_7202_20_12,
        "data_7202_20_13": data_7202_20_13,
        "data_7202_20_14": data_7202_20_14,
        "data_7202_20_15": data_7202_20_15,
        "data_7202_20_16": data_7202_20_16,
        "data_7202_20_17": data_7202_20_17,
        "data_7202_20_18": data_7202_20_18,
        "data_7202_20_19": data_7202_20_19,
        "data_7202_20_20": data_7202_20_20,
        "data_7202_20_21": data_7202_20_21,
        "data_7202_20_22": data_7202_20_22,
        "data_7202_20_23": data_7202_20_23,
        "data_7202_20_24": data_7202_20_24,
        "data_7202_20_25": data_7202_20_25,
        "data_7202_20_26": data_7202_20_26,
        "data_7202_20_27": data_7202_20_27,
        "data_7202_20_28": data_7202_20_28,
        "data_7202_20_29": data_7202_20_29,
        "data_7202_20_30": data_7202_20_30,
        "data_7202_20_31": data_7202_20_31,
        "data_7202_20_32": data_7202_20_32,
        "data_7202_20_33": data_7202_20_33,
        "data_7202_20_34": data_7202_20_34,
        "data_7202_20_35": data_7202_20_35,
        "data_7202_20_total_credit": data_total_2020_credit
    }  

    return data_7202_20

def get_sch_3_20_data(sheet_name):
    sheet = gsheet_client.open(sheet_name).get_worksheet(2)

    try:
        data_sch_3_20_1 = sheet.cell(10,28).value.strip()
    except:
        data_sch_3_20_1 = ''
    time.sleep(0.1)
    try:
        data_sch_3_20_2 = sheet.cell(11,28).value.strip()
    except:
        data_sch_3_20_2 = ''
    time.sleep(0.1)
    try:
        data_sch_3_20_3 = sheet.cell(12,28).value.strip()
    except:
        data_sch_3_20_3 = ''
    time.sleep(0.1)
    try:
        data_sch_3_20_4 = sheet.cell(13,28).value.strip()
    except:
        data_sch_3_20_4 = ''
    time.sleep(0.1)
    try:
        data_sch_3_20_5 = sheet.cell(14,28).value.strip()
    except:
        data_sch_3_20_5 = ''
    time.sleep(0.1)
    try:
        data_sch_3_20_6 = sheet.cell(15,28).value.strip()
    except:
        data_sch_3_20_6 = ''
    time.sleep(0.1)
    try:
        data_sch_3_20_7 = sheet.cell(16,28).value.strip()
    except:
        data_sch_3_20_7 = ''
    time.sleep(0.1)
    try:
        data_sch_3_20_8 = sheet.cell(18,28).value.strip()
    except:
        data_sch_3_20_8 = ''
    time.sleep(0.1)
    try:
        data_sch_3_20_9 = sheet.cell(19,28).value.strip()
    except:
        data_sch_3_20_9 = ''
    try:
        data_sch_3_20_10 = sheet.cell(20,28).value.strip()
    except:
        data_sch_3_20_10 = ''
    time.sleep(0.1)
    try:
        data_sch_3_20_11 = sheet.cell(21,28).value.strip()
    except:
        data_sch_3_20_11 = ''
    time.sleep(0.1)
    try:
        data_sch_3_20_12a = sheet.cell(23,22).value.strip()
    except:
        data_sch_3_20_12a = ''
    try:
        data_sch_3_20_12b = sheet.cell(25,22).value.strip()
    except:
        data_sch_3_20_12b = ''
    try:
        data_sch_3_20_12c = sheet.cell(26,22).value.strip()
    except:
        data_sch_3_20_12c = ''
    time.sleep(0.1)
    try:
        data_sch_3_20_12d = sheet.cell(27,22).value.strip()
    except:
        data_sch_3_20_12d = ''   
    try:
        data_sch_3_20_12e = sheet.cell(28,22).value.strip()
    except:
        data_sch_3_20_12e = ''
    try:
        data_sch_3_20_12f = sheet.cell(29,28).value.strip()
    except:
        data_sch_3_20_12f = ''
    time.sleep(0.1)
    try:
        data_sch_3_20_13 = sheet.cell(30,28).value.strip()
    except:
        data_sch_3_20_13 = ''
    data_sch_3_20 = {
            "data_sch_3_20_1" : data_sch_3_20_1,
            "data_sch_3_20_2" : data_sch_3_20_2,
            "data_sch_3_20_3" : data_sch_3_20_3,
            "data_sch_3_20_4" : data_sch_3_20_4,
            "data_sch_3_20_5" : data_sch_3_20_5,
            "data_sch_3_20_6" : data_sch_3_20_6,
            "data_sch_3_20_7" : data_sch_3_20_7,
            "data_sch_3_20_8" : data_sch_3_20_8,
            "data_sch_3_20_9" : data_sch_3_20_9,
            "data_sch_3_20_10" : data_sch_3_20_10,
            "data_sch_3_20_11" : data_sch_3_20_11,
            "data_sch_3_20_12a" : data_sch_3_20_12a,
            "data_sch_3_20_12b" : data_sch_3_20_12b,
            "data_sch_3_20_12c" : data_sch_3_20_12c,
            "data_sch_3_20_12d" : data_sch_3_20_12d,
            "data_sch_3_20_12e" : data_sch_3_20_12e,
            "data_sch_3_20_12f" : data_sch_3_20_12f,
            "data_sch_3_20_13" : data_sch_3_20_13
    }

    return data_sch_3_20

def get_1040_20_data(sheet_name):
    sheet = gsheet_client.open(sheet_name).get_worksheet(3)

    try:
        data_1040_20_1 = sheet.cell(35,28).value.strip()
    except:
        data_1040_20_1 = ''
    time.sleep(0.1)
    try:
        data_1040_20_7 = sheet.cell(41,28).value.strip()
    except:
        data_1040_20_7 = ''
    try:
        data_1040_20_8 = sheet.cell(42,28).value.strip()
    except:
        data_1040_20_8 = ''
    time.sleep(0.1)
    try:
        data_1040_20_9 = sheet.cell(43,28).value.strip()
    except:
        data_1040_20_9 = ''
    try:
        data_1040_20_11 = sheet.cell(48,28).value.strip()
    except:
        data_1040_20_11 = ''
    try:
        data_1040_20_12 = sheet.cell(49,28).value.strip()
    except:
        data_1040_20_12 = ''
    time.sleep(0.1)
    try:
        data_1040_20_13 = sheet.cell(50,28).value.strip()
    except:
        data_1040_20_13 = ''
    try:
        data_1040_20_14 = sheet.cell(51,28).value.strip()
    except:
        data_1040_20_14 = ''
    time.sleep(0.1)
    try:
        data_1040_20_15 = sheet.cell(52,28).value.strip()
    except:
        data_1040_20_15 = ''
    time.sleep(0.1)
    try:
        data_1040_20_16 = sheet.cell(55,28).value.strip()
    except:
        data_1040_20_16 = ''
    time.sleep(0.1)
    try:
        data_1040_20_17 = sheet.cell(56,28).value.strip()
    except:
        data_1040_20_17 = ''
    time.sleep(0.1)
    try:
        data_1040_20_18 = sheet.cell(57,28).value.strip()
    except:
        data_1040_20_18 = ''
    time.sleep(0.1)
    try:
        data_1040_20_19 = sheet.cell(58,28).value.strip()
    except:
        data_1040_20_19 = ''
    try:
        data_1040_20_20 = sheet.cell(59,28).value.strip()
    except:
        data_1040_20_20 = ''
    try:
        data_1040_20_21 = sheet.cell(60,28).value.strip()
    except:
        data_1040_20_21 = ''
    try:
        data_1040_20_22 = sheet.cell(61,28).value.strip()
    except:
        data_1040_20_22 = '' 
    time.sleep(0.1)
    try:
        data_1040_20_23 = sheet.cell(62,28).value.strip()
    except:
        data_1040_20_23 = '' 
    time.sleep(0.1)
    try:
        data_1040_20_24 = sheet.cell(63,28).value.strip()
    except:
        data_1040_20_24 = '' 
    try:
        data_1040_20_26 = sheet.cell(69,28).value.strip()
    except:
        data_1040_20_26 = '' 
    time.sleep(0.1)
    try:
        data_1040_20_27 = sheet.cell(70,24).value.strip()
    except:
        data_1040_20_27 = '' 
    time.sleep(0.1)
    try:
        data_1040_20_28 = sheet.cell(71,24).value.strip()
    except:
        data_1040_20_28 = '' 
    time.sleep(0.1)
    try:
        data_1040_20_29 = sheet.cell(72,24).value.strip()
    except:
        data_1040_20_29 = '' 
    time.sleep(0.1)
    try:
        data_1040_20_30 = sheet.cell(73,24).value.strip()
    except:
        data_1040_20_30 = '' 
    time.sleep(0.1)
    try:
        data_1040_20_31 = sheet.cell(74,24).value.strip()
    except:
        data_1040_20_31 = '' 
    time.sleep(0.1)
    try:
        data_1040_20_32 = sheet.cell(75,28).value.strip()
    except:
        data_1040_20_32 = ''
    time.sleep(0.1)
    try:
        data_1040_20_33 = sheet.cell(76,28).value.strip()
    except:
        data_1040_20_33 = '' 
    time.sleep(0.1)
    try:
        data_1040_20_34 = sheet.cell(77,28).value.strip()
    except:
        data_1040_20_34 = ''
    time.sleep(0.1)
    try:
        data_1040_20_36 = sheet.cell(81,21).value.strip()
    except:
        data_1040_20_36 = '' 
    try:
        data_1040_20_37 = sheet.cell(82,28).value.strip()
    except:
        data_1040_20_37 = '' 
    try:
        data_1040_20_38 = sheet.cell(84,21).value.strip()
    except:
        data_1040_20_38 = '' 
    time.sleep(0.1)
    try:
        data_1040_20_35a = sheet.cell(78,28).value.strip()
    except:
        data_1040_20_35a = ''
    time.sleep(0.1)
    try:
        data_1040_20_2a = sheet.cell(36,13).value.strip()
    except:
        data_1040_20_2a = '' 
    time.sleep(0.1)
    try:
        data_1040_20_3a = sheet.cell(37,13).value.strip()
    except:
        data_1040_20_3a = ''
    time.sleep(0.1)
    try:
        data_1040_20_4a = sheet.cell(38,13).value.strip()
    except:
        data_1040_20_4a = ''
    try:
        data_1040_20_5a = sheet.cell(39,13).value.strip()
    except:
        data_1040_20_5a = ''
    time.sleep(0.1)
    try:
        data_1040_20_6a = sheet.cell(40,13).value.strip()
    except:
        data_1040_20_6a = ''
    try:
        data_1040_20_2b = sheet.cell(36,28).value.strip()
    except:
        data_1040_20_2b = ''
    time.sleep(0.1)
    try:
        data_1040_20_3b = sheet.cell(37,28).value.strip()
    except:
        data_1040_20_3b = ''
    time.sleep(0.1)
    try:
        data_1040_20_4b = sheet.cell(38,28).value.strip()
    except:
        data_1040_20_4b = ''
    try:
        data_1040_20_5b = sheet.cell(39,28).value.strip()
    except:
        data_1040_20_5b = ''
    time.sleep(0.1)
    try:
        data_1040_20_6b = sheet.cell(40,28).value.strip()
    except:
        data_1040_20_6b = ''
    try:
        data_1040_20_10a = sheet.cell(45,24).value.strip()
    except:
        data_1040_20_10a = ''
    try:
        data_1040_20_10b = sheet.cell(46,24).value.strip()
    except:
        data_1040_20_10b = '' 
    try:
        data_1040_20_10c = sheet.cell(47,28).value.strip()
    except:
        data_1040_20_10c = ''
    try:
        data_1040_20_25a = sheet.cell(65,24).value.strip()
    except:
        data_1040_20_25a = ''
    time.sleep(0.1)
    try:
        data_1040_20_25b = sheet.cell(66,24).value.strip()
    except:
        data_1040_20_25b = ''
    try:
        data_1040_20_25c = sheet.cell(67,24).value.strip()
    except:
        data_1040_20_25c = ''
    time.sleep(0.1)
    try:
        data_1040_20_25d = sheet.cell(68,28).value.strip()
    except:
        data_1040_20_25d = ''
    
    data_1040_20 = {
        "data_1040_20_1": data_1040_20_1,
        "data_1040_20_2a": data_1040_20_2a,
        "data_1040_20_2b": data_1040_20_2b,
        "data_1040_20_3a": data_1040_20_3a,
        "data_1040_20_3b": data_1040_20_3b,
        "data_1040_20_4a": data_1040_20_4a,
        "data_1040_20_4b": data_1040_20_4b,
        "data_1040_20_5a": data_1040_20_5a,
        "data_1040_20_5b": data_1040_20_5b,
        "data_1040_20_6a": data_1040_20_6a,
        "data_1040_20_6b": data_1040_20_6b,
        "data_1040_20_7": data_1040_20_7,
        "data_1040_20_8": data_1040_20_8,
        "data_1040_20_9": data_1040_20_9,
        "data_1040_20_10a": data_1040_20_10a,
        "data_1040_20_10b": data_1040_20_10b,
        "data_1040_20_10c": data_1040_20_10c,
        "data_1040_20_11": data_1040_20_11,
        "data_1040_20_12": data_1040_20_12,
        "data_1040_20_13": data_1040_20_13,
        "data_1040_20_14": data_1040_20_14,
        "data_1040_20_15": data_1040_20_15,
        "data_1040_20_16": data_1040_20_16,
        "data_1040_20_17": data_1040_20_17,
        "data_1040_20_18": data_1040_20_18,
        "data_1040_20_19": data_1040_20_19,
        "data_1040_20_20": data_1040_20_20,
        "data_1040_20_21": data_1040_20_21,
        "data_1040_20_22": data_1040_20_22,
        "data_1040_20_23": data_1040_20_23,
        "data_1040_20_24": data_1040_20_24,
        "data_1040_20_25a": data_1040_20_25a,
        "data_1040_20_25b": data_1040_20_25b,
        "data_1040_20_25c": data_1040_20_25c,
        "data_1040_20_25d": data_1040_20_25d,
        "data_1040_20_26": data_1040_20_26,
        "data_1040_20_27": data_1040_20_27,
        "data_1040_20_28": data_1040_20_28,
        "data_1040_20_29": data_1040_20_29,
        "data_1040_20_30": data_1040_20_30,
        "data_1040_20_31": data_1040_20_31,
        "data_1040_20_32": data_1040_20_32,
        "data_1040_20_33": data_1040_20_33,
        "data_1040_20_34": data_1040_20_34,
        "data_1040_20_35a": data_1040_20_35a,
        "data_1040_20_36": data_1040_20_36,
        "data_1040_20_37": data_1040_20_37,
        "data_1040_20_38": data_1040_20_38,
    }

    return data_1040_20

def get_1040x_20_data(sheet_name):
    sheet = gsheet_client.open(sheet_name).get_worksheet(4)

    try:
        data_1040x_20_original_1 = sheet.cell(12,11).value.strip()
    except:
        data_1040x_20_original_1 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_correct_1 = sheet.cell(12,19).value.strip()
    except:
        data_1040x_20_correct_1 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_original_2 = sheet.cell(13,11).value.strip()
    except:
        data_1040x_20_original_2 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_correct_2 = sheet.cell(13,19).value.strip()
    except:
        data_1040x_20_correct_2 = ''
    try:
        data_1040x_20_original_3 = sheet.cell(14,11).value.strip()
    except:
        data_1040x_20_original_3 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_correct_3 = sheet.cell(14,19).value.strip()
    except:
        data_1040x_20_correct_3 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_original_4a = sheet.cell(15,11).value.strip()
    except:
        data_1040x_20_original_4a = ''
    time.sleep(0.1)
    try:
        data_1040x_20_correct_4a = sheet.cell(15,19).value.strip()
    except:
        data_1040x_20_correct_4a = ''
    time.sleep(0.1)
    try:
        data_1040x_20_original_4b = sheet.cell(16,11).value.strip()
    except:
        data_1040x_20_original_4b = ''
    try:
        data_1040x_20_correct_4b = sheet.cell(16,19).value.strip()
    except:
        data_1040x_20_correct_4b = ''
    try:
        data_1040x_20_original_5 = sheet.cell(17,11).value.strip()
    except:
        data_1040x_20_original_5 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_correct_5 = sheet.cell(17,19).value.strip()
    except:
        data_1040x_20_correct_5 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_original_6 = sheet.cell(18,11).value.strip()
    except:
        data_1040x_20_original_6 = ''
    try:
        data_1040x_20_correct_6 = sheet.cell(18,19).value.strip()
    except:
        data_1040x_20_correct_6 = ''
    try:
        data_1040x_20_original_7  = sheet.cell(19,11).value.strip()
    except:
        data_1040x_20_original_7  = ''
    time.sleep(0.1)
    try:
        data_1040x_20_correct_7  = sheet.cell(19,19).value.strip()
    except:
        data_1040x_20_correct_7  = ''
    try:
        data_1040x_20_original_8 = sheet.cell(20,11).value.strip()
    except:
        data_1040x_20_original_8 = ''
    try:
        data_1040x_20_correct_8 = sheet.cell(20,19).value.strip()
    except:
        data_1040x_20_correct_8 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_original_9 = sheet.cell(21,11).value.strip()
    except:
        data_1040x_20_original_9 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_correct_9 = sheet.cell(21,19).value.strip()
    except:
        data_1040x_20_correct_9 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_original_10 = sheet.cell(22,11).value.strip()
    except:
        data_1040x_20_original_10 = ''
    try:
        data_1040x_20_correct_10 = sheet.cell(22,19).value.strip()
    except:
        data_1040x_20_correct_10 = ''
    try:
        data_1040x_20_original_11 = sheet.cell(23,11).value.strip()
    except:
        data_1040x_20_original_11 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_correct_11 = sheet.cell(23,19).value.strip()
    except:
        data_1040x_20_correct_11 = ''
    try:
        data_1040x_20_original_12 = sheet.cell(24,11).value.strip()
    except:
        data_1040x_20_original_12 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_correct_12 = sheet.cell(24,19).value.strip()
    except:
        data_1040x_20_correct_12 = ''
    try:
        data_1040x_20_original_13 = sheet.cell(25,11).value.strip()
    except:
        data_1040x_20_original_13 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_correct_13 = sheet.cell(25,19).value.strip()
    except:
        data_1040x_20_correct_13 = ''
    try:
        data_1040x_20_original_14 = sheet.cell(26,11).value.strip()
    except:
        data_1040x_20_original_14 = ''
    try:
        data_1040x_20_correct_14 = sheet.cell(26,19).value.strip()
    except:
        data_1040x_20_correct_14 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_original_15 = sheet.cell(27,11).value.strip()
    except:
        data_1040x_20_original_15 = ''
    try:
        data_1040x_20_correct_15 = sheet.cell(27,19).value.strip()
    except:
        data_1040x_20_correct_15 = ''
    try:
        data_1040x_20_change_15 = sheet.cell(27,15).value.strip()
    except:
        data_1040x_20_change_15 = '' 
    time.sleep(0.1)
    try:
        data_1040x_20_correct_16 = sheet.cell(28,19).value.strip()
    except:
        data_1040x_20_correct_16 = ''
    try:
        data_1040x_20_correct_17 = sheet.cell(29,19).value.strip()
    except:
        data_1040x_20_correct_17 = ''
    try:
        data_1040x_20_correct_17 = sheet.cell(29,19).value.strip()
    except:
        data_1040x_20_correct_17 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_correct_18 = sheet.cell(30,19).value.strip()
    except:
        data_1040x_20_correct_18 = ''
    try:
        data_1040x_20_correct_19 = sheet.cell(31,19).value.strip()
    except:
        data_1040x_20_correct_19 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_correct_20 = sheet.cell(32,19).value.strip()
    except:
        data_1040x_20_correct_20 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_correct_21 = sheet.cell(33,19).value.strip()
    except:
        data_1040x_20_correct_21 = ''
    try:
        data_1040x_20_correct_22 = sheet.cell(34,19).value.strip()
    except:
        data_1040x_20_correct_22 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_23 = sheet.cell(35,17).value.strip()
    except:
        data_1040x_20_23 = ''
    try:
        data_1040x_20_28 = sheet.cell(39,10).value.strip()
    except:
        data_1040x_20_28 = ''
    try:
        data_1040x_20_29 = sheet.cell(40,10).value.strip()
    except:
        data_1040x_20_29 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_30 = sheet.cell(41,10).value.strip()
    except:
        data_1040x_20_30 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_31 = sheet.cell(42,10).value.strip()
    except:
        data_1040x_20_31 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_37 = sheet.cell(44,10).value.strip()
    except:
        data_1040x_20_37 = ''
    try:
        data_1040x_20_38 = sheet.cell(45,10).value.strip()
    except:
        data_1040x_20_38 = ''
    time.sleep(0.1)
    try:
        data_1040x_20_org_sch_3_9 = sheet.cell(49,10).value.strip()
    except:
        data_1040x_20_org_sch_3_9 = ''

    data_1040x_20 = {
        "data_1040x_20_orginal_1": data_1040x_20_original_1,
        "data_1040x_20_correct_1": data_1040x_20_correct_1,
        "data_1040x_20_orginal_2": data_1040x_20_original_2,
        "data_1040x_20_correct_2": data_1040x_20_correct_2,
        "data_1040x_20_orginal_3": data_1040x_20_original_3,
        "data_1040x_20_correct_3": data_1040x_20_correct_3,
        "data_1040x_20_orginal_4a": data_1040x_20_original_4a,
        "data_1040x_20_correct_4a": data_1040x_20_correct_4a,
        "data_1040x_20_orginal_4b": data_1040x_20_original_4b,
        "data_1040x_20_correct_4b": data_1040x_20_correct_4b,
        "data_1040x_20_orginal_5": data_1040x_20_original_5,
        "data_1040x_20_correct_5": data_1040x_20_correct_5,
        "data_1040x_20_orginal_6": data_1040x_20_original_6,
        "data_1040x_20_correct_6": data_1040x_20_correct_6,
        "data_1040x_20_orginal_7": data_1040x_20_original_7,
        "data_1040x_20_correct_7": data_1040x_20_correct_7,
        "data_1040x_20_orginal_8": data_1040x_20_original_8,
        "data_1040x_20_correct_8": data_1040x_20_correct_8,
        "data_1040x_20_orginal_9": data_1040x_20_original_9,
        "data_1040x_20_correct_9": data_1040x_20_correct_9,
        "data_1040x_20_orginal_10": data_1040x_20_original_10,
        "data_1040x_20_correct_10": data_1040x_20_correct_10,
        "data_1040x_20_orginal_11": data_1040x_20_original_11,
        "data_1040x_20_correct_11": data_1040x_20_correct_11,
        "data_1040x_20_orginal_12": data_1040x_20_original_12,
        "data_1040x_20_correct_12": data_1040x_20_correct_12,
        "data_1040x_20_orginal_13": data_1040x_20_original_13,
        "data_1040x_20_correct_13": data_1040x_20_correct_13,
        "data_1040x_20_orginal_14": data_1040x_20_original_14,
        "data_1040x_20_correct_14": data_1040x_20_correct_14,
        "data_1040x_20_orginal_15": data_1040x_20_original_15,
        "data_1040x_20_correct_15": data_1040x_20_correct_15,
        "data_1040x_20_change_15": data_1040x_20_change_15,
        "data_1040x_20_correct_16": data_1040x_20_correct_16,
        "data_1040x_20_correct_17": data_1040x_20_correct_17,
        "data_1040x_20_correct_18": data_1040x_20_correct_18,
        "data_1040x_20_correct_19": data_1040x_20_correct_19,
        "data_1040x_20_correct_20": data_1040x_20_correct_20,
        "data_1040x_20_correct_21": data_1040x_20_correct_21,
        "data_1040x_20_correct_22": data_1040x_20_correct_22,
        "data_1040x_20_23": data_1040x_20_23,
        "data_1040x_20_28": data_1040x_20_28,
        "data_1040x_20_29": data_1040x_20_29,
        "data_1040x_20_30": data_1040x_20_30,
        "data_1040x_20_31": data_1040x_20_31,
        "data_1040x_20_37": data_1040x_20_37,
        "data_1040x_20_38": data_1040x_20_38,
        "data_1040x_20_org_sch_3_9": data_1040x_20_org_sch_3_9,
    }
    
    return data_1040x_20

def get_7202_21_data(sheet_name):
    sheet = gsheet_client.open(sheet_name).get_worksheet(5)

    try:
        data_7202_21_1 = sheet.cell(5,7).value.strip()
    except:
        data_7202_21_1 = '' 
    time.sleep(0.1)
    try:
        data_7202_21_2 = sheet.cell(6,7).value.strip()
    except:
        data_7202_21_2 = ''
    try:
        data_7202_21_3a = sheet.cell(7,7).value.strip()
    except:
        data_7202_21_3a = ''    
    try:
        data_7202_21_3b = sheet.cell(8,7).value.strip()
    except:
        data_7202_21_3b = ''
    time.sleep(0.1)
    try:
        data_7202_21_3c = sheet.cell(9,7).value.strip()
    except:
        data_7202_21_3c = ''
    try:
        data_7202_21_3d = sheet.cell(10,7).value.strip()
    except:
        data_7202_21_3d = ''
    time.sleep(0.1)
    try:
        data_7202_21_4a = sheet.cell(11,7).value.strip()
    except:
        data_7202_21_4a = ''
    try:
        data_7202_21_5 = sheet.cell(13,7).value.strip()
    except:
        data_7202_21_5 = ''
    time.sleep(0.1)
    try:
        data_7202_21_6a = sheet.cell(14,7).value.strip()
    except:
        data_7202_21_6a = ''
    time.sleep(0.1)
    try:
        data_7202_21_7a = sheet.cell(16,7).value.strip()
    except:
        data_7202_21_7a = ''
    time.sleep(0.1)
    try:
        data_7202_21_8 = sheet.cell(18,7).value.strip()
    except:
        data_7202_21_8 = ''
    try:
        data_7202_21_9 = sheet.cell(19,7).value.strip()
    except:
        data_7202_21_9 = ''
    time.sleep(0.1)
    try:
        data_7202_21_10 = sheet.cell(20,7).value.strip()
    except:
        data_7202_21_10 = ''
    time.sleep(0.1)
    try:
        data_7202_21_11 = sheet.cell(21,7).value.strip()
    except:
        data_7202_21_11 = ''
    try:
        data_7202_21_12 = sheet.cell(22,7).value.strip()
    except:
        data_7202_21_12 = ''
    try:
        data_7202_21_13 = sheet.cell(23,7).value.strip()
    except:
        data_7202_21_13 = ''
    try:
        data_7202_21_14 = sheet.cell(24,7).value.strip()
    except:
        data_7202_21_14 = ''
    try:
        data_7202_21_15a = sheet.cell(25,7).value.strip()
    except:
        data_7202_21_15a = ''
    time.sleep(0.1)
    try:
        data_7202_21_15b = sheet.cell(26,7).value.strip()
    except:
        data_7202_21_15b = ''
    try:
        data_7202_21_15c = sheet.cell(27,7).value.strip()
    except:
        data_7202_21_15c = ''
    try:
        data_7202_21_16a = sheet.cell(28,7).value.strip()
    except:
        data_7202_21_16a = ''
    try:
        data_7202_21_16b = sheet.cell(29,7).value.strip()
    except:
        data_7202_21_16b = ''
    time.sleep(0.1)
    try:
        data_7202_21_16c = sheet.cell(30,7).value.strip()
    except:
        data_7202_21_16c = ''
    time.sleep(0.1)
    try:
        data_7202_21_17a = sheet.cell(32,7).value.strip()
    except:
        data_7202_21_17a = ''
    try:
        data_7202_21_17b = sheet.cell(33,7).value.strip()
    except:
        data_7202_21_17b = ''
    time.sleep(0.1)
    try:
        data_7202_21_17c = sheet.cell(34,7).value.strip()
    except:
        data_7202_21_17c = ''
    time.sleep(0.1)
    try:
        data_7202_21_18 = sheet.cell(35,7).value.strip()
    except:
        data_7202_21_18 = ''
    time.sleep(0.1)
    try:
        data_7202_21_19 = sheet.cell(36,7).value.strip()
    except:
        data_7202_21_19 = ''
    try:
        data_7202_21_20a = sheet.cell(37,7).value.strip()
    except:
        data_7202_21_20a = ''
    try:
        data_7202_21_20b = sheet.cell(38,7).value.strip()
    except:
        data_7202_21_20b = ''
    try:
        data_7202_21_20c = sheet.cell(39,7).value.strip()
    except:
        data_7202_21_20c = ''
    time.sleep(0.1)
    try:
        data_7202_21_21 = sheet.cell(40,7).value.strip()
    except:
        data_7202_21_21 = ''
    try:
        data_7202_21_22 = sheet.cell(41,7).value.strip()
    except:
        data_7202_21_22 = ''
    time.sleep(0.1)
    try:
        data_7202_21_23 = sheet.cell(42,7).value.strip()
    except:
        data_7202_21_23 = ''
    try:
        data_7202_21_24 = sheet.cell(43,7).value.strip()
    except:
        data_7202_21_24 = ''
    try:
        data_7202_21_25a = sheet.cell(46,7).value.strip()
    except:
        data_7202_21_25a = ''
    try:
        data_7202_21_25b = sheet.cell(47,7).value.strip()
    except:
        data_7202_21_25b = ''
    time.sleep(0.1)
    try:
        data_7202_21_25c = sheet.cell(48,7).value.strip()
    except:
        data_7202_21_25c = ''
    try:
        data_7202_21_25d = sheet.cell(49,7).value.strip()
    except:
        data_7202_21_25d = ''
    try:
        data_7202_21_26a = sheet.cell(50,7).value.strip()
    except:
        data_7202_21_26a = ''
    time.sleep(0.1)
    try:
        data_7202_21_27 = sheet.cell(52,7).value.strip()
    except:
        data_7202_21_27 = ''
    try:
        data_7202_21_28 = sheet.cell(53,7).value.strip()
    except:
        data_7202_21_28 = ''
    try:
        data_7202_21_29 = sheet.cell(54,7).value.strip()
    except:
        data_7202_21_29 = ''
    try:
        data_7202_21_30 = sheet.cell(55,7).value.strip()
    except:
        data_7202_21_30 = ''
    time.sleep(0.1)
    try:
        data_7202_21_31a = sheet.cell(56,7).value.strip()
    except:
        data_7202_21_31a = ''
    try:
        data_7202_21_31b = sheet.cell(57,7).value.strip()
    except:
        data_7202_21_31b = ''
    time.sleep(0.1)
    try:
        data_7202_21_31c = sheet.cell(58,7).value.strip()
    except:
        data_7202_21_31c = ''
    time.sleep(0.1)
    try:
        data_7202_21_32a = sheet.cell(60,7).value.strip()
    except:
        data_7202_21_32a = ''
    try:
        data_7202_21_32b = sheet.cell(61,7).value.strip()
    except:
        data_7202_21_32b = ''
    time.sleep(0.1)
    try:
        data_7202_21_32c = sheet.cell(62,7).value.strip()
    except:
        data_7202_21_32c = ''
    time.sleep(0.1)
    try:
        data_7202_21_33 = sheet.cell(63,7).value.strip()
    except:
        data_7202_21_33 = ''
    try:
        data_7202_21_34 = sheet.cell(64,7).value.strip()
    except:
        data_7202_21_34 = ''
    time.sleep(0.1)
    try:
        data_7202_21_35 = sheet.cell(65,7).value.strip()
    except:
        data_7202_21_35 = ''
    time.sleep(0.1)
    try:
        data_7202_21_36 = sheet.cell(67,7).value.strip()
    except:
        data_7202_21_36 = ''
    try:
        data_7202_21_37 = sheet.cell(68,7).value.strip()
    except:
        data_7202_21_37 = ''
    try:
        data_7202_21_38a = sheet.cell(69,7).value.strip()
    except:
        data_7202_21_38a = ''
    try:
        data_7202_21_39 = sheet.cell(71,7).value.strip()
    except:
        data_7202_21_39 = ''
    time.sleep(0.1)
    try:
        data_7202_21_40a = sheet.cell(72,7).value.strip()
    except:
        data_7202_21_40a = ''
    try:
        data_7202_21_41a = sheet.cell(74,7).value.strip()
    except:
        data_7202_21_41a = ''
    try:
        data_7202_21_42 = sheet.cell(76,7).value.strip()
    except:
        data_7202_21_42 = ''
    time.sleep(0.1)
    try:
        data_7202_21_43 = sheet.cell(77,7).value.strip()
    except:
        data_7202_21_43 = ''
    try:
        data_7202_21_44 = sheet.cell(78, 7).value.strip()
    except:
        data_7202_21_44 = ''
    time.sleep(0.1)
    try:
        data_7202_21_45 = sheet.cell(79, 7).value.strip()
    except:
        data_7202_21_45 = ''
    time.sleep(0.1)
    try:
        data_7202_21_46 = sheet.cell(80, 7).value.strip()
    except:
        data_7202_21_46 = ''
    time.sleep(0.1)
    try:
        data_7202_21_47 = sheet.cell(81, 7).value.strip()
    except:
        data_7202_21_47 = ''
    time.sleep(0.1)
    try:
        data_7202_21_48 = sheet.cell(82, 7).value.strip()
    except:
        data_7202_21_48 = ''
    time.sleep(0.1)
    try:
        data_7202_21_49 = sheet.cell(83, 7).value.strip()
    except:
        data_7202_21_49 = ''
    time.sleep(0.1)
    try:
        data_7202_21_50 = sheet.cell(84,7).value.strip()
    except:
        data_7202_21_50 = ''
    time.sleep(0.1)
    try:
        data_7202_21_51 = sheet.cell(86, 7).value.strip()
    except:
        data_7202_21_51 = ''
    time.sleep(0.1)
    try:
        data_7202_21_52 = sheet.cell(87, 7).value.strip()
    except:
        data_7202_21_52 = ''
    try:
        data_7202_21_53 = sheet.cell(88, 7).value.strip()
    except:
        data_7202_21_53 = ''
    time.sleep(0.1)
    try:
        data_7202_21_54 = sheet.cell(89, 7).value.strip()
    except:
        data_7202_21_54 = ''
    time.sleep(0.1)
    try:
        data_7202_21_55 = sheet.cell(90, 7).value.strip()
    except:
        data_7202_21_55 = ''
    time.sleep(0.1)
    try:
        data_7202_21_56 = sheet.cell(91, 7).value.strip()
    except:
        data_7202_21_56 = ''
    time.sleep(0.1)
    try:
        data_7202_21_57 = sheet.cell(92, 7).value.strip()
    except:
        data_7202_21_57 = ''
    time.sleep(0.1)
    try:
        data_7202_21_58 = sheet.cell(93, 7).value.strip()
    except:
        data_7202_21_58 = ''
    time.sleep(0.1)
    try:
        data_7202_21_59 = sheet.cell(96, 7).value.strip()
    except:
        data_7202_21_59 = ''
    time.sleep(0.1)
    try:
        data_7202_21_60a = sheet.cell(97, 7).value.strip()
    except:
        data_7202_21_60a = ''
    time.sleep(0.1)
    try:
        data_7202_21_61 = sheet.cell(99, 7).value.strip()
    except:
        data_7202_21_61 = ''
    time.sleep(0.1)
    try:
        data_7202_21_62 = sheet.cell(100, 7).value.strip()
    except:
        data_7202_21_62 = ''
    time.sleep(0.1)
    try:
        data_7202_21_63 = sheet.cell(101, 7).value.strip()
    except:
        data_7202_21_63 = ''
    try:
        data_7202_21_64 = sheet.cell(102, 7).value.strip()
    except:
        data_7202_21_64 = ''
    time.sleep(0.1)
    try:
        data_7202_21_65 = sheet.cell(103, 7).value.strip()
    except:
        data_7202_21_65 = ''
    time.sleep(0.1)
    try:
        data_7202_21_66 = sheet.cell(105, 7).value.strip()
    except:
        data_7202_21_66 = ''
    time.sleep(0.1)
    try:
        data_7202_21_67 = sheet.cell(106, 7).value.strip()
    except:
        data_7202_21_67 = ''
    time.sleep(0.1)
    try:
        data_7202_21_68 = sheet.cell(107, 7).value.strip()
    except:
        data_7202_21_68 = ''
    time.sleep(0.1)
    try:
        data_7202_21_69 = sheet.cell(108, 7).value.strip()
    except:
        data_7202_21_69 = ''  
    try:
        data_7202_21_sch_3_13b = sheet.cell(111,8).value.strip()
    except:
        data_7202_21_sch_3_13b = ''
    time.sleep(0.1)
    try:
        data_7202_21_sch_3_13h = sheet.cell(112,8).value.strip()
    except:
        data_7202_21_sch_3_13h = ''

    data_7202_21 = {
        "data_7202_21_1": data_7202_21_1,
        "data_7202_21_2": data_7202_21_2,
        "data_7202_21_3a": data_7202_21_3a,
        "data_7202_21_3b": data_7202_21_3b,
        "data_7202_21_3c": data_7202_21_3c,
        "data_7202_21_3d": data_7202_21_3d,
        "data_7202_21_4a": data_7202_21_4a,
        "data_7202_21_5": data_7202_21_5,
        "data_7202_21_6a": data_7202_21_6a,
        "data_7202_21_7a": data_7202_21_7a,
        "data_7202_21_8": data_7202_21_8,
        "data_7202_21_9": data_7202_21_9,
        "data_7202_21_10": data_7202_21_10,
        "data_7202_21_11": data_7202_21_11,
        "data_7202_21_12": data_7202_21_12,
        "data_7202_21_13": data_7202_21_13,
        "data_7202_21_14": data_7202_21_14,
        "data_7202_21_15a": data_7202_21_15a,
        "data_7202_21_15b": data_7202_21_15b,
        "data_7202_21_15c": data_7202_21_15c,
        "data_7202_21_16a": data_7202_21_16a,
        "data_7202_21_16b": data_7202_21_16b,
        "data_7202_21_16c": data_7202_21_16c,
        "data_7202_21_17a": data_7202_21_17a,
        "data_7202_21_17b": data_7202_21_17b,
        "data_7202_21_17c": data_7202_21_17c,
        "data_7202_21_18": data_7202_21_18,
        "data_7202_21_19": data_7202_21_19,
        "data_7202_21_20a": data_7202_21_20a,
        "data_7202_21_20b": data_7202_21_20b,
        "data_7202_21_20c": data_7202_21_20c,
        "data_7202_21_21": data_7202_21_21,
        "data_7202_21_22": data_7202_21_22,
        "data_7202_21_23": data_7202_21_23,
        "data_7202_21_24": data_7202_21_24,
        "data_7202_21_25a": data_7202_21_25a,
        "data_7202_21_25b": data_7202_21_25b,
        "data_7202_21_25c": data_7202_21_25c,
        "data_7202_21_25d": data_7202_21_25d,
        "data_7202_21_26a": data_7202_21_26a,
        "data_7202_21_27": data_7202_21_27,
        "data_7202_21_28": data_7202_21_28,
        "data_7202_21_29": data_7202_21_29,
        "data_7202_21_30": data_7202_21_30,
        "data_7202_21_31a": data_7202_21_31a,
        "data_7202_21_31b": data_7202_21_31b,
        "data_7202_21_31c": data_7202_21_31c,
        "data_7202_21_32a": data_7202_21_32a,
        "data_7202_21_32b": data_7202_21_32b,
        "data_7202_21_32c": data_7202_21_32c,
        "data_7202_21_33": data_7202_21_33,
        "data_7202_21_34": data_7202_21_34,
        "data_7202_21_35": data_7202_21_35,
        "data_7202_21_36": data_7202_21_36,
        "data_7202_21_37": data_7202_21_37,
        "data_7202_21_38a": data_7202_21_38a,
        "data_7202_21_39": data_7202_21_39,
        "data_7202_21_40a": data_7202_21_40a,
        "data_7202_21_41a": data_7202_21_41a,
        "data_7202_21_42": data_7202_21_42,
        "data_7202_21_43": data_7202_21_43,
        "data_7202_21_44": data_7202_21_44,
        "data_7202_21_45": data_7202_21_45,
        "data_7202_21_46": data_7202_21_46,
        "data_7202_21_47": data_7202_21_47,
        "data_7202_21_48": data_7202_21_48,
        "data_7202_21_49": data_7202_21_49,
        "data_7202_21_50": data_7202_21_50,
        "data_7202_21_51": data_7202_21_51,
        "data_7202_21_52": data_7202_21_52,
        "data_7202_21_53": data_7202_21_53,
        "data_7202_21_54": data_7202_21_54,
        "data_7202_21_55": data_7202_21_55,
        "data_7202_21_56": data_7202_21_56,
        "data_7202_21_57": data_7202_21_57,
        "data_7202_21_58": data_7202_21_58,
        "data_7202_21_59": data_7202_21_59,
        "data_7202_21_60a": data_7202_21_60a,
        "data_7202_21_61": data_7202_21_61,
        "data_7202_21_62": data_7202_21_62,
        "data_7202_21_63": data_7202_21_63,
        "data_7202_21_64": data_7202_21_64,
        "data_7202_21_65": data_7202_21_65,
        "data_7202_21_66": data_7202_21_66,
        "data_7202_21_67": data_7202_21_67,
        "data_7202_21_68": data_7202_21_68,
        "data_7202_21_69": data_7202_21_69,
        "data_7202_21_sch_3_13b": data_7202_21_sch_3_13b,
        "data_7202_21_sch_3_13h": data_7202_21_sch_3_13h
    }

    return data_7202_21

def get_sch_3_21_data(sheet_name):
    sheet = gsheet_client.open(sheet_name).get_worksheet(6)

    try:
        data_sch_3_21_1 = sheet.cell(10,28).value.strip()
    except:
        data_sch_3_21_1 = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_2 = sheet.cell(12,28).value.strip()
    except:
        data_sch_3_21_2 = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_3 = sheet.cell(13,28).value.strip()
    except:
        data_sch_3_21_3 = ''
    try:
        data_sch_3_21_4 = sheet.cell(14,28).value.strip()
    except:
        data_sch_3_21_4 = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_5 = sheet.cell(15,28).value.strip()
    except:
        data_sch_3_21_5 = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_6a = sheet.cell(17,22).value.strip()
    except:
        data_sch_3_21_6a = ''
    try:
        data_sch_3_21_6b = sheet.cell(18,22).value.strip()
    except:
        data_sch_3_21_6b = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_6c = sheet.cell(19,22).value.strip()
    except:
        data_sch_3_21_6c = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_6d = sheet.cell(20,22).value.strip()
    except:
        data_sch_3_21_6d = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_6e = sheet.cell(21,22).value.strip()
    except:
        data_sch_3_21_6e = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_6f = sheet.cell(22,22).value.strip()
    except:
        data_sch_3_21_6f = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_6g = sheet.cell(23,22).value.strip()
    except:
        data_sch_3_21_6g = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_6h = sheet.cell(24,22).value.strip()
    except:
        data_sch_3_21_6h = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_6i = sheet.cell(25,22).value.strip()
    except:
        data_sch_3_21_6i = ''
    try:
        data_sch_3_21_6j = sheet.cell(26,22).value.strip()
    except:
        data_sch_3_21_6j = ''
    try:
        data_sch_3_21_6k = sheet.cell(27,22).value.strip()
    except:
        data_sch_3_21_6k = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_6l = sheet.cell(28,22).value.strip()
    except:
        data_sch_3_21_6l = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_6z = sheet.cell(30,22).value.strip()
    except:
        data_sch_3_21_6z = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_7 = sheet.cell(31,28).value.strip()
    except:
        data_sch_3_21_7 = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_8 = sheet.cell(33,28).value.strip()
    except:
        data_sch_3_21_8 = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_9 = sheet.cell(38,28).value.strip()
    except:
        data_sch_3_21_9 = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_10 = sheet.cell(39,28).value.strip()
    except:
        data_sch_3_21_10 = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_11 = sheet.cell(40,28).value.strip()
    except:
        data_sch_3_21_11 = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_12 = sheet.cell(41,28).value.strip()
    except:
        data_sch_3_21_12 = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_13a = sheet.cell(43,22).value.strip()
    except:
        data_sch_3_21_13a = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_13b = sheet.cell(45,22).value.strip()
    except:
        data_sch_3_21_13b = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_13c = sheet.cell(46,22).value.strip()
    except:
        data_sch_3_21_13c = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_13d = sheet.cell(48,22).value.strip()
    except:
        data_sch_3_21_13d = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_13e = sheet.cell(49,22).value.strip()
    except:
        data_sch_3_21_13e = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_13f = sheet.cell(50,22).value.strip()
    except:
        data_sch_3_21_13f = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_13g = sheet.cell(52,22).value.strip()
    except:
        data_sch_3_21_13g = ''
    try:
        data_sch_3_21_13h = sheet.cell(54,22).value.strip()
    except:
        data_sch_3_21_13h = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_13z = sheet.cell(56,22).value.strip()
    except:
        data_sch_3_21_13z = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_14 = sheet.cell(57,28).value.strip()
    except:
        data_sch_3_21_14 = ''
    time.sleep(0.1)
    try:
        data_sch_3_21_15 = sheet.cell(59,28).value.strip()
    except:
        data_sch_3_21_15 = ''

    data_sch_3_21 = {
        "data_sch_3_21_1": data_sch_3_21_1,
        "data_sch_3_21_2": data_sch_3_21_2,
        "data_sch_3_21_3": data_sch_3_21_3,
        "data_sch_3_21_4": data_sch_3_21_4,
        "data_sch_3_21_5": data_sch_3_21_5,
        "data_sch_3_21_6a": data_sch_3_21_6a,
        "data_sch_3_21_6b": data_sch_3_21_6b,
        "data_sch_3_21_6c": data_sch_3_21_6c,
        "data_sch_3_21_6d": data_sch_3_21_6d,
        "data_sch_3_21_6e": data_sch_3_21_6e,
        "data_sch_3_21_6f": data_sch_3_21_6f,
        "data_sch_3_21_6g": data_sch_3_21_6g,
        "data_sch_3_21_6h": data_sch_3_21_6h,
        "data_sch_3_21_6i": data_sch_3_21_6i,
        "data_sch_3_21_6j": data_sch_3_21_6j,
        "data_sch_3_21_6k": data_sch_3_21_6k,
        "data_sch_3_21_6l": data_sch_3_21_6l,
        "data_sch_3_21_6z": data_sch_3_21_6z,
        "data_sch_3_21_7": data_sch_3_21_7,
        "data_sch_3_21_8": data_sch_3_21_8,
        "data_sch_3_21_9": data_sch_3_21_9,
        "data_sch_3_21_10": data_sch_3_21_10,
        "data_sch_3_21_11": data_sch_3_21_11,
        "data_sch_3_21_12": data_sch_3_21_12,
        "data_sch_3_21_13a": data_sch_3_21_13a,
        "data_sch_3_21_13b": data_sch_3_21_13b,
        "data_sch_3_21_13c": data_sch_3_21_13c,
        "data_sch_3_21_13d": data_sch_3_21_13d,
        "data_sch_3_21_13e": data_sch_3_21_13e,
        "data_sch_3_21_13f": data_sch_3_21_13f,
        "data_sch_3_21_13g": data_sch_3_21_13g,
        "data_sch_3_21_13h": data_sch_3_21_13h,
        "data_sch_3_21_13z": data_sch_3_21_13z,
        "data_sch_3_21_14": data_sch_3_21_14,
        "data_sch_3_21_15": data_sch_3_21_15
    }

    return data_sch_3_21

def get_1040_21_data(sheet_name):
    sheet = gsheet_client.open(sheet_name).get_worksheet(7)

    try:
        data_1040_21_1 = sheet.cell(35,28).value.strip()
    except:
        data_1040_21_1 = ''
    time.sleep(0.1)
    try:
        data_1040_21_7 = sheet.cell(41,28).value.strip()
    except:
        data_1040_21_7 = ''
    time.sleep(0.1)
    try:
        data_1040_21_8 = sheet.cell(42,28).value.strip()
    except:
        data_1040_21_8 = ''
    time.sleep(0.1)
    try:
        data_1040_21_9 = sheet.cell(43,28).value.strip()
    except:
        data_1040_21_9 = ''
    time.sleep(0.1)
    try:
        data_1040_21_10 = sheet.cell(44,28).value.strip()
    except:
        data_1040_21_10 = ''
    time.sleep(0.1)
    try:
        data_1040_21_11 = sheet.cell(45,28).value.strip()
    except:
        data_1040_21_11 = ''
    time.sleep(0.1)
    try:
        data_1040_21_12c = sheet.cell(48,28).value.strip()
    except:
        data_1040_21_12c = ''
    time.sleep(0.1)
    try:
        data_1040_21_13 = sheet.cell(49,28).value.strip()
    except:
        data_1040_21_13 = ''
    time.sleep(0.1)
    try:
        data_1040_21_14 = sheet.cell(50,28).value.strip()
    except:
        data_1040_21_14 = ''
    time.sleep(0.1)
    try:
        data_1040_21_15 = sheet.cell(51,28).value.strip()
    except:
        data_1040_21_15 = ''
    time.sleep(0.1)
    try:
        data_1040_21_16 = sheet.cell(54,28).value.strip()
    except:
        data_1040_21_16 = ''
    time.sleep(0.1)
    try:
        data_1040_21_17 = sheet.cell(55,28).value.strip()
    except:
        data_1040_21_17 = ''
    time.sleep(0.1)
    try:
        data_1040_21_18 = sheet.cell(56,28).value.strip()
    except:
        data_1040_21_18 = ''
    time.sleep(0.1)
    try:
        data_1040_21_19 = sheet.cell(57,28).value.strip()
    except:
        data_1040_21_19 = ''
    time.sleep(0.1)
    try:
        data_1040_21_20 = sheet.cell(58,28).value.strip()
    except:
        data_1040_21_20 = ''
    time.sleep(0.1)
    try:
        data_1040_21_21 = sheet.cell(59,28).value.strip()
    except:
        data_1040_21_21 = ''
    time.sleep(0.1)
    try:
        data_1040_21_22 = sheet.cell(60,28).value.strip()
    except:
        data_1040_21_22 = ''
    time.sleep(0.1)
    try:
        data_1040_21_23 = sheet.cell(61,28).value.strip()
    except:
        data_1040_21_23 = ''
    time.sleep(0.1)
    try:
        data_1040_21_24 = sheet.cell(62,28).value.strip()
    except:
        data_1040_21_24 = ''
    time.sleep(0.1)
    try:
        data_1040_21_25d = sheet.cell(67,28).value.strip()
    except:
        data_1040_21_25d = ''
    time.sleep(0.1)
    try:
        data_1040_21_26 = sheet.cell(68,28).value.strip()
    except:
        data_1040_21_26 = ''
    time.sleep(0.1)
    try:
        data_1040_21_32 = sheet.cell(79,28).value.strip()
    except:
        data_1040_21_32 = ''
    time.sleep(0.1)
    try:
        data_1040_21_33 = sheet.cell(80,28).value.strip()
    except:
        data_1040_21_33 = ''
    time.sleep(0.1)
    try:
        data_1040_21_34 = sheet.cell(81,28).value.strip()
    except:
        data_1040_21_34 = ''
    time.sleep(0.1)
    try:
        data_1040_21_35a = sheet.cell(82,28).value.strip()
    except:
        data_1040_21_35a = ''
    time.sleep(0.1)
    try:
        data_1040_21_37 = sheet.cell(86,28).value.strip()
    except:
        data_1040_21_37 = ''
    time.sleep(0.1)
    try:
        data_1040_21_36 = sheet.cell(85,21).value.strip()
    except:
        data_1040_21_36 = ''
    time.sleep(0.1)
    try:
        data_1040_21_38 = sheet.cell(87,21).value.strip()
    except:
        data_1040_21_38 = ''
    time.sleep(0.1)
    try:
        data_1040_21_27a = sheet.cell(69,24).value.strip()
    except:
        data_1040_21_27a = ''
    time.sleep(0.1)
    try:
        data_1040_21_28 = sheet.cell(75,24).value.strip()
    except:
        data_1040_21_28 = ''
    time.sleep(0.1)
    try:
        data_1040_21_29 = sheet.cell(76,28).value.strip()
    except:
        data_1040_21_29 = ''
    time.sleep(0.1)
    try:
        data_1040_21_30 = sheet.cell(77,28).value.strip()
    except:
        data_1040_21_30 = ''
    time.sleep(0.1)
    try:
        data_1040_21_31 = sheet.cell(78,28).value.strip()
    except:
        data_1040_21_31 = ''
    time.sleep(0.1)
    try:
        data_1040_21_27b = sheet.cell(73,28).value.strip()
    except:
        data_1040_21_27b = ''
    time.sleep(0.1)
    try:
        data_1040_21_27c = sheet.cell(74,28).value.strip()
    except:
        data_1040_21_27c = ''
    time.sleep(0.1)
    try:
        data_1040_21_25a = sheet.cell(64,24).value.strip()
    except:
        data_1040_21_25a = ''
    try:
        data_1040_21_25b = sheet.cell(65,24).value.strip()
    except:
        data_1040_21_25b = ''
    time.sleep(0.1)
    try:
        data_1040_21_25c = sheet.cell(66,24).value.strip()
    except:
        data_1040_21_25c = ''
    time.sleep(0.1)
    try:
        data_1040_21_12a = sheet.cell(46,24).value.strip()
    except:
        data_1040_21_12a = ''
    time.sleep(0.1)
    try:
        data_1040_21_12b = sheet.cell(47,24).value.strip()
    except:
        data_1040_21_12b = ''
    time.sleep(0.1)
    try:
        data_1040_21_2a = sheet.cell(36,13).value.strip()
    except:
        data_1040_21_2a = ''
    time.sleep(0.1)
    try:
        data_1040_21_3a = sheet.cell(37,13).value.strip()
    except:
        data_1040_21_3a = ''
    time.sleep(0.1)
    try:
        data_1040_21_4a = sheet.cell(38,13).value.strip()
    except:
        data_1040_21_4a = ''
    time.sleep(0.1)
    try:
        data_1040_21_5a = sheet.cell(39,13).value.strip()
    except:
        data_1040_21_5a = ''
    time.sleep(0.1)
    try:
        data_1040_21_6a = sheet.cell(40,13).value.strip()
    except:
        data_1040_21_6a = ''

    data_1040_21 = {
        "data_1040_21_1": data_1040_21_1,
        "data_1040_21_2a": data_1040_21_2a,
        "data_1040_21_3a": data_1040_21_3a,
        "data_1040_21_4a": data_1040_21_4a,
        "data_1040_21_5a": data_1040_21_5a,
        "data_1040_21_6a": data_1040_21_6a,
        "data_1040_21_7": data_1040_21_7,
        "data_1040_21_8": data_1040_21_8,
        "data_1040_21_9": data_1040_21_9,
        "data_1040_21_10": data_1040_21_10,
        "data_1040_21_11": data_1040_21_11,
        "data_1040_21_12a": data_1040_21_12a,
        "data_1040_21_12b": data_1040_21_12b,
        "data_1040_21_12c": data_1040_21_12c,
        "data_1040_21_13": data_1040_21_13,
        "data_1040_21_14": data_1040_21_14,
        "data_1040_21_15": data_1040_21_15,
        "data_1040_21_16": data_1040_21_16,
        "data_1040_21_17": data_1040_21_17,
        "data_1040_21_18": data_1040_21_18,
        "data_1040_21_19": data_1040_21_19,
        "data_1040_21_20": data_1040_21_20,
        "data_1040_21_21": data_1040_21_21,
        "data_1040_21_22": data_1040_21_22,
        "data_1040_21_23": data_1040_21_23,
        "data_1040_21_24": data_1040_21_24,
        "data_1040_21_25a": data_1040_21_25a,
        "data_1040_21_25b": data_1040_21_25b,
        "data_1040_21_25c": data_1040_21_25c,
        "data_1040_21_25d": data_1040_21_25d,
        "data_1040_21_26": data_1040_21_26,
        "data_1040_21_27a": data_1040_21_27a,
        "data_1040_21_27b": data_1040_21_27b,
        "data_1040_21_27c": data_1040_21_27c,
        "data_1040_21_28": data_1040_21_28,
        "data_1040_21_29": data_1040_21_29,
        "data_1040_21_30": data_1040_21_30,
        "data_1040_21_31": data_1040_21_31,
        "data_1040_21_32": data_1040_21_32,
        "data_1040_21_33": data_1040_21_33,
        "data_1040_21_34": data_1040_21_34,
        "data_1040_21_35a": data_1040_21_35a,
        "data_1040_21_36": data_1040_21_36,
        "data_1040_21_37": data_1040_21_37,
        "data_1040_21_38": data_1040_21_38
    }
    
    return data_1040_21

def get_1040x_21_data(sheet_name):
    sheet = gsheet_client.open(sheet_name).get_worksheet(8)
    try:
        data_1040x_21_original_1 = sheet.cell(12,11).value.strip()
    except:
        data_1040x_21_original_1 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_1 = sheet.cell(12,19).value.strip()
    except:
        data_1040x_21_correct_1 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_original_2 = sheet.cell(13,11).value.strip()
    except:
        data_1040x_21_original_2 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_2 = sheet.cell(13,19).value.strip()
    except:
        data_1040x_21_correct_2 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_original_3 = sheet.cell(14,11).value.strip()
    except:
        data_1040x_21_original_3 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_3 = sheet.cell(14,19).value.strip()
    except:
        data_1040x_21_correct_3 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_original_4a = sheet.cell(15,11).value.strip()
    except:
        data_1040x_21_original_4a = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_4a = sheet.cell(15,19).value.strip()
    except:
        data_1040x_21_correct_4a = ''
    time.sleep(0.1)
    try:
        data_1040x_21_original_4b = sheet.cell(16,11).value.strip()
    except:
        data_1040x_21_original_4b = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_4b = sheet.cell(16,19).value.strip()
    except:
        data_1040x_21_correct_4b = ''
    time.sleep(0.1)
    try:
        data_1040x_21_original_5 = sheet.cell(17,11).value.strip()
    except:
        data_1040x_21_original_5 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_5 = sheet.cell(17,19).value.strip()
    except:
        data_1040x_21_correct_5 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_original_6 = sheet.cell(18,11).value.strip()
    except:
        data_1040x_21_original_6 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_6 = sheet.cell(18,19).value.strip()
    except:
        data_1040x_21_correct_6 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_original_7  = sheet.cell(19,11).value.strip()
    except:
        data_1040x_21_original_7  = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_7  = sheet.cell(19,19).value.strip()
    except:
        data_1040x_21_correct_7  = ''
    time.sleep(0.1)
    try:
        data_1040x_21_original_8 = sheet.cell(20,11).value.strip()
    except:
        data_1040x_21_original_8 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_8 = sheet.cell(20,19).value.strip()
    except:
        data_1040x_21_correct_8 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_original_9 = sheet.cell(21,11).value.strip()
    except:
        data_1040x_21_original_9 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_9 = sheet.cell(21,19).value.strip()
    except:
        data_1040x_21_correct_9 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_original_10 = sheet.cell(22,11).value.strip()
    except:
        data_1040x_21_original_10 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_10 = sheet.cell(22,19).value.strip()
    except:
        data_1040x_21_correct_10 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_original_11 = sheet.cell(23,11).value.strip()
    except:
        data_1040x_21_original_11 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_11 = sheet.cell(23,19).value.strip()
    except:
        data_1040x_21_correct_11 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_original_12 = sheet.cell(24,11).value.strip()
    except:
        data_1040x_21_original_12 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_12 = sheet.cell(24,19).value.strip()
    except:
        data_1040x_21_correct_12 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_original_13 = sheet.cell(25,11).value.strip()
    except:
        data_1040x_21_original_13 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_13 = sheet.cell(25,19).value.strip()
    except:
        data_1040x_21_correct_13 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_original_14 = sheet.cell(26,11).value.strip()
    except:
        data_1040x_21_original_14 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_14 = sheet.cell(26,19).value.strip()
    except:
        data_1040x_21_correct_14 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_original_15 = sheet.cell(27,11).value.strip()
    except:
        data_1040x_21_original_15 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_15 = sheet.cell(27,19).value.strip()
    except:
        data_1040x_21_correct_15 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_change_15 = sheet.cell(27,15).value.strip()
    except:
        data_1040x_21_change_15 = '' 
    time.sleep(0.1)
    try:
        data_1040x_21_correct_17 = sheet.cell(29,19).value.strip()
    except:
        data_1040x_21_correct_17 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_17 = sheet.cell(29,19).value.strip()
    except:
        data_1040x_21_correct_17 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_18 = sheet.cell(30,19).value.strip()
    except:
        data_1040x_21_correct_18 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_19 = sheet.cell(31,19).value.strip()
    except:
        data_1040x_21_correct_19 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_20 = sheet.cell(32,19).value.strip()
    except:
        data_1040x_21_correct_20 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_21 = sheet.cell(33,19).value.strip()
    except:
        data_1040x_21_correct_21 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_correct_22 = sheet.cell(34,19).value.strip()
    except:
        data_1040x_21_correct_22 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_23 = sheet.cell(35,17).value.strip()
    except:
        data_1040x_21_23 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_28 = sheet.cell(39,10).value.strip()
    except:
        data_1040x_21_28 = ''
    try:
        data_1040x_21_29 = sheet.cell(40,10).value.strip()
    except:
        data_1040x_21_29 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_30 = sheet.cell(41,10).value.strip()
    except:
        data_1040x_21_30 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_31 = sheet.cell(42,10).value.strip()
    except:
        data_1040x_21_31 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_37 = sheet.cell(44,10).value.strip()
    except:
        data_1040x_21_37 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_38 = sheet.cell(45,10).value.strip()
    except:
        data_1040x_21_38 = ''
    time.sleep(0.1)
    try:
        data_1040x_21_org_sch_3_10 = sheet.cell(49,10).value.strip()
    except:
        data_1040x_21_org_sch_3_10 = ''

    data_1040x_21 = {
        "data_1040x_21_original_1": data_1040x_21_original_1,
        "data_1040x_21_correct_1": data_1040x_21_correct_1,
        "data_1040x_21_original_2": data_1040x_21_original_2,
        "data_1040x_21_correct_2": data_1040x_21_correct_2,
        "data_1040x_21_original_3": data_1040x_21_original_3,
        "data_1040x_21_correct_3": data_1040x_21_correct_3,
        "data_1040x_21_original_4a": data_1040x_21_original_4a,
        "data_1040x_21_correct_4a": data_1040x_21_correct_4a,
        "data_1040x_21_original_4b": data_1040x_21_original_4b,
        "data_1040x_21_correct_4b": data_1040x_21_correct_4b,
        "data_1040x_21_original_5": data_1040x_21_original_5,
        "data_1040x_21_correct_5": data_1040x_21_correct_5,
        "data_1040x_21_original_6": data_1040x_21_original_6,
        "data_1040x_21_correct_6": data_1040x_21_correct_6,
        "data_1040x_21_original_7": data_1040x_21_original_7,
        "data_1040x_21_correct_7": data_1040x_21_correct_7,
        "data_1040x_21_original_8": data_1040x_21_original_8,
        "data_1040x_21_correct_8": data_1040x_21_correct_8,
        "data_1040x_21_original_9": data_1040x_21_original_9,
        "data_1040x_21_correct_9": data_1040x_21_correct_9,
        "data_1040x_21_original_10": data_1040x_21_original_10,
        "data_1040x_21_correct_10": data_1040x_21_correct_10,
        "data_1040x_21_original_11": data_1040x_21_original_11,
        "data_1040x_21_correct_11": data_1040x_21_correct_11,
        "data_1040x_21_original_12": data_1040x_21_original_12,
        "data_1040x_21_correct_12": data_1040x_21_correct_12,
        "data_1040x_21_original_13": data_1040x_21_original_13,
        "data_1040x_21_correct_13": data_1040x_21_correct_13,
        "data_1040x_21_original_14": data_1040x_21_original_14,
        "data_1040x_21_correct_14": data_1040x_21_correct_14,
        "data_1040x_21_original_15": data_1040x_21_original_15,
        "data_1040x_21_correct_15": data_1040x_21_correct_15,
        "data_1040x_21_change_15": data_1040x_21_change_15,
        "data_1040x_21_correct_17": data_1040x_21_correct_17,
        "data_1040x_21_correct_18": data_1040x_21_correct_18,
        "data_1040x_21_correct_19": data_1040x_21_correct_19,
        "data_1040x_21_correct_20": data_1040x_21_correct_20,
        "data_1040x_21_correct_21": data_1040x_21_correct_21,
        "data_1040x_21_correct_22": data_1040x_21_correct_22,
        "data_1040x_21_23": data_1040x_21_23,
        "data_1040x_21_28": data_1040x_21_28,
        "data_1040x_21_29": data_1040x_21_29,
        "data_1040x_21_30": data_1040x_21_30,
        "data_1040x_21_31": data_1040x_21_31,
        "data_1040x_21_37": data_1040x_21_37,
        "data_1040x_21_38": data_1040x_21_38,
        "data_1040x_21_org_sch_3_10": data_1040x_21_org_sch_3_10
    }

    return data_1040x_21

