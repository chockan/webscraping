import os
import win32com.client


a="d:/python course/Book1.xlsx"
class ExcelAutomation:

    def __init__(self,a):
        self.a=a
        self.b=win32com.client.Dispatch("Excel.Application")
        self.workbook=None
        self.worksheet=None

    def open_workbook(self):
        try:
            self.workbook=self.b.Workbooks.Open(self.a)
            self.worksheet=self.workbook.Worksheets(1)
        except Exception as e:
            print("error")

    def insert_data(self):
        self.worksheet.Range("A2").Value = "edit"
    def update_data(self,c,d):
        self.worksheet.Range(c).Value = d
        
    def delete_data(self,e):
        self.worksheet.Rows(e).Delete()
    def save_data(self):
        self.workbook.Save()
    def close_data(self):
        self.b.Quit()

ex=ExcelAutomation(a)
ex.open_workbook()
#ex.insert_data()
#ex.update_data("A2","dhoni")
ex.delete_data(2)
ex.save_data()
ex.close_data()



