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
            '2019': data_2019_reca_list,
            '2020': data_2020_reca_list,
            '2021': data_2021_reca_list
        })
        print(extracted_data)

    return extracted_data



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
        "data_7202_20_total_credit": Total_2020_Credit,
        "twenty_7202_20_Line_6": twenty_7202_20_Line_6,
        "twenty_7202_20_Line_4c_result": twenty_7202_20_Line_4c_result,
        "twenty_7202_20_Line_4c": twenty_7202_20_Line_4c,
        "twenty_7202_20_Line_5a": twenty_7202_20_Line_5a,
        "twenty_7202_20_Line_5b_result": twenty_7202_20_Line_5b_result,
        "twenty_7202_20_Line_5b": twenty_7202_20_Line_5b,
        "twenty_7202_20_Line_6_result": twenty_7202_20_Line_6_result,
        "twenty_7202_20_Line_6": twenty_7202_20_Line_6
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
    data_7202 = get_7202_20_data(data_variables)
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
    twenty1040_19 = int(instructions_data['twenty_child_and_other_dependent_credit_per_computer'])
    twenty1040_20 = int(sch_3_data['data_sch_3_20_7']) if 'data_sch_3_20_7' in sch_3_data else 0
    twenty1040_21 = twenty1040_19 + twenty1040_20
    # Assigns the result of the formula to twenty1040_22
    # twenty1040_22 = max(twenty1040_18 - twenty1040_21, 0)
    twenty1040_22 = 0
    if (twenty1040_18 - twenty1040_21) < 0:
        twenty1040_22 = 0
    else:
        twenty1040_22 = twenty1040_18 - twenty1040_21

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

    # =IF(AB77-'2020 7202'!AJ49<=0,"N/A",AB77-'2020 7202'!AJ49)
    # this is the right varibale on 34
    twenty1040_37b = 0
    if twenty1040_37b - data_7202['data_7202_20_total_credit'] <= 0:
        twenty1040_37b = "N/A"
    else:
        twenty1040_37b = twenty1040_37b - data_7202['data_7202_20_total_credit']

    # this is on the right of 37 
    twenty1040_34b = 0
    if twenty1040_37b == "N/A":
        twenty1040_34b = abs(twenty1040_24 - twenty1040_33 + data_7202['data_7202_20_total_credit'] + twenty1040_38)
    else:
        twenty1040_34b = 0   

    print(twenty1040_34b)
    print(twenty1040_37b)

    #print(twenty1040_18)
    #print(twenty1040_19)
    #print(twenty1040_20)
    #print(twenty1040_21)
    #print(twenty1040_22)
    #print(twenty1040_23)
    #print(twenty1040_24)
    #print(twenty1040_32)
    #print(twenty1040_33)
    #print(twenty1040_34)
    #print(twenty1040_35a)
    # print("37b",  twenty1040_37b)
    # print("34b",  twenty1040_34b)
    # print(twenty1040_23)     
    # print(twenty1040_24)
    # print(twenty1040_33)
    # print(data_7202['data_7202_20_total_credit'])
    # print(twenty1040_38)

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
        "data_1040_20_34b": twenty1040_34b,
        "data_1040_20_35a": twenty1040_35a,
        "data_1040_20_37": twenty1040_37,
        "data_1040_20_37b": twenty1040_37b,
        "data_1040_20_38": twenty1040_38,
    }

    return data_1040_20

def get_1040x_20_data(data_variables):
    #1040X Extra Data Variables
    data_1040_20 = get_1040_20_data(data_variables)
    data_7202 = get_7202_20_data(data_variables)
    data_sch_3 = get_sch_3_20_data(data_variables)
    
    Orig_1040_28 = data_1040_20['data_1040_20_28']
    Orig_1040_29 = data_1040_20['data_1040_20_29']
    Orig_1040_30 = data_1040_20['data_1040_20_30']
    Orig_1040_31 = data_sch_3['data_sch_3_20_13']
    Orig_1040_37 = 0 if data_1040_20['data_1040_20_37'] == 0 else data_1040_20['data_1040_20_37']
    Orig_1040_38 = 0 if data_1040_20['data_1040_20_37'] <= 0 else data_1040_20['data_1040_20_38']

    twenty_1040_11a = data_1040_20['data_1040_20_24']
    twenty_1040_11b = twenty_1040_11a
    twenty_1040_12a = data_1040_20['data_1040_20_25d']
    twenty_1040_12b = twenty_1040_12a
    twenty_1040_13a = data_1040_20['data_1040_20_26']
    twenty_1040_13b = twenty_1040_13a
    twenty_1040_14a = data_1040_20['data_1040_20_27']
    twenty_1040_14b = twenty_1040_14a
    twenty_1040_15a = Orig_1040_28 + Orig_1040_29 + Orig_1040_30
    twenty_1040_15b = Orig_1040_31
    twenty_1040_15c = twenty_1040_15a + twenty_1040_15b
    twenty_1040_16 = 0 if Orig_1040_37 - Orig_1040_38 <= 0 else Orig_1040_37 - Orig_1040_38
    twenty_1040_17 = twenty_1040_12b + twenty_1040_13b + twenty_1040_14b + twenty_1040_15c + twenty_1040_16
    #2020 1040'!AI77 is on the right side of 34 hence why 34b
    # =IF('2020 1040'!AI77="N/A",0,'2020 1040'!AI77)
    twenty_1040_18 = 0 if data_1040_20['data_1040_20_34'] - data_7202['data_7202_20_total_credit'] <= 0 else data_1040_20['data_1040_20_34'] - data_7202['data_7202_20_total_credit']

    # =S29-S30
    twenty_1040_19 = twenty_1040_17 - twenty_1040_18

    #=IF(S23>S31,S23-S31,0)
    twenty_1040_20 = twenty_1040_11b - twenty_1040_19 if twenty_1040_11b > twenty_1040_19 else 0

    twenty_1040_21 = twenty_1040_19 - twenty_1040_11b if twenty_1040_11b < twenty_1040_19 else 0
    twenty_1040_22 = twenty_1040_21 if twenty_1040_21 > 0 else 0


    cal_check_20 = False
    if twenty_1040_15b == twenty_1040_21 and twenty_1040_15b  == twenty_1040_22:
        cal_check_20 = True
    else:
        pass
        
    data_1040x_20 = {
        "data_1040x_20_orginal_1": '',
        "data_1040x_20_correct_1": '',
        "data_1040x_20_orginal_2": '',
        "data_1040x_20_correct_2": '',
        "data_1040x_20_orginal_3": '',
        "data_1040x_20_correct_3": '',
        "data_1040x_20_orginal_4a": '',
        "data_1040x_20_correct_4a": '',
        "data_1040x_20_orginal_4b": '',
        "data_1040x_20_correct_4b": '',
        "data_1040x_20_orginal_5": '',
        "data_1040x_20_correct_5": '',
        "data_1040x_20_orginal_6": '',
        "data_1040x_20_correct_6": '',
        "data_1040x_20_orginal_7": '',
        "data_1040x_20_correct_7": '',
        "data_1040x_20_orginal_8": '',
        "data_1040x_20_correct_8": '',
        "data_1040x_20_orginal_9": '',
        "data_1040x_20_correct_9": '',
        "data_1040x_20_orginal_10": '',
        "data_1040x_20_correct_10": '',
        "data_1040x_20_orginal_11": twenty_1040_11a,
        "data_1040x_20_correct_11": twenty_1040_11b,
        "data_1040x_20_orginal_12": twenty_1040_12a,
        "data_1040x_20_correct_12": twenty_1040_12b,
        "data_1040x_20_orginal_13": twenty_1040_13a,
        "data_1040x_20_correct_13": twenty_1040_13b,
        "data_1040x_20_orginal_14": twenty_1040_14a,
        "data_1040x_20_correct_14": twenty_1040_14b,
        "data_1040x_20_orginal_15": twenty_1040_15a,
        "data_1040x_20_correct_15": twenty_1040_15c,
        "data_1040x_20_change_15": twenty_1040_15b,
        "data_1040x_20_correct_16": twenty_1040_16,
        "data_1040x_20_correct_17": twenty_1040_17,
        "data_1040x_20_correct_18": twenty_1040_18,
        "data_1040x_20_correct_19": twenty_1040_19,
        "data_1040x_20_correct_20": twenty_1040_20,
        "data_1040x_20_correct_21": twenty_1040_21,
        "data_1040x_20_correct_22": twenty_1040_22,
        "data_1040x_20_23": '',
        "data_1040x_20_28": Orig_1040_28,
        "data_1040x_20_29": Orig_1040_29,
        "data_1040x_20_30": Orig_1040_30,
        "data_1040x_20_31": Orig_1040_31,
        "data_1040x_20_37": Orig_1040_37,
        "data_1040x_20_38": Orig_1040_38,
        "data_1040x_20_org_sch_3_9": '',
        "cal_check_20": cal_check_20
    }

    return data_1040x_20

