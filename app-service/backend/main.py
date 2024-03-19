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
import math
from utility import *
from tenacity import retry, stop_after_attempt, wait_exponential

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

db_7202_20_url = os.getenv('db_7202_20_url')
db_sch_3_20_url = os.getenv('db_sch_3_20_url')
db_1040_20_url = os.getenv('db_1040_20_url')
db_1040x_20_url = os.getenv('db_1040x_20_url')

db_7202_21_url = os.getenv('db_7202_21_url')
db_sch_3_21_url = os.getenv('db_sch_3_21_url')
db_1040_21_url = os.getenv('db_1040_21_url')
db_1040x_21_url = os.getenv('db_1040x_21_url')

gsheet_scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
gsheet_creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", gsheet_scope)
gsheet_client = gspread.authorize(gsheet_creds)
  

app = Flask(__name__)
CORS(app)




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

            cell = sheet.find(email, in_column=sheet.find("Email").col) 
            time.sleep(1)

            if cell:  
                status_cell = sheet.cell(cell.row, status_column.col)
                if not status_cell.value:
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
    

@app.route('/fill_calculation_sheet', methods=['POST'])
def fill_calculation_sheet():
    try:
        data = request.json
        sheet_name = data['sheet_name']
        page = data['page']
        per_page = data['per_page']
        offset = data['offset']
    except KeyError:
        return {"message": "Required data not provided in JSON request"}, 400

    @retry(
        stop=stop_after_attempt(3), 
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    def make_get_request(url):
        response = requests.get(url)
        response.raise_for_status()
        return response

    try:
        total_count_response = make_get_request("https://xyrm-sqqj-hx6t.n7c.xano.io/api:zFwSjuSC/get_taxStatus_count")
        total_count = total_count_response.json()

        total_pages = math.ceil(total_count / per_page)

        while page <= total_pages:
            final_result_response = make_get_request(
                f"https://xyrm-sqqj-hx6t.n7c.xano.io/api:zFwSjuSC/get_taxStatus_data?page={page}&per_page={per_page}&offset={offset}")
            final_result = final_result_response.json()

            first_name = final_result.get('items', [])[0].get('First_Name', '')
            last_name = final_result.get('items', [])[0].get('Last_Name', '')
            email = final_result.get('items', [])[0].get('Email', '')

            response_email_exists = make_get_request(
                f"https://xyrm-sqqj-hx6t.n7c.xano.io/api:zFwSjuSC/has_email_21_1040x?email={email}")
            response_email_exists_2020 = make_get_request(f"https://xyrm-sqqj-hx6t.n7c.xano.io/api:zFwSjuSC/email_exists_2020_7202?email={email}")

            email_exists = response_email_exists.json()
            email_exists_20 = response_email_exists_2020.json()

            if email_exists == True or email_exists_20 == True:
                print(f"Skipping {page}, email already exists")
                page += 1
                continue

            data_variables = extract_data_keys_and_values(final_result)

            place_data_variables(sheet_name, data_variables)

            sheet_20 = gsheet_client.open(sheet_name).get_worksheet(1)
            try:
                data_total_2020_credit = sheet_20.cell(49, 36).value.strip()
            except AttributeError:
                data_total_2020_credit = ''

            sheet_21 = gsheet_client.open(sheet_name).get_worksheet(5)

            try:
                data_total_2021_credit = sheet_21.cell(112, 8).value.strip()
            except AttributeError:
                data_total_2021_credit = ''

            try:
                data_total_2021_credit_2 = sheet_21.cell(111, 8).value.strip()
            except AttributeError:
                data_total_2021_credit_2 = ''

            if data_total_2020_credit != '-':
                print(f"Processing year 2020 page={page}")

                data_7202_20 = get_7202_20_data(sheet_name)
                payload_7202_20 = {
                    "First_Name": first_name,
                    "Last_Name": last_name,
                    "Email": email,
                    "result": data_7202_20
                }

                requests.post(db_7202_20_url, json=payload_7202_20)

                data_sch_3_20 = get_sch_3_20_data(sheet_name)

                payload_sch_3_20 = {
                    "First_Name": first_name,
                    "Last_Name": last_name,
                    "Email": email,
                    "result": data_sch_3_20
                }

                requests.post(db_sch_3_20_url, json=payload_sch_3_20)

                data_1040_20 = get_1040_20_data(sheet_name)

                payload_1040_20 = {
                    "First_Name": first_name,
                    "Last_Name": last_name,
                    "Email": email,
                    "result": data_1040_20
                }

                requests.post(db_1040_20_url, json=payload_1040_20)

                data_1040x_20 = get_1040x_20_data(sheet_name)

                payload_1040x_20 = {
                    "First_Name": first_name,
                    "Last_Name": last_name,
                    "Email": email,
                    "result": data_1040x_20
                }

                requests.post(db_1040x_20_url, json=payload_1040x_20)

            if data_total_2021_credit != '-' or data_total_2021_credit_2 != '-':
                print(f"Processing year 2021 page={page}")
                data_7202_21 = get_7202_21_data(sheet_name)

                payload_7202_21 = {
                    "First_Name": first_name,
                    "Last_Name": last_name,
                    "Email": email,
                    "result": data_7202_21
                }

                requests.post(db_7202_21_url, json=payload_7202_21)

                data_sch_3_21 = get_sch_3_21_data(sheet_name)

                payload_sch_3_21 = {
                    "First_Name": first_name,
                    "Last_Name": last_name,
                    "Email": email,
                    "result": data_sch_3_21
                }

                requests.post(db_sch_3_21_url, json=payload_sch_3_21)

                data_1040_21 = get_1040_21_data(sheet_name)

                payload_1040_21 = {
                    "First_Name": first_name,
                    "Last_Name": last_name,
                    "Email": email,
                    "result": data_1040_21
                }

                requests.post(db_1040_21_url, json=payload_1040_21)

                data_1040x_21 = get_1040x_21_data(sheet_name)

                payload_1040x_21 = {
                    "First_Name": first_name,
                    "Last_Name": last_name,
                    "Email": email,
                    "result": data_1040x_21
                }

                requests.post(db_1040x_21_url, json=payload_1040x_21)

            page += 1

    except requests.exceptions.RequestException as e:
        return {"message": f"Request failed: {e}"}, 500
    except Exception as e:
        return {"message": f"An unexpected error occurred: {e}"}, 500

    return {'message': 'Data added to the dbs'}


if __name__ == '__main__':
    app.run(debug=True)