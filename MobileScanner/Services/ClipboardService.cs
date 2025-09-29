using System;
using Microsoft.Maui.ApplicationModel.DataTransfer;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Syncfusion.Pdf;
using Syncfusion.Pdf.Graphics;
using System.IO;
using Microsoft.Maui.Storage;


namespace MobileScanner.Services
{
    public class ClipboardService
    {
        private readonly List<string> _clipboardHistory;
        private const int MaxHistoryItems = 50;
        

        public ClipboardService()
        {
            _clipboardHistory = new List<string>();
        }

        
        /// <summary>
        /// Copying text to clipboard and adding to history.
        /// </summary>
        public async Task<bool> CopyTextAsync(string text)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(text))
                    return false;

                await Clipboard.SetTextAsync(text);

                // Add to history (avoid duplicates)
                if (!_clipboardHistory.Contains(text))
                {
                    _clipboardHistory.Insert(0, text);

                    // Keep only the last MaxHistoryItems
                    if (_clipboardHistory.Count > MaxHistoryItems)
                    {
                        _clipboardHistory.RemoveAt(_clipboardHistory.Count - 1);
                    }
                }

                return true;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Clipboard copy failed: {ex.Message}");
                return false;
            }
        }

    public class ClipboardHistoryItem
{
    public string Text { get; set; }
    public DateTime Timestamp { get; set; }

    public ClipboardHistoryItem(string text)
    {
        Text = text;
        Timestamp = DateTime.Now;
    }

    public override string ToString()
    {
        return $"{Text} ({Timestamp:yyyy-MM-dd HH:mm:ss})";
    }
}

        /// <summary>
        /// Getting text from clipboard
        /// </summary>
        public async Task<string> GetTextAsync()
        {
            try
            {
                if (Clipboard.HasText)
                {
                    return await Clipboard.GetTextAsync() ?? string.Empty;
                }
                return string.Empty;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Clipboard get text failed: {ex.Message}");
                return string.Empty;
            }
        }
        public async Task<bool> CopyAllHistoryAsync(string separator = "\n")
        {
            try
            {
                if (_clipboardHistory.Count == 0)
                    return false;

                string allHistory = string.Join(separator, _clipboardHistory);
                await Clipboard.SetTextAsync(allHistory);
                return true;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Copy all history failed: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Copies selected history items to clipboard
        /// </summary>
        public async Task<bool> CopySelectedHistoryAsync(IEnumerable<int> indices, string separator = "\n")
        {
            try
            {
                var selectedItems = indices
                    .Where(i => i >= 0 && i < _clipboardHistory.Count)
                    .Select(i => _clipboardHistory[i])
                    .ToList();

                if (selectedItems.Count == 0)
                    return false;

                string selectedHistory = string.Join(separator, selectedItems);
                await Clipboard.SetTextAsync(selectedHistory);
                return true;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Copy selected history failed: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Copies a specific history item by index
        /// </summary>
        public async Task<bool> CopyHistoryItemAsync(int index)
        {
            try
            {
                if (index < 0 || index >= _clipboardHistory.Count)
                    return false;

                return await CopyTextAsync(_clipboardHistory[index]);
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Copy history item failed: {ex.Message}");
                return false;
            }
        }

        /// <summary>
        /// Gets formatted history with line numbers for display
        /// </summary>
        public List<string> GetFormattedHistory()
        {
            return _clipboardHistory
                .Select((item, index) => $"{index + 1}. {item}")
                .ToList();
        }

        /// <summary>
        /// Exports history as CSV format
        /// </summary>
        public async Task<bool> CopyHistoryAsCsvAsync()
        {
            try
            {
                if (_clipboardHistory.Count == 0)
                    return false;

                var csvContent = new StringBuilder();
                csvContent.AppendLine("Index,Content,Timestamp");

                for (int i = 0; i < _clipboardHistory.Count; i++)
                {
                    // Escape quotes in CSV
                    string escapedContent = _clipboardHistory[i].Replace("\"", "\"\"");
                    csvContent.AppendLine($"{i + 1},\"{escapedContent}\",{DateTime.Now:yyyy-MM-dd HH:mm:ss}");
                }

                await Clipboard.SetTextAsync(csvContent.ToString());
                return true;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Copy history as CSV failed: {ex.Message}");
                return false;
            }
        }

        // Checks if clipboard has text
        public bool HasText => Clipboard.HasText;

        // Gets clipboard history
        public List<string> GetHistory()
        {
            return _clipboardHistory.ToList();
        }

        // Gets history count
        public int HistoryCount => _clipboardHistory.Count;

        // Clears clipboard history
        public void ClearHistory()
        {
            _clipboardHistory.Clear();
        }

        /// <summary>
        /// Removes a specific item from history
        /// </summary>
        public bool RemoveHistoryItem(int index)
        {
            try
            {
                if (index >= 0 && index < _clipboardHistory.Count)
                {
                    _clipboardHistory.RemoveAt(index);
                    return true;
                }
                return false;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Remove history item failed: {ex.Message}");
                return false;
            }
        }

        // Copies a barcode with formatted message
        public async Task<bool> CopyBarcodeAsync(string barcode, string? prefix = null)
        {
            try
            {
                string textToCopy = string.IsNullOrEmpty(prefix)
                    ? barcode : $"{prefix} {barcode}";
                return await CopyTextAsync(textToCopy);
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Copy barcode failed: {ex.Message}");
                return false;
            }
        }
    }
}
