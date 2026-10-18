import streamlit as st
import os
import re
from collections import Counter

# =========================================================
# KONFIGURASI
# =========================================================

st.set_page_config(
    page_title="AI Tutor Bahasa Indonesia",
    page_icon="📚",
    layout="wide"
)

FOLDER_DATABASE = "database"


# =========================================================
# MATERI KELAS IX
# =========================================================

materi_kelas_9 = """
# TEKS PIDATO PERSUASIF

## 1. Pengertian

Teks pidato persuasif adalah teks yang berisi gagasan,
pendapat, atau ajakan yang disampaikan kepada pendengar
dengan tujuan memengaruhi mereka agar melakukan sesuatu
sesuai dengan yang disampaikan oleh pembicara.

Pidato persuasif tidak hanya memberikan informasi,
tetapi juga berusaha meyakinkan pendengar melalui
alasan, fakta, dan ajakan.

## 2. Tujuan

Tujuan utama pidato persuasif adalah memengaruhi
pendengar agar menerima gagasan atau melakukan
tindakan tertentu.

Contohnya:
- Mengajak siswa menjaga kebersihan sekolah.
- Mengajak masyarakat mengurangi penggunaan plastik.
- Mengajak remaja menggunakan media sosial secara bijak.
- Mengajak siswa rajin membaca.

## 3. Ciri-Ciri

Ciri-ciri teks pidato persuasif antara lain:

1. Berisi ajakan atau imbauan.
2. Bertujuan memengaruhi pendengar.
3. Menggunakan alasan yang logis.
4. Dapat menggunakan fakta atau data.
5. Menggunakan bahasa yang mudah dipahami.
6. Menggunakan kata-kata persuasif.

Kata yang sering digunakan:
ayo, mari, marilah, hendaknya, sebaiknya.

## 4. Struktur

### A. Pembukaan

Pembukaan merupakan bagian awal pidato.
Biasanya berisi salam pembuka, sapaan kepada pendengar,
ucapan syukur, dan pengantar menuju topik.

### B. Isi

Isi merupakan bagian utama pidato.
Pada bagian ini pembicara menyampaikan gagasan,
pendapat, alasan, fakta, dan ajakan.

### C. Penutup

Penutup merupakan bagian akhir pidato.
Bagian ini dapat berisi simpulan, harapan,
ajakan kembali, ucapan terima kasih,
permohonan maaf, dan salam penutup.

## 5. Kaidah Kebahasaan

Kaidah kebahasaan pidato persuasif antara lain:

- Kata ajakan.
- Kata kerja yang menunjukkan tindakan.
- Kata hubung.
- Kalimat persuasif.
- Kata yang menunjukkan hubungan sebab-akibat.
- Bahasa yang santun dan mudah dipahami.

## 6. Contoh

Teman-teman yang saya banggakan,

Kebersihan sekolah merupakan tanggung jawab kita
bersama. Lingkungan sekolah yang bersih membuat kita
lebih nyaman dalam belajar. Oleh karena itu, mari kita
membuang sampah pada tempatnya dan menjaga kebersihan
kelas setiap hari.

Jika kita membiasakan hidup bersih, sekolah kita akan
menjadi tempat belajar yang nyaman dan sehat.

Terima kasih atas perhatian teman-teman.
"""


# =========================================================
# DATABASE TXT
# =========================================================

def baca_database():

    data = []

    if not os.path.exists(FOLDER_DATABASE):
        os.makedirs(FOLDER_DATABASE)

    for nama_file in os.listdir(FOLDER_DATABASE):

        if nama_file.lower().endswith(".txt"):

            lokasi = os.path.join(
                FOLDER_DATABASE,
                nama_file
            )

            try:

                with open(
                    lokasi,
                    "r",
                    encoding="utf-8"
                ) as file:

                    isi = file.read()

                data.append({
                    "nama_file": nama_file,
                    "isi": isi
                })

            except Exception as error:

                st.error(
                    f"Gagal membaca {nama_file}: {error}"
                )

    return data


