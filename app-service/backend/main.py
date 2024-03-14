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
import time
from PyPDF2 import PdfFileMerger

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
  

app = Flask(__name__)
CORS(app)


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


@app.route('/process_users',methods=['POST'])
def process_user():
    try:
        data = request.json
        sheet_name = data.get("sheet_name")
        if isinstance(data, dict):            
            data_list = data.get("uniquePreQualifiedLeadsList", [])
        elif isinstance(data, list):
            data_list = data
        else:
            return jsonify({"error": "Invalid JSON format"}, 400)

    except Exception as e:
        return jsonify({"error": "Invalid JSON format", "message": str(e)}, 400)
    

    sheet = gsheet_client.open(sheet_name).sheet1
    if sheet.row_count == 0:
        headers = ["First Name", "Last Name", "Email", "PDF 1", "PDF 2", "Refund 2020", "Refund 2021","Status/Stage","Referral Source"]
        sheet.append_row(headers)  

    for user in data_list:
        try:
            email = user.get('Email', '')

            if email in sheet.col_values(3):
                print(f'{email} exists already')
                time.sleep(1.2)
                continue

            if email:
                api_url = f'http://ltt.aip.global.bizopsaip.com/flow/api/flow-rest-selfauth/getTaxCaculation?Email={email}'
                response = requests.get(api_url)
                tax_data = response.json()

                tax_data = tax_data['taxCaculationReturn']
        
                first_name = user.get('First_Name', '')
                last_name = user.get('Last_Name', '')
                status = user.get('Stage','')
                referral = user.get('Lead_Source','')

                try:
                    pdf_file_name1 = email +  "_" + tax_data['UploadFile2020Local']["resources"][0]['fileName']
                except:
                    pdf_file_name1 = ''

                try:
                    pdf_url1 = tax_data['UploadFile2020Local']["resources"][0]['url']
                    s3_pdf1 = upload_pdf_to_s3(pdf_url1,pdf_file_name1)
                except:
                    pdf_url1 = ''
                    s3_pdf1 = ''

                try:
                    pdf_file_name2 = email +  "_" + tax_data['UploadFile2021Local']["resources"][0]['fileName']
                except:
                    pdf_file_name2 = ''

                try:
                    pdf_url2 = tax_data['UploadFile2021Local']["resources"][0]['url']
                    s3_pdf2 = upload_pdf_to_s3(pdf_url2,pdf_file_name2)
                except:
                    pdf_url2 = ''
                    s3_pdf2 = ''                

                try:
                    refund_2020 = json.loads(tax_data['calculateOutput']['longText'])
                    refund_2020 = refund_2020['Result_2020_1040X']['Refund_or_Amount_you_Owe_22C']
                except:
                    refund_2020 = ''

                try:
                    refund_2021 = json.loads(tax_data['calculateOutput']['longText'])
                    refund_2021 = refund_2021['Result_2021_1040X']['Refund_or_Amount_you_Owe_22C']
                except:
                    refund_2021 = ''
                
                row_data = [first_name, last_name, email, s3_pdf1, s3_pdf2, refund_2020, refund_2021,status,referral]
                sheet.append_row(row_data)

        except Exception as e:
            return {'status': 'error', 'message': str(e)}
        
    return {'status': 'success'}


@app.route('/merge_pdf', methods=['POST'])
def merge_pdf():

    try:
        try:
            data = request.json
        except:
            return {"error": "no json found"}

        merge_url_1 = data.get('merge_url_1')
        merge_url_2 = data.get('merge_url_2')
        sheet_name = data.get('sheet_name')

        sheet = gsheet_client.open(sheet_name).sheet1

        row_number = 2
        for row in sheet.get_all_records():
            first_name = row.get('First Name')
            last_name = row.get('Last Name')
            pdf_1_url = row.get('PDF 1')
            pdf_2_url = row.get('PDF 2')
            merge1_value = row.get('Merge1')
            merge2_value = row.get('Merge2')
            output1_value = row.get('Output1')
            output2_value = row.get('Output2')

            print(first_name)
            print(last_name)
            print(pdf_1_url)
            print(pdf_2_url)

            if pdf_1_url and not merge1_value and not output1_value:
                pdf_1 = BytesIO(requests.get(pdf_1_url).content)
                merger = PdfFileMerger()
                merger.append(BytesIO(requests.get(merge_url_1).content))
                merger.append(pdf_1)
                merged_pdf_1_content = BytesIO()
                merger.write(merged_pdf_1_content)

                s3_url_1 = upload_pdf_to_s3_2(merged_pdf_1_content.getvalue(), f"{first_name.replace(' ','_')}_{last_name.replace(' ','_')}_merged_pdf_1.pdf")
                sheet.update_cell(row_number, sheet.find('Output1').col, s3_url_1)
                sheet.update_cell(row_number, sheet.find('Merge1').col, merge_url_1)

            if pdf_2_url and not merge2_value and not output2_value:
                pdf_2 = BytesIO(requests.get(pdf_2_url).content)
                merger = PdfFileMerger()
                merger.append(BytesIO(requests.get(merge_url_2).content))
                merger.append(pdf_2)
                merged_pdf_2_content = BytesIO()
                merger.write(merged_pdf_2_content)

                s3_url_2 = upload_pdf_to_s3_2(merged_pdf_2_content.getvalue(), f"{first_name.replace(' ','_')}_{last_name.replace(' ','_')}_merged_pdf_2.pdf")
                sheet.update_cell(row_number, sheet.find('Output2').col, s3_url_2)
                sheet.update_cell(row_number, sheet.find('Merge2').col, merge_url_2)        

            row_number += 1
    except Exception as e:
        return jsonify({"error":e})

    return jsonify({"message": "PDFs merged, uploaded to S3, and Google Sheet updated successfully."})


