import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_kompas_lipsus_full(base_url):
    print(f"Mulai menyedot SELURUH halaman dari: {base_url}\n")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    all_links = []
    page = 1
    
    # TAHAP 1: Menyusuri Semua Halaman (Paginasi)
    while True:
        print(f"Mencari link di Halaman {page}...")
        
        # Menambahkan parameter ?page= ke URL
        page_url = f"{base_url}?page={page}"
        
        try:
            response = requests.get(page_url, headers=headers)
            if response.status_code != 200:
                print(f"Halaman {page} gagal diakses. Berhenti mencari halaman baru.")
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"Error koneksi di halaman {page}: {e}")
            break

        new_links_found = 0
        
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            
            if 'tekno.kompas.com/read/' in link:
                title = a_tag.text.strip()
                title = " ".join(title.split())
                
                if title and len(title) > 20:
                    # Memastikan link belum ada di dalam list (mencegah duplikat)
                    if not any(d['url'] == link for d in all_links):
                        all_links.append({'title': title, 'url': link})
                        new_links_found += 1
                        
        # Logika Berhenti: Jika di halaman ini tidak ada link berita baru, 
        # berarti kita sudah mencapai halaman paling akhir.
        if new_links_found == 0:
            print("-> Tidak ada artikel baru lagi. Paginasi selesai!\n")
            break
            
        page += 1
        time.sleep(1) # Jeda sopan antar halaman

    print(f"TOTAL ARTIKEL DITEMUKAN: {len(all_links)}\n")
    
    if not all_links:
        return pd.DataFrame()

    # TAHAP 2: Scraping Konten Teks (Tanpa Limit)
    news_data = []
    
    # Perhatikan: limit [:5] sudah saya hapus. Dia akan mengambil SEMUANYA.
    for i, item in enumerate(all_links, start=1): 
        print(f"Mengambil konten [{i}/{len(all_links)}]: {item['title'][:40]}...")
        try:
            res = requests.get(item['url'], headers=headers)
            art_soup = BeautifulSoup(res.text, 'html.parser')
            
            body = art_soup.find('div', class_='read__content')
            
            if body:
                paragraphs = body.find_all('p')
                content_list = [p.text.strip() for p in paragraphs if p.text.strip() and "Baca juga" not in p.text]
                item['content'] = " ".join(content_list)
            else:
                item['content'] = "Struktur teks konten tidak ditemukan."
                
            news_data.append(item)
            time.sleep(1.5) # Jeda agar tidak diblokir karena menyedot terlalu banyak
            
        except Exception as e:
            print(f"Error scraping konten {item['url']}: {e}")

    return pd.DataFrame(news_data)

# --- Eksekusi Kode ---
url_target = "https://tekno.kompas.com/lipsus/9981/Galaxy.Unpacked.2026"
df_hasil = scrape_kompas_lipsus_full(url_target)

print("\n=== Preview Data ===")
print(df_hasil.head())

# Wajib diaktifkan untuk tugasmu: Menyimpan hasil ke file CSV
df_hasil.to_csv('berita_kompas_galaxy2026.csv', index=False, encoding='utf-8')
print("\nSukses! Semua data telah disimpan ke dalam file 'berita_kompas_galaxy2026.csv'")