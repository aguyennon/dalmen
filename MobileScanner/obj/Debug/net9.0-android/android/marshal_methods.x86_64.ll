; ModuleID = 'marshal_methods.x86_64.ll'
source_filename = "marshal_methods.x86_64.ll"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-android21"

%struct.MarshalMethodName = type {
	i64, ; uint64_t id
	ptr ; char* name
}

%struct.MarshalMethodsManagedClass = type {
	i32, ; uint32_t token
	ptr ; MonoClass klass
}

@assembly_image_cache = dso_local local_unnamed_addr global [377 x ptr] zeroinitializer, align 16

; Each entry maps hash of an assembly name to an index into the `assembly_image_cache` array
@assembly_image_cache_hashes = dso_local local_unnamed_addr constant [1131 x i64] [
	i64 u0x00067106fe65b365, ; 0: Microsoft.Kiota.Serialization.Text.dll => 219
	i64 u0x001e58127c546039, ; 1: lib_System.Globalization.dll.so => 42
	i64 u0x0024d0f62dee05bd, ; 2: Xamarin.KotlinX.Coroutines.Core.dll => 331
	i64 u0x0071cf2d27b7d61e, ; 3: lib_Xamarin.AndroidX.SwipeRefreshLayout.dll.so => 308
	i64 u0x01109b0e4d99e61f, ; 4: System.ComponentModel.Annotations.dll => 13
	i64 u0x01af0bd6467d518e, ; 5: lib_ZXing.Net.MAUI.dll.so => 336
	i64 u0x02123411c4e01926, ; 6: lib_Xamarin.AndroidX.Navigation.Runtime.dll.so => 298
	i64 u0x022e81ea9c46e03a, ; 7: lib_CommunityToolkit.Maui.Core.dll.so => 178
	i64 u0x02827b47e97f2378, ; 8: System.Security.Cryptography.Pkcs.dll => 239
	i64 u0x0284512fad379f7e, ; 9: System.Runtime.Handles => 105
	i64 u0x02abedc11addc1ed, ; 10: lib_Mono.Android.Runtime.dll.so => 171
	i64 u0x02f55bf70672f5c8, ; 11: lib_System.IO.FileSystem.DriveInfo.dll.so => 48
	i64 u0x032267b2a94db371, ; 12: lib_Xamarin.AndroidX.AppCompat.dll.so => 250
	i64 u0x033a1d0324ba06bd, ; 13: Microsoft.IO.RecyclableMemoryStream.dll => 212
	i64 u0x03621c804933a890, ; 14: System.Buffers => 7
	i64 u0x0399610510a38a38, ; 15: lib_System.Private.DataContractSerialization.dll.so => 86
	i64 u0x043032f1d071fae0, ; 16: ru/Microsoft.Maui.Controls.resources => 362
	i64 u0x044440a55165631e, ; 17: lib-cs-Microsoft.Maui.Controls.resources.dll.so => 340
	i64 u0x046eb1581a80c6b0, ; 18: vi/Microsoft.Maui.Controls.resources => 368
	i64 u0x0470607fd33c32db, ; 19: Microsoft.IdentityModel.Abstractions.dll => 205
	i64 u0x047408741db2431a, ; 20: Xamarin.AndroidX.DynamicAnimation => 274
	i64 u0x0517ef04e06e9f76, ; 21: System.Net.Primitives => 71
	i64 u0x0565d18c6da3de38, ; 22: Xamarin.AndroidX.RecyclerView => 301
	i64 u0x0581db89237110e9, ; 23: lib_System.Collections.dll.so => 12
	i64 u0x05989cb940b225a9, ; 24: Microsoft.Maui.dll => 222
	i64 u0x05a1c25e78e22d87, ; 25: lib_System.Runtime.CompilerServices.Unsafe.dll.so => 102
	i64 u0x06076b5d2b581f08, ; 26: zh-HK/Microsoft.Maui.Controls.resources => 369
	i64 u0x06388ffe9f6c161a, ; 27: System.Xml.Linq.dll => 156
	i64 u0x06600c4c124cb358, ; 28: System.Configuration.dll => 19
	i64 u0x067f95c5ddab55b3, ; 29: lib_Xamarin.AndroidX.Fragment.Ktx.dll.so => 279
	i64 u0x0680a433c781bb3d, ; 30: Xamarin.AndroidX.Collection.Jvm => 261
	i64 u0x069fff96ec92a91d, ; 31: System.Xml.XPath.dll => 161
	i64 u0x070b0847e18dab68, ; 32: Xamarin.AndroidX.Emoji2.ViewsHelper.dll => 276
	i64 u0x0739448d84d3b016, ; 33: lib_Xamarin.AndroidX.VectorDrawable.dll.so => 311
	i64 u0x07469f2eecce9e85, ; 34: mscorlib.dll => 167
	i64 u0x07c57877c7ba78ad, ; 35: ru/Microsoft.Maui.Controls.resources.dll => 362
	i64 u0x07dcdc7460a0c5e4, ; 36: System.Collections.NonGeneric => 10
	i64 u0x08122e52765333c8, ; 37: lib_Microsoft.Extensions.Logging.Debug.dll.so => 198
	i64 u0x0862024e5db21191, ; 38: System.Private.Windows.Core.dll => 235
	i64 u0x088610fc2509f69e, ; 39: lib_Xamarin.AndroidX.VectorDrawable.Animated.dll.so => 312
	i64 u0x08881a0a9768df86, ; 40: lib_Azure.Core.dll.so => 174
	i64 u0x08a7c865576bbde7, ; 41: System.Reflection.Primitives => 96
	i64 u0x08c9d051a4a817e5, ; 42: Xamarin.AndroidX.CustomView.PoolingContainer.dll => 272
	i64 u0x08f266f8aa30ea83, ; 43: lib_Microsoft.Kiota.Serialization.Text.dll.so => 219
	i64 u0x08f3c9788ee2153c, ; 44: Xamarin.AndroidX.DrawerLayout => 273
	i64 u0x09138715c92dba90, ; 45: lib_System.ComponentModel.Annotations.dll.so => 13
	i64 u0x0919c28b89381a0b, ; 46: lib_Microsoft.Extensions.Options.dll.so => 199
	i64 u0x092266563089ae3e, ; 47: lib_System.Collections.NonGeneric.dll.so => 10
	i64 u0x095cacaf6b6a32e4, ; 48: System.Memory.Data => 238
	i64 u0x09b574aaed8045a8, ; 49: lib_Microsoft.Graph.dll.so => 201
	i64 u0x09d144a7e214d457, ; 50: System.Security.Cryptography => 127
	i64 u0x09e2b9f743db21a8, ; 51: lib_System.Reflection.Metadata.dll.so => 95
	i64 u0x0a980941fa112bc4, ; 52: System.Security.Cryptography.Xml => 240
	i64 u0x0abb3e2b271edc45, ; 53: System.Threading.Channels.dll => 140
	i64 u0x0b06b1feab070143, ; 54: System.Formats.Tar => 39
	i64 u0x0b3b632c3bbee20c, ; 55: sk/Microsoft.Maui.Controls.resources => 363
	i64 u0x0b6aff547b84fbe9, ; 56: Xamarin.KotlinX.Serialization.Core.Jvm => 334
	i64 u0x0bda4c81cfb5f63b, ; 57: Syncfusion.Pdf.Portable => 232
	i64 u0x0be2e1f8ce4064ed, ; 58: Xamarin.AndroidX.ViewPager => 314
	i64 u0x0c3ca6cc978e2aae, ; 59: pt-BR/Microsoft.Maui.Controls.resources => 359
	i64 u0x0c3d7adcdb333bf0, ; 60: Xamarin.AndroidX.Camera.Lifecycle => 257
	i64 u0x0c59ad9fbbd43abe, ; 61: Mono.Android => 172
	i64 u0x0c65741e86371ee3, ; 62: lib_Xamarin.Android.Glide.GifDecoder.dll.so => 244
	i64 u0x0c74af560004e816, ; 63: Microsoft.Win32.Registry.dll => 5
	i64 u0x0c7790f60165fc06, ; 64: lib_Microsoft.Maui.Essentials.dll.so => 223
	i64 u0x0c83c82812e96127, ; 65: lib_System.Net.Mail.dll.so => 67
	i64 u0x0cce4bce83380b7f, ; 66: Xamarin.AndroidX.Security.SecurityCrypto => 305
	i64 u0x0d13cd7cce4284e4, ; 67: System.Security.SecureString => 130
	i64 u0x0d3b5ab8b2766190, ; 68: lib_Microsoft.Bcl.AsyncInterfaces.dll.so => 186
	i64 u0x0d63f4f73521c24f, ; 69: lib_Xamarin.AndroidX.SavedState.SavedState.Ktx.dll.so => 304
	i64 u0x0e04e702012f8463, ; 70: Xamarin.AndroidX.Emoji2 => 275
	i64 u0x0e14e73a54dda68e, ; 71: lib_System.Net.NameResolution.dll.so => 68
	i64 u0x0f37dd7a62ae99af, ; 72: lib_Xamarin.AndroidX.Collection.Ktx.dll.so => 262
	i64 u0x0f5e7abaa7cf470a, ; 73: System.Net.HttpListener => 66
	i64 u0x1001f97bbe242e64, ; 74: System.IO.UnmanagedMemoryStream => 57
	i64 u0x102861e4055f511a, ; 75: Microsoft.Bcl.AsyncInterfaces.dll => 186
	i64 u0x102a31b45304b1da, ; 76: Xamarin.AndroidX.CustomView => 271
	i64 u0x1065c4cb554c3d75, ; 77: System.IO.IsolatedStorage.dll => 52
	i64 u0x10f6cfcbcf801616, ; 78: System.IO.Compression.Brotli => 43
	i64 u0x111e7120c198511e, ; 79: DocumentFormat.OpenXml.Framework.dll => 180
	i64 u0x114443cdcf2091f1, ; 80: System.Security.Cryptography.Primitives => 125
	i64 u0x118d570f508803d1, ; 81: Xamarin.AndroidX.Camera.Camera2.dll => 255
	i64 u0x11a603952763e1d4, ; 82: System.Net.Mail => 67
	i64 u0x11a70d0e1009fb11, ; 83: System.Net.WebSockets.dll => 81
	i64 u0x11f26371eee0d3c1, ; 84: lib_Xamarin.AndroidX.Lifecycle.Runtime.Ktx.dll.so => 289
	i64 u0x11fbe62d469cc1c8, ; 85: Microsoft.VisualStudio.DesignTools.TapContract.dll => 374
	i64 u0x12128b3f59302d47, ; 86: lib_System.Xml.Serialization.dll.so => 158
	i64 u0x123639456fb056da, ; 87: System.Reflection.Emit.Lightweight.dll => 92
	i64 u0x12521e9764603eaa, ; 88: lib_System.Resources.Reader.dll.so => 99
	i64 u0x125b7f94acb989db, ; 89: Xamarin.AndroidX.RecyclerView.dll => 301
	i64 u0x126ee4b0de53cbfd, ; 90: Microsoft.IdentityModel.Protocols.OpenIdConnect.dll => 209
	i64 u0x12d3b63863d4ab0b, ; 91: lib_System.Threading.Overlapped.dll.so => 141
	i64 u0x134eab1061c395ee, ; 92: System.Transactions => 151
	i64 u0x137b34d6751da129, ; 93: System.Drawing.Common => 234
	i64 u0x138567fa954faa55, ; 94: Xamarin.AndroidX.Browser => 254
	i64 u0x13a01de0cbc3f06c, ; 95: lib-fr-Microsoft.Maui.Controls.resources.dll.so => 346
	i64 u0x13beedefb0e28a45, ; 96: lib_System.Xml.XmlDocument.dll.so => 162
	i64 u0x13f1e5e209e91af4, ; 97: lib_Java.Interop.dll.so => 169
	i64 u0x13f1e880c25d96d1, ; 98: he/Microsoft.Maui.Controls.resources => 347
	i64 u0x143a1f6e62b82b56, ; 99: Microsoft.IdentityModel.Protocols.OpenIdConnect => 209
	i64 u0x143d8ea60a6a4011, ; 100: Microsoft.Extensions.DependencyInjection.Abstractions => 192
	i64 u0x1497051b917530bd, ; 101: lib_System.Net.WebSockets.dll.so => 81
	i64 u0x14b78ce3adce0011, ; 102: Microsoft.VisualStudio.DesignTools.TapContract => 374
	i64 u0x14d612a531c79c05, ; 103: Xamarin.JSpecify.dll => 326
	i64 u0x14e68447938213b7, ; 104: Xamarin.AndroidX.Collection.Ktx.dll => 262
	i64 u0x152a448bd1e745a7, ; 105: Microsoft.Win32.Primitives => 4
	i64 u0x1557de0138c445f4, ; 106: lib_Microsoft.Win32.Registry.dll.so => 5
	i64 u0x15bdc156ed462f2f, ; 107: lib_System.IO.FileSystem.dll.so => 51
	i64 u0x15e300c2c1668655, ; 108: System.Resources.Writer.dll => 101
	i64 u0x16bf2a22df043a09, ; 109: System.IO.Pipes.dll => 56
	i64 u0x16d2f10b6ba5c55c, ; 110: MobileScanner.dll => 0
	i64 u0x16ea2b318ad2d830, ; 111: System.Security.Cryptography.Algorithms => 120
	i64 u0x16eeae54c7ebcc08, ; 112: System.Reflection.dll => 98
	i64 u0x17125c9a85b4929f, ; 113: lib_netstandard.dll.so => 168
	i64 u0x1716866f7416792e, ; 114: lib_System.Security.AccessControl.dll.so => 118
	i64 u0x174f71c46216e44a, ; 115: Xamarin.KotlinX.Coroutines.Core => 331
	i64 u0x1752c12f1e1fc00c, ; 116: System.Core => 21
	i64 u0x17b56e25558a5d36, ; 117: lib-hu-Microsoft.Maui.Controls.resources.dll.so => 350
	i64 u0x17f9358913beb16a, ; 118: System.Text.Encodings.Web => 137
	i64 u0x1809fb23f29ba44a, ; 119: lib_System.Reflection.TypeExtensions.dll.so => 97
	i64 u0x18402a709e357f3b, ; 120: lib_Xamarin.KotlinX.Serialization.Core.Jvm.dll.so => 334
	i64 u0x184e267d06b0b855, ; 121: EPPlus.System.Drawing.dll => 183
	i64 u0x18a9befae51bb361, ; 122: System.Net.WebClient => 77
	i64 u0x18f0ce884e87d89a, ; 123: nb/Microsoft.Maui.Controls.resources.dll => 356
	i64 u0x19777fba3c41b398, ; 124: Xamarin.AndroidX.Startup.StartupRuntime.dll => 307
	i64 u0x19a4c090f14ebb66, ; 125: System.Security.Claims => 119
	i64 u0x1a040febb58bf51e, ; 126: lib_Xamarin.AndroidX.Camera.View.dll.so => 258
	i64 u0x1a91866a319e9259, ; 127: lib_System.Collections.Concurrent.dll.so => 8
	i64 u0x1aac34d1917ba5d3, ; 128: lib_System.dll.so => 165
	i64 u0x1aad60783ffa3e5b, ; 129: lib-th-Microsoft.Maui.Controls.resources.dll.so => 365
	i64 u0x1aea8f1c3b282172, ; 130: lib_System.Net.Ping.dll.so => 70
	i64 u0x1b4b7a1d0d265fa2, ; 131: Xamarin.Android.Glide.DiskLruCache => 243
	i64 u0x1bbdb16cfa73e785, ; 132: Xamarin.AndroidX.Lifecycle.Runtime.Ktx.Android => 290
	i64 u0x1bc766e07b2b4241, ; 133: Xamarin.AndroidX.ResourceInspection.Annotation.dll => 302
	i64 u0x1c5217a9e4973753, ; 134: lib_Microsoft.Extensions.FileProviders.Physical.dll.so => 194
	i64 u0x1c753b5ff15bce1b, ; 135: Mono.Android.Runtime.dll => 171
	i64 u0x1cd47467799d8250, ; 136: System.Threading.Tasks.dll => 145
	i64 u0x1d23eafdc6dc346c, ; 137: System.Globalization.Calendars.dll => 40
	i64 u0x1da4110562816681, ; 138: Xamarin.AndroidX.Security.SecurityCrypto.dll => 305
	i64 u0x1db6820994506bf5, ; 139: System.IO.FileSystem.AccessControl.dll => 47
	i64 u0x1dbb0c2c6a999acb, ; 140: System.Diagnostics.StackTrace => 30
	i64 u0x1e3d87657e9659bc, ; 141: Xamarin.AndroidX.Navigation.UI => 299
	i64 u0x1e71143913d56c10, ; 142: lib-ko-Microsoft.Maui.Controls.resources.dll.so => 354
	i64 u0x1e7c31185e2fb266, ; 143: lib_System.Threading.Tasks.Parallel.dll.so => 144
	i64 u0x1ecd8f8a12012ea7, ; 144: lib_Syncfusion.Compression.Portable.dll.so => 230
	i64 u0x1ed8fcce5e9b50a0, ; 145: Microsoft.Extensions.Options.dll => 199
	i64 u0x1f055d15d807e1b2, ; 146: System.Xml.XmlSerializer => 163
	i64 u0x1f1ed22c1085f044, ; 147: lib_System.Diagnostics.FileVersionInfo.dll.so => 28
	i64 u0x1f61df9c5b94d2c1, ; 148: lib_System.Numerics.dll.so => 84
	i64 u0x1f750bb5421397de, ; 149: lib_Xamarin.AndroidX.Tracing.Tracing.dll.so => 309
	i64 u0x20237ea48006d7a8, ; 150: lib_System.Net.WebClient.dll.so => 77
	i64 u0x209375905fcc1bad, ; 151: lib_System.IO.Compression.Brotli.dll.so => 43
	i64 u0x20fab3cf2dfbc8df, ; 152: lib_System.Diagnostics.Process.dll.so => 29
	i64 u0x2110167c128cba15, ; 153: System.Globalization => 42
	i64 u0x212dabedfbeb018b, ; 154: lib_EPPlus.dll.so => 181
	i64 u0x21419508838f7547, ; 155: System.Runtime.CompilerServices.VisualC => 103
	i64 u0x2174319c0d835bc9, ; 156: System.Runtime => 117
	i64 u0x2198e5bc8b7153fa, ; 157: Xamarin.AndroidX.Annotation.Experimental.dll => 248
	i64 u0x2199f06354c82d3b, ; 158: System.ClientModel.dll => 233
	i64 u0x219ea1b751a4dee4, ; 159: lib_System.IO.Compression.ZipFile.dll.so => 45
	i64 u0x21cc7e445dcd5469, ; 160: System.Reflection.Emit.ILGeneration => 91
	i64 u0x220fd4f2e7c48170, ; 161: th/Microsoft.Maui.Controls.resources => 365
	i64 u0x224538d85ed15a82, ; 162: System.IO.Pipes => 56
	i64 u0x22908438c6bed1af, ; 163: lib_System.Threading.Timer.dll.so => 148
	i64 u0x22fbc14e981e3b45, ; 164: lib_Microsoft.VisualStudio.DesignTools.MobileTapContracts.dll.so => 373
	i64 u0x235fb4941dc174e1, ; 165: DocumentFormat.OpenXml => 179
	i64 u0x237be844f1f812c7, ; 166: System.Threading.Thread.dll => 146
	i64 u0x23852b3bdc9f7096, ; 167: System.Resources.ResourceManager => 100
	i64 u0x23986dd7e5d4fc01, ; 168: System.IO.FileSystem.Primitives.dll => 49
	i64 u0x2407aef2bbe8fadf, ; 169: System.Console => 20
	i64 u0x240abe014b27e7d3, ; 170: Xamarin.AndroidX.Core.dll => 267
	i64 u0x24707cada0dad313, ; 171: Microsoft.Office.Interop.Excel.dll => 225
	i64 u0x247619fe4413f8bf, ; 172: System.Runtime.Serialization.Primitives.dll => 114
	i64 u0x24de8d301281575e, ; 173: Xamarin.Android.Glide => 241
	i64 u0x25165b0abac617ca, ; 174: Syncfusion.Pdf.Portable.dll => 232
	i64 u0x252073cc3caa62c2, ; 175: fr/Microsoft.Maui.Controls.resources.dll => 346
	i64 u0x256b8d41255f01b1, ; 176: Xamarin.Google.Crypto.Tink.Android => 321
	i64 u0x25e1850d10cdc8f7, ; 177: lib_Xamarin.AndroidX.Camera.Camera2.dll.so => 255
	i64 u0x2662c629b96b0b30, ; 178: lib_Xamarin.Kotlin.StdLib.dll.so => 327
	i64 u0x268c1439f13bcc29, ; 179: lib_Microsoft.Extensions.Primitives.dll.so => 200
	i64 u0x268f1dca6d06d437, ; 180: Xamarin.AndroidX.Camera.Core => 256
	i64 u0x26a670e154a9c54b, ; 181: System.Reflection.Extensions.dll => 94
	i64 u0x26d077d9678fe34f, ; 182: System.IO.dll => 58
	i64 u0x270a44600c921861, ; 183: System.IdentityModel.Tokens.Jwt => 236
	i64 u0x273f3515de5faf0d, ; 184: id/Microsoft.Maui.Controls.resources.dll => 351
	i64 u0x2742545f9094896d, ; 185: hr/Microsoft.Maui.Controls.resources => 349
	i64 u0x2759af78ab94d39b, ; 186: System.Net.WebSockets => 81
	i64 u0x27b2b16f3e9de038, ; 187: Xamarin.Google.Crypto.Tink.Android.dll => 321
	i64 u0x27b410442fad6cf1, ; 188: Java.Interop.dll => 169
	i64 u0x27b97e0d52c3034a, ; 189: System.Diagnostics.Debug => 26
	i64 u0x2801845a2c71fbfb, ; 190: System.Net.Primitives.dll => 71
	i64 u0x286835e259162700, ; 191: lib_Xamarin.AndroidX.ProfileInstaller.ProfileInstaller.dll.so => 300
	i64 u0x2949f3617a02c6b2, ; 192: Xamarin.AndroidX.ExifInterface => 277
	i64 u0x294b9b92ac1a634f, ; 193: Microsoft.Kiota.Serialization.Text => 219
	i64 u0x29f947844fb7fc11, ; 194: Microsoft.Maui.Controls.HotReload.Forms => 372
	i64 u0x2a128783efe70ba0, ; 195: uk/Microsoft.Maui.Controls.resources.dll => 367
	i64 u0x2a3b095612184159, ; 196: lib_System.Net.NetworkInformation.dll.so => 69
	i64 u0x2a6507a5ffabdf28, ; 197: System.Diagnostics.TraceSource.dll => 33
	i64 u0x2ad156c8e1354139, ; 198: fi/Microsoft.Maui.Controls.resources => 345
	i64 u0x2ad5d6b13b7a3e04, ; 199: System.ComponentModel.DataAnnotations.dll => 14
	i64 u0x2af298f63581d886, ; 200: System.Text.RegularExpressions.dll => 139
	i64 u0x2af615542f04da50, ; 201: System.IdentityModel.Tokens.Jwt.dll => 236
	i64 u0x2afc1c4f898552ee, ; 202: lib_System.Formats.Asn1.dll.so => 38
	i64 u0x2b148910ed40fbf9, ; 203: zh-Hant/Microsoft.Maui.Controls.resources.dll => 371
	i64 u0x2b4d4904cebfa4e9, ; 204: Microsoft.Extensions.FileSystemGlobbing => 195
	i64 u0x2b6989d78cba9a15, ; 205: Xamarin.AndroidX.Concurrent.Futures.dll => 263
	i64 u0x2b73dc6bb40edd58, ; 206: EPPlus.Interfaces.dll => 182
	i64 u0x2c8bd14bb93a7d82, ; 207: lib-pl-Microsoft.Maui.Controls.resources.dll.so => 358
	i64 u0x2cbd9262ca785540, ; 208: lib_System.Text.Encoding.CodePages.dll.so => 134
	i64 u0x2cc9e1fed6257257, ; 209: lib_System.Reflection.Emit.Lightweight.dll.so => 92
	i64 u0x2cd723e9fe623c7c, ; 210: lib_System.Private.Xml.Linq.dll.so => 88
	i64 u0x2cdbe1c1d4183ec1, ; 211: lib_Syncfusion.Licensing.dll.so => 231
	i64 u0x2d169d318a968379, ; 212: System.Threading.dll => 149
	i64 u0x2d1a116bc3e7586c, ; 213: Microsoft.Kiota.Serialization.Form.dll => 216
	i64 u0x2d47774b7d993f59, ; 214: sv/Microsoft.Maui.Controls.resources.dll => 364
	i64 u0x2d5ffcae1ad0aaca, ; 215: System.Data.dll => 24
	i64 u0x2db915caf23548d2, ; 216: System.Text.Json.dll => 138
	i64 u0x2dcaa0bb15a4117a, ; 217: System.IO.UnmanagedMemoryStream.dll => 57
	i64 u0x2ddc23ce366af58c, ; 218: Microsoft.Kiota.Serialization.Json.dll => 217
	i64 u0x2e5a40c319acb800, ; 219: System.IO.FileSystem => 51
	i64 u0x2e6f1f226821322a, ; 220: el/Microsoft.Maui.Controls.resources.dll => 343
	i64 u0x2f02f94df3200fe5, ; 221: System.Diagnostics.Process => 29
	i64 u0x2f2e98e1c89b1aff, ; 222: System.Xml.ReaderWriter => 157
	i64 u0x2f5911d9ba814e4e, ; 223: System.Diagnostics.Tracing => 34
	i64 u0x2f84070a459bc31f, ; 224: lib_System.Xml.dll.so => 164
	i64 u0x309ee9eeec09a71e, ; 225: lib_Xamarin.AndroidX.Fragment.dll.so => 278
	i64 u0x309f2bedefa9a318, ; 226: Microsoft.IdentityModel.Abstractions => 205
	i64 u0x30c6dda129408828, ; 227: System.IO.IsolatedStorage => 52
	i64 u0x31195fef5d8fb552, ; 228: _Microsoft.Android.Resource.Designer.dll => 376
	i64 u0x312c8ed623cbfc8d, ; 229: Xamarin.AndroidX.Window.dll => 316
	i64 u0x31496b779ed0663d, ; 230: lib_System.Reflection.DispatchProxy.dll.so => 90
	i64 u0x315f08d19390dc36, ; 231: Xamarin.Google.ErrorProne.TypeAnnotations => 323
	i64 u0x32243413e774362a, ; 232: Xamarin.AndroidX.CardView.dll => 259
	i64 u0x3235427f8d12dae1, ; 233: lib_System.Drawing.Primitives.dll.so => 35
	i64 u0x329753a17a517811, ; 234: fr/Microsoft.Maui.Controls.resources => 346
	i64 u0x32aa989ff07a84ff, ; 235: lib_System.Xml.ReaderWriter.dll.so => 157
	i64 u0x33642d5508314e46, ; 236: Microsoft.Extensions.FileSystemGlobbing.dll => 195
	i64 u0x33829542f112d59b, ; 237: System.Collections.Immutable => 9
	i64 u0x33a31443733849fe, ; 238: lib-es-Microsoft.Maui.Controls.resources.dll.so => 344
	i64 u0x341abc357fbb4ebf, ; 239: lib_System.Net.Sockets.dll.so => 76
	i64 u0x3496c1e2dcaf5ecc, ; 240: lib_System.IO.Pipes.AccessControl.dll.so => 55
	i64 u0x34dfd74fe2afcf37, ; 241: Microsoft.Maui => 222
	i64 u0x34e292762d9615df, ; 242: cs/Microsoft.Maui.Controls.resources.dll => 340
	i64 u0x34f847545107e6d0, ; 243: lib_Microsoft.Kiota.Serialization.Multipart.dll.so => 218
	i64 u0x3508234247f48404, ; 244: Microsoft.Maui.Controls => 220
	i64 u0x353590da528c9d22, ; 245: System.ComponentModel.Annotations => 13
	i64 u0x3549870798b4cd30, ; 246: lib_Xamarin.AndroidX.ViewPager2.dll.so => 315
	i64 u0x355282fc1c909694, ; 247: Microsoft.Extensions.Configuration => 187
	i64 u0x3552fc5d578f0fbf, ; 248: Xamarin.AndroidX.Arch.Core.Common => 252
	i64 u0x355c649948d55d97, ; 249: lib_System.Runtime.Intrinsics.dll.so => 109
	i64 u0x35ea9d1c6834bc8c, ; 250: Xamarin.AndroidX.Lifecycle.ViewModel.Ktx.dll => 293
	i64 u0x3628ab68db23a01a, ; 251: lib_System.Diagnostics.Tools.dll.so => 32
	i64 u0x3673b042508f5b6b, ; 252: lib_System.Runtime.Extensions.dll.so => 104
	i64 u0x36740f1a8ecdc6c4, ; 253: System.Numerics => 84
	i64 u0x36afeb96b7d720bc, ; 254: lib_Microsoft.Office.Interop.Excel.dll.so => 225
	i64 u0x36b2b50fdf589ae2, ; 255: System.Reflection.Emit.Lightweight => 92
	i64 u0x36cada77dc79928b, ; 256: System.IO.MemoryMappedFiles => 53
	i64 u0x374ef46b06791af6, ; 257: System.Reflection.Primitives.dll => 96
	i64 u0x376bf93e521a5417, ; 258: lib_Xamarin.Jetbrains.Annotations.dll.so => 325
	i64 u0x37bc29f3183003b6, ; 259: lib_System.IO.dll.so => 58
	i64 u0x380134e03b1e160a, ; 260: System.Collections.Immutable.dll => 9
	i64 u0x38049b5c59b39324, ; 261: System.Runtime.CompilerServices.Unsafe => 102
	i64 u0x385c17636bb6fe6e, ; 262: Xamarin.AndroidX.CustomView.dll => 271
	i64 u0x38869c811d74050e, ; 263: System.Net.NameResolution.dll => 68
	i64 u0x38e93ec1c057cdf6, ; 264: Microsoft.IdentityModel.Protocols => 208
	i64 u0x393c226616977fdb, ; 265: lib_Xamarin.AndroidX.ViewPager.dll.so => 314
	i64 u0x395e37c3334cf82a, ; 266: lib-ca-Microsoft.Maui.Controls.resources.dll.so => 339
	i64 u0x39c3107c28752af1, ; 267: lib_Microsoft.Extensions.FileProviders.Abstractions.dll.so => 193
	i64 u0x3a67fa982ce4abf0, ; 268: RBush => 227
	i64 u0x3a76a7a156f3d989, ; 269: System.IO.Packaging => 237
	i64 u0x3ab5859054645f72, ; 270: System.Security.Cryptography.Primitives.dll => 125
	i64 u0x3ad31bc4ddf45918, ; 271: ClosedXML.dll => 175
	i64 u0x3ad75090c3fac0e9, ; 272: lib_Xamarin.AndroidX.ResourceInspection.Annotation.dll.so => 302
	i64 u0x3ae44ac43a1fbdbb, ; 273: System.Runtime.Serialization => 116
	i64 u0x3b860f9932505633, ; 274: lib_System.Text.Encoding.Extensions.dll.so => 135
	i64 u0x3bea9ebe8c027c01, ; 275: lib_Microsoft.IdentityModel.Tokens.dll.so => 210
	i64 u0x3c3aafb6b3a00bf6, ; 276: lib_System.Security.Cryptography.X509Certificates.dll.so => 126
	i64 u0x3c4049146b59aa90, ; 277: System.Runtime.InteropServices.JavaScript => 106
	i64 u0x3c7c495f58ac5ee9, ; 278: Xamarin.Kotlin.StdLib => 327
	i64 u0x3c7e5ed3d5db71bb, ; 279: System.Security => 131
	i64 u0x3cd9d281d402eb9b, ; 280: Xamarin.AndroidX.Browser.dll => 254
	i64 u0x3ced6a4f3010aa96, ; 281: ZXing.Net.MAUI.Controls => 337
	i64 u0x3d1c50cc001a991e, ; 282: Xamarin.Google.Guava.ListenableFuture.dll => 324
	i64 u0x3d2b1913edfc08d7, ; 283: lib_System.Threading.ThreadPool.dll.so => 147
	i64 u0x3d46f0b995082740, ; 284: System.Xml.Linq => 156
	i64 u0x3d551d0efdd24596, ; 285: System.IO.Packaging.dll => 237
	i64 u0x3d8a8f400514a790, ; 286: Xamarin.AndroidX.Fragment.Ktx.dll => 279
	i64 u0x3d9c2a242b040a50, ; 287: lib_Xamarin.AndroidX.Core.dll.so => 267
	i64 u0x3db495de2204755c, ; 288: Microsoft.Extensions.Configuration.FileExtensions => 189
	i64 u0x3dbb6b9f5ab90fa7, ; 289: lib_Xamarin.AndroidX.DynamicAnimation.dll.so => 274
	i64 u0x3e5441657549b213, ; 290: Xamarin.AndroidX.ResourceInspection.Annotation => 302
	i64 u0x3e57d4d195c53c2e, ; 291: System.Reflection.TypeExtensions => 97
	i64 u0x3e616ab4ed1f3f15, ; 292: lib_System.Data.dll.so => 24
	i64 u0x3f1d226e6e06db7e, ; 293: Xamarin.AndroidX.SlidingPaneLayout.dll => 306
	i64 u0x3f510adf788828dd, ; 294: System.Threading.Tasks.Extensions => 143
	i64 u0x407a10bb4bf95829, ; 295: lib_Xamarin.AndroidX.Navigation.Common.dll.so => 296
	i64 u0x40c98b6bd77346d4, ; 296: Microsoft.VisualBasic.dll => 3
	i64 u0x41833cf766d27d96, ; 297: mscorlib => 167
	i64 u0x41cab042be111c34, ; 298: lib_Xamarin.AndroidX.AppCompat.AppCompatResources.dll.so => 251
	i64 u0x423a9ecc4d905a88, ; 299: lib_System.Resources.ResourceManager.dll.so => 100
	i64 u0x423bf51ae7def810, ; 300: System.Xml.XPath => 161
	i64 u0x42462ff15ddba223, ; 301: System.Resources.Reader.dll => 99
	i64 u0x4291015ff4e5ef71, ; 302: Xamarin.AndroidX.Core.ViewTree.dll => 269
	i64 u0x42a31b86e6ccc3f0, ; 303: System.Diagnostics.Contracts => 25
	i64 u0x430e95b891249788, ; 304: lib_System.Reflection.Emit.dll.so => 93
	i64 u0x43375950ec7c1b6a, ; 305: netstandard.dll => 168
	i64 u0x434c4e1d9284cdae, ; 306: Mono.Android.dll => 172
	i64 u0x43505013578652a0, ; 307: lib_Xamarin.AndroidX.Activity.Ktx.dll.so => 246
	i64 u0x437d06c381ed575a, ; 308: lib_Microsoft.VisualBasic.dll.so => 3
	i64 u0x43950f84de7cc79a, ; 309: pl/Microsoft.Maui.Controls.resources.dll => 358
	i64 u0x43e8ca5bc927ff37, ; 310: lib_Xamarin.AndroidX.Emoji2.ViewsHelper.dll.so => 276
	i64 u0x440c274c940f0550, ; 311: Microsoft.Graph.Core => 203
	i64 u0x448bd33429269b19, ; 312: Microsoft.CSharp => 1
	i64 u0x4499fa3c8e494654, ; 313: lib_System.Runtime.Serialization.Primitives.dll.so => 114
	i64 u0x4515080865a951a5, ; 314: Xamarin.Kotlin.StdLib.dll => 327
	i64 u0x4545802489b736b9, ; 315: Xamarin.AndroidX.Fragment.Ktx => 279
	i64 u0x454b4d1e66bb783c, ; 316: Xamarin.AndroidX.Lifecycle.Process => 286
	i64 u0x458d2df79ac57c1d, ; 317: lib_System.IdentityModel.Tokens.Jwt.dll.so => 236
	i64 u0x45c40276a42e283e, ; 318: System.Diagnostics.TraceSource => 33
	i64 u0x45d443f2a29adc37, ; 319: System.AppContext.dll => 6
	i64 u0x463d680a1dec0810, ; 320: System.Security.Cryptography.Xml.dll => 240
	i64 u0x46a4213bc97fe5ae, ; 321: lib-ru-Microsoft.Maui.Controls.resources.dll.so => 362
	i64 u0x47358bd471172e1d, ; 322: lib_System.Xml.Linq.dll.so => 156
	i64 u0x4787a936949fcac2, ; 323: System.Memory.Data.dll => 238
	i64 u0x47daf4e1afbada10, ; 324: pt/Microsoft.Maui.Controls.resources => 360
	i64 u0x480c0a47dd42dd81, ; 325: lib_System.IO.MemoryMappedFiles.dll.so => 53
	i64 u0x48e9c8e5d5e8555a, ; 326: DocumentFormat.OpenXml.dll => 179
	i64 u0x49e952f19a4e2022, ; 327: System.ObjectModel => 85
	i64 u0x49f9e6948a8131e4, ; 328: lib_Xamarin.AndroidX.VersionedParcelable.dll.so => 313
	i64 u0x4a5667b2462a664b, ; 329: lib_Xamarin.AndroidX.Navigation.UI.dll.so => 299
	i64 u0x4a7a18981dbd56bc, ; 330: System.IO.Compression.FileSystem.dll => 44
	i64 u0x4aa5c60350917c06, ; 331: lib_Xamarin.AndroidX.Lifecycle.LiveData.Core.Ktx.dll.so => 285
	i64 u0x4b07a0ed0ab33ff4, ; 332: System.Runtime.Extensions.dll => 104
	i64 u0x4b576d47ac054f3c, ; 333: System.IO.FileSystem.AccessControl => 47
	i64 u0x4b7b6532ded934b7, ; 334: System.Text.Json => 138
	i64 u0x4b8f8ea3c2df6bb0, ; 335: System.ClientModel => 233
	i64 u0x4c69a4a1b905a70e, ; 336: ClosedXML.Parser.dll => 176
	i64 u0x4c7755cf07ad2d5f, ; 337: System.Net.Http.Json.dll => 64
	i64 u0x4cc5f15266470798, ; 338: lib_Xamarin.AndroidX.Loader.dll.so => 295
	i64 u0x4cf6f67dc77aacd2, ; 339: System.Net.NetworkInformation.dll => 69
	i64 u0x4d3183dd245425d4, ; 340: System.Net.WebSockets.Client.dll => 80
	i64 u0x4d479f968a05e504, ; 341: System.Linq.Expressions.dll => 59
	i64 u0x4d55a010ffc4faff, ; 342: System.Private.Xml => 89
	i64 u0x4d5cbe77561c5b2e, ; 343: System.Web.dll => 154
	i64 u0x4d6001db23f8cd87, ; 344: lib_System.ClientModel.dll.so => 233
	i64 u0x4d77512dbd86ee4c, ; 345: lib_Xamarin.AndroidX.Arch.Core.Common.dll.so => 252
	i64 u0x4d7793536e79c309, ; 346: System.ServiceProcess => 133
	i64 u0x4d95fccc1f67c7ca, ; 347: System.Runtime.Loader.dll => 110
	i64 u0x4dcf44c3c9b076a2, ; 348: it/Microsoft.Maui.Controls.resources.dll => 352
	i64 u0x4dd9247f1d2c3235, ; 349: Xamarin.AndroidX.Loader.dll => 295
	i64 u0x4e2aeee78e2c4a87, ; 350: Xamarin.AndroidX.ProfileInstaller.ProfileInstaller => 300
	i64 u0x4e32f00cb0937401, ; 351: Mono.Android.Runtime => 171
	i64 u0x4e5eea4668ac2b18, ; 352: System.Text.Encoding.CodePages => 134
	i64 u0x4ebd0c4b82c5eefc, ; 353: lib_System.Threading.Channels.dll.so => 140
	i64 u0x4ee8eaa9c9c1151a, ; 354: System.Globalization.Calendars => 40
	i64 u0x4f21ee6ef9eb527e, ; 355: ca/Microsoft.Maui.Controls.resources => 339
	i64 u0x4f798ff775385060, ; 356: lib_Syncfusion.Pdf.Portable.dll.so => 232
	i64 u0x4ffd65baff757598, ; 357: Microsoft.IdentityModel.Tokens => 210
	i64 u0x500ae17e02316f13, ; 358: lib_Microsoft.Kiota.Authentication.Azure.dll.so => 214
	i64 u0x5037f0be3c28c7a3, ; 359: lib_Microsoft.Maui.Controls.dll.so => 220
	i64 u0x506203448c473a65, ; 360: Xamarin.Google.AutoValue.Annotations => 319
	i64 u0x50c3a29b21050d45, ; 361: System.Linq.Parallel.dll => 60
	i64 u0x5131bbe80989093f, ; 362: Xamarin.AndroidX.Lifecycle.ViewModel.Android.dll => 292
	i64 u0x516324a5050a7e3c, ; 363: System.Net.WebProxy => 79
	i64 u0x516d6f0b21a303de, ; 364: lib_System.Diagnostics.Contracts.dll.so => 25
	i64 u0x51bb8a2afe774e32, ; 365: System.Drawing => 36
	i64 u0x51f43453dd033104, ; 366: System.Private.Windows.Core => 235
	i64 u0x5247c5c32a4140f0, ; 367: System.Resources.Reader => 99
	i64 u0x526bb15e3c386364, ; 368: Xamarin.AndroidX.Lifecycle.Runtime.Ktx.dll => 289
	i64 u0x526ce79eb8e90527, ; 369: lib_System.Net.Primitives.dll.so => 71
	i64 u0x52829f00b4467c38, ; 370: lib_System.Data.Common.dll.so => 22
	i64 u0x529ffe06f39ab8db, ; 371: Xamarin.AndroidX.Core => 267
	i64 u0x52ff996554dbf352, ; 372: Microsoft.Maui.Graphics => 224
	i64 u0x535f7e40e8fef8af, ; 373: lib-sk-Microsoft.Maui.Controls.resources.dll.so => 363
	i64 u0x53978aac584c666e, ; 374: lib_System.Security.Cryptography.Cng.dll.so => 121
	i64 u0x53a96d5c86c9e194, ; 375: System.Net.NetworkInformation => 69
	i64 u0x53be1038a61e8d44, ; 376: System.Runtime.InteropServices.RuntimeInformation.dll => 107
	i64 u0x53c3014b9437e684, ; 377: lib-zh-HK-Microsoft.Maui.Controls.resources.dll.so => 369
	i64 u0x5435e6f049e9bc37, ; 378: System.Security.Claims.dll => 119
	i64 u0x54795225dd1587af, ; 379: lib_System.Runtime.dll.so => 117
	i64 u0x547a34f14e5f6210, ; 380: Xamarin.AndroidX.Lifecycle.Common.dll => 281
	i64 u0x556e8b63b660ab8b, ; 381: Xamarin.AndroidX.Lifecycle.Common.Jvm.dll => 282
	i64 u0x5588627c9a108ec9, ; 382: System.Collections.Specialized => 11
	i64 u0x55a898e4f42e3fae, ; 383: Microsoft.VisualBasic.Core.dll => 2
	i64 u0x55fa0c610fe93bb1, ; 384: lib_System.Security.Cryptography.OpenSsl.dll.so => 124
	i64 u0x56442b99bc64bb47, ; 385: System.Runtime.Serialization.Xml.dll => 115
	i64 u0x56a8b26e1aeae27b, ; 386: System.Threading.Tasks.Dataflow => 142
	i64 u0x56f932d61e93c07f, ; 387: System.Globalization.Extensions => 41
	i64 u0x571c5cfbec5ae8e2, ; 388: System.Private.Uri => 87
	i64 u0x576499c9f52fea31, ; 389: Xamarin.AndroidX.Annotation => 247
	i64 u0x579a06fed6eec900, ; 390: System.Private.CoreLib.dll => 173
	i64 u0x57c542c14049b66d, ; 391: System.Diagnostics.DiagnosticSource => 27
	i64 u0x581a8bd5cfda563e, ; 392: System.Threading.Timer => 148
	i64 u0x58601b2dda4a27b9, ; 393: lib-ja-Microsoft.Maui.Controls.resources.dll.so => 353
	i64 u0x58688d9af496b168, ; 394: Microsoft.Extensions.DependencyInjection.dll => 191
	i64 u0x588c167a79db6bfb, ; 395: lib_Xamarin.Google.ErrorProne.Annotations.dll.so => 322
	i64 u0x5906028ae5151104, ; 396: Xamarin.AndroidX.Activity.Ktx => 246
	i64 u0x595a356d23e8da9a, ; 397: lib_Microsoft.CSharp.dll.so => 1
	i64 u0x59f9e60b9475085f, ; 398: lib_Xamarin.AndroidX.Annotation.Experimental.dll.so => 248
	i64 u0x5a70033ca9d003cb, ; 399: lib_System.Memory.Data.dll.so => 238
	i64 u0x5a745f5101a75527, ; 400: lib_System.IO.Compression.FileSystem.dll.so => 44
	i64 u0x5a89a886ae30258d, ; 401: lib_Xamarin.AndroidX.CoordinatorLayout.dll.so => 266
	i64 u0x5a8f6699f4a1caa9, ; 402: lib_System.Threading.dll.so => 149
	i64 u0x5ae9cd33b15841bf, ; 403: System.ComponentModel => 18
	i64 u0x5b54391bdc6fcfe6, ; 404: System.Private.DataContractSerialization => 86
	i64 u0x5b5f0e240a06a2a2, ; 405: da/Microsoft.Maui.Controls.resources.dll => 341
	i64 u0x5b8109e8e14c5e3e, ; 406: System.Globalization.Extensions.dll => 41
	i64 u0x5bddd04d72a9e350, ; 407: Xamarin.AndroidX.Lifecycle.LiveData.Core.Ktx => 285
	i64 u0x5bdf16b09da116ab, ; 408: Xamarin.AndroidX.Collection => 260
	i64 u0x5c019d5266093159, ; 409: lib_Xamarin.AndroidX.Lifecycle.Runtime.Ktx.Android.dll.so => 290
	i64 u0x5c30a4a35f9cc8c4, ; 410: lib_System.Reflection.Extensions.dll.so => 94
	i64 u0x5c393624b8176517, ; 411: lib_Microsoft.Extensions.Logging.dll.so => 196
	i64 u0x5c53c29f5073b0c9, ; 412: System.Diagnostics.FileVersionInfo => 28
	i64 u0x5c87463c575c7616, ; 413: lib_System.Globalization.Extensions.dll.so => 41
	i64 u0x5d0a4a29b02d9d3c, ; 414: System.Net.WebHeaderCollection.dll => 78
	i64 u0x5d1b514fc45c92d4, ; 415: ZXing.Net.MAUI => 336
	i64 u0x5d40c9b15181641f, ; 416: lib_Xamarin.AndroidX.Emoji2.dll.so => 275
	i64 u0x5d5caf2d8be953e8, ; 417: Microsoft.Graph => 201
	i64 u0x5d6ca10d35e9485b, ; 418: lib_Xamarin.AndroidX.Concurrent.Futures.dll.so => 263
	i64 u0x5d7ec76c1c703055, ; 419: System.Threading.Tasks.Parallel => 144
	i64 u0x5db0cbbd1028510e, ; 420: lib_System.Runtime.InteropServices.dll.so => 108
	i64 u0x5db30905d3e5013b, ; 421: Xamarin.AndroidX.Collection.Jvm.dll => 261
	i64 u0x5e467bc8f09ad026, ; 422: System.Collections.Specialized.dll => 11
	i64 u0x5e5173b3208d97e7, ; 423: System.Runtime.Handles.dll => 105
	i64 u0x5ea92fdb19ec8c4c, ; 424: System.Text.Encodings.Web.dll => 137
	i64 u0x5eb8046dd40e9ac3, ; 425: System.ComponentModel.Primitives => 16
	i64 u0x5ec272d219c9aba4, ; 426: System.Security.Cryptography.Csp.dll => 122
	i64 u0x5eee1376d94c7f5e, ; 427: System.Net.HttpListener.dll => 66
	i64 u0x5f36ccf5c6a57e24, ; 428: System.Xml.ReaderWriter.dll => 157
	i64 u0x5f4294b9b63cb842, ; 429: System.Data.Common => 22
	i64 u0x5f9a2d823f664957, ; 430: lib-el-Microsoft.Maui.Controls.resources.dll.so => 343
	i64 u0x5fa6da9c3cd8142a, ; 431: lib_Xamarin.KotlinX.Serialization.Core.dll.so => 333
	i64 u0x5fac98e0b37a5b9d, ; 432: System.Runtime.CompilerServices.Unsafe.dll => 102
	i64 u0x609f4b7b63d802d4, ; 433: lib_Microsoft.Extensions.DependencyInjection.dll.so => 191
	i64 u0x60cd4e33d7e60134, ; 434: Xamarin.KotlinX.Coroutines.Core.Jvm => 332
	i64 u0x60f62d786afcf130, ; 435: System.Memory => 63
	i64 u0x61a3b9f0f15a3269, ; 436: lib_SixLabors.Fonts.dll.so => 228
	i64 u0x61bb78c89f867353, ; 437: System.IO => 58
	i64 u0x61be8d1299194243, ; 438: Microsoft.Maui.Controls.Xaml => 221
	i64 u0x61d2cba29557038f, ; 439: de/Microsoft.Maui.Controls.resources => 342
	i64 u0x61d88f399afb2f45, ; 440: lib_System.Runtime.Loader.dll.so => 110
	i64 u0x622eef6f9e59068d, ; 441: System.Private.CoreLib => 173
	i64 u0x6259a2b81531f5de, ; 442: Microsoft.Kiota.Abstractions => 213
	i64 u0x63cdbd66ac39bb46, ; 443: lib_Microsoft.VisualStudio.DesignTools.XamlTapContract.dll.so => 375
	i64 u0x63d5e3aa4ef9b931, ; 444: Xamarin.KotlinX.Coroutines.Android.dll => 330
	i64 u0x63f1f6883c1e23c2, ; 445: lib_System.Collections.Immutable.dll.so => 9
	i64 u0x6400f68068c1e9f1, ; 446: Xamarin.Google.Android.Material.dll => 318
	i64 u0x640e3b14dbd325c2, ; 447: System.Security.Cryptography.Algorithms.dll => 120
	i64 u0x64587004560099b9, ; 448: System.Reflection => 98
	i64 u0x647b8d50058e8d26, ; 449: Microsoft.Kiota.Authentication.Azure.dll => 214
	i64 u0x64b1529a438a3c45, ; 450: lib_System.Runtime.Handles.dll.so => 105
	i64 u0x6525e13597f85586, ; 451: Microsoft.Kiota.Serialization.Form => 216
	i64 u0x6565fba2cd8f235b, ; 452: Xamarin.AndroidX.Lifecycle.ViewModel.Ktx => 293
	i64 u0x658f524e4aba7dad, ; 453: CommunityToolkit.Maui.dll => 177
	i64 u0x65ecac39144dd3cc, ; 454: Microsoft.Maui.Controls.dll => 220
	i64 u0x65ece51227bfa724, ; 455: lib_System.Runtime.Numerics.dll.so => 111
	i64 u0x661722438787b57f, ; 456: Xamarin.AndroidX.Annotation.Jvm.dll => 249
	i64 u0x6668e5c50e448662, ; 457: EPPlus => 181
	i64 u0x6679b2337ee6b22a, ; 458: lib_System.IO.FileSystem.Primitives.dll.so => 49
	i64 u0x6692e924eade1b29, ; 459: lib_System.Console.dll.so => 20
	i64 u0x66a4e5c6a3fb0bae, ; 460: lib_Xamarin.AndroidX.Lifecycle.ViewModel.Android.dll.so => 292
	i64 u0x66ad21286ac74b9d, ; 461: lib_System.Drawing.Common.dll.so => 234
	i64 u0x66d13304ce1a3efa, ; 462: Xamarin.AndroidX.CursorAdapter => 270
	i64 u0x674303f65d8fad6f, ; 463: lib_System.Net.Quic.dll.so => 72
	i64 u0x6756ca4cad62e9d6, ; 464: lib_Xamarin.AndroidX.ConstraintLayout.Core.dll.so => 265
	i64 u0x67c0802770244408, ; 465: System.Windows.dll => 155
	i64 u0x68100b69286e27cd, ; 466: lib_System.Formats.Tar.dll.so => 39
	i64 u0x68558ec653afa616, ; 467: lib-da-Microsoft.Maui.Controls.resources.dll.so => 341
	i64 u0x6872ec7a2e36b1ac, ; 468: System.Drawing.Primitives.dll => 35
	i64 u0x68bb2c417aa9b61c, ; 469: Xamarin.KotlinX.AtomicFU.dll => 328
	i64 u0x68fbbbe2eb455198, ; 470: System.Formats.Asn1 => 38
	i64 u0x69063fc0ba8e6bdd, ; 471: he/Microsoft.Maui.Controls.resources.dll => 347
	i64 u0x69a3e26c76f6eec4, ; 472: Xamarin.AndroidX.Window.Extensions.Core.Core.dll => 317
	i64 u0x6a4d7577b2317255, ; 473: System.Runtime.InteropServices.dll => 108
	i64 u0x6ace3b74b15ee4a4, ; 474: nb/Microsoft.Maui.Controls.resources => 356
	i64 u0x6afcedb171067e2b, ; 475: System.Core.dll => 21
	i64 u0x6bef98e124147c24, ; 476: Xamarin.Jetbrains.Annotations => 325
	i64 u0x6ce874bff138ce2b, ; 477: Xamarin.AndroidX.Lifecycle.ViewModel.dll => 291
	i64 u0x6d12bfaa99c72b1f, ; 478: lib_Microsoft.Maui.Graphics.dll.so => 224
	i64 u0x6d6f065f514b3a86, ; 479: Syncfusion.Compression.Portable.dll => 230
	i64 u0x6d70755158ca866e, ; 480: lib_System.ComponentModel.EventBasedAsync.dll.so => 15
	i64 u0x6d79993361e10ef2, ; 481: Microsoft.Extensions.Primitives => 200
	i64 u0x6d7eeca99577fc8b, ; 482: lib_System.Net.WebProxy.dll.so => 79
	i64 u0x6d8515b19946b6a2, ; 483: System.Net.WebProxy.dll => 79
	i64 u0x6d86d56b84c8eb71, ; 484: lib_Xamarin.AndroidX.CursorAdapter.dll.so => 270
	i64 u0x6d9bea6b3e895cf7, ; 485: Microsoft.Extensions.Primitives.dll => 200
	i64 u0x6e25a02c3833319a, ; 486: lib_Xamarin.AndroidX.Navigation.Fragment.dll.so => 297
	i64 u0x6e6be4a99c3561a0, ; 487: Syncfusion.Compression.Portable => 230
	i64 u0x6e79c6bd8627412a, ; 488: Xamarin.AndroidX.SavedState.SavedState.Ktx => 304
	i64 u0x6e838d9a2a6f6c9e, ; 489: lib_System.ValueTuple.dll.so => 152
	i64 u0x6e9965ce1095e60a, ; 490: lib_System.Core.dll.so => 21
	i64 u0x6fd2265da78b93a4, ; 491: lib_Microsoft.Maui.dll.so => 222
	i64 u0x6fdfc7de82c33008, ; 492: cs/Microsoft.Maui.Controls.resources => 340
	i64 u0x6ffc4967cc47ba57, ; 493: System.IO.FileSystem.Watcher.dll => 50
	i64 u0x701cd46a1c25a5fe, ; 494: System.IO.FileSystem.dll => 51
	i64 u0x70e99f48c05cb921, ; 495: tr/Microsoft.Maui.Controls.resources.dll => 366
	i64 u0x70fd3deda22442d2, ; 496: lib-nb-Microsoft.Maui.Controls.resources.dll.so => 356
	i64 u0x71485e7ffdb4b958, ; 497: System.Reflection.Extensions => 94
	i64 u0x7162a2fce67a945f, ; 498: lib_Xamarin.Android.Glide.Annotations.dll.so => 242
	i64 u0x71a495ea3761dde8, ; 499: lib-it-Microsoft.Maui.Controls.resources.dll.so => 352
	i64 u0x71ad672adbe48f35, ; 500: System.ComponentModel.Primitives.dll => 16
	i64 u0x71bc142d620e986a, ; 501: lib_System.Security.Cryptography.Pkcs.dll.so => 239
	i64 u0x720f102581a4a5c8, ; 502: Xamarin.AndroidX.Core.ViewTree => 269
	i64 u0x725f5a9e82a45c81, ; 503: System.Security.Cryptography.Encoding => 123
	i64 u0x72b1fb4109e08d7b, ; 504: lib-hr-Microsoft.Maui.Controls.resources.dll.so => 349
	i64 u0x72e0300099accce1, ; 505: System.Xml.XPath.XDocument => 160
	i64 u0x730bfb248998f67a, ; 506: System.IO.Compression.ZipFile => 45
	i64 u0x732b2d67b9e5c47b, ; 507: Xamarin.Google.ErrorProne.Annotations.dll => 322
	i64 u0x734b76fdc0dc05bb, ; 508: lib_GoogleGson.dll.so => 185
	i64 u0x73a2b85f84dcec96, ; 509: lib_DocumentFormat.OpenXml.dll.so => 179
	i64 u0x73a6be34e822f9d1, ; 510: lib_System.Runtime.Serialization.dll.so => 116
	i64 u0x73e4ce94e2eb6ffc, ; 511: lib_System.Memory.dll.so => 63
	i64 u0x743a1eccf080489a, ; 512: WindowsBase.dll => 166
	i64 u0x755a91767330b3d4, ; 513: lib_Microsoft.Extensions.Configuration.dll.so => 187
	i64 u0x75c326eb821b85c4, ; 514: lib_System.ComponentModel.DataAnnotations.dll.so => 14
	i64 u0x75f59536ad2b55b1, ; 515: SixLabors.Fonts => 228
	i64 u0x76012e7334db86e5, ; 516: lib_Xamarin.AndroidX.SavedState.dll.so => 303
	i64 u0x76ca07b878f44da0, ; 517: System.Runtime.Numerics.dll => 111
	i64 u0x7736c8a96e51a061, ; 518: lib_Xamarin.AndroidX.Annotation.Jvm.dll.so => 249
	i64 u0x77564dc3bfb31c3f, ; 519: Std.UriTemplate.dll => 229
	i64 u0x778a805e625329ef, ; 520: System.Linq.Parallel => 60
	i64 u0x779290cc2b801eb7, ; 521: Xamarin.KotlinX.AtomicFU.Jvm => 329
	i64 u0x779f67ad3b8efbd5, ; 522: Microsoft.Extensions.Configuration.Json.dll => 190
	i64 u0x77bf40592cd67602, ; 523: Xamarin.Google.AutoValue.Annotations.dll => 319
	i64 u0x77cba97b3c0d590e, ; 524: Microsoft.Office.Interop.Excel => 225
	i64 u0x77f8a4acc2fdc449, ; 525: System.Security.Cryptography.Cng.dll => 121
	i64 u0x780bc73597a503a9, ; 526: lib-ms-Microsoft.Maui.Controls.resources.dll.so => 355
	i64 u0x782c5d8eb99ff201, ; 527: lib_Microsoft.VisualBasic.Core.dll.so => 2
	i64 u0x783606d1e53e7a1a, ; 528: th/Microsoft.Maui.Controls.resources.dll => 365
	i64 u0x78a45e51311409b6, ; 529: Xamarin.AndroidX.Fragment.dll => 278
	i64 u0x78ed4ab8f9d800a1, ; 530: Xamarin.AndroidX.Lifecycle.ViewModel => 291
	i64 u0x793914ac7e9dd4f3, ; 531: MobileScanner => 0
	i64 u0x79f2a1023f4320f2, ; 532: Microsoft.Win32.SystemEvents => 226
	i64 u0x7a316882bd085c35, ; 533: ExcelNumberFormat.dll => 184
	i64 u0x7a39601d6f0bb831, ; 534: lib_Xamarin.KotlinX.AtomicFU.dll.so => 328
	i64 u0x7a5207a7c82d30b4, ; 535: lib_Xamarin.JSpecify.dll.so => 326
	i64 u0x7a7e7eddf79c5d26, ; 536: lib_Xamarin.AndroidX.Lifecycle.ViewModel.dll.so => 291
	i64 u0x7a9a57d43b0845fa, ; 537: System.AppContext => 6
	i64 u0x7ad0f4f1e5d08183, ; 538: Xamarin.AndroidX.Collection.dll => 260
	i64 u0x7adb8da2ac89b647, ; 539: fi/Microsoft.Maui.Controls.resources.dll => 345
	i64 u0x7b13d9eaa944ade8, ; 540: Xamarin.AndroidX.DynamicAnimation.dll => 274
	i64 u0x7b2641c52a771341, ; 541: lib_Microsoft.Graph.Core.dll.so => 203
	i64 u0x7b428dbcccbfb39c, ; 542: Microsoft.IdentityModel.Validators.dll => 211
	i64 u0x7b4927e421291c41, ; 543: Microsoft.IdentityModel.JsonWebTokens.dll => 206
	i64 u0x7bef86a4335c4870, ; 544: System.ComponentModel.TypeConverter => 17
	i64 u0x7c0820144cd34d6a, ; 545: sk/Microsoft.Maui.Controls.resources.dll => 363
	i64 u0x7c2a0bd1e0f988fc, ; 546: lib-de-Microsoft.Maui.Controls.resources.dll.so => 342
	i64 u0x7c41d387501568ba, ; 547: System.Net.WebClient.dll => 77
	i64 u0x7c482cd79bd24b13, ; 548: lib_Xamarin.AndroidX.ConstraintLayout.dll.so => 264
	i64 u0x7c7a2ef29cf6daf4, ; 549: Microsoft.IdentityModel.Validators => 211
	i64 u0x7c8cb8cf04bee12b, ; 550: lib_Xamarin.Google.AutoValue.Annotations.dll.so => 319
	i64 u0x7cc637f941f716d0, ; 551: CommunityToolkit.Maui.Core => 178
	i64 u0x7cc97975275cce3c, ; 552: Microsoft.Kiota.Http.HttpClientLibrary => 215
	i64 u0x7cd2ec8eaf5241cd, ; 553: System.Security.dll => 131
	i64 u0x7cf9ae50dd350622, ; 554: Xamarin.Jetbrains.Annotations.dll => 325
	i64 u0x7d649b75d580bb42, ; 555: ms/Microsoft.Maui.Controls.resources.dll => 355
	i64 u0x7d8ee2bdc8e3aad1, ; 556: System.Numerics.Vectors => 83
	i64 u0x7df5df8db8eaa6ac, ; 557: Microsoft.Extensions.Logging.Debug => 198
	i64 u0x7dfc3d6d9d8d7b70, ; 558: System.Collections => 12
	i64 u0x7e2e564fa2f76c65, ; 559: lib_System.Diagnostics.Tracing.dll.so => 34
	i64 u0x7e302e110e1e1346, ; 560: lib_System.Security.Claims.dll.so => 119
	i64 u0x7e4084a672f9c30e, ; 561: lib_System.Security.Cryptography.Xml.dll.so => 240
	i64 u0x7e4465b3f78ad8d0, ; 562: Xamarin.KotlinX.Serialization.Core.dll => 333
	i64 u0x7e571cad5915e6c3, ; 563: lib_Xamarin.AndroidX.Lifecycle.Process.dll.so => 286
	i64 u0x7e6b1ca712437d7d, ; 564: Xamarin.AndroidX.Emoji2.ViewsHelper => 276
	i64 u0x7e946809d6008ef2, ; 565: lib_System.ObjectModel.dll.so => 85
	i64 u0x7ea0272c1b4a9635, ; 566: lib_Xamarin.Android.Glide.dll.so => 241
	i64 u0x7ecc13347c8fd849, ; 567: lib_System.ComponentModel.dll.so => 18
	i64 u0x7f00ddd9b9ca5a13, ; 568: Xamarin.AndroidX.ViewPager.dll => 314
	i64 u0x7f9351cd44b1273f, ; 569: Microsoft.Extensions.Configuration.Abstractions => 188
	i64 u0x7fae0ef4dc4770fe, ; 570: Microsoft.Identity.Client => 204
	i64 u0x7fbd557c99b3ce6f, ; 571: lib_Xamarin.AndroidX.Lifecycle.LiveData.Core.dll.so => 284
	i64 u0x8052dc0289c3c90a, ; 572: lib_ClosedXML.dll.so => 175
	i64 u0x8076a9a44a2ca331, ; 573: System.Net.Quic => 72
	i64 u0x80b7e726b0280681, ; 574: Microsoft.VisualStudio.DesignTools.MobileTapContracts => 373
	i64 u0x80da183a87731838, ; 575: System.Reflection.Metadata => 95
	i64 u0x812c069d5cdecc17, ; 576: System.dll => 165
	i64 u0x81381be520a60adb, ; 577: Xamarin.AndroidX.Interpolator.dll => 280
	i64 u0x81657cec2b31e8aa, ; 578: System.Net => 82
	i64 u0x81ab745f6c0f5ce6, ; 579: zh-Hant/Microsoft.Maui.Controls.resources => 371
	i64 u0x8277f2be6b5ce05f, ; 580: Xamarin.AndroidX.AppCompat => 250
	i64 u0x828f06563b30bc50, ; 581: lib_Xamarin.AndroidX.CardView.dll.so => 259
	i64 u0x82920a8d9194a019, ; 582: Xamarin.KotlinX.AtomicFU.Jvm.dll => 329
	i64 u0x82b399cb01b531c4, ; 583: lib_System.Web.dll.so => 154
	i64 u0x82df8f5532a10c59, ; 584: lib_System.Drawing.dll.so => 36
	i64 u0x82f0b6e911d13535, ; 585: lib_System.Transactions.dll.so => 151
	i64 u0x82f6403342e12049, ; 586: uk/Microsoft.Maui.Controls.resources => 367
	i64 u0x83a7afd2c49adc86, ; 587: lib_Microsoft.IdentityModel.Abstractions.dll.so => 205
	i64 u0x83c14ba66c8e2b8c, ; 588: zh-Hans/Microsoft.Maui.Controls.resources => 370
	i64 u0x844ac8f64fd78edc, ; 589: Xamarin.AndroidX.Camera.View.dll => 258
	i64 u0x846ce984efea52c7, ; 590: System.Threading.Tasks.Parallel.dll => 144
	i64 u0x8478602014b59199, ; 591: lib_EPPlus.System.Drawing.dll.so => 183
	i64 u0x84ae73148a4557d2, ; 592: lib_System.IO.Pipes.dll.so => 56
	i64 u0x84b01102c12a9232, ; 593: System.Runtime.Serialization.Json.dll => 113
	i64 u0x850c5ba0b57ce8e7, ; 594: lib_Xamarin.AndroidX.Collection.dll.so => 260
	i64 u0x851d02edd334b044, ; 595: Xamarin.AndroidX.VectorDrawable => 311
	i64 u0x85c919db62150978, ; 596: Xamarin.AndroidX.Transition.dll => 310
	i64 u0x8662aaeb94fef37f, ; 597: lib_System.Dynamic.Runtime.dll.so => 37
	i64 u0x86a909228dc7657b, ; 598: lib-zh-Hant-Microsoft.Maui.Controls.resources.dll.so => 371
	i64 u0x86b3e00c36b84509, ; 599: Microsoft.Extensions.Configuration.dll => 187
	i64 u0x86b62cb077ec4fd7, ; 600: System.Runtime.Serialization.Xml => 115
	i64 u0x8704193f462e892e, ; 601: lib_Microsoft.Extensions.FileSystemGlobbing.dll.so => 195
	i64 u0x8706ffb12bf3f53d, ; 602: Xamarin.AndroidX.Annotation.Experimental => 248
	i64 u0x872a5b14c18d328c, ; 603: System.ComponentModel.DataAnnotations => 14
	i64 u0x872fb9615bc2dff0, ; 604: Xamarin.Android.Glide.Annotations.dll => 242
	i64 u0x87c69b87d9283884, ; 605: lib_System.Threading.Thread.dll.so => 146
	i64 u0x87f6569b25707834, ; 606: System.IO.Compression.Brotli.dll => 43
	i64 u0x8842b3a5d2d3fb36, ; 607: Microsoft.Maui.Essentials => 223
	i64 u0x88926583efe7ee86, ; 608: Xamarin.AndroidX.Activity.Ktx.dll => 246
	i64 u0x88ba6bc4f7762b03, ; 609: lib_System.Reflection.dll.so => 98
	i64 u0x88bda98e0cffb7a9, ; 610: lib_Xamarin.KotlinX.Coroutines.Core.Jvm.dll.so => 332
	i64 u0x8930322c7bd8f768, ; 611: netstandard => 168
	i64 u0x897a606c9e39c75f, ; 612: lib_System.ComponentModel.Primitives.dll.so => 16
	i64 u0x89911a22005b92b7, ; 613: System.IO.FileSystem.DriveInfo.dll => 48
	i64 u0x89c5188089ec2cd5, ; 614: lib_System.Runtime.InteropServices.RuntimeInformation.dll.so => 107
	i64 u0x8a19e3dc71b34b2c, ; 615: System.Reflection.TypeExtensions.dll => 97
	i64 u0x8ac8d025b93e29e9, ; 616: Syncfusion.Licensing => 231
	i64 u0x8ad229ea26432ee2, ; 617: Xamarin.AndroidX.Loader => 295
	i64 u0x8b4ff5d0fdd5faa1, ; 618: lib_System.Diagnostics.DiagnosticSource.dll.so => 27
	i64 u0x8b541d476eb3774c, ; 619: System.Security.Principal.Windows => 128
	i64 u0x8b8d01333a96d0b5, ; 620: System.Diagnostics.Process.dll => 29
	i64 u0x8b9ceca7acae3451, ; 621: lib-he-Microsoft.Maui.Controls.resources.dll.so => 347
	i64 u0x8ba96f31f69ece34, ; 622: Microsoft.Win32.SystemEvents.dll => 226
	i64 u0x8c53ae18581b14f0, ; 623: Azure.Core => 174
	i64 u0x8c575135aa1ccef4, ; 624: Microsoft.Extensions.FileProviders.Abstractions => 193
	i64 u0x8cb8f612b633affb, ; 625: Xamarin.AndroidX.SavedState.SavedState.Ktx.dll => 304
	i64 u0x8cdfdb4ce85fb925, ; 626: lib_System.Security.Principal.Windows.dll.so => 128
	i64 u0x8cdfe7b8f4caa426, ; 627: System.IO.Compression.FileSystem => 44
	i64 u0x8d0f420977c2c1c7, ; 628: Xamarin.AndroidX.CursorAdapter.dll => 270
	i64 u0x8d4090b147c3167c, ; 629: lib_Microsoft.Kiota.Serialization.Form.dll.so => 216
	i64 u0x8d52f7ea2796c531, ; 630: Xamarin.AndroidX.Emoji2.dll => 275
	i64 u0x8d7b8ab4b3310ead, ; 631: System.Threading => 149
	i64 u0x8da188285aadfe8e, ; 632: System.Collections.Concurrent => 8
	i64 u0x8e10aa836d236cb3, ; 633: RBush.dll => 227
	i64 u0x8e40b785660ff661, ; 634: lib_Microsoft.Graph.Auth.dll.so => 202
	i64 u0x8e937db395a74375, ; 635: lib_Microsoft.Identity.Client.dll.so => 204
	i64 u0x8ed807bfe9858dfc, ; 636: Xamarin.AndroidX.Navigation.Common => 296
	i64 u0x8ee08b8194a30f48, ; 637: lib-hi-Microsoft.Maui.Controls.resources.dll.so => 348
	i64 u0x8ef7601039857a44, ; 638: lib-ro-Microsoft.Maui.Controls.resources.dll.so => 361
	i64 u0x8f32c6f611f6ffab, ; 639: pt/Microsoft.Maui.Controls.resources.dll => 360
	i64 u0x8f44b45eb046bbd1, ; 640: System.ServiceModel.Web.dll => 132
	i64 u0x8f8829d21c8985a4, ; 641: lib-pt-BR-Microsoft.Maui.Controls.resources.dll.so => 359
	i64 u0x8fbf5b0114c6dcef, ; 642: System.Globalization.dll => 42
	i64 u0x8fcc8c2a81f3d9e7, ; 643: Xamarin.KotlinX.Serialization.Core => 333
	i64 u0x90263f8448b8f572, ; 644: lib_System.Diagnostics.TraceSource.dll.so => 33
	i64 u0x903101b46fb73a04, ; 645: _Microsoft.Android.Resource.Designer => 376
	i64 u0x90393bd4865292f3, ; 646: lib_System.IO.Compression.dll.so => 46
	i64 u0x905e2b8e7ae91ae6, ; 647: System.Threading.Tasks.Extensions.dll => 143
	i64 u0x90634f86c5ebe2b5, ; 648: Xamarin.AndroidX.Lifecycle.ViewModel.Android => 292
	i64 u0x907b636704ad79ef, ; 649: lib_Microsoft.Maui.Controls.Xaml.dll.so => 221
	i64 u0x90e9efbfd68593e0, ; 650: lib_Xamarin.AndroidX.Lifecycle.LiveData.dll.so => 283
	i64 u0x91418dc638b29e68, ; 651: lib_Xamarin.AndroidX.CustomView.dll.so => 271
	i64 u0x914647982e998267, ; 652: Microsoft.Extensions.Configuration.Json => 190
	i64 u0x9157bd523cd7ed36, ; 653: lib_System.Text.Json.dll.so => 138
	i64 u0x91a74f07b30d37e2, ; 654: System.Linq.dll => 62
	i64 u0x91cb86ea3b17111d, ; 655: System.ServiceModel.Web => 132
	i64 u0x91fa41a87223399f, ; 656: ca/Microsoft.Maui.Controls.resources.dll => 339
	i64 u0x92054e486c0c7ea7, ; 657: System.IO.FileSystem.DriveInfo => 48
	i64 u0x928614058c40c4cd, ; 658: lib_System.Xml.XPath.XDocument.dll.so => 160
	i64 u0x92b138fffca2b01e, ; 659: lib_Xamarin.AndroidX.Arch.Core.Runtime.dll.so => 253
	i64 u0x92dfc2bfc6c6a888, ; 660: Xamarin.AndroidX.Lifecycle.LiveData => 283
	i64 u0x933da2c779423d68, ; 661: Xamarin.Android.Glide.Annotations => 242
	i64 u0x9388aad9b7ae40ce, ; 662: lib_Xamarin.AndroidX.Lifecycle.Common.dll.so => 281
	i64 u0x93cfa73ab28d6e35, ; 663: ms/Microsoft.Maui.Controls.resources => 355
	i64 u0x941c00d21e5c0679, ; 664: lib_Xamarin.AndroidX.Transition.dll.so => 310
	i64 u0x944077d8ca3c6580, ; 665: System.IO.Compression.dll => 46
	i64 u0x948cffedc8ed7960, ; 666: System.Xml => 164
	i64 u0x948d746a7702861f, ; 667: Microsoft.IdentityModel.Logging.dll => 207
	i64 u0x94c8990839c4bdb1, ; 668: lib_Xamarin.AndroidX.Interpolator.dll.so => 280
	i64 u0x9502fd818eed2359, ; 669: lib_Microsoft.IdentityModel.Protocols.OpenIdConnect.dll.so => 209
	i64 u0x9564283c37ed59a9, ; 670: lib_Microsoft.IdentityModel.Logging.dll.so => 207
	i64 u0x95c6b36f5f5d7039, ; 671: Xamarin.AndroidX.Camera.Camera2 => 255
	i64 u0x95d757769563d0d3, ; 672: Xamarin.AndroidX.Camera.Lifecycle.dll => 257
	i64 u0x9656a5a4ef359a71, ; 673: Microsoft.Graph.Auth => 202
	i64 u0x967fc325e09bfa8c, ; 674: es/Microsoft.Maui.Controls.resources => 344
	i64 u0x9686161486d34b81, ; 675: lib_Xamarin.AndroidX.ExifInterface.dll.so => 277
	i64 u0x971adf65d74c2825, ; 676: Microsoft.Kiota.Authentication.Azure => 214
	i64 u0x9732d8dbddea3d9a, ; 677: id/Microsoft.Maui.Controls.resources => 351
	i64 u0x978be80e5210d31b, ; 678: Microsoft.Maui.Graphics.dll => 224
	i64 u0x97b8c771ea3e4220, ; 679: System.ComponentModel.dll => 18
	i64 u0x97e144c9d3c6976e, ; 680: System.Collections.Concurrent.dll => 8
	i64 u0x984184e3c70d4419, ; 681: GoogleGson => 185
	i64 u0x9843944103683dd3, ; 682: Xamarin.AndroidX.Core.Core.Ktx => 268
	i64 u0x98d720cc4597562c, ; 683: System.Security.Cryptography.OpenSsl => 124
	i64 u0x99052c1297204af4, ; 684: lib_Xamarin.AndroidX.Camera.Core.dll.so => 256
	i64 u0x991d510397f92d9d, ; 685: System.Linq.Expressions => 59
	i64 u0x996ceeb8a3da3d67, ; 686: System.Threading.Overlapped.dll => 141
	i64 u0x99a00ca5270c6878, ; 687: Xamarin.AndroidX.Navigation.Runtime => 298
	i64 u0x99cdc6d1f2d3a72f, ; 688: ko/Microsoft.Maui.Controls.resources.dll => 354
	i64 u0x9a01b1da98b6ee10, ; 689: Xamarin.AndroidX.Lifecycle.Runtime.dll => 287
	i64 u0x9a0cc42c6f36dfc9, ; 690: lib_Microsoft.IdentityModel.Protocols.dll.so => 208
	i64 u0x9a5ccc274fd6e6ee, ; 691: Jsr305Binding.dll => 320
	i64 u0x9a816d9654deff7c, ; 692: Microsoft.IO.RecyclableMemoryStream => 212
	i64 u0x9ae6940b11c02876, ; 693: lib_Xamarin.AndroidX.Window.dll.so => 316
	i64 u0x9b211a749105beac, ; 694: System.Transactions.Local => 150
	i64 u0x9b8734714671022d, ; 695: System.Threading.Tasks.Dataflow.dll => 142
	i64 u0x9bc6aea27fbf034f, ; 696: lib_Xamarin.KotlinX.Coroutines.Core.dll.so => 331
	i64 u0x9bd8cc74558ad4c7, ; 697: Xamarin.KotlinX.AtomicFU => 328
	i64 u0x9c244ac7cda32d26, ; 698: System.Security.Cryptography.X509Certificates.dll => 126
	i64 u0x9c465f280cf43733, ; 699: lib_Xamarin.KotlinX.Coroutines.Android.dll.so => 330
	i64 u0x9c8f6872beab6408, ; 700: System.Xml.XPath.XDocument.dll => 160
	i64 u0x9ce01cf91101ae23, ; 701: System.Xml.XmlDocument => 162
	i64 u0x9d128180c81d7ce6, ; 702: Xamarin.AndroidX.CustomView.PoolingContainer => 272
	i64 u0x9d5dbcf5a48583fe, ; 703: lib_Xamarin.AndroidX.Activity.dll.so => 245
	i64 u0x9d74dee1a7725f34, ; 704: Microsoft.Extensions.Configuration.Abstractions.dll => 188
	i64 u0x9e4534b6adaf6e84, ; 705: nl/Microsoft.Maui.Controls.resources => 357
	i64 u0x9e4b95dec42769f7, ; 706: System.Diagnostics.Debug.dll => 26
	i64 u0x9eaf1efdf6f7267e, ; 707: Xamarin.AndroidX.Navigation.Common.dll => 296
	i64 u0x9ef542cf1f78c506, ; 708: Xamarin.AndroidX.Lifecycle.LiveData.Core => 284
	i64 u0x9fbb2961ca18e5c2, ; 709: Microsoft.Extensions.FileProviders.Physical.dll => 194
	i64 u0x9ff334e3cf272fd6, ; 710: lib_Xamarin.AndroidX.Camera.Lifecycle.dll.so => 257
	i64 u0x9ffbb6b1434ad2df, ; 711: Microsoft.Identity.Client.dll => 204
	i64 u0xa00832eb975f56a8, ; 712: lib_System.Net.dll.so => 82
	i64 u0xa073c238e883b3ab, ; 713: Microsoft.Graph.dll => 201
	i64 u0xa0ad78236b7b267f, ; 714: Xamarin.AndroidX.Window => 316
	i64 u0xa0d8259f4cc284ec, ; 715: lib_System.Security.Cryptography.dll.so => 127
	i64 u0xa0e17ca50c77a225, ; 716: lib_Xamarin.Google.Crypto.Tink.Android.dll.so => 321
	i64 u0xa0ff9b3e34d92f11, ; 717: lib_System.Resources.Writer.dll.so => 101
	i64 u0xa12fbfb4da97d9f3, ; 718: System.Threading.Timer.dll => 148
	i64 u0xa1440773ee9d341e, ; 719: Xamarin.Google.Android.Material => 318
	i64 u0xa1b9d7c27f47219f, ; 720: Xamarin.AndroidX.Navigation.UI.dll => 299
	i64 u0xa2572680829d2c7c, ; 721: System.IO.Pipelines.dll => 54
	i64 u0xa26597e57ee9c7f6, ; 722: System.Xml.XmlDocument.dll => 162
	i64 u0xa308401900e5bed3, ; 723: lib_mscorlib.dll.so => 167
	i64 u0xa395572e7da6c99d, ; 724: lib_System.Security.dll.so => 131
	i64 u0xa3c64c49e90a9987, ; 725: System.Security.Cryptography.Pkcs => 239
	i64 u0xa3e683f24b43af6f, ; 726: System.Dynamic.Runtime.dll => 37
	i64 u0xa4145becdee3dc4f, ; 727: Xamarin.AndroidX.VectorDrawable.Animated => 312
	i64 u0xa46aa1eaa214539b, ; 728: ko/Microsoft.Maui.Controls.resources => 354
	i64 u0xa4edc8f2ceae241a, ; 729: System.Data.Common.dll => 22
	i64 u0xa5494f40f128ce6a, ; 730: System.Runtime.Serialization.Formatters.dll => 112
	i64 u0xa54b74df83dce92b, ; 731: System.Reflection.DispatchProxy => 90
	i64 u0xa5b7152421ed6d98, ; 732: lib_System.IO.FileSystem.Watcher.dll.so => 50
	i64 u0xa5c3844f17b822db, ; 733: lib_System.Linq.Parallel.dll.so => 60
	i64 u0xa5ce5c755bde8cb8, ; 734: lib_System.Security.Cryptography.Csp.dll.so => 122
	i64 u0xa5e599d1e0524750, ; 735: System.Numerics.Vectors.dll => 83
	i64 u0xa5f1ba49b85dd355, ; 736: System.Security.Cryptography.dll => 127
	i64 u0xa61975a5a37873ea, ; 737: lib_System.Xml.XmlSerializer.dll.so => 163
	i64 u0xa6593e21584384d2, ; 738: lib_Jsr305Binding.dll.so => 320
	i64 u0xa66cbee0130865f7, ; 739: lib_WindowsBase.dll.so => 166
	i64 u0xa67dbee13e1df9ca, ; 740: Xamarin.AndroidX.SavedState.dll => 303
	i64 u0xa684b098dd27b296, ; 741: lib_Xamarin.AndroidX.Security.SecurityCrypto.dll.so => 305
	i64 u0xa68a420042bb9b1f, ; 742: Xamarin.AndroidX.DrawerLayout.dll => 273
	i64 u0xa6d26156d1cacc7c, ; 743: Xamarin.Android.Glide.dll => 241
	i64 u0xa75386b5cb9595aa, ; 744: Xamarin.AndroidX.Lifecycle.Runtime.Android => 288
	i64 u0xa763fbb98df8d9fb, ; 745: lib_Microsoft.Win32.Primitives.dll.so => 4
	i64 u0xa77e30733da34712, ; 746: lib_Std.UriTemplate.dll.so => 229
	i64 u0xa78ce3745383236a, ; 747: Xamarin.AndroidX.Lifecycle.Common.Jvm => 282
	i64 u0xa7a2f0662ebff901, ; 748: Microsoft.Graph.Auth.dll => 202
	i64 u0xa7c31b56b4dc7b33, ; 749: hu/Microsoft.Maui.Controls.resources => 350
	i64 u0xa7eab29ed44b4e7a, ; 750: Mono.Android.Export => 170
	i64 u0xa8195217cbf017b7, ; 751: Microsoft.VisualBasic.Core => 2
	i64 u0xa82fd211eef00a5b, ; 752: Microsoft.Extensions.FileProviders.Physical => 194
	i64 u0xa859a95830f367ff, ; 753: lib_Xamarin.AndroidX.Lifecycle.ViewModel.Ktx.dll.so => 293
	i64 u0xa8b52f21e0dbe690, ; 754: System.Runtime.Serialization.dll => 116
	i64 u0xa8c84ce526c2b4bd, ; 755: Microsoft.VisualStudio.DesignTools.XamlTapContract.dll => 375
	i64 u0xa8e6320dd07580ef, ; 756: lib_Microsoft.IdentityModel.JsonWebTokens.dll.so => 206
	i64 u0xa8ee4ed7de2efaee, ; 757: Xamarin.AndroidX.Annotation.dll => 247
	i64 u0xa95590e7c57438a4, ; 758: System.Configuration => 19
	i64 u0xa964304b5631e28a, ; 759: CommunityToolkit.Maui.Core.dll => 178
	i64 u0xaa2219c8e3449ff5, ; 760: Microsoft.Extensions.Logging.Abstractions => 197
	i64 u0xaa443ac34067eeef, ; 761: System.Private.Xml.dll => 89
	i64 u0xaa52de307ef5d1dd, ; 762: System.Net.Http => 65
	i64 u0xaa9a7b0214a5cc5c, ; 763: System.Diagnostics.StackTrace.dll => 30
	i64 u0xaaaf86367285a918, ; 764: Microsoft.Extensions.DependencyInjection.Abstractions.dll => 192
	i64 u0xaaf432d11af52d87, ; 765: Microsoft.Graph.Core.dll => 203
	i64 u0xaaf84bb3f052a265, ; 766: el/Microsoft.Maui.Controls.resources => 343
	i64 u0xab9af77b5b67a0b8, ; 767: Xamarin.AndroidX.ConstraintLayout.Core => 265
	i64 u0xab9c1b2687d86b0b, ; 768: lib_System.Linq.Expressions.dll.so => 59
	i64 u0xab9c576dc13fe678, ; 769: lib_Microsoft.Kiota.Serialization.Json.dll.so => 217
	i64 u0xabe040529690b3a1, ; 770: EPPlus.System.Drawing => 183
	i64 u0xac2af3fa195a15ce, ; 771: System.Runtime.Numerics => 111
	i64 u0xac5376a2a538dc10, ; 772: Xamarin.AndroidX.Lifecycle.LiveData.Core.dll => 284
	i64 u0xac5acae88f60357e, ; 773: System.Diagnostics.Tools.dll => 32
	i64 u0xac79c7e46047ad98, ; 774: System.Security.Principal.Windows.dll => 128
	i64 u0xac98d31068e24591, ; 775: System.Xml.XDocument => 159
	i64 u0xacd46e002c3ccb97, ; 776: ro/Microsoft.Maui.Controls.resources => 361
	i64 u0xacdd9e4180d56dda, ; 777: Xamarin.AndroidX.Concurrent.Futures => 263
	i64 u0xacf42eea7ef9cd12, ; 778: System.Threading.Channels => 140
	i64 u0xad434add46c9e108, ; 779: lib_Microsoft.IdentityModel.Validators.dll.so => 211
	i64 u0xad89c07347f1bad6, ; 780: nl/Microsoft.Maui.Controls.resources.dll => 357
	i64 u0xadbb53caf78a79d2, ; 781: System.Web.HttpUtility => 153
	i64 u0xadc90ab061a9e6e4, ; 782: System.ComponentModel.TypeConverter.dll => 17
	i64 u0xadca1b9030b9317e, ; 783: Xamarin.AndroidX.Collection.Ktx => 262
	i64 u0xadd8eda2edf396ad, ; 784: Xamarin.Android.Glide.GifDecoder => 244
	i64 u0xadf4cf30debbeb9a, ; 785: System.Net.ServicePoint.dll => 75
	i64 u0xadf511667bef3595, ; 786: System.Net.Security => 74
	i64 u0xae031e1cb05086cb, ; 787: lib_EPPlus.Interfaces.dll.so => 182
	i64 u0xae0aaa94fdcfce0f, ; 788: System.ComponentModel.EventBasedAsync.dll => 15
	i64 u0xae282bcd03739de7, ; 789: Java.Interop => 169
	i64 u0xae53579c90db1107, ; 790: System.ObjectModel.dll => 85
	i64 u0xaec7c0c7e2ed4575, ; 791: lib_Xamarin.KotlinX.AtomicFU.Jvm.dll.so => 329
	i64 u0xaf732d0b2193b8f5, ; 792: System.Security.Cryptography.OpenSsl.dll => 124
	i64 u0xafdb94dbccd9d11c, ; 793: Xamarin.AndroidX.Lifecycle.LiveData.dll => 283
	i64 u0xafe29f45095518e7, ; 794: lib_Xamarin.AndroidX.Lifecycle.ViewModelSavedState.dll.so => 294
	i64 u0xb03ae931fb25607e, ; 795: Xamarin.AndroidX.ConstraintLayout => 264
	i64 u0xb05b6f0a6cc8ddbb, ; 796: lib_Microsoft.IO.RecyclableMemoryStream.dll.so => 212
	i64 u0xb05cc42cd94c6d9d, ; 797: lib-sv-Microsoft.Maui.Controls.resources.dll.so => 364
	i64 u0xb0ac21bec8f428c5, ; 798: Xamarin.AndroidX.Lifecycle.Runtime.Ktx.Android.dll => 290
	i64 u0xb0bb43dc52ea59f9, ; 799: System.Diagnostics.Tracing.dll => 34
	i64 u0xb1dd05401aa8ee63, ; 800: System.Security.AccessControl => 118
	i64 u0xb220631954820169, ; 801: System.Text.RegularExpressions => 139
	i64 u0xb2376e1dbf8b4ed7, ; 802: System.Security.Cryptography.Csp => 122
	i64 u0xb2a1959fe95c5402, ; 803: lib_System.Runtime.InteropServices.JavaScript.dll.so => 106
	i64 u0xb2a3f67f3bf29fce, ; 804: da/Microsoft.Maui.Controls.resources => 341
	i64 u0xb3011a0a57f7ffb2, ; 805: Microsoft.VisualStudio.DesignTools.MobileTapContracts.dll => 373
	i64 u0xb31efb7ff1c40e7a, ; 806: EPPlus.dll => 181
	i64 u0xb343b35350be6ef3, ; 807: DocumentFormat.OpenXml.Framework => 180
	i64 u0xb3874072ee0ecf8c, ; 808: Xamarin.AndroidX.VectorDrawable.Animated.dll => 312
	i64 u0xb3f0a0fcda8d3ebc, ; 809: Xamarin.AndroidX.CardView => 259
	i64 u0xb3f832258cb83db4, ; 810: Syncfusion.Licensing.dll => 231
	i64 u0xb46be1aa6d4fff93, ; 811: hi/Microsoft.Maui.Controls.resources => 348
	i64 u0xb477491be13109d8, ; 812: ar/Microsoft.Maui.Controls.resources => 338
	i64 u0xb4bd7015ecee9d86, ; 813: System.IO.Pipelines => 54
	i64 u0xb4c53d9749c5f226, ; 814: lib_System.IO.FileSystem.AccessControl.dll.so => 47
	i64 u0xb4ff710863453fda, ; 815: System.Diagnostics.FileVersionInfo.dll => 28
	i64 u0xb5c38bf497a4cfe2, ; 816: lib_System.Threading.Tasks.dll.so => 145
	i64 u0xb5c7fcdafbc67ee4, ; 817: Microsoft.Extensions.Logging.Abstractions.dll => 197
	i64 u0xb5ea31d5244c6626, ; 818: System.Threading.ThreadPool.dll => 147
	i64 u0xb6f92eaf47db4cab, ; 819: lib_System.Private.Windows.Core.dll.so => 235
	i64 u0xb7212c4683a94afe, ; 820: System.Drawing.Primitives => 35
	i64 u0xb7b7753d1f319409, ; 821: sv/Microsoft.Maui.Controls.resources => 364
	i64 u0xb81a2c6e0aee50fe, ; 822: lib_System.Private.CoreLib.dll.so => 173
	i64 u0xb8b0a9b3dfbc5cb7, ; 823: Xamarin.AndroidX.Window.Extensions.Core.Core => 317
	i64 u0xb8c60af47c08d4da, ; 824: System.Net.ServicePoint => 75
	i64 u0xb8e68d20aad91196, ; 825: lib_System.Xml.XPath.dll.so => 161
	i64 u0xb9185c33a1643eed, ; 826: Microsoft.CSharp.dll => 1
	i64 u0xb9b8001adf4ed7cc, ; 827: lib_Xamarin.AndroidX.SlidingPaneLayout.dll.so => 306
	i64 u0xb9f64d3b230def68, ; 828: lib-pt-Microsoft.Maui.Controls.resources.dll.so => 360
	i64 u0xb9fc3c8a556e3691, ; 829: ja/Microsoft.Maui.Controls.resources => 353
	i64 u0xba4670aa94a2b3c6, ; 830: lib_System.Xml.XDocument.dll.so => 159
	i64 u0xba48785529705af9, ; 831: System.Collections.dll => 12
	i64 u0xba965b8c86359996, ; 832: lib_System.Windows.dll.so => 155
	i64 u0xbb286883bc35db36, ; 833: System.Transactions.dll => 151
	i64 u0xbb65706fde942ce3, ; 834: System.Net.Sockets => 76
	i64 u0xbb6dc0b35452c1a0, ; 835: ZXing.Net.MAUI.dll => 336
	i64 u0xbba28979413cad9e, ; 836: lib_System.Runtime.CompilerServices.VisualC.dll.so => 103
	i64 u0xbbd180354b67271a, ; 837: System.Runtime.Serialization.Formatters => 112
	i64 u0xbc260cdba33291a3, ; 838: Xamarin.AndroidX.Arch.Core.Common.dll => 252
	i64 u0xbd0e2c0d55246576, ; 839: System.Net.Http.dll => 65
	i64 u0xbd3fbd85b9e1cb29, ; 840: lib_System.Net.HttpListener.dll.so => 66
	i64 u0xbd437a2cdb333d0d, ; 841: Xamarin.AndroidX.ViewPager2 => 315
	i64 u0xbd4f572d2bd0a789, ; 842: System.IO.Compression.ZipFile.dll => 45
	i64 u0xbd5d0b88d3d647a5, ; 843: lib_Xamarin.AndroidX.Browser.dll.so => 254
	i64 u0xbd877b14d0b56392, ; 844: System.Runtime.Intrinsics.dll => 109
	i64 u0xbe08e3083025c53d, ; 845: ZXing.Net.MAUI.Controls.dll => 337
	i64 u0xbe532a80075c3dc8, ; 846: Xamarin.AndroidX.Camera.Core.dll => 256
	i64 u0xbe65a49036345cf4, ; 847: lib_System.Buffers.dll.so => 7
	i64 u0xbedf4e9b29564ad3, ; 848: lib_MobileScanner.dll.so => 0
	i64 u0xbee1b395605474f1, ; 849: System.Drawing.Common.dll => 234
	i64 u0xbee38d4a88835966, ; 850: Xamarin.AndroidX.AppCompat.AppCompatResources => 251
	i64 u0xbef9919db45b4ca7, ; 851: System.IO.Pipes.AccessControl => 55
	i64 u0xbf0fa68611139208, ; 852: lib_Xamarin.AndroidX.Annotation.dll.so => 247
	i64 u0xbfc1e1fb3095f2b3, ; 853: lib_System.Net.Http.Json.dll.so => 64
	i64 u0xc040a4ab55817f58, ; 854: ar/Microsoft.Maui.Controls.resources.dll => 338
	i64 u0xc07cadab29efeba0, ; 855: Xamarin.AndroidX.Core.Core.Ktx.dll => 268
	i64 u0xc0c7d9274d1f6be3, ; 856: lib_Microsoft.Kiota.Abstractions.dll.so => 213
	i64 u0xc0d928351ab5ca77, ; 857: System.Console.dll => 20
	i64 u0xc0f5a221a9383aea, ; 858: System.Runtime.Intrinsics => 109
	i64 u0xc111030af54d7191, ; 859: System.Resources.Writer => 101
	i64 u0xc12b8b3afa48329c, ; 860: lib_System.Linq.dll.so => 62
	i64 u0xc183ca0b74453aa9, ; 861: lib_System.Threading.Tasks.Dataflow.dll.so => 142
	i64 u0xc1d2d5e987094943, ; 862: ClosedXML => 175
	i64 u0xc1ff9ae3cdb6e1e6, ; 863: Xamarin.AndroidX.Activity.dll => 245
	i64 u0xc2054e3663642113, ; 864: lib_ExcelNumberFormat.dll.so => 184
	i64 u0xc256638aedbc4a74, ; 865: EPPlus.Interfaces => 182
	i64 u0xc26c064effb1dea9, ; 866: System.Buffers.dll => 7
	i64 u0xc278de356ad8a9e3, ; 867: Microsoft.IdentityModel.Logging => 207
	i64 u0xc28c50f32f81cc73, ; 868: ja/Microsoft.Maui.Controls.resources.dll => 353
	i64 u0xc2902f6cf5452577, ; 869: lib_Mono.Android.Export.dll.so => 170
	i64 u0xc2a3bca55b573141, ; 870: System.IO.FileSystem.Watcher => 50
	i64 u0xc2bcfec99f69365e, ; 871: Xamarin.AndroidX.ViewPager2.dll => 315
	i64 u0xc30b52815b58ac2c, ; 872: lib_System.Runtime.Serialization.Xml.dll.so => 115
	i64 u0xc36d7d89c652f455, ; 873: System.Threading.Overlapped => 141
	i64 u0xc396b285e59e5493, ; 874: GoogleGson.dll => 185
	i64 u0xc3c86c1e5e12f03d, ; 875: WindowsBase => 166
	i64 u0xc3f0e03e56ce7b69, ; 876: zxing => 335
	i64 u0xc421b61fd853169d, ; 877: lib_System.Net.WebSockets.Client.dll.so => 80
	i64 u0xc463e077917aa21d, ; 878: System.Runtime.Serialization.Json => 113
	i64 u0xc4d3858ed4d08512, ; 879: Xamarin.AndroidX.Lifecycle.ViewModelSavedState.dll => 294
	i64 u0xc50fded0ded1418c, ; 880: lib_System.ComponentModel.TypeConverter.dll.so => 17
	i64 u0xc519125d6bc8fb11, ; 881: lib_System.Net.Requests.dll.so => 73
	i64 u0xc5293b19e4dc230e, ; 882: Xamarin.AndroidX.Navigation.Fragment => 297
	i64 u0xc5325b2fcb37446f, ; 883: lib_System.Private.Xml.dll.so => 89
	i64 u0xc535cb9a21385d9b, ; 884: lib_Xamarin.Android.Glide.DiskLruCache.dll.so => 243
	i64 u0xc5a0f4b95a699af7, ; 885: lib_System.Private.Uri.dll.so => 87
	i64 u0xc5cdcd5b6277579e, ; 886: lib_System.Security.Cryptography.Algorithms.dll.so => 120
	i64 u0xc5ec286825cb0bf4, ; 887: Xamarin.AndroidX.Tracing.Tracing => 309
	i64 u0xc659b586d4c229e2, ; 888: Microsoft.Extensions.Configuration.FileExtensions.dll => 189
	i64 u0xc6706bc8aa7fe265, ; 889: Xamarin.AndroidX.Annotation.Jvm => 249
	i64 u0xc6c65ca6318f6fde, ; 890: lib_System.IO.Packaging.dll.so => 237
	i64 u0xc7c01e7d7c93a110, ; 891: System.Text.Encoding.Extensions.dll => 135
	i64 u0xc7ce851898a4548e, ; 892: lib_System.Web.HttpUtility.dll.so => 153
	i64 u0xc809d4089d2556b2, ; 893: System.Runtime.InteropServices.JavaScript.dll => 106
	i64 u0xc858a28d9ee5a6c5, ; 894: lib_System.Collections.Specialized.dll.so => 11
	i64 u0xc8ac7c6bf1c2ec51, ; 895: System.Reflection.DispatchProxy.dll => 90
	i64 u0xc9c62c8f354ac568, ; 896: lib_System.Diagnostics.TextWriterTraceListener.dll.so => 31
	i64 u0xc9e54b32fc19baf3, ; 897: lib_CommunityToolkit.Maui.dll.so => 177
	i64 u0xca3a723e7342c5b6, ; 898: lib-tr-Microsoft.Maui.Controls.resources.dll.so => 366
	i64 u0xca5801070d9fccfb, ; 899: System.Text.Encoding => 136
	i64 u0xcab3493c70141c2d, ; 900: pl/Microsoft.Maui.Controls.resources => 358
	i64 u0xcab69b9a31439815, ; 901: lib_Xamarin.Google.ErrorProne.TypeAnnotations.dll.so => 323
	i64 u0xcacfddc9f7c6de76, ; 902: ro/Microsoft.Maui.Controls.resources.dll => 361
	i64 u0xcadbc92899a777f0, ; 903: Xamarin.AndroidX.Startup.StartupRuntime => 307
	i64 u0xcba1cb79f45292b5, ; 904: Xamarin.Android.Glide.GifDecoder.dll => 244
	i64 u0xcbb5f80c7293e696, ; 905: lib_System.Globalization.Calendars.dll.so => 40
	i64 u0xcbd4fdd9cef4a294, ; 906: lib__Microsoft.Android.Resource.Designer.dll.so => 376
	i64 u0xcc15da1e07bbd994, ; 907: Xamarin.AndroidX.SlidingPaneLayout => 306
	i64 u0xcc182c3afdc374d6, ; 908: Microsoft.Bcl.AsyncInterfaces => 186
	i64 u0xcc2876b32ef2794c, ; 909: lib_System.Text.RegularExpressions.dll.so => 139
	i64 u0xcc5c3bb714c4561e, ; 910: Xamarin.KotlinX.Coroutines.Core.Jvm.dll => 332
	i64 u0xcc76886e09b88260, ; 911: Xamarin.KotlinX.Serialization.Core.Jvm.dll => 334
	i64 u0xcc9fa2923aa1c9ef, ; 912: System.Diagnostics.Contracts.dll => 25
	i64 u0xccf25c4b634ccd3a, ; 913: zh-Hans/Microsoft.Maui.Controls.resources.dll => 370
	i64 u0xcd10a42808629144, ; 914: System.Net.Requests => 73
	i64 u0xcdca1b920e9f53ba, ; 915: Xamarin.AndroidX.Interpolator => 280
	i64 u0xcdd0c48b6937b21c, ; 916: Xamarin.AndroidX.SwipeRefreshLayout => 308
	i64 u0xcde1fa22dc303670, ; 917: Microsoft.VisualStudio.DesignTools.XamlTapContract => 375
	i64 u0xceb28d385f84f441, ; 918: Azure.Core.dll => 174
	i64 u0xcf23d8093f3ceadf, ; 919: System.Diagnostics.DiagnosticSource.dll => 27
	i64 u0xcf5ff6b6b2c4c382, ; 920: System.Net.Mail.dll => 67
	i64 u0xcf8fc898f98b0d34, ; 921: System.Private.Xml.Linq => 88
	i64 u0xd04b5f59ed596e31, ; 922: System.Reflection.Metadata.dll => 95
	i64 u0xd063299fcfc0c93f, ; 923: lib_System.Runtime.Serialization.Json.dll.so => 113
	i64 u0xd0de8a113e976700, ; 924: System.Diagnostics.TextWriterTraceListener => 31
	i64 u0xd0fc33d5ae5d4cb8, ; 925: System.Runtime.Extensions => 104
	i64 u0xd1194e1d8a8de83c, ; 926: lib_Xamarin.AndroidX.Lifecycle.Common.Jvm.dll.so => 282
	i64 u0xd12beacdfc14f696, ; 927: System.Dynamic.Runtime => 37
	i64 u0xd198e7ce1b6a8344, ; 928: System.Net.Quic.dll => 72
	i64 u0xd2d7ebaf4c12e35f, ; 929: lib_RBush.dll.so => 227
	i64 u0xd3144156a3727ebe, ; 930: Xamarin.Google.Guava.ListenableFuture => 324
	i64 u0xd3299c184f2cad6e, ; 931: Microsoft.Kiota.Http.HttpClientLibrary.dll => 215
	i64 u0xd333d0af9e423810, ; 932: System.Runtime.InteropServices => 108
	i64 u0xd33a415cb4278969, ; 933: System.Security.Cryptography.Encoding.dll => 123
	i64 u0xd3426d966bb704f5, ; 934: Xamarin.AndroidX.AppCompat.AppCompatResources.dll => 251
	i64 u0xd3651b6fc3125825, ; 935: System.Private.Uri.dll => 87
	i64 u0xd373685349b1fe8b, ; 936: Microsoft.Extensions.Logging.dll => 196
	i64 u0xd3801faafafb7698, ; 937: System.Private.DataContractSerialization.dll => 86
	i64 u0xd3e4c8d6a2d5d470, ; 938: it/Microsoft.Maui.Controls.resources => 352
	i64 u0xd3edcc1f25459a50, ; 939: System.Reflection.Emit => 93
	i64 u0xd42c5e61f624b295, ; 940: ExcelNumberFormat => 184
	i64 u0xd4645626dffec99d, ; 941: lib_Microsoft.Extensions.DependencyInjection.Abstractions.dll.so => 192
	i64 u0xd4fa0abb79079ea9, ; 942: System.Security.Principal.dll => 129
	i64 u0xd5507e11a2b2839f, ; 943: Xamarin.AndroidX.Lifecycle.ViewModelSavedState => 294
	i64 u0xd567f168deeeaf3c, ; 944: lib_zxing.dll.so => 335
	i64 u0xd5d04bef8478ea19, ; 945: Xamarin.AndroidX.Tracing.Tracing.dll => 309
	i64 u0xd60815f26a12e140, ; 946: Microsoft.Extensions.Logging.Debug.dll => 198
	i64 u0xd63b432ec9306914, ; 947: zxing.dll => 335
	i64 u0xd65786d27a4ad960, ; 948: lib_Microsoft.Maui.Controls.HotReload.Forms.dll.so => 372
	i64 u0xd6694f8359737e4e, ; 949: Xamarin.AndroidX.SavedState => 303
	i64 u0xd6949e129339eae5, ; 950: lib_Xamarin.AndroidX.Core.Core.Ktx.dll.so => 268
	i64 u0xd6d21782156bc35b, ; 951: Xamarin.AndroidX.SwipeRefreshLayout.dll => 308
	i64 u0xd6de019f6af72435, ; 952: Xamarin.AndroidX.ConstraintLayout.Core.dll => 265
	i64 u0xd6f697a581fc6fe3, ; 953: Xamarin.Google.ErrorProne.TypeAnnotations.dll => 323
	i64 u0xd70956d1e6deefb9, ; 954: Jsr305Binding => 320
	i64 u0xd72329819cbbbc44, ; 955: lib_Microsoft.Extensions.Configuration.Abstractions.dll.so => 188
	i64 u0xd72c760af136e863, ; 956: System.Xml.XmlSerializer.dll => 163
	i64 u0xd753f071e44c2a03, ; 957: lib_System.Security.SecureString.dll.so => 130
	i64 u0xd7b3764ada9d341d, ; 958: lib_Microsoft.Extensions.Logging.Abstractions.dll.so => 197
	i64 u0xd7f0088bc5ad71f2, ; 959: Xamarin.AndroidX.VersionedParcelable => 313
	i64 u0xd8fb25e28ae30a12, ; 960: Xamarin.AndroidX.ProfileInstaller.ProfileInstaller.dll => 300
	i64 u0xd9d04d95a2671e29, ; 961: lib_ZXing.Net.MAUI.Controls.dll.so => 337
	i64 u0xda1dfa4c534a9251, ; 962: Microsoft.Extensions.DependencyInjection => 191
	i64 u0xdad05a11827959a3, ; 963: System.Collections.NonGeneric.dll => 10
	i64 u0xdaefdfe71aa53cf9, ; 964: System.IO.FileSystem.Primitives => 49
	i64 u0xdb5383ab5865c007, ; 965: lib-vi-Microsoft.Maui.Controls.resources.dll.so => 368
	i64 u0xdb58816721c02a59, ; 966: lib_System.Reflection.Emit.ILGeneration.dll.so => 91
	i64 u0xdbeda89f832aa805, ; 967: vi/Microsoft.Maui.Controls.resources.dll => 368
	i64 u0xdbf2a779fbc3ac31, ; 968: System.Transactions.Local.dll => 150
	i64 u0xdbf9607a441b4505, ; 969: System.Linq => 62
	i64 u0xdbfc90157a0de9b0, ; 970: lib_System.Text.Encoding.dll.so => 136
	i64 u0xdc75032002d1a212, ; 971: lib_System.Transactions.Local.dll.so => 150
	i64 u0xdca8be7403f92d4f, ; 972: lib_System.Linq.Queryable.dll.so => 61
	i64 u0xdce2c53525640bf3, ; 973: Microsoft.Extensions.Logging => 196
	i64 u0xdd2b722d78ef5f43, ; 974: System.Runtime.dll => 117
	i64 u0xdd67031857c72f96, ; 975: lib_System.Text.Encodings.Web.dll.so => 137
	i64 u0xdd70765ad6162057, ; 976: Xamarin.JSpecify => 326
	i64 u0xdd92e229ad292030, ; 977: System.Numerics.dll => 84
	i64 u0xdde30e6b77aa6f6c, ; 978: lib-zh-Hans-Microsoft.Maui.Controls.resources.dll.so => 370
	i64 u0xde110ae80fa7c2e2, ; 979: System.Xml.XDocument.dll => 159
	i64 u0xde4726fcdf63a198, ; 980: Xamarin.AndroidX.Transition => 310
	i64 u0xde572c2b2fb32f93, ; 981: lib_System.Threading.Tasks.Extensions.dll.so => 143
	i64 u0xde8769ebda7d8647, ; 982: hr/Microsoft.Maui.Controls.resources.dll => 349
	i64 u0xdee075f3477ef6be, ; 983: Xamarin.AndroidX.ExifInterface.dll => 277
	i64 u0xdf4b773de8fb1540, ; 984: System.Net.dll => 82
	i64 u0xdf5820c64c84eafc, ; 985: ClosedXML.Parser => 176
	i64 u0xdfa254ebb4346068, ; 986: System.Net.Ping => 70
	i64 u0xe0142572c095a480, ; 987: Xamarin.AndroidX.AppCompat.dll => 250
	i64 u0xe021eaa401792a05, ; 988: System.Text.Encoding.dll => 136
	i64 u0xe02f89350ec78051, ; 989: Xamarin.AndroidX.CoordinatorLayout.dll => 266
	i64 u0xe0496b9d65ef5474, ; 990: Xamarin.Android.Glide.DiskLruCache.dll => 243
	i64 u0xe10b760bb1462e7a, ; 991: lib_System.Security.Cryptography.Primitives.dll.so => 125
	i64 u0xe1566bbdb759c5af, ; 992: Microsoft.Maui.Controls.HotReload.Forms.dll => 372
	i64 u0xe192a588d4410686, ; 993: lib_System.IO.Pipelines.dll.so => 54
	i64 u0xe1a08bd3fa539e0d, ; 994: System.Runtime.Loader => 110
	i64 u0xe1a77eb8831f7741, ; 995: System.Security.SecureString.dll => 130
	i64 u0xe1b52f9f816c70ef, ; 996: System.Private.Xml.Linq.dll => 88
	i64 u0xe1e199c8ab02e356, ; 997: System.Data.DataSetExtensions.dll => 23
	i64 u0xe1ecfdb7fff86067, ; 998: System.Net.Security.dll => 74
	i64 u0xe2252a80fe853de4, ; 999: lib_System.Security.Principal.dll.so => 129
	i64 u0xe22fa4c9c645db62, ; 1000: System.Diagnostics.TextWriterTraceListener.dll => 31
	i64 u0xe2420585aeceb728, ; 1001: System.Net.Requests.dll => 73
	i64 u0xe26692647e6bcb62, ; 1002: Xamarin.AndroidX.Lifecycle.Runtime.Ktx => 289
	i64 u0xe29b73bc11392966, ; 1003: lib-id-Microsoft.Maui.Controls.resources.dll.so => 351
	i64 u0xe2ad448dee50fbdf, ; 1004: System.Xml.Serialization => 158
	i64 u0xe2d920f978f5d85c, ; 1005: System.Data.DataSetExtensions => 23
	i64 u0xe2e426c7714fa0bc, ; 1006: Microsoft.Win32.Primitives.dll => 4
	i64 u0xe2ecad4b18de7d3c, ; 1007: Std.UriTemplate => 229
	i64 u0xe332bacb3eb4a806, ; 1008: Mono.Android.Export.dll => 170
	i64 u0xe3811d68d4fe8463, ; 1009: pt-BR/Microsoft.Maui.Controls.resources.dll => 359
	i64 u0xe3b7cbae5ad66c75, ; 1010: lib_System.Security.Cryptography.Encoding.dll.so => 123
	i64 u0xe4292b48f3224d5b, ; 1011: lib_Xamarin.AndroidX.Core.ViewTree.dll.so => 269
	i64 u0xe494f7ced4ecd10a, ; 1012: hu/Microsoft.Maui.Controls.resources.dll => 350
	i64 u0xe4a9b1e40d1e8917, ; 1013: lib-fi-Microsoft.Maui.Controls.resources.dll.so => 345
	i64 u0xe4f74a0b5bf9703f, ; 1014: System.Runtime.Serialization.Primitives => 114
	i64 u0xe50653e2bf1f4af6, ; 1015: Microsoft.Kiota.Serialization.Multipart => 218
	i64 u0xe5434e8a119ceb69, ; 1016: lib_Mono.Android.dll.so => 172
	i64 u0xe55703b9ce5c038a, ; 1017: System.Diagnostics.Tools => 32
	i64 u0xe57013c8afc270b5, ; 1018: Microsoft.VisualBasic => 3
	i64 u0xe6246bb45a39d0c5, ; 1019: Microsoft.Kiota.Serialization.Multipart.dll => 218
	i64 u0xe62913cc36bc07ec, ; 1020: System.Xml.dll => 164
	i64 u0xe770aaabc753743d, ; 1021: lib_Microsoft.Kiota.Http.HttpClientLibrary.dll.so => 215
	i64 u0xe7bea09c4900a191, ; 1022: Xamarin.AndroidX.VectorDrawable.dll => 311
	i64 u0xe7e03cc18dcdeb49, ; 1023: lib_System.Diagnostics.StackTrace.dll.so => 30
	i64 u0xe7e147ff99a7a380, ; 1024: lib_System.Configuration.dll.so => 19
	i64 u0xe86b0df4ba9e5db8, ; 1025: lib_Xamarin.AndroidX.Lifecycle.Runtime.Android.dll.so => 288
	i64 u0xe896622fe0902957, ; 1026: System.Reflection.Emit.dll => 93
	i64 u0xe89a2a9ef110899b, ; 1027: System.Drawing.dll => 36
	i64 u0xe8c5f8c100b5934b, ; 1028: Microsoft.Win32.Registry => 5
	i64 u0xe957c3976986ab72, ; 1029: lib_Xamarin.AndroidX.Window.Extensions.Core.Core.dll.so => 317
	i64 u0xe975d06779bc7baf, ; 1030: SixLabors.Fonts.dll => 228
	i64 u0xe98163eb702ae5c5, ; 1031: Xamarin.AndroidX.Arch.Core.Runtime => 253
	i64 u0xe994f23ba4c143e5, ; 1032: Xamarin.KotlinX.Coroutines.Android => 330
	i64 u0xe9b9c8c0458fd92a, ; 1033: System.Windows => 155
	i64 u0xe9d166d87a7f2bdb, ; 1034: lib_Xamarin.AndroidX.Startup.StartupRuntime.dll.so => 307
	i64 u0xea5a4efc2ad81d1b, ; 1035: Xamarin.Google.ErrorProne.Annotations => 322
	i64 u0xeb2313fe9d65b785, ; 1036: Xamarin.AndroidX.ConstraintLayout.dll => 264
	i64 u0xeb9e30ac32aac03e, ; 1037: lib_Microsoft.Win32.SystemEvents.dll.so => 226
	i64 u0xed19c616b3fcb7eb, ; 1038: Xamarin.AndroidX.VersionedParcelable.dll => 313
	i64 u0xed60c6fa891c051a, ; 1039: lib_Microsoft.VisualStudio.DesignTools.TapContract.dll.so => 374
	i64 u0xedc4817167106c23, ; 1040: System.Net.Sockets.dll => 76
	i64 u0xedc632067fb20ff3, ; 1041: System.Memory.dll => 63
	i64 u0xedc8e4ca71a02a8b, ; 1042: Xamarin.AndroidX.Navigation.Runtime.dll => 298
	i64 u0xee81f5b3f1c4f83b, ; 1043: System.Threading.ThreadPool => 147
	i64 u0xeeb7ebb80150501b, ; 1044: lib_Xamarin.AndroidX.Collection.Jvm.dll.so => 261
	i64 u0xeefc635595ef57f0, ; 1045: System.Security.Cryptography.Cng => 121
	i64 u0xef03b1b5a04e9709, ; 1046: System.Text.Encoding.CodePages.dll => 134
	i64 u0xef602c523fe2e87a, ; 1047: lib_Xamarin.Google.Guava.ListenableFuture.dll.so => 324
	i64 u0xef72742e1bcca27a, ; 1048: Microsoft.Maui.Essentials.dll => 223
	i64 u0xefd1e0c4e5c9b371, ; 1049: System.Resources.ResourceManager.dll => 100
	i64 u0xefd684bb6d739244, ; 1050: Microsoft.Kiota.Abstractions.dll => 213
	i64 u0xefe8f8d5ed3c72ea, ; 1051: System.Formats.Tar.dll => 39
	i64 u0xefec0b7fdc57ec42, ; 1052: Xamarin.AndroidX.Activity => 245
	i64 u0xf00c29406ea45e19, ; 1053: es/Microsoft.Maui.Controls.resources.dll => 344
	i64 u0xf09e47b6ae914f6e, ; 1054: System.Net.NameResolution => 68
	i64 u0xf0ac2b489fed2e35, ; 1055: lib_System.Diagnostics.Debug.dll.so => 26
	i64 u0xf0bb49dadd3a1fe1, ; 1056: lib_System.Net.ServicePoint.dll.so => 75
	i64 u0xf0de2537ee19c6ca, ; 1057: lib_System.Net.WebHeaderCollection.dll.so => 78
	i64 u0xf1138779fa181c68, ; 1058: lib_Xamarin.AndroidX.Lifecycle.Runtime.dll.so => 287
	i64 u0xf11b621fc87b983f, ; 1059: Microsoft.Maui.Controls.Xaml.dll => 221
	i64 u0xf161f4f3c3b7e62c, ; 1060: System.Data => 24
	i64 u0xf1624296ce223787, ; 1061: lib_ClosedXML.Parser.dll.so => 176
	i64 u0xf16eb650d5a464bc, ; 1062: System.ValueTuple => 152
	i64 u0xf1c4b4005493d871, ; 1063: System.Formats.Asn1.dll => 38
	i64 u0xf238bd79489d3a96, ; 1064: lib-nl-Microsoft.Maui.Controls.resources.dll.so => 357
	i64 u0xf2feea356ba760af, ; 1065: Xamarin.AndroidX.Arch.Core.Runtime.dll => 253
	i64 u0xf300e085f8acd238, ; 1066: lib_System.ServiceProcess.dll.so => 133
	i64 u0xf34e52b26e7e059d, ; 1067: System.Runtime.CompilerServices.VisualC.dll => 103
	i64 u0xf37221fda4ef8830, ; 1068: lib_Xamarin.Google.Android.Material.dll.so => 318
	i64 u0xf3ad9b8fb3eefd12, ; 1069: lib_System.IO.UnmanagedMemoryStream.dll.so => 57
	i64 u0xf3ddfe05336abf29, ; 1070: System => 165
	i64 u0xf408654b2a135055, ; 1071: System.Reflection.Emit.ILGeneration.dll => 91
	i64 u0xf4103170a1de5bd0, ; 1072: System.Linq.Queryable.dll => 61
	i64 u0xf42d20c23173d77c, ; 1073: lib_System.ServiceModel.Web.dll.so => 132
	i64 u0xf4c1dd70a5496a17, ; 1074: System.IO.Compression => 46
	i64 u0xf4ecf4b9afc64781, ; 1075: System.ServiceProcess.dll => 133
	i64 u0xf4eeeaa566e9b970, ; 1076: lib_Xamarin.AndroidX.CustomView.PoolingContainer.dll.so => 272
	i64 u0xf518f63ead11fcd1, ; 1077: System.Threading.Tasks => 145
	i64 u0xf5dc86709fe55ab9, ; 1078: Microsoft.Kiota.Serialization.Json => 217
	i64 u0xf5e59d7ac34b50aa, ; 1079: Microsoft.IdentityModel.Protocols.dll => 208
	i64 u0xf5fc7602fe27b333, ; 1080: System.Net.WebHeaderCollection => 78
	i64 u0xf6077741019d7428, ; 1081: Xamarin.AndroidX.CoordinatorLayout => 266
	i64 u0xf61ade9836ad4692, ; 1082: Microsoft.IdentityModel.Tokens.dll => 210
	i64 u0xf64aa85b130b0651, ; 1083: lib_DocumentFormat.OpenXml.Framework.dll.so => 180
	i64 u0xf6742cbf457c450b, ; 1084: Xamarin.AndroidX.Lifecycle.Runtime.Android.dll => 288
	i64 u0xf6c0e7d55a7a4e4f, ; 1085: Microsoft.IdentityModel.JsonWebTokens => 206
	i64 u0xf6de7fa3776f8927, ; 1086: lib_Microsoft.Extensions.Configuration.Json.dll.so => 190
	i64 u0xf70c0a7bf8ccf5af, ; 1087: System.Web => 154
	i64 u0xf77b20923f07c667, ; 1088: de/Microsoft.Maui.Controls.resources.dll => 342
	i64 u0xf7e2cac4c45067b3, ; 1089: lib_System.Numerics.Vectors.dll.so => 83
	i64 u0xf7e74930e0e3d214, ; 1090: zh-HK/Microsoft.Maui.Controls.resources.dll => 369
	i64 u0xf84773b5c81e3cef, ; 1091: lib-uk-Microsoft.Maui.Controls.resources.dll.so => 367
	i64 u0xf8aac5ea82de1348, ; 1092: System.Linq.Queryable => 61
	i64 u0xf8abd63acd77d37b, ; 1093: Xamarin.AndroidX.Camera.View => 258
	i64 u0xf8b77539b362d3ba, ; 1094: lib_System.Reflection.Primitives.dll.so => 96
	i64 u0xf8e045dc345b2ea3, ; 1095: lib_Xamarin.AndroidX.RecyclerView.dll.so => 301
	i64 u0xf915dc29808193a1, ; 1096: System.Web.HttpUtility.dll => 153
	i64 u0xf96c777a2a0686f4, ; 1097: hi/Microsoft.Maui.Controls.resources.dll => 348
	i64 u0xf9be54c8bcf8ff3b, ; 1098: System.Security.AccessControl.dll => 118
	i64 u0xf9eec5bb3a6aedc6, ; 1099: Microsoft.Extensions.Options => 199
	i64 u0xfa0e82300e67f913, ; 1100: lib_System.AppContext.dll.so => 6
	i64 u0xfa2fdb27e8a2c8e8, ; 1101: System.ComponentModel.EventBasedAsync => 15
	i64 u0xfa3f278f288b0e84, ; 1102: lib_System.Net.Security.dll.so => 74
	i64 u0xfa504dfa0f097d72, ; 1103: Microsoft.Extensions.FileProviders.Abstractions.dll => 193
	i64 u0xfa5ed7226d978949, ; 1104: lib-ar-Microsoft.Maui.Controls.resources.dll.so => 338
	i64 u0xfa645d91e9fc4cba, ; 1105: System.Threading.Thread => 146
	i64 u0xfad4d2c770e827f9, ; 1106: lib_System.IO.IsolatedStorage.dll.so => 52
	i64 u0xfb06dd2338e6f7c4, ; 1107: System.Net.Ping.dll => 70
	i64 u0xfb087abe5365e3b7, ; 1108: lib_System.Data.DataSetExtensions.dll.so => 23
	i64 u0xfb846e949baff5ea, ; 1109: System.Xml.Serialization.dll => 158
	i64 u0xfbad3e4ce4b98145, ; 1110: System.Security.Cryptography.X509Certificates => 126
	i64 u0xfbf0a31c9fc34bc4, ; 1111: lib_System.Net.Http.dll.so => 65
	i64 u0xfc6b7527cc280b3f, ; 1112: lib_System.Runtime.Serialization.Formatters.dll.so => 112
	i64 u0xfc719aec26adf9d9, ; 1113: Xamarin.AndroidX.Navigation.Fragment.dll => 297
	i64 u0xfc82690c2fe2735c, ; 1114: Xamarin.AndroidX.Lifecycle.Process.dll => 286
	i64 u0xfc93fc307d279893, ; 1115: System.IO.Pipes.AccessControl.dll => 55
	i64 u0xfcd302092ada6328, ; 1116: System.IO.MemoryMappedFiles.dll => 53
	i64 u0xfd22f00870e40ae0, ; 1117: lib_Xamarin.AndroidX.DrawerLayout.dll.so => 273
	i64 u0xfd49b3c1a76e2748, ; 1118: System.Runtime.InteropServices.RuntimeInformation => 107
	i64 u0xfd536c702f64dc47, ; 1119: System.Text.Encoding.Extensions => 135
	i64 u0xfd583f7657b6a1cb, ; 1120: Xamarin.AndroidX.Fragment => 278
	i64 u0xfd8dd91a2c26bd5d, ; 1121: Xamarin.AndroidX.Lifecycle.Runtime => 287
	i64 u0xfda36abccf05cf5c, ; 1122: System.Net.WebSockets.Client => 80
	i64 u0xfdbe4710aa9beeff, ; 1123: CommunityToolkit.Maui => 177
	i64 u0xfddbe9695626a7f5, ; 1124: Xamarin.AndroidX.Lifecycle.Common => 281
	i64 u0xfe9856c3af9365ab, ; 1125: lib_Microsoft.Extensions.Configuration.FileExtensions.dll.so => 189
	i64 u0xfeae9952cf03b8cb, ; 1126: tr/Microsoft.Maui.Controls.resources => 366
	i64 u0xfebe1950717515f9, ; 1127: Xamarin.AndroidX.Lifecycle.LiveData.Core.Ktx.dll => 285
	i64 u0xff270a55858bac8d, ; 1128: System.Security.Principal => 129
	i64 u0xff9b54613e0d2cc8, ; 1129: System.Net.Http.Json => 64
	i64 u0xffdb7a971be4ec73 ; 1130: System.ValueTuple.dll => 152
], align 16

