from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QInputDialog,
    QAbstractItemView
)
from PySide6.QtCore import Qt
from database.conn import koneksi_database

class Jurusan (QWidget):
    def __init__(self):
        super().__init__()
        layout=QVBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(5)
        self.label=QLabel("Jurusan Sekolah")
        baris_atas = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Cari Barang...")

        self.tambah = QPushButton("Tambah")
        self.tambah.clicked.connect(self.tambah_jurusan)

        self.edit = QPushButton("Edit")
        self.edit.clicked.connect(self.edit_jurusan)
        self.hapus = QPushButton("Hapus")
        self.hapus.clicked.connect(self.hapus_jurusan)

        baris_atas.addWidget(self.search)
        baris_atas.addWidget(self.tambah)
        baris_atas.addWidget(self.edit)
        baris_atas.addWidget(self.hapus)

        layout.addWidget(self.label)
        layout.addLayout(baris_atas)
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(self.search)
        self.tabel=QTableWidget()
        self.tabel.setColumnCount(2)
        self.tabel.setHorizontalHeaderLabels([
            "ID",
            "Nama Jurusan"
        ])
        self.tabel.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tabel.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabel.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabel.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.tabel)

        self.label.setStyleSheet("""
            QLabel{
                color:black;
                font-size: 20px;
                font-weight: bold;
            }
            """)

        self.setStyleSheet("""
            QLabel{
                color:black;
                font-size: 20px;
                font-weight: bold;
            }
        """)

        
        self.search.setStyleSheet("""
            QLineEdit{
                color:black;
                background-color:white;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 4px;
            }
            """)
        self.search.textChanged.connect(self.cari_jurusan)
        self.cari_jurusan("")
        self.setLayout(layout)

    def cari_jurusan(self, teks):
        db=koneksi_database()
        cursor= db.cursor(dictionary=True)
        query="SELECT id, nama_jurusan FROM jurusan WHERE nama_jurusan LIKE %s"
        cursor.execute(query, (f"%{teks}%", ))
        data=cursor.fetchall()
        print(data)
        self.tabel.setRowCount(0)
        for jurusan in data:
            baris= self.tabel.rowCount()
            self.tabel.insertRow(baris)
            self.tabel.setItem(baris, 0, QTableWidgetItem(str(jurusan["id"])))
            self.tabel.setItem(baris, 1, QTableWidgetItem(jurusan["nama_jurusan"]))
        cursor.close()
        db.close()

    def tambah_jurusan(self):
        nama, ok = QInputDialog.getText(
            self,
            "Tambah Kategori",
            "Nama Kategori:"
        )
        if not ok:
            return
        
        nama = nama.strip()
        
        if not nama:
            
            QMessageBox.warning(
                self,
                "Peringatan",
                "Nama kategori tidak boleh kosong."
            )
            return
        
        try:
           
            db = koneksi_database()
            cursor = db.cursor()
            query = """INSERT INTO jurusan (nama_jurusan) VALUES (%s)"""
            
            cursor.execute(query, (nama,))
           
            db.commit()
            cursor.close()
            db.close()
            QMessageBox.information(
                self,
                "Berhasil",
                "Kategori berhasil ditambahkan."
            )
            
            self.cari_jurusan(
                self.search.text()
            )
        
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Database",
                f"Gagal menambahkan kategori:\n{e}"
            )

    def edit_jurusan(self):

        baris = self.tabel.currentRow()

        if baris < 0:
            QMessageBox.warning(
                self,
                "Peringatan",
                "Silakan pilih kategori yang ingin diedit."
            )
            return

        jurusan_id = self.tabel.item(baris, 0).text()
        nama_lama = self.tabel.item(baris, 1).text()

        nama_baru, ok = QInputDialog.getText(
            self,
            "Edit Kategori",
            "Nama Kategori:",
            text=nama_lama
        )

        if not ok:
            return

        nama_baru = nama_baru.strip()

        if not nama_baru:
            QMessageBox.warning(
                self,
                "Peringatan",
                "Nama kategori tidak boleh kosong."
            )
            return

        try:

            db = koneksi_database()
            cursor = db.cursor()

            query = """
                UPDATE jurusan
                SET nama_jurusan = %s
                WHERE id = %s
            """

            cursor.execute(
                query,
                (nama_baru, jurusan_id)
            )

            db.commit()

            cursor.close()
            db.close()

            QMessageBox.information(
                self,
                "Berhasil",
                "Kategori berhasil diperbarui."
            )

            self.cari_jurusan(
                self.search.text()
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error Database",
                f"Gagal mengedit kategori:\n{e}"
            )

    def hapus_jurusan(self):

        baris = self.tabel.currentRow()

        if baris < 0:
            QMessageBox.warning(
                self,
                "Peringatan",
                "Silakan pilih kategori yang ingin dihapus."
            )
            return

        jurusan_id = self.tabel.item(baris, 0).text()
        nama_jurusan = self.tabel.item(baris, 1).text()

        konfirmasi = QMessageBox.question(
            self,
            "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus kategori "
            f"'{nama_jurusan}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if konfirmasi != QMessageBox.Yes:
            return

        try:

            db = koneksi_database()
            cursor = db.cursor()
            query=("""
                SELECT COUNT(*)
                FROM siswa
                WHERE jurusan_id = %s
                """,
                (jurusan_id,)
            )

            # Hapus kategori
            cursor.execute(
                """
                DELETE FROM jurusan
                WHERE id = %s
                """,
                (jurusan_id,)
            )

            db.commit()

            cursor.close()
            db.close()

            QMessageBox.information(
                self,
                "Berhasil",
                f"Kategori '{nama_jurusan}' berhasil dihapus."
            )

            self.cari_jurusan(
                self.search.text()
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error Database",
                f"Gagal menghapus kategori:\n{e}"
            )