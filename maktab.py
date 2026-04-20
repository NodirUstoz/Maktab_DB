"""
==============================================================
  DATABASE COURSE
  MAVZU: MAKTAB AXBOROT TIZIMI (School Information System)

  SELECT bo'yicha chuqurlashtirilgan dars:
     - ORDER BY  (saralash)
     - LIMIT     (chegaralash)
     - LIKE      (matn qidirish)
     - BETWEEN   (oraliq)
     - IN        (ro'yxatdan)
     - DISTINCT  (takrorlanmaydigan)
     - COUNT, SUM, AVG, MIN, MAX  (aggregate funksiyalar)
     - GROUP BY  (guruhlash)
     - HAVING    (guruh filtri)

  Maqsad: O'quvchilar, fanlar va baholar jadvallaridan
          professional darajada ma'lumot olishni o'rganish.
==============================================================
"""

import sqlite3 as sq

with sq.connect("maktab.db") as con:
    cur = con.cursor()

    # ============================================================
    # 1-BO'LIM. JADVALARNI YARATISH
    # ============================================================
    # Maktab axborot tizimida 3 ta asosiy jadval bo'ladi:
    #   1) oquvchilar - o'quvchilar haqida ma'lumot
    #   2) fanlar     - o'qitiladigan fanlar va ularning ustozlari
    #   3) baholar    - o'quvchilarning fanlardan olgan baholari
    # Jadvallar bir-biri bilan id orqali bog'langan (foreign key).
    # ============================================================

    cur.execute("""CREATE TABLE IF NOT EXISTS oquvchilar (
        id INTEGER PRIMARY KEY,
        ism TEXT NOT NULL,
        familiya TEXT NOT NULL,
        sinf TEXT NOT NULL,           -- masalan: '10-A', '11-B'
        tugilgan_yil INTEGER,
        telefon TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS fanlar (
        id INTEGER PRIMARY KEY,
        nomi TEXT NOT NULL UNIQUE,
        oqituvchi TEXT NOT NULL,
        haftalik_soat INTEGER         -- haftada necha soat o'qitiladi
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS baholar (
        id INTEGER PRIMARY KEY,
        oquvchi_id INTEGER NOT NULL,
        fan_id INTEGER NOT NULL,
        ball INTEGER NOT NULL,        -- 0 dan 100 gacha
        sana TEXT NOT NULL,           -- 'YYYY-MM-DD' formatida
        FOREIGN KEY (oquvchi_id) REFERENCES oquvchilar(id),
        FOREIGN KEY (fan_id)     REFERENCES fanlar(id)
    )""")

    # ============================================================
    # 2-BO'LIM. MA'LUMOTLARNI KIRITISH
    # ============================================================
    # executemany() yordamida bir nechta qatorni bir buyruqda
    # qo'shamiz. INSERT OR IGNORE - id takrorlanmasligi uchun.
    # ============================================================

    oquvchilar_royxati = [
        # (id, ism,        familiya,      sinf,   tugilgan_yil, telefon)
        (1,  'Bekzod',     'Karimov',     '10-A', 2010, '+998901234567'),
        (2,  'Madina',     'Yusupova',    '10-A', 2010, '+998901234568'),
        (3,  'Aziz',       'Rahimov',     '10-A', 2009, '+998901234569'),
        (4,  'Nilufar',    'Tursunova',   '10-A', 2010, '+998901234570'),
        (5,  'Jasur',      'Nazarov',     '10-B', 2010, '+998901234571'),
        (6,  'Sevara',     'Ismoilova',   '10-B', 2010, '+998901234572'),
        (7,  'Otabek',     'Sharipov',    '10-B', 2009, '+998901234573'),
        (8,  'Dilnoza',    'Karimova',    '11-A', 2009, '+998901234574'),
        (9,  'Alisher',    'Xolmatov',    '11-A', 2008, '+998901234575'),
        (10, 'Gulnora',    'Abdullayeva', '11-A', 2009, '+998901234576'),
        (11, 'Sherzod',    'Mirzayev',    '11-B', 2008, '+998901234577'),
        (12, 'Zarina',     'Saidova',     '11-B', 2009, '+998901234578'),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO oquvchilar VALUES (?, ?, ?, ?, ?, ?)",
        oquvchilar_royxati
    )

    fanlar_royxati = [
        # (id, nomi,                  oqituvchi,                          haftalik_soat)
        (1, 'Matematika',             'Karimova Zulfiya Akmalovna',       6),
        (2, 'Fizika',                 'Rahimov Botir Sodiqovich',         4),
        (3, 'Kimyo',                  'Yusupova Mavluda Bahodirovna',     3),
        (4, 'Biologiya',              'Tursunov Sherzod Ravshanovich',    3),
        (5, 'Ona tili va adabiyot',   'Saidova Munira Akromovna',         5),
        (6, 'Ingliz tili',            'Olimova Nargiza Tolibovna',        4),
        (7, 'Tarix',                  'Nazarov Akmal Tursunovich',        2),
        (8, 'Informatika',            'Sharipov Jasur Komilovich',        3),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO fanlar VALUES (?, ?, ?, ?)",
        fanlar_royxati
    )

    baholar_royxati = [
        # (id, oquvchi_id, fan_id, ball, sana)
        # Bekzod Karimov (1)
        (1,  1, 1, 92, '2026-04-05'),  (2,  1, 2, 78, '2026-04-08'),
        (3,  1, 3, 85, '2026-04-12'),  (4,  1, 5, 88, '2026-04-15'),
        (5,  1, 8, 95, '2026-04-18'),
        # Madina Yusupova (2)
        (6,  2, 1, 98, '2026-04-05'),  (7,  2, 2, 95, '2026-04-08'),
        (8,  2, 3, 90, '2026-04-12'),  (9,  2, 4, 96, '2026-04-14'),
        (10, 2, 5, 92, '2026-04-15'),
        # Aziz Rahimov (3)
        (11, 3, 1, 65, '2026-04-05'),  (12, 3, 2, 70, '2026-04-08'),
        (13, 3, 3, 58, '2026-04-12'),  (14, 3, 6, 75, '2026-04-16'),
        # Nilufar Tursunova (4)
        (15, 4, 1, 88, '2026-04-05'),  (16, 4, 4, 94, '2026-04-14'),
        (17, 4, 5, 90, '2026-04-15'),  (18, 4, 6, 85, '2026-04-16'),
        # Jasur Nazarov (5)
        (19, 5, 1, 72, '2026-04-05'),  (20, 5, 7, 80, '2026-04-17'),
        (21, 5, 8, 88, '2026-04-18'),
        # Sevara Ismoilova (6)
        (22, 6, 3, 95, '2026-04-12'),  (23, 6, 4, 92, '2026-04-14'),
        (24, 6, 6, 89, '2026-04-16'),
        # Otabek Sharipov (7)
        (25, 7, 2, 82, '2026-04-08'),  (26, 7, 8, 91, '2026-04-18'),
        # Dilnoza Karimova (8)
        (27, 8, 1, 86, '2026-04-05'),  (28, 8, 5, 94, '2026-04-15'),
        (29, 8, 6, 88, '2026-04-16'),
        # Alisher Xolmatov (9)
        (30, 9, 2, 76, '2026-04-08'),  (31, 9, 7, 85, '2026-04-17'),
        # Gulnora Abdullayeva (10)
        (32, 10, 3, 89, '2026-04-12'), (33, 10, 4, 91, '2026-04-14'),
        (34, 10, 5, 87, '2026-04-15'),
        # Sherzod Mirzayev (11)
        (35, 11, 1, 55, '2026-04-05'), (36, 11, 2, 60, '2026-04-08'),
        (37, 11, 8, 78, '2026-04-18'),
        # Zarina Saidova (12)
        (38, 12, 5, 96, '2026-04-15'), (39, 12, 6, 93, '2026-04-16'),
        (40, 12, 7, 90, '2026-04-17'),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO baholar VALUES (?, ?, ?, ?, ?)",
        baholar_royxati
    )

    con.commit()

    # Natijalarni chiroyli chiqarish uchun yordamchi funksiya
    def chiqar(sarlavha, qatorlar):
        print("\n" + "=" * 65)
        print(f"  {sarlavha}")
        print("=" * 65)
        if not qatorlar:
            print("  (natija bo'sh)")
            return
        for q in qatorlar:
            print(" ", q)


    # ============================================================
    # 3-BO'LIM. ORDER BY - SARALASH
    # ============================================================
    # ORDER BY natijani ustun qiymati bo'yicha tartiblaydi.
    #   ASC  - o'sish tartibi (kichikdan kattaga) - default
    #   DESC - kamayish tartibi (kattadan kichikka)
    # ============================================================

    # 3.1) O'quvchilarni tug'ilgan yili bo'yicha (eng kichik birinchi)
    cur.execute("""
        SELECT ism, familiya, tugilgan_yil
        FROM oquvchilar
        ORDER BY tugilgan_yil ASC
    """)
    chiqar("O'quvchilar tug'ilgan yili bo'yicha (kichikdan kattaga)",
           cur.fetchall())

    # 3.2) Familiya bo'yicha alifbo tartibida
    cur.execute("""
        SELECT familiya, ism, sinf
        FROM oquvchilar
        ORDER BY familiya ASC
    """)
    chiqar("O'quvchilar familiyasi bo'yicha alifbo tartibida",
           cur.fetchall())

    # 3.3) Bir nechta ustun bo'yicha saralash:
    #      avval sinf bo'yicha (10-A, 10-B, 11-A, 11-B),
    #      keyin har bir sinf ichida familiya bo'yicha
    cur.execute("""
        SELECT sinf, familiya, ism
        FROM oquvchilar
        ORDER BY sinf ASC, familiya ASC
    """)
    chiqar("Sinf bo'yicha guruhlangan, ichida familiya tartibida",
           cur.fetchall())


    # ============================================================
    # 4-BO'LIM. LIMIT va OFFSET - CHEGARALASH
    # ============================================================
    # LIMIT  - natijadan necha qator olishni belgilaydi
    # OFFSET - boshidan necha qatorni o'tkazib yuborish
    # Sahifalashda (pagination) keng qo'llaniladi.
    # ============================================================

    # 4.1) Eng yuqori 5 ta baho
    cur.execute("""
        SELECT oquvchi_id, fan_id, ball, sana
        FROM baholar
        ORDER BY ball DESC
        LIMIT 5
    """)
    chiqar("Eng yuqori 5 ta baho", cur.fetchall())

    # 4.2) Sahifalash misoli: 6-10 o'rindagi baholar
    #      OFFSET 5 -> dastlabki 5 tani o'tkaz, keyin 5 ta ol
    cur.execute("""
        SELECT oquvchi_id, fan_id, ball
        FROM baholar
        ORDER BY ball DESC
        LIMIT 5 OFFSET 5
    """)
    chiqar("6-10 o'rindagi baholar (sahifalash)", cur.fetchall())


    # ============================================================
    # 5-BO'LIM. LIKE - MATN BO'YICHA QIDIRISH
    # ============================================================
    # LIKE matn ustunlarida namuna (pattern) bo'yicha qidiradi.
    #   %  - istalgan miqdordagi belgi (0 ta yoki ko'p)
    #   _  - aynan bitta belgi
    # ============================================================

    # 5.1) Familiyasi 'K' harfi bilan boshlanadigan o'quvchilar
    cur.execute("""
        SELECT ism, familiya
        FROM oquvchilar
        WHERE familiya LIKE 'K%'
    """)
    chiqar("Familiyasi 'K' bilan boshlanadiganlar", cur.fetchall())

    # 5.2) Familiyasi 'ova' bilan tugagan o'quvchilar (ko'pincha qiz bolalar)
    cur.execute("""
        SELECT ism, familiya, sinf
        FROM oquvchilar
        WHERE familiya LIKE '%ova'
    """)
    chiqar("Familiyasi 'ova' bilan tugaganlar", cur.fetchall())

    # 5.3) Telefon raqami '+99890' bilan boshlanadigan o'quvchilar
    cur.execute("""
        SELECT ism, familiya, telefon
        FROM oquvchilar
        WHERE telefon LIKE '+99890%'
    """)
    chiqar("Beeline operatorida telefoni borlar (+99890)",
           cur.fetchall())


    # ============================================================
    # 6-BO'LIM. BETWEEN - ORALIQ
    # ============================================================
    # BETWEEN A AND B - A va B oralig'idagilar (chetlari ham kiradi)
    # ============================================================

    # 6.1) 2009 va 2010 yillarda tug'ilgan o'quvchilar
    cur.execute("""
        SELECT ism, familiya, tugilgan_yil
        FROM oquvchilar
        WHERE tugilgan_yil BETWEEN 2009 AND 2010
    """)
    chiqar("2009-2010 yillarda tug'ilganlar", cur.fetchall())

    # 6.2) "Yaxshi" diapazondagi baholar (70-89)
    cur.execute("""
        SELECT oquvchi_id, fan_id, ball
        FROM baholar
        WHERE ball BETWEEN 70 AND 89
        ORDER BY ball DESC
    """)
    chiqar("Yaxshi baholar oralig'i (70-89)", cur.fetchall())


    # ============================================================
    # 7-BO'LIM. IN - RO'YXATDAN BIRORTASIGA TENG
    # ============================================================
    # IN (...) - qiymat ro'yxatdagi qiymatlardan birortasiga teng
    # ============================================================

    # 7.1) Faqat 10-A va 11-A sinf o'quvchilari
    cur.execute("""
        SELECT ism, familiya, sinf
        FROM oquvchilar
        WHERE sinf IN ('10-A', '11-A')
        ORDER BY sinf, familiya
    """)
    chiqar("10-A va 11-A sinf o'quvchilari", cur.fetchall())

    # 7.2) NOT IN - 11-sinflardan tashqari hamma
    cur.execute("""
        SELECT ism, familiya, sinf
        FROM oquvchilar
        WHERE sinf NOT IN ('11-A', '11-B')
    """)
    chiqar("11-sinflardan tashqari o'quvchilar", cur.fetchall())


    # ============================================================
    # 8-BO'LIM. DISTINCT - TAKRORLANMAYDIGAN QIYMATLAR
    # ============================================================
    # DISTINCT bir xil qiymatlarni faqat bir marta qaytaradi
    # ============================================================

    # 8.1) Maktabda nechta turli sinf bor?
    cur.execute("SELECT DISTINCT sinf FROM oquvchilar ORDER BY sinf")
    chiqar("Maktabdagi sinflar ro'yxati", cur.fetchall())

    # 8.2) Baho qo'yilgan kunlar (sanalar)
    cur.execute("SELECT DISTINCT sana FROM baholar ORDER BY sana")
    chiqar("Baho qo'yilgan kunlar", cur.fetchall())


    # ============================================================
    # 9-BO'LIM. AGGREGATE FUNKSIYALAR
    # ============================================================
    # COUNT(*)  - qatorlar soni
    # SUM(x)    - ustun yig'indisi
    # AVG(x)    - o'rtacha qiymat
    # MIN(x)    - eng kichik qiymat
    # MAX(x)    - eng katta qiymat
    # ============================================================

    # 9.1) Maktabda jami nechta o'quvchi bor
    cur.execute("SELECT COUNT(*) FROM oquvchilar")
    print(f"\n  Maktabda jami: {cur.fetchone()[0]} ta o'quvchi")

    # 9.2) Eng kichik va eng katta tug'ilgan yil
    cur.execute("""
        SELECT MIN(tugilgan_yil), MAX(tugilgan_yil)
        FROM oquvchilar
    """)
    eng_kichik, eng_katta = cur.fetchone()
    print(f"  Eng kichik tug'ilgan yil: {eng_kichik}")
    print(f"  Eng katta tug'ilgan yil:  {eng_katta}")

    # 9.3) Hamma fanlar bo'yicha umumiy o'rtacha ball
    cur.execute("SELECT AVG(ball) FROM baholar")
    print(f"  Maktab bo'yicha o'rtacha ball: {cur.fetchone()[0]:.2f}")

    # 9.4) Eng yuqori va eng past baho
    cur.execute("SELECT MIN(ball), MAX(ball) FROM baholar")
    eng_past, eng_yuqori = cur.fetchone()
    print(f"  Eng past baho: {eng_past},  eng yuqori baho: {eng_yuqori}")


    # ============================================================
    # 10-BO'LIM. GROUP BY - GURUHLASH
    # ============================================================
    # GROUP BY ma'lumotni guruhlarga ajratadi va har bir guruh
    # uchun aggregate funksiyani alohida hisoblaydi.
    # ============================================================

    # 10.1) Har bir sinfda nechta o'quvchi bor
    cur.execute("""
        SELECT sinf, COUNT(*) AS oquvchilar_soni
        FROM oquvchilar
        GROUP BY sinf
        ORDER BY sinf
    """)
    chiqar("Sinflar bo'yicha o'quvchilar soni", cur.fetchall())

    # 10.2) Har bir fan bo'yicha o'rtacha ball
    cur.execute("""
        SELECT f.nomi, ROUND(AVG(b.ball), 2) AS ortacha_ball,
               COUNT(b.id) AS baholar_soni
        FROM fanlar f
        JOIN baholar b ON f.id = b.fan_id
        GROUP BY f.id
        ORDER BY ortacha_ball DESC
    """)
    chiqar("Fanlar bo'yicha o'rtacha ball va baholar soni",
           cur.fetchall())

    # 10.3) Har bir o'quvchining o'rtacha bahosi (reyting)
    cur.execute("""
        SELECT o.ism || ' ' || o.familiya AS oquvchi,
               o.sinf,
               ROUND(AVG(b.ball), 2) AS ortacha_ball,
               COUNT(b.id) AS fanlar_soni
        FROM oquvchilar o
        JOIN baholar b ON o.id = b.oquvchi_id
        GROUP BY o.id
        ORDER BY ortacha_ball DESC
    """)
    chiqar("O'quvchilar reytingi (o'rtacha ball bo'yicha)",
           cur.fetchall())

    # 10.4) Har bir sinfning umumiy o'rtacha bahosi
    cur.execute("""
        SELECT o.sinf, ROUND(AVG(b.ball), 2) AS sinf_ortachasi
        FROM oquvchilar o
        JOIN baholar b ON o.id = b.oquvchi_id
        GROUP BY o.sinf
        ORDER BY sinf_ortachasi DESC
    """)
    chiqar("Sinflarning o'rtacha bahosi", cur.fetchall())


    # ============================================================
    # 11-BO'LIM. HAVING - GURUHLAR UCHUN FILTR
    # ============================================================
    # WHERE  - alohida qatorlarni filtrlaydi (GROUP BY dan OLDIN)
    # HAVING - guruhlangan natijalarni filtrlaydi (GROUP BY dan KEYIN)
    # ============================================================

    # 11.1) Faqat o'rtacha bahosi 85 dan yuqori bo'lgan o'quvchilar
    cur.execute("""
        SELECT o.ism || ' ' || o.familiya AS oquvchi,
               ROUND(AVG(b.ball), 2) AS ortacha
        FROM oquvchilar o
        JOIN baholar b ON o.id = b.oquvchi_id
        GROUP BY o.id
        HAVING ortacha > 85
        ORDER BY ortacha DESC
    """)
    chiqar("A'lochi o'quvchilar (o'rtacha > 85)", cur.fetchall())

    # 11.2) 3 dan ortiq o'quvchisi bor sinflar
    cur.execute("""
        SELECT sinf, COUNT(*) AS soni
        FROM oquvchilar
        GROUP BY sinf
        HAVING COUNT(*) > 3
    """)
    chiqar("3 dan ortiq o'quvchisi bor sinflar", cur.fetchall())

    # 11.3) O'rtacha bahosi 80 dan yuqori bo'lgan fanlar
    cur.execute("""
        SELECT f.nomi, ROUND(AVG(b.ball), 2) AS ortacha
        FROM fanlar f
        JOIN baholar b ON f.id = b.fan_id
        GROUP BY f.id
        HAVING ortacha > 80
        ORDER BY ortacha DESC
    """)
    chiqar("O'quvchilar yaxshi o'zlashtirayotgan fanlar (>80)",
           cur.fetchall())


    # ============================================================
    # 12-BO'LIM. KOMPLEKS SO'ROV - HAMMASINI BIRGA
    # ============================================================
    # Real vaziyat: Direktor uchun hisobot kerak.
    #
    # "10-A va 10-B sinflaridagi 2010-yilda tug'ilgan
    #  o'quvchilarning o'rtacha bahosi 80 dan yuqori bo'lganlarini
    #  o'rtacha ball bo'yicha kamayuvchi tartibda chiqaring."
    # ============================================================

    cur.execute("""
        SELECT o.ism || ' ' || o.familiya AS oquvchi,
               o.sinf,
               o.tugilgan_yil,
               ROUND(AVG(b.ball), 2) AS ortacha_ball
        FROM oquvchilar o
        JOIN baholar b ON o.id = b.oquvchi_id
        WHERE o.sinf IN ('10-A', '10-B')
          AND o.tugilgan_yil = 2010
        GROUP BY o.id
        HAVING ortacha_ball > 80
        ORDER BY ortacha_ball DESC
    """)
    chiqar("DIREKTOR HISOBOTI: 10-sinf 2010-yil tug'ilganlar reytingi",
           cur.fetchall())


    # ============================================================
    # MUSTAQIL ISH UCHUN VAZIFALAR
    # ============================================================
    # 1) Eng past o'rtacha bahoga ega 3 o'quvchini toping.
    #
    # 2) Ismi 'A' harfi bilan boshlanadigan o'quvchilarni
    #    sinflari bilan birga chiqaring.
    #
    # 3) Har bir o'qituvchining qancha o'quvchiga baho
    #    qo'yganini hisoblang.
    #    (Maslahat: fanlar JOIN baholar, GROUP BY oqituvchi)
    #
    # 4) 2026-04-15 sanasida qo'yilgan barcha baholarni,
    #    o'quvchi ism-familiyasi va fan nomi bilan ko'rsating.
    #
    # 5) Qaysi sinfda eng yuqori o'rtacha ball bor va u qancha?
    # ============================================================

    print("\n" + "=" * 65)
    print("  Dars yakuniga yetdi. Mustaqil vazifalarni bajaring!")
    print("=" * 65)
