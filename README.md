# >_ DATA SPACE

<p align="center">
  <img src="https://github.com/Oenm176/dataspace/blob/d001f2ccad96c921cb1cf9c2c123d8750e6d53e3/15364605_5607654.jpg" alt="DataSpace Banner" width="100%">
</p>

![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-000000?style=for-the-badge&logo=tailwind-css&logoColor=38B2AC)
![Python](https://img.shields.io/badge/Python-000000?style=for-the-badge&logo=python&logoColor=FFD43B)

**Eksplorasi Data Science.** Katalog dataset dan eksperimen open-source. Dibangun untuk merekam perjalanan riset, membagikan insight, dan membangun masa depan berbasis data.

🌐 **[Kunjungi Website DataSpace](https://oenm176.github.io/dataspace)** 

---

## 📂 Struktur Repositori

Repositori ini menggunakan pendekatan *monorepo* yang memisahkan antara data mentah/eksperimen dengan kode antarmuka (website).

```text
dataspace/
│
├── 📁 datasets/                # Pusat arsip data mentah & eksperimen
│   ├── 📁 text-mining/         # Skrip Python, Jupyter Notebook, dan CSV
│   └── 📁 computer-vision/     # Dataset gambar dan model (via Git LFS / Link eksternal)
│
└── 📁 website/                 # Kode sumber antarmuka web (Next.js)
    ├── 📁 src/app/             # Routing halaman (Home, Katalog, dll)
    └── 📁 src/components/      # Komponen UI (Navbar, Footer, Cards)
