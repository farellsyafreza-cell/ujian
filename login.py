from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QMessageBox,
    QWidget,
    QLineEdit,
    QVBoxLayout
)
from PySide6.QtCore import Qt
from database.conn import koneksi_database

class Login (QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(400, 460)
        self.buat_ui()

    def buat_ui(self):
        self.login=QLabel("Login")
        self.login.setAlignment(Qt.AlignCenter)
        self.login.setStyleSheet("""
                QLabel{
                    color:red;
                    font-size:26px;
                    font-weight:bold;
                }
        """)
        self.username=QLabel("Username")
        self.isi_username=QLineEdit()
        self.isi_username.setPlaceholderText("Isi Username")
        self.password=QLabel("Password")
        self.isi_password=QLineEdit()
        self.isi_password.setPlaceholderText("Isi Password")
        self.isi_password.setEchoMode(QLineEdit.Password)
        self.masuk=QPushButton("Masuk")
        self.masuk.clicked.connect(self.jalan)
        self.masuk.setStyleSheet("""
            QPushButton{
                color:white;
                border-radius:5px;
                padding:5px;
                background-color:green;
            }
        """)
        self.keluar=QPushButton("Keluar")
        self.keluar.clicked.connect(self.close)
        self.keluar.setStyleSheet("""
                    QPushButton{
                        color:white;
                        border-radius:5px;
                        padding:5px;
                        background-color:red;
                    }
                """)
        layout=QVBoxLayout()
        layout.addWidget(self.login)
        layout.addWidget(self.username)
        layout.addWidget(self.isi_username)
        layout.addWidget(self.password)
        layout.addWidget(self.isi_password)
        layout.setSpacing(5)
        layout.addSpacing(15)
        layout.addWidget(self.masuk)
        layout.addSpacing(5)
        layout.addWidget(self.keluar)
        layout.addSpacing(5)
        layout.setContentsMargins(20, 10, 20, 10)
        self.setLayout(layout)
        self.setStyleSheet("""
                QLabel{
                    color: black;
                    font-size: 16px;
                    font-weight: bold;
                }

                QLineEdit{
                    background-color:#FFFFFF;
                    border:1 px solid  #cbd5e1;
                    border-radius:8px;
                    padding:8px
                }
        """)
    def jalan(self):
        nama=self.isi_username.text()
        pw=self.isi_password.text()

        if nama == "" or pw == "":
            QMessageBox.warning(self, "error", "Diisi dengan lengkap")
            return

        try:
            db=koneksi_database()
            cursor=db.cursor(dictionary=True)
            query= "SELECT * FROM login WHERE username = %s AND password = %s"
            cursor.execute(query, (nama, pw))
            login=cursor.fetchone()
            cursor.close()
            db.close()

            if login:
                QMessageBox.information(self, "Berhasil", "Berhasil Masuk")
                username= login["username"]
                password= login["password"]
                self.buka_dashboard(username, password)
            else:
                QMessageBox.warning(self, "Error", "Nama tidak sesuai")
                return
        except Exception as e:
            QMessageBox.critical(self, "Error database", f"Tidak bisa tersambung {e}")
            return 

    def buka_dashboard(self, username, password):
        from dashboard import Dashboard
        self.dashboard=Dashboard(username, password)
        self.dashboard.show()
        self.close()

if __name__ == "__main__":
   app=QApplication()
   window=Login()
   window.show()
   app.exec()
