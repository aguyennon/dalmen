using MobileScanner.Services;
using MobileScanner.Views;
using Microsoft.Extensions.DependencyInjection;
using CommunityToolkit.Maui;
using ClosedXML.Excel;
using System.IO;
using Microsoft.Office.Interop.Excel;


namespace MobileScanner;

public partial class MainPage : ContentPage
{
    private readonly AuthService _authService;
    

    public MainPage()
    {
        InitializeComponent();
        _authService = new AuthService();
        _authService = _authService ?? throw new ArgumentNullException(nameof(_authService));
        _ = InitExcelAsync();
    }


    private string? _excelPath;
    private async Task InitExcelAsync()
    {
        bool picked = await PickExcelFileAsync();
        if (!picked)
        {
            await DisplayAlert("Excel Missing", "You need to select an Excel file to store scans.", "OK");
        }
    }

    private async void ScanButton_Clicked(object sender, EventArgs e)
    {
        if (string.IsNullOrEmpty(_excelPath))
        {
            await DisplayAlert("Excel Not Selected", "Please select an Excel file first.", "OK");
            return;
        }

        await SaveScanToExcelAsync("ScannedBarcodeGoesHere");
    }

    public async Task<bool> PickExcelFileAsync()
    {
        var result = await FilePicker.Default.PickAsync(new PickOptions
        {
            PickerTitle = "Please select an Excel file",
            FileTypes = new FilePickerFileType(new Dictionary<DevicePlatform, IEnumerable<string>>
        {
            { DevicePlatform.Android, new[] { "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" } },
            { DevicePlatform.iOS, new[] { "com.microsoft.excel.xlsx" } },
            { DevicePlatform.WinUI, new[] { ".xlsx" } },
            { DevicePlatform.MacCatalyst, new[] { "xlsx" } },
        })
        });

        if (result != null)
        {
            _excelPath = result.FullPath;

            return true;
        }

        return false;
    }

    private async Task SaveScanToExcelAsync(string scannedValue)
    {
        try
        {
            using (var workbook = new XLWorkbook(_excelPath))
            {
                var ws = workbook.Worksheets.FirstOrDefault() ?? workbook.AddWorksheet("Scans");

                int lastRow = ws.LastRowUsed()?.RowNumber() ?? 0;
                ws.Cell(lastRow + 1, 1).Value = scannedValue;
                ws.Cell(lastRow + 1, 2).Value = DateTime.Now;

                workbook.Save();
            }

            await DisplayAlert("Success", "Scan saved to Excel!", "OK");
        }
        catch (Exception ex)
        {
            await DisplayAlert("Error", $"Could not write to Excel: {ex.Message}", "OK");
        }
    }


    private async void OnTakePhotoClicked(object sender, EventArgs e)
    {
        try
        {
            var status = await Permissions.RequestAsync<Permissions.Camera>();
            if (status != PermissionStatus.Granted)
            {
                await DisplayAlert("Permission denied", "Camera access is required.", "OK.");
                return;
            }

            var photo = await MediaPicker.Default.CapturePhotoAsync();
            if (photo != null)
            {
                var stream = await photo.OpenReadAsync();
                PhotoResult.Source = ImageSource.FromStream(() => stream);
            }
        }
        catch (Exception ex)
        {
            await DisplayAlert("Error", $"Camera failed: {ex.Message}", "OK");
        }

    }

    private async Task CapturePhoto()
    {
        if (MediaPicker.Default.IsCaptureSupported)
        {
            FileResult? photo = await MediaPicker.Default.CapturePhotoAsync();

            if (photo != null)
            {
                // Get the photo stream
                using Stream sourceStream = await photo.OpenReadAsync();
                using MemoryStream memoryStream = new MemoryStream();
                await sourceStream.CopyToAsync(memoryStream);

                // Update UI
                PhotoResult.Source = ImageSource.FromStream(() => new MemoryStream(memoryStream.ToArray()));
            }
        }
    }


    private async void CameraButton_Clicked(object sender, EventArgs e)
    {
        await CapturePhoto();
    }


    private async void OnUpdateExcelClicked(object sender, EventArgs e)
    {
        string fileName = Path.Combine(FileSystem.Current.AppDataDirectory, "scanthermos.xlsm");

        if (!File.Exists(fileName))
        {
            await DisplayAlert("File Not Found", "The file scanthermos.xlsm was not found in the app data directory.", "OK");
            return;
        }

        using var workbook = new XLWorkbook(fileName);
        var worksheet = workbook.Worksheet("SCANS");

        int firstRow = 5;
        var newRow = firstRow + 1;

        workbook.Save();

        await DisplayAlert("Excel Updated", $"Excel file updated. Next empty row is {newRow}.", "OK");
    }
    


}