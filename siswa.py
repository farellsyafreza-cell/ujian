from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidgetItem,
    QLineEdit,
    QTableWidget,
    QHeaderView,
    QMessageBox,
    QAbstractItemView,
    QDialog,
    QFormLayout,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    
)
from PySide6.QtCore import Qt
from database.conn import koneksi_database

class Siswa (QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(5)
        self.label=QLabel("Siswa")

        baris_atas = QHBoxLayout()

        self.cari = QLineEdit()
        self.cari.setPlaceholderText("Cari Siswa...")

        self.tambah = QPushButton("Tambah")
        self.tambah.clicked.connect(self.tambah_siswa)

        self.edit = QPushButton("Edit")
        self.edit.clicked.connect(self.edit_siswa)

        self.hapus = QPushButton("Hapus")
        self.hapus.clicked.connect(self.hapus_siswa)

        baris_atas.addWidget(self.cari)
        baris_atas.addWidget(self.tambah)
        baris_atas.addWidget(self.edit)
        baris_atas.addWidget(self.hapus)

        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self.label)
        layout.addLayout(baris_atas)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Nama Siswa",
            "Alamat",
            "Jenis kelamin",
            "Jurusan"
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        layout.addWidget(self.table)
        self.cari.textChanged.connect(self.cari_siswa)
        self.cari_siswa("")
        self.setLayout(layout)

        self.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 20px;
                font-weight: bold;
            }
        """)
        self.cari.setStyleSheet("""
            QLineEdit {
                color: black;
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 4px;
            }
        """)

    def cari_siswa(self, teks):
        try:
            db = koneksi_database()
            cursor = db.cursor(dictionary=True)
            query = """
                SELECT p.id, p.nama_siswa, p.alamat, p.jenis_kelamin, c.nama_jurusan AS jurusan,
                       p.jurusan_id
                FROM siswa p
                LEFT JOIN jurusan c ON p.jurusan_id = c.id
                WHERE p.nama_siswa LIKE %s
                OR p.id LIKE %s
                ORDER BY p.id ASC
            """
            keyword = (f"%{teks}%")
            cursor.execute(query, (keyword, keyword))
            hasil = cursor.fetchall()
            self.table.setRowCount(0)

            for siswa in hasil:
                barisan = self.table.rowCount()
                self.table.insertRow(barisan)
                self.table.setItem(barisan, 0, QTableWidgetItem(str(siswa["id"])))
                self.table.setItem(barisan, 1, QTableWidgetItem(str(siswa["nama_siswa"])))
                self.table.setItem(barisan, 2, QTableWidgetItem(str(siswa["alamat"])))
                self.table.setItem(barisan, 3, QTableWidgetItem(str(siswa["jenis_kelamin"])))
                kategori = siswa["jurusan"] or "-"
                self.table.setItem(barisan, 4, QTableWidgetItem(str(siswa["jurusan"])))
            cursor.close()
            db.close()
        except Exception as e:
            QMessageBox.warning(self, "Error Database", f"Gagal mengambil data produk:\n{e}")

    def tambah_siswa(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Tambah Produk")
        dialog.setMinimumWidth(400)

        layout = QFormLayout()

        kode = QLineEdit()
        kode.setPlaceholderText("Contoh: 1")
        layout.addRow("Id siswa:", kode)

        nama = QLineEdit()
        nama.setPlaceholderText("Contoh: Andi")
        layout.addRow("Nama Siswa:", nama)

        alamat= QLineEdit()
        alamat.setPlaceholderText("Contoh: jl.perumahan A")
        layout.addRow("Alamat Siswa:", alamat)

        jenis_kelamin = QComboBox()
        jenis_kelamin.addItem("Laki-laki", "L")
        jenis_kelamin.addItem("Perempuan", "P")
        jenis_kelamin.setCurrentIndex(0)
        layout.addRow("Jenis Kelamin:", jenis_kelamin)
        
        jurusan = QComboBox()

        try:

            db = koneksi_database()
            cursor = db.cursor(dictionary=True)

            query = """
                SELECT id, nama_jurusan
                FROM jurusan
                ORDER BY nama_jurusan ASC
            """

            cursor.execute(query)

            daftar_jurusan = cursor.fetchall()

            cursor.close()
            db.close()

            for item in daftar_jurusan:

                jurusan.addItem(
                    item["nama_jurusan"],
                    item["id"]
                )

        except Exception as e:

            QMessageBox.warning(
                self,
                "Error Database",
                f"Gagal mengambil jurusan:\n{e}"
            )

        layout.addRow(
            "Jurusan:",
            jurusan
        )

        # Button
        tombol_simpan = QPushButton("Simpan")
        tombol_batal = QPushButton("Batal")

        baris_tombol = QHBoxLayout()

        baris_tombol.addWidget(tombol_simpan)
        baris_tombol.addWidget(tombol_batal)

        layout.addRow(baris_tombol)

        dialog.setLayout(layout)

        tombol_batal.clicked.connect(
            dialog.reject
        )

        tombol_simpan.clicked.connect(
            lambda: self.simpan_siswa(
                dialog,
                nama,
                alamat,
                jenis_kelamin,
                jurusan
            )
        )

        dialog.exec()

    def simpan_siswa(self, dialog, nama, alamat, jenis_kelamin, jurusan):
        try:

                nama_siswa = nama.text().strip()
                alamat_siswa = alamat.text().strip()
                jk = jenis_kelamin.itemData(jenis_kelamin.currentIndex(),Qt.UserRole)
                jurusan_id = jurusan.itemData(jurusan.currentIndex(),Qt.UserRole)
                
                if not nama_siswa:
                    QMessageBox.warning(
                        self,
                        "Peringatan",
                        "Nama siswa wajib diisi!"
                    )
                    return

                if not alamat_siswa:
                    QMessageBox.warning(
                        self,
                        "Peringatan",
                        "Alamat wajib diisi!"
                    )
                    return

                if jurusan_id is None:
                    QMessageBox.warning(
                        self,
                        "Peringatan",
                        "Jurusan wajib dipilih!"
                    )
                    return
                
                db = koneksi_database()
                cursor = db.cursor()

                query = """
                    INSERT INTO siswa
                    (
                        nama_siswa,
                        alamat,
                        jenis_kelamin,
                        jurusan_id
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s
                    )
                """

                cursor.execute(
                    query,
                    (
                        nama_siswa,
                        alamat_siswa,
                        jk,
                        jurusan_id
                    )
                )

                db.commit()

                cursor.close()
                db.close()

                QMessageBox.information(
                    self,
                    "Berhasil",
                    "Data siswa berhasil ditambahkan!"
                )

                dialog.accept()

                self.cari_siswa(
                    self.cari.text()
                )
                
        except Exception as e:

                QMessageBox.critical(
                    self,
                    "Error Database",
                    f"Gagal menyimpan siswa:\n{e}"
                )

    def edit_siswa(self):
        baris = self.table.currentRow()

        if baris < 0:
            QMessageBox.warning(
                self,
                "Peringatan",
                "Silakan pilih siswa yang ingin diubah dari tabel terlebih dahulu."
            )
            return

        siswa_id = self.table.item(baris, 0).text()

        try:
            db = koneksi_database()
            cursor = db.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM siswa WHERE id = %s",
                (siswa_id,)
            )

            data_siswa = cursor.fetchone()

            cursor.close()
            db.close()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Database",
                f"Gagal mengambil detail siswa:\n{e}"
            )
            return

        if not data_siswa:
            QMessageBox.warning(
                self,
                "Peringatan",
                "Data siswa tidak ditemukan."
            )
            return

        dialog = QDialog(self)

        dialog.setWindowTitle("Edit Siswa")
        dialog.setMinimumWidth(400)

        layout = QFormLayout()

        nama = QLineEdit()

        nama.setText(
            str(data_siswa["nama_siswa"])
        )

        layout.addRow(
            "Nama Siswa:",
            nama
        )

        alamat = QLineEdit()

        alamat.setText(
            str(data_siswa["alamat"])
        )

        layout.addRow(
            "Alamat:",
            alamat
        )

        jenis_kelamin = QComboBox()

        jenis_kelamin.addItem("Laki-laki")
        jenis_kelamin.addItem("Perempuan")

        jk_saat_ini = data_siswa["jenis_kelamin"]

        index_jk = jenis_kelamin.findText(
            str(jk_saat_ini)
        )

        if index_jk != -1:
            jenis_kelamin.setCurrentIndex(
                index_jk
            )

        layout.addRow(
            "Jenis Kelamin:",
            jenis_kelamin
        )

        jurusan = QComboBox()

        jurusan_id_saat_ini = data_siswa["jurusan_id"]

        try:
            db = koneksi_database()
            cursor = db.cursor(dictionary=True)

            cursor.execute("""
                SELECT id, nama_jurusan
                FROM jurusan
                ORDER BY nama_jurusan ASC
            """)

            daftar_jurusan = cursor.fetchall()

            cursor.close()
            db.close()

            index_jurusan = -1

            for idx, item in enumerate(daftar_jurusan):

                jurusan.addItem(
                    item["nama_jurusan"],
                    item["id"]
                )

                if item["id"] == jurusan_id_saat_ini:
                    index_jurusan = idx

            if index_jurusan != -1:
                jurusan.setCurrentIndex(
                    index_jurusan
                )

        except Exception as e:
            QMessageBox.warning(
                self,
                "Error Database",
                f"Gagal mengambil jurusan:\n{e}"
            )

        layout.addRow(
            "Jurusan:",
            jurusan
        )

        tombol_simpan = QPushButton(
            "Update"
        )

        tombol_batal = QPushButton(
            "Batal"
        )

        baris_tombol = QHBoxLayout()

        baris_tombol.addWidget(
            tombol_simpan
        )

        baris_tombol.addWidget(
            tombol_batal
        )

        layout.addRow(
            baris_tombol
        )

        dialog.setLayout(
            layout
        )

        tombol_batal.clicked.connect(
            dialog.reject
        )

        tombol_simpan.clicked.connect(
            lambda: self.update_siswa(
            dialog,
            siswa_id,
            nama,
            alamat,
            jenis_kelamin,
            jurusan
            )
        )


        dialog.exec()

    def update_siswa(self, dialog, siswa_id, nama,alamat, jenis_kelamin, jurusan):
            try:
                nama_siswa = nama.text().strip()
                alamat_siswa = alamat.text().strip()

                # Ambil L / P
                if jenis_kelamin.currentIndex() == 0:
                    jk = "L"
                elif jenis_kelamin.currentIndex() == 1:
                    jk = "P"
                else:
                    QMessageBox.warning(
                        self,
                        "Peringatan",
                        "Pilih jenis kelamin terlebih dahulu."
                    )
                    return

                # Ambil ID jurusan
                jurusan_id = jurusan.itemData(
                    jurusan.currentIndex(),
                    Qt.UserRole
                )

                if not nama_siswa:
                    QMessageBox.warning(
                        self,
                        "Peringatan",
                        "Nama siswa wajib diisi."
                    )
                    return

                if not alamat_siswa:
                    QMessageBox.warning(
                        self,
                        "Peringatan",
                        "Alamat wajib diisi."
                    )
                    return

                if jurusan_id is None:
                    QMessageBox.warning(
                        self,
                        "Peringatan",
                        "Jurusan wajib dipilih."
                    )
                    return

                # UPDATE DATABASE
                db = koneksi_database()
                cursor = db.cursor()

                query = """
                    UPDATE siswa
                    SET
                        nama_siswa = %s,
                        alamat = %s,
                        jenis_kelamin = %s,
                        jurusan_id = %s
                    WHERE id = %s
                """

                cursor.execute(
                    query,
                    (
                        nama_siswa,
                        alamat_siswa,
                        jk,
                        jurusan_id,
                        siswa_id
                    )
                )

                db.commit()

                cursor.close()
                db.close()

                QMessageBox.information(
                    self,
                    "Berhasil",
                    "Data siswa berhasil diperbarui."
                )

                dialog.accept()

                # Refresh tabel
                self.cari_siswa(
                    self.cari.text()
                )

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error Database",
                    f"Gagal mengupdate siswa:\n{e}"
                )
    
    def hapus_siswa(self):
        baris = self.table.currentRow()

        if baris < 0:
            QMessageBox.warning(
                self,
                "Peringatan",
                "Silakan pilih siswa yang ingin dihapus dari tabel terlebih dahulu."
            )
            return

        siswa_id = self.table.item(baris, 0).text()

        nama_siswa = self.table.item(baris, 1).text()

        konfirmasi = QMessageBox.question(
            self,
            "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus siswa '{nama_siswa}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if konfirmasi == QMessageBox.Yes:

            try:

                db = koneksi_database()
                cursor = db.cursor()

                cursor.execute(
                    "DELETE FROM siswa WHERE id = %s",
                    (siswa_id,)
                )

                db.commit()

                cursor.close()
                db.close()

                QMessageBox.information(
                    self,
                    "Berhasil",
                    f"Siswa '{nama_siswa}' berhasil dihapus."
                )

                self.cari_siswa(
                    self.cari.text()
                )

            except Exception as e:

                QMessageBox.critical(
                    self,
                    "Error Database",
                    f"Gagal menghapus siswa:\n{e}"
                )