# =========================================================
# PENCARIAN MATERI
# =========================================================

def bersihkan_teks(teks):

    teks = teks.lower()

    teks = re.sub(
        r"[^a-zA-ZÀ-ÿ0-9\s]",
        " ",
        teks
    )

    teks = re.sub(
        r"\s+",
        " ",
        teks
    )

    return teks.strip()


STOPWORDS = {
    "yang", "dan", "di", "ke", "dari",
    "pada", "dengan", "untuk", "dalam",
    "adalah", "itu", "ini", "atau",
    "apa", "bagaimana", "mengapa",
    "sebutkan", "jelaskan", "tentang",
    "suatu", "sebuah", "secara",
    "merupakan", "dapat", "akan",
    "sebagai", "oleh", "lebih",
    "juga", "tidak", "tersebut"
}


def ambil_kata_kunci(pertanyaan):

    teks = bersihkan_teks(
        pertanyaan
    )

    kata = teks.split()

    return [
        item
        for item in kata
        if len(item) > 2
        and item not in STOPWORDS
    ]


def hitung_relevansi(
    pertanyaan,
    isi
):

    kata_kunci = ambil_kata_kunci(
        pertanyaan
    )

    if not kata_kunci:
        return 0

    teks = bersihkan_teks(
        isi
    )

    frekuensi = Counter(
        teks.split()
    )

    skor = 0

    for kata in kata_kunci:

        if kata in frekuensi:

            jumlah = frekuensi[kata]

            skor += min(
                jumlah,
                10
            )

    return skor


def cari_materi(
    pertanyaan,
    database
):

    hasil = []

    for data in database:

        skor = hitung_relevansi(
            pertanyaan,
            data["isi"]
        )

        if skor > 0:

            hasil.append({
                "nama_file":
                    data["nama_file"],

                "isi":
                    data["isi"],

                "skor":
                    skor
            })

    hasil.sort(
        key=lambda x: x["skor"],
        reverse=True
    )

    return hasil


# =========================================================
# DATABASE
# =========================================================

database = baca_database()


# =========================================================
# SESSION STATE
# =========================================================

if "halaman" not in st.session_state:

    st.session_state.halaman = "Beranda"


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("📚 AI Tutor")

    st.caption(
        "Bahasa Indonesia Kelas IX"
    )

    st.divider()

    st.subheader("🎓 MENU UTAMA")

    if st.button(
        "🏠 Beranda",
        use_container_width=True
    ):
        st.session_state.halaman = "Beranda"

    if st.button(
        "📚 Materi",
        use_container_width=True
    ):
        st.session_state.halaman = "Materi"

    if st.button(
        "🤖 Tanya AI",
        use_container_width=True
    ):
        st.session_state.halaman = "Tanya AI"

    if st.button(
        "📝 Latihan",
        use_container_width=True
    ):
        st.session_state.halaman = "Latihan"

    if st.button(
        "📋 Perangkat Pembelajaran",
        use_container_width=True
    ):
        st.session_state.halaman = "Perangkat Pembelajaran"

    if st.button(
        "🔄 Remedial",
        use_container_width=True
    ):
        st.session_state.halaman = "Remedial"

    if st.button(
        "⭐ Pengayaan",
        use_container_width=True
    ):
        st.session_state.halaman = "Pengayaan"

    if st.button(
        "🎬 Media Pembelajaran",
        use_container_width=True
    ):
        st.session_state.halaman = "Media Pembelajaran"

    st.divider()

    st.subheader("📖 Knowledge Base")

    st.write(
        f"File TXT: **{len(database)}**"
    )

    if len(database) > 0:

        for data in database:

            nama = data["nama_file"]

            nama = nama.replace(
                ".txt",
                ""
            )

            nama = nama.replace(
                "_",
                " "
            )

            st.caption(
                "📄 " + nama.title()
            )

    else:

        st.caption(
            "Belum ada file tambahan."
        )