def combine_fields(data_1040_20,data_1040x_20,data_7202_20,data_sch_3_20):

    pdf_fields_1040_20 = {
        "data_1040_20_1": f"0;topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_28[0]",
        "data_1040_20_7": f"0;topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_39[0]",
        "data_1040_20_8": f"0;topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_40[0]",
        "data_1040_20_9": f"0;topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_41[0]",
        "data_1040_20_11": f"0;topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_45[0]",
        "data_1040_20_12": f"0;topmostSubform[0].Page1[0].f1_46[0]",
        "data_1040_20_13": f"0;topmostSubform[0].Page1[0].f1_47[0]",
        "data_1040_20_14": f"0;topmostSubform[0].Page1[0].f1_48[0]",
        "data_1040_20_15": f"0;topmostSubform[0].Page1[0].f1_49[0]",
        "data_1040_20_16": f"1;topmostSubform[0].Page2[0].f2_02[0]",
        "data_1040_20_17": f"1;topmostSubform[0].Page2[0].f2_03[0]",
        "data_1040_20_18": f"1;topmostSubform[0].Page2[0].f2_04[0]",
        "data_1040_20_19": f"1;topmostSubform[0].Page2[0].f2_05[0]",
        "data_1040_20_20": f"1;topmostSubform[0].Page2[0].f2_06[0]",
        "data_1040_20_21": f"1;topmostSubform[0].Page2[0].f2_07[0]",
        "data_1040_20_22": f"1;topmostSubform[0].Page2[0].f2_08[0]",
        "data_1040_20_23": f"1;topmostSubform[0].Page2[0].f2_09[0]",
        "data_1040_20_24": f"1;topmostSubform[0].Page2[0].f2_10[0]",
        "data_1040_20_26": f"1;topmostSubform[0].Page2[0].Lines26-27_ReadOrder[0].f2_15[0]",
        "data_1040_20_27": f"1;topmostSubform[0].Page2[0].Lines27-32_ReadOrder[0].f2_16[0]",
        "data_1040_20_28": f"1;topmostSubform[0].Page2[0].Lines27-32_ReadOrder[0].f2_17[0]",
        "data_1040_20_29": f"1;topmostSubform[0].Page2[0].Lines27-32_ReadOrder[0].f2_18[0]",
        "data_1040_20_2a": f"0;topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_29[0]",
        "data_1040_20_2b": f"0;topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_30[0]",
        "data_1040_20_30": f"1;topmostSubform[0].Page2[0].Lines27-32_ReadOrder[0].f2_19[0]",
        "data_1040_20_31": f"1;topmostSubform[0].Page2[0].Lines27-32_ReadOrder[0].f2_20[0]",
        "data_1040_20_32": f"1;topmostSubform[0].Page2[0].Line32-33_ReadOrder[0].f2_21[0]",
        "data_1040_20_33": f"1;topmostSubform[0].Page2[0].f2_22[0]",
        "data_1040_20_34": f"1;topmostSubform[0].Page2[0].f2_23[0]",
        "data_1040_20_36": f"1;topmostSubform[0].Page2[0].f2_27[0]",
        "data_1040_20_37": f"1;topmostSubform[0].Page2[0].f2_28[0]",
        "data_1040_20_38": f"1;topmostSubform[0].Page2[0].number38[0]",
        "data_1040_20_3a": f"0;topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_31[0]",
        "data_1040_20_3b": f"0;topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_32[0]",
        "data_1040_20_4a": f"0;topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_33[0]",
        "data_1040_20_4b": f"0;topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_34[0]",
        "data_1040_20_5a": f"0;topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_35[0]",
        "data_1040_20_5b": f"0;topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_36[0]",
        "data_1040_20_6a": f"0;topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_37[0]",
        "data_1040_20_6b": f"0;topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_38[0]",
        "data_1040_20_10a": f"0;topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].Line10-12_ReadOrder[0].f1_42[0]",
        "data_1040_20_10b": f"0;topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].Line10-12_ReadOrder[0].f1_42[0]",
        "data_1040_20_10c": f"0;topmostSubform[0].Page1[0].Lines1-11_ReadOrder[0].f1_44[0]",
        "data_1040_20_25a": f"1;topmostSubform[0].Page2[0].Line25_ReadOrder[0].f2_11[0]",
        "data_1040_20_25b": f"1;topmostSubform[0].Page2[0].Line25_ReadOrder[0].f2_12[0]",
        "data_1040_20_25c": f"1;topmostSubform[0].Page2[0].Line25_ReadOrder[0].f2_13[0]",
        "data_1040_20_25d": f"1;topmostSubform[0].Page2[0].Lines26-27_ReadOrder[0].f2_14[0]",
        "data_1040_20_35a": f"1;topmostSubform[0].Page2[0].f2_24[0]",
        "data_1040_20_firstName": f"0;topmostSubform[0].Page1[0].firstName1040[0]",
        "data_1040_20_lastName": f"0;topmostSubform[0].Page1[0].lastName1040[0]"
    }

    pdf_fields_1040x_20 = {
        "data_1040x_20_orginal_1": f"2;topmostSubform[0].Page1[0].Table_IncomeDeductions[0].Line1[0].f1_17[0]",
        "data_1040x_20_correct_1": f"2;topmostSubform[0].Page1[0].Table_IncomeDeductions[0].Line1[0].f1_19[0]",
        "data_1040x_20_orginal_2": f"2;topmostSubform[0].Page1[0].Table_IncomeDeductions[0].Line2[0].f1_20[0]",
        "data_1040x_20_correct_2":f"2;topmostSubform[0].Page1[0].Table_IncomeDeductions[0].Line2[0].f1_22[0]",
        "data_1040x_20_orginal_3": f"2;topmostSubform[0].Page1[0].Table_IncomeDeductions[0].Line3[0].f1_23[0]",
        "data_1040x_20_correct_3":f"2;topmostSubform[0].Page1[0].Table_IncomeDeductions[0].Line3[0].f1_25[0]",
        "data_1040x_20_orginal_4a":f"2;topmostSubform[0].Page1[0].Table_IncomeDeductions[0].Line4a[0].f1_26[0]",
        "data_1040x_20_correct_4a": f"2;topmostSubform[0].Page1[0].Table_IncomeDeductions[0].Line4a[0].f1_28[0]",
        "data_1040x_20_orginal_4b": f"2;topmostSubform[0].Page1[0].Table_IncomeDeductions[0].Line4b[0].f1_29[0]",
        "data_1040x_20_correct_4b": f"2;topmostSubform[0].Page1[0].Table_IncomeDeductions[0].Line4b[0].f1_31[0]",
        "data_1040x_20_orginal_5": f"2;topmostSubform[0].Page1[0].Table_IncomeDeductions[0].Line5[0].f1_32[0]",
        "data_1040x_20_correct_5": f"2;topmostSubform[0].Page1[0].Table_IncomeDeductions[0].Line5[0].f1_34[0]",
        "data_1040x_20_orginal_6": f"2;topmostSubform[0].Page1[0].Table_TaxLiability[0].Line6[0].f1_36[0]",
        "data_1040x_20_correct_6": f"2;topmostSubform[0].Page1[0].Table_TaxLiability[0].Line6[0].f1_38[0]",
        "data_1040x_20_orginal_7": f"2;topmostSubform[0].Page1[0].Table_TaxLiability[0].Line7[0].f1_39[0]",
        "data_1040x_20_correct_7": f"2;topmostSubform[0].Page1[0].Table_TaxLiability[0].Line7[0].f1_41[0]",
        "data_1040x_20_orginal_8": f"2;topmostSubform[0].Page1[0].Table_TaxLiability[0].Line8[0].f1_42[0]",
        "data_1040x_20_correct_8": f"2;topmostSubform[0].Page1[0].Table_TaxLiability[0].Line8[0].f1_44[0]",
        "data_1040x_20_orginal_9": f"2;topmostSubform[0].Page1[0].Table_TaxLiability[0].Line9[0].f1_45[0]",
        "data_1040x_20_correct_9":  "2;topmostSubform[0].Page1[0].Table_TaxLiability[0].Line9[0].f1_47[0]",
        "data_1040x_20_orginal_10": f"2;topmostSubform[0].Page1[0].Table_TaxLiability[0].Line10[0].f1_48[0]",
        "data_1040x_20_correct_10": f"2;topmostSubform[0].Page1[0].Table_TaxLiability[0].Line10[0].f1_50[0]",
        "data_1040x_20_orginal_11": f"2;topmostSubform[0].Page1[0].Table_TaxLiability[0].Line11[0].f1_51[0]",
        "data_1040x_20_correct_11": f"2;topmostSubform[0].Page1[0].Table_TaxLiability[0].Line11[0].f1_53[0]",
        "data_1040x_20_orginal_12":f"2;topmostSubform[0].Page1[0].Table_Payments[0].Line12[0].f1_54[0]",
        "data_1040x_20_correct_12": f"2;topmostSubform[0].Page1[0].Table_Payments[0].Line12[0].f1_56[0]",
        "data_1040x_20_orginal_13": f"2;topmostSubform[0].Page1[0].Table_Payments[0].Line13[0].f1_57[0]",
        "data_1040x_20_correct_13": f"2;topmostSubform[0].Page1[0].Table_Payments[0].Line13[0].f1_59[0]",
        "data_1040x_20_orginal_14": f"2;topmostSubform[0].Page1[0].Table_Payments[0].Line14[0].f1_60[0]",
        "data_1040x_20_correct_14": f"2;topmostSubform[0].Page1[0].Table_Payments[0].Line14[0].f1_62[0]",
        "data_1040x_20_orginal_15": f"2;topmostSubform[0].Page1[0].Table_Payments[0].Line15[0].f1_64[0]",
        "data_1040x_20_correct_15": f"2;topmostSubform[0].Page1[0].Table_Payments[0].Line15[0].f1_66[0]",
        "data_1040x_20_change_15": f"2;topmostSubform[0].Page1[0].Table_Payments[0].Line15[0].f1_65[0]",
        "data_1040x_20_correct_16": f"2;topmostSubform[0].Page1[0].f1_67[0]",
        "data_1040x_20_correct_17": f"2;topmostSubform[0].Page1[0].f1_68[0]",
        "data_1040x_20_correct_18": f"2;topmostSubform[0].Page1[0].f1_69[0]",
        "data_1040x_20_correct_19": f"2;topmostSubform[0].Page1[0].f1_70[0]",
        "data_1040x_20_correct_20": f"2;topmostSubform[0].Page1[0].f1_71[0]",
        "data_1040x_20_correct_21": f"2;topmostSubform[0].Page1[0].f1_72[0]",
        "data_1040x_20_correct_22": f"2;topmostSubform[0].Page1[0].f1_73[0]",
        "data_1040x_20_23": f"2;topmostSubform[0].Page1[0].f1_75[0]",
        "data_1040x_20_28": f"3;topmostSubform[0].Page2[0].Table_Lines24-29[0].Line28[0].f2_13[0]",
        "data_1040x_20_29": f"3;topmostSubform[0].Page2[0].Table_Lines24-29[0].Line28[0].f2_16[0]",
        "data_1040x_20_15_checkbox_field": f"2;checkbox_field",
        "data_1040x_20_15_checkbox": f"2;topmostSubform[0].Page1[0].Table_Payments[0].Line15[0].Refundable[0].c1_12[0];true",
        "data_1040x_20_firstName": f"2;topmostSubform[0].Page1[0].firstName1040x[0]",
        "data_1040x_20_lastName": f"2;topmostSubform[0].Page1[0].lastName1040x[0]",
        "data_1040x_20_explain_of_changes": f"3;explain_of_changes"
    }

    pdf_fields_7202_20 = {
        "data_7202_20_1": f"4;topmostSubform[0].Page1[0].f1_3[0]",
        "data_7202_20_2": f"4;topmostSubform[0].Page1[0].f1_4[0]",
        "data_7202_20_3": f"4;topmostSubform[0].Page1[0].f1_5[0]",
        "data_7202_20_4": f"4;topmostSubform[0].Page1[0].f1_6[0]",
        "data_7202_20_5": f"4;topmostSubform[0].Page1[0].f1_7[0]",
        "data_7202_20_6": f"4;topmostSubform[0].Page1[0].f1_8[0]",
        "data_7202_20_7": f"4;topmostSubform[0].Page1[0].f1_9[0]",
        "data_7202_20_8": f"4;topmostSubform[0].Page1[0].number8[0]",
        "data_7202_20_9": f"4;topmostSubform[0].Page1[0].number9[0]",
        "data_7202_20_10": f"4;topmostSubform[0].Page1[0].number10[0]",
        "data_7202_20_11": f"4;topmostSubform[0].Page1[0].number11[0]",
        "data_7202_20_12": f"4;topmostSubform[0].Page1[0].number12[0]",
        "data_7202_20_13": f"4;topmostSubform[0].Page1[0].number13[0]",
        "data_7202_20_14": f"4;topmostSubform[0].Page1[0].number14[0]",
        "data_7202_20_15": f"4;topmostSubform[0].Page1[0].f1_17[0]",
        "data_7202_20_16": f"4;topmostSubform[0].Page1[0].f1_18[0]",
        "data_7202_20_17": f"4;topmostSubform[0].Page1[0].f1_19[0]",
        "data_7202_20_18": f"4;topmostSubform[0].Page1[0].f1_20[0]",
        "data_7202_20_19": f"4;topmostSubform[0].Page1[0].f1_21[0]",
        "data_7202_20_20": f"4;topmostSubform[0].Page1[0].f1_22[0]",
        "data_7202_20_21": f"4;topmostSubform[0].Page1[0].f1_23[0]",
        "data_7202_20_22": f"4;topmostSubform[0].Page1[0].f1_24[0]",
        "data_7202_20_23": f"4;topmostSubform[0].Page1[0].f1_25[0]",
        "data_7202_20_24": f"4;topmostSubform[0].Page1[0].f1_26[0]",
        "data_7202_20_25": f"4;topmostSubform[0].Page1[0].f1_27[0]",
        "data_7202_20_26": f"4;topmostSubform[0].Page1[0].f1_28[0]",
        "data_7202_20_27": f"4;topmostSubform[0].Page1[0].f1_29[0]",
        "data_7202_20_28": f"4;topmostSubform[0].Page1[0].f1_30[0]",
        "data_7202_20_29": f"4;topmostSubform[0].Page1[0].f1_31[0]",
        "data_7202_20_30": f"4;topmostSubform[0].Page1[0].f1_32[0]",
        "data_7202_20_31": f"4;topmostSubform[0].Page1[0].f1_33[0]",
        "data_7202_20_32": f"4;topmostSubform[0].Page1[0].f1_34[0]",
        "data_7202_20_33": f"4;topmostSubform[0].Page1[0].f1_35[0]",
        "data_7202_20_34": f"4;topmostSubform[0].Page1[0].f1_36[0]",
        "data_7202_20_35": f"4;topmostSubform[0].Page1[0].f1_37[0]",
        "data_7202_20_name": f"4;topmostSubform[0].Page1[0].name7202[0]"

    }

    pdf_fields_sch_3_20 = {
        "data_sch_3_20_1": f"5;form1[0].Page1[0].f1_03[0]",
        "data_sch_3_20_2": f"5;form1[0].Page1[0].f1_04[0]",
        "data_sch_3_20_3": f"5;form1[0].Page1[0].f1_05[0]",
        "data_sch_3_20_4": f"5;form1[0].Page1[0].f1_06[0]",
        "data_sch_3_20_5": f"5;form1[0].Page1[0].f1_07[0]",
        "data_sch_3_20_6": f"5;form1[0].Page1[0].f1_09[0]",
        "data_sch_3_20_7": f"5;form1[0].Page1[0].f1_10[0]",
        "data_sch_3_20_8": f"5;form1[0].Page1[0].f1_11[0]",
        "data_sch_3_20_9": f"5;form1[0].Page1[0].f1_12[0]",
        "data_sch_3_20_10": f"5;form1[0].Page1[0].f1_13[0]",
        "data_sch_3_20_11": f"5;form1[0].Page1[0].f1_14[0]",
        "data_sch_3_20_13": f"5;form1[0].Page1[0].f1_22[0]",
        "data_sch_3_20_12a": f"5;form1[0].Page1[0].Line12_ReadOrder[0].f1_15[0]",
        "data_sch_3_20_12b": f"5;form1[0].Page1[0].f1_16[0]",
        "data_sch_3_20_12c": f"5;form1[0].Page1[0].f1_17[0]",
        "data_sch_3_20_12d": f"5;form1[0].Page1[0].f1_19[0]",
        "data_sch_3_20_12e": f"5;form1[0].Page1[0].f1_20[0]",
        "data_sch_3_20_12f": f"5;form1[0].Page1[0].f1_21[0]",
        "data_sch_3_20_name": f"5;form1[0].Page1[0].name_sch_3[0]"
    }

    combined_values = []

    data_variables_1040_20 = data_1040_20['result']
    data_variables_1040x_20 = data_1040x_20['result']
    data_variables_7202_20 = data_7202_20['result']
    data_variables_sch_3_20 = data_sch_3_20['result']

    data_variables_1040_20['data_1040_20_firstName'] = data_1040_20['First_Name']
    data_variables_1040_20['data_1040_20_lastName'] = data_1040_20['Last_Name']

    data_variables_1040x_20['data_1040x_20_15_checkbox_field'] = '7202'
    data_variables_1040x_20['data_1040x_20_firstName'] = data_1040x_20['First_Name']
    data_variables_1040x_20['data_1040x_20_lastName'] = data_1040x_20['Last_Name']
    data_variables_1040x_20['data_1040x_20_explain_of_changes'] = "THIS AMENDMENT IS BEING FILED TO CLAIM SICK LEAVE AND FAMILY LEAVE CREDIT AS SELF EMPLOYED INDIVIDUAL. ONLY FORM 7202 ATTACHED WITH THE FORM 1040X FOR CLAIMING SICK LEAVE AND FAMILY LEAVE CREDIT AS SELF EMPLOYED  INDIVIDUAL"

    data_variables_7202_20['data_7202_20_name'] = data_7202_20['First_Name'] + " " + data_7202_20['Last_Name']

    data_variables_sch_3_20['data_sch_3_20_name'] = data_sch_3_20['First_Name'] + " " + data_sch_3_20['Last_Name']


    for key, value in pdf_fields_1040_20.items():
        val = data_variables_1040_20.get(key, "")

        combined_values.append(f"{value};{val}")

    for key, value in pdf_fields_1040x_20.items():
        val = data_variables_1040x_20.get(key, "")

        combined_values.append(f"{value};{val}")

    for key, value in pdf_fields_7202_20.items():
        val = data_variables_7202_20.get(key, "")

        combined_values.append(f"{value};{val}")

    for key, value in pdf_fields_sch_3_20.items():
        val = data_variables_sch_3_20.get(key, "")

        combined_values.append(f"{value};{val}")

    return "|".join(combined_values)

