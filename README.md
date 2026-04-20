# Maktab axborot tizimi: SQL bilan Ma'lumotlarni boshqarish

### *SELECT bo'yicha chuqurlashtirilgan dars qo'llanmasi*

> **Mavzu:** ORDER BY, LIMIT, LIKE, BETWEEN, IN, DISTINCT, GROUP BY, HAVING va aggregate funksiyalar

> **Avvaldan bilish kerak:** CRUD asoslari (CREATE, INSERT, UPDATE, DELETE)

> **Davomiyligi:** 60-75 daqiqa

---

## Muammo: Real maktabda nima sodir bo'ladi

Tasavvur qiling, siz maktab direktorining yordamchisisiz. Direktor sizdan quyidagi savollarga javob so'raydi:

1. *"10-A sinfining bu choragi o'rtacha bahosi qancha?"*
2. *"Maktabda eng a'lochi 5 ta o'quvchini ayting."*
3. *"Familiyasi 'Karimov' bo'lganlar nechta? Telefonlarini bering."*
4. *"Qaysi fan bo'yicha o'quvchilar eng past o'zlashtiryapti?"*
5. *"2010-yilda tug'ilgan, 10-sinfdagi a'lochilar ro'yxatini chiqaring."*

500 nafarli maktab jurnalini qo'lda varaqlasangiz — bir kun ketadi.

To'g'ri yozilgan SQL so'rovi bilan — **0.01 soniya**.

Bugun shu so'rovlarni yozishni o'rganamiz.

---

## 1. Maktab ma'lumotlar bazasi tuzilishi

Real maktab axborot tizimida ma'lumotlar bir nechta jadvallarda saqlanadi. Bizning misolimizda 3 ta jadval bor:

```
+----------------------+        +----------------------+
|     OQUVCHILAR       |        |       BAHOLAR        |
|----------------------|        |----------------------|
| id            (PK)   |<------>| oquvchi_id     (FK)  |
| ism                  |        | fan_id         (FK)  |<--+
| familiya             |        | ball                 |   |
| sinf                 |        | sana                 |   |
| tugilgan_yil         |        +----------------------+   |
| telefon              |                                   |
+----------------------+        +----------------------+   |
                                |       FANLAR         |   |
                                |----------------------|   |
                                | id            (PK)   |<--+
                                | nomi                 |
                                | oqituvchi            |
                                | haftalik_soat        |
                                +----------------------+
```

**Atamalar:**
- **PK** (Primary Key) — har bir qator uchun noyob identifikator
- **FK** (Foreign Key) — boshqa jadvalga ishora qiluvchi maydon

**Misol:** `baholar` jadvalidagi `oquvchi_id = 1` qiymati `oquvchilar` jadvalidagi `id = 1` ga (Bekzod Karimov) tegishli baho ekanligini bildiradi.

---

## 2. ORDER BY — Ma'lumotlarni saralash

### Hayotiy misol

Excel'da ustun ustiga bosib "A→Z" tugmasini bosish bilan barobar amal. SQL'da bu `ORDER BY` orqali bajariladi.

### Sintaksis

```sql
SELECT ustunlar FROM jadval ORDER BY ustun [ASC | DESC];
```

- `ASC` — kichikdan kattaga (A→Z, 1→9). **Default qiymat.**
- `DESC` — kattadan kichikka (Z→A, 9→1).

### Misol 1: O'quvchilarni tug'ilgan yili bo'yicha tartiblash

```sql
SELECT ism, familiya, tugilgan_yil
FROM oquvchilar
ORDER BY tugilgan_yil ASC;
```

**Natija:**
```
Alisher Xolmatov     2008
Sherzod Mirzayev     2008
Aziz Rahimov         2009
Otabek Sharipov      2009
...
```

### Misol 2: Familiya bo'yicha alifbo tartibida (sinf jurnali)

```sql
SELECT familiya, ism, sinf
FROM oquvchilar
ORDER BY familiya ASC;
```

Bu — har bir o'qituvchi sinf jurnalini ochganida ko'radigan tartib.

### Misol 3: Ko'p ustun bo'yicha saralash

Sinflar bo'yicha guruhlash, har bir sinf ichida familiya tartibida:

```sql
SELECT sinf, familiya, ism
FROM oquvchilar
ORDER BY sinf ASC, familiya ASC;
```

