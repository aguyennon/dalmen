using CommunityToolkit.Maui.Alerts;
using CommunityToolkit.Maui.Core;
using Microsoft.Maui.ApplicationModel;
using Microsoft.Maui.Controls;
using Microsoft.Maui.Storage;
using MobileScanner.Services;
using OfficeOpenXml;
using Syncfusion.Pdf;
using Syncfusion.Pdf.Graphics;
using System;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using ZXing.Net.Maui;
using ZXing.Net.Maui.Controls;
using ClosedXML.Excel;
using System.Collections.Generic;
using CommunityToolkit.Maui.Media;
using Plugin.Maui.OCR;
using Microsoft.Maui.Devices;
using Microsoft.Maui;
using Microsoft.Maui.ApplicationModel.DataTransfer;
using Microsoft.Maui.Media;



namespace MobileScanner.Views;

public partial class ScanPage : ContentPage
{
    private readonly AuthService _authService;
    private readonly ExcelService _excelService;
    private readonly ClipboardService _clipboardService;
    private readonly AutomationService _automationService;

    private Button _autoLoginButton;
    private IOcrService? _ocrService;
    private CameraBarcodeReaderView? _cameraView;
    private Label _statusLabel;
    private Entry _barcodeEntry;
    private Entry _quantityEntry;
    private Picker _unitPicker;

    private Button _copyButton;
    private Button _excelButton;
    private Button _clearButton;
    private Button _historyButton;
    private Button _confirmButton;
    private Button _copyAllButton;
    private Button _nextButton;
    private Button _createPdfButton;
    private Button _sendExcel;

    // Group history (scans + optional quantity)
    private List<GroupScanData> groupHistory = new List<GroupScanData>();

    private int scanCount = 0;
    private const int MAX_SCANS = 3;
    private const int MAX_GROUP_HISTORY = 20;
    private bool isGroupScanMode = false;
    private bool isTextMode = false;
    private bool isProcessingOcr = false;

    private const uint FadeDuration = 250;
    private const uint SlideDuration = 250;
    private const double SlideDistance = 20;

    private readonly TimeSpan DuplicateWindow = TimeSpan.FromSeconds(5);
    private readonly object _scanLock = new object();
    private readonly Dictionary<string, DateTime> _recentScans = new Dictionary<string, DateTime>();

    private List<string> currentScanSession = new List<string>();

    // ========= Inner class for group history =========
    public class GroupScanData
    {
        public List<string> Scans { get; set; } = new List<string>();
        public int? Quantity { get; set; } = null;

        public string GetFormattedString()
        {
            if (Scans.Count == 0) return string.Empty;

            string result = string.Join(",", Scans);
            if (Quantity.HasValue)
            {
                result += $",{Quantity.Value}";
            }
            return result;
        }
    }

    // ========= Constructor =========
    public ScanPage(AuthService authService)
    {
        InitializeComponent();

        _authService = authService ?? new AuthService();
        _excelService = new ExcelService(_authService);
        _clipboardService = new ClipboardService();
        _automationService = new AutomationService();

        // Grab controls from XAML
        _cameraView = this.FindByName<CameraBarcodeReaderView>("CameraView");
        _statusLabel = this.FindByName<Label>("StatusLabel");
        _barcodeEntry = this.FindByName<Entry>("BarcodeEntry");
        _quantityEntry = this.FindByName<Entry>("QuantityEntry");
        _unitPicker = this.FindByName<Picker>("UnitPicker");

        _copyButton = this.FindByName<Button>("ScanCopyButton");
        _excelButton = this.FindByName<Button>("ScanSendButton");
        _clearButton = this.FindByName<Button>("ClearButton");
        _historyButton = this.FindByName<Button>("HistoryButton");
        _confirmButton = this.FindByName<Button>("ConfirmButton");
        _copyAllButton = this.FindByName<Button>("CopyAllButton");
        _nextButton = this.FindByName<Button>("NextButton");
        _createPdfButton = this.FindByName<Button>("CreatePdfButton");
        _sendExcel = this.FindByName<Button>("SendExcelButton");
        _autoLoginButton = this.FindByName<Button>("AutoLoginButton");

        _ocrService = OcrPlugin.Default;

        var modeSwitch = this.FindByName<Switch>("ModeSwitch");
        if (modeSwitch != null)
        {
            modeSwitch.Toggled += ModeSwitch_Toggled;
        }

        var captureButton = this.FindByName<Button>("CaptureButton");
        if (captureButton != null)
        {
            captureButton.Clicked += OnCaptureClicked;
        }

        try
        {
            if (_copyButton != null)
                _copyButton.Clicked += OnCopyClicked;

            if (_clearButton != null)
                _clearButton.Clicked += OnClearClicked;

            if (_excelButton != null)
                _excelButton.Clicked += OnSendExcelClicked;

            if (_copyAllButton != null)
                _copyAllButton.Clicked += OnCopyAllClicked;

            if (_createPdfButton != null)
                _createPdfButton.Clicked += OnCreatePdfClicked;

            if (_historyButton != null)
                _historyButton.Clicked += OnGroupHistoryClicked;

            if (_sendExcel != null)
                _sendExcel.Clicked += OnSendExcelClicked;

            if (_autoLoginButton != null)
            {
                _autoLoginButton.Clicked -= OnAutoLoginClicked;
                _autoLoginButton.Clicked += OnAutoLoginClicked;
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"Failed wiring buttons: {ex}");
        }

        if (_cameraView != null)
            _cameraView.BarcodesDetected += CameraView_BarcodesDetected;

        if (_nextButton != null)
        {
            _nextButton.IsEnabled = true;
            _nextButton.Clicked += OnNextClicked;
            System.Diagnostics.Debug.WriteLine("Next button initialized successfully");
        }
        else
        {
            System.Diagnostics.Debug.WriteLine("ERROR: Next button is null!");
        }

        EnableActionButtons(false);
    }