def combine_fields_21(data_1040_21,data_1040x_21,data_7202_21,data_sch_3_21):
    
    pdf_fields_1040_21 = {
        "data_1040_21_1": "0;data_1040_21_1",
        "data_1040_21_7": "0;data_1040_21_7",
        "data_1040_21_8": "0;data_1040_21_8",
        "data_1040_21_9": "0;data_1040_21_9",
        "data_1040_21_10": "0;data_1040_21_10",
        "data_1040_21_11": "0;data_1040_21_11",
        "data_1040_21_13": "0;data_1040_21_13",
        "data_1040_21_14": "0;data_1040_21_14",
        "data_1040_21_15": "0;data_1040_21_15",
        "data_1040_21_16": "1;data_1040_21_16",
        "data_1040_21_17": "1;data_1040_21_17",
        "data_1040_21_18": "1;data_1040_21_18",
        "data_1040_21_19": "1;data_1040_21_19",
        "data_1040_21_20": "1;data_1040_21_20",
        "data_1040_21_21": "1;data_1040_21_21",
        "data_1040_21_22": "1;data_1040_21_22",
        "data_1040_21_23": "1;data_1040_21_23",
        "data_1040_21_24": "1;data_1040_21_24",
        "data_1040_21_26": "1;data_1040_21_26",
        "data_1040_21_28": "1;data_1040_21_28",
        "data_1040_21_29": "1;data_1040_21_29",
        "data_1040_21_2a": "0;data_1040_21_2a",
        "data_1040_21_30": "1;data_1040_21_30",
        "data_1040_21_31": "1;data_1040_21_31",
        "data_1040_21_32": "1;data_1040_21_32",
        "data_1040_21_33": "1;data_1040_21_33",
        "data_1040_21_34": "1;data_1040_21_34",
        "data_1040_21_36": "1;data_1040_21_36",
        "data_1040_21_37": "1;data_1040_21_37",
        "data_1040_21_38": "1;data_1040_21_38",
        "data_1040_21_3a": "0;data_1040_21_3a",
        "data_1040_21_4a": "0;data_1040_21_4a",
        "data_1040_21_5a": "0;data_1040_21_5a",
        "data_1040_21_6a": "0;data_1040_21_6a",
        "data_1040_21_12a": "0;data_1040_21_12a",
        "data_1040_21_12b": "0;data_1040_21_12b",
        "data_1040_21_12c": "0;data_1040_21_12c",
        "data_1040_21_25a": "1;data_1040_21_25a",
        "data_1040_21_25b": "1;data_1040_21_25b",
        "data_1040_21_25c": "1;data_1040_21_25c",
        "data_1040_21_25d": "1;data_1040_21_25d",
        "data_1040_21_27a": "1;data_1040_21_27a",
        "data_1040_21_27b": "1;data_1040_21_27b",
        "data_1040_21_27c": "1;data_1040_21_27c",
        "data_1040_21_35a": "1;data_1040_21_35a",
        "data_1040_21_firstName": "0;first_name_1040",
        "data_1040_21_lastName": "0;last_name_1040",

    }

    pdf_fields_1040x_21 = {
    "data_1040x_21_23": "2;data_1040x_21_23",
    "data_1040x_21_28": "3;data_1040x_21_28",
    "data_1040x_21_29": "3;data_1040x_21_29",
    "data_1040x_21_30": "3;data_1040x_21_30",
    "data_1040x_21_31": "3;data_1040x_21_31",
    "data_1040x_21_37": "3;data_1040x_21_37",
    "data_1040x_21_38": "3;data_1040x_21_38",
    "data_1040x_21_change_15": "2;data_1040x_21_change_15",
    "data_1040x_21_correct_1": "2;data_1040x_21_correct_1",
    "data_1040x_21_correct_2": "2;data_1040x_21_correct_2",
    "data_1040x_21_correct_3": "2;data_1040x_21_correct_3",
    "data_1040x_21_correct_5": "2;data_1040x_21_correct_5",
    "data_1040x_21_correct_6": "2;data_1040x_21_correct_6",
    "data_1040x_21_correct_7": "2;data_1040x_21_correct_7",
    "data_1040x_21_correct_8": "2;data_1040x_21_correct_8",
    "data_1040x_21_correct_9": "2;data_1040x_21_correct_9",
    "data_1040x_21_correct_10": "2;data_1040x_21_correct_10",
    "data_1040x_21_correct_11": "2;data_1040x_21_correct_11",
    "data_1040x_21_correct_12": "2;data_1040x_21_correct_12",
    "data_1040x_21_correct_13": "2;data_1040x_21_correct_13",
    "data_1040x_21_correct_14": "2;data_1040x_21_correct_14",
    "data_1040x_21_correct_15": "2;data_1040x_21_correct_15",
    "data_1040x_21_correct_17": "2;data_1040x_21_correct_17",
    "data_1040x_21_correct_18": "2;data_1040x_21_correct_18",
    "data_1040x_21_correct_19": "2;data_1040x_21_correct_19",
    "data_1040x_21_correct_20": "2;data_1040x_21_correct_20",
    "data_1040x_21_correct_21": "2;data_1040x_21_correct_21",
    "data_1040x_21_correct_22": "2;data_1040x_21_correct_22",
    "data_1040x_21_correct_4a": "2;data_1040x_21_correct_4a",
    "data_1040x_21_correct_4b": "2;data_1040x_21_correct_4b",
    "data_1040x_21_original_1": "2;data_1040x_21_original_1",
    "data_1040x_21_original_2": "2;data_1040x_21_original_2",
    "data_1040x_21_original_3": "2;data_1040x_21_original_3",
    "data_1040x_21_original_5": "2;data_1040x_21_original_5",
    "data_1040x_21_original_6": "2;data_1040x_21_original_6",
    "data_1040x_21_original_7": "2;data_1040x_21_original_7",
    "data_1040x_21_original_8": "2;data_1040x_21_original_8",
    "data_1040x_21_original_9": "2;data_1040x_21_original_9",
    "data_1040x_21_original_10": "2;data_1040x_21_original_10",
    "data_1040x_21_original_11": "2;data_1040x_21_original_11",
    "data_1040x_21_original_12": "2;data_1040x_21_original_12",
    "data_1040x_21_original_13": "2;data_1040x_21_original_13",
    "data_1040x_21_original_14": "2;data_1040x_21_original_14",
    "data_1040x_21_original_15": "2;data_1040x_21_original_15",
    "data_1040x_21_original_4a": "2;data_1040x_21_original_4a",
    "data_1040x_21_original_4b": "2;data_1040x_21_original_4b",
    "data_1040x_21_org_sch_3_10": "3;data_1040x_21_org_sch_3_10",
    "data_1040x_21_firstName": "2;first_name_1040x",
    "data_1040x_21_lastName": "2;last_name_1040x",
    "data_1040x_21_explain_of_changes": "3;explain_of_changes",
    "data_checkbox": "2;data_checkbox;true",
    "data_1040x_21_15_checkbox_field": "2;data_1040x_21_check_field"
}

    pdf_fields_7202_21 = {
    "data_7202_21_1": "4;data_7202_21_1",
    "data_7202_21_2": "4;data_7202_21_2",
    "data_7202_21_3a": "4;data_7202_21_3a",
    "data_7202_21_3b": "4;data_7202_21_3b",
    "data_7202_21_3c": "4;data_7202_21_3c",
    "data_7202_21_3d": "4;data_7202_21_3d",
    "data_7202_21_4a": "4;data_7202_21_4a",
    "data_7202_21_4b": "4;data_7202_21_4b",
    "data_7202_21_5": "4;data_7202_21_5",
    "data_7202_21_6a": "4;data_7202_21_6a",
    "data_7202_21_6b": "4;data_7202_21_6b",
    "data_7202_21_7a": "4;data_7202_21_7a",
    "data_7202_21_8": "4;data_7202_21_8",
    "data_7202_21_9": "4;data_7202_21_9",
    "data_7202_21_10": "4;data_7202_21_10",
    "data_7202_21_11": "4;data_7202_21_11",
    "data_7202_21_12": "4;data_7202_21_12",
    "data_7202_21_13": "4;data_7202_21_13",
    "data_7202_21_14": "4;data_7202_21_14",
    "data_7202_21_15a": "4;data_7202_21_15a",
    "data_7202_21_15b": "4;data_7202_21_15b",
    "data_7202_21_15c": "4;data_7202_21_15c",
    "data_7202_21_16a": "4;data_7202_21_16a",
    "data_7202_21_16b": "4;data_7202_21_16b",
    "data_7202_21_16c": "4;data_7202_21_16c",
    "data_7202_21_17a": "4;data_7202_21_17a",
    "data_7202_21_17b": "4;data_7202_21_17b",
    "data_7202_21_17c": "4;data_7202_21_17c",
    "data_7202_21_18": "4;data_7202_21_18",
    "data_7202_21_19": "4;data_7202_21_19",
    "data_7202_21_20a": "4;data_7202_21_20a",
    "data_7202_21_20b": "4;data_7202_21_20b",
    "data_7202_21_20c": "4;data_7202_21_20c",
    "data_7202_21_21": "4;data_7202_21_21",
    "data_7202_21_22": "4;data_7202_21_22",
    "data_7202_21_23": "4;data_7202_21_23",
    "data_7202_21_24": "4;data_7202_21_24",
    "data_7202_21_25a": "5;data_7202_21_25a",
    "data_7202_21_25b": "5;data_7202_21_25b",
    "data_7202_21_25c": "5;data_7202_21_25c",
    "data_7202_21_25d": "5;data_7202_21_25d",
    "data_7202_21_26a": "5;data_7202_21_26a",
    "data_7202_21_27": "5;data_7202_21_27",
    "data_7202_21_28": "5;data_7202_21_28",
    "data_7202_21_29": "5;data_7202_21_29",
    "data_7202_21_30": "5;data_7202_21_30",
    "data_7202_21_31a": "5;data_7202_21_31a",
    "data_7202_21_31b": "5;data_7202_21_31b",
    "data_7202_21_31c": "5;data_7202_21_31c",
    "data_7202_21_32a": "5;data_7202_21_32a",
    "data_7202_21_32b": "5;data_7202_21_32b",
    "data_7202_21_32c": "5;data_7202_21_32c",
    "data_7202_21_33": "5;data_7202_21_33",
    "data_7202_21_34": "5;data_7202_21_34",
    "data_7202_21_35": "5;data_7202_21_35",
    "data_7202_21_36": "5;data_7202_21_36",
    "data_7202_21_37": "5;data_7202_21_37",
    "data_7202_21_38a": "5;data_7202_21_38a",
    "data_7202_21_38b": "5;data_7202_21_38b",
    "data_7202_21_39": "5;data_7202_21_39",
    "data_7202_21_40a": "5;data_7202_21_40a",
    "data_7202_21_40b": "5;data_7202_21_40b",
    "data_7202_21_41a": "5;data_7202_21_41a",
    "data_7202_21_42": "5;data_7202_21_42",
    "data_7202_21_43": "5;data_7202_21_43",
    "data_7202_21_44": "5;data_7202_21_44",
    "data_7202_21_45": "5;data_7202_21_45",
    "data_7202_21_46": "5;data_7202_21_46",
    "data_7202_21_47": "5;data_7202_21_47",
    "data_7202_21_48": "5;data_7202_21_48",
    "data_7202_21_49": "5;data_7202_21_49",
    "data_7202_21_50": "5;data_7202_21_50",
    "data_7202_21_51": "5;data_7202_21_51",
    "data_7202_21_52": "5;data_7202_21_52",
    "data_7202_21_53": "5;data_7202_21_53",
    "data_7202_21_54": "5;data_7202_21_54",
    "data_7202_21_55": "5;data_7202_21_55",
    "data_7202_21_56": "5;data_7202_21_56",
    "data_7202_21_57": "5;data_7202_21_57",
    "data_7202_21_58": "5;data_7202_21_58",
    "data_7202_21_59": "6;data_7202_21_59",
    "data_7202_21_60a": "6;data_7202_21_60a",
    "data_7202_21_61": "6;data_7202_21_61",
    "data_7202_21_62": "6;data_7202_21_62",
    "data_7202_21_63": "6;data_7202_21_63",
    "data_7202_21_64": "6;data_7202_21_64",
    "data_7202_21_65": "6;data_7202_21_65",
    "data_7202_21_66": "6;data_7202_21_66",
    "data_7202_21_67": "6;data_7202_21_67",
    "data_7202_21_68": "6;data_7202_21_68",
    "data_7202_21_69": "6;data_7202_21_69",    
    "data_7202_21_name" : "4;name_7202"
}

    pdf_fields_sch_3_21 = {
        "data_sch_3_21_1": "7;data_sch_3_21_1",
        "data_sch_3_21_2": "7;data_sch_3_21_2",
        "data_sch_3_21_3": "7;data_sch_3_21_3",
        "data_sch_3_21_4": "7;data_sch_3_21_4",
        "data_sch_3_21_5": "7;data_sch_3_21_5",
        "data_sch_3_21_6a": "7;data_sch_3_21_6a",
        "data_sch_3_21_6b": "7;data_sch_3_21_6b",
        "data_sch_3_21_6c": "7;data_sch_3_21_6c",
        "data_sch_3_21_6d": "7;data_sch_3_21_6d",
        "data_sch_3_21_6e": "7;data_sch_3_21_6e",
        "data_sch_3_21_6f": "7;data_sch_3_21_6f",
        "data_sch_3_21_6g": "7;data_sch_3_21_6g",
        "data_sch_3_21_6h": "7;data_sch_3_21_6h",
        "data_sch_3_21_6i": "7;data_sch_3_21_6i",
        "data_sch_3_21_6j": "7;data_sch_3_21_6j",
        "data_sch_3_21_6k": "7;data_sch_3_21_6k",
        "data_sch_3_21_6l": "7;data_sch_3_21_6l",
        "data_sch_3_21_6z": "7;data_sch_3_21_6z",
        "data_sch_3_21_7": "7;data_sch_3_21_7",
        "data_sch_3_21_8": "7;data_sch_3_21_8",
        "data_sch_3_21_9": "8;data_sch_3_21_9",
        "data_sch_3_21_10": "8;data_sch_3_21_10",
        "data_sch_3_21_11": "8;data_sch_3_21_11",
        "data_sch_3_21_12": "8;data_sch_3_21_12",
        "data_sch_3_21_13a": "8;data_sch_3_21_13a",
        "data_sch_3_21_13b": "8;data_sch_3_21_13b",
        "data_sch_3_21_13c": "8;data_sch_3_21_13c",
        "data_sch_3_21_13d": "8;data_sch_3_21_13d",
        "data_sch_3_21_13e": "8;data_sch_3_21_13e",
        "data_sch_3_21_13f": "8;data_sch_3_21_13f",
        "data_sch_3_21_13g": "8;data_sch_3_21_13g",
        "data_sch_3_21_13h": "8;data_sch_3_21_13h",
        "data_sch_3_21_13z": "8;data_sch_3_21_13z",
        "data_sch_3_21_14": "8;data_sch_3_21_14",
        "data_sch_3_21_15": "8;data_sch_3_21_15",
        "data_sch_3_21_name": "8;data_sch_3_21_name"
    }

    data_variables_1040_21 = data_1040_21['result']
    data_variables_1040x_21 = data_1040x_21['result']
    data_variables_7202_21 = data_7202_21['result']
    data_variables_sch_3_21 = data_sch_3_21['result']

    data_variables_1040_21['data_1040_21_firstName'] = data_1040_21['First_Name']
    data_variables_1040_21['data_1040_21_lastName'] = data_1040_21['Last_Name']

    data_variables_1040x_21['data_1040x_21_15_checkbox_field'] = '7202'
    data_variables_1040x_21['data_1040x_21_firstName'] = data_1040x_21['First_Name']
    data_variables_1040x_21['data_1040x_21_lastName'] = data_1040x_21['Last_Name']
    data_variables_1040x_21['data_1040x_21_explain_of_changes'] = "THIS AMENDMENT IS BEING FILED TO CLAIM SICK LEAVE AND FAMILY LEAVE CREDIT AS SELF EMPLOYED INDIVIDUAL. ONLY FORM 7202 ATTACHED WITH THE FORM 1040X FOR CLAIMING SICK LEAVE AND FAMILY LEAVE CREDIT AS SELF EMPLOYED  INDIVIDUAL"

    data_variables_7202_21['data_7202_21_name'] = data_7202_21['First_Name'] + " " + data_7202_21['Last_Name']



    data_variables_sch_3_21['data_sch_3_21_name'] = data_sch_3_21['First_Name'] + " " + data_sch_3_21['Last_Name']


    combined_values = []

    for key, value in pdf_fields_1040_21.items():
        val = data_variables_1040_21.get(key, "")

        combined_values.append(f"{value};{val}")

    for key, value in pdf_fields_1040x_21.items():
        val = data_variables_1040x_21.get(key, "")

        combined_values.append(f"{value};{val}")

    for key, value in pdf_fields_7202_21.items():
        val = data_variables_7202_21.get(key, "")

        combined_values.append(f"{value};{val}")

    for key, value in pdf_fields_sch_3_21.items():
        val = data_variables_sch_3_21.get(key, "")

        combined_values.append(f"{value};{val}")
    
    print(combined_values)
    return "|".join(combined_values)

