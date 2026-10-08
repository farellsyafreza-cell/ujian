import PySide6.QtWidgets as QtWidgets
from PySide6.QtCore import Qt
from login import Login

if __name__ == "__main__":
   app=QtWidgets.QApplication([])
   window=Login()
   window.show()
   app.exec()
   