    // ========= Mode / OCR =========

    private void ModeSwitch_Toggled(object sender, ToggledEventArgs e)
    {
        isTextMode = e.Value;

        var captureButton = this.FindByName<Button>("CaptureButton");
        if (captureButton != null)
            captureButton.IsVisible = isTextMode;

        if (_statusLabel != null)
        {
            _statusLabel.Text = isTextMode
                ? "TEXT MODE - Tap CAPTURE TEXT to scan"
                : "READY TO SCAN. (CODE 128)";
        }
    }

    private async void OnCaptureClicked(object sender, EventArgs e)
    {
        if (!isTextMode || _ocrService == null || isProcessingOcr)
            return;

        isProcessingOcr = true;

        try
        {
            _statusLabel.Text = "Taking photo...";
            var photo = await MediaPicker.CapturePhotoAsync(new MediaPickerOptions
            {
                Title = "Capture text to scan"
            });

            if (photo == null)
            {
                _statusLabel.Text = "TEXT MODE - Tap CAPTURE TEXT to scan";
                return;
            }

            _statusLabel.Text = "Processing text...";

            using var stream = await photo.OpenReadAsync();
            using var ms = new MemoryStream();
            await stream.CopyToAsync(ms);
            var imageBytes = ms.ToArray();

            var result = await _ocrService.RecognizeTextAsync(imageBytes);

            if (!string.IsNullOrWhiteSpace(result?.AllText))
            {
                string recognizedText = result.AllText.Trim();
                System.Diagnostics.Debug.WriteLine($"OCR detected: {recognizedText}");

                string filteredText = ExtractNumbersUntilSpace(recognizedText);

                if (!string.IsNullOrEmpty(filteredText))
                {
                    _barcodeEntry.Text = filteredText;
                    _statusLabel.Text = $"Numbers recognized: {filteredText}";

                    currentScanSession.Add(filteredText);
                    EnableActionButtons(true);

                    var toast = Toast.Make("NUMBERS RECOGNIZED!", ToastDuration.Short, 14);
                    await toast.Show();
                }
                else
                {
                    _statusLabel.Text = $"OCR found: '{recognizedText}' but no numbers extracted";
                    await DisplayAlert("No Numbers",
                        $"Detected text: '{recognizedText}'\n\nBut no numbers found before first space.",
                        "OK");
                }
            }
            else
            {
                _statusLabel.Text = "No text recognized - try again";
                await DisplayAlert("No Text",
                    "Could not recognize any text. Try:\n- Better lighting\n- Clearer text\n- Holding camera steady",
                    "OK");
            }
        }
        catch (Exception ex)
        {
            _statusLabel.Text = "OCR error";
            await DisplayAlert("Error", $"Text recognition failed: {ex.Message}", "OK");
        }
        finally
        {
            isProcessingOcr = false;
        }
    }

    private string ExtractNumbersUntilSpace(string input)
    {
        if (string.IsNullOrEmpty(input))
            return string.Empty;

        var result = new System.Text.StringBuilder();

        foreach (char c in input)
        {
            if (char.IsWhiteSpace(c))
                break;

            if (char.IsDigit(c) || c == '-')
                result.Append(c);
        }

        return result.ToString();
    }

    // ========= Camera / scanning =========

    protected override async void OnAppearing()
    {
        base.OnAppearing();
        await EnsureCameraPermissionAsync();
        if (_cameraView != null)
            _cameraView.IsDetecting = true;
    }

