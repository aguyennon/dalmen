using Microsoft.Maui;
using Microsoft.Maui.Controls;
using Microsoft.Maui.Storage;
using Microsoft.Maui.ApplicationModel;
using System;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Linq;
using Microsoft.Maui.Media;
using Microsoft.Maui.Devices;
using System.IO;
using MobileScanner.Services;
using ClosedXML.Excel;



namespace MobileScanner;

public partial class MainPage : ContentPage
{
    private readonly AuthService _authService;


    public MainPage()
    {
        InitializeComponent();
        _authService = new AuthService();
        _authService = _authService ?? throw new ArgumentNullException(nameof(_authService));
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