@app.route('/update_status_if_empty', methods=['POST'])
def update_status_if_empty_endpoint():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data found in the request body"}), 400
        

        sheet_name = data.get('sheet_name')
        sheet = gsheet_client.open(sheet_name).sheet1
        status_column = sheet.find('Status/Stage')

        for row_data in data['data']:
            email = row_data.get('Email')
            stage = row_data.get('Stage')

            cell = sheet.find(email, in_column=sheet.find("Email").col)  # Find the cell containing the email
            time.sleep(1)

            if cell:  # If the email is found in the sheet
                status_cell = sheet.cell(cell.row, status_column.col)
                if not status_cell.value:  # Check if the 'Status' column is empty
                    sheet.update_cell(cell.row, status_column.col, stage)


        return jsonify({"message": "Status updated successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/update_referral_if_empty', methods=['POST'])
def update_referral_if_empty_endpoint():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data found in the request body"}), 400
        

        sheet_name = data.get('sheet_name')
        sheet = gsheet_client.open(sheet_name).sheet1
        referral_column = sheet.find('Referral Source')

        for row_data in data['data']:
            email = row_data.get('Email')
            referral = row_data.get('Lead_Source','')

            cell = sheet.find(email, in_column=sheet.find("Email").col)
            time.sleep(1.3)

            if cell:  
                referral_cell = sheet.cell(cell.row, referral_column.col)
                if not referral_cell.value: 
                    sheet.update_cell(cell.row, referral_column.col, referral)


        return jsonify({"message": "Status updated successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/process_taxStatus', methods=['POST'])
def process_taxStatus():
    token_response = requests.post(taxStatus_token_url, data={
        'grant_type': 'client_credentials',
        'client_id': taxStatus_client_id,
        'client_secret': taxStatus_client_secret,
        'scope': taxStatus_scope
    })

    if token_response.status_code == 200:
        access_token = token_response.json().get('access_token')

        resolve_api_url = 'https://api.taxstatus.net/api/taxdata/v1/resolvetp'
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'euid': taxStatus_euid,
            'Content-Type': 'application/json'
        }

        request_data = request.json

        resolve_api_response = requests.post(resolve_api_url, headers=headers, json=request_data)

        if resolve_api_response.status_code == 200:
            data = resolve_api_response.json()

            first_name = request_data.get('firstName','')
            last_name = request_data.get('lastName','')
            email = request_data.get('email','')
            companyId = request_data['companyId']
            tin = data['ClientId']

            result = {}

            year_transcript_data = {
                "2019": ["ACTR", "RECA"],
                "2020": ["ACTR", "RECA"],
                "2021": ["ACTR", "RECA"]
            }

            transcript_api_url = 'https://api.taxstatus.net/api/taxdata/v1/transcriptdetail'

            for year, transcript_types in year_transcript_data.items():
                for transcript_type in transcript_types:
                    data_year_transcript = {
                        "companyId": companyId,
                        "tin": tin,
                        "transcriptType": transcript_type,
                        "transcriptForm": "1040",
                        "transcriptPeriod": year + "12"
                    }

                    transcript_api_response = requests.post(transcript_api_url, headers=headers, json=data_year_transcript)
                    result[year + "_" + transcript_type] = transcript_api_response.json()

            final_result = {
                "First_Name": first_name,
                "Last_Name": last_name,
                "Email": email,
                "result": result
            }

            return jsonify(final_result), resolve_api_response.status_code
        else:
            return jsonify({'error': 'Failed to resolve TP'}), resolve_api_response.status_code
    else:
        return jsonify({'error': 'Failed to obtain access token'}), token_response.status_code




if __name__ == '__main__':
    app.run(debug=True)