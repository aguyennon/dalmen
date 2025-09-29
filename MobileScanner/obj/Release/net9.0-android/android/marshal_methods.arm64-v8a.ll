; ModuleID = 'marshal_methods.arm64-v8a.ll'
source_filename = "marshal_methods.arm64-v8a.ll"
target datalayout = "e-m:e-i8:8:32-i16:16:32-i64:64-i128:128-n32:64-S128"
target triple = "aarch64-unknown-linux-android21"

%struct.MarshalMethodName = type {
	i64, ; uint64_t id
	ptr ; char* name
}

%struct.MarshalMethodsManagedClass = type {
	i32, ; uint32_t token
	ptr ; MonoClass klass
}

@assembly_image_cache = dso_local local_unnamed_addr global [179 x ptr] zeroinitializer, align 8

; Each entry maps hash of an assembly name to an index into the `assembly_image_cache` array
@assembly_image_cache_hashes = dso_local local_unnamed_addr constant [537 x i64] [
	i64 u0x0071cf2d27b7d61e, ; 0: lib_Xamarin.AndroidX.SwipeRefreshLayout.dll.so => 93
	i64 u0x01af0bd6467d518e, ; 1: lib_ZXing.Net.MAUI.dll.so => 102
	i64 u0x02123411c4e01926, ; 2: lib_Xamarin.AndroidX.Navigation.Runtime.dll.so => 89
	i64 u0x022e81ea9c46e03a, ; 3: lib_CommunityToolkit.Maui.Core.dll.so => 39
	i64 u0x02abedc11addc1ed, ; 4: lib_Mono.Android.Runtime.dll.so => 177
	i64 u0x032267b2a94db371, ; 5: lib_Xamarin.AndroidX.AppCompat.dll.so => 67
	i64 u0x03621c804933a890, ; 6: System.Buffers => 106
	i64 u0x043032f1d071fae0, ; 7: ru/Microsoft.Maui.Controls.resources => 24
	i64 u0x044440a55165631e, ; 8: lib-cs-Microsoft.Maui.Controls.resources.dll.so => 2
	i64 u0x046eb1581a80c6b0, ; 9: vi/Microsoft.Maui.Controls.resources => 30
	i64 u0x0470607fd33c32db, ; 10: Microsoft.IdentityModel.Abstractions.dll => 54
	i64 u0x0517ef04e06e9f76, ; 11: System.Net.Primitives => 137
	i64 u0x0565d18c6da3de38, ; 12: Xamarin.AndroidX.RecyclerView => 91
	i64 u0x0581db89237110e9, ; 13: lib_System.Collections.dll.so => 111
	i64 u0x05989cb940b225a9, ; 14: Microsoft.Maui.dll => 57
	i64 u0x05a1c25e78e22d87, ; 15: lib_System.Runtime.CompilerServices.Unsafe.dll.so => 147
	i64 u0x06076b5d2b581f08, ; 16: zh-HK/Microsoft.Maui.Controls.resources => 31
	i64 u0x06388ffe9f6c161a, ; 17: System.Xml.Linq.dll => 170
	i64 u0x0680a433c781bb3d, ; 18: Xamarin.AndroidX.Collection.Jvm => 74
	i64 u0x07c57877c7ba78ad, ; 19: ru/Microsoft.Maui.Controls.resources.dll => 24
	i64 u0x07dcdc7460a0c5e4, ; 20: System.Collections.NonGeneric => 109
	i64 u0x08881a0a9768df86, ; 21: lib_Azure.Core.dll.so => 35
	i64 u0x08f3c9788ee2153c, ; 22: Xamarin.AndroidX.DrawerLayout => 79
	i64 u0x0919c28b89381a0b, ; 23: lib_Microsoft.Extensions.Options.dll.so => 49
	i64 u0x092266563089ae3e, ; 24: lib_System.Collections.NonGeneric.dll.so => 109
	i64 u0x095cacaf6b6a32e4, ; 25: System.Memory.Data => 65
	i64 u0x09d144a7e214d457, ; 26: System.Security.Cryptography => 158
	i64 u0x0abb3e2b271edc45, ; 27: System.Threading.Channels.dll => 165
	i64 u0x0b3b632c3bbee20c, ; 28: sk/Microsoft.Maui.Controls.resources => 25
	i64 u0x0b6aff547b84fbe9, ; 29: Xamarin.KotlinX.Serialization.Core.Jvm => 100
	i64 u0x0be2e1f8ce4064ed, ; 30: Xamarin.AndroidX.ViewPager => 94
	i64 u0x0c3ca6cc978e2aae, ; 31: pt-BR/Microsoft.Maui.Controls.resources => 21
	i64 u0x0c3d7adcdb333bf0, ; 32: Xamarin.AndroidX.Camera.Lifecycle => 71
	i64 u0x0c59ad9fbbd43abe, ; 33: Mono.Android => 178
	i64 u0x0c7790f60165fc06, ; 34: lib_Microsoft.Maui.Essentials.dll.so => 58
	i64 u0x0d13cd7cce4284e4, ; 35: System.Security.SecureString => 159
	i64 u0x0e14e73a54dda68e, ; 36: lib_System.Net.NameResolution.dll.so => 135
	i64 u0x102a31b45304b1da, ; 37: Xamarin.AndroidX.CustomView => 78
	i64 u0x10f6cfcbcf801616, ; 38: System.IO.Compression.Brotli => 125
	i64 u0x111e7120c198511e, ; 39: DocumentFormat.OpenXml.Framework.dll => 41
	i64 u0x125b7f94acb989db, ; 40: Xamarin.AndroidX.RecyclerView.dll => 91
	i64 u0x138567fa954faa55, ; 41: Xamarin.AndroidX.Browser => 69
	i64 u0x13a01de0cbc3f06c, ; 42: lib-fr-Microsoft.Maui.Controls.resources.dll.so => 8
	i64 u0x13f1e5e209e91af4, ; 43: lib_Java.Interop.dll.so => 176
	i64 u0x13f1e880c25d96d1, ; 44: he/Microsoft.Maui.Controls.resources => 9
	i64 u0x143d8ea60a6a4011, ; 45: Microsoft.Extensions.DependencyInjection.Abstractions => 46
	i64 u0x15bdc156ed462f2f, ; 46: lib_System.IO.FileSystem.dll.so => 127
	i64 u0x16d2f10b6ba5c55c, ; 47: MobileScanner.dll => 104
	i64 u0x17125c9a85b4929f, ; 48: lib_netstandard.dll.so => 174
	i64 u0x17b56e25558a5d36, ; 49: lib-hu-Microsoft.Maui.Controls.resources.dll.so => 12
	i64 u0x17f9358913beb16a, ; 50: System.Text.Encodings.Web => 162
	i64 u0x18402a709e357f3b, ; 51: lib_Xamarin.KotlinX.Serialization.Core.Jvm.dll.so => 100
	i64 u0x18f0ce884e87d89a, ; 52: nb/Microsoft.Maui.Controls.resources.dll => 18
	i64 u0x19a4c090f14ebb66, ; 53: System.Security.Claims => 156
	i64 u0x1a040febb58bf51e, ; 54: lib_Xamarin.AndroidX.Camera.View.dll.so => 72
	i64 u0x1a91866a319e9259, ; 55: lib_System.Collections.Concurrent.dll.so => 107
	i64 u0x1aac34d1917ba5d3, ; 56: lib_System.dll.so => 173
	i64 u0x1aad60783ffa3e5b, ; 57: lib-th-Microsoft.Maui.Controls.resources.dll.so => 27
	i64 u0x1c753b5ff15bce1b, ; 58: Mono.Android.Runtime.dll => 177
	i64 u0x1cd47467799d8250, ; 59: System.Threading.Tasks.dll => 166
	i64 u0x1e3d87657e9659bc, ; 60: Xamarin.AndroidX.Navigation.UI => 90
	i64 u0x1e71143913d56c10, ; 61: lib-ko-Microsoft.Maui.Controls.resources.dll.so => 16
	i64 u0x1ed8fcce5e9b50a0, ; 62: Microsoft.Extensions.Options.dll => 49
	i64 u0x209375905fcc1bad, ; 63: lib_System.IO.Compression.Brotli.dll.so => 125
	i64 u0x2174319c0d835bc9, ; 64: System.Runtime => 155
	i64 u0x2199f06354c82d3b, ; 65: System.ClientModel.dll => 63
	i64 u0x220fd4f2e7c48170, ; 66: th/Microsoft.Maui.Controls.resources => 27
	i64 u0x235fb4941dc174e1, ; 67: DocumentFormat.OpenXml => 40
	i64 u0x237be844f1f812c7, ; 68: System.Threading.Thread.dll => 167
	i64 u0x23852b3bdc9f7096, ; 69: System.Resources.ResourceManager => 146
	i64 u0x2407aef2bbe8fadf, ; 70: System.Console => 115
	i64 u0x240abe014b27e7d3, ; 71: Xamarin.AndroidX.Core.dll => 76
	i64 u0x247619fe4413f8bf, ; 72: System.Runtime.Serialization.Primitives.dll => 154
	i64 u0x252073cc3caa62c2, ; 73: fr/Microsoft.Maui.Controls.resources.dll => 8
	i64 u0x2662c629b96b0b30, ; 74: lib_Xamarin.Kotlin.StdLib.dll.so => 98
	i64 u0x268c1439f13bcc29, ; 75: lib_Microsoft.Extensions.Primitives.dll.so => 50
	i64 u0x268f1dca6d06d437, ; 76: Xamarin.AndroidX.Camera.Core => 70
	i64 u0x26d077d9678fe34f, ; 77: System.IO.dll => 129
	i64 u0x273f3515de5faf0d, ; 78: id/Microsoft.Maui.Controls.resources.dll => 13
	i64 u0x2742545f9094896d, ; 79: hr/Microsoft.Maui.Controls.resources => 11
	i64 u0x27b410442fad6cf1, ; 80: Java.Interop.dll => 176
	i64 u0x27b97e0d52c3034a, ; 81: System.Diagnostics.Debug => 117
	i64 u0x2801845a2c71fbfb, ; 82: System.Net.Primitives.dll => 137
	i64 u0x2a128783efe70ba0, ; 83: uk/Microsoft.Maui.Controls.resources.dll => 29
	i64 u0x2a3b095612184159, ; 84: lib_System.Net.NetworkInformation.dll.so => 136
	i64 u0x2a6507a5ffabdf28, ; 85: System.Diagnostics.TraceSource.dll => 120
	i64 u0x2ad156c8e1354139, ; 86: fi/Microsoft.Maui.Controls.resources => 7
	i64 u0x2af298f63581d886, ; 87: System.Text.RegularExpressions.dll => 164
	i64 u0x2afc1c4f898552ee, ; 88: lib_System.Formats.Asn1.dll.so => 124
	i64 u0x2b148910ed40fbf9, ; 89: zh-Hant/Microsoft.Maui.Controls.resources.dll => 33
	i64 u0x2c8bd14bb93a7d82, ; 90: lib-pl-Microsoft.Maui.Controls.resources.dll.so => 20
	i64 u0x2cd723e9fe623c7c, ; 91: lib_System.Private.Xml.Linq.dll.so => 144
	i64 u0x2d169d318a968379, ; 92: System.Threading.dll => 168
	i64 u0x2d47774b7d993f59, ; 93: sv/Microsoft.Maui.Controls.resources.dll => 26
	i64 u0x2db915caf23548d2, ; 94: System.Text.Json.dll => 163
	i64 u0x2e5a40c319acb800, ; 95: System.IO.FileSystem => 127
	i64 u0x2e6f1f226821322a, ; 96: el/Microsoft.Maui.Controls.resources.dll => 5
	i64 u0x2f2e98e1c89b1aff, ; 97: System.Xml.ReaderWriter => 171
	i64 u0x2f5911d9ba814e4e, ; 98: System.Diagnostics.Tracing => 121
	i64 u0x309ee9eeec09a71e, ; 99: lib_Xamarin.AndroidX.Fragment.dll.so => 80
	i64 u0x309f2bedefa9a318, ; 100: Microsoft.IdentityModel.Abstractions => 54
	i64 u0x31195fef5d8fb552, ; 101: _Microsoft.Android.Resource.Designer.dll => 34
	i64 u0x32243413e774362a, ; 102: Xamarin.AndroidX.CardView.dll => 73
	i64 u0x3235427f8d12dae1, ; 103: lib_System.Drawing.Primitives.dll.so => 122
	i64 u0x329753a17a517811, ; 104: fr/Microsoft.Maui.Controls.resources => 8
	i64 u0x32aa989ff07a84ff, ; 105: lib_System.Xml.ReaderWriter.dll.so => 171
	i64 u0x33829542f112d59b, ; 106: System.Collections.Immutable => 108
	i64 u0x33a31443733849fe, ; 107: lib-es-Microsoft.Maui.Controls.resources.dll.so => 6
	i64 u0x341abc357fbb4ebf, ; 108: lib_System.Net.Sockets.dll.so => 140
	i64 u0x34dfd74fe2afcf37, ; 109: Microsoft.Maui => 57
	i64 u0x34e292762d9615df, ; 110: cs/Microsoft.Maui.Controls.resources.dll => 2
	i64 u0x3508234247f48404, ; 111: Microsoft.Maui.Controls => 55
	i64 u0x3549870798b4cd30, ; 112: lib_Xamarin.AndroidX.ViewPager2.dll.so => 95
	i64 u0x355282fc1c909694, ; 113: Microsoft.Extensions.Configuration => 43
	i64 u0x3628ab68db23a01a, ; 114: lib_System.Diagnostics.Tools.dll.so => 119
	i64 u0x3673b042508f5b6b, ; 115: lib_System.Runtime.Extensions.dll.so => 148
	i64 u0x37bc29f3183003b6, ; 116: lib_System.IO.dll.so => 129
	i64 u0x380134e03b1e160a, ; 117: System.Collections.Immutable.dll => 108
	i64 u0x38049b5c59b39324, ; 118: System.Runtime.CompilerServices.Unsafe => 147
	i64 u0x385c17636bb6fe6e, ; 119: Xamarin.AndroidX.CustomView.dll => 78
	i64 u0x38869c811d74050e, ; 120: System.Net.NameResolution.dll => 135
	i64 u0x393c226616977fdb, ; 121: lib_Xamarin.AndroidX.ViewPager.dll.so => 94
	i64 u0x395e37c3334cf82a, ; 122: lib-ca-Microsoft.Maui.Controls.resources.dll.so => 1
	i64 u0x3a67fa982ce4abf0, ; 123: RBush => 60
	i64 u0x3a76a7a156f3d989, ; 124: System.IO.Packaging => 64
	i64 u0x3ad31bc4ddf45918, ; 125: ClosedXML.dll => 36
	i64 u0x3b860f9932505633, ; 126: lib_System.Text.Encoding.Extensions.dll.so => 160
	i64 u0x3c3aafb6b3a00bf6, ; 127: lib_System.Security.Cryptography.X509Certificates.dll.so => 157
	i64 u0x3c7c495f58ac5ee9, ; 128: Xamarin.Kotlin.StdLib => 98
	i64 u0x3cd9d281d402eb9b, ; 129: Xamarin.AndroidX.Browser.dll => 69
	i64 u0x3ced6a4f3010aa96, ; 130: ZXing.Net.MAUI.Controls => 103
	i64 u0x3d1c50cc001a991e, ; 131: Xamarin.Google.Guava.ListenableFuture.dll => 97
	i64 u0x3d46f0b995082740, ; 132: System.Xml.Linq => 170
	i64 u0x3d551d0efdd24596, ; 133: System.IO.Packaging.dll => 64
	i64 u0x3d9c2a242b040a50, ; 134: lib_Xamarin.AndroidX.Core.dll.so => 76
	i64 u0x407a10bb4bf95829, ; 135: lib_Xamarin.AndroidX.Navigation.Common.dll.so => 87
	i64 u0x41cab042be111c34, ; 136: lib_Xamarin.AndroidX.AppCompat.AppCompatResources.dll.so => 68
	i64 u0x423a9ecc4d905a88, ; 137: lib_System.Resources.ResourceManager.dll.so => 146
	i64 u0x43375950ec7c1b6a, ; 138: netstandard.dll => 174
	i64 u0x434c4e1d9284cdae, ; 139: Mono.Android.dll => 178
	i64 u0x43950f84de7cc79a, ; 140: pl/Microsoft.Maui.Controls.resources.dll => 20
	i64 u0x440c274c940f0550, ; 141: Microsoft.Graph.Core => 52
	i64 u0x448bd33429269b19, ; 142: Microsoft.CSharp => 105
	i64 u0x4499fa3c8e494654, ; 143: lib_System.Runtime.Serialization.Primitives.dll.so => 154
	i64 u0x4515080865a951a5, ; 144: Xamarin.Kotlin.StdLib.dll => 98
	i64 u0x45c40276a42e283e, ; 145: System.Diagnostics.TraceSource => 120
	i64 u0x46a4213bc97fe5ae, ; 146: lib-ru-Microsoft.Maui.Controls.resources.dll.so => 24
	i64 u0x47358bd471172e1d, ; 147: lib_System.Xml.Linq.dll.so => 170
	i64 u0x4787a936949fcac2, ; 148: System.Memory.Data.dll => 65
	i64 u0x47daf4e1afbada10, ; 149: pt/Microsoft.Maui.Controls.resources => 22
	i64 u0x48e9c8e5d5e8555a, ; 150: DocumentFormat.OpenXml.dll => 40
	i64 u0x49e952f19a4e2022, ; 151: System.ObjectModel => 142
	i64 u0x4a5667b2462a664b, ; 152: lib_Xamarin.AndroidX.Navigation.UI.dll.so => 90
	i64 u0x4b07a0ed0ab33ff4, ; 153: System.Runtime.Extensions.dll => 148
	i64 u0x4b7b6532ded934b7, ; 154: System.Text.Json => 163
	i64 u0x4b8f8ea3c2df6bb0, ; 155: System.ClientModel => 63
	i64 u0x4c69a4a1b905a70e, ; 156: ClosedXML.Parser.dll => 37
	i64 u0x4cc5f15266470798, ; 157: lib_Xamarin.AndroidX.Loader.dll.so => 86
	i64 u0x4cf6f67dc77aacd2, ; 158: System.Net.NetworkInformation.dll => 136
	i64 u0x4d479f968a05e504, ; 159: System.Linq.Expressions.dll => 130
	i64 u0x4d55a010ffc4faff, ; 160: System.Private.Xml => 145
	i64 u0x4d6001db23f8cd87, ; 161: lib_System.ClientModel.dll.so => 63
	i64 u0x4d95fccc1f67c7ca, ; 162: System.Runtime.Loader.dll => 151
	i64 u0x4dcf44c3c9b076a2, ; 163: it/Microsoft.Maui.Controls.resources.dll => 14
	i64 u0x4dd9247f1d2c3235, ; 164: Xamarin.AndroidX.Loader.dll => 86
	i64 u0x4e32f00cb0937401, ; 165: Mono.Android.Runtime => 177
	i64 u0x4ebd0c4b82c5eefc, ; 166: lib_System.Threading.Channels.dll.so => 165
	i64 u0x4f21ee6ef9eb527e, ; 167: ca/Microsoft.Maui.Controls.resources => 1
	i64 u0x5037f0be3c28c7a3, ; 168: lib_Microsoft.Maui.Controls.dll.so => 55
	i64 u0x50c3a29b21050d45, ; 169: System.Linq.Parallel.dll => 131
	i64 u0x5131bbe80989093f, ; 170: Xamarin.AndroidX.Lifecycle.ViewModel.Android.dll => 84
	i64 u0x51bb8a2afe774e32, ; 171: System.Drawing => 123
	i64 u0x526ce79eb8e90527, ; 172: lib_System.Net.Primitives.dll.so => 137
	i64 u0x52829f00b4467c38, ; 173: lib_System.Data.Common.dll.so => 116
	i64 u0x529ffe06f39ab8db, ; 174: Xamarin.AndroidX.Core => 76
	i64 u0x52ff996554dbf352, ; 175: Microsoft.Maui.Graphics => 59
	i64 u0x535f7e40e8fef8af, ; 176: lib-sk-Microsoft.Maui.Controls.resources.dll.so => 25
	i64 u0x53a96d5c86c9e194, ; 177: System.Net.NetworkInformation => 136
	i64 u0x53be1038a61e8d44, ; 178: System.Runtime.InteropServices.RuntimeInformation.dll => 149
	i64 u0x53c3014b9437e684, ; 179: lib-zh-HK-Microsoft.Maui.Controls.resources.dll.so => 31
	i64 u0x5435e6f049e9bc37, ; 180: System.Security.Claims.dll => 156
	i64 u0x54795225dd1587af, ; 181: lib_System.Runtime.dll.so => 155
	i64 u0x547a34f14e5f6210, ; 182: Xamarin.AndroidX.Lifecycle.Common.dll => 81
	i64 u0x556e8b63b660ab8b, ; 183: Xamarin.AndroidX.Lifecycle.Common.Jvm.dll => 82
	i64 u0x5588627c9a108ec9, ; 184: System.Collections.Specialized => 110
	i64 u0x571c5cfbec5ae8e2, ; 185: System.Private.Uri => 143
	i64 u0x579a06fed6eec900, ; 186: System.Private.CoreLib.dll => 175
	i64 u0x57c542c14049b66d, ; 187: System.Diagnostics.DiagnosticSource => 118
	i64 u0x58601b2dda4a27b9, ; 188: lib-ja-Microsoft.Maui.Controls.resources.dll.so => 15
	i64 u0x58688d9af496b168, ; 189: Microsoft.Extensions.DependencyInjection.dll => 45
	i64 u0x595a356d23e8da9a, ; 190: lib_Microsoft.CSharp.dll.so => 105
	i64 u0x5a70033ca9d003cb, ; 191: lib_System.Memory.Data.dll.so => 65
	i64 u0x5a89a886ae30258d, ; 192: lib_Xamarin.AndroidX.CoordinatorLayout.dll.so => 75
	i64 u0x5a8f6699f4a1caa9, ; 193: lib_System.Threading.dll.so => 168
	i64 u0x5ae9cd33b15841bf, ; 194: System.ComponentModel => 114
	i64 u0x5b5f0e240a06a2a2, ; 195: da/Microsoft.Maui.Controls.resources.dll => 3
	i64 u0x5c393624b8176517, ; 196: lib_Microsoft.Extensions.Logging.dll.so => 47
	i64 u0x5d1b514fc45c92d4, ; 197: ZXing.Net.MAUI => 102
	i64 u0x5db0cbbd1028510e, ; 198: lib_System.Runtime.InteropServices.dll.so => 150
	i64 u0x5db30905d3e5013b, ; 199: Xamarin.AndroidX.Collection.Jvm.dll => 74
	i64 u0x5e467bc8f09ad026, ; 200: System.Collections.Specialized.dll => 110
	i64 u0x5ea92fdb19ec8c4c, ; 201: System.Text.Encodings.Web.dll => 162
	i64 u0x5eb8046dd40e9ac3, ; 202: System.ComponentModel.Primitives => 112
	i64 u0x5f36ccf5c6a57e24, ; 203: System.Xml.ReaderWriter.dll => 171
	i64 u0x5f4294b9b63cb842, ; 204: System.Data.Common => 116
	i64 u0x5f9a2d823f664957, ; 205: lib-el-Microsoft.Maui.Controls.resources.dll.so => 5
	i64 u0x5fac98e0b37a5b9d, ; 206: System.Runtime.CompilerServices.Unsafe.dll => 147
	i64 u0x609f4b7b63d802d4, ; 207: lib_Microsoft.Extensions.DependencyInjection.dll.so => 45
	i64 u0x60cd4e33d7e60134, ; 208: Xamarin.KotlinX.Coroutines.Core.Jvm => 99
	i64 u0x60f62d786afcf130, ; 209: System.Memory => 133
	i64 u0x61a3b9f0f15a3269, ; 210: lib_SixLabors.Fonts.dll.so => 61
	i64 u0x61bb78c89f867353, ; 211: System.IO => 129
	i64 u0x61be8d1299194243, ; 212: Microsoft.Maui.Controls.Xaml => 56
	i64 u0x61d2cba29557038f, ; 213: de/Microsoft.Maui.Controls.resources => 4
	i64 u0x61d88f399afb2f45, ; 214: lib_System.Runtime.Loader.dll.so => 151
	i64 u0x622eef6f9e59068d, ; 215: System.Private.CoreLib => 175
	i64 u0x63f1f6883c1e23c2, ; 216: lib_System.Collections.Immutable.dll.so => 108
	i64 u0x6400f68068c1e9f1, ; 217: Xamarin.Google.Android.Material.dll => 96
	i64 u0x658f524e4aba7dad, ; 218: CommunityToolkit.Maui.dll => 38
	i64 u0x65ecac39144dd3cc, ; 219: Microsoft.Maui.Controls.dll => 55
	i64 u0x65ece51227bfa724, ; 220: lib_System.Runtime.Numerics.dll.so => 152
	i64 u0x6692e924eade1b29, ; 221: lib_System.Console.dll.so => 115
	i64 u0x66a4e5c6a3fb0bae, ; 222: lib_Xamarin.AndroidX.Lifecycle.ViewModel.Android.dll.so => 84
	i64 u0x66d13304ce1a3efa, ; 223: Xamarin.AndroidX.CursorAdapter => 77
	i64 u0x68558ec653afa616, ; 224: lib-da-Microsoft.Maui.Controls.resources.dll.so => 3
	i64 u0x6872ec7a2e36b1ac, ; 225: System.Drawing.Primitives.dll => 122
	i64 u0x68fbbbe2eb455198, ; 226: System.Formats.Asn1 => 124
	i64 u0x69063fc0ba8e6bdd, ; 227: he/Microsoft.Maui.Controls.resources.dll => 9
	i64 u0x6a4d7577b2317255, ; 228: System.Runtime.InteropServices.dll => 150
	i64 u0x6ace3b74b15ee4a4, ; 229: nb/Microsoft.Maui.Controls.resources => 18
	i64 u0x6d12bfaa99c72b1f, ; 230: lib_Microsoft.Maui.Graphics.dll.so => 59
	i64 u0x6d79993361e10ef2, ; 231: Microsoft.Extensions.Primitives => 50
	i64 u0x6d86d56b84c8eb71, ; 232: lib_Xamarin.AndroidX.CursorAdapter.dll.so => 77
	i64 u0x6d9bea6b3e895cf7, ; 233: Microsoft.Extensions.Primitives.dll => 50
	i64 u0x6e25a02c3833319a, ; 234: lib_Xamarin.AndroidX.Navigation.Fragment.dll.so => 88
	i64 u0x6fd2265da78b93a4, ; 235: lib_Microsoft.Maui.dll.so => 57
	i64 u0x6fdfc7de82c33008, ; 236: cs/Microsoft.Maui.Controls.resources => 2
	i64 u0x701cd46a1c25a5fe, ; 237: System.IO.FileSystem.dll => 127
	i64 u0x70e99f48c05cb921, ; 238: tr/Microsoft.Maui.Controls.resources.dll => 28
	i64 u0x70fd3deda22442d2, ; 239: lib-nb-Microsoft.Maui.Controls.resources.dll.so => 18
	i64 u0x71a495ea3761dde8, ; 240: lib-it-Microsoft.Maui.Controls.resources.dll.so => 14
	i64 u0x71ad672adbe48f35, ; 241: System.ComponentModel.Primitives.dll => 112
	i64 u0x72b1fb4109e08d7b, ; 242: lib-hr-Microsoft.Maui.Controls.resources.dll.so => 11
	i64 u0x73a2b85f84dcec96, ; 243: lib_DocumentFormat.OpenXml.dll.so => 40
	i64 u0x73e4ce94e2eb6ffc, ; 244: lib_System.Memory.dll.so => 133
	i64 u0x755a91767330b3d4, ; 245: lib_Microsoft.Extensions.Configuration.dll.so => 43
	i64 u0x75f59536ad2b55b1, ; 246: SixLabors.Fonts => 61
	i64 u0x76012e7334db86e5, ; 247: lib_Xamarin.AndroidX.SavedState.dll.so => 92
	i64 u0x76ca07b878f44da0, ; 248: System.Runtime.Numerics.dll => 152
	i64 u0x77564dc3bfb31c3f, ; 249: Std.UriTemplate.dll => 62
	i64 u0x778a805e625329ef, ; 250: System.Linq.Parallel => 131
	i64 u0x780bc73597a503a9, ; 251: lib-ms-Microsoft.Maui.Controls.resources.dll.so => 17
	i64 u0x783606d1e53e7a1a, ; 252: th/Microsoft.Maui.Controls.resources.dll => 27
	i64 u0x78a45e51311409b6, ; 253: Xamarin.AndroidX.Fragment.dll => 80
	i64 u0x793914ac7e9dd4f3, ; 254: MobileScanner => 104
	i64 u0x7a316882bd085c35, ; 255: ExcelNumberFormat.dll => 42
	i64 u0x7adb8da2ac89b647, ; 256: fi/Microsoft.Maui.Controls.resources.dll => 7
	i64 u0x7b2641c52a771341, ; 257: lib_Microsoft.Graph.Core.dll.so => 52
	i64 u0x7bef86a4335c4870, ; 258: System.ComponentModel.TypeConverter => 113
	i64 u0x7c0820144cd34d6a, ; 259: sk/Microsoft.Maui.Controls.resources.dll => 25
	i64 u0x7c2a0bd1e0f988fc, ; 260: lib-de-Microsoft.Maui.Controls.resources.dll.so => 4
	i64 u0x7cc637f941f716d0, ; 261: CommunityToolkit.Maui.Core => 39
	i64 u0x7d649b75d580bb42, ; 262: ms/Microsoft.Maui.Controls.resources.dll => 17
	i64 u0x7d8ee2bdc8e3aad1, ; 263: System.Numerics.Vectors => 141
	i64 u0x7dfc3d6d9d8d7b70, ; 264: System.Collections => 111
	i64 u0x7e2e564fa2f76c65, ; 265: lib_System.Diagnostics.Tracing.dll.so => 121
	i64 u0x7e302e110e1e1346, ; 266: lib_System.Security.Claims.dll.so => 156
	i64 u0x7e946809d6008ef2, ; 267: lib_System.ObjectModel.dll.so => 142
	i64 u0x7ecc13347c8fd849, ; 268: lib_System.ComponentModel.dll.so => 114
	i64 u0x7f00ddd9b9ca5a13, ; 269: Xamarin.AndroidX.ViewPager.dll => 94
	i64 u0x7f9351cd44b1273f, ; 270: Microsoft.Extensions.Configuration.Abstractions => 44
	i64 u0x7fae0ef4dc4770fe, ; 271: Microsoft.Identity.Client => 53
	i64 u0x7fbd557c99b3ce6f, ; 272: lib_Xamarin.AndroidX.Lifecycle.LiveData.Core.dll.so => 83
	i64 u0x8052dc0289c3c90a, ; 273: lib_ClosedXML.dll.so => 36
	i64 u0x812c069d5cdecc17, ; 274: System.dll => 173
	i64 u0x81ab745f6c0f5ce6, ; 275: zh-Hant/Microsoft.Maui.Controls.resources => 33
	i64 u0x8277f2be6b5ce05f, ; 276: Xamarin.AndroidX.AppCompat => 67
	i64 u0x828f06563b30bc50, ; 277: lib_Xamarin.AndroidX.CardView.dll.so => 73
	i64 u0x82df8f5532a10c59, ; 278: lib_System.Drawing.dll.so => 123
	i64 u0x82f6403342e12049, ; 279: uk/Microsoft.Maui.Controls.resources => 29
	i64 u0x83a7afd2c49adc86, ; 280: lib_Microsoft.IdentityModel.Abstractions.dll.so => 54
	i64 u0x83c14ba66c8e2b8c, ; 281: zh-Hans/Microsoft.Maui.Controls.resources => 32
	i64 u0x844ac8f64fd78edc, ; 282: Xamarin.AndroidX.Camera.View.dll => 72
	i64 u0x86a909228dc7657b, ; 283: lib-zh-Hant-Microsoft.Maui.Controls.resources.dll.so => 33
	i64 u0x86b3e00c36b84509, ; 284: Microsoft.Extensions.Configuration.dll => 43
	i64 u0x87c69b87d9283884, ; 285: lib_System.Threading.Thread.dll.so => 167
	i64 u0x87f6569b25707834, ; 286: System.IO.Compression.Brotli.dll => 125
	i64 u0x8842b3a5d2d3fb36, ; 287: Microsoft.Maui.Essentials => 58
	i64 u0x88bda98e0cffb7a9, ; 288: lib_Xamarin.KotlinX.Coroutines.Core.Jvm.dll.so => 99
	i64 u0x8930322c7bd8f768, ; 289: netstandard => 174
	i64 u0x897a606c9e39c75f, ; 290: lib_System.ComponentModel.Primitives.dll.so => 112
	i64 u0x89c5188089ec2cd5, ; 291: lib_System.Runtime.InteropServices.RuntimeInformation.dll.so => 149
	i64 u0x8ad229ea26432ee2, ; 292: Xamarin.AndroidX.Loader => 86
	i64 u0x8b4ff5d0fdd5faa1, ; 293: lib_System.Diagnostics.DiagnosticSource.dll.so => 118
	i64 u0x8b9ceca7acae3451, ; 294: lib-he-Microsoft.Maui.Controls.resources.dll.so => 9
	i64 u0x8c53ae18581b14f0, ; 295: Azure.Core => 35
	i64 u0x8d0f420977c2c1c7, ; 296: Xamarin.AndroidX.CursorAdapter.dll => 77
	i64 u0x8d7b8ab4b3310ead, ; 297: System.Threading => 168
	i64 u0x8da188285aadfe8e, ; 298: System.Collections.Concurrent => 107
	i64 u0x8e10aa836d236cb3, ; 299: RBush.dll => 60
	i64 u0x8e40b785660ff661, ; 300: lib_Microsoft.Graph.Auth.dll.so => 51
	i64 u0x8e937db395a74375, ; 301: lib_Microsoft.Identity.Client.dll.so => 53
	i64 u0x8ed807bfe9858dfc, ; 302: Xamarin.AndroidX.Navigation.Common => 87
	i64 u0x8ee08b8194a30f48, ; 303: lib-hi-Microsoft.Maui.Controls.resources.dll.so => 10
	i64 u0x8ef7601039857a44, ; 304: lib-ro-Microsoft.Maui.Controls.resources.dll.so => 23
	i64 u0x8f32c6f611f6ffab, ; 305: pt/Microsoft.Maui.Controls.resources.dll => 22
	i64 u0x8f8829d21c8985a4, ; 306: lib-pt-BR-Microsoft.Maui.Controls.resources.dll.so => 21
	i64 u0x90263f8448b8f572, ; 307: lib_System.Diagnostics.TraceSource.dll.so => 120
	i64 u0x903101b46fb73a04, ; 308: _Microsoft.Android.Resource.Designer => 34
	i64 u0x90393bd4865292f3, ; 309: lib_System.IO.Compression.dll.so => 126
	i64 u0x90634f86c5ebe2b5, ; 310: Xamarin.AndroidX.Lifecycle.ViewModel.Android => 84
	i64 u0x907b636704ad79ef, ; 311: lib_Microsoft.Maui.Controls.Xaml.dll.so => 56
	i64 u0x91418dc638b29e68, ; 312: lib_Xamarin.AndroidX.CustomView.dll.so => 78
	i64 u0x9157bd523cd7ed36, ; 313: lib_System.Text.Json.dll.so => 163
	i64 u0x91a74f07b30d37e2, ; 314: System.Linq.dll => 132
	i64 u0x91fa41a87223399f, ; 315: ca/Microsoft.Maui.Controls.resources.dll => 1
	i64 u0x9388aad9b7ae40ce, ; 316: lib_Xamarin.AndroidX.Lifecycle.Common.dll.so => 81
	i64 u0x93cfa73ab28d6e35, ; 317: ms/Microsoft.Maui.Controls.resources => 17
	i64 u0x944077d8ca3c6580, ; 318: System.IO.Compression.dll => 126
	i64 u0x95d757769563d0d3, ; 319: Xamarin.AndroidX.Camera.Lifecycle.dll => 71
	i64 u0x9656a5a4ef359a71, ; 320: Microsoft.Graph.Auth => 51
	i64 u0x967fc325e09bfa8c, ; 321: es/Microsoft.Maui.Controls.resources => 6
	i64 u0x9732d8dbddea3d9a, ; 322: id/Microsoft.Maui.Controls.resources => 13
	i64 u0x978be80e5210d31b, ; 323: Microsoft.Maui.Graphics.dll => 59
	i64 u0x97b8c771ea3e4220, ; 324: System.ComponentModel.dll => 114
	i64 u0x97e144c9d3c6976e, ; 325: System.Collections.Concurrent.dll => 107
	i64 u0x99052c1297204af4, ; 326: lib_Xamarin.AndroidX.Camera.Core.dll.so => 70
	i64 u0x991d510397f92d9d, ; 327: System.Linq.Expressions => 130
	i64 u0x99a00ca5270c6878, ; 328: Xamarin.AndroidX.Navigation.Runtime => 89
	i64 u0x99cdc6d1f2d3a72f, ; 329: ko/Microsoft.Maui.Controls.resources.dll => 16
	i64 u0x9c244ac7cda32d26, ; 330: System.Security.Cryptography.X509Certificates.dll => 157
	i64 u0x9d5dbcf5a48583fe, ; 331: lib_Xamarin.AndroidX.Activity.dll.so => 66
	i64 u0x9d74dee1a7725f34, ; 332: Microsoft.Extensions.Configuration.Abstractions.dll => 44
	i64 u0x9e4534b6adaf6e84, ; 333: nl/Microsoft.Maui.Controls.resources => 19
	i64 u0x9e4b95dec42769f7, ; 334: System.Diagnostics.Debug.dll => 117
	i64 u0x9eaf1efdf6f7267e, ; 335: Xamarin.AndroidX.Navigation.Common.dll => 87
	i64 u0x9ef542cf1f78c506, ; 336: Xamarin.AndroidX.Lifecycle.LiveData.Core => 83
	i64 u0x9ff334e3cf272fd6, ; 337: lib_Xamarin.AndroidX.Camera.Lifecycle.dll.so => 71
	i64 u0x9ffbb6b1434ad2df, ; 338: Microsoft.Identity.Client.dll => 53
	i64 u0xa0d8259f4cc284ec, ; 339: lib_System.Security.Cryptography.dll.so => 158
	i64 u0xa1440773ee9d341e, ; 340: Xamarin.Google.Android.Material => 96
	i64 u0xa1b9d7c27f47219f, ; 341: Xamarin.AndroidX.Navigation.UI.dll => 90
	i64 u0xa2572680829d2c7c, ; 342: System.IO.Pipelines.dll => 128
	i64 u0xa46aa1eaa214539b, ; 343: ko/Microsoft.Maui.Controls.resources => 16
	i64 u0xa4edc8f2ceae241a, ; 344: System.Data.Common.dll => 116
	i64 u0xa5494f40f128ce6a, ; 345: System.Runtime.Serialization.Formatters.dll => 153
	i64 u0xa5c3844f17b822db, ; 346: lib_System.Linq.Parallel.dll.so => 131
	i64 u0xa5e599d1e0524750, ; 347: System.Numerics.Vectors.dll => 141
	i64 u0xa5f1ba49b85dd355, ; 348: System.Security.Cryptography.dll => 158
	i64 u0xa67dbee13e1df9ca, ; 349: Xamarin.AndroidX.SavedState.dll => 92
	i64 u0xa68a420042bb9b1f, ; 350: Xamarin.AndroidX.DrawerLayout.dll => 79
	i64 u0xa77e30733da34712, ; 351: lib_Std.UriTemplate.dll.so => 62
	i64 u0xa78ce3745383236a, ; 352: Xamarin.AndroidX.Lifecycle.Common.Jvm => 82
	i64 u0xa7a2f0662ebff901, ; 353: Microsoft.Graph.Auth.dll => 51
	i64 u0xa7c31b56b4dc7b33, ; 354: hu/Microsoft.Maui.Controls.resources => 12
	i64 u0xa964304b5631e28a, ; 355: CommunityToolkit.Maui.Core.dll => 39
	i64 u0xaa2219c8e3449ff5, ; 356: Microsoft.Extensions.Logging.Abstractions => 48
	i64 u0xaa443ac34067eeef, ; 357: System.Private.Xml.dll => 145
	i64 u0xaa52de307ef5d1dd, ; 358: System.Net.Http => 134
	i64 u0xaaaf86367285a918, ; 359: Microsoft.Extensions.DependencyInjection.Abstractions.dll => 46
	i64 u0xaaf432d11af52d87, ; 360: Microsoft.Graph.Core.dll => 52
	i64 u0xaaf84bb3f052a265, ; 361: el/Microsoft.Maui.Controls.resources => 5
	i64 u0xab9c1b2687d86b0b, ; 362: lib_System.Linq.Expressions.dll.so => 130
	i64 u0xac2af3fa195a15ce, ; 363: System.Runtime.Numerics => 152
	i64 u0xac5376a2a538dc10, ; 364: Xamarin.AndroidX.Lifecycle.LiveData.Core.dll => 83
	i64 u0xac5acae88f60357e, ; 365: System.Diagnostics.Tools.dll => 119
	i64 u0xac98d31068e24591, ; 366: System.Xml.XDocument => 172
	i64 u0xacd46e002c3ccb97, ; 367: ro/Microsoft.Maui.Controls.resources => 23
	i64 u0xacf42eea7ef9cd12, ; 368: System.Threading.Channels => 165
	i64 u0xad89c07347f1bad6, ; 369: nl/Microsoft.Maui.Controls.resources.dll => 19
	i64 u0xadbb53caf78a79d2, ; 370: System.Web.HttpUtility => 169
	i64 u0xadc90ab061a9e6e4, ; 371: System.ComponentModel.TypeConverter.dll => 113
	i64 u0xadf511667bef3595, ; 372: System.Net.Security => 139
	i64 u0xae282bcd03739de7, ; 373: Java.Interop => 176
	i64 u0xae53579c90db1107, ; 374: System.ObjectModel.dll => 142
	i64 u0xafe29f45095518e7, ; 375: lib_Xamarin.AndroidX.Lifecycle.ViewModelSavedState.dll.so => 85
	i64 u0xb05cc42cd94c6d9d, ; 376: lib-sv-Microsoft.Maui.Controls.resources.dll.so => 26
	i64 u0xb0bb43dc52ea59f9, ; 377: System.Diagnostics.Tracing.dll => 121
	i64 u0xb220631954820169, ; 378: System.Text.RegularExpressions => 164
	i64 u0xb2a3f67f3bf29fce, ; 379: da/Microsoft.Maui.Controls.resources => 3
	i64 u0xb343b35350be6ef3, ; 380: DocumentFormat.OpenXml.Framework => 41
	i64 u0xb3f0a0fcda8d3ebc, ; 381: Xamarin.AndroidX.CardView => 73
	i64 u0xb46be1aa6d4fff93, ; 382: hi/Microsoft.Maui.Controls.resources => 10
	i64 u0xb477491be13109d8, ; 383: ar/Microsoft.Maui.Controls.resources => 0
	i64 u0xb4bd7015ecee9d86, ; 384: System.IO.Pipelines => 128
	i64 u0xb5c38bf497a4cfe2, ; 385: lib_System.Threading.Tasks.dll.so => 166
	i64 u0xb5c7fcdafbc67ee4, ; 386: Microsoft.Extensions.Logging.Abstractions.dll => 48
	i64 u0xb7212c4683a94afe, ; 387: System.Drawing.Primitives => 122
	i64 u0xb7b7753d1f319409, ; 388: sv/Microsoft.Maui.Controls.resources => 26
	i64 u0xb81a2c6e0aee50fe, ; 389: lib_System.Private.CoreLib.dll.so => 175
	i64 u0xb9185c33a1643eed, ; 390: Microsoft.CSharp.dll => 105
	i64 u0xb9f64d3b230def68, ; 391: lib-pt-Microsoft.Maui.Controls.resources.dll.so => 22
	i64 u0xb9fc3c8a556e3691, ; 392: ja/Microsoft.Maui.Controls.resources => 15
	i64 u0xba4670aa94a2b3c6, ; 393: lib_System.Xml.XDocument.dll.so => 172
	i64 u0xba48785529705af9, ; 394: System.Collections.dll => 111
	i64 u0xbb65706fde942ce3, ; 395: System.Net.Sockets => 140
	i64 u0xbb6dc0b35452c1a0, ; 396: ZXing.Net.MAUI.dll => 102
	i64 u0xbbd180354b67271a, ; 397: System.Runtime.Serialization.Formatters => 153
	i64 u0xbd0e2c0d55246576, ; 398: System.Net.Http.dll => 134
	i64 u0xbd437a2cdb333d0d, ; 399: Xamarin.AndroidX.ViewPager2 => 95
	i64 u0xbd5d0b88d3d647a5, ; 400: lib_Xamarin.AndroidX.Browser.dll.so => 69
	i64 u0xbe08e3083025c53d, ; 401: ZXing.Net.MAUI.Controls.dll => 103
	i64 u0xbe532a80075c3dc8, ; 402: Xamarin.AndroidX.Camera.Core.dll => 70
	i64 u0xbe65a49036345cf4, ; 403: lib_System.Buffers.dll.so => 106
	i64 u0xbedf4e9b29564ad3, ; 404: lib_MobileScanner.dll.so => 104
	i64 u0xbee38d4a88835966, ; 405: Xamarin.AndroidX.AppCompat.AppCompatResources => 68
	i64 u0xc040a4ab55817f58, ; 406: ar/Microsoft.Maui.Controls.resources.dll => 0
	i64 u0xc0d928351ab5ca77, ; 407: System.Console.dll => 115
	i64 u0xc12b8b3afa48329c, ; 408: lib_System.Linq.dll.so => 132
	i64 u0xc1d2d5e987094943, ; 409: ClosedXML => 36
	i64 u0xc1ff9ae3cdb6e1e6, ; 410: Xamarin.AndroidX.Activity.dll => 66
	i64 u0xc2054e3663642113, ; 411: lib_ExcelNumberFormat.dll.so => 42
	i64 u0xc26c064effb1dea9, ; 412: System.Buffers.dll => 106
	i64 u0xc28c50f32f81cc73, ; 413: ja/Microsoft.Maui.Controls.resources.dll => 15
	i64 u0xc2bcfec99f69365e, ; 414: Xamarin.AndroidX.ViewPager2.dll => 95
	i64 u0xc3f0e03e56ce7b69, ; 415: zxing => 101
	i64 u0xc4d3858ed4d08512, ; 416: Xamarin.AndroidX.Lifecycle.ViewModelSavedState.dll => 85
	i64 u0xc50fded0ded1418c, ; 417: lib_System.ComponentModel.TypeConverter.dll.so => 113
	i64 u0xc519125d6bc8fb11, ; 418: lib_System.Net.Requests.dll.so => 138
	i64 u0xc5293b19e4dc230e, ; 419: Xamarin.AndroidX.Navigation.Fragment => 88
	i64 u0xc5325b2fcb37446f, ; 420: lib_System.Private.Xml.dll.so => 145
	i64 u0xc5a0f4b95a699af7, ; 421: lib_System.Private.Uri.dll.so => 143
	i64 u0xc6c65ca6318f6fde, ; 422: lib_System.IO.Packaging.dll.so => 64
	i64 u0xc7c01e7d7c93a110, ; 423: System.Text.Encoding.Extensions.dll => 160
	i64 u0xc7ce851898a4548e, ; 424: lib_System.Web.HttpUtility.dll.so => 169
	i64 u0xc858a28d9ee5a6c5, ; 425: lib_System.Collections.Specialized.dll.so => 110
	i64 u0xc9e54b32fc19baf3, ; 426: lib_CommunityToolkit.Maui.dll.so => 38
	i64 u0xca3a723e7342c5b6, ; 427: lib-tr-Microsoft.Maui.Controls.resources.dll.so => 28
	i64 u0xca5801070d9fccfb, ; 428: System.Text.Encoding => 161
	i64 u0xcab3493c70141c2d, ; 429: pl/Microsoft.Maui.Controls.resources => 20
	i64 u0xcacfddc9f7c6de76, ; 430: ro/Microsoft.Maui.Controls.resources.dll => 23
	i64 u0xcbd4fdd9cef4a294, ; 431: lib__Microsoft.Android.Resource.Designer.dll.so => 34
	i64 u0xcc2876b32ef2794c, ; 432: lib_System.Text.RegularExpressions.dll.so => 164
	i64 u0xcc5c3bb714c4561e, ; 433: Xamarin.KotlinX.Coroutines.Core.Jvm.dll => 99
	i64 u0xcc76886e09b88260, ; 434: Xamarin.KotlinX.Serialization.Core.Jvm.dll => 100
	i64 u0xccf25c4b634ccd3a, ; 435: zh-Hans/Microsoft.Maui.Controls.resources.dll => 32
	i64 u0xcd10a42808629144, ; 436: System.Net.Requests => 138
	i64 u0xcdd0c48b6937b21c, ; 437: Xamarin.AndroidX.SwipeRefreshLayout => 93
	i64 u0xceb28d385f84f441, ; 438: Azure.Core.dll => 35
	i64 u0xcf23d8093f3ceadf, ; 439: System.Diagnostics.DiagnosticSource.dll => 118
	i64 u0xcf8fc898f98b0d34, ; 440: System.Private.Xml.Linq => 144
	i64 u0xd0fc33d5ae5d4cb8, ; 441: System.Runtime.Extensions => 148
	i64 u0xd1194e1d8a8de83c, ; 442: lib_Xamarin.AndroidX.Lifecycle.Common.Jvm.dll.so => 82
	i64 u0xd2d7ebaf4c12e35f, ; 443: lib_RBush.dll.so => 60
	i64 u0xd3144156a3727ebe, ; 444: Xamarin.Google.Guava.ListenableFuture => 97
	i64 u0xd333d0af9e423810, ; 445: System.Runtime.InteropServices => 150
	i64 u0xd3426d966bb704f5, ; 446: Xamarin.AndroidX.AppCompat.AppCompatResources.dll => 68
	i64 u0xd3651b6fc3125825, ; 447: System.Private.Uri.dll => 143
	i64 u0xd373685349b1fe8b, ; 448: Microsoft.Extensions.Logging.dll => 47
	i64 u0xd3e4c8d6a2d5d470, ; 449: it/Microsoft.Maui.Controls.resources => 14
	i64 u0xd42c5e61f624b295, ; 450: ExcelNumberFormat => 42
	i64 u0xd4645626dffec99d, ; 451: lib_Microsoft.Extensions.DependencyInjection.Abstractions.dll.so => 46
	i64 u0xd5507e11a2b2839f, ; 452: Xamarin.AndroidX.Lifecycle.ViewModelSavedState => 85
	i64 u0xd567f168deeeaf3c, ; 453: lib_zxing.dll.so => 101
	i64 u0xd63b432ec9306914, ; 454: zxing.dll => 101
	i64 u0xd6694f8359737e4e, ; 455: Xamarin.AndroidX.SavedState => 92
	i64 u0xd6d21782156bc35b, ; 456: Xamarin.AndroidX.SwipeRefreshLayout.dll => 93
	i64 u0xd72329819cbbbc44, ; 457: lib_Microsoft.Extensions.Configuration.Abstractions.dll.so => 44
	i64 u0xd753f071e44c2a03, ; 458: lib_System.Security.SecureString.dll.so => 159
	i64 u0xd7b3764ada9d341d, ; 459: lib_Microsoft.Extensions.Logging.Abstractions.dll.so => 48
	i64 u0xd9d04d95a2671e29, ; 460: lib_ZXing.Net.MAUI.Controls.dll.so => 103
	i64 u0xda1dfa4c534a9251, ; 461: Microsoft.Extensions.DependencyInjection => 45
	i64 u0xdad05a11827959a3, ; 462: System.Collections.NonGeneric.dll => 109
	i64 u0xdb5383ab5865c007, ; 463: lib-vi-Microsoft.Maui.Controls.resources.dll.so => 30
	i64 u0xdbeda89f832aa805, ; 464: vi/Microsoft.Maui.Controls.resources.dll => 30
	i64 u0xdbf9607a441b4505, ; 465: System.Linq => 132
	i64 u0xdbfc90157a0de9b0, ; 466: lib_System.Text.Encoding.dll.so => 161
	i64 u0xdce2c53525640bf3, ; 467: Microsoft.Extensions.Logging => 47
	i64 u0xdd2b722d78ef5f43, ; 468: System.Runtime.dll => 155
	i64 u0xdd67031857c72f96, ; 469: lib_System.Text.Encodings.Web.dll.so => 162
	i64 u0xdde30e6b77aa6f6c, ; 470: lib-zh-Hans-Microsoft.Maui.Controls.resources.dll.so => 32
	i64 u0xde110ae80fa7c2e2, ; 471: System.Xml.XDocument.dll => 172
	i64 u0xde8769ebda7d8647, ; 472: hr/Microsoft.Maui.Controls.resources.dll => 11
	i64 u0xdf5820c64c84eafc, ; 473: ClosedXML.Parser => 37
	i64 u0xe0142572c095a480, ; 474: Xamarin.AndroidX.AppCompat.dll => 67
	i64 u0xe021eaa401792a05, ; 475: System.Text.Encoding.dll => 161
	i64 u0xe02f89350ec78051, ; 476: Xamarin.AndroidX.CoordinatorLayout.dll => 75
	i64 u0xe192a588d4410686, ; 477: lib_System.IO.Pipelines.dll.so => 128
	i64 u0xe1a08bd3fa539e0d, ; 478: System.Runtime.Loader => 151
	i64 u0xe1a77eb8831f7741, ; 479: System.Security.SecureString.dll => 159
	i64 u0xe1b52f9f816c70ef, ; 480: System.Private.Xml.Linq.dll => 144
	i64 u0xe1ecfdb7fff86067, ; 481: System.Net.Security.dll => 139
	i64 u0xe2420585aeceb728, ; 482: System.Net.Requests.dll => 138
	i64 u0xe29b73bc11392966, ; 483: lib-id-Microsoft.Maui.Controls.resources.dll.so => 13
	i64 u0xe2ecad4b18de7d3c, ; 484: Std.UriTemplate => 62
	i64 u0xe3811d68d4fe8463, ; 485: pt-BR/Microsoft.Maui.Controls.resources.dll => 21
	i64 u0xe494f7ced4ecd10a, ; 486: hu/Microsoft.Maui.Controls.resources.dll => 12
	i64 u0xe4a9b1e40d1e8917, ; 487: lib-fi-Microsoft.Maui.Controls.resources.dll.so => 7
	i64 u0xe4f74a0b5bf9703f, ; 488: System.Runtime.Serialization.Primitives => 154
	i64 u0xe5434e8a119ceb69, ; 489: lib_Mono.Android.dll.so => 178
	i64 u0xe55703b9ce5c038a, ; 490: System.Diagnostics.Tools => 119
	i64 u0xe89a2a9ef110899b, ; 491: System.Drawing.dll => 123
	i64 u0xe975d06779bc7baf, ; 492: SixLabors.Fonts.dll => 61
	i64 u0xedc4817167106c23, ; 493: System.Net.Sockets.dll => 140
	i64 u0xedc632067fb20ff3, ; 494: System.Memory.dll => 133
	i64 u0xedc8e4ca71a02a8b, ; 495: Xamarin.AndroidX.Navigation.Runtime.dll => 89
	i64 u0xeeb7ebb80150501b, ; 496: lib_Xamarin.AndroidX.Collection.Jvm.dll.so => 74
	i64 u0xef602c523fe2e87a, ; 497: lib_Xamarin.Google.Guava.ListenableFuture.dll.so => 97
	i64 u0xef72742e1bcca27a, ; 498: Microsoft.Maui.Essentials.dll => 58
	i64 u0xefd1e0c4e5c9b371, ; 499: System.Resources.ResourceManager.dll => 146
	i64 u0xefec0b7fdc57ec42, ; 500: Xamarin.AndroidX.Activity => 66
	i64 u0xf00c29406ea45e19, ; 501: es/Microsoft.Maui.Controls.resources.dll => 6
	i64 u0xf09e47b6ae914f6e, ; 502: System.Net.NameResolution => 135
	i64 u0xf0ac2b489fed2e35, ; 503: lib_System.Diagnostics.Debug.dll.so => 117
	i64 u0xf11b621fc87b983f, ; 504: Microsoft.Maui.Controls.Xaml.dll => 56
	i64 u0xf1624296ce223787, ; 505: lib_ClosedXML.Parser.dll.so => 37
	i64 u0xf1c4b4005493d871, ; 506: System.Formats.Asn1.dll => 124
	i64 u0xf238bd79489d3a96, ; 507: lib-nl-Microsoft.Maui.Controls.resources.dll.so => 19
	i64 u0xf37221fda4ef8830, ; 508: lib_Xamarin.Google.Android.Material.dll.so => 96
	i64 u0xf3ddfe05336abf29, ; 509: System => 173
	i64 u0xf4c1dd70a5496a17, ; 510: System.IO.Compression => 126
	i64 u0xf518f63ead11fcd1, ; 511: System.Threading.Tasks => 166
	i64 u0xf6077741019d7428, ; 512: Xamarin.AndroidX.CoordinatorLayout => 75
	i64 u0xf64aa85b130b0651, ; 513: lib_DocumentFormat.OpenXml.Framework.dll.so => 41
	i64 u0xf77b20923f07c667, ; 514: de/Microsoft.Maui.Controls.resources.dll => 4
	i64 u0xf7e2cac4c45067b3, ; 515: lib_System.Numerics.Vectors.dll.so => 141
	i64 u0xf7e74930e0e3d214, ; 516: zh-HK/Microsoft.Maui.Controls.resources.dll => 31
	i64 u0xf84773b5c81e3cef, ; 517: lib-uk-Microsoft.Maui.Controls.resources.dll.so => 29
	i64 u0xf8abd63acd77d37b, ; 518: Xamarin.AndroidX.Camera.View => 72
	i64 u0xf8e045dc345b2ea3, ; 519: lib_Xamarin.AndroidX.RecyclerView.dll.so => 91
	i64 u0xf915dc29808193a1, ; 520: System.Web.HttpUtility.dll => 169
	i64 u0xf96c777a2a0686f4, ; 521: hi/Microsoft.Maui.Controls.resources.dll => 10
	i64 u0xf9eec5bb3a6aedc6, ; 522: Microsoft.Extensions.Options => 49
	i64 u0xfa3f278f288b0e84, ; 523: lib_System.Net.Security.dll.so => 139
	i64 u0xfa5ed7226d978949, ; 524: lib-ar-Microsoft.Maui.Controls.resources.dll.so => 0
	i64 u0xfa645d91e9fc4cba, ; 525: System.Threading.Thread => 167
	i64 u0xfbad3e4ce4b98145, ; 526: System.Security.Cryptography.X509Certificates => 157
	i64 u0xfbf0a31c9fc34bc4, ; 527: lib_System.Net.Http.dll.so => 134
	i64 u0xfc6b7527cc280b3f, ; 528: lib_System.Runtime.Serialization.Formatters.dll.so => 153
	i64 u0xfc719aec26adf9d9, ; 529: Xamarin.AndroidX.Navigation.Fragment.dll => 88
	i64 u0xfd22f00870e40ae0, ; 530: lib_Xamarin.AndroidX.DrawerLayout.dll.so => 79
	i64 u0xfd49b3c1a76e2748, ; 531: System.Runtime.InteropServices.RuntimeInformation => 149
	i64 u0xfd536c702f64dc47, ; 532: System.Text.Encoding.Extensions => 160
	i64 u0xfd583f7657b6a1cb, ; 533: Xamarin.AndroidX.Fragment => 80
	i64 u0xfdbe4710aa9beeff, ; 534: CommunityToolkit.Maui => 38
	i64 u0xfddbe9695626a7f5, ; 535: Xamarin.AndroidX.Lifecycle.Common => 81
	i64 u0xfeae9952cf03b8cb ; 536: tr/Microsoft.Maui.Controls.resources => 28
], align 8