@assembly_image_cache_indices = dso_local local_unnamed_addr constant [1131 x i32] [
	i32 219, i32 42, i32 331, i32 308, i32 13, i32 336, i32 298, i32 178,
	i32 239, i32 105, i32 171, i32 48, i32 250, i32 212, i32 7, i32 86,
	i32 362, i32 340, i32 368, i32 205, i32 274, i32 71, i32 301, i32 12,
	i32 222, i32 102, i32 369, i32 156, i32 19, i32 279, i32 261, i32 161,
	i32 276, i32 311, i32 167, i32 362, i32 10, i32 198, i32 235, i32 312,
	i32 174, i32 96, i32 272, i32 219, i32 273, i32 13, i32 199, i32 10,
	i32 238, i32 201, i32 127, i32 95, i32 240, i32 140, i32 39, i32 363,
	i32 334, i32 232, i32 314, i32 359, i32 257, i32 172, i32 244, i32 5,
	i32 223, i32 67, i32 305, i32 130, i32 186, i32 304, i32 275, i32 68,
	i32 262, i32 66, i32 57, i32 186, i32 271, i32 52, i32 43, i32 180,
	i32 125, i32 255, i32 67, i32 81, i32 289, i32 374, i32 158, i32 92,
	i32 99, i32 301, i32 209, i32 141, i32 151, i32 234, i32 254, i32 346,
	i32 162, i32 169, i32 347, i32 209, i32 192, i32 81, i32 374, i32 326,
	i32 262, i32 4, i32 5, i32 51, i32 101, i32 56, i32 0, i32 120,
	i32 98, i32 168, i32 118, i32 331, i32 21, i32 350, i32 137, i32 97,
	i32 334, i32 183, i32 77, i32 356, i32 307, i32 119, i32 258, i32 8,
	i32 165, i32 365, i32 70, i32 243, i32 290, i32 302, i32 194, i32 171,
	i32 145, i32 40, i32 305, i32 47, i32 30, i32 299, i32 354, i32 144,
	i32 230, i32 199, i32 163, i32 28, i32 84, i32 309, i32 77, i32 43,
	i32 29, i32 42, i32 181, i32 103, i32 117, i32 248, i32 233, i32 45,
	i32 91, i32 365, i32 56, i32 148, i32 373, i32 179, i32 146, i32 100,
	i32 49, i32 20, i32 267, i32 225, i32 114, i32 241, i32 232, i32 346,
	i32 321, i32 255, i32 327, i32 200, i32 256, i32 94, i32 58, i32 236,
	i32 351, i32 349, i32 81, i32 321, i32 169, i32 26, i32 71, i32 300,
	i32 277, i32 219, i32 372, i32 367, i32 69, i32 33, i32 345, i32 14,
	i32 139, i32 236, i32 38, i32 371, i32 195, i32 263, i32 182, i32 358,
	i32 134, i32 92, i32 88, i32 231, i32 149, i32 216, i32 364, i32 24,
	i32 138, i32 57, i32 217, i32 51, i32 343, i32 29, i32 157, i32 34,
	i32 164, i32 278, i32 205, i32 52, i32 376, i32 316, i32 90, i32 323,
	i32 259, i32 35, i32 346, i32 157, i32 195, i32 9, i32 344, i32 76,
	i32 55, i32 222, i32 340, i32 218, i32 220, i32 13, i32 315, i32 187,
	i32 252, i32 109, i32 293, i32 32, i32 104, i32 84, i32 225, i32 92,
	i32 53, i32 96, i32 325, i32 58, i32 9, i32 102, i32 271, i32 68,
	i32 208, i32 314, i32 339, i32 193, i32 227, i32 237, i32 125, i32 175,
	i32 302, i32 116, i32 135, i32 210, i32 126, i32 106, i32 327, i32 131,
	i32 254, i32 337, i32 324, i32 147, i32 156, i32 237, i32 279, i32 267,
	i32 189, i32 274, i32 302, i32 97, i32 24, i32 306, i32 143, i32 296,
	i32 3, i32 167, i32 251, i32 100, i32 161, i32 99, i32 269, i32 25,
	i32 93, i32 168, i32 172, i32 246, i32 3, i32 358, i32 276, i32 203,
	i32 1, i32 114, i32 327, i32 279, i32 286, i32 236, i32 33, i32 6,
	i32 240, i32 362, i32 156, i32 238, i32 360, i32 53, i32 179, i32 85,
	i32 313, i32 299, i32 44, i32 285, i32 104, i32 47, i32 138, i32 233,
	i32 176, i32 64, i32 295, i32 69, i32 80, i32 59, i32 89, i32 154,
	i32 233, i32 252, i32 133, i32 110, i32 352, i32 295, i32 300, i32 171,
	i32 134, i32 140, i32 40, i32 339, i32 232, i32 210, i32 214, i32 220,
	i32 319, i32 60, i32 292, i32 79, i32 25, i32 36, i32 235, i32 99,
	i32 289, i32 71, i32 22, i32 267, i32 224, i32 363, i32 121, i32 69,
	i32 107, i32 369, i32 119, i32 117, i32 281, i32 282, i32 11, i32 2,
	i32 124, i32 115, i32 142, i32 41, i32 87, i32 247, i32 173, i32 27,
	i32 148, i32 353, i32 191, i32 322, i32 246, i32 1, i32 248, i32 238,
	i32 44, i32 266, i32 149, i32 18, i32 86, i32 341, i32 41, i32 285,
	i32 260, i32 290, i32 94, i32 196, i32 28, i32 41, i32 78, i32 336,
	i32 275, i32 201, i32 263, i32 144, i32 108, i32 261, i32 11, i32 105,
	i32 137, i32 16, i32 122, i32 66, i32 157, i32 22, i32 343, i32 333,
	i32 102, i32 191, i32 332, i32 63, i32 228, i32 58, i32 221, i32 342,
	i32 110, i32 173, i32 213, i32 375, i32 330, i32 9, i32 318, i32 120,
	i32 98, i32 214, i32 105, i32 216, i32 293, i32 177, i32 220, i32 111,
	i32 249, i32 181, i32 49, i32 20, i32 292, i32 234, i32 270, i32 72,
	i32 265, i32 155, i32 39, i32 341, i32 35, i32 328, i32 38, i32 347,
	i32 317, i32 108, i32 356, i32 21, i32 325, i32 291, i32 224, i32 230,
	i32 15, i32 200, i32 79, i32 79, i32 270, i32 200, i32 297, i32 230,
	i32 304, i32 152, i32 21, i32 222, i32 340, i32 50, i32 51, i32 366,
	i32 356, i32 94, i32 242, i32 352, i32 16, i32 239, i32 269, i32 123,
	i32 349, i32 160, i32 45, i32 322, i32 185, i32 179, i32 116, i32 63,
	i32 166, i32 187, i32 14, i32 228, i32 303, i32 111, i32 249, i32 229,
	i32 60, i32 329, i32 190, i32 319, i32 225, i32 121, i32 355, i32 2,
	i32 365, i32 278, i32 291, i32 0, i32 226, i32 184, i32 328, i32 326,
	i32 291, i32 6, i32 260, i32 345, i32 274, i32 203, i32 211, i32 206,
	i32 17, i32 363, i32 342, i32 77, i32 264, i32 211, i32 319, i32 178,
	i32 215, i32 131, i32 325, i32 355, i32 83, i32 198, i32 12, i32 34,
	i32 119, i32 240, i32 333, i32 286, i32 276, i32 85, i32 241, i32 18,
	i32 314, i32 188, i32 204, i32 284, i32 175, i32 72, i32 373, i32 95,
	i32 165, i32 280, i32 82, i32 371, i32 250, i32 259, i32 329, i32 154,
	i32 36, i32 151, i32 367, i32 205, i32 370, i32 258, i32 144, i32 183,
	i32 56, i32 113, i32 260, i32 311, i32 310, i32 37, i32 371, i32 187,
	i32 115, i32 195, i32 248, i32 14, i32 242, i32 146, i32 43, i32 223,
	i32 246, i32 98, i32 332, i32 168, i32 16, i32 48, i32 107, i32 97,
	i32 231, i32 295, i32 27, i32 128, i32 29, i32 347, i32 226, i32 174,
	i32 193, i32 304, i32 128, i32 44, i32 270, i32 216, i32 275, i32 149,
	i32 8, i32 227, i32 202, i32 204, i32 296, i32 348, i32 361, i32 360,
	i32 132, i32 359, i32 42, i32 333, i32 33, i32 376, i32 46, i32 143,
	i32 292, i32 221, i32 283, i32 271, i32 190, i32 138, i32 62, i32 132,
	i32 339, i32 48, i32 160, i32 253, i32 283, i32 242, i32 281, i32 355,
	i32 310, i32 46, i32 164, i32 207, i32 280, i32 209, i32 207, i32 255,
	i32 257, i32 202, i32 344, i32 277, i32 214, i32 351, i32 224, i32 18,
	i32 8, i32 185, i32 268, i32 124, i32 256, i32 59, i32 141, i32 298,
	i32 354, i32 287, i32 208, i32 320, i32 212, i32 316, i32 150, i32 142,
	i32 331, i32 328, i32 126, i32 330, i32 160, i32 162, i32 272, i32 245,
	i32 188, i32 357, i32 26, i32 296, i32 284, i32 194, i32 257, i32 204,
	i32 82, i32 201, i32 316, i32 127, i32 321, i32 101, i32 148, i32 318,
	i32 299, i32 54, i32 162, i32 167, i32 131, i32 239, i32 37, i32 312,
	i32 354, i32 22, i32 112, i32 90, i32 50, i32 60, i32 122, i32 83,
	i32 127, i32 163, i32 320, i32 166, i32 303, i32 305, i32 273, i32 241,
	i32 288, i32 4, i32 229, i32 282, i32 202, i32 350, i32 170, i32 2,
	i32 194, i32 293, i32 116, i32 375, i32 206, i32 247, i32 19, i32 178,
	i32 197, i32 89, i32 65, i32 30, i32 192, i32 203, i32 343, i32 265,
	i32 59, i32 217, i32 183, i32 111, i32 284, i32 32, i32 128, i32 159,
	i32 361, i32 263, i32 140, i32 211, i32 357, i32 153, i32 17, i32 262,
	i32 244, i32 75, i32 74, i32 182, i32 15, i32 169, i32 85, i32 329,
	i32 124, i32 283, i32 294, i32 264, i32 212, i32 364, i32 290, i32 34,
	i32 118, i32 139, i32 122, i32 106, i32 341, i32 373, i32 181, i32 180,
	i32 312, i32 259, i32 231, i32 348, i32 338, i32 54, i32 47, i32 28,
	i32 145, i32 197, i32 147, i32 235, i32 35, i32 364, i32 173, i32 317,
	i32 75, i32 161, i32 1, i32 306, i32 360, i32 353, i32 159, i32 12,
	i32 155, i32 151, i32 76, i32 336, i32 103, i32 112, i32 252, i32 65,
	i32 66, i32 315, i32 45, i32 254, i32 109, i32 337, i32 256, i32 7,
	i32 0, i32 234, i32 251, i32 55, i32 247, i32 64, i32 338, i32 268,
	i32 213, i32 20, i32 109, i32 101, i32 62, i32 142, i32 175, i32 245,
	i32 184, i32 182, i32 7, i32 207, i32 353, i32 170, i32 50, i32 315,
	i32 115, i32 141, i32 185, i32 166, i32 335, i32 80, i32 113, i32 294,
	i32 17, i32 73, i32 297, i32 89, i32 243, i32 87, i32 120, i32 309,
	i32 189, i32 249, i32 237, i32 135, i32 153, i32 106, i32 11, i32 90,
	i32 31, i32 177, i32 366, i32 136, i32 358, i32 323, i32 361, i32 307,
	i32 244, i32 40, i32 376, i32 306, i32 186, i32 139, i32 332, i32 334,
	i32 25, i32 370, i32 73, i32 280, i32 308, i32 375, i32 174, i32 27,
	i32 67, i32 88, i32 95, i32 113, i32 31, i32 104, i32 282, i32 37,
	i32 72, i32 227, i32 324, i32 215, i32 108, i32 123, i32 251, i32 87,
	i32 196, i32 86, i32 352, i32 93, i32 184, i32 192, i32 129, i32 294,
	i32 335, i32 309, i32 198, i32 335, i32 372, i32 303, i32 268, i32 308,
	i32 265, i32 323, i32 320, i32 188, i32 163, i32 130, i32 197, i32 313,
	i32 300, i32 337, i32 191, i32 10, i32 49, i32 368, i32 91, i32 368,
	i32 150, i32 62, i32 136, i32 150, i32 61, i32 196, i32 117, i32 137,
	i32 326, i32 84, i32 370, i32 159, i32 310, i32 143, i32 349, i32 277,
	i32 82, i32 176, i32 70, i32 250, i32 136, i32 266, i32 243, i32 125,
	i32 372, i32 54, i32 110, i32 130, i32 88, i32 23, i32 74, i32 129,
	i32 31, i32 73, i32 289, i32 351, i32 158, i32 23, i32 4, i32 229,
	i32 170, i32 359, i32 123, i32 269, i32 350, i32 345, i32 114, i32 218,
	i32 172, i32 32, i32 3, i32 218, i32 164, i32 215, i32 311, i32 30,
	i32 19, i32 288, i32 93, i32 36, i32 5, i32 317, i32 228, i32 253,
	i32 330, i32 155, i32 307, i32 322, i32 264, i32 226, i32 313, i32 374,
	i32 76, i32 63, i32 298, i32 147, i32 261, i32 121, i32 134, i32 324,
	i32 223, i32 100, i32 213, i32 39, i32 245, i32 344, i32 68, i32 26,
	i32 75, i32 78, i32 287, i32 221, i32 24, i32 176, i32 152, i32 38,
	i32 357, i32 253, i32 133, i32 103, i32 318, i32 57, i32 165, i32 91,
	i32 61, i32 132, i32 46, i32 133, i32 272, i32 145, i32 217, i32 208,
	i32 78, i32 266, i32 210, i32 180, i32 288, i32 206, i32 190, i32 154,
	i32 342, i32 83, i32 369, i32 367, i32 61, i32 258, i32 96, i32 301,
	i32 153, i32 348, i32 118, i32 199, i32 6, i32 15, i32 74, i32 193,
	i32 338, i32 146, i32 52, i32 70, i32 23, i32 158, i32 126, i32 65,
	i32 112, i32 297, i32 286, i32 55, i32 53, i32 273, i32 107, i32 135,
	i32 278, i32 287, i32 80, i32 177, i32 281, i32 189, i32 366, i32 285,
	i32 129, i32 64, i32 152
], align 16

