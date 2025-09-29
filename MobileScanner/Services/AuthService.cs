using Microsoft.Identity.Client;
using System;
using System.Linq;
using System.Threading.Tasks;
using System.Net.Http;

namespace MobileScanner.Services
{
    public class AuthService
    {
        private IPublicClientApplication _pca;
        // Change _accessToken to nullable
        private string? _accessToken;
        
        private string[] _scopes = { "User.Read", "Files.ReadWrite", "Files.ReadWrite.All" };


        public bool IsAuthenticated { get; private set; }
        // Change Username property to nullable
        public string? Username { get; private set; }


        public AuthService()
        {
            _pca = PublicClientApplicationBuilder
                .Create("cb1b39da-ac96-4bb0-a2e9-64d2b357a832")
                .WithAuthority("https://login.microsoftonline.com/common")
                .WithRedirectUri("msalcb1b39da-ac96-4bb0-a2e9-64d2b357a832://auth")
                .Build();
        }

        public async Task<bool> LoginAsync()
        {
            try
            {
                // Try silent login first
                var accounts = await _pca.GetAccountsAsync();
                if (accounts.Any())
                {
                    var result = await _pca.AcquireTokenSilent(_scopes, accounts.FirstOrDefault())
                        .ExecuteAsync();

                    _accessToken = result.AccessToken;
                    Username = result.Account.Username;
                    IsAuthenticated = true;
                    return true;
                }

                // Interactive login
                var interactiveResult = await _pca.AcquireTokenInteractive(_scopes)
                    .WithPrompt(Prompt.SelectAccount)
                    .ExecuteAsync();

                _accessToken = interactiveResult.AccessToken;
                Username = interactiveResult.Account.Username;
                IsAuthenticated = true;
                return true;
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"Login failed: {ex.Message}");
                IsAuthenticated = false;
                return false;
            }
        }

        public string GetAccessToken()
        {
            return _accessToken ?? string.Empty;
        }

        public HttpClient? GetAuthenticatedHttpClient()
        {
            if (!IsAuthenticated || string.IsNullOrEmpty(_accessToken))
                return null;

            var httpClient = new HttpClient();
            httpClient.DefaultRequestHeaders.Add("Authorization", $"Bearer {_accessToken}");
            return httpClient;
        }

        public async Task LogoutAsync()
        {
            var accounts = await _pca.GetAccountsAsync();
            foreach (var account in accounts)
            {
                await _pca.RemoveAsync(account);
            }

            IsAuthenticated = false;
            Username = null;
            _accessToken = null;
        }
    }
}