import xlrd
import csv

def csv_from_excel(filename,sheetname):
    wb = xlrd.open_workbook(filename+'.xlsx')
    sh = wb.sheet_by_name(sheetname)
    your_csv_file = open(filename+'.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()