Bu **ikki bosqichli saralash**: avval birinchi ustun bo'yicha, agar tenglik bo'lsa — ikkinchi ustun bo'yicha.

---

## 3. LIMIT va OFFSET — Natijani chegaralash

### Muammo

12 ta o'quvchidan TOP-3 sini olish kerak. Hammasini olib, keyin Pythonda kesib olishimiz mumkin — lekin bu samarasiz. Ma'lumotlar bazasiga 1 millionta yozuv bo'lsa-chi?

### Yechim

```sql
SELECT oquvchi_id, fan_id, ball
FROM baholar
ORDER BY ball DESC
LIMIT 5;
```

`LIMIT 5` — birinchi 5 ta natijani qaytaradi.

### OFFSET — sahifalashda muhim

Veb-saytlarda ko'p uchraydigan vaziyat: bitta sahifada 10 natija ko'rsatish.

```sql
-- 1-sahifa (1-10)
LIMIT 10 OFFSET 0

-- 2-sahifa (11-20)
LIMIT 10 OFFSET 10

-- 3-sahifa (21-30)
LIMIT 10 OFFSET 20
```

**Real misol:** Google qidiruvi har sahifada 10 natija ko'rsatadi. "Next" tugmasini bosganingizda — orqada `OFFSET` qiymati o'zgaradi.

---

## 4. LIKE — Matn ichidan qidirish

### Muammo

Familiyasi 'K' bilan boshlanadigan o'quvchilarni topish kerak. `WHERE familiya = 'K'` ishlamaydi — chunki bu aynan "K" matniga tengligini tekshiradi.

### Yechim: maxsus belgilar

| Belgi | Ma'nosi | Misol |
|---|---|---|
| `%` | Istalgan miqdordagi belgi (0 ta yoki ko'p) | `'K%'` → "K..." |
| `_` | Aynan bitta belgi | `'___'` → 3 harfli |

### Misol 1: 'K' bilan boshlanadigan familiyalar

```sql
SELECT ism, familiya
FROM oquvchilar
WHERE familiya LIKE 'K%';
```

**Natija:** Bekzod Karimov, Dilnoza Karimova

### Misol 2: 'ova' bilan tugaydigan familiyalar

```sql
SELECT ism, familiya, sinf
FROM oquvchilar
WHERE familiya LIKE '%ova';
```

**Natija:** Madina Yusupova, Nilufar Tursunova, Sevara Ismoilova, Dilnoza Karimova, Gulnora Abdullayeva, Zarina Saidova

### Misol 3: Operator bo'yicha telefon raqamlari

```sql
SELECT ism, familiya, telefon
FROM oquvchilar
WHERE telefon LIKE '+99890%';
```

Bu Beeline operatorining barcha mijozlarini qaytaradi (kod 90).

### Real qo'llanma

- Login formasidagi qidiruv: `WHERE login LIKE 'admin%'`
- Email tekshirish: `WHERE email LIKE '%@gmail.com'`
- Telefon validatsiyasi: `WHERE telefon LIKE '+998%'`

---

## 5. BETWEEN — Oraliq bo'yicha filtrlash

### Tushuntirish

Quyidagi ikki yozuv **mutlaqo bir xil**:

```sql
WHERE tugilgan_yil >= 2009 AND tugilgan_yil <= 2010
```

```sql
WHERE tugilgan_yil BETWEEN 2009 AND 2010
```

`BETWEEN` qisqaroq va o'qish osonroq.

### Muhim eslatma

`BETWEEN A AND B` — **A va B ham** ichiga oladi (inclusive). Ya'ni `BETWEEN 70 AND 89` — 70 va 89 ham natijaga tushadi.

### Misol: O'quvchilarning bahosi bo'yicha tasniflash

| Diapazon | Sifat |
|---|---|
| 90-100 | A'lo |
| 70-89 | Yaxshi |
| 50-69 | Qoniqarli |
| 0-49 | Yomon |

```sql
SELECT oquvchi_id, fan_id, ball
FROM baholar
WHERE ball BETWEEN 70 AND 89
ORDER BY ball DESC;
```

---

## 6. IN — Ro'yxat bo'yicha filtr

### Muammo

Faqat 10-A va 11-A sinflarini olishimiz kerak. Yozish mumkin:

```sql
WHERE sinf = '10-A' OR sinf = '11-A'
```

Ammo agar 10 ta sinf bo'lsa-chi? Yozuv juda uzayadi.

### Yechim

```sql
WHERE sinf IN ('10-A', '11-A')
```

10 ta sinf bo'lsa:

```sql
WHERE sinf IN ('10-A', '10-B', '10-V', '11-A', '11-B', ...)
```

### NOT IN — qarama-qarshi

11-sinflardan tashqari hammani:

```sql
WHERE sinf NOT IN ('11-A', '11-B')
```

### Real qo'llanma

- Onlayn do'konda filtrlash: `WHERE brend IN ('Apple', 'Samsung', 'Xiaomi')`
- HR tizimida: `WHERE bolim IN ('IT', 'Marketing', 'Sotuv')`
- Statistikada: `WHERE viloyat IN ('Toshkent', 'Samarqand', 'Buxoro')`

---

## 7. DISTINCT — Takrorlanmaydigan qiymatlar

### Muammo

`SELECT sinf FROM oquvchilar` so'rovi **12 ta natija** qaytaradi (har bir o'quvchi uchun bittadan). Lekin sinflar atigi 4 ta. Faqat noyoblarini olish kerak.

### Yechim

```sql
SELECT DISTINCT sinf FROM oquvchilar ORDER BY sinf;
```

**Natija:** `10-A`, `10-B`, `11-A`, `11-B` — har biri **bir martadan**.

### Boshqa misol

Ushbu maktabda baholar qaysi kunlarda qo'yilgan?

```sql
SELECT DISTINCT sana FROM baholar ORDER BY sana;
```

### Real qo'llanma

- Internet-do'konda: "Bizda qaysi shaharlardan mijozlar bor?" — `SELECT DISTINCT shahar FROM mijozlar`
- Marketingda: "Foydalanuvchilarimiz qaysi qurilmalardan kiradi?" — `SELECT DISTINCT qurilma_turi FROM seans`

---

## 8. Aggregate funksiyalar — Hisoblovchilar

Bu funksiyalar bir nechta qatordan **bitta yakuniy qiymat** chiqaradi.

| Funksiya | Vazifasi | Misol |
|---|---|---|
| `COUNT(*)` | Qatorlar sonini sanaydi | `SELECT COUNT(*) FROM oquvchilar` → 12 |
| `SUM(x)` | Ustun yig'indisini topadi | `SELECT SUM(ball) FROM baholar` |
| `AVG(x)` | O'rtacha qiymatni hisoblaydi | `SELECT AVG(ball) FROM baholar` → 84.43 |
| `MIN(x)` | Eng kichik qiymat | `SELECT MIN(ball) FROM baholar` → 55 |
| `MAX(x)` | Eng katta qiymat | `SELECT MAX(ball) FROM baholar` → 98 |

### Bir so'rovda bir nechta funksiya

```sql
SELECT
    COUNT(*) AS jami_baholar,
    AVG(ball) AS ortacha,
    MIN(ball) AS eng_past,
    MAX(ball) AS eng_yuqori
FROM baholar;
```

**Natija:** `40 ta baho, o'rtacha 84.43, eng past 55, eng yuqori 98`

### Real qo'llanma

- Banking: `SELECT SUM(qoldiq) FROM hisoblar WHERE mijoz_id = 123` — mijozning umumiy mablag'i
- E-commerce: `SELECT AVG(bayho) FROM mahsulotlar WHERE id = 456` — mahsulot reytingi
- Analitika: `SELECT COUNT(*) FROM tashriflar WHERE sana = '2026-04-20'` — bugungi tashriflar

---

## 9. GROUP BY — Guruhlash

Bu darsdagi **eng muhim mavzu**.

### Muammo

`COUNT(*)` jami sonni beradi. Lekin "har bir sinfda alohida nechta o'quvchi bor?" degan savolga javob bera olmaydi.

### Yechim

```sql
SELECT sinf, COUNT(*) AS oquvchilar_soni
FROM oquvchilar
GROUP BY sinf
ORDER BY sinf;
```

**Natija:**
```
10-A    4
10-B    3
11-A    3
11-B    2
```

### GROUP BY qanday ishlaydi (tushuntirish)

Tasavvur qiling: barcha o'quvchilarning kartochkalari stol ustida. Siz ularni quyidagicha ajratasiz:

```
[10-A guruhi]    [10-B guruhi]    [11-A guruhi]    [11-B guruhi]
  Bekzod           Jasur            Dilnoza          Sherzod
  Madina           Sevara           Alisher          Zarina
  Aziz             Otabek           Gulnora
  Nilufar
```

Keyin har bir guruhga `COUNT(*)` qo'llaysiz.

### Misol 2: JOIN bilan birga ishlatish

Har bir fan bo'yicha o'rtacha ball:

```sql
SELECT f.nomi, ROUND(AVG(b.ball), 2) AS ortacha
FROM fanlar f
JOIN baholar b ON f.id = b.fan_id
GROUP BY f.id
ORDER BY ortacha DESC;
```

**Natija:**
```
Biologiya               93.25
Ona tili va adabiyot    91.17
Informatika             88.00
Ingliz tili             86.00
Tarix                   85.00
Kimyo                   83.40
Matematika              79.43
Fizika                  76.83
```

Endi o'qituvchi qaysi fan bo'yicha ko'proq mehnat qilish kerakligini aniq biladi (Fizika va Matematika).

### Misol 3: O'quvchilar reytingi

```sql
SELECT o.ism || ' ' || o.familiya AS oquvchi,
       o.sinf,
       ROUND(AVG(b.ball), 2) AS ortacha_ball
FROM oquvchilar o
JOIN baholar b ON o.id = b.oquvchi_id
GROUP BY o.id
ORDER BY ortacha_ball DESC;
```

`||` — SQL'da matnlarni birlashtirish operatori (Pythonda `+` kabi).

---

## 10. HAVING — Guruhlar uchun filtr

### Muhim farq: WHERE va HAVING

Bu ikki tushuncha aralashib ketishi mumkin:

| Operator | Nima qiladi | Qachon ishlaydi |
|---|---|---|
| `WHERE` | Alohida qatorlarni filtrlaydi | GROUP BY dan **OLDIN** |
| `HAVING` | Guruhlangan natijalarni filtrlaydi | GROUP BY dan **KEYIN** |

### Misol: A'lochi o'quvchilar

```sql
SELECT o.ism || ' ' || o.familiya AS oquvchi,
       ROUND(AVG(b.ball), 2) AS ortacha
FROM oquvchilar o
JOIN baholar b ON o.id = b.oquvchi_id
GROUP BY o.id
HAVING ortacha > 85
ORDER BY ortacha DESC;
```

**Nima uchun WHERE emas?** Chunki `ortacha` aggregate funksiya natijasi — u har bir guruh uchun hisoblanadi. WHERE alohida qatorlarda ishlaydi, guruh natijasini bilmaydi.

### Sodda qoida

> Agar shartingizda `COUNT()`, `AVG()`, `SUM()` kabi funksiyalar qatnashsa — **HAVING** ishlatiladi.
> Agar shartingiz oddiy ustun qiymati bilan bo'lsa — **WHERE** ishlatiladi.

### Birgalikda ishlatish

```sql
SELECT sinf, AVG(ball) AS ortacha
FROM oquvchilar o
JOIN baholar b ON o.id = b.oquvchi_id
WHERE o.tugilgan_yil >= 2009    -- alohida qator filtri (tug'ilgan yil)
GROUP BY sinf
HAVING ortacha > 80;             -- guruh filtri (o'rtacha ball)
```

---

## 11. SQL so'rovining bajarilish tartibi (juda muhim!)

Yozuv tartibi va bajarilish tartibi **boshqa-boshqa**. Buni bilish ko'p xatolardan saqlaydi.

| Yozuv tartibi | Bajarilish tartibi |
|---|---|
| `SELECT` | 5. SELECT (ustunlar tanlanadi) |
| `FROM` | 1. FROM (jadvallardan ma'lumot olinadi) |
| `WHERE` | 2. WHERE (qatorlar filtrlanadi) |
| `GROUP BY` | 3. GROUP BY (guruhlash) |
| `HAVING` | 4. HAVING (guruhlar filtrlanadi) |
| `ORDER BY` | 6. ORDER BY (saralash) |
| `LIMIT` | 7. LIMIT (chegaralash) |

**Eslab qoling:**
```
FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
```

---

## 12. Real masala: Direktor uchun hisobot

Bu darsda o'rgangan hamma narsani birlashtiramiz.

**Vazifa:**
> "10-A va 10-B sinflaridagi 2010-yilda tug'ilgan o'quvchilarning o'rtacha bahosi 80 dan yuqori bo'lganlarini o'rtacha ball bo'yicha kamayuvchi tartibda chiqaring."

**Yechim:**

```sql
SELECT o.ism || ' ' || o.familiya AS oquvchi,
       o.sinf,
       o.tugilgan_yil,
       ROUND(AVG(b.ball), 2) AS ortacha_ball
FROM oquvchilar o
JOIN baholar b ON o.id = b.oquvchi_id
WHERE o.sinf IN ('10-A', '10-B')      -- IN
  AND o.tugilgan_yil = 2010            -- oddiy filtr
GROUP BY o.id                          -- har bir o'quvchi uchun
HAVING ortacha_ball > 80               -- guruh filtri
ORDER BY ortacha_ball DESC;            -- saralash
```

**Natija:**
```
Madina Yusupova       10-A    2010    94.20
Sevara Ismoilova      10-B    2010    92.00
Nilufar Tursunova     10-A    2010    89.25
Bekzod Karimov        10-A    2010    87.60
```

Bitta so'rovda **6 ta SQL elementi**: `JOIN`, `WHERE`, `IN`, `GROUP BY`, `HAVING`, `ORDER BY`.

---

## Mustaqil ish uchun vazifalar

### 1-vazifa
Eng past o'rtacha bahoga ega 3 o'quvchini toping.
> *Maslahat:* `JOIN`, `GROUP BY`, `ORDER BY ortacha ASC`, `LIMIT 3`

### 2-vazifa
Ismi 'A' harfi bilan boshlanadigan o'quvchilarni sinflari bilan birga chiqaring.
> *Maslahat:* `WHERE ism LIKE 'A%'`

### 3-vazifa
Har bir o'qituvchining qancha o'quvchiga baho qo'yganini hisoblang.
> *Maslahat:* `fanlar JOIN baholar`, `GROUP BY oqituvchi`, `COUNT(DISTINCT oquvchi_id)`

### 4-vazifa
2026-04-15 sanasida qo'yilgan barcha baholarni o'quvchi ism-familiyasi va fan nomi bilan ko'rsating.
> *Maslahat:* uchta jadvalni ham JOIN qilish kerak.

### 5-vazifa
Qaysi sinfda eng yuqori o'rtacha ball bor va u qancha?
> *Maslahat:* `GROUP BY sinf`, `ORDER BY AVG(ball) DESC`, `LIMIT 1`

---

## Bu mavzular qayerda qo'llaniladi?

| Soha | Misol |
|---|---|
| **Bank tizimi** | "Oxirgi 30 kun ichida 10 mln so'mdan ortiq o'tkazma qilgan mijozlar" |
| **Onlayn do'kon** | "Bu oy eng ko'p sotilgan TOP-10 mahsulot" |
| **Ijtimoiy tarmoq** | "Foydalanuvchilarning eng faol vaqtlari (soatlar bo'yicha)" |
| **Tibbiyot** | "2025-yilda har viloyatda qancha bemor ro'yxatga olingan" |
| **Logistika** | "Har bir filialdagi yetkazib berishlar soni va o'rtacha vaqti" |

Bu darsda o'rgangan SQL so'rovlari — **butun dunyodagi har bir jiddiy IT tizimida** ishlatiladigan asboblardir.

---

## Yakuniy xulosa

Bugungi darsda o'rganilgan 9 ta buyruq:

```
[1] ORDER BY    - saralash (ASC / DESC)
[2] LIMIT       - chegaralash (TOP-N)
[3] OFFSET      - sahifalash
[4] LIKE        - matn bo'yicha qidirish (%, _)
[5] BETWEEN     - oraliq filtri
[6] IN          - ro'yxat bo'yicha filter
[7] DISTINCT    - takrorlanmaydigan qiymatlar
[8] GROUP BY    - guruhlash + aggregate funksiyalar
[9] HAVING      - guruh natijalarini filtrlash
```

Bu buyruqlarni o'zlashtirgan dasturchi har qanday ma'lumotlar bazasidan kerakli ma'lumotni **tezda va aniq** olish qobiliyatiga ega bo'ladi.

> *"Ma'lumotlar bilan ishlash — bu zamonaviy savodxonlik. Bugungi kunda ma'lumotni o'qiy olmaslik — XX asrda kitobni o'qiy olmaslik kabidir."*

---
