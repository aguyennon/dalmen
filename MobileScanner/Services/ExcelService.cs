using ClosedXML.Excel;
using System;
using System.IO;
using System.Threading.Tasks;

namespace MobileScanner.Services
{
    public class ExcelService
    {
        private readonly AuthService _authService;

        public ExcelService(AuthService authService)
        {
            _authService = authService;
        }


        public async Task<bool> AppendScanToExcelAsync(string code)
        {
            try
            {
                string filePath = Path.Combine(FileSystem.Current.AppDataDirectory, "scanthermos.xlsm");

                // Debug: Check if file already exists
                System.Diagnostics.Debug.WriteLine($"Target file path: {filePath}");
                System.Diagnostics.Debug.WriteLine($"File exists: {File.Exists(filePath)}");
                System.Diagnostics.Debug.WriteLine($"AppDataDirectory: {FileSystem.Current.AppDataDirectory}");

                // Copy the template if missing
                if (!File.Exists(filePath))
                {
                    // Let's skip the template and create our own file
                    System.Diagnostics.Debug.WriteLine("File doesn't exist, creating new Excel file...");
                    await CreateBasicExcelFile(filePath);
                }

                // Small delay to ensure file is not locked
                await Task.Delay(50);

                // Verify file exists and is accessible
                if (!File.Exists(filePath))
                    throw new Exception($"Excel file still not found after creation attempt at: {filePath}");

                // Try to open and modify the workbook
                using var workbook = new XLWorkbook(filePath);
                var worksheet = workbook.Worksheet("SCANS");
                if (worksheet == null)
                    throw new Exception("Worksheet 'SCANS' not found in scanthermos.xlsx");

                var lastRow = worksheet.LastRowUsed()?.RowNumber() ?? 0;
                int newRow = lastRow + 1;

                // Add the data
                worksheet.Cell(newRow, 1).Value = DateTime.Now;
                worksheet.Cell(newRow, 2).Value = code;

                // Save the workbook
                workbook.Save();

                System.Diagnostics.Debug.WriteLine($"Successfully added scan '{code}' to row {newRow}");
                return true;
            }
            catch (UnauthorizedAccessException ex)
            {
                var errorMsg = "Access denied to Excel file. Check app permissions.";
                System.Diagnostics.Debug.WriteLine($"Access Error: {ex.Message}");
                await ShowErrorAlert("Permission Error", errorMsg);
                return false;
            }
            catch (IOException ex)
            {
                var errorMsg = "File is in use or corrupted. Try closing other apps.";
                System.Diagnostics.Debug.WriteLine($"IO Error: {ex.Message}");
                await ShowErrorAlert("File Error", errorMsg);
                return false;
            }
            catch (Exception ex)
            {
                var errorMsg = $"Unexpected error: {ex.Message}";
                System.Diagnostics.Debug.WriteLine($"Excel Error Details:");
                System.Diagnostics.Debug.WriteLine($"Message: {ex.Message}");
                System.Diagnostics.Debug.WriteLine($"Type: {ex.GetType().Name}");
                System.Diagnostics.Debug.WriteLine($"Stack Trace: {ex.StackTrace}");

                if (ex.InnerException != null)
                {
                    System.Diagnostics.Debug.WriteLine($"Inner Exception: {ex.InnerException.Message}");
                }

                await ShowErrorAlert("Excel Error", errorMsg);
                return false;
            }
        }

        private async Task CreateBasicExcelFile(string filePath)
        {
            try
            {
                System.Diagnostics.Debug.WriteLine("Creating basic Excel file from scratch...");

                using var workbook = new XLWorkbook();
                var worksheet = workbook.Worksheets.Add("SCANS");

                // Add headers
                worksheet.Cell(1, 1).Value = "DateTime";
                worksheet.Cell(1, 2).Value = "Code";

                // Format headers
                worksheet.Range("A1:B1").Style.Font.Bold = true;
                worksheet.Range("A1:B1").Style.Fill.BackgroundColor = XLColor.LightBlue;

                await Task.Delay(1); // Small delay to ensure file system is ready

                // Auto-fit columns
                worksheet.Columns().AdjustToContents();

                workbook.SaveAs(filePath);
                System.Diagnostics.Debug.WriteLine($"Successfully created Excel file at: {filePath}");
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Failed to create basic Excel file: {ex.Message}");
                throw new Exception($"Failed to create basic Excel file: {ex.Message}", ex);
            }
        }

        private async Task ShowErrorAlert(string title, string message)
        {
            try
            {
                var mainPage = Application.Current?.Windows.FirstOrDefault()?.Page;
                if (mainPage != null)
                {
                    await mainPage.DisplayAlert(title, message, "OK");
                }
                else
                {
                    System.Diagnostics.Debug.WriteLine($"Could not show alert - no main page found. {title}: {message}");
                }
            }
            catch (Exception alertEx)
            {
                System.Diagnostics.Debug.WriteLine($"Failed to show error alert: {alertEx.Message}");
            }
        }






    }
}
