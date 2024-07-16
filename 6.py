import os
import win32com.client  #pip install pywin32


class ExcelAutomation:
    def __init__(self, file_path):
        self.file_path = file_path
        self.excel = win32com.client.Dispatch("Excel.Application")
        self.workbook = None
        self.worksheet = None

    def open_workbook(self):
        try:
            self.workbook = self.excel.Workbooks.Open(self.file_path)
            self.worksheet = self.workbook.Worksheets(1)  # First worksheet by default
        except Exception as e:
            print("An error occurred while opening the workbook:", e)

    def modify_data(self):
        if self.worksheet:
            try:
                # Example: Update value in cell A1
                self.worksheet.Range("A2").Value = "rohit"  # Update value in cell A2
                self.worksheet.Range("A3").Value = "yuvi"  # Update value in cell A3
                self.worksheet.Range("A4").Value = "markam"  # Update value in cell A4
                self.worksheet.Range("A5").Value = "jadeja"  # Update value in cell A5
                self.worksheet.Range("A6").Value = ""  # Clear value in cell A6
                # Add more modifications as needed
            except Exception as e:
                print("An error occurred while modifying data:", e)



def main(excel_file_path):
    if os.path.exists(excel_file_path):
        excel_automation = ExcelAutomation(excel_file_path)
        excel_automation.open_workbook()

        # Modify data
        excel_automation.modify_data()

        # Update cell
        excel_automation.update_cell("A7", "Atri")

        # Delete row
        excel_automation.delete_row(8)

        excel_automation.save_changes()
        excel_automation.close_excel()
    else:
        print("Excel file not found")


if __name__ == "__main__":
    sample_file_path = "d:/python course/Book1.xlsx"  # Replace with your sample file path
    main(sample_file_path)