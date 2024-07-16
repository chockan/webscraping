import os
import win32com.client  #  pip install pywin32


class ExcelAutomation:

    def __init__(self,a):
        self.a=a
        self.excel = win32com.client.Dispatch("Excel.Application")
        self.workbook = None
        self.worksheet = None

    def open_workbook(self):
        try:
            self.workbook = self.excel.Workbooks.Open(self.a)
            self.worksheet = self.workbook.Worksheets(1)  # First worksheet by default
        except Exception as e:
            print("An error occurred while opening the workbook:", e)

    def modify_data(self):

        if self.worksheet:
            try:
                # Example: Update value in cell A1
                self.worksheet.Range("a2").Value = "dhoni"
                self.worksheet.Range("a3").Value = "shewag"
                self.worksheet.Range("a4").Value = "patil"
                self.worksheet.Range("a5").Value = "bumra"
                self.worksheet.Range("a6").Value = "mahi"
                # Add more modifications as needed
            except Exception as e:
                print("An error occurred while modifying data:", e)
    def save_changes(self):
        if self.workbook:
            try:
                self.workbook.Save()
            except Exception as e:
                print("An error occurred while saving changes:", e)
    
    def close_excel(self):
        try:
            self.excel.Quit()
        except Exception as e:
            print("An error occurred while closing Excel:", e)


def main(a):

    if os.path.exists(a):
        excel_automation = ExcelAutomation(a)
        excel_automation.open_workbook()
        excel_automation.modify_data()
        excel_automation.save_changes()
        excel_automation.close_excel()


if __name__ == "__main__":
    a="d:/python course/Book1.xlsx"
    main(a)