    protected override void OnDisappearing()
    {
        base.OnDisappearing();
        if (_cameraView != null)
            _cameraView.IsDetecting = false;
    }

    private async Task EnsureCameraPermissionAsync()
    {
        var status = await Permissions.CheckStatusAsync<Permissions.Camera>();
        if (status != PermissionStatus.Granted)
            status = await Permissions.RequestAsync<Permissions.Camera>();

        if (status != PermissionStatus.Granted)
        {
            await DisplayAlert("Permission Denied",
                "Camera permission is required to scan barcodes.", "OK");
        }
    }

    private string NormalizeBarcode(string input)
    {
        if (string.IsNullOrEmpty(input)) return string.Empty;
        return input.Trim().Replace("\r", "").Replace("\n", "");
    }

    private void OnBarcodeScanned(string scannedValue)
    {
        if (string.IsNullOrWhiteSpace(scannedValue))
            return;

        scannedValue = NormalizeBarcode(scannedValue);
        currentScanSession.Add(scannedValue);

        _barcodeEntry.Text = scannedValue;
        _statusLabel.Text = scannedValue;
    }

    private async void CameraView_BarcodesDetected(object? sender, BarcodeDetectionEventArgs e)
    {
        if (isTextMode) return;

        try
        {
            var values = e.Results?
                .Select(r => NormalizeBarcode(r.Value))
                .Where(v => !string.IsNullOrEmpty(v))
                .Distinct()
                .ToList();

            if (values == null || values.Count == 0)
                return;

            if (_cameraView != null)
                _cameraView.IsDetecting = false;

            var now = DateTime.UtcNow;

            foreach (var scannedCode in values)
            {
                bool shouldHandle = false;

                // Takes care of any old scans beyond the duplicate window
                lock (_scanLock)
                {
                    var oldKeys = _recentScans
                        .Where(kv => (now - kv.Value) > DuplicateWindow)
                        .Select(kv => kv.Key)
                        .ToList();

                    foreach (var k in oldKeys)
                        _recentScans.Remove(k);

                    if (!_recentScans.TryGetValue(scannedCode, out var last) ||
                        (now - last) > DuplicateWindow)
                    {
                        _recentScans[scannedCode] = now;
                        shouldHandle = true;
                    }
                }

                if (!shouldHandle)
                    continue;

                await MainThread.InvokeOnMainThreadAsync(async () =>
                {
                    try { HapticFeedback.Default.Perform(HapticFeedbackType.Click); } catch { }

                    var toast = Toast.Make("BARCODE SCANNED!", ToastDuration.Short, 14);
                    await toast.Show();

                    if (isGroupScanMode)
                    {
                        OnBarcodeScannedInGroup(scannedCode);
                    }
                    else
                    {
                        OnBarcodeScanned(scannedCode);
                        EnableActionButtons(true);
                    }
                });
            }
        }
        catch (Exception ex)
        {
            System.Diagnostics.Debug.WriteLine($"CameraView_BarcodesDetected error: {ex}");
        }
        finally
        {
            await Task.Delay(500);
            if (_cameraView != null)
                _cameraView.IsDetecting = true;
        }
    }

    // ========= Basic buttons (copy / clear / history / excel) =========

    private void OnClearHistoryClicked(object sender, EventArgs e)
    {
        _barcodeEntry.Text = string.Empty;
        _statusLabel.Text = "READY TO SCAN. (CODE 128)";

        lock (_scanLock)
        {
            _recentScans.Clear();
        }

        EnableActionButtons(false);
    }

    private async void OnCopyClicked(object sender, EventArgs e)
    {
        try
        {
            var text = _barcodeEntry?.Text?.Trim();

            if (string.IsNullOrEmpty(text))
            {
                _statusLabel.Text = "Nothing to copy.";
                var t = Toast.Make("No barcode to copy", ToastDuration.Short, 14);
                await t.Show();
                return;
            }

            bool success = await _clipboardService.CopyBarcodeAsync(text);

            if (success)
            {
                _statusLabel.Text = $"Copied: {text}";
                _barcodeEntry.Text = string.Empty;

                lock (_scanLock)
                {
                    _recentScans.Remove(text);
                }

                await DisplayAlert("CLIPBOARD", "Barcode copied to clipboard!", "OK");
            }
            else
            {
                _statusLabel.Text = "Failed to copy to clipboard...";
                await DisplayAlert("Error", "Failed to copy barcode.", "OK");
            }
        }
        catch (Exception ex)
        {
            await DisplayAlert("Error", $"Copy error: {ex.Message}", "OK");
        }
    }