# =========================================================
# HEADER
# =========================================================

st.title(
    "📚 AI Tutor Bahasa Indonesia"
)

st.caption(
    "Media pembelajaran interaktif "
    "Bahasa Indonesia Kelas IX"
)

st.divider()


# =========================================================
# BERANDA
# =========================================================

if st.session_state.halaman == "Beranda":

    st.header("🏠 Selamat Datang")

    st.write(
        """
        Selamat datang di **AI Tutor Bahasa Indonesia**.

        Aplikasi ini dirancang untuk membantu siswa
        mempelajari materi Bahasa Indonesia secara
        mandiri dan interaktif.
        """
    )

    st.subheader(
        "📖 Materi Pembelajaran"
    )

    st.success(
        "Bahasa Indonesia Kelas IX"
    )

    st.write(
        "**Materi utama:** Teks Pidato Persuasif"
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📚 Materi",
            "1 Topik"
        )

    with col2:

        st.metric(
            "📝 Latihan",
            "10 Soal"
        )

    with col3:

        st.metric(
            "🤖 Tanya AI",
            "Aktif"
        )

    st.info(
        "💡 Gunakan menu di sebelah kiri "
        "untuk mulai belajar."
    )


# =========================================================
# MATERI
# =========================================================

elif st.session_state.halaman == "Materi":

    st.header(
        "📚 Materi Pembelajaran"
    )

    st.subheader(
        "Bahasa Indonesia Kelas IX"
    )

    st.markdown(
        materi_kelas_9
    )

    st.success(
        "Setelah mempelajari materi, "
        "silakan lanjutkan ke menu Latihan."
    )


# =========================================================
# TANYA AI
# =========================================================

elif st.session_state.halaman == "Tanya AI":

    st.header(
        "🤖 Tanya AI"
    )

    st.write(
        "Ajukan pertanyaan mengenai "
        "teks pidato persuasif."
    )

    pertanyaan = st.text_area(
        "Pertanyaan Anda:",
        placeholder=(
            "Contoh: Apa tujuan teks pidato persuasif?"
        ),
        height=120
    )

    if st.button(
        "🔍 TANYAKAN",
        use_container_width=True
    ):

        if pertanyaan.strip() == "":

            st.warning(
                "Silakan masukkan pertanyaan."
            )

        else:

            database_ai = database.copy()

            database_ai.append({
                "nama_file":
                    "Materi Kelas IX - Teks Pidato Persuasif",

                "isi":
                    materi_kelas_9
            })

            hasil = cari_materi(
                pertanyaan,
                database_ai
            )

            if hasil:

                sumber = hasil[0]

                teks = sumber["isi"]

                kata_kunci = ambil_kata_kunci(
                    pertanyaan
                )

                paragraf = teks.split("\n\n")

                paragraf_cocok = []

                for p in paragraf:

                    skor = 0

                    p_bersih = bersihkan_teks(
                        p
                    )

                    for kata in kata_kunci:

                        if kata in p_bersih:
                            skor += 1

                    if skor > 0:

                        paragraf_cocok.append(
                            (skor, p)
                        )

                paragraf_cocok.sort(
                    reverse=True
                )

                if paragraf_cocok:

                    jawaban = "\n\n".join(
                        [
                            item[1]
                            for item in paragraf_cocok[:3]
                        ]
                    )

                else:

                    jawaban = teks[:1500]

                st.success(
                    "Jawaban ditemukan dari materi."
                )

                st.subheader(
                    "💡 Jawaban"
                )

                st.info(
                    jawaban
                )

                st.caption(
                    "Sumber: "
                    + sumber["nama_file"]
                )

            else:

                st.warning(
                    "Jawaban belum ditemukan."
                )


# =========================================================
# LATIHAN
# =========================================================