def get_7202_21_data(data_variables):
    
    instructions_data =  get_instructions_data(data_variables)
    data_7202_20 = get_7202_20_data(data_variables)

    twentyOne_7202_Day_Overide_1 = int(instructions_data['Gov_January_1_2021_through_March_31_2021'])
    # pull the date variable from Gov_January_1_2021_through_March_31_2021
    # K7
    K7 = twentyOne_7202_Day_Overide_1

    twentyOne_7202_Day_Overide_2 = int(instructions_data['Child_January_1_2021_through_March_31_2021'])
    # pull the date variable from Child_January_1_2021_through_March_31_2021
    # K8
    K8 = twentyOne_7202_Day_Overide_2

    twentyOne_7202_Day_Overide_3 = int(instructions_data['Family_January_1_2021_through_March_31_2021'])
    # pull the date variable from Family_January_1_2021_through_March_31_2021
    # = K9
    K9 = twentyOne_7202_Day_Overide_3

    twentyOne_7202_Day_Overide_4 = int(instructions_data['Gov_April_1_2021_through_September_30_2021'])
    twentyOne_7202_Day_Overide_5 = int(instructions_data['Child_April_1_2021_through_September_30_2021'])
    twentyOne_7202_Day_Overide_6 = int(instructions_data['Family_April_1_2021_through_September_30_2021'])


    # this is the 2019 income variable
    twenty_7202_2019 = int(instructions_data['nineteen_ADJUSTED_GROSS_INCOME'])

    # this is the 2020 income variables
    twenty_7202_20Schedule_SE_Line_3 = int(instructions_data['twenty_SE_income_per_computer'])

    # formula =ROUND(IF(AL24>0,AL24*0.9235,AL24),0)
    # Given value of AL24
    AL24 = int(twenty_7202_20Schedule_SE_Line_3)
    # Applying the formula
    AL24result = int(round(AL24 * 0.9235 if AL24 > 0 else AL24, 0))
    twenty_7202_20_Line_4a = AL24result
    print(AL24result)

    twenty_7202_20_Line_4b = 0
    # was AL26

    # AL27
    # =MAX(SUM(AL25,AL26),0)
    # AL25 = twenty_7202_20_Line_4a,  AL26= twenty_7202_20_Line 4b
    # Given values of AL25 and AL26
    AL25 = twenty_7202_20_Line_4a
    AL26 = twenty_7202_20_Line_4b

    # Applying the formula
    twenty_7202_20_Line_4c_result = max(sum([AL25, AL26]), 0)
    twenty_7202_20_Line_4c = twenty_7202_20_Line_4c_result



    twenty_7202_20_Line_5a = 0

    # AL29
    # =ROUND(AL28*0.9235,0)
    # Given value of AL28
    AL28 = twenty_7202_20_Line_5a
    # Applying the formula
    twenty_7202_20_Line_5b_result = int(round(AL28 * 0.9235, 0))
    twenty_7202_20_Line_5b = twenty_7202_20_Line_5b_result



    # =AL27+AL29
    # Given Values of AL27 AL29
    AL27 = twenty_7202_20_Line_4c
    AL29 = twenty_7202_20_Line_5b
    # Adding the values
    twenty_7202_20_Line_6_result = AL27 + AL29
    twenty_7202_20_Line_6 = twenty_7202_20_Line_6_result

    twentyOne_IncomeSELine3 = int(instructions_data['twenty_twenty_one_SE_income_per_computer'])
    twentyOne_Line4a = int(round(twentyOne_IncomeSELine3 * 0.9235 if twentyOne_IncomeSELine3 > 0 else twentyOne_IncomeSELine3, 0))
    # Assigns the rounded result of the calculation to twentyOne_Line4a
    twentyOne_Line4b = 0
    # Assigns the maximum of the sum of L31 and L32 or 0 to twentyOne_Line4c
    twentyOne_Line4c = max(twentyOne_Line4a + twentyOne_Line4b, 0)
    twentyOne_Line5a = 0
    twentyOne_Line5b = int(round(twentyOne_Line5a*0.9235,0))
    twentyOne_Line6 = twentyOne_Line4c + twentyOne_Line5b



    Fiscal_Year_Return = True
    Sick_Leave_1 = 0
    Sick_Leave_2 = 0
    Sick_Leave_3 = 0
    AL21 = Sick_Leave_3


    # start the Column for the 7202 form

    # Line 1
    # Assigns the value based on the condition

    twentyOne_7202_1 = twentyOne_7202_Day_Overide_1
    # = G5
    # =IF(G5>9,0,MIN(10-G5,SUMIF($L$7:$L$17,"Other",$O$7:$O$17)))
    # =IF(G5>9,0,MIN(10-G5,G5)))
    G5 = twentyOne_7202_1

    # Line 2
    # =IF(G5>9,0,MIN(10-G5,SUMIF($L$7:$L$17,"Other",$O$7:$O$17)))
    # G5 = twentyOne_7202_1  Sum replace twentyOne_7202_Day_Overide_2
    # =IF(twentyOne_7202_1>9,0,MIN(10-twentyOne_7202_1,twentyOne_7202_Day_Overide_2))
    # Assigns the value based on the condition
    twentyOne_7202_2 = 0  # Default value
    if twentyOne_7202_1 > 9:
        twentyOne_7202_2 = 0
    else:
        twentyOne_7202_2 = min(10 - twentyOne_7202_1, twentyOne_7202_Day_Overide_2)



    #line 3a
    # ='2020 7202'!AJ8
    twentyOne_7202_3a = data_7202_20['data_7202_20_4']

    # line 3b
    #='2020 7202'!AJ10
    twentyOne_7202_3b = data_7202_20['data_7202_20_6']

    # Line 3c
    # =G7+G8  which is 3a + 3b
    twentyOne_7202_3c = twentyOne_7202_3a + twentyOne_7202_3b

    # line 3d
    # =IF(G5=0,0,10-G9)
    # twentyOne_7202_3d = =IF(twentyOne_7202_1=0,0,10-twentyOne_7202_3c)
    twentyOne_7202_3d = None  # Initializing the variable
    # Assigns the value based on the condition
    if twentyOne_7202_1 == 0:
        twentyOne_7202_3d = 0
    else:
        twentyOne_7202_3d = 10 - twentyOne_7202_3c

    #line 4a
    # =MIN(G5,G10)
    twentyOne_7202_4a = min(twentyOne_7202_1,twentyOne_7202_3d)

    #line 5
    # formula: =G10-G11
    twentyOne_7202_5 = abs(twentyOne_7202_3d - twentyOne_7202_4a)

    #Line 6a
    # =MIN(G6,G12)
    twentyOne_7202_6a = min(twentyOne_7202_2,twentyOne_7202_5)

    # line 7a
    # =MAX(K36:L36)
    twentyOne_7202_7a = max(twenty_7202_20_Line_6,twentyOne_Line6)

    # line 8
    # =ROUND(G15/260,0)
    twentyOne_7202_8 = int(round(twentyOne_7202_7a/260,0))

    #line 9
    # =MIN(G17,511)
    twentyOne_7202_9 = min(twentyOne_7202_8, 511)

    #line 10
    # =G11*G19
    twentyOne_7202_10 = twentyOne_7202_4a * twentyOne_7202_9

    #11
    # =ROUND(G17*0.67,0)
    twentyOne_7202_11 = int(round(twentyOne_7202_8*0.67,0))

    #12
    # =MIN(G21,200)
    twentyOne_7202_12 = min(twentyOne_7202_11,200)

    #13
    # =G14*G22
    twentyOne_7202_13 = twentyOne_7202_6a*twentyOne_7202_12

    #14
    # =G23+G20
    twentyOne_7202_14 = twentyOne_7202_13 + twentyOne_7202_10
    twentyOne_7202_15a = Sick_Leave_1

    #15b
    # ='2020 7202'!AJ19
    twentyOne_7202_15b = data_7202_20['data_7202_20_15']

    #15c
    # =G25+G26
    twentyOne_7202_15c = twentyOne_7202_15a + twentyOne_7202_15b

    # 16a
    # =K22
    twentyOne_7202_16a = Sick_Leave_2

    #16b
    # ='2020 7202'!AJ20
    twentyOne_7202_16b = data_7202_20['data_7202_20_16']
    #16c
    # =G28+G29
    twentyOne_7202_16c = twentyOne_7202_16a + twentyOne_7202_16b

    #=G23+G30
    twentyOne_7202_17a = twentyOne_7202_13 + twentyOne_7202_16c

    # ='2020 7202'!AJ17
    twentyOne_7202_17b = data_7202_20['data_7202_20_13']
    # =G31+G33
    twentyOne_7202_17c = twentyOne_7202_17a + twentyOne_7202_17b

    # =MIN(G34,2000)
    twentyOne_7202_18 = min(twentyOne_7202_17c, 2000)
    # =G34-G35
    twentyOne_7202_19 = twentyOne_7202_17c + twentyOne_7202_18

    # =G20+G27+G35
    twentyOne_7202_20a = twentyOne_7202_10 + twentyOne_7202_15c + twentyOne_7202_18

    # ='2020 7202'!AJ14
    twentyOne_7202_20b = data_7202_20['data_7202_20_10']

    # =G37+G38
    twentyOne_7202_20c = twentyOne_7202_20a + twentyOne_7202_20b

    # =MIN(G39,5110)
    twentyOne_7202_21 = min(twentyOne_7202_20c, 5110)

    #=G39-G40
    twentyOne_7202_22 = abs(twentyOne_7202_20c - twentyOne_7202_21)

    #=G36+G41
    twentyOne_7202_23 = twentyOne_7202_19 + twentyOne_7202_22


    #=IF(G30+G27=0,G24,MAX(G24-G42,0))
    # IF(twentyOne_7202_19+twentyOne_7202_15c=0,twentyOne_7202_14,max(twentyOne_7202_14-twentyOne_7202_23,0))
    twentyOne_7202_24 = 0
    if twentyOne_7202_19 + twentyOne_7202_15c == 0:
        twentyOne_7202_24 = twentyOne_7202_14
    else:
        twentyOne_7202_24 = max(twentyOne_7202_14 - twentyOne_7202_23, 0)

    # =MIN(SUMIF($L$7:$L$17,"Fam Leave",$O$7:$O$17)-G6,50)
    # =min(Sick_Leave_3-twentyOne_7202_2,50)
    twentyOne_7202_25a = min(twentyOne_7202_Day_Overide_3 - twentyOne_7202_2, 50)

    #='2020 7202'!AJ32
    twentyOne_7202_25b = data_7202_20['data_7202_20_25']

    # =IF(G46=0,0,50-G47)
    # = if(twentyOne_7202_25a=0,0,50-twentyOne_7202_25b)
    twentyOne_7202_25c = 0 if twentyOne_7202_25a == 0 else 50 - twentyOne_7202_25b

    # =MIN(G48,G46)
    twentyOne_7202_25d = min(twentyOne_7202_25c, twentyOne_7202_25a)

    # =MAX(K36:L36)
    twentyOne_7202_26a = max(twenty_7202_20_Line_6,twentyOne_Line6)

    # =ROUND(G50/260,0)
    twentyOne_7202_27 = int(round(twentyOne_7202_26a/260,0))

    #=ROUND(G51*0.67,0)
    twentyOne_7202_28 = int(round(twentyOne_7202_27*0.67,0))

    # =MIN(G53,200)
    twentyOne_7202_29 = min(twentyOne_7202_28,200)
    # =ROUND(G54*G49,0)
    twentyOne_7202_30 = int(round(twentyOne_7202_29*twentyOne_7202_25d,0))
    # =K23
    twentyOne_7202_31a = Sick_Leave_3

    # ='2020 7202'!AJ40
    twentyOne_7202_31b = data_7202_20['data_7202_20_31']

    # =G56+G57
    twentyOne_7202_31c = twentyOne_7202_31a + twentyOne_7202_31b

    # =G58+G55
    twentyOne_7202_32a = twentyOne_7202_30 + twentyOne_7202_31c

    # ='2020 7202'!AJ39
    twentyOne_7202_32b = data_7202_20['data_7202_20_30']

    # =G59+G61
    twentyOne_7202_32c = twentyOne_7202_32a + twentyOne_7202_32b

    # =MIN(G62,10000)
    twentyOne_7202_33 = int(min(twentyOne_7202_32c,10000))

    # =G62-G63
    twentyOne_7202_34 = twentyOne_7202_32c - twentyOne_7202_33

    # =MAX(G55-G64,0)
    twentyOne_7202_35 = max(twentyOne_7202_30 - twentyOne_7202_34,0)

    #=SUMIF($L$70:$L$79,"Self",$O$70:$O$79)
    #
    twentyOne_7202_36 = twentyOne_7202_Day_Overide_4

    # =IF(G67>9,0,MIN(10-G67,SUMIF($L$70:$L$79,"Other",$O$70:$O$79)))
    # twentyOne_7202_37 = IF (twentyOne_7202_36>9,0,MIN(10-twentyOne_7202_36,twentyOne_7202_Day_Overide_4))
    twentyOne_7202_37 = 0
    if twentyOne_7202_36 > 9:
        twentyOne_7202_37 = 0
    else:
        twentyOne_7202_37 = min(10 - twentyOne_7202_36, twentyOne_7202_Day_Overide_4)

    # =MIN(10,G67)
    twentyOne_7202_38a = min(10,twentyOne_7202_36)

    #=IF(G67=0,0,10-G69)
    # twentyOne_7202_39 = IF (twentyOne_7202_36=0,0,10-twentyOne_7202_38a)
    twentyOne_7202_39 = 0
    if twentyOne_7202_36 == 0:
        twentyOne_7202_39 = 0
    else:
        twentyOne_7202_39 = 10 - twentyOne_7202_38a

    # =MIN(G68,G70)
    twentyOne_7202_40a = min(twentyOne_7202_37,twentyOne_7202_39)

    # =MAX(K36:L36)
    twentyOne_7202_41a = max(twenty_7202_20_Line_6,twentyOne_Line6)

    # =ROUND(G73/260,0)
    twentyOne_7202_42 = int(round(twentyOne_7202_41a/260,0))

    # =MIN(G75,511)
    twentyOne_7202_43 = min(twentyOne_7202_42,511)

    #=G69*G77
    twentyOne_7202_44 = twentyOne_7202_43 * twentyOne_7202_38a

    # =ROUND(G75*0.67,0)
    twentyOne_7202_45 = int(round(twentyOne_7202_42*0.67,0))

    #=MIN(G79,200)
    twentyOne_7202_46 = min(twentyOne_7202_45,200)

    # =G80*G72
    twentyOne_7202_47 = twentyOne_7202_46 * twentyOne_7202_40a

    # =G78+G81
    twentyOne_7202_48 = twentyOne_7202_44 + twentyOne_7202_47

    # =K83
    twentyOne_7202_49 = Sick_Leave_1

    # =K84
    twentyOne_7202_50 = Sick_Leave_2

    # =G81+G84
    twentyOne_7202_51 = twentyOne_7202_47 + twentyOne_7202_50

    # =MIN(G85,2000)
    twentyOne_7202_52 = min(twentyOne_7202_51,2000)

    # =G85-G87
    twentyOne_7202_53 = twentyOne_7202_51 - twentyOne_7202_52

    # =G78+G83+G87
    twentyOne_7202_54 = twentyOne_7202_44 + twentyOne_7202_49 + twentyOne_7202_52

    #=MIN(G89,5110)
    twentyOne_7202_55 = min(twentyOne_7202_54, 5110)

    # =G89-G90
    twentyOne_7202_56 = twentyOne_7202_54 - twentyOne_7202_55

    # =G88+G91
    twentyOne_7202_57 = twentyOne_7202_53 + twentyOne_7202_56

    # =MAX(G82-G92,0)
    twentyOne_7202_58 = max(twentyOne_7202_48-twentyOne_7202_57,0)

    # =MIN(SUMIF($L$70:$L$79,"Fam Leave",$O$70:$O$79),60)
    # =min(twentyOne_7202_Day_Overide_6,60)
    twentyOne_7202_59 = min(twentyOne_7202_Day_Overide_6,60)

    # =MAX(K36:L36)
    twentyOne_7202_60a =max(twenty_7202_20_Line_6,twentyOne_Line6)

    # =ROUND(G97/260,0)
    twentyOne_7202_61 = int(round(twentyOne_7202_60a/260,0))

    #=ROUND(G98*0.67,0)
    twentyOne_7202_62 =int(round(twentyOne_7202_61*0.67,0))

    # =MIN(G100,200)
    twentyOne_7202_63 = min(twentyOne_7202_62,200)

    #=G96*G101
    twentyOne_7202_64 = twentyOne_7202_59 * twentyOne_7202_63

    #=K85
    twentyOne_7202_65 = Sick_Leave_3

    # =G102+G103
    twentyOne_7202_66 = twentyOne_7202_64 + twentyOne_7202_65

    # =MIN(G104,12000)
    twentyOne_7202_67 = min(twentyOne_7202_66,12000)

    # =G104-G106
    twentyOne_7202_68 = twentyOne_7202_66 - twentyOne_7202_67

    # =MAX(G102-G107,0)
    twentyOne_7202_69 = max(twentyOne_7202_64-twentyOne_7202_68,0)


    #=G43+G65
    Schedule3_13b = twentyOne_7202_24+twentyOne_7202_35

    #=G93+G108
    Schedule3_13h = twentyOne_7202_58 + twentyOne_7202_69
    
    data_7202_21_4b = instructions_data['Zoho_21_7202_4b']

    data_7202_21_6b  = instructions_data['Zoho_21_7202_6b']

    data_7202_21_38b = instructions_data['Zoho_21_7202_38b']

    data_7202_21_40b = instructions_data['Zoho_21_7202_40b']

    data_7202_21 = {
        "data_7202_21_1": twentyOne_7202_1,
        "data_7202_21_2": twentyOne_7202_2,
        "data_7202_21_3a": twentyOne_7202_3a,
        "data_7202_21_3b": twentyOne_7202_3b,
        "data_7202_21_3c": twentyOne_7202_3c,
        "data_7202_21_3d": twentyOne_7202_3d,
        "data_7202_21_4a": twentyOne_7202_4a,
        "data_7202_21_4b": data_7202_21_4b,
        "data_7202_21_5": twentyOne_7202_5,
        "data_7202_21_6a": twentyOne_7202_6a,
        "data_7202_21_6b": data_7202_21_6b,
        "data_7202_21_7a": twentyOne_7202_7a,
        "data_7202_21_8": twentyOne_7202_8,
        "data_7202_21_9": twentyOne_7202_9,
        "data_7202_21_10": twentyOne_7202_10,
        "data_7202_21_11": twentyOne_7202_11,
        "data_7202_21_12": twentyOne_7202_12,
        "data_7202_21_13": twentyOne_7202_13,
        "data_7202_21_14": twentyOne_7202_14,
        "data_7202_21_15a": twentyOne_7202_15a,
        "data_7202_21_15b": twentyOne_7202_15b,
        "data_7202_21_15c": twentyOne_7202_15c,
        "data_7202_21_16a": twentyOne_7202_16a,
        "data_7202_21_16b": twentyOne_7202_16b,
        "data_7202_21_16c": twentyOne_7202_16c,
        "data_7202_21_17a": twentyOne_7202_17a,
        "data_7202_21_17b": twentyOne_7202_17b,
        "data_7202_21_17c": twentyOne_7202_17c,
        "data_7202_21_18": twentyOne_7202_18,
        "data_7202_21_19": twentyOne_7202_19,
        "data_7202_21_20a": twentyOne_7202_20a,
        "data_7202_21_20b": twentyOne_7202_20b,
        "data_7202_21_20c": twentyOne_7202_20c,
        "data_7202_21_21": twentyOne_7202_21,
        "data_7202_21_22": twentyOne_7202_22,
        "data_7202_21_23": twentyOne_7202_23,
        "data_7202_21_24": twentyOne_7202_24,
        "data_7202_21_25a": twentyOne_7202_25a,
        "data_7202_21_25b": twentyOne_7202_25b,
        "data_7202_21_25c": twentyOne_7202_25c,
        "data_7202_21_25d": twentyOne_7202_25d,
        "data_7202_21_26a": twentyOne_7202_26a,
        "data_7202_21_27": twentyOne_7202_27,
        "data_7202_21_28": twentyOne_7202_28,
        "data_7202_21_29": twentyOne_7202_29,
        "data_7202_21_30": twentyOne_7202_30,
        "data_7202_21_31a": twentyOne_7202_31a,
        "data_7202_21_31b": twentyOne_7202_31b,
        "data_7202_21_31c": twentyOne_7202_31c,
        "data_7202_21_32a": twentyOne_7202_32a,
        "data_7202_21_32b": twentyOne_7202_32b,
        "data_7202_21_32c": twentyOne_7202_32c,
        "data_7202_21_33": twentyOne_7202_33,
        "data_7202_21_34": twentyOne_7202_34,
        "data_7202_21_35": twentyOne_7202_35,
        "data_7202_21_36": twentyOne_7202_36,
        "data_7202_21_37": twentyOne_7202_37,
        "data_7202_21_38a": twentyOne_7202_38a,
        "data_7202_21_38b": data_7202_21_38b,
        "data_7202_21_39": twentyOne_7202_39,
        "data_7202_21_40a": twentyOne_7202_40a,
        "data_7202_21_40b": data_7202_21_40b,
        "data_7202_21_41a": twentyOne_7202_41a,
        "data_7202_21_42": twentyOne_7202_42,
        "data_7202_21_43": twentyOne_7202_43,
        "data_7202_21_44": twentyOne_7202_44,
        "data_7202_21_45": twentyOne_7202_45,
        "data_7202_21_46": twentyOne_7202_46,
        "data_7202_21_47": twentyOne_7202_47,
        "data_7202_21_48": twentyOne_7202_48,
        "data_7202_21_49": twentyOne_7202_49,
        "data_7202_21_50": twentyOne_7202_50,
        "data_7202_21_51": twentyOne_7202_51,
        "data_7202_21_52": twentyOne_7202_52,
        "data_7202_21_53": twentyOne_7202_53,
        "data_7202_21_54": twentyOne_7202_54,
        "data_7202_21_55": twentyOne_7202_55,
        "data_7202_21_56": twentyOne_7202_56,
        "data_7202_21_57": twentyOne_7202_57,
        "data_7202_21_58": twentyOne_7202_58,
        "data_7202_21_59": twentyOne_7202_59,
        "data_7202_21_60a": twentyOne_7202_60a,
        "data_7202_21_61": twentyOne_7202_61,
        "data_7202_21_62": twentyOne_7202_62,
        "data_7202_21_63": twentyOne_7202_63,
        "data_7202_21_64": twentyOne_7202_64,
        "data_7202_21_65": twentyOne_7202_65,
        "data_7202_21_66": twentyOne_7202_66,
        "data_7202_21_67": twentyOne_7202_67,
        "data_7202_21_68": twentyOne_7202_68,
        "data_7202_21_69": twentyOne_7202_69,
        "data_7202_21_sch_3_13b":  Schedule3_13b,
        "data_7202_21_sch_3_13h": Schedule3_13h
    }

    return data_7202_21


