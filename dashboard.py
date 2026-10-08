from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget
)
from PySide6.QtCore import Qt

class Dashboard(QMainWindow):

    def __init__(self, username, password):
        from siswa import Siswa
        from jurusan import Jurusan
        super().__init__()
        self.nama= username
        self.role= password

        self.setWindowTitle("Dashboard")
        self.resize(900, 650)

        layout=QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(0)

        header=QWidget()
        header.setFixedHeight(70)
        header_layout=QHBoxLayout()
        header_layout.setContentsMargins(20, 0, 20, 0)
        logo=QLabel("Dashboard")
        header_layout.addWidget(logo)
        header_layout.addStretch()
        name=QLabel(self.nama)
        keluar=QPushButton("Logout")
        keluar.setObjectName("keluar")
        keluar.clicked.connect(self.logout)
        header_layout.addWidget(name)
        header_layout.addSpacing(20)
        header_layout.addWidget(keluar)
        header.setLayout(header_layout)

        layout.addWidget(header)

        sidebar=QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sidebar_layout=QVBoxLayout()
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.addSpacing(10)
        dashboard_button=QPushButton("Dashboard")
        jurusan_button=QPushButton("Nama Jurusan")
        siswa_button=QPushButton("Daftar Siswa")
        
        sidebar_layout.addWidget(dashboard_button)
        sidebar_layout.addWidget(siswa_button)
        sidebar_layout.addWidget(jurusan_button)
        sidebar_layout.addStretch()
        sidebar_layout.addSpacing(10)
        sidebar.setLayout(sidebar_layout)

        header.setObjectName("header")

        self.pages=QStackedWidget()
        self.page_dashboard=self.halaman_dashboard()
        self.page_jurusan=Jurusan()
        self.page_siswa=Siswa()

        self.pages.addWidget(self.page_dashboard)
        self.pages.addWidget(self.page_jurusan)
        self.pages.addWidget(self.page_siswa)
    
        body= QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        body.addWidget(sidebar)
        body.addWidget(self.pages)
        layout.addLayout(body)

        central=QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
        

        dashboard_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.page_dashboard)
        )
        jurusan_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.page_jurusan)
        )
        siswa_button.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.page_siswa)
        )

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }

            QWidget#header {
                background-color: #1e293b;
            }

            QWidget#sidebar {
                background-color: #0f172a;
            }

            QLabel {
                font-size: 20px;
                color: white;
            }

            QLabel#page_title{
                color:black;
                font-size: 20px;
                font-weight: bold;
            }

            QPushButton {
                padding: 10px;
                border-radius: 6px;
                background-color: navy;
                color: white;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #2563eb;
            }

            QPushButton#keluar {
                background-color: red;
                font-size: 18px;
            }

            QPushButton#keluar:hover {
                background-color: darkred;
            }
        """)

    def halaman_dashboard(self):
        page = QWidget()
        layout = QVBoxLayout()
        label = QLabel("Selamat datang di Dashboard")
        label.setObjectName("page_title")
        label.setAlignment(Qt.AlignTop)
        layout.addWidget(label)
        page.setLayout(layout)
        return page

    def logout(self):
        from login import Login
        self.login=Login()
        self.login.show()
        self.close()



if __name__ == "__main__":
    app=QApplication([])
    window=Dashboard()
    window.show()
    app.exec()