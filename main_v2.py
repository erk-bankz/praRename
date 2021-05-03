from ui import Ui_Dialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QApplication
from pathlib import Path
import re
from PyQt5 import QtWidgets
import modules


class Dialog (QDialog, Ui_Dialog):
    """
    Copy and paste from ORT to excel or vice versa
    """
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
    #     self.pushButton.clicked.connect(self.buttonClicked)  # alternative way to call your method
    #
    # def buttonClicked(self):
    #     # write code

    @pyqtSlot()  # decorator
    def on_pushButton_clicked(self):
        fp = self.lineEdit.text()
        file_path = Path(self.lineEdit.text())
        if not fp.endswith("\\"):
            fp = fp+"\\"
        modules.removeHistory(file_path)
        modules.checkFolderStructure(file_path)
        try:
            modules.moveLPFolder(fp)
            modules.removePdGibberish(file_path)
            modules.extractTXLF(fp)
            modules.folderDestroyer(fp)
            modules.renameTXLF(fp)
            modules.destroySubFolders(fp)
            modules.createTargetFolders(fp)
            modules.moveTXLFtoTargetFolders(fp)
        except:
            e = sys.exc_info()
            QtWidgets.QMessageBox.critical(Dialog(), "Error", str(e[1]))
        QtWidgets.QMessageBox.information(Dialog(), "Macro finished",
                                          "Files has finished processing")

    def on_pushButton_2_clicked(self):
        Dialog.close(self)


if __name__ == "__main__":
    import sys
    application = QApplication(sys.argv)
    macro_dialog = Dialog() # create object of dialog, **use the name of your class (ie class Dialog)**
    macro_dialog.show()
    sys.exit(application.exec_())
