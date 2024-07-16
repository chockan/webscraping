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
                self.worksheet.Range("A2").Value = "wwwww"  # Update value in cell A2
                self.worksheet.Range("A3").Value = "xxxxx"  # Update value in cell A3
                self.worksheet.Range("A4").Value = "yyyyy"  # Update value in cell A4
                self.worksheet.Range("A5").Value = "gggg"  # Update value in cell A5
                self.worksheet.Range("A6").Value = "kkkk"  # Clear value in cell A6
                # Add more modifications as needed
            except Exception as e:
                print("An error occurred while modifying data:", e)


    
    def update_cell(self, cell, value):
        if self.worksheet:
            try:
                self.worksheet.Range(cell).Value = value
            except Exception as e:
                print(f"An error occurred while updating cell {cell}: {e}")

    def delete_row(self, row):
        if self.worksheet:
            try:
                self.worksheet.Rows(row).Delete()
            except Exception as e:
                print(f"An error occurred while deleting row {row}: {e}")

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






def main():
    excel_automation = ExcelAutomation(a)
    excel_automation.open_workbook()
    excel_automation.modify_data()
    excel_automation.update_cell("a2","dhoni")
    excel_automation.delete_row(6)
    excel_automation.save_changes()

        # Modify data
    excel_automation.close_excel()



if __name__ == "__main__":
    a="d:/python course/Book1.xlsx"
    main()