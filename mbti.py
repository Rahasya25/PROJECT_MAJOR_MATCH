import os

mbti_question = [
    ("Pilih yang paling sesuai dengan kamu:",
     "A. Saya lebih senang ada banyak orang di sekitar saya.",
     "B. Saya butuh banyak waktu untuk sendiri.", "E", "I"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Perhatian saya mudah teralihkan.",
     "B. Saya dapat berkonsentrasi pada masalah yang sedang dihadapi.", "E", "I"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Saya merasa mudah mendekati orang lain dan menjalin hubungan baru.",
     "B. Saya tipe yang lebih pendiam dan menjajaki hubungan baru dengan hati-hati.", "E", "I"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Saya sering membuat keputusan-keputusan seketika.",
     "B. Saya berpikir masak-masak sebelum bertindak.", "E", "I"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Saya senang mengatur waktu luang saya dengan aktif dan bersama-sama dengan orang lain.",
     "B. Saya suka menghabiskan waktu luang sendirian dengan melamun.", "E", "I"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Perhatian saya mudah teralihkan.",
     "B. Saya dapat berkonsentrasi pada masalah yang sedang dihadapi.", "E", "I"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Saya lebih senang mendiskusikan masalah dengan orang lain.",
     "B. Jika sesuatu membebani pikiran saya, saya segera mencoba mengatasinya sendiri.", "E", "I"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Ketika membuat keputusan, saya membiarkan diri dibimbing oleh kelima indra saya.",
     "B. Ketika membuat keputusan, saya membiarkan diri dibimbing oleh intuisi saya.", "S", "N"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Saya tidak suka menggantungkan diri pada peruntungan.",
     "B. Saya tidak suka ketika semua hal bisa diketahui sebelumnya dengan tepat.", "S", "N"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Saya lebih suka bekerja secara praktek.",
     "B. Saya lebih suka bekerja secara teoritis.", "S", "N"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Saya biasanya tidak keberatan berbagi ruang dan waktu pribadi dengan orang lain.",
     "B. Saya membutuhkan ruang pribadi sendiri dan banyak waktu untuk diri sendiri.", "S", "N"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Ketika bekerja, kekuatan saya antara lain adalah kesabaran dan ketelitian.",
     "B. Saya lebih suka bekerja secara garis besar tapi hasilnya biasanya tetap baik.", "S", "N"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Perhatian saya mudah teralihkan.",
     "B. Saya dapat berkonsentrasi pada masalah yang sedang dihadapi.", "S", "N"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Secara keseluruhan, saya puas dengan kehidupan saya.",
     "B. Saya selalu mencari ide-ide baru dan kemungkinan-kemungkinan pengembangan.", "S", "N"),

    ("Pilih yang paling sesuai dengan kamu:",
     "A. Keputusan saya biasanya dilandaskan pada pertimbangan-pertimbangan logis.",
     "B. Saya lebih banyak melandaskan keputusan saya pada naluri.", "T", "F"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Dalam pekerjaan saya, diperlukan pemikiran analitis dan tindakan yang masuk akal.",
     "B. Saya suka bekerja dengan orang lain dan tidak memiliki masalah berempati dengan mereka serta menanggapi mereka.", "T", "F"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Saya biasanya melontarkan pendapat jujur saya.",
     "B. Saya berusaha untuk tidak menyakiti orang lain dengan kata-kata saya.", "T", "F"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Saya cukup dapat menerima ketika seseorang mengkritik saya atau tidak menyukai saya.",
     "B. Saya agak sensitif dan cepat tersinggung.", "T", "F"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Berkata-kata halus bukanlah keahlian saya; seharusnya orang langsung saja mengatakan apa yang mereka inginkan.",
     "B. Saya dengan cepat bisa merasa jika ada sesuatu yang diucapkan secara tersirat.", "T", "F"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Saya menyukai diskusi dan bahkan berdebat demi sesuatu.",
     "B. Saya berusaha menghindari perselisihan karena keselarasan sangat penting bagi saya.", "T", "F"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Yang paling penting dari segalanya, saya membiarkan diri dibimbing oleh otak saya.",
     "B. Saya mendengarkan perasaan-perasaan saya.", "T", "F"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Saya tidak merasa sulit mengerjakan beberapa hal pada waktu bersamaan.",
     "B. Saya biasanya tepat waktu dan dapat diandalkan, saya tidak suka ketika ada orang lain yang tidak tepat waktu.", "P", "J"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Saya bekerja untuk hidup dan bukan sebaliknya.",
     "B. Bekerja dulu baru bersenang-senang .", "P", "J"),

    ("Pilih yang paling sesuai dengan kamu:",
     "A. Saya sering kesulitan membuat keputusan karena saya suka membiarkan semua kemungkinan terbuka.",
     "B. Saya suka membuat keputusan yang cepat, jelas, dan berharap orang lain melakukan hal yang sama.", "P", "J"),

    ("Pilih yang paling sesuai dengan kamu:",
     "A. Spontanitas dan keluwesan lebih penting ketimbang kaidah dan peraturan.",
     "B. Saya butuh keteraturan dan struktur dan saya kesal jika orang lain tidak berkerja sesuai rencana.", "P", "J"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Sering terjadi saya tidak menyelesaikan pekerjaan hingga menit terakhir.",
     "B. Saya merencanakan pekerjaan dengan matang sehingga tidak panik dan terburu-buru di belakang.", "P", "J"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Saya sama sekali tidak tahu apa yang akan saya lakukan akhir pekan depan",
     "B. Saya sudah tahu apa yang akan saya lakukan akhir pekan depan.", "P", "J"),

     ("Pilih yang paling sesuai dengan kamu:",
     "A. Saya mempunyai kebiasaan buruk menunda-nunda, terutama hal-hal yang tidak menyenangkan.",
     "B. Saya lebih sering melakukan hal-hal yang tidak saya sukai lebih dahulu sehingga saya sudah melaluinya.", "P", "J"),

]

def hitung(jawaban):
    skor = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    for i in range(len(jawaban)):
        if jawaban[i].lower() == "a":
            skor[mbti_question[i][3]] += 1
        else:
            skor[mbti_question[i][4]] += 1

    hasil = ""
    hasil += "E" if skor["E"] >= skor["I"] else "I"
    hasil += "S" if skor["S"] >= skor["N"] else "N"
    hasil += "T" if skor["T"] >= skor["F"] else "F"
    hasil += "J" if skor["J"] >= skor["P"] else "P"
    return hasil

data = []
nama = input("Masukkan nama kamu: ")
jawaban = []

i = 0
while i < len(mbti_question):
    os.system('cls')
    print(f"\n{i+1}. {mbti_question[i][0]}")
    print(mbti_question[i][1])
    print(mbti_question[i][2])
    answer = input("Jawaban kamu (a/b): ").lower()
    if answer in ['a', 'b']:
        jawaban.append(answer)
        i += 1
    else:
        print("Jawaban tidak valid. Masukkan a atau b: ")

os.system('cls')
hasil = hitung(jawaban)
data.append([nama, hasil])
print(f"\nHasil MBTI untuk {nama} adalah: {hasil}")

