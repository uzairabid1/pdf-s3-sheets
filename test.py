import os
import requests


API_KEY = "ben@automateboring.net_MuC2b1kLoT6q59O4CygKR64aS0oUN8v6h9kTdb43vV7WKNpv1M30a9L9PKW57W8M2qkXkU4DP67CuZ9lL1I27ZC4FF7H9H61bkG062L1bUZT7kpH233cJHi3dudENR3ckELQ5DE59wPrR34ckq77655499"

BASE_URL = "https://api.pdf.co/v1"

SourceFileUrl = "https://setcpro-automate-boring.s3.us-east-2.amazonaws.com/form_2020_merged_final2.pdf"

DestinationFile = ".\\result.pdf"

Async = "False"

def combine_fields(data_variables,data_variables_1040x_20,data_variables_7202_20,data_variables_sch_3_20):

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
        "data_1040x_20_15_field": f"3;topmostSubform[0].Page1[0].Table_Payments[0].Line15[0].Refundable[0].f1_63[0];7202",
        "data_1040x_20_15_checkbox": f"2;topmostSubform[0].Page1[0].Table_Payments[0].Line15[0].Refundable[0].c1_12[0];true",
        "data_1040x_20_firstName": f"2;topmostSubform[0].Page1[0].firstName1040x[0]",
        "data_1040x_20_lastName": f"2;topmostSubform[0].Page1[0].lastName1040x[0]"
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
        "data_sch_3_20_name": f"5;topmostSubform[0].Page1[0].name_sch_3[0]"
    }

    combined_values = []

    for key, value in pdf_fields_1040_20.items():
        val = data_variables.get(key, "")

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

def main(args = None):
    fillPDFForm(SourceFileUrl, DestinationFile)


