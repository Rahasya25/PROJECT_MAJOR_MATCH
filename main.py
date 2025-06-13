import csv
import os
import pandas as pd
from datetime import datetime
import time

def LaunchPage():
    os.system("cls")
    print(''' 
╔════════════════════════════════════════════════════════════════════════════╗
║                    ✧･ﾟ: *✧･ﾟ:*  SELAMAT DATANG  *:･ﾟ✧*:･ﾟ✧                  ║
║                                                                            ║
║                            ░▒▓█►  DI  ◄█▓▒░                                ║
║                                                                            ║
║                            🎓  ⱮɑᴊօɾⱮɑեϲհ  🎓                             ║
║                                                                            ║
║       🔎 Sistem Rekomendasi Jurusan Berdasarkan MBTI & Nilai Akademik      ║
╚════════════════════════════════════════════════════════════════════════════╝
''')
    input("\nTekan Enter untuk lanjut...")


def login():
    os.system("cls")
    global Username
    print('╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗')
    print('║                                                                  LOGIN                                                                  ║')
    print('╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝')
    akun = pd.read_csv('daftar_pengguna.csv')
    Username = input('👤 Username: ').strip().lower()
    password = input('🔑 Password: ').strip().lower()

    if Username == "admin" and password == "admin123":
        os.system("cls")
        print("Selamat datang Admin!".center(150))
        time.sleep(1)
        menu_admin()
    elif Username in akun['Username'].values:
        pass_benar = akun.loc[akun['Username'] == Username, 'Password'].values[0]
        if password == pass_benar:
            print(f"Selamat datang, {Username}!")
            input("Tekan Enter untuk lanjut...")
            menu_user()
        else:
            print("Password salah.")
            input("Coba lagi...")
    else:
        print("Username tidak ditemukan.")
        input("Coba lagi...")

def buat_akun():
    os.system('cls')
    pengguna = pd.read_csv('daftar_pengguna.csv')
    print('=== BUAT AKUN BARU ===')
    while True: 
        username = input('Username: ').strip().lower()
        if username in pengguna['Username'].values:
            print('Username sudah dipakai! Coba masukkan username lain..')
        else:
            break
        
        password = input('Password: ').strip().lower()
        email = input('Email: ').strip().lower()
        notelp = input('No. Telepon: ')
        baru = {'Username': username, 'Password': password, 'Email': email, 'Notelp': notelp}
        pengguna = pd.concat([pengguna, pd.DataFrame([baru])], ignore_index=True)
        pengguna.to_csv('daftar_pengguna.csv', index=False)
        print('Akun berhasil dibuat!')
        input('Tekan Enter untuk login...')

def menu_user():
    os.system('cls')
    while True:
        print('╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗')
        print('║                                                                  MENU USER                                                              ║')
        print('╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝')
        print("1. Tes MBTI")
        print("2. Input MBTI dan Nilai Akademik + Rekomendasi")
        print("3. Logout")
        
        pilihan = input("Pilih menu (1-3): ")
        
        if pilihan == "1":
            tes_mbti()
            
        elif pilihan == "2":
            # Input MBTI manual atau gunakan hasil tes
            mbti = input("Masukkan MBTI Anda (atau ketik 'tes' untuk tes ulang): ").upper()
            if mbti == 'TES':
                mbti = tes_mbti()
            
            # Input nilai
            nilai_user = input_nilai()
            
            # Dapatkan rekomendasi
            rekomendasi = rekomendasi_jurusan(nilai_user, mbti)
            
            print("\n=== TOP 3 REKOMENDASI JURUSAN ===")
            for i, (jurusan, skor) in enumerate(rekomendasi, 1):
                print(f"{i}. {jurusan} (Skor: {skor:.2f})")
                
            simpan_hasil(Username, mbti, rekomendasi)
            input("Tekan enter untuk lanjut...")
            print("\nHasil rekomendasi telah disimpan!")
            return

        elif pilihan == "3":
            logout()
            break
        else:
            print("Pilihan tidak valid!")

