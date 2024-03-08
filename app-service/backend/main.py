from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import boto3
import json
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv


load_dotenv()

s3_access_key = os.getenv('s3_access_key')
s3_secret_key = os.getenv('s3_secret_key')
s3_bucket_name = os.getenv('s3_bucket_name')
s3_bucket_region = os.getenv('s3_bucket_region')
gsheet_scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
gsheet_creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", gsheet_scope)
gsheet_client = gspread.authorize(gsheet_creds)

sheet = gsheet_client.open("SETCPRO-D1-March").sheet1

if sheet.row_count == 0:
    headers = ["First Name", "Last Name", "Email", "PDF 1", "PDF 2", "Refund 2020", "Refund 2021"]
    sheet.append_row(headers)    

app = Flask(__name__)
CORS(app)


@app.route('/process_users',methods=['POST'])
def process_user():
    try:
        data = request.json
    except:
        return jsonify({"error": "Invalid JSON format"},400)

    for user in data["uniquePreQualifiedLeadsList"]:
        try:
            email = user.get('Email', '')
            if email:
                api_url = f'http://ltt.aip.global.bizopsaip.com/flow/api/flow-rest-selfauth/getTaxCaculation?Email={email}'
                response = requests.get(api_url)
                tax_data = response.json()

                tax_data = tax_data['taxCaculationReturn']
        
                first_name = user.get('First_Name', '')
                last_name = user.get('Last_Name', '')

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
                
                row_data = [first_name, last_name, email, s3_pdf1, s3_pdf2, refund_2020, refund_2021]
                sheet.append_row(row_data)

                print(email)
                print(first_name)
                print(last_name)
                print(s3_pdf1)
                print(s3_pdf2)
                print(refund_2020)
                print(refund_2021)

        except Exception as e:
            return {'status': 'error', 'message': str(e)}
        
    return {'status': 'success'}    


def upload_pdf_to_s3(pdf_url,pdf_file_name):

    pdf_content = requests.get(pdf_url).content        
    s3_client = boto3.client('s3', aws_access_key_id=s3_access_key, aws_secret_access_key=s3_secret_key)
    s3_key = pdf_file_name
    s3_client.put_object(Body=pdf_content, Bucket= s3_bucket_name, Key=s3_key, ContentType='application/pdf')
        

    s3_url = f'https://setcpro-automate-boring.s3.us-east-2.amazonaws.com/{s3_key}'    
    return s3_url

if __name__ == '__main__':
    app.run(debug=True)