    private async void OnCopyAllClicked(object sender, EventArgs e)
    {
        try
        {
            _statusLabel.Text = "Copying all history...";

            var success = await _clipboardService.CopyAllHistoryAsync();

            if (success)
            {
                var historyCount = _clipboardService.HistoryCount;
                _statusLabel.Text = $"Copied all {historyCount} items to clipboard";

                await DisplayAlert("Success",
                    $"All {historyCount} history items copied to clipboard!",
                    "OK");
            }
            else
            {
                _statusLabel.Text = "No history to copy";
                await DisplayAlert("Info", "No history items to copy.", "OK");
            }
        }
        catch (Exception ex)
        {
            _statusLabel.Text = "Failed to copy history";
            await DisplayAlert("Error", $"Failed to copy history: {ex.Message}", "OK");
        }
    }

    async void OnCopyGroupHistoryClicked(object sender, EventArgs e)
    {
        if (groupHistory.Count == 0)
        {
            await DisplayAlert("No Group History", "There are no groups to copy yet", "OK");
            return;
        }

        // Updated to use formatted strings with quantities
        var allFormattedGroups = groupHistory.Select(g => g.GetFormattedString()).ToList();
        string allGroupsText = string.Join("\n", allFormattedGroups);

        try
        {
            await Clipboard.SetTextAsync(allGroupsText);

            int totalCodes = groupHistory.Sum(g => g.Scans.Count);
            await DisplayAlert("Copied", $"All {groupHistory.Count} groups ({totalCodes} total codes) copied to clipboard!", "OK");

            if (_statusLabel != null)
                _statusLabel.Text = "All group history copied to clipboard.";
        }
        catch (Exception ex)
        {
            await DisplayAlert("Error", $"Failed to copy group history: {ex.Message}", "OK");
        }
    }

    private async void OnSendExcelClicked(object sender, EventArgs e)
    {
        try
        {
            string filePath = Path.Combine(FileSystem.AppDataDirectory, "GroupAndScans.xlsx");

            // When the time comes, create an excel workbook
            using (var workbook = new XLWorkbook())
            {
                var ws = workbook.Worksheets.Add("Scans");
                int row = 1;

                if (groupHistory != null && groupHistory.Count > 0)
                {
                    foreach (var group in groupHistory)
                    {
                        string line = group.GetFormattedString();
                        if (!string.IsNullOrEmpty(line))
                        {
                            // To separate into their own sections
                            string[] parts = line.Split(',');

                            for (int col = 0; col < parts.Length; col++)
                            {
                                ws.Cell(row, col + 1).Value = parts[col].Trim();
                            }
                            row++;
                        }
                    }

                    row++;
                }

                if (currentScanSession != null && currentScanSession.Count > 0)
                {
                    foreach (var barcode in currentScanSession)
                    {
                        ws.Cell(row, 1).Value = barcode;
                        row++;
                    }
                }

                ws.Columns().AdjustToContents();
                workbook.SaveAs(filePath);
            }

            await Launcher.OpenAsync(new OpenFileRequest
            {
                File = new ReadOnlyFile(filePath)
            });
        }
        catch (Exception ex)
        {
            await DisplayAlert("Error", ex.Message, "OK");
        }
    }

    // Unused for the moment
    async Task PostScanToExcelAsync(string code)
    {
        try
        {
            _statusLabel.Text = "Posting to Excel...";
            bool success = await _excelService.AppendScanToExcelAsync(code);

            if (success)
            {
                _statusLabel.Text = $" Added to Excel: {code}";
                await DisplayAlert("Success",
                    $"Scan successfully added to Excel!\nCode: {code}",
                    "OK");
            }
            else
            {
                _statusLabel.Text = " Failed to add to Excel";
                await DisplayAlert("Error",
                    "Failed to add scan to Excel. Please try again.",
                    "OK");
            }
        }
        catch (Exception ex)
        {
            _statusLabel.Text = " Excel error";
            await DisplayAlert("Excel Error",
                $"Failed to update Excel: {ex.Message}",
                "OK");
        }
    }

    // ========= Group scanning =========

    private void OnBarcodeScannedInGroup(string barcodeValue)
    {
        _barcodeEntry.Text = barcodeValue;
        _statusLabel.Text = "GROUP MODE: Barcodes ready to scan.";

        if (_nextButton != null)
        {
            _nextButton.IsEnabled = true;
            _nextButton.Text = $"CONFIRM SCAN: {scanCount + 1} of {MAX_SCANS}";
        }
    }

