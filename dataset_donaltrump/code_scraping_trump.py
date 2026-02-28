import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

def scrape_kompas_tag_robust(base_url, max_pages=100):
    print(f"Mulai menyedot halaman tag dari: {base_url}\n")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    all_links = []
    page = 1
    
    # TAHAP 1: Menyusuri Halaman Paginasi dengan Timeout
    while page <= max_pages:
        print(f"Mencari link di Halaman {page}...")
        page_url = f"{base_url}?page={page}"
        
        # Coba maksimal 3 kali kalau nyangkut
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # TAMBAHAN KRUSIAL: timeout=10. Jika 10 detik Kompas tidak merespons, batalkan!
                response = requests.get(page_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    break # Berhasil, keluar dari loop percobaan
                else:
                    print(f"  -> Ditolak server (Status: {response.status_code}). Percobaan {attempt+1}/{max_retries}")
                    time.sleep(3) # Tunggu 3 detik sebelum coba lagi
                    
            except requests.exceptions.Timeout:
                print(f"  -> Server nyangkut/Timeout! Percobaan {attempt+1}/{max_retries}")
                time.sleep(3)
            except Exception as e:
                print(f"  -> Error lain: {e}")
                break
        else:
            print(f"Halaman {page} gagal total setelah {max_retries} kali percobaan. Lewati halaman ini.")
            soup = None # Gagal dapat HTML

        new_links_found = 0
        
        if soup:
            for a_tag in soup.find_all('a', href=True):
                link = a_tag['href']
                if '.kompas.com/read/' in link:
                    title = a_tag.text.strip()
                    title = " ".join(title.split())
                    
                    if title and len(title) > 20:
                        if not any(d['url'] == link for d in all_links):
                            all_links.append({'title': title, 'url': link})
                            new_links_found += 1
                            
        # Logika anti-berhenti prematur:
        # Jika halaman kosong, kita tidak langsung BREAK, tapi continue ke halaman selanjutnya
        # Siapa tahu hanya halaman 14 yang error, tapi halaman 15 ada isinya.
        if new_links_found == 0 and soup is not None:
             print("  -> Tidak ada artikel baru di halaman ini.")
             # Hapus kata 'break' di sini agar dia lanjut mencari ke halaman berikutnya
             
        page += 1
        time.sleep(2) # Saya naikkan jedanya jadi 2 detik agar lebih aman dari blokir

    print(f"\nTOTAL ARTIKEL DITEMUKAN: {len(all_links)}\n")
    
    if not all_links:
        return pd.DataFrame()

    # TAHAP 2: Scraping Konten Teks & AUTO-SAVE
    news_data = []
    file_name = 'berita_kompas_trump.csv'
    
    for i, item in enumerate(all_links, start=1): 
        print(f"Mengambil konten [{i}/{len(all_links)}]: {item['title'][:40]}...")
        try:
            # Tambahkan timeout 10 detik juga di sini
            res = requests.get(item['url'], headers=headers, timeout=10)
            art_soup = BeautifulSoup(res.text, 'html.parser')
            
            body = art_soup.find('div', class_='read__content')
            
            if body:
                paragraphs = body.find_all('p')
                content_list = [p.text.strip() for p in paragraphs if p.text.strip() and "Baca juga" not in p.text]
                item['content'] = " ".join(content_list)
            else:
                item['content'] = "Struktur teks konten tidak ditemukan."
                
            news_data.append(item)
            
            # --- FITUR AUTO SAVE ---
            # Setiap kelipatan 10 artikel, langsung simpan (timpa) ke CSV
            if i % 10 == 0:
                pd.DataFrame(news_data).to_csv(file_name, index=False, encoding='utf-8')
                print("  [Auto-Save: Data diamankan]")
                
            time.sleep(2) # Jeda aman 2 detik
            
        except Exception as e:
            print(f"Error scraping konten {item['url']}: {e}")

    # Simpan sisanya di akhir
    df_final = pd.DataFrame(news_data)
    df_final.to_csv(file_name, index=False, encoding='utf-8')
    return df_final

# --- Eksekusi Kode ---
url_target = "https://www.kompas.com/tag/donald-trump"
batas_halaman = 555 

print(f"\nMEMULAI PROSES SCRAPING {batas_halaman} HALAMAN...")
df_hasil = scrape_kompas_tag_robust(url_target, max_pages=batas_halaman)

print("\nSukses! Semua data telah diamankan ke file 'berita_kompas_trump.csv'")