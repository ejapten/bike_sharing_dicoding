Menjalankan Dashboard Bike sharing

- Setup-Environment-Anaconda
  conda create --name main-ds python=3.9
  conda activate main-ds
  pip install -r requirements.txt

- Setup-Environment-Terminal
  mkdir proyek_analisis_data
  cd proyek_analisis_data
  pipenv install
  pipenv shell
  pip install -r requirements.txt

- Run streamlit App
  streamlit run dashboard.py

---

Cara yang saya mengerti

1. Pastikan package streamlit sudah terinstall
2. Download file zip proyek_analisis_data
3. Ekstraks file zip
4. Buka cmd/terminal
5. jalankan perintah cd path/to/proyek_analisis_data dimana path tersebeut menuji file proyek_analisis_data
6. jika sudah di folder proyek_analisis_data jalankan

- python -m venv venv
- source venv/bin/activate (kode untuk linux)
- venv\Scripts\activate (kode untuk windows)

7. jalankan pip install -r requirements.txt
8. jalankan streamlit run dashboard/dashboard.py