    private void OnNextClicked(object sender, EventArgs e)
    {
        if (!isGroupScanMode)
        {
            if (groupHistory.Count >= MAX_GROUP_HISTORY)
            {
                MainThread.BeginInvokeOnMainThread(async () =>
                {
                    await DisplayAlert("Group Limit Reached",
                        $"Maximum {MAX_GROUP_HISTORY} groups reached. Please clear group history to use again.",
                        "OK");
                });
                return;
            }

            StartGroupScanning();
            return;
        }

        string currentBarcode = _barcodeEntry?.Text?.Trim();

        if (string.IsNullOrEmpty(currentBarcode))
        {
            return;
        }

        currentScanSession.Add(currentBarcode);
        scanCount++;

        if (scanCount >= MAX_SCANS)
        {
            if (currentScanSession.Count >= MAX_SCANS)
            {
                var groupData = new GroupScanData();
                groupData.Scans.AddRange(currentScanSession);
                groupHistory.Add(groupData);

                MainThread.BeginInvokeOnMainThread(async () =>
                {
                    await DisplayAlert("Group Scans Complete",
                        $"{currentScanSession[0]}\n" +
                        $"{currentScanSession[1]}\n" +
                        $"{currentScanSession[2]}",
                        "OK");
                });

                ResetGroupScanning();
            }
        }
        else
        {
            PrepareForNextScan();
        }
    }

    private void StartGroupScanning()
    {
        isGroupScanMode = true;
        currentScanSession.Clear();
        scanCount = 0;

        if (_nextButton != null)
        {
            _nextButton.Text = "AWAITING FIRST SCAN (0/3)";
            _nextButton.IsEnabled = false;
        }

        _statusLabel.Text = "GROUP MODE: Scan barcode (1/3)";
    }

    private void PrepareForNextScan()
    {
        _barcodeEntry.Text = string.Empty;

        if (_nextButton != null)
            _nextButton.IsEnabled = false;

        _statusLabel.Text = $"GROUP MODE: Scan barcode {scanCount + 1}/3";

        MainThread.BeginInvokeOnMainThread(async () =>
        {
            await DisplayAlert("Next Scan",
                $"Barcode {scanCount}/3 confirmed! Now scan barcode {scanCount + 1} of 3",
                "OK");
        });
    }

    private void ResetGroupScanning()
    {
        isGroupScanMode = false;
        currentScanSession.Clear();
        scanCount = 0;

        if (_nextButton != null)
        {
            if (groupHistory.Count >= MAX_GROUP_HISTORY)
            {
                _nextButton.Text = "GROUP IS FULL";
                _nextButton.IsEnabled = false;
            }
            else
            {
                _nextButton.Text = "START GROUP";
                _nextButton.IsEnabled = true;
            }
        }

        _statusLabel.Text = "READY TO SCAN. (CODE 128)";
        _barcodeEntry.Text = string.Empty;
    }

    async void OnHistoryClicked(object sender, EventArgs e)
    {
        var history = _clipboardService.GetHistory();

        if (!history.Any())
        {
            await DisplayAlert("Clipboard History", "No items in clipboard history yet.", "OK");
            return;
        }

        var actions = history.Take(5).ToArray();
        string selectedItem = await DisplayActionSheet(
            "Clipboard History:",
            "Cancel",
            "Clear History",
            actions);

        if (selectedItem == "Clear History")
        {
            _clipboardService.ClearHistory();
            await DisplayAlert("History Cleared", "Clipboard history has been cleared.", "OK");
        }
        else if (selectedItem != "Cancel" && !string.IsNullOrEmpty(selectedItem))
        {
            if (_barcodeEntry != null)
                _barcodeEntry.Text = selectedItem.Replace("SCANNED: ", "");
            EnableActionButtons(true);
        }

    }

    private async void OnGroupHistoryClicked(object sender, EventArgs e)
    {
        if (groupHistory.Count == 0)
        {
            await DisplayAlert("No Group History", "No barcode groups have been scanned yet.", "OK");
            return;
        }

        string action = await DisplayActionSheet("Group History",
            "Cancel", "Clear All Groups",
            "View Groups", "Add QTY");

        if (action == "Clear All Groups")
        {
            await ClearGroupHistory();
        }
        else if (action == "View Groups")
        {
            await ShowGroupHistoryDetails();
        }
        else if (action == "Add QTY")
        {
            await ShowAddQuantityDialog();
        }
    }

    private async Task ShowGroupHistoryDetails()
    {
        string historyText = "GROUP HISTORY:\n\n";

        for (int i = 0; i < groupHistory.Count; i++)
        {
            historyText += $"Group {i + 1}:\n";
            historyText += groupHistory[i].GetFormattedString();
            historyText += "\n\n";
        }

        await DisplayAlert("Group History", historyText, "OK");
    }

