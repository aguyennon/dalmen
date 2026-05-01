using Microsoft.Extensions.Logging;
using MobileScanner.Services;
using ZXing.Net.Maui;
using ZXing.Net.Maui.Controls;
using CommunityToolkit.Maui;
using MobileScanner.Views;
using Microsoft.Maui;
using Microsoft.Maui.Hosting;
using Plugin.Maui.OCR;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Maui.Controls;
using Microsoft.Maui.Controls.Hosting;


namespace MobileScanner
{
    public static class MauiProgram
    {
        public static MauiApp CreateMauiApp()
        {
            var builder = MauiApp.CreateBuilder();
            builder
                .UseMauiApp<App>()
                .UseBarcodeReader()
                .UseMauiCommunityToolkit()
                .UseOcr()  
                .ConfigureFonts(fonts =>
                {
                    fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
                });
            // Register services for dependency injection
            builder.Services.AddSingleton<AuthService>();
            builder.Services.AddSingleton<ClipboardService>();
            builder.Services.AddTransient<MainPage>();
            builder.Services.AddTransient<ScanPage>();
#if DEBUG
            builder.Logging.AddDebug();
#endif
            return builder.Build();
        }
    }
}