def fillPDFForm(uploadedFileUrl, destinationFile):

    data_variables_1040_20 = {
        "data_1040_20_1": "155,187",
        "data_1040_20_7": "-",
        "data_1040_20_8": "-",
        "data_1040_20_9": "201,547",
        "data_1040_20_11": "201,547",
        "data_1040_20_12": "-",
        "data_1040_20_13": "-",
        "data_1040_20_14": "-",
        "data_1040_20_15": "201,547",
        "data_1040_20_16": "29,865",
        "data_1040_20_17": "-",
        "data_1040_20_18": "29,865",
        "data_1040_20_19": "-",
        "data_1040_20_20": "-",
        "data_1040_20_21": "-",
        "data_1040_20_22": "29,865",
        "data_1040_20_23": "-",
        "data_1040_20_24": "29,865",
        "data_1040_20_26": "-",
        "data_1040_20_27": "-",
        "data_1040_20_28": "-",
        "data_1040_20_29": "-",
        "data_1040_20_2a": "-",
        "data_1040_20_2b": "-",
        "data_1040_20_30": "-",
        "data_1040_20_31": "13,710",
        "data_1040_20_32": "13,710",
        "data_1040_20_33": "13,710",
        "data_1040_20_34": "-",
        "data_1040_20_36": "",
        "data_1040_20_37": "16,155",
        "data_1040_20_38": "56",
        "data_1040_20_3a": "-",
        "data_1040_20_3b": "-",
        "data_1040_20_4a": "-",
        "data_1040_20_4b": "-",
        "data_1040_20_5a": "213,861",
        "data_1040_20_5b": "46,360",
        "data_1040_20_6a": "-",
        "data_1040_20_6b": "-",
        "data_1040_20_10a": "-",
        "data_1040_20_10b": "-",
        "data_1040_20_10c": "-",
        "data_1040_20_25a": "-",
        "data_1040_20_25b": "-",
        "data_1040_20_25c": "-",
        "data_1040_20_25d": "-",
        "data_1040_20_35a": "-"
    }

    data_variables_1040x_20 = {
        "data_1040x_20_23": "",
        "data_1040x_20_28": "-",
        "data_1040x_20_29": "-",
        "data_1040x_20_30": "-",
        "data_1040x_20_31": "15,110",
        "data_1040x_20_37": "29,921",
        "data_1040x_20_38": "56",
        "data_1040x_20_change_15": "15,110",
        "data_1040x_20_correct_1": "",
        "data_1040x_20_correct_2": "",
        "data_1040x_20_correct_3": "",
        "data_1040x_20_correct_5": "",
        "data_1040x_20_correct_6": "",
        "data_1040x_20_correct_7": "",
        "data_1040x_20_correct_8": "",
        "data_1040x_20_correct_9": "",
        "data_1040x_20_orginal_1": "",
        "data_1040x_20_orginal_2": "",
        "data_1040x_20_orginal_3": "",
        "data_1040x_20_orginal_5": "",
        "data_1040x_20_orginal_6": "",
        "data_1040x_20_orginal_7": "",
        "data_1040x_20_orginal_8": "",
        "data_1040x_20_orginal_9": "",
        "data_1040x_20_correct_10": "",
        "data_1040x_20_correct_11": "29,865",
        "data_1040x_20_correct_12": "-",
        "data_1040x_20_correct_13": "-",
        "data_1040x_20_correct_14": "-",
        "data_1040x_20_correct_15": "15,110",
        "data_1040x_20_correct_16": "29,865",
        "data_1040x_20_correct_17": "44,975",
        "data_1040x_20_correct_18": "-",
        "data_1040x_20_correct_19": "44,975",
        "data_1040x_20_correct_20": "-",
        "data_1040x_20_correct_21": "15,110",
        "data_1040x_20_correct_22": "15,110",
        "data_1040x_20_correct_4a": "",
        "data_1040x_20_correct_4b": "",
        "data_1040x_20_orginal_10": "",
        "data_1040x_20_orginal_11": "29,865",
        "data_1040x_20_orginal_12": "-",
        "data_1040x_20_orginal_13": "-",
        "data_1040x_20_orginal_14": "-",
        "data_1040x_20_orginal_15": "-",
        "data_1040x_20_orginal_4a": "",
        "data_1040x_20_orginal_4b": "",
        "data_1040x_20_org_sch_3_9": "-"
    }
   
    data_variables_7202_20 = {
        "data_7202_20_1": "3",
        "data_7202_20_2": "7",
        "data_7202_20_3": "10",
        "data_7202_20_4": "3",
        "data_7202_20_5": "7",
        "data_7202_20_6": "7",
        "data_7202_20_7": "3,181",
        "data_7202_20_8": "12",
        "data_7202_20_9": "12",
        "data_7202_20_10": "36",
        "data_7202_20_11": "8",
        "data_7202_20_12": "8",
        "data_7202_20_13": "56",
        "data_7202_20_14": "92",
        "data_7202_20_15": "-",
        "data_7202_20_16": "-",
        "data_7202_20_17": "56",
        "data_7202_20_18": "56",
        "data_7202_20_19": "-",
        "data_7202_20_20": "92",
        "data_7202_20_21": "92",
        "data_7202_20_22": "-",
        "data_7202_20_23": "-",
        "data_7202_20_24": "92",
        "data_7202_20_25": "50",
        "data_7202_20_26": "3,181",
        "data_7202_20_27": "12",
        "data_7202_20_28": "8",
        "data_7202_20_29": "8",
        "data_7202_20_30": "400",
        "data_7202_20_31": "-",
        "data_7202_20_32": "400",
        "data_7202_20_33": "400",
        "data_7202_20_34": "-",
        "data_7202_20_35": "400"
        }
    
    data_variables_sch_3_20 = {
        "data_sch_3_20_1": "1",
        "data_sch_3_20_2": "2",
        "data_sch_3_20_3": "3",
        "data_sch_3_20_4": "4",
        "data_sch_3_20_5": "5",
        "data_sch_3_20_6": "6",
        "data_sch_3_20_7": "7",
        "data_sch_3_20_8": "8",
        "data_sch_3_20_9": "9",
        "data_sch_3_20_10": "10",
        "data_sch_3_20_11": "11",
        "data_sch_3_20_13": "14,510",
        "data_sch_3_20_12a": "12a",
        "data_sch_3_20_12b": "14,510",
        "data_sch_3_20_12c": "12c",
        "data_sch_3_20_12d": "12d",
        "data_sch_3_20_12e": "12e",
        "data_sch_3_20_12f": "14,510"
    }
    
    FieldsStrings = combine_fields(data_variables_1040_20,data_variables_1040x_20,data_variables_7202_20,data_variables_sch_3_20)  
    
    parameters = {}
    parameters["name"] = os.path.basename(destinationFile)
    parameters["url"] = uploadedFileUrl
    parameters["fieldsString"] = FieldsStrings
    parameters["async"] = Async

    url = "{}/pdf/edit/add".format(BASE_URL)

    response = requests.post(url, data=parameters, headers={ "x-api-key": API_KEY })
    if (response.status_code == 200):
        json = response.json()

        if json["error"] == False:
            resultFileUrl = json["url"]
            r = requests.get(resultFileUrl, stream=True)
            if (r.status_code == 200):
                with open(destinationFile, 'wb') as file:
                    for chunk in r:
                        file.write(chunk)
                print(f"Result file saved as \"{destinationFile}\" file.")
            else:
                print(f"Request error: {response.status_code} {response.reason}")
        else:
            print(json["message"])
    else:
        print(f"Request error: {response.status_code} {response.reason}")

if __name__ == '__main__':
    main()