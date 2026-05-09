-- ============================================================
--  Formula None — MariaDB Database Script
--  Compatible: MariaDB >= 10.6.2
--  Encoding  : utf8mb4 / utf8mb4_unicode_ci
-- ============================================================

CREATE DATABASE IF NOT EXISTS formula_none
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE formula_none;

-- ============================================================
--  TABEL DASAR (tanpa FK ke tabel lain)
-- ============================================================

CREATE TABLE Negara (
    nama  VARCHAR(100) NOT NULL,
    kode  CHAR(3)      NOT NULL,
    PRIMARY KEY (nama)
) ENGINE=InnoDB;

-- ============================================================

CREATE TABLE Musim (
    tahun YEAR NOT NULL,
    -- total_balapan() → derived, lihat VIEW v_total_balapan_musim
    PRIMARY KEY (tahun)
) ENGINE=InnoDB;

-- ============================================================

CREATE TABLE Sirkuit (
    nama             VARCHAR(100)   NOT NULL,
    panjang_lintasan DECIMAL(6,3),          -- dalam kilometer
    jumlah_tikungan  SMALLINT UNSIGNED,
    negara           VARCHAR(100)   NOT NULL,
    PRIMARY KEY (nama),
    CONSTRAINT fk_sirkuit_negara
        FOREIGN KEY (negara) REFERENCES Negara(nama)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ============================================================

CREATE TABLE Tim (
    nama           VARCHAR(100)    NOT NULL,
    prinsipal_tim  VARCHAR(100),
    anggaran_musim DECIMAL(15, 2),          -- dalam USD
    negara         VARCHAR(100)    NOT NULL,
    PRIMARY KEY (nama),
    CONSTRAINT fk_tim_negara
        FOREIGN KEY (negara) REFERENCES Negara(nama)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ============================================================

CREATE TABLE Pemasok_mesin (
    nama   VARCHAR(100) NOT NULL,
    negara VARCHAR(100) NOT NULL,
    PRIMARY KEY (nama),
    CONSTRAINT fk_pemasok_negara
        FOREIGN KEY (negara) REFERENCES Negara(nama)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ============================================================

CREATE TABLE Marshal (
    nama               VARCHAR(100) NOT NULL,
    level_sertifikasi  VARCHAR(50),
    PRIMARY KEY (nama)
) ENGINE=InnoDB;

-- ============================================================
--  TABEL DENGAN FK KE TABEL DASAR
-- ============================================================

CREATE TABLE Pembalap (
    nama    VARCHAR(100) NOT NULL,
    no_balap TINYINT UNSIGNED,
    -- poin_total() → derived, lihat VIEW v_poin_total_pembalap
    negara  VARCHAR(100) NOT NULL,
    PRIMARY KEY (nama),
    CONSTRAINT fk_pembalap_negara
        FOREIGN KEY (negara) REFERENCES Negara(nama)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ============================================================
--  SUBTYPE PEMBALAP (ISA / Generalisasi-Spesialisasi)
-- ============================================================

CREATE TABLE Pembalap_aktif (
    nama_pembalap   VARCHAR(100) NOT NULL,
    tahun_debut     YEAR,
    status_kontrak  ENUM('Aktif','Bebas Transfer') NOT NULL DEFAULT 'Aktif',
    PRIMARY KEY (nama_pembalap),
    CONSTRAINT fk_aktif_pembalap
        FOREIGN KEY (nama_pembalap) REFERENCES Pembalap(nama)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================

CREATE TABLE Pembalap_pensiun (
    nama_pembalap  VARCHAR(100) NOT NULL,
    tahun_pensiun  YEAR,
    -- total_balapan() → derived, lihat VIEW v_total_balapan_pensiun
    PRIMARY KEY (nama_pembalap),
    CONSTRAINT fk_pensiun_pembalap
        FOREIGN KEY (nama_pembalap) REFERENCES Pembalap(nama)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================
--  TABEL RELASI MANY-TO-MANY DENGAN MUSIM
-- ============================================================

CREATE TABLE Memasok (
    nama_pemasok VARCHAR(100) NOT NULL,
    nama_tim     VARCHAR(100) NOT NULL,
    musim        YEAR        NOT NULL,
    PRIMARY KEY (nama_pemasok, nama_tim, musim),
    CONSTRAINT fk_memasok_pemasok
        FOREIGN KEY (nama_pemasok) REFERENCES Pemasok_mesin(nama)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_memasok_tim
        FOREIGN KEY (nama_tim) REFERENCES Tim(nama)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_memasok_musim
        FOREIGN KEY (musim) REFERENCES Musim(tahun)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ============================================================

CREATE TABLE Kontrak (
    nama_tim      VARCHAR(100) NOT NULL,
    nama_pembalap VARCHAR(100) NOT NULL,
    musim         YEAR        NOT NULL,
    PRIMARY KEY (nama_tim, nama_pembalap, musim),
    CONSTRAINT fk_kontrak_tim
        FOREIGN KEY (nama_tim) REFERENCES Tim(nama)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_kontrak_pembalap
        FOREIGN KEY (nama_pembalap) REFERENCES Pembalap(nama)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_kontrak_musim
        FOREIGN KEY (musim) REFERENCES Musim(tahun)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ============================================================
--  GRAND PRIX & TURUNANNYA
-- ============================================================

CREATE TABLE Grand_prix (
    nama_grandprix VARCHAR(150) NOT NULL,   -- unik per konvensi, mis. "Monaco GP 2024"
    sirkuit        VARCHAR(100) NOT NULL,
    musim          YEAR        NOT NULL,
    PRIMARY KEY (nama_grandprix),
    CONSTRAINT fk_gp_sirkuit
        FOREIGN KEY (sirkuit) REFERENCES Sirkuit(nama)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_gp_musim
        FOREIGN KEY (musim) REFERENCES Musim(tahun)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ============================================================

CREATE TABLE Sesi (
    nama       VARCHAR(50)  NOT NULL,   -- 'FP1','FP2','Kualifikasi','Sprint','Race'
    grandprix  VARCHAR(150) NOT NULL,
    waktu_mulai DATETIME,
    durasi      SMALLINT UNSIGNED,      -- dalam menit
    PRIMARY KEY (nama, grandprix),
    CONSTRAINT fk_sesi_gp
        FOREIGN KEY (grandprix) REFERENCES Grand_prix(nama_grandprix)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================

CREATE TABLE Balapan (
    pembalap      VARCHAR(100) NOT NULL,
    grandprix     VARCHAR(150) NOT NULL,
    posisi_finish TINYINT UNSIGNED,
    waktu_tempuh  VARCHAR(20),           -- misal '1:32:05.123' atau 'DNF'
    poin          DECIMAL(5, 2) UNSIGNED DEFAULT 0,
    PRIMARY KEY (pembalap, grandprix),
    CONSTRAINT fk_balapan_pembalap
        FOREIGN KEY (pembalap) REFERENCES Pembalap(nama)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_balapan_gp
        FOREIGN KEY (grandprix) REFERENCES Grand_prix(nama_grandprix)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ============================================================

CREATE TABLE Penghargaan (
    nama_penghargaan VARCHAR(100) NOT NULL,  -- 'Fastest Lap','Driver of the Day', dll
    nama_pembalap    VARCHAR(100) NOT NULL,
    grandprix        VARCHAR(150) NOT NULL,
    deskripsi        TEXT,
    PRIMARY KEY (nama_penghargaan, nama_pembalap, grandprix),
    -- FK ke Balapan (keikutsertaan spesifik)
    CONSTRAINT fk_penghargaan_balapan
        FOREIGN KEY (nama_pembalap, grandprix) REFERENCES Balapan(pembalap, grandprix)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================
--  MARSHAL & RELASI MENJAGA
-- ============================================================

CREATE TABLE Spesialisasi_marshal (
    nama_marshal VARCHAR(100) NOT NULL,
    spesialisasi VARCHAR(100) NOT NULL,
    PRIMARY KEY (nama_marshal, spesialisasi),
    CONSTRAINT fk_spesial_marshal
        FOREIGN KEY (nama_marshal) REFERENCES Marshal(nama)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================

CREATE TABLE Menjaga (
    nama_grandprix VARCHAR(150) NOT NULL,
    nama_sesi      VARCHAR(50)  NOT NULL,
    nama_marshal   VARCHAR(100) NOT NULL,
    PRIMARY KEY (nama_grandprix, nama_sesi, nama_marshal),
    -- FK ke Sesi (composite PK: nama, grandprix)
    CONSTRAINT fk_menjaga_sesi
        FOREIGN KEY (nama_sesi, nama_grandprix) REFERENCES Sesi(nama, grandprix)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_menjaga_marshal
        FOREIGN KEY (nama_marshal) REFERENCES Marshal(nama)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ============================================================
--  VIEW UNTUK ATRIBUT DERIVED (ditandai pink di diagram)
-- ============================================================

-- poin_total per pembalap (dari tabel Balapan)
CREATE OR REPLACE VIEW v_poin_total_pembalap AS
SELECT
    p.nama                          AS nama_pembalap,
    COALESCE(SUM(b.poin), 0)        AS poin_total
FROM Pembalap p
LEFT JOIN Balapan b ON p.nama = b.pembalap
GROUP BY p.nama;

-- total_balapan per pembalap yang sudah pensiun
CREATE OR REPLACE VIEW v_total_balapan_pensiun AS
SELECT
    pp.nama_pembalap,
    COUNT(b.pembalap)               AS total_balapan
FROM Pembalap_pensiun pp
LEFT JOIN Balapan b ON pp.nama_pembalap = b.pembalap
GROUP BY pp.nama_pembalap;

-- total_balapan per musim (jumlah Grand Prix dalam musim tersebut)
CREATE OR REPLACE VIEW v_total_balapan_musim AS
SELECT
    musim,
    COUNT(nama_grandprix)           AS total_balapan
FROM Grand_prix
GROUP BY musim;

-- ============================================================
--  END OF SCRIPT
-- ============================================================
