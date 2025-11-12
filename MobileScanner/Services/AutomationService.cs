using Microsoft.Graph.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace MobileScanner.Services
{
    public class AutomationService
    {
        private readonly HttpClient _httpClient;
        private const string SERVER_URL = "http://192.168.1.186:5000";

        public AutomationService()
        {
            _httpClient = new HttpClient
            {
                Timeout = TimeSpan.FromSeconds(30)
            };
        }

        public async Task<(bool Success, string Message)> SendBarcodeAsync(string barcode)
        {
            try
            {
                var content = new StringContent(
                    JsonSerializer.Serialize(new { barcode }),
                    Encoding.UTF8,
                    "application/json");

                var response = await _httpClient.PostAsync($"{SERVER_URL}/input_barcode", content);

                var resultJson = await response.Content.ReadAsStringAsync();
                var result = JsonSerializer.Deserialize<ApiResponse>(resultJson);

                return (result?.Success ?? false, result?.Message ?? "Unknown error");
            }
            catch (Exception ex)
            {
                return (false, $"Connection error: {ex.Message}");
            }
        }
        
        public async Task<(bool Success, string Message)> TriggerLoginAsync()
        {
            try
            {
                var response = await _httpClient.PostAsync(
                    $"{SERVER_URL}/login", null);

                var content = await response.Content.ReadAsStringAsync();
                var result = JsonSerializer.Deserialize<ApiResponse>(content);

                return (result?.Success ?? false, result?.Message ?? "Unknown error");
            }
            catch (Exception ex)
            {
                return (false, $"Connection error: {ex.Message}");
            }
        }

        public async Task<bool> CheckServerStatusAsync()
        {
            try
            {
                var response = await _httpClient.GetAsync($"{SERVER_URL}/status");
                return response.IsSuccessStatusCode;
            }
            catch
            {
                return false;
            }
        }

        public async Task<bool> CloseBrowserAsync()
        {
            try
            {
                var response = await _httpClient.PostAsync($"{SERVER_URL}/close", null); 
                return response.IsSuccessStatusCode;
            }
            catch
            {
                return false;
            }
        }

        private class ApiResponse
        {
            public bool Success { get; set; }
            public string Message { get; set; }
        }
    }
}
