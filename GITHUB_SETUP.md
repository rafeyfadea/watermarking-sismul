# Push Repository ke GitHub

Ikuti langkah berikut untuk mengunggah repository ini ke GitHub.

## Langkah 1: Buat Repository di GitHub

1. Buka https://github.com/new
2. Isi form:
   - **Repository name**: `watermark-sismul-dct`
   - **Description**: DCT-based invisible image watermarking library for JPEG robustness evaluation
   - **Visibility**: Pilih **Public** untuk membuat public repository
   - **DO NOT** initialize dengan README (sudah ada)
   - **DO NOT** add .gitignore (sudah ada)
   - **DO NOT** add license (sudah ada)
3. Klik **Create repository**

## Langkah 2: Add Remote dan Push

Setelah membuat repository, GitHub akan menampilkan perintah. Jalankan:

```bash
cd /Users/danesha/watermarking-sismul/watermark-sismul-dct

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/watermark-sismul-dct.git

# Rename branch ke main (jika perlu)
git branch -M main

# Push ke GitHub
git push -u origin main
```

**Ganti `YOUR_USERNAME` dengan username GitHub Anda.**

## Langkah 3: Update URL di setup.py

Edit `setup.py` dan ganti:
```python
url="https://github.com/yourusername/watermark-sismul-dct",
```

Dengan URL repository Anda yang sebenarnya.

## Langkah 4: Verify

1. Buka https://github.com/YOUR_USERNAME/watermark-sismul-dct
2. Pastikan semua file sudah ter-upload
3. Verifikasi README menampilkan dengan baik

## Tambahan: Add SSH Key (Optional tapi recommended)

Untuk push tanpa password setiap kali:

```bash
# Generate SSH key (jika belum punya)
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add key ke ssh-agent
ssh-add ~/.ssh/id_ed25519

# Copy public key (untuk ditambahkan ke GitHub)
cat ~/.ssh/id_ed25519.pub
```

Tambahkan public key di: https://github.com/settings/keys

Lalu gunakan SSH URL saat menambahkan remote:
```bash
git remote add origin git@github.com:YOUR_USERNAME/watermark-sismul-dct.git
```

## Troubleshooting

### Error: "fatal: A branch named 'main' does not exist"
```bash
git checkout -b main
git push -u origin main
```

### Error: "fatal: The current branch has no upstream branch"
```bash
git push -u origin main
```

### Error: "Authentication failed"
- Pastikan credentials GitHub sudah benar
- Atau gunakan SSH key sebagai alternatif

---

Setelah repository terupload, repository siap untuk:
- ✅ Dibagikan ke GitHub
- ✅ Di-install via pip (setup.py sudah siap)
- ✅ Dikembangkan lebih lanjut
- ✅ Dikontribusikan ke komunitas
