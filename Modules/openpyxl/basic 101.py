print(5)
import openpyxl


wb = openpyxl.load_workbook("Modules\openpyxl\sample_data.xlsx")
sheetnames = wb.sheetnames  # fetch all the sheet names inside xlsx file
print(sheetnames)