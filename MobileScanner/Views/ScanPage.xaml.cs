using CommunityToolkit
.Maui.Alerts;
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
using System.Linq.Expressions;
using System.Threading.Tasks;
using ZXing.Net.Maui;
using ZXing.Net.Maui.Controls;
using ClosedXML.Excel;
using System.Runtime.InteropServices;






namespace MobileScanner.Views;

public partial class ScanPage : ContentPage
{

    private readonly AuthService _authService;
    private readonly ExcelService _excelService;
    private readonly ClipboardService _clipboardService;
    private CameraBarcodeReaderView? _cameraView;
    private Label _statusLabel;
    private Entry _barcodeEntry;
    private Button _copyButton;
    private Button _excelButton;
    private Button _clearButton;
    private Button _historyButton;
    private Button _torchButton;
    private Button _confirmButton;
    private Button _copyAllButton;
    private Button _nextButton;
    private List<string> currentScanSession = new List<string>();
    private Button _createPdfButton;
    private Button _sendExcel;

    // Changed to store groups with quantities
    private List<GroupScanData> groupHistory = new List<GroupScanData>();

    private int scanCount = 0;
    private const int MAX_SCANS = 3;
    private const int MAX_GROUP_HISTORY = 20;
    private bool isGroupScanMode = false;

    // Class to store group scan data with quantity
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