@assembly_image_cache_indices = dso_local local_unnamed_addr constant [537 x i32] [
	i32 93, i32 102, i32 89, i32 39, i32 177, i32 67, i32 106, i32 24,
	i32 2, i32 30, i32 54, i32 137, i32 91, i32 111, i32 57, i32 147,
	i32 31, i32 170, i32 74, i32 24, i32 109, i32 35, i32 79, i32 49,
	i32 109, i32 65, i32 158, i32 165, i32 25, i32 100, i32 94, i32 21,
	i32 71, i32 178, i32 58, i32 159, i32 135, i32 78, i32 125, i32 41,
	i32 91, i32 69, i32 8, i32 176, i32 9, i32 46, i32 127, i32 104,
	i32 174, i32 12, i32 162, i32 100, i32 18, i32 156, i32 72, i32 107,
	i32 173, i32 27, i32 177, i32 166, i32 90, i32 16, i32 49, i32 125,
	i32 155, i32 63, i32 27, i32 40, i32 167, i32 146, i32 115, i32 76,
	i32 154, i32 8, i32 98, i32 50, i32 70, i32 129, i32 13, i32 11,
	i32 176, i32 117, i32 137, i32 29, i32 136, i32 120, i32 7, i32 164,
	i32 124, i32 33, i32 20, i32 144, i32 168, i32 26, i32 163, i32 127,
	i32 5, i32 171, i32 121, i32 80, i32 54, i32 34, i32 73, i32 122,
	i32 8, i32 171, i32 108, i32 6, i32 140, i32 57, i32 2, i32 55,
	i32 95, i32 43, i32 119, i32 148, i32 129, i32 108, i32 147, i32 78,
	i32 135, i32 94, i32 1, i32 60, i32 64, i32 36, i32 160, i32 157,
	i32 98, i32 69, i32 103, i32 97, i32 170, i32 64, i32 76, i32 87,
	i32 68, i32 146, i32 174, i32 178, i32 20, i32 52, i32 105, i32 154,
	i32 98, i32 120, i32 24, i32 170, i32 65, i32 22, i32 40, i32 142,
	i32 90, i32 148, i32 163, i32 63, i32 37, i32 86, i32 136, i32 130,
	i32 145, i32 63, i32 151, i32 14, i32 86, i32 177, i32 165, i32 1,
	i32 55, i32 131, i32 84, i32 123, i32 137, i32 116, i32 76, i32 59,
	i32 25, i32 136, i32 149, i32 31, i32 156, i32 155, i32 81, i32 82,
	i32 110, i32 143, i32 175, i32 118, i32 15, i32 45, i32 105, i32 65,
	i32 75, i32 168, i32 114, i32 3, i32 47, i32 102, i32 150, i32 74,
	i32 110, i32 162, i32 112, i32 171, i32 116, i32 5, i32 147, i32 45,
	i32 99, i32 133, i32 61, i32 129, i32 56, i32 4, i32 151, i32 175,
	i32 108, i32 96, i32 38, i32 55, i32 152, i32 115, i32 84, i32 77,
	i32 3, i32 122, i32 124, i32 9, i32 150, i32 18, i32 59, i32 50,
	i32 77, i32 50, i32 88, i32 57, i32 2, i32 127, i32 28, i32 18,
	i32 14, i32 112, i32 11, i32 40, i32 133, i32 43, i32 61, i32 92,
	i32 152, i32 62, i32 131, i32 17, i32 27, i32 80, i32 104, i32 42,
	i32 7, i32 52, i32 113, i32 25, i32 4, i32 39, i32 17, i32 141,
	i32 111, i32 121, i32 156, i32 142, i32 114, i32 94, i32 44, i32 53,
	i32 83, i32 36, i32 173, i32 33, i32 67, i32 73, i32 123, i32 29,
	i32 54, i32 32, i32 72, i32 33, i32 43, i32 167, i32 125, i32 58,
	i32 99, i32 174, i32 112, i32 149, i32 86, i32 118, i32 9, i32 35,
	i32 77, i32 168, i32 107, i32 60, i32 51, i32 53, i32 87, i32 10,
	i32 23, i32 22, i32 21, i32 120, i32 34, i32 126, i32 84, i32 56,
	i32 78, i32 163, i32 132, i32 1, i32 81, i32 17, i32 126, i32 71,
	i32 51, i32 6, i32 13, i32 59, i32 114, i32 107, i32 70, i32 130,
	i32 89, i32 16, i32 157, i32 66, i32 44, i32 19, i32 117, i32 87,
	i32 83, i32 71, i32 53, i32 158, i32 96, i32 90, i32 128, i32 16,
	i32 116, i32 153, i32 131, i32 141, i32 158, i32 92, i32 79, i32 62,
	i32 82, i32 51, i32 12, i32 39, i32 48, i32 145, i32 134, i32 46,
	i32 52, i32 5, i32 130, i32 152, i32 83, i32 119, i32 172, i32 23,
	i32 165, i32 19, i32 169, i32 113, i32 139, i32 176, i32 142, i32 85,
	i32 26, i32 121, i32 164, i32 3, i32 41, i32 73, i32 10, i32 0,
	i32 128, i32 166, i32 48, i32 122, i32 26, i32 175, i32 105, i32 22,
	i32 15, i32 172, i32 111, i32 140, i32 102, i32 153, i32 134, i32 95,
	i32 69, i32 103, i32 70, i32 106, i32 104, i32 68, i32 0, i32 115,
	i32 132, i32 36, i32 66, i32 42, i32 106, i32 15, i32 95, i32 101,
	i32 85, i32 113, i32 138, i32 88, i32 145, i32 143, i32 64, i32 160,
	i32 169, i32 110, i32 38, i32 28, i32 161, i32 20, i32 23, i32 34,
	i32 164, i32 99, i32 100, i32 32, i32 138, i32 93, i32 35, i32 118,
	i32 144, i32 148, i32 82, i32 60, i32 97, i32 150, i32 68, i32 143,
	i32 47, i32 14, i32 42, i32 46, i32 85, i32 101, i32 101, i32 92,
	i32 93, i32 44, i32 159, i32 48, i32 103, i32 45, i32 109, i32 30,
	i32 30, i32 132, i32 161, i32 47, i32 155, i32 162, i32 32, i32 172,
	i32 11, i32 37, i32 67, i32 161, i32 75, i32 128, i32 151, i32 159,
	i32 144, i32 139, i32 138, i32 13, i32 62, i32 21, i32 12, i32 7,
	i32 154, i32 178, i32 119, i32 123, i32 61, i32 140, i32 133, i32 89,
	i32 74, i32 97, i32 58, i32 146, i32 66, i32 6, i32 135, i32 117,
	i32 56, i32 37, i32 124, i32 19, i32 96, i32 173, i32 126, i32 166,
	i32 75, i32 41, i32 4, i32 141, i32 31, i32 29, i32 72, i32 91,
	i32 169, i32 10, i32 49, i32 139, i32 0, i32 167, i32 157, i32 134,
	i32 153, i32 88, i32 79, i32 149, i32 160, i32 80, i32 38, i32 81,
	i32 28
], align 4

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
@.str.0 = private unnamed_addr constant [40 x i8] c"get_function_pointer MUST be specified\0A\00", align 1

;MarshalMethodName
@.MarshalMethodName.0_name = private unnamed_addr constant [1 x i8] c"\00", align 1

; External functions

; Function attributes: noreturn "no-trapping-math"="true" nounwind "stack-protector-buffer-size"="8"
declare void @abort() local_unnamed_addr #2

; Function attributes: nofree nounwind
declare noundef i32 @puts(ptr noundef) local_unnamed_addr #1
attributes #0 = { memory(write, argmem: none, inaccessiblemem: none) "min-legal-vector-width"="0" mustprogress nofree norecurse nosync "no-trapping-math"="true" nounwind "stack-protector-buffer-size"="8" "target-cpu"="generic" "target-features"="+fix-cortex-a53-835769,+neon,+outline-atomics,+v8a" uwtable willreturn }
attributes #1 = { nofree nounwind }
attributes #2 = { noreturn "no-trapping-math"="true" nounwind "stack-protector-buffer-size"="8" "target-cpu"="generic" "target-features"="+fix-cortex-a53-835769,+neon,+outline-atomics,+v8a" }

; Metadata
!llvm.module.flags = !{!0, !1, !7, !8, !9, !10}
!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"PIC Level", i32 2}
!llvm.ident = !{!2}
!2 = !{!".NET for Android remotes/origin/release/9.0.1xx @ be1cab92326783479054e72990da08008e5be819"}
!3 = !{!4, !4, i64 0}
!4 = !{!"any pointer", !5, i64 0}
!5 = !{!"omnipotent char", !6, i64 0}
!6 = !{!"Simple C++ TBAA"}
!7 = !{i32 1, !"branch-target-enforcement", i32 0}
!8 = !{i32 1, !"sign-return-address", i32 0}
!9 = !{i32 1, !"sign-return-address-all", i32 0}
!10 = !{i32 1, !"sign-return-address-with-bkey", i32 0}
