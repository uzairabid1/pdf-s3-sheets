import os
import requests
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




BASE_URL = "https://api.pdf.co/v1"

SourceFileUrl = "https://setcpro-automate-boring.s3.us-east-2.amazonaws.com/form_2020_merged_final_output.pdf"

DestinationFile = ".\\result.pdf"

Async = "False"


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

def combine_fields_21(data_variables_1040_21,data_variables_1040x_21,data_variables_7202_21,data_variables_sch_3_21):
    
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
        "first_name_1040": "0;first_name_1040",
        "last_name_1040": "0;last_name_1040",

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
    "first_name_1040x": "2;first_name_1040x",
    "last_name_1040x": "2;last_name_1040x",
    "explain_of_changes": "3;explain_of_changes",
    "data_checkbox": "2;data_checkbox;true",
    "data_1040x_21_check_field": "2;data_1040x_21_check_field"
}

    pdf_fields_7202_21 = {
    "data_7202_21_1": "4;data_7202_21_1",
    "data_7202_21_2": "4;data_7202_21_2",
    "data_7202_21_3a": "4;data_7202_21_3a",
    "data_7202_21_3b": "4;data_7202_21_3b",
    "data_7202_21_3c": "4;data_7202_21_3c",
    "data_7202_21_3d": "4;data_7202_21_3d",
    "data_7202_21_4a": "4;data_7202_21_4a",
    "data_7202_21_5": "4;data_7202_21_5",
    "data_7202_21_6a": "4;data_7202_21_6a",
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
    "data_7202_21_39": "5;data_7202_21_39",
    "data_7202_21_40a": "5;data_7202_21_40a",
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
    "name_7202" : "4;name_7202"
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

def main(args = None):
    fillPDFForm(SourceFileUrl, DestinationFile)


def fillPDFForm(uploadedFileUrl, destinationFile):

    response_user_list = requests.get("https://xyrm-sqqj-hx6t.n7c.xano.io/api:zFwSjuSC/get_users")
    
    user_list = response_user_list.json()

    for user in user_list:
        email = user.get("Email","")    

        print(email)

        email_exists_7202_response = requests.get(f"https://xyrm-sqqj-hx6t.n7c.xano.io/api:zFwSjuSC/email_exists_2020_7202?email={email}")
        email_exists_1040_response= requests.get(f"https://xyrm-sqqj-hx6t.n7c.xano.io/api:zFwSjuSC/email_exists_2020_1040?email={email}")
        email_exists_1040x_response = requests.get(f"https://xyrm-sqqj-hx6t.n7c.xano.io/api:zFwSjuSC/email_exists_1040x?email={email}")
        email_exists_sch_3_response = requests.get(f"https://xyrm-sqqj-hx6t.n7c.xano.io/api:zFwSjuSC/email_exists_2020_sch_3?email={email}")

        email_exists_7202 = email_exists_7202_response.json()
        email_exists_1040 = email_exists_1040_response.json()
        email_exists_1040x = email_exists_1040x_response.json()
        email_exists_sch_3 = email_exists_sch_3_response.json()

        if email_exists_1040 and email_exists_1040x and email_exists_7202 and email_exists_sch_3:
                response_1040 =  requests.get(f"https://xyrm-sqqj-hx6t.n7c.xano.io/api:Dga0jXwg/get_1040_20_email?email={email}")
                response_1040x = requests.get(f"https://xyrm-sqqj-hx6t.n7c.xano.io/api:Dga0jXwg/get_1040x_20_email?email={email}")
                response_7202 =  requests.get(f"https://xyrm-sqqj-hx6t.n7c.xano.io/api:Dga0jXwg/get_7202_email?email={email}")
                response_sch_3 = requests.get(f"https://xyrm-sqqj-hx6t.n7c.xano.io/api:Dga0jXwg/get_sch_3_20_email?email={email}")

                data_variables_1040_20 = response_1040.json()
                data_variables_1040x_20 = response_1040x.json()
                data_variables_7202_20 = response_7202.json()
                data_variables_sch_3_20 = response_sch_3.json()

                FieldsStrings = combine_fields(data_variables_1040_20, data_variables_1040x_20, data_variables_7202_20, data_variables_sch_3_20)

                parameters = {}
                parameters["name"] = os.path.basename(destinationFile)
                parameters["url"] = uploadedFileUrl
                parameters["fieldsString"] = FieldsStrings
                parameters["async"] = Async

                url = "{}/pdf/edit/add".format(BASE_URL)

                response = requests.post(url, data=parameters, headers={"x-api-key": API_KEY})
                if response.status_code == 200:
                    json_data = response.json()

                    if not json_data["error"]:
                        resultFileUrl = json_data["url"]
                        s3_url = upload_pdf_to_s3(resultFileUrl, os.path.basename(destinationFile))
                        print(f"Result file saved to S3 and URL is: {s3_url}")
                        break
                    else:
                        print(json_data["message"])
                else:
                    print(f"Request error: {response.status_code} {response.reason}")
        else:
            print(f'skipping {email}')
            continue



def upload_pdf_to_s3(pdf_url, pdf_file_name):
    pdf_content = requests.get(pdf_url).content
    s3_client = boto3.client('s3', aws_access_key_id=s3_access_key, aws_secret_access_key=s3_secret_key)
    s3_key = pdf_file_name
    s3_client.put_object(Body=pdf_content, Bucket=s3_bucket_name, Key=s3_key, ContentType='application/pdf')

    s3_url = f'https://{s3_bucket_name}.s3.amazonaws.com/{s3_key}'
    return s3_url        

if __name__ == '__main__':
    fillPDFForm(SourceFileUrl, "filled_pdf.pdf")