    private async Task ShowAddQuantityDialog()
    {
        if (groupHistory.Count == 0)
        {
            await DisplayAlert("No Groups", "No barcode groups available to add quantity to.", "OK");
            return;
        }

        var groupOptions = new string[groupHistory.Count + 1];
        groupOptions[0] = "Cancel";

        for (int i = 0; i < groupHistory.Count; i++)
        {
            var preview = groupHistory[i].Scans.Count > 0
                ? groupHistory[i].Scans[0].Substring(0, Math.Min(10, groupHistory[i].Scans[0].Length)) + "..."
                : "Empty";

            string qtyText = groupHistory[i].Quantity.HasValue
                ? $" (QTY: {groupHistory[i].Quantity})"
                : " (No QTY)";

            groupOptions[i + 1] = $"Group {i + 1}: {preview}{qtyText}";
        }

        string selectedGroup = await DisplayActionSheet(
            "Select Group to Add Quantity",
            groupOptions[0], null,
            groupOptions.Skip(1).ToArray());

        if (selectedGroup == "Cancel" || string.IsNullOrEmpty(selectedGroup))
            return;

        int groupIndex = -1;
        for (int i = 0; i < groupHistory.Count; i++)
        {
            if (selectedGroup.StartsWith($"Group {i + 1}:"))
            {
                groupIndex = i;
                break;
            }
        }

        if (groupIndex == -1)
            return;

        string quantityInput = await DisplayPromptAsync(
            "Add Quantity",
            $"Enter quantity for Group {groupIndex + 1}:",
            "OK", "Cancel",
            "Enter number...", -1, Keyboard.Numeric);

        if (string.IsNullOrWhiteSpace(quantityInput))
            return;

        if (int.TryParse(quantityInput, out int quantity) && quantity > 0)
        {
            groupHistory[groupIndex].Quantity = quantity;

            await DisplayAlert("Success",
                $"Quantity {quantity} added to Group {groupIndex + 1}!\n\n" +
                $"Updated format:\n{groupHistory[groupIndex].GetFormattedString()}",
                "OK");

            _statusLabel.Text = $"Quantity {quantity} added to Group {groupIndex + 1}";
        }
        else
        {
            await DisplayAlert("Invalid Input", "Please enter a valid positive number.", "OK");
        }
    }

    private async Task ClearGroupHistory()
    {
        bool confirm = await DisplayAlert(
            "Clear Group History",
            "Are you sure you want to clear all group history? This cannot be undone.",
            "Yes", "No");

        if (confirm)
        {
            groupHistory.Clear();

            if (_nextButton != null)
            {
                _nextButton.Text = "START GROUP";
                _nextButton.IsEnabled = true;
            }

            await DisplayAlert("Cleared", "Group history has been cleared.", "OK");
        }
    }

    private void EnableActionButtons(bool enabled)
    {
        if (_copyButton != null)
            _copyButton.IsEnabled = enabled;

        if (_excelButton != null)
            _excelButton.IsEnabled = enabled;

        if (_clearButton != null)
            _clearButton.IsEnabled = enabled;

        if (_confirmButton != null)
            _confirmButton.IsEnabled = enabled;

        if (_copyAllButton != null)
            _copyAllButton.IsEnabled = enabled;
    }

    // ========= Unit picker helpers (Fenêtres / Portes) =========

    private void SetUnits(params string[] units)
    {
        if (_unitPicker == null) return;

        _unitPicker.ItemsSource = units.ToList();
        if (units.Length > 0)
            _unitPicker.SelectedIndex = 0;
    }

    // Fenêtres button
    private void OnFenetreOptionClicked(object sender, EventArgs e)
    {
        // All units for Fenêtres
        SetUnits("/ BARRES", "/ RACK", "/ BOITES", "/ unité", "/ LONGUEUR");
        _statusLabel.Text = "Unit list set for Fenêtres.";
    }

    // Portes - EXTRUSION
    private void OnPorteExtrusionClicked(object sender, EventArgs e)
    {
        // Example: only bar-style units
        SetUnits("/ BARRES", "/ BOITES", "/ LONGUEUR");
        _statusLabel.Text = "Unit list set for Portes - Extrusion.";
    }

    // Portes - QUINCAILLERIE
    private void OnPorteQuincaillerieClicked(object sender, EventArgs e)
    {
        // Example: box / unit based
        SetUnits("/ BOITES", "/ unité");
        _statusLabel.Text = "Unit list set for Portes - Quincaillerie.";
    }

    // Portes - VITRAGE (GLAZING)
    private void OnPorteVitrageClicked(object sender, EventArgs e)
    {
        SetUnits("/ unité");
        _statusLabel.Text = "Unit list set for Portes - Vitrage.";
    }

    // ========= Menus (Main / Third-party / History / PC Automation) =========