def menu_admin():
    os.system('cls')
    while True:
        print('╔═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗')
        print('║                                                                  MENU ADMIN                                                             ║')
        print('╚═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝')
        print("1 ▸ ✏️  Ubah/Tambah Daftar Jurusan")
        print("2 ▸ 🧠  Ubah/Tambah Pertanyaan MBTI")
        print("3 ▸ 📊  Lihat Hasil Rekomendasi User")
        print("4 ▸ 🚪  Logout")
        
        pilihan = input("Pilih menu (1-4): ")
        
        if pilihan == "1":
            kelola_jurusan()
        elif pilihan == "2":
            kelola_mbti_questions()
        elif pilihan == "3":
            lihat_hasil_rekomendasi()
        elif pilihan == "4":
            logout()
            break
        else:
            print("Pilihan tidak valid!")
        os.system('cls')

# Daftar mata pelajaran
mapel_list = [
    'matematika', 'fisika', 'biologi', 'kimia', 'seni', 
    'bahasa indonesia', 'ekonomi', 'sejarah', 'agama', 
    'TIK', 'bahasa inggris', 'PKN', 'geografi', 'sosiologi', 'penjas'
]

def urutkan_skors(scores_list):
    n = len(scores_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if scores_list[j][1] < scores_list[j + 1][1]:  
                scores_list[j], scores_list[j + 1] = scores_list[j + 1], scores_list[j]
    return scores_list

def hitung_bobot_mapel(nilai_5_semester):
    global bobot_mapel
    bobot_mapel = {}
    for mapel in mapel_list:
        if mapel in nilai_5_semester:
            rata_rata = sum(nilai_5_semester[mapel]) / len(nilai_5_semester[mapel])
            bobot_mapel[mapel] = rata_rata / 100
        else:
            bobot_mapel[mapel] = 0
    return bobot_mapel

def knapsack_01(nilai_user, kapasitas_max=100):
    """Knapsack 0/1 untuk optimasi pemilihan mata pelajaran"""
    mapel_keys = list(bobot_mapel.keys())
    n = len(mapel_keys)

    dp = [[0 for _ in range(kapasitas_max + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        mapel = mapel_keys[i-1]
        bobot = int(bobot_mapel[mapel] * 100) 
        nilai = nilai_user.get(mapel, 0)
        
        for w in range(kapasitas_max + 1):
            if bobot <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w-bobot] + nilai)
            else:
                dp[i][w] = dp[i-1][w]
    
    return dp[n][kapasitas_max]

def hitung_skor_akademik(nilai_user):
    total_skor = 0
    total_bobot = 0
    
    for mapel, nilai in nilai_user.items():
        if mapel in bobot_mapel:
            bobot = bobot_mapel[mapel]
            total_skor += nilai * bobot
            total_bobot += bobot
    
    return total_skor / total_bobot if total_bobot > 0 else 0

def cocok_mbti(user_mbti, jurusan_mbti_str):
    jurusan_mbti_list = jurusan_mbti_str.split(';')
    return user_mbti in jurusan_mbti_list

def rekomendasi_jurusan(nilai_user, user_mbti):
    os.system('cls')
    jurusan_data = pd.read_csv('jurusan.csv')
    if jurusan_data.empty:
        print("Tidak dapat memuat data jurusan!")
        return []
    
    skor_jurusan = []
    
    for index, jurusan in jurusan_data.iterrows():
        skor_akademik = 0
        total_bobot_jurusan = 0
        
        # Hitung skor berdasarkan mata pelajaran yang dibutuhkan jurusan
        for mapel in bobot_mapel.keys():
            if mapel in jurusan and str(jurusan[mapel]).isdigit() and int(jurusan[mapel]) > 0:
                bobot_mapel_val = bobot_mapel[mapel]
                bobot_jurusan = int(jurusan[mapel]) / 100  # Convert 90 -> 0.9
                nilai_mapel = nilai_user.get(mapel, 0)
                
                skor_akademik += nilai_mapel * bobot_mapel_val * bobot_jurusan
                total_bobot_jurusan += bobot_mapel_val * bobot_jurusan
        
        if total_bobot_jurusan > 0:
            skor_akademik = skor_akademik / total_bobot_jurusan
        
        # Bonus MBTI
        bonus_mbti = 10 if cocok_mbti(user_mbti, jurusan['mbti']) else 0
    
        # Gunakan knapsack untuk optimasi
        knapsack_score = knapsack_01(nilai_user) / 100  # Normalize
        
        skor_total = skor_akademik + bonus_mbti + knapsack_score
        skor_jurusan.append((jurusan['name'], skor_total))
    
    # Sort menggunakan bubble sort
    skor_jurusan = urutkan_skors(skor_jurusan)
    
    return skor_jurusan[:3]  # Top 3

def tes_mbti():
    os.system('cls')
    print("\n=== TES MBTI ===")
    print("Jawab dengan A atau B untuk setiap pertanyaan")

    try:
        mbti_questions = pd.read_csv("mbti_questions.csv")
    except FileNotFoundError:
        print("File mbti_questions.csv tidak ditemukan!")
        return
    except Exception as e:
        print("Terjadi kesalahan saat membaca file:", e)
        return

    if mbti_questions.empty:
        print("Tidak ada pertanyaan dalam file MBTI!")
        return

    dimensi_score = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}

    for i, row in mbti_questions.iterrows():
        os.system("cls" if os.name == "nt" else "clear")
        print(f"\n{i+1}. {row['pertanyaan']}")
        print(f"A. {row['A']}")
        print(f"B. {row['B']}")

        while True:
            jawaban = input("Pilihan (A/B): ").strip().upper()
            if jawaban == 'A':
                dimensi_score[row['dimensi_a']] += 1
                break
            elif jawaban == 'B':
                dimensi_score[row['dimensi_b']] += 1
                break
            else:
                print("Pilih A atau B!")

    # Tentukan MBTI
    mbti = ""
    mbti += 'E' if dimensi_score['E'] > dimensi_score['I'] else 'I'
    mbti += 'S' if dimensi_score['S'] > dimensi_score['N'] else 'N'
    mbti += 'T' if dimensi_score['T'] > dimensi_score['F'] else 'F'
    mbti += 'J' if dimensi_score['J'] > dimensi_score['P'] else 'P'

    os.system('cls')
    print(f"\nHasil MBTI Anda: {mbti}")
    print(f"MBTI Anda tersimpan: {mbti}")
    input("\nTekan enter untuk lanjut")
    os.system('cls')
    return 

def input_nilai():
    os.system('cls')
    print("\n=== INPUT NILAI AKADEMIK ===")
    print("Masukkan nilai rata-rata untuk 5 semester (0-100)")
    
    nilai_5_semester = {}
    
    # Input nilai per semester untuk setiap mata pelajaran
    for mapel in mapel_list:
        print(f"\nMata Pelajaran: {mapel.title()}")
        nilai_mapel = []
        for semester in range(1, 6):
            while True:
                try:
                    nilai = float(input(f"Semester {semester}: "))
                    if 0 <= nilai <= 100:
                        nilai_mapel.append(nilai)
                        break
                    else:
                        print("Nilai harus antara 0-100!")
                except ValueError:
                    print("Masukkan angka yang valid!")
        nilai_5_semester[mapel] = nilai_mapel
    
    # Hitung bobot berdasarkan nilai 5 semester
    hitung_bobot_mapel(nilai_5_semester)
    
    # Return nilai rata-rata untuk rekomendasi
    nilai_user = {}
    for mapel, nilai_list in nilai_5_semester.items():
        nilai_user[mapel] = sum(nilai_list) / len(nilai_list)
     #hjbbg
    
    return nilai_user

def simpan_hasil(username, mbti, rekomendasi):
    os.system('cls')
    try:
        df_hasil = pd.read_csv('hasil_rekomendasi.csv')
    except FileNotFoundError:
        df_hasil = pd.DataFrame(columns=['username', 'mbti', 'tanggal', 'jurusan_1', 'score_1', 'jurusan_2', 'score_2', 'jurusan_3', 'score_3'])
    
    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Siapkan data untuk ditambahkan
    data_baru = {
        'username': username,
        'mbti': mbti,
        'tanggal': tanggal,
        'jurusan_1': rekomendasi[0][0] if len(rekomendasi) > 0 else "",
        'score_1': f"{rekomendasi[0][1]:.2f}" if len(rekomendasi) > 0 else "",
        'jurusan_2': rekomendasi[1][0] if len(rekomendasi) > 1 else "",
        'score_2': f"{rekomendasi[1][1]:.2f}" if len(rekomendasi) > 1 else "",
        'jurusan_3': rekomendasi[2][0] if len(rekomendasi) > 2 else "",
        'score_3': f"{rekomendasi[2][1]:.2f}" if len(rekomendasi) > 2 else ""
    }
    
    # Tambah data baru
    new_row = pd.DataFrame([data_baru])
    df_hasil = pd.concat([df_hasil, new_row], ignore_index=True)
    df_hasil.to_csv('hasil_rekomendasi.csv', index=False)

def kelola_jurusan():
    os.system('cls')
    """Kelola data jurusan"""
    print("\n=== KELOLA JURUSAN ===")
    print("1. Lihat semua jurusan")
    print("2. Tambah jurusan baru")
    print("3. Edit jurusan")
    
    pilihan = input("Pilih (1-3): ")
    
    if pilihan == "1":
        jurusan_data = pd.read_csv("jurusan.csv")
        print("\nDaftar Jurusan:")
        for i, jurusan in jurusan_data.iterrows():
            print(f"{i+1}. {jurusan['name']}")
            
    elif pilihan == "2":
        nama = input("Nama jurusan baru: ")
        jurusan_baru = {'name': nama}
        
        print("Masukkan bobot mata pelajaran (0-90):")
        for mapel in mapel_list:
            while True:
                try:
                    bobot = int(input(f"{mapel.title()}: "))
                    if 0 <= bobot <= 90:
                        jurusan_baru[mapel] = str(bobot)
                        break
                    else:
                        print("Bobot harus 0-90!")
                except ValueError:
                    print("Masukkan angka yang valid!")
        
        mbti = input("MBTI yang cocok (pisahkan dengan ;): ")
        jurusan_baru['mbti'] = mbti
    
    elif pilihan == "3":
        jurusan_data = pd.read_csv("jurusan.csv")
        print("\nDaftar Jurusan:")
        for i, jurusan in jurusan_data.iterrows():
            print(f"{i+1}. {jurusan['name']}")
        try:
            idx = int(input("Pilih jurusan yang ingin diubah (nomor): ")) - 1
            if idx < 0 or idx >= len(jurusan_data):
                print("Nomor jurusan tidak valid!")
                return
            kolom = input("Kolom yang ingin diganti (name/matematika/fisika/.../mbti): ").lower()
            if kolom in jurusan_data.columns:
                nilai = input(f"Nilai baru untuk {kolom}: ")
                jurusan_data.at[idx, kolom] = nilai
                jurusan_data.to_csv('jurusan.csv', index=False)
                print("Jurusan berhasil diperbarui!")
            else:
                print("Kolom tidak valid!")
        except ValueError:
            print("Input tidak valid!")
        # Load data existing
        jurusan_data = pd.read_csv("jurusan.csv")
        jurusan_data = pd.concat([jurusan_data, pd.DataFrame([jurusan_baru])], ignore_index=True)
        # Simpan ke CSV
        jurusan_data.to_csv('jurusan.csv', index=False)
        print("Jurusan berhasil ditambahkan!")

def kelola_mbti_questions():
    os.system('cls')
    """Kelola pertanyaan MBTI"""
    print("\n=== KELOLA PERTANYAAN MBTI ===")
    print("1. Lihat semua pertanyaan")
    print("2. Tambah pertanyaan baru")
    
    pilihan = input("Pilih (1-2): ")
    
    if pilihan == "1":
        mbti_questions = pd.read_csv("mbti_questions.csv")
        for i, q in mbti_questions.iterrows():
            print(f"{i+1}. {q['pertanyaan']}")
            print(f"   A: {q['A']} ({q['dimensi_a']})")
            print(f"   B: {q['B']} ({q['dimensi_b']})")
            
    elif pilihan == "2":
        pertanyaan = input("Pertanyaan baru: ")
        pilihan_a = input("Pilihan A: ")
        pilihan_b = input("Pilihan B: ")
        dimensi_a = input("Dimensi A (E/I/S/N/T/F/J/P): ").upper()
        dimensi_b = input("Dimensi B (E/I/S/N/T/F/J/P): ").upper()
        
        pertanyaan_baru = {
            'pertanyaan': pertanyaan,
            'A': pilihan_a,
            'B': pilihan_b,
            'dimensi_a': dimensi_a,
            'dimensi_b': dimensi_b
        }
        
        # Load data existing
        mbti_questions = pd.read_csv("mbti_questions.csv")
        mbti_questions = pd.concat([mbti_questions, pd.DataFrame([pertanyaan_baru])], ignore_index=True)
        
        # Simpan ke CSV
        mbti_questions.to_csv('mbti_questions.csv', index=False)
        print("Pertanyaan berhasil ditambahkan!")

def lihat_hasil_rekomendasi():
    os.system('cls')
    """Lihat hasil rekomendasi semua user"""
    print("\n=== HASIL REKOMENDASI USER ===")
    try:
        df_hasil = pd.read_csv('hasil_rekomendasi.csv')
        if df_hasil.empty:
            print("Belum ada hasil rekomendasi.")
        else:
            for _, row in df_hasil.iterrows():
                print(f"User: {row['username']}")
                print(f"MBTI: {row['mbti']}")
                print(f"Tanggal: {row['tanggal']}")
                print(f"Rekomendasi 1: {row['jurusan_1']} ({row['score_1']})")
                print(f"Rekomendasi 2: {row['jurusan_2']} ({row['score_2']})")
                print(f"Rekomendasi 3: {row['jurusan_3']} ({row['score_3']})")
                print("-" * 50)
    except FileNotFoundError:
        print("Belum ada hasil rekomendasi.")

def logout():
    os.system('cls')
    print("\n#========================================================================== ==#")
    print("#           |                                                         |         #")
    print("#           |   Terima kasih telah menggunakan aplikasi MAJOR MATCH   |         #")
    print("#           |                         BYE-BYE                         |         #")
    print("#           |                                                         |         #")
    print("#===============================================================================#")
    time.sleep(2)
    a = input("Tekan Enter untuk kembali ke menu utama...")
    os.system('cls')

def main_menu():
    LaunchPage()
    while True:
        os.system("cls")
        print('''
╔═════════════════════════════╗
║         PILIHAN MENU        ║
╠═════════════════════════════╣
║ 1. Login                    ║
║ 2. Buat Akun                ║
║ 3. Keluar                   ║
╚═════════════════════════════╝''')
        
        pilihan = input("Pilih menu (1-3): ")
        
        if pilihan == "1":
            login()
                    
        elif pilihan == "2":
            buat_akun()
            
        elif pilihan == "3":
            print("Terima kasih telah menggunakan sistem ini!")
            break
            
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    main_menu()