elif st.session_state.halaman == "Latihan":

    st.header(
        "📝 Latihan"
    )

    st.write(
        "**Materi: Teks Pidato Persuasif**"
    )

    st.write(
        "Pilih satu jawaban yang paling tepat."
    )

    soal = [

        (
            "Apa yang dimaksud dengan teks pidato persuasif?",
            [
                "Teks yang berisi cerita pengalaman.",
                "Teks yang bertujuan memengaruhi pendengar.",
                "Teks yang menjelaskan langkah-langkah.",
                "Teks yang menggambarkan suatu tempat."
            ],
            1
        ),

        (
            "Tujuan utama pidato persuasif adalah...",
            [
                "Menghibur pendengar.",
                "Menceritakan pengalaman.",
                "Memengaruhi pendengar.",
                "Menggambarkan suatu objek."
            ],
            2
        ),

        (
            "Berikut yang merupakan ciri pidato persuasif adalah...",
            [
                "Berisi ajakan.",
                "Tidak memiliki tujuan.",
                "Hanya berisi dialog.",
                "Tidak membutuhkan alasan."
            ],
            0
        ),

        (
            "Kata yang menunjukkan ajakan adalah...",
            [
                "Tetapi",
                "Karena",
                "Mari",
                "Kemudian"
            ],
            2
        ),

        (
            "Bagian pidato yang berisi gagasan dan alasan disebut...",
            [
                "Pembukaan",
                "Isi",
                "Penutup",
                "Salam"
            ],
            1
        ),

        (
            "Bagian awal pidato biasanya berisi...",
            [
                "Salam pembuka dan pengantar.",
                "Simpulan.",
                "Daftar pustaka.",
                "Daftar pertanyaan."
            ],
            0
        ),

        (
            "Hal yang dapat memperkuat argumen pidato adalah...",
            [
                "Fakta atau data.",
                "Cerita khayalan.",
                "Kata yang tidak berhubungan.",
                "Kalimat tidak jelas."
            ],
            0
        ),

        (
            "Kalimat persuasif adalah...",
            [
                "Sekolah itu memiliki banyak kelas.",
                "Saya pergi ke sekolah.",
                "Mari menjaga kebersihan sekolah.",
                "Sekolah berada di tengah kota."
            ],
            2
        ),

        (
            "Bagian penutup pidato dapat berisi...",
            [
                "Salam pembuka.",
                "Pengenalan pembicara.",
                "Simpulan dan ucapan terima kasih.",
                "Judul buku."
            ],
            2
        ),

        (
            "Mengapa bahasa pidato harus santun?",
            [
                "Agar pendengar mudah memahami pesan.",
                "Agar pidato lebih panjang.",
                "Agar menggunakan banyak kata.",
                "Agar pendengar bingung."
            ],
            0
        )
    ]

    jawaban = []

    for nomor, item in enumerate(soal):

        pertanyaan = item[0]
        pilihan = item[1]

        st.subheader(
            f"Soal {nomor + 1}"
        )

        st.write(
            pertanyaan
        )

        pilihan_siswa = st.radio(
            "Pilih jawaban:",
            pilihan,
            key=f"jawaban_{nomor}",
            index=None
        )

        jawaban.append(
            pilihan_siswa
        )

        st.divider()

    if st.button(
        "✅ SELESAI & LIHAT NILAI",
        use_container_width=True
    ):

        benar = 0

        belum = 0

        for i, item in enumerate(soal):

            if jawaban[i] is None:

                belum += 1

            elif jawaban[i] == item[1][item[2]]:

                benar += 1

        if belum > 0:

            st.warning(
                f"Masih ada {belum} soal "
                "yang belum dijawab."
            )

        else:

            nilai = benar * 10

            st.subheader(
                "🎉 Hasil Latihan"
            )

            st.metric(
                "Nilai",
                nilai
            )

            st.write(
                f"Jawaban benar: "
                f"**{benar} dari 10 soal**"
            )

            if nilai >= 80:

                st.success(
                    "🎉 Sangat baik! "
                    "Kamu sudah memahami materi."
                )

            elif nilai >= 60:

                st.warning(
                    "👍 Cukup baik. "
                    "Pelajari kembali bagian yang belum dikuasai."
                )

            else:

                st.error(
                    "📖 Kamu perlu mempelajari "
                    "materi kembali."
                )


# =========================================================
# PERANGKAT PEMBELAJARAN
# =========================================================

elif st.session_state.halaman == "Perangkat Pembelajaran":

    st.header(
        "📋 Perangkat Pembelajaran"
    )

    st.subheader(
        "Modul Ajar Bahasa Indonesia"
    )

    st.write(
        "**Kelas:** IX SMP"
    )

    st.write(
        "**Materi:** Teks Pidato Persuasif"
    )

    st.write(
        "**Alokasi waktu:** 2 × 40 menit"
    )

    st.divider()

    st.subheader(
        "🎯 Tujuan Pembelajaran"
    )

    st.markdown(
        """
        Setelah mengikuti pembelajaran, siswa diharapkan mampu:

        1. Menjelaskan pengertian teks pidato persuasif.
        2. Mengidentifikasi tujuan pidato persuasif.
        3. Mengidentifikasi struktur pidato persuasif.
        4. Menentukan ciri-ciri pidato persuasif.
        5. Mengidentifikasi kaidah kebahasaan pidato persuasif.
        6. Menganalisis isi teks pidato persuasif.
        """
    )

    st.subheader(
        "📌 Kegiatan Pembelajaran"
    )

    st.markdown(
        """
        **Pendahuluan**
        - Guru membuka pembelajaran.
        - Guru menyampaikan tujuan pembelajaran.
        - Guru mengaitkan materi dengan kehidupan sehari-hari.

        **Kegiatan Inti**
        - Siswa membaca materi.
        - Siswa mengidentifikasi struktur pidato.
        - Siswa menemukan kata ajakan.
        - Siswa berdiskusi mengenai contoh pidato.

        **Penutup**
        - Siswa menyimpulkan materi.
        - Guru memberikan latihan.
        - Guru memberikan penguatan.
        """
    )

    st.subheader(
        "📊 Asesmen"
    )

    st.markdown(
        """
        - Pengetahuan: latihan pilihan ganda.
        - Keterampilan: menganalisis struktur pidato.
        - Sikap: keaktifan dan tanggung jawab dalam pembelajaran.
        """
    )


# =========================================================
# REMEDIAL
# =========================================================

elif st.session_state.halaman == "Remedial":

    st.header(
        "🔄 Remedial"
    )

    st.write(
        "Remedial ditujukan bagi siswa yang "
        "belum mencapai nilai ketuntasan."
    )

    st.subheader(
        "📖 Ringkasan Materi"
    )

    st.markdown(
        """
        **Pidato persuasif** adalah pidato yang bertujuan
        memengaruhi pendengar.

        Struktur utamanya:

        1. Pembukaan
        2. Isi
        3. Penutup

        Kata ajakan yang sering digunakan:

        **ayo, mari, marilah, hendaknya, sebaiknya.**
        """
    )

    st.divider()

    st.subheader(
        "📝 Soal Remedial"
    )

    remedial_soal = [

        (
            "Tujuan pidato persuasif adalah...",
            [
                "Menghibur",
                "Memengaruhi",
                "Menggambarkan",
                "Menceritakan"
            ],
            1
        ),

        (
            "Kata yang menunjukkan ajakan adalah...",
            [
                "Mari",
                "Tetapi",
                "Karena",
                "Namun"
            ],
            0
        ),

        (
            "Struktur pidato terdiri atas...",
            [
                "Orientasi, komplikasi, resolusi",
                "Pembukaan, isi, penutup",
                "Tesis, argumentasi, penegasan",
                "Identitas, deskripsi, simpulan"
            ],
            1
        ),

        (
            "Bagian utama pidato adalah...",
            [
                "Isi",
                "Salam",
                "Judul",
                "Sapaan"
            ],
            0
        ),

        (
            "Salah satu penguat argumen adalah...",
            [
                "Fakta",
                "Khayalan",
                "Tebakan",
                "Rumor"
            ],
            0
        )
    ]

    remedial_jawaban = []

    for i, item in enumerate(remedial_soal):

        st.write(
            f"**{i + 1}. {item[0]}**"
        )

        pilihan = st.radio(
            "Pilih jawaban:",
            item[1],
            key=f"remedial_{i}",
            index=None
        )

        remedial_jawaban.append(
            pilihan
        )

    if st.button(
        "✅ Periksa Remedial",
        use_container_width=True
    ):

        benar = 0

        for i, item in enumerate(remedial_soal):

            if (
                remedial_jawaban[i]
                == item[1][item[2]]
            ):

                benar += 1

        nilai = benar * 20

        st.success(
            f"Nilai remedial: **{nilai}**"
        )


# =========================================================
# PENGAYAAN
# =========================================================

elif st.session_state.halaman == "Pengayaan":

    st.header(
        "⭐ Pengayaan"
    )

    st.write(
        "Kegiatan pengayaan ditujukan bagi siswa "
        "yang sudah memahami materi dasar."
    )

    st.subheader(
        "🎯 Tantangan Pengayaan"
    )

    st.write(
        """
        Buatlah sebuah teks pidato persuasif dengan
        tema **menjaga kebersihan lingkungan sekolah**.
        """
    )

    st.write(
        "Pidato harus memiliki:"
    )

    st.markdown(
        """
        - Pembukaan
        - Isi
        - Alasan atau fakta pendukung
        - Kalimat ajakan
        - Penutup
        """
    )

    teks_pengayaan = st.text_area(
        "Tulis rancangan pidato Anda:",
        height=250
    )

    if st.button(
        "💾 Simpan Jawaban Pengayaan",
        use_container_width=True
    ):

        if teks_pengayaan.strip() == "":

            st.warning(
                "Silakan tuliskan jawaban terlebih dahulu."
            )

        else:

            st.success(
                "Jawaban pengayaan berhasil dibuat."
            )


# =========================================================
# MEDIA PEMBELAJARAN
# =========================================================

elif st.session_state.halaman == "Media Pembelajaran":

    st.header(
        "🎬 Media Pembelajaran"
    )

    st.write(
        "Media pembelajaran untuk membantu memahami "
        "teks pidato persuasif."
    )

    st.subheader(
        "🧠 Peta Konsep"
    )

    st.markdown(
        """
        ### TEKS PIDATO PERSUASIF

        **Tujuan**
        ↓  
        Memengaruhi pendengar

        **Struktur**
        ↓  
        Pembukaan → Isi → Penutup

        **Ciri**
        ↓  
        Ajakan + alasan + fakta

        **Kata Ajakan**
        ↓  
        Ayo + Mari + Hendaknya + Sebaiknya
        """
    )

    st.divider()

    st.subheader(
        "🎥 Rekomendasi Aktivitas Video"
    )

    st.info(
        """
        Siswa dapat menonton video contoh pidato
        persuasif yang disediakan guru, kemudian
        mengidentifikasi pembukaan, isi, penutup,
        serta kalimat ajakan yang digunakan.
        """
    )

    st.subheader(
        "💡 Aktivitas Setelah Menonton"
    )

    st.markdown(
        """
        1. Catat topik pidato.
        2. Tentukan tujuan pidato.
        3. Identifikasi struktur pidato.
        4. Temukan kata atau kalimat ajakan.
        5. Tuliskan kesimpulan.
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AI Tutor Bahasa Indonesia | "
    "Kelas IX | Python + Streamlit"
)