    private async Task HideAllMenus()
    {
        var menus = new[] { ThirdPartyMenu, HistoryMenu, PcAutomationMenu };
        foreach (var menu in menus)
        {
            if (menu.IsVisible)
            {
                await Task.WhenAll(
                    menu.FadeTo(0, FadeDuration, Easing.CubicOut),
                    menu.TranslateTo(0, SlideDistance, SlideDuration, Easing.CubicIn)
                );
                menu.IsVisible = false;
            }
        }
    }

    private async Task ShowMenu(StackLayout menu)
    {
        await HideAllMenus();
        MainMenu.IsVisible = false;

        await Task.WhenAll(
            MainMenu.FadeTo(0, FadeDuration, Easing.CubicOut),
            MainMenu.TranslateTo(0, SlideDistance, SlideDuration, Easing.CubicIn)
        );

        menu.TranslationY = SlideDistance;
        menu.Opacity = 0;
        menu.IsVisible = true;

        await Task.WhenAll(
            menu.FadeTo(1, FadeDuration, Easing.CubicOut),
            menu.TranslateTo(0, 0, SlideDuration, Easing.CubicOut)
        );
    }

    private async void OnBackClicked(object sender, EventArgs e)
    {
        await HideAllMenus();
        MainMenu.TranslationY = SlideDistance;
        MainMenu.Opacity = 0;
        MainMenu.IsVisible = true;

        await Task.WhenAll(
            MainMenu.FadeTo(1, FadeDuration, Easing.CubicOut),
            MainMenu.TranslateTo(0, 0, SlideDuration, Easing.CubicOut)
        );
    }

    private async void OnThirdPartyClicked(object sender, EventArgs e)
    {
        await ShowMenu(ThirdPartyMenu);
    }

    private async void OnHistoryMenuClicked(object sender, EventArgs e)
    {
        await ShowMenu(HistoryMenu);
    }

    private async void OnPcAutomationClicked(object sender, EventArgs e)
    {
        await ShowMenu(PcAutomationMenu);
    }

    // ========= PDF generation =========

    private async void OnCreatePdfClicked(object sender, EventArgs e)
    {
        await CreatePdf();
    }

    public async Task CreatePdf()
    {
        using (PdfDocument document = new PdfDocument())
        {
            PdfPage page = document.Pages.Add();
            PdfGraphics graphics = page.Graphics;
            PdfFont font = new PdfStandardFont(PdfFontFamily.Helvetica, 14);

            float yPosition = 20;

            foreach (var group in groupHistory)
            {
                string line = group.GetFormattedString();

                if (!string.IsNullOrEmpty(line))
                {
                    graphics.DrawString(line, font, PdfBrushes.Black, new Syncfusion.Drawing.PointF(20, yPosition));
                    yPosition += 20;

                    if (yPosition > page.GetClientSize().Height - 40)
                    {
                        page = document.Pages.Add();
                        graphics = page.Graphics;
                        yPosition = 20;
                    }
                }
            }

            using (MemoryStream stream = new MemoryStream())
            {
                document.Save(stream);
                document.Close(true);

                string filePath = Path.Combine(FileSystem.AppDataDirectory, "GroupHistory.pdf");
                File.WriteAllBytes(filePath, stream.ToArray());

                await Launcher.OpenAsync(new OpenFileRequest
                {
                    File = new ReadOnlyFile(filePath)
                });
            }
        }
    }

