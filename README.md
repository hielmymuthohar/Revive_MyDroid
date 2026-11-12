# 🚗 ReviveMyDroid

**Ubah HP atau tablet Android lama Anda menjadi Head Unit Android Auto yang ringan, cepat, dan 100% Tanpa Root.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![ADB](https://img.shields.io/badge/Requires-ADB%20(Tanpa%20Root)-orange.svg)]()

Punya HP Android lama dengan RAM 2GB yang tersimpan di laci? Daripada menjadi limbah elektronik (*e-waste*), **ReviveMyDroid** menghapus *bloatware* bawaan pabrik, mengoptimalkan animasi serta konsumsi daya via ADB, dan menyulap perangkat lama Anda menjadi **Receiver Layar Android Auto Wireless / USB** yang ditenagai oleh [Open Headunit](https://github.com/andreknieriem/open-headunit).

---

## ✨ Fitur Utama

- **🧹 Non-Root Debloater Multi-Merk:** Daftar kurasi *bloatware* untuk **Google Universal**, **Samsung**, **Xiaomi (MIUI/HyperOS)**, **Oppo/Realme (ColorOS/RealmeUI)**, **Vivo (FuntouchOS)**, dan **Asus (ZenUI)**.
- **🗑️ Pembersih Aplikasi Pihak Ketiga (User Apps):** Pindai dan bersihkan sisa aplikasi yang pernah diinstal (medsos, game, belanja) dalam 1 klik (`[A]`) atau pilih nomor tertentu, lengkap dengan backup otomatis untuk *rollback*.
- **🛡️ Aman & Bisa Dikembalikan (Automatic Rollback):** Pilih antara `disable-user` (bekukan) atau `uninstall --user 0`. Setiap sesi menghasilkan log pencadangan JSON di folder `backups/` sehingga aplikasi yang dihapus bisa dipulihkan kapan saja dengan 1 klik.
- **⚡ Optimasi Head Unit Rendah RAM:** Otomatis mematikan animasi antarmuka (`0.0x`), mengaktifkan **Layar Tetap Menyala saat Mengisi Daya** (Stay Awake AC/USB/Wireless), menonaktifkan *lockscreen*, dan membersihkan *cache* sistem.
- **📱 Unduh & Pasang Open Headunit Otomatis:** Mengambil rilis `.apk` resmi terbaru langsung dari repositori [`andreknieriem/open-headunit`](https://github.com/andreknieriem/open-headunit) via GitHub API dan memasangnya melalui ADB.
- **⚙️ Konfigurasi Head Unit Otomatis (Tanpa Root):** Otomatis menyalakan & membuka kunci layar, memberikan izin sistem (`pm grant` + overlay `appops`), serta mengatur konfigurasi optimal **Resolusi (720p/480p)**, **Frame Rate (30 FPS)**, **Hardware Codec (H.264)**, dan **Audio Sink** agar lancar di HP dengan RAM 2GB.
- **🚗 Modifikasi Dasbor Mobil Lanjutan:** Nyala otomatis saat kontak mobil ON (*Auto-Power On on Charge*), Kiosk Mode (Open Headunit sebagai launcher permanen), DPI layar besar untuk kemudahan sentuh saat mengemudi, *downscale* resolusi 720p, mode gelap anti-silau, serta proteksi baterai dan suhu kabin mobil.
- **📦 Tanpa Ketergantungan Eksternal:** Ditulis murni menggunakan pustaka standar Python 3 bawaan. Tidak perlu menjalankan `pip install`!

---

## 🎯 Pengaturan Otomatis Performa Rendah RAM

ReviveMyDroid menerapkan konfigurasi baku optimal yang dirancang khusus untuk HP penerima dengan RAM 2GB:

| Pengaturan | Nilai Baku | Mengapa Ini Penting? |
| :--- | :--- | :--- |
| **Resolusi** | **720p (1280x720)** atau **480p** | Mencegah *thermal throttling*, video tersendat, dan kehabisan memori GPU/RAM pada chipset lama (menghindari beban berat 1080p). |
| **Frame Rate** | **30 FPS** | Mengurangi beban pemrosesan *decode* video hingga 50% dibanding 60 FPS, namun navigasi peta dan teks tetap terbaca sangat mulus. |
| **Video Codec** | **Hardware (H.264)** | Memanfaatkan chip akselerator grafis bawaan HP secara langsung tanpa membebani prosesor (CPU) yang lemah. |
| **Audio Sink** | **Nonaktif (Opsional)** | Menghilangkan beban transmisi suara di jalur nirkabel dengan mengalirkan audio musik/panggilan langsung dari HP utama ke Bluetooth mobil. |

---

## 🚀 Panduan Mulai Cepat

### 📱 Persiapan HP (Wajib Dilakukan Sebelum Menjalankan Alat)

Sebelum menjalankan ReviveMyDroid (baik lewat skrip manual maupun AI Coding Agent), aktifkan pengaturan berikut di HP lama Anda:

1. **Aktifkan Opsi Pengembang (Developer Options):**
   - Buka **Pengaturan (Settings)** $\to$ **Tentang Ponsel (About Phone)**.
   - Ketuk **Nomor Bentukan (Build Number)** atau **Versi MIUI** sebanyak **7 kali** sampai muncul pesan *"Anda sekarang adalah seorang pengembang!"*.
2. **Aktifkan USB Debugging:**
   - Masuk ke **Pengaturan** $\to$ **Opsi Pengembang (Developer Options)** (biasanya ada di menu *Sistem* atau *Setelan Tambahan*).
   - Aktifkan toggle **USB Debugging**.
3. **Aktifkan "Install via USB" (Sangat Penting untuk Xiaomi/MIUI, Oppo, Realme):**
   - Di dalam menu **Opsi Pengembang**, aktifkan toggle **"Install via USB"** (dan *"USB debugging (Security settings)"* jika tersedia).
   - *Tujuannya:* Mencegah sistem keamanan HP memblokir instalasi aplikasi otomatis melalui ADB (`INSTALL_FAILED_USER_RESTRICTED`).
4. **Hubungkan Kabel & Izinkan Akses Komputer:**
   - Hubungkan HP ke komputer menggunakan kabel data USB yang berkualitas baik.
   - Saat pop-up perizinan muncul di layar HP (*"Izinkan USB Debugging?"*), centang **"Selalu izinkan dari komputer ini"** lalu ketuk **Izinkan / OK**.

---

### Cara A: Menjalankan Skrip Interaktif (Manual)

1. **Clone repositori ini:**
   ```bash
   git clone https://github.com/hielmymuthohar/Revive_MyDroid.git
   cd Revive_MyDroid
   ```
2. **Jalankan Alat:**
   - **Windows:** Klik dua kali file `run_windows.bat` (atau jalankan `python revive.py` di terminal).
   - **Linux / macOS:** Jalankan `./run_unix.sh`.

---

### Cara B: Setup Otomatis via AI Coding Agent (Tinggal Terima Beres 🤖)

Jika Anda tidak ingin mengetik perintah atau memilih menu satu per satu, cukup sambungkan HP ke komputer via USB dan salin teks perintah (*prompt*) di bawah ini ke **AI Coding Agent** Anda (misalnya Antigravity, Claude Code, Cursor, atau Windsurf):

#### 📋 Template Prompt AI Agent:
```text
Tolong ubah perangkat Android lama saya yang terhubung ini menjadi Head Unit Android Auto menggunakan repositori berikut:
https://github.com/hielmymuthohar/Revive_MyDroid

HP saya sudah terhubung via USB dengan Developer Options, USB Debugging, dan "Install via USB" aktif. Tolong lakukan seluruh proses setup secara otomatis dari awal sampai akhir:
1. Periksa koneksi ADB (adb devices). Jika platform-tools belum ada di PC, unduh secara lokal.
2. Deteksi merek/model perangkat dan jalankan pembersihan bloatware (debloat) yang aman untuk melegakan RAM.
3. Terapkan penyesuaian sistem head unit (matikan animasi ke 0.0x, buat layar tetap menyala saat dicas, dan nonaktifkan lockscreen).
4. Unduh rilis resmi APK Open Headunit terbaru dari GitHub dan pasang ke perangkat via ADB.
5. Jalankan konfigurasi otomatis: berikan izin sistem, kunci resolusi di 720p @ 30 FPS, pilih codec Hardware H.264, dan atur audio sink.
6. Beri tahu saya jika seluruh proses telah selesai dan siap digunakan di mobil.
```

---

## 🧹 Aturan Debloat & Pembersih Aplikasi

ReviveMyDroid menggunakan sistem pembersihan dua lapis untuk membebaskan ruang RAM sebesar mungkin:

### 1. Profil Bloatware Sistem & Pabrikan (OEM)
Daftar kurasi paket sistem yang aman dihapus tanpa merusak fungsi inti Android:
- **Google Universal:** YouTube, Chrome, Google App, Docs, Digital Wellbeing, Talkback, Layanan Cetak, dll.
- **Samsung (OneUI / TouchWiz):** Bixby, Samsung Pay, AR Zone, Game Launcher, Dex, Samsung Cloud, dll.
- **Xiaomi (MIUI / HyperOS):** Mi Browser, Mi Video, Mi Pay, Layanan Iklan (`msa`), Joyose, Layanan Cloud, Cleaner, Layanan Cuaca, dll.
- **Oppo / Realme (ColorOS / RealmeUI):** HeyTap, Theme Store, Game Space, Roaming, Browser bawaan, dll.
- **Vivo (FuntouchOS / OriginOS):** V-Appstore, iManager, Vivo Cloud, Jovi, Game Center, dll.
- **Asus (ZenUI):** Asus Support, ZenUI Services, Mobile Manager, dll.

### 2. Pembersih Aplikasi Pihak Ketiga (Aplikasi yang Pernah Diinstal Pengguna)
Sebelum dijadikan layar mobil, sisa aplikasi lama (game, media sosial, e-commerce) sering kali berjalan diam-diam di latar belakang:
- **Deteksi Otomatis:** Memindai seluruh aplikasi non-sistem (`pm list packages -3`).
- **Proteksi Aplikasi Penting:** Paket penting seperti Open Headunit (`com.andrerinas.headunitrevived`) otomatis dilindungi dari penghapusan.
- **Fleksibel:** Ketik `A` untuk menghapus seluruh aplikasi pihak ketiga sekaligus agar HP bersih seperti baru, atau pilih nomor tertentu (contoh: `1,3,5`).
- **Metode Non-Root:** Pilihan antara `disable-user` (membekukan aplikasi) atau `uninstall --user 0` (menghapus aplikasi dan *cache*).

---

## 🚗 Modifikasi Dasbor Mobil Lanjutan (Menu Opsi [6])

Sempurnakan HP head unit Anda dengan fitur integrasi kendaraan yang dirancang khusus:

| Modifikasi | Perintah / Teknologi | Manfaat Nyata di Kendaraan |
| :--- | :--- | :--- |
| **🔑 Auto-Power On on Charge** | `fastboot oem off-mode-charge 0` / Qualcomm props | HP menyala otomatis begitu kontak mobil ON (menerima arus daya 5V USB) — tidak perlu lagi menekan tombol power fisik! |
| **🖥️ Kiosk Mode Permanen** | `cmd package set-home-activity` | Mengunci Open Headunit sebagai launcher permanen (Home App). HP tidak akan pernah menampilkan layar desktop atau wallpaper bawaan. |
| **👁️ Tombol Menu Besar (DPI 160)** | `wm density 160` (Dapat disesuaikan) | Memperbesar tampilan Google Maps, Spotify, dan tombol telepon agar jauh lebih mudah dan aman disentuh saat menyetir. |
| **📉 Native 720p Display Downscaling** | `wm size 720x...` | Merender seluruh sistem Android pada resolusi 720p asli, mengurangi beban memori GPU, dan menjaga HP tetap dingin di bawah terik matahari. |
| **🌙 Mode Gelap Anti-Silau** | `cmd uimode night yes` | Tampilan dasbor kontras tinggi bernuansa gelap yang nyaman di mata, tidak menyilaukan kabin di malam hari, dan menghemat baterai. |
| **🛡️ Proteksi Baterai & Suhu Kabin** | `settings put system screen_off_timeout 15000` | Layar terus menyala selama mobil berjalan (mengisi daya), namun langsung mati dalam 15 detik dan masuk mode tidur begitu mesin mobil dimatikan. |

---

## ⏪ Cara Mengembalikan Aplikasi & Pengaturan (Restore / Rollback)

Semua tindakan yang dilakukan oleh ReviveMyDroid **100% aman dan dapat dikembalikan seperti semula tanpa perlu factory reset atau flash ulang**.

### Mengembalikan Aplikasi yang Terhapus
Setiap sesi pembersihan secara otomatis menyimpan catatan cadangan berformat JSON di folder `backups/` (contoh: `rollback_Redmi_8A_Pro_20261111_233510.json`).

1. Hubungkan HP ke komputer via USB dan jalankan ReviveMyDroid.
2. Dari Menu Utama, pilih:
   ```text
   [7] ⏪ Restore / Rollback Debloated Packages from Backup
   ```
3. Masukkan nomor cadangan yang ingin dipulihkan.
4. Aplikasi akan langsung terpasang kembali secara instan menggunakan perintah bawaan Android `cmd package install-existing <pkg>` dan `pm enable <pkg>` — **tanpa perlu koneksi internet atau download ulang APK!**

### Mengembalikan Pengaturan Tampilan & Animasi Pabrik
Jika Anda ingin mengembalikan animasi layar ke normal, menyalakan kembali *lockscreen*, atau mengembalikan resolusi asli:
1. Pilih opsi **`[8] 🔄 Revert System & Display Tweaks to Factory Defaults`** pada Menu Utama.
2. Animasi jendela akan dikembalikan ke `1.0x`, *lockscreen* diaktifkan kembali, batas waktu layar disetel ke 60 detik, dan resolusi/DPI layar di-reset ke setelan pabrik.

---

## 📡 Panduan Koneksi Wireless Android Auto (Native Mode)

Setelah perangkat head unit Anda disiapkan menggunakan ReviveMyDroid, menghubungkan HP harian Anda secara nirkabel melalui **Native Mode (Wi-Fi Direct)** sangatlah mudah, otomatis, dan berlaku universal untuk semua merek smartphone (Samsung, Xiaomi, Vivo, Oppo, Google Pixel, dll).

Native Mode bekerja persis seperti head unit mobil bawaan pabrik: proses jabat tangan (*handshake*) awal dimulai otomatis lewat **Bluetooth**, kemudian Open Headunit otomatis mengalirkan data layar melalui **Wi-Fi Direct**.

### 🔹 Tahap 1: Hubungkan Bluetooth Kedua HP (Cukup Sekali di Awal)
1. **Nyalakan Bluetooth & Wi-Fi** di kedua smartphone (**HP Utama** dan **HP Headunit**).
2. Di **HP Utama**, buka menu Bluetooth $\to$ cari nama Bluetooth **HP Headunit** $\to$ lakukan penyandingan (*Pairing*) hingga keduanya saling terhubung.
3. Di **HP Headunit**, buka aplikasi **Open Headunit**:
   - Masuk ke **Settings** $\to$ **Wireless Connection**.
   - Pada menu **"Bluetooth your phone pairs with"**, pilih nama Bluetooth dari **HP Utama** Anda.

### 🔹 Tahap 2: Memulai Proyeksi Android Auto (Otomatis)
1. Buka aplikasi **Open Headunit** di HP Headunit (biarkan berada di layar utama / mode siaga).
2. Pastikan koneksi Bluetooth antara **HP Utama** dan **HP Headunit** terhubung.
3. **Konfirmasi Sambungan Layar (Hanya di sesi pertama):**
   - Di layar **HP Utama**, sistem Android Auto akan otomatis memunculkan notifikasi atau jendela persetujuan koneksi Wi-Fi Direct / Android Auto.
   - Ketuk tombol **Setujui / Hubungkan (Connect)** di HP Utama.
4. **Selesai:** Jalur data otomatis berpindah ke Wi-Fi Direct berkecepatan tinggi, dan antarmuka native Android Auto akan langsung terpampang di layar HP Headunit Anda!

### 💡 Tips Penting Agar Koneksi Stabil & Tidak Putus-Putus:
- **Matikan "Asisten Jaringan" / "Peralihan Pintar" di HP Utama:** Karena Wi-Fi Direct ke headunit tidak menyediakan akses internet keluar, sistem smartphone sering kali mencoba memutus Wi-Fi secara sepihak untuk kembali ke data seluler (4G/5G). Masuk ke Pengaturan Wi-Fi di HP Utama $\to$ matikan fitur *Asisten Wi-Fi*, *Beralih ke data seluler otomatis*, atau *Akselerasi jaringan*.
- **Matikan Pemindaian Latar Belakang di Kedua HP:** Buka **Pengaturan $\to$ Lokasi $\to$ Pemindaian Wi-Fi dan Bluetooth**, lalu ubah **Pemindaian Wi-Fi** dan **Pemindaian Bluetooth** ke **NONAKTIF (OFF)** agar antena tidak melompat frekuensi (*channel hop*) setiap 20 detik saat navigasi berjalan.
- **Persetujuan "Wi-Fi Tanpa Internet":** Jika di HP Utama muncul pop-up notifikasi *"Wi-Fi ini tidak menyediakan internet. Tetap terhubung?"*, ketuk **"Ya / Tetap Terhubung"** dan centang **"Jangan tanya lagi"**.