def get_sch_3_21_data(data_variables):

    data_7202_21 = get_7202_21_data(data_variables)

    twentyOne_schd3_13b = data_7202_21['data_7202_21_sch_3_13b']

    twentyOne_schd3_13h = data_7202_21['data_7202_21_sch_3_13h']

    twentyOne_schd3_14 = twentyOne_schd3_13b + twentyOne_schd3_13h

    twentyOne_schd3_15 = twentyOne_schd3_14

    data_sch_3_21 = {
        "data_sch_3_21_13b": twentyOne_schd3_13b,
        "data_sch_3_21_13h": twentyOne_schd3_13h,
        "data_sch_3_21_14": twentyOne_schd3_14,
        "data_sch_3_21_15": twentyOne_schd3_15
    }

    return data_sch_3_21


def get_1040_21_data(data_variables):

    instructions_data = get_instructions_data(data_variables)
    data_sch_3_21 = get_sch_3_21_data(data_variables)
    data_7202_21 = get_7202_21_data(data_variables)


    twentyOne_1040_1 =  instructions_data['twenty_twenty_one_wages_salaries_tips_etc']
    twentyOne_1040_2a = instructions_data['twenty_twenty_one_tax_exempt_interest']
    twentyOne_1040_2b = instructions_data['twenty_twenty_one_taxable_interest_income']
    twentyOne_1040_3a = instructions_data['twenty_twenty_one_qualified_dividends']
    twentyOne_1040_3b = instructions_data['twenty_twenty_one_ordinary_dividend_income']
    twentyOne_1040_4a = instructions_data['twenty_twenty_one_total_IRA_distributions']
    twentyOne_1040_4b = instructions_data['twenty_twenty_one_taxable_IRA_distributions']
    twentyOne_1040_5a = instructions_data['twenty_twenty_one_total_pensions_and_annuities']
    twentyOne_1040_5b = instructions_data['twenty_twenty_one_taxable_pension_annuity_amount']
    twentyOne_1040_6a = instructions_data['twenty_twenty_one_total_social_security_benefits']
    twentyOne_1040_6b = instructions_data['twenty_twenty_one_taxable_social_security_benefits_per_computer']
    twentyOne_1040_7 =  instructions_data['twenty_twenty_one_capital_gain_or_loss']
    twentyOne_1040_8 =  instructions_data['twenty_twenty_one_other_income']
    twentyOne_1040_9 = twentyOne_1040_1 + twentyOne_1040_2b + twentyOne_1040_3b + twentyOne_1040_4b + twentyOne_1040_5b + twentyOne_1040_6b + twentyOne_1040_7 + twentyOne_1040_8
    twentyOne_1040_10 = instructions_data['twenty_twenty_one_total_adjustments_per_computer']

    # =AB43-AB44
    twentyOne_1040_11 = abs(twentyOne_1040_9 - twentyOne_1040_10)
    twentyOne_1040_12a = instructions_data['twenty_twenty_one_standard_deduction_per_computer']
    twentyOne_1040_12b = instructions_data['twenty_twenty_one_non_itemized_charitable_contribution_per_computer']
    twentyOne_1040_12c = twentyOne_1040_12a + twentyOne_1040_12b
    twentyOne_1040_13 = instructions_data['twenty_twenty_one_qualified_business_income_deduction_computer']
    # =AB48+AB49
    twentyOne_1040_14 = twentyOne_1040_12c + twentyOne_1040_13

    # =IF(AB45-AB50<0,"0",AB45-AB50)
    twentyOne_1040_15 = 0
    if twentyOne_1040_11 - twentyOne_1040_14 < 0:
        twentyOne_1040_15 = "0"
    else:
        twentyOne_1040_15 = twentyOne_1040_11 - twentyOne_1040_14

    twentyOne_1040_16 = instructions_data['twenty_twenty_one_tentative_tax']
    twentyOne_1040_17 = 0

    # =AB54+AB55
    twentyOne_1040_18 = twentyOne_1040_16 + twentyOne_1040_17
    twentyOne_1040_19 = instructions_data['twenty_twenty_one_child_and_other_dependent_credit_per_computer']
    twentyOne_1040_20 = 0
    # =AB57+AB58
    twentyOne_1040_21 = twentyOne_1040_19 + twentyOne_1040_20

    # =IF(AB56-AB59<0,0,AB56-AB59)
    twentyOne_1040_22 = 0
    if twentyOne_1040_18 - twentyOne_1040_21 < 0:
        twentyOne_1040_22 = 0
    else:
        twentyOne_1040_22 = twentyOne_1040_18 - twentyOne_1040_21

    twentyOne_1040_23 = instructions_data['twenty_twenty_one_SE_tax']

    # =AB60+AB61
    twentyOne_1040_24 = twentyOne_1040_22 + twentyOne_1040_23
    twentyOne_1040_25a = 0
    twentyOne_1040_25b = 0
    twentyOne_1040_25c = 0
    twentyOne_1040_25d = 0
    twentyOne_1040_26 = instructions_data['twenty_twenty_one_applied_to_next_years_estimated_tax']
    twentyOne_1040_27a = instructions_data['twenty_twenty_one_earned_income_credit']
    twentyOne_1040_28 = instructions_data['twenty_twenty_one_schedule_8812_additional_child_tax_credit']
    twentyOne_1040_29 = instructions_data['twenty_twenty_one_total_education_credit_amount_per_computer']
    twentyOne_1040_30 = instructions_data['twenty_twenty_one_recovery_rebate_credit_per_computer']
    twentyOne_1040_31 = data_sch_3_21['data_sch_3_21_15']
    twentyOne_1040_32 = twentyOne_1040_27a + twentyOne_1040_28 + twentyOne_1040_29 + twentyOne_1040_30 + twentyOne_1040_31

    # =AB67+AB68+AB79
    twentyOne_1040_33 = twentyOne_1040_25d + twentyOne_1040_26 + twentyOne_1040_32

    # =IF(AB80>AB62,AB80-AB62,0)
    twentyOne_1040_34 = twentyOne_1040_33 - twentyOne_1040_24 if twentyOne_1040_33 > twentyOne_1040_24 else 0

    twentyOne_1040_35a = twentyOne_1040_34

    twentyOne_1040_36 = 0

    # =IF(AB81=0,AB62-AB80,0)
    twentyOne_1040_37 = 0
    if twentyOne_1040_34 == 0:
        twentyOne_1040_37 = twentyOne_1040_24 - twentyOne_1040_33
    else:
        twentyOne_1040_37 = 0
    
    twentyOne_1040_38 = instructions_data['twenty_twenty_one_estimated_tax_penalty']
    
    # 34b
    # =IF(AB81-'2021 7202'!H111-'2021 7202'!H112<=0,"N/A",AB81-'2021 7202'!H111-'2021 7202'!H112)
    # this is wrong: data_twentyOne_schd3_14['data_twentyOne_schd3_14']
    twentyOne_1040_34b = 0
    if twentyOne_1040_34 - data_sch_3_21['data_sch_3_21_14']<= 0:
        twentyOne_1040_34b = "N/A"
    else:
        twentyOne_1040_34b = twentyOne_1040_34 - data_sch_3_21['data_sch_3_21_14']
    
    if twentyOne_1040_34b == "N/A":
        twentyOne_1040_37b = twentyOne_1040_24 - twentyOne_1040_33 + data_7202_21['data_7202_21_sch_3_13b'] + data_7202_21['data_7202_21_sch_3_13h'] + twentyOne_1040_38
    else:
        twentyOne_1040_37b = 0

    data_1040_21 = {
        "data_1040_21_1": twentyOne_1040_1,
        "data_1040_21_2a": twentyOne_1040_2a,
        "data_1040_21_3a": twentyOne_1040_3a,
        "data_1040_21_4a": twentyOne_1040_4a,
        "data_1040_21_5a": twentyOne_1040_5a,
        "data_1040_21_6a": twentyOne_1040_6a,
        "data_1040_21_7": twentyOne_1040_7,
        "data_1040_21_8": twentyOne_1040_8,
        "data_1040_21_9": twentyOne_1040_9,
        "data_1040_21_10": twentyOne_1040_10,
        "data_1040_21_11": twentyOne_1040_11,
        "data_1040_21_12a": twentyOne_1040_12a,
        "data_1040_21_12b": twentyOne_1040_12b,
        "data_1040_21_12c": twentyOne_1040_12c,
        "data_1040_21_13": twentyOne_1040_13,
        "data_1040_21_14": twentyOne_1040_14,
        "data_1040_21_15": twentyOne_1040_15,
        "data_1040_21_16": twentyOne_1040_16,
        "data_1040_21_17": twentyOne_1040_17,
        "data_1040_21_18": twentyOne_1040_18,
        "data_1040_21_19": twentyOne_1040_19,
        "data_1040_21_20": twentyOne_1040_20,
        "data_1040_21_21": twentyOne_1040_21,
        "data_1040_21_22": twentyOne_1040_22,
        "data_1040_21_23": twentyOne_1040_23,
        "data_1040_21_24": twentyOne_1040_24,
        "data_1040_21_25a": twentyOne_1040_25a,
        "data_1040_21_25b": twentyOne_1040_25b,
        "data_1040_21_25c": twentyOne_1040_25c,
        "data_1040_21_25d": twentyOne_1040_25d,
        "data_1040_21_26": twentyOne_1040_26,
        "data_1040_21_27a": twentyOne_1040_27a,
        "data_1040_21_28": twentyOne_1040_28,
        "data_1040_21_29": twentyOne_1040_29,
        "data_1040_21_30": twentyOne_1040_30,
        "data_1040_21_31": twentyOne_1040_31,
        "data_1040_21_32": twentyOne_1040_32,
        "data_1040_21_33": twentyOne_1040_33,
        "data_1040_21_34": twentyOne_1040_34,
        "data_1040_21_34b": twentyOne_1040_34b,
        "data_1040_21_35a": twentyOne_1040_35a,
        "data_1040_21_36": twentyOne_1040_36,
        "data_1040_21_37": twentyOne_1040_37,
        "data_1040_21_37b": twentyOne_1040_37b,
        "data_1040_21_38": twentyOne_1040_38
    }

    return data_1040_21


def get_1040x_21_data(data_variables):
    #1040X Extra Data Variables
    data_sch_3_21 = get_sch_3_21_data(data_variables)
    data_1040_21 = get_1040_21_data(data_variables)

    twentyOne_Orig_1040_28 = data_1040_21['data_1040_21_28']
    twentyOne_Orig_1040_29 = data_1040_21['data_1040_21_29']
    twentyOne_Orig_1040_30 = data_1040_21['data_1040_21_30']
    twentyOne_Orig_1040_31 = data_sch_3_21['data_sch_3_21_14']
    twentyOne_Orig_1040_37 = data_1040_21['data_1040_21_37b']
    Orig_1040_twentyOne_38 = data_1040_21['data_1040_21_38']

    twentyOne_1040x_11a = data_1040_21['data_1040_21_24']
    twentyOne_1040x_11c = twentyOne_1040x_11a
    twentyOne_1040x_12a = data_1040_21['data_1040_21_25d']
    twentyOne_1040x_12c = twentyOne_1040x_12a
    twentyOne_1040x_13a = data_1040_21['data_1040_21_26']
    twentyOne_1040x_13c = twentyOne_1040x_13a
    twentyOne_1040x_14a = data_1040_21['data_1040_21_27a']
    twentyOne_1040x_14c = twentyOne_1040x_14a
    twentyOne_1040x_15a = data_1040_21['data_1040_21_28'] + data_1040_21['data_1040_21_29'] + data_1040_21['data_1040_21_30']
    twentyOne_1040x_15b = twentyOne_Orig_1040_31
    twentyOne_1040x_15c = twentyOne_1040x_15a + twentyOne_1040x_15b

    # =IF(J44-J45+J49<=0,0,J44-J45+J49)
    if twentyOne_Orig_1040_37 - Orig_1040_twentyOne_38 <= 0:
        twentyOne_1040x_16 = 0
    else:
        twentyOne_1040x_16 = twentyOne_Orig_1040_37 - Orig_1040_twentyOne_38
    twentyOne_1040x_16 = 0 if twentyOne_Orig_1040_37 - Orig_1040_twentyOne_38 <= 0 else twentyOne_Orig_1040_37 - Orig_1040_twentyOne_38

    twentyOne_1040x_17 = twentyOne_1040x_12c + twentyOne_1040x_13c + twentyOne_1040x_14c + twentyOne_1040x_15c

    # twenty_1040_18 = 0 if twenty1040_34 - Total_2020_Credit <= 0 else twenty1040_34 - Total_2020_Credit
    twentyOne_1040x_18 = data_1040_21['data_1040_21_34'] - data_1040_21['data_1040_21_31']
    # =S29-S30
    twentyOne_1040x_19 = abs(twentyOne_1040x_17 - twentyOne_1040x_18)

    # =IF(S23>S31,S23-S31,0)
    twentyOne_1040x_20 = twentyOne_1040x_11c - twentyOne_1040x_19 if twentyOne_1040x_11c > twentyOne_1040x_19 else 0

    # =IF(S23<S31,S31-S23,0)
    twentyOne_1040x_21 = twentyOne_1040x_19 - twentyOne_1040x_11c if twentyOne_1040x_11c < twentyOne_1040x_19 else 0
    # Define twenty_1040_2
    twentyOne_1040x_22 = 0 if twentyOne_1040x_21 <= 0 else twentyOne_1040x_21

    cal_check_21 = False
    if twentyOne_1040x_15b == twentyOne_1040x_21 and twentyOne_1040x_15b  == twentyOne_1040x_22:
        cal_check_21 = True
    else:
        pass

    data_1040x_21 = {
        "data_1040x_21_original_1": '',
        "data_1040x_21_correct_1": '',
        "data_1040x_21_original_2": '',
        "data_1040x_21_correct_2": '',
        "data_1040x_21_original_3": '',
        "data_1040x_21_correct_3": '',
        "data_1040x_21_original_4a": '',
        "data_1040x_21_correct_4a": '',
        "data_1040x_21_original_4b": '',
        "data_1040x_21_correct_4b": '',
        "data_1040x_21_original_5": '',
        "data_1040x_21_correct_5": '',
        "data_1040x_21_original_6": '',
        "data_1040x_21_correct_6": '',
        "data_1040x_21_original_7": '',
        "data_1040x_21_correct_7": '',
        "data_1040x_21_original_8": '',
        "data_1040x_21_correct_8": '',
        "data_1040x_21_original_9": '',
        "data_1040x_21_correct_9": '',
        "data_1040x_21_original_10": '',
        "data_1040x_21_correct_10": '',
        "data_1040x_21_original_11": twentyOne_1040x_11a,
        "data_1040x_21_correct_11": twentyOne_1040x_11c,
        "data_1040x_21_original_12": twentyOne_1040x_12a,
        "data_1040x_21_correct_12": twentyOne_1040x_12c,
        "data_1040x_21_original_13": twentyOne_1040x_13a,
        "data_1040x_21_correct_13": twentyOne_1040x_13c,
        "data_1040x_21_original_14": twentyOne_1040x_14a,
        "data_1040x_21_correct_14": twentyOne_1040x_14c,
        "data_1040x_21_original_15": twentyOne_1040x_15a,
        "data_1040x_21_correct_15": twentyOne_1040x_15c,
        "data_1040x_21_change_15": twentyOne_1040x_15b,
        "data_1040x_21_correct_16": twentyOne_1040x_16,
        "data_1040x_21_correct_17": twentyOne_1040x_17,
        "data_1040x_21_correct_18": abs(twentyOne_1040x_18),
        "data_1040x_21_correct_19": twentyOne_1040x_19,
        "data_1040x_21_correct_20": twentyOne_1040x_20,
        "data_1040x_21_correct_21": twentyOne_1040x_21,
        "data_1040x_21_correct_22": twentyOne_1040x_22,
        "data_1040x_21_23": '',
        "data_1040x_21_28": twentyOne_Orig_1040_28,
        "data_1040x_21_29": twentyOne_Orig_1040_29,
        "data_1040x_21_30": twentyOne_Orig_1040_30,
        "data_1040x_21_31": twentyOne_Orig_1040_31,
        "data_1040x_21_37": twentyOne_Orig_1040_37,
        "data_1040x_21_38": Orig_1040_twentyOne_38,
        "data_1040x_21_org_sch_3_10": '',
        "cal_check_21": cal_check_21
    }


    return data_1040x_21