@marshal_methods_number_of_classes = dso_local local_unnamed_addr constant i32 0, align 4

@marshal_methods_class_cache = dso_local local_unnamed_addr global [0 x %struct.MarshalMethodsManagedClass] zeroinitializer, align 8

; Names of classes in which marshal methods reside
@mm_class_names = dso_local local_unnamed_addr constant [0 x ptr] zeroinitializer, align 8

@mm_method_names = dso_local local_unnamed_addr constant [1 x %struct.MarshalMethodName] [
	%struct.MarshalMethodName {
		i64 u0x0000000000000000, ; name: 
		ptr @.MarshalMethodName.0_name; char* name
	} ; 0
], align 8

; get_function_pointer (uint32_t mono_image_index, uint32_t class_index, uint32_t method_token, void*& target_ptr)
@get_function_pointer = internal dso_local unnamed_addr global ptr null, align 8

; Functions

; Function attributes: memory(write, argmem: none, inaccessiblemem: none) "min-legal-vector-width"="0" mustprogress nofree norecurse nosync "no-trapping-math"="true" nounwind "stack-protector-buffer-size"="8" uwtable willreturn
define void @xamarin_app_init(ptr nocapture noundef readnone %env, ptr noundef %fn) local_unnamed_addr #0
{
	%fnIsNull = icmp eq ptr %fn, null
	br i1 %fnIsNull, label %1, label %2

1: ; preds = %0
	%putsResult = call noundef i32 @puts(ptr @.str.0)
	call void @abort()
	unreachable 

2: ; preds = %1, %0
	store ptr %fn, ptr @get_function_pointer, align 8, !tbaa !3
	ret void
}

; Strings
@.str.0 = private unnamed_addr constant [40 x i8] c"get_function_pointer MUST be specified\0A\00", align 16

;MarshalMethodName
@.MarshalMethodName.0_name = private unnamed_addr constant [1 x i8] c"\00", align 1

; External functions

; Function attributes: noreturn "no-trapping-math"="true" nounwind "stack-protector-buffer-size"="8"
declare void @abort() local_unnamed_addr #2

; Function attributes: nofree nounwind
declare noundef i32 @puts(ptr noundef) local_unnamed_addr #1
attributes #0 = { memory(write, argmem: none, inaccessiblemem: none) "min-legal-vector-width"="0" mustprogress nofree norecurse nosync "no-trapping-math"="true" nounwind "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+crc32,+cx16,+cx8,+fxsr,+mmx,+popcnt,+sse,+sse2,+sse3,+sse4.1,+sse4.2,+ssse3,+x87" "tune-cpu"="generic" uwtable willreturn }
attributes #1 = { nofree nounwind }
attributes #2 = { noreturn "no-trapping-math"="true" nounwind "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+crc32,+cx16,+cx8,+fxsr,+mmx,+popcnt,+sse,+sse2,+sse3,+sse4.1,+sse4.2,+ssse3,+x87" "tune-cpu"="generic" }

; Metadata
!llvm.module.flags = !{!0, !1}
!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"PIC Level", i32 2}
!llvm.ident = !{!2}
!2 = !{!".NET for Android remotes/origin/release/9.0.1xx @ be1cab92326783479054e72990da08008e5be819"}
!3 = !{!4, !4, i64 0}
!4 = !{!"any pointer", !5, i64 0}
!5 = !{!"omnipotent char", !6, i64 0}
!6 = !{!"Simple C++ TBAA"}