    // Very important function as it is the base of the whole automation feature added.
    private async void OnAutoLoginClicked(object sender, EventArgs e)
    {
        try
        {
            string barcode = _barcodeEntry?.Text?.Trim() ?? string.Empty;
            string qtyText = _quantityEntry?.Text?.Trim() ?? string.Empty;
            string? unit = (_unitPicker?.SelectedItem as string)?.Trim();

            // --- VALIDATION ---
            if (string.IsNullOrEmpty(barcode))
            {
                await DisplayAlert("No Barcode", "Scan a barcode first!", "OK");
                return;
            }

            int? qty = null;
            if (!string.IsNullOrWhiteSpace(qtyText))
            {
                if (!int.TryParse(qtyText, out int parsed))
                {
                    await DisplayAlert("Invalid Quantity", "Please enter a valid numeric QTY.", "OK");
                    return;
                }
                qty = parsed;
            }

            if (string.IsNullOrEmpty(unit))
            {
                await DisplayAlert("No Unit", "Please select a unit before sending to PC.", "OK");
                return;
            }

            _statusLabel.Text = "Connecting to PC...";
            _autoLoginButton.IsEnabled = false;

            // --- STEP 1: CHECK SERVER ---
            bool serverRunning = await _automationService.CheckServerStatusAsync();
            if (!serverRunning)
            {
                await DisplayAlert("Connection Error",
                    "Cannot reach the PC.\n\n" +
                    "Make sure:\n" +
                    "• Python server is running\n" +
                    "• Devices are on same WiFi\n" +
                    "• PC IP address is correct",
                    "OK");

                _statusLabel.Text = "PC not reachable";
                return;
            }

            // --- STEP 2: LOGIN ---
            _statusLabel.Text = "Logging in on PC...";
            var (loginSuccess, loginMessage) = await _automationService.TriggerLoginAsync();

            if (!loginSuccess)
            {
                _statusLabel.Text = "Login failed";
                await DisplayAlert("Login Error", loginMessage, "OK");
                return;
            }

            // --- STEP 3: SEND BARCODE + QTY + UNIT + SAVE ---
            _statusLabel.Text = "Sending to PC...";

            var (sendSuccess, sendMessage) =
                await _automationService.SendBarcodeAsync(barcode, qty, unit);

            if (sendSuccess)
            {
                // Show success status
                _statusLabel.Text = sendMessage;

                // Show success toast
                var toast = Toast.Make($"✓ SAVED TO INVENTORY!", ToastDuration.Long, 16);
                await toast.Show();

                // Show detailed alert
                string qtyDisplay = qty.HasValue ? qty.Value.ToString() : "N/A";
                await DisplayAlert("✓ Success",
                    $"Item saved to inventory!\n\n" +
                    $"Code: {barcode}\n" +
                    $"Quantity: {qtyDisplay}\n" +
                    $"Unit: {unit}\n\n" +
                    sendMessage,
                    "OK");

                // Clear entries for next scan
                _barcodeEntry.Text = "";
                _quantityEntry.Text = "";

                // Optional: Keep unit selected for similar items
                // _unitPicker.SelectedIndex = -1;
            }
            else
            {
                _statusLabel.Text = "❌ Save failed";

                // Show error toast
                var errorToast = Toast.Make("❌ FAILED TO SAVE", ToastDuration.Long, 16);
                await errorToast.Show();

                await DisplayAlert("❌ Send Error", sendMessage, "OK");
            }
        }
        catch (Exception ex)
        {
            _statusLabel.Text = "Error during automation";
            await DisplayAlert("Error", ex.Message, "OK");
        }
        finally
        {
            _autoLoginButton.IsEnabled = true;
        }
    }

    private void OnClearClicked(object sender, EventArgs e)
    {
        BarcodeEntry.Text = string.Empty;
        QuantityEntry.Text = string.Empty;
        StatusLabel.Text = "CLEARED.";
    }

    private void OnExtrusionsClicked(object sender, EventArgs e)
    {
        UnitPicker.ItemsSource = new List<string> { "/ BARRES", "/ RACK", "/ BOITES" };
        UnitPicker.SelectedIndex = 0;
        StatusLabel.Text = "Units set for Fenêtres → Extrusion.";
    }

    private void OnQuincaillerieClicked(object sender, EventArgs e)
    {
        UnitPicker.ItemsSource = new List<string> { "/ BOITES", "/ unité" };
        UnitPicker.SelectedIndex = 0;
        StatusLabel.Text = "Units set for Fenêtres → Quincaillerie.";
    }

    private void OnFenetresBoisClicked(object sender, EventArgs e)
    {
        UnitPicker.ItemsSource = new List<string> { "/ LONGUEUR" };
        UnitPicker.SelectedIndex = 0;
        StatusLabel.Text = "Units set for Fenêtres → Bois.";
    }

    private void OnSlabClicked(object sender, EventArgs e)
    {
        UnitPicker.ItemsSource = new List<string> { "/ unité" };
        UnitPicker.SelectedIndex = 0;
        StatusLabel.Text = "Units set for Portes → Slab";
    }

    private void OnGlazingClicked(object sender, EventArgs e)
    {
        UnitPicker.ItemsSource = new List<string> { "/ unité" };
        UnitPicker.SelectedIndex = 0;
        StatusLabel.Text = "Units set for Portes → Glazing";
    }

    private void OnComposantesClicked(object sender, EventArgs e)
    {
        UnitPicker.ItemsSource = new List<string> { "/ BOITES", "/ unité" };
        UnitPicker.SelectedIndex = 0;
        StatusLabel.Text = "Units set for Portes → Composantes";
    }

    private void OnPorteBoisClicked(object sender, EventArgs e)
    {
        UnitPicker.ItemsSource = new List<string> { "/ LONGUEUR" };
        UnitPicker.SelectedIndex = 0;
        StatusLabel.Text = "Units set for Portes → Bois";
    }
}