    public ScanPage(AuthService authService)
    {
        InitializeComponent();
        _authService = authService ?? new AuthService();
        _excelService = new ExcelService(_authService);
        _clipboardService = new ClipboardService();

        // Get references to controls after InitializeComponent
        _cameraView = this.FindByName<CameraBarcodeReaderView>("CameraView");
        _statusLabel = this.FindByName<Label>("StatusLabel");
        _barcodeEntry = this.FindByName<Entry>("BarcodeEntry");
        _copyButton = this.FindByName<Button>("ScanCopyButton");
        _excelButton = this.FindByName<Button>("ScanSendButton");
        _clearButton = this.FindByName<Button>("ClearButton");
        _historyButton = this.FindByName<Button>("HistoryButton");
        _torchButton = this.FindByName<Button>("TorchButton");
        _confirmButton = this.FindByName<Button>("ConfirmButton");
        _copyAllButton = this.FindByName<Button>("CopyAllButton");
        _nextButton = this.FindByName<Button>("NextButton");
        _createPdfButton = this.FindByName<Button>("CreatePdfButton");
        _sendExcel = this.FindByName<Button>("SendExcelButton");

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
                _sendExcel.Clicked += OnSendExcelClicked; // if you have separate send-to-excel button
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

    private string _lastScannedValue;
    private DateTime _lastScanTime;
    private const double DuplicateWindowSeconds = 5;
    private readonly TimeSpan DuplicateWindow = TimeSpan.FromSeconds(5);
    private readonly object _scanLock = new object();
    private readonly Dictionary<string, DateTime> _recentScans = new Dictionary<string, DateTime>();

    private void OnBarcodeScanned(string scannedValue)
    {
        if (string.IsNullOrWhiteSpace(scannedValue))
            return;

        scannedValue = NormalizeBarcode(scannedValue);

        // add to session list
        currentScanSession.Add(scannedValue);

        // update UI
        if (_barcodeEntry != null)
            _barcodeEntry.Text = scannedValue;
        if (_statusLabel != null)
            _statusLabel.Text = scannedValue;

    }

    private string NormalizeBarcode(string input)
    {
        if (string.IsNullOrEmpty(input)) return string.Empty;
        // trim and remove CR/LF and surrounding whitespace
        return input.Trim().Replace("\r", "").Replace("\n", "");
    }


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

    async Task EnsureCameraPermissionAsync()
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

    private async void ConfirmButton_Clicked(object sender, EventArgs e)
    {
        try
        {
            string? scannedCode = _barcodeEntry?.Text?.Trim();

            if (string.IsNullOrEmpty(scannedCode))
            {
                if (_statusLabel != null)
                    _statusLabel.Text = "NO CODE TO SAVE.";

                await DisplayAlert("No Code", "There is no scanned code to confirm.", "OK");
            }

            bool success = await _clipboardService.CopyBarcodeAsync(scannedCode);

            if (success)
            {
                if (_statusLabel != null)
                    _statusLabel.Text = $"CONFIRMED AND SAVED: {scannedCode}";

                await DisplayAlert("Confirmed",
                    $"Scanned code confirmed and saved to history!\nCode: {scannedCode}", "OK");

                if (_barcodeEntry != null)
                    _barcodeEntry.Text = string.Empty;

                EnableActionButtons(false);

                await Task.Delay(2000);
                if (_statusLabel != null)
                    _statusLabel.Text = "READY TO SCAN. (CODE 128)";
            }
            else
            {
                if (_statusLabel != null)
                    _statusLabel.Text = " Failed to save code...";
                await DisplayAlert("Error",
                    "Failed to save scanned code. Please try again.", "OK");
            }
        }
        catch (Exception ex)
        {
            if (_statusLabel != null)
                _statusLabel.Text = " Error during confirmation";

            await DisplayAlert("Error", $"Failed to save. {ex.Message}", "OK");
        }

    }

    private async void OnSendExcelClicked(object sender, EventArgs e)
    {
        try
        {
            string filePath = Path.Combine(FileSystem.AppDataDirectory, "GroupAndScans.xlsx");

            using (var workbook = new XLWorkbook())
            {
                var ws = workbook.Worksheets.Add("Scans");
                int row = 1;

                // Write group history, splitting each group line into separate columns
                if (groupHistory != null && groupHistory.Count > 0)
                {
                    foreach (var group in groupHistory)
                    {
                        string line = group.GetFormattedString();
                        if (!string.IsNullOrEmpty(line))
                        {
                            string[] parts = line.Split(',');

                            for (int col = 0; col < parts.Length; col++)
                            {
                                ws.Cell(row, col + 1).Value = parts[col].Trim();
                            }
                            row++;
                        }
                    }

                    // Add a blank row between group history and scanned barcodes
                    row++;
                }

                // Write scanned barcodes (each one in its own row, col A)
                if (currentScanSession != null && currentScanSession.Count > 0)
                {
                    foreach (var barcode in currentScanSession)
                    {
                        ws.Cell(row, 1).Value = barcode;
                        row++;
                    }
                }

                // Autofit columns so all content is visible
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



    private async void CameraView_BarcodesDetected(object? sender, BarcodeDetectionEventArgs e)
    {
        try
    {
        // Collect distinct normalized values from the event
        var values = e.Results?
            .Select(r => NormalizeBarcode(r.Value))
            .Where(v => !string.IsNullOrEmpty(v))
            .Distinct()
            .ToList();

        if (values == null || values.Count == 0)
            return;

        // Pause detection briefly while we process (keeps things stable)
        if (_cameraView != null)
            _cameraView.IsDetecting = false;

        var now = DateTime.UtcNow;

        foreach (var scannedCode in values)
        {
            bool shouldHandle = false;

            lock (_scanLock)
            {
                // cleanup old entries
                var oldKeys = _recentScans.Where(kv => (now - kv.Value) > DuplicateWindow)
                                          .Select(kv => kv.Key)
                                          .ToList();
                foreach (var k in oldKeys)
                    _recentScans.Remove(k);

                // check whether this code was seen recently
                if (!_recentScans.TryGetValue(scannedCode, out var last) || (now - last) > DuplicateWindow)
                {
                    // mark as seen now
                    _recentScans[scannedCode] = now;
                    shouldHandle = true;
                }
            }

            if (!shouldHandle)
            {
                // optional: small feedback for duplicate ignored (comment out if noisy)
                try
                {
                    MainThread.BeginInvokeOnMainThread(async () =>
                    {
                        var t = Toast.Make("Duplicate scan ignored", ToastDuration.Short, 12);
                        await t.Show();
                    });
                }
                catch { }

                continue;
            }

            // Handle on main thread (UI updates)
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
        // avoid crashing if something goes wrong in the detection event
        System.Diagnostics.Debug.WriteLine($"CameraView_BarcodesDetected error: {ex}");
    }
    finally
    {
        // small delay so processing settles, then resume detection
        await Task.Delay(500);
        if (_cameraView != null)
            _cameraView.IsDetecting = true;
    }
    }


    async void OnExcelClicked(object sender, EventArgs e)
    {
        if (_barcodeEntry?.Text != null)
        {
            await PostScanToExcelAsync(_barcodeEntry.Text);
        }
    }

    void OnClearClicked(object sender, EventArgs e)
    {
        if (_barcodeEntry != null)
            _barcodeEntry.Text = string.Empty;

        if (_statusLabel != null)
            _statusLabel.Text = "READY TO SCAN. (CODE 128)";

        // clear debounce so same code can be scanned again immediately
        lock (_scanLock)
        {
            _recentScans.Clear();
        }

        EnableActionButtons(false);
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

    private async void OnCopyClicked(object sender, EventArgs e)
    {
        try
        {
            var text = _barcodeEntry?.Text?.Trim();

            if (string.IsNullOrEmpty(text))
            {
                if (_statusLabel != null)
                    _statusLabel.Text = "Nothing to copy.";
                var t = Toast.Make("No barcode to copy", ToastDuration.Short, 14);
                await t.Show();
                return;
            }

            bool success = await _clipboardService.CopyBarcodeAsync(text);

            if (success)
            {
                if (_statusLabel != null)
                    _statusLabel.Text = $"Copied: {text}";

                _barcodeEntry.Text = string.Empty;

                // reset debounce so user can scan again immediately if needed
                lock (_scanLock)
                {
                    _recentScans.Remove(text);
                }

                await DisplayAlert("CLIPBOARD", "Barcode copied to clipboard!", "OK");
            }
            else
            {
                if (_statusLabel != null)
                    _statusLabel.Text = "Failed to copy to clipboard...";
                await DisplayAlert("Error", "Failed to copy barcode.", "OK");
            }
        }
        catch (Exception ex)
        {
            await DisplayAlert("Error", $"Copy error: {ex.Message}", "OK");
        }
    }


    //  Copy All History button handler
    async void OnCopyAllClicked(object sender, EventArgs e)
    {
        try
        {
            if (_statusLabel != null)
                _statusLabel.Text = "Copying all history...";

            var success = await _clipboardService.CopyAllHistoryAsync();

            if (success)
            {
                var historyCount = _clipboardService.HistoryCount;
                if (_statusLabel != null)
                    _statusLabel.Text = $"Copied all {historyCount} items to clipboard";

                await DisplayAlert("Success",
                    $"All {historyCount} history items copied to clipboard!", "OK");
            }
            else
            {
                if (_statusLabel != null)
                    _statusLabel.Text = "No history to copy";

                await DisplayAlert("Info", "No history items to copy.", "OK");
            }
        }
        catch (Exception ex)
        {
            if (_statusLabel != null)
                _statusLabel.Text = "Failed to copy history";

            await DisplayAlert("Error", $"Failed to copy history: {ex.Message}", "OK");
        }
    }

    async void OnPasteClicked(object sender, EventArgs e)
    {
        try
        {
            if (_statusLabel != null)
                _statusLabel.Text = "Checking clipboard...";

            if (!_clipboardService.HasText)
            {
                await DisplayAlert("Clipboard Empty", "No text found in clipboard.", "OK");
                if (_statusLabel != null)
                    _statusLabel.Text = "READY TO SCAN. (CODE 128)";
                return;
            }

            string clipboardText = await _clipboardService.GetTextAsync();

            if (string.IsNullOrWhiteSpace(clipboardText))
            {
                await DisplayAlert("Clipboard Empty", "Clipboard contains no text.", "OK");
                if (_statusLabel != null)
                    _statusLabel.Text = "READY TO SCAN. (CODE 128)";
                return;
            }

            if (_barcodeEntry != null)
                _barcodeEntry.Text = clipboardText;

            if (_statusLabel != null)
                _statusLabel.Text = $"Pasted from clipboard: {clipboardText}";

            EnableActionButtons(true);
        }
        catch (Exception ex)
        {
            if (_statusLabel != null)
                _statusLabel.Text = "Failed to paste from clipboard";
            await DisplayAlert("Paste Error", $"Failed to paste: {ex.Message}", "OK");
        }
    }

    private void OnBarcodeScannedInGroup(string barcodeValue)
    {

        if (_barcodeEntry != null)
            _barcodeEntry.Text = barcodeValue;

        if (_statusLabel != null)
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
                        $"Maximum {MAX_GROUP_HISTORY} groups reached. Please clear group history to use again.", "OK");
                });
                return;
            }

            StartGroupScanning();
            return;
        }

        string currentBarcode = _barcodeEntry?.Text?.Trim();

        if (string.IsNullOrEmpty(currentBarcode))
        {
            return; // So that after the second scan it keeps going instead of displaying the bugged message
        }

        currentScanSession.Add(currentBarcode);
        scanCount++;

        if (scanCount >= MAX_SCANS)
        {
            if (currentScanSession.Count >= MAX_SCANS)
            {
                // Create new GroupScanData and add to history
                var groupData = new GroupScanData();
                groupData.Scans.AddRange(currentScanSession);
                groupHistory.Add(groupData);

                MainThread.BeginInvokeOnMainThread(async () =>
                {
                    await DisplayAlert("Group Scans Complete",
                    $"{currentScanSession[0]}\n" +
                    $"{currentScanSession[1]}\n" +
                    $"{currentScanSession[2]}", "OK");
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

        if (_statusLabel != null)
            _statusLabel.Text = "GROUP MODE: Scan barcode (1/3)";
    }

    private void PrepareForNextScan()
    {
        if (_barcodeEntry != null)
            _barcodeEntry.Text = string.Empty;

        if (_nextButton != null)
            _nextButton.IsEnabled = false;

        if (_statusLabel != null)
            _statusLabel.Text = $"GROUP MODE: Scan barcode {scanCount + 1}/3";

        MainThread.BeginInvokeOnMainThread(async () =>
        {
            await DisplayAlert("Next Scan", $"Barcode {scanCount}/3 confirmed! Now scan barcode {scanCount + 1} of 3", "OK");
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

        if (_statusLabel != null)
            _statusLabel.Text = "READY TO SCAN. (CODE 128)";

        if (_barcodeEntry != null)
            _barcodeEntry.Text = string.Empty;

    }

    private async void OnGroupHistoryClicked(object sender, EventArgs e)
    {

        if (groupHistory.Count == 0)
        {
            await DisplayAlert("No Group History", "No barcode groups have been scanned yet.", "OK");
            return;
        }

        // Updated to use new DisplayActionSheet with Add QTY option
        string action = await DisplayActionSheet("Group History", "Cancel", "Clear All Groups", "View Groups", "Add QTY");

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

        // First, let user select which group to add quantity to
        var groupOptions = new string[groupHistory.Count + 1];
        groupOptions[0] = "Cancel";

        for (int i = 0; i < groupHistory.Count; i++)
        {
            var preview = groupHistory[i].Scans.Count > 0 ?
                groupHistory[i].Scans[0].Substring(0, Math.Min(10, groupHistory[i].Scans[0].Length)) + "..." :
                "Empty";

            string qtyText = groupHistory[i].Quantity.HasValue ? $" (QTY: {groupHistory[i].Quantity})" : " (No QTY)";
            groupOptions[i + 1] = $"Group {i + 1}: {preview}{qtyText}";
        }

        string selectedGroup = await DisplayActionSheet("Select Group to Add Quantity",
            groupOptions[0], null, groupOptions.Skip(1).ToArray());

        if (selectedGroup == "Cancel" || string.IsNullOrEmpty(selectedGroup))
            return;

        // Extract group index from selection
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

        // Prompt for quantity
        string quantityInput = await DisplayPromptAsync("Add Quantity",
            $"Enter quantity for Group {groupIndex + 1}:", "OK", "Cancel",
            "Enter number...", -1, Keyboard.Numeric);

        if (string.IsNullOrWhiteSpace(quantityInput))
            return;

        if (int.TryParse(quantityInput, out int quantity) && quantity > 0)
        {
            groupHistory[groupIndex].Quantity = quantity;

            await DisplayAlert("Success",
                $"Quantity {quantity} added to Group {groupIndex + 1}!\n\n" +
                $"Updated format:\n{groupHistory[groupIndex].GetFormattedString()}", "OK");

            if (_statusLabel != null)
                _statusLabel.Text = $"Quantity {quantity} added to Group {groupIndex + 1}";
        }
        else
        {
            await DisplayAlert("Invalid Input", "Please enter a valid positive number.", "OK");
        }
    }

    private async Task ClearGroupHistory()
    {
        bool confirm = await DisplayAlert("Clear Group History",
            "Are you sure you want to clear all group history? This cannot be undone.", "Yes", "No");

        if (confirm)
        {
            groupHistory.Clear();

            // Re-enable group scanning if it was disabled
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

        // Add others if you want them to be toggled together
        // Example:
        // if (_historyButton != null)
        //     _historyButton.IsEnabled = enabled;
    }


    async Task PostScanToExcelAsync(string code)
    {
        try
        {
            if (_statusLabel != null)
                _statusLabel.Text = "Posting to Excel...";

            bool success = await _excelService.AppendScanToExcelAsync(code);

            if (success)
            {
                if (_statusLabel != null)
                    _statusLabel.Text = $" Added to Excel: {code}";
                await DisplayAlert("Success",
                    $"Scan successfully added to Excel!\nCode: {code}", "OK");
            }
            else
            {
                if (_statusLabel != null)
                    _statusLabel.Text = " Failed to add to Excel";
                await DisplayAlert("Error",
                    "Failed to add scan to Excel. Please try again.", "OK");
            }
        }
        catch (Exception ex)
        {
            if (_statusLabel != null)
                _statusLabel.Text = " Excel error";
            await DisplayAlert("Excel Error",
                $"Failed to update Excel: {ex.Message}", "OK");
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

    void OnTorchClicked(object sender, EventArgs e)
    {
        if (_cameraView != null) 
            _cameraView.IsTorchOn = !_cameraView.IsTorchOn;
    }

    void OnFlipClicked(object sender, EventArgs e)
    {
        if (_cameraView != null)
        {
            _cameraView.CameraLocation = _cameraView.CameraLocation == CameraLocation.Rear
                ? CameraLocation.Front
                : CameraLocation.Rear;
        }
    }

    private void OnCaptureClicked(object sender, EventArgs e)
    {
        // TODO: Implement the logic for the capture button click
        // For now, you can leave it empty or add a placeholder
    }


}