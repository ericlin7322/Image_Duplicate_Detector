from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread
import classifier
import sys

class MyUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Duplicate Detector')
        self.resize(300, 200)
        self.setUpdatesEnabled(True)
        self.select_photo = ""
        self.select_folder = ""
        self.ui()

    def ui(self):

        self.v_layout = QtWidgets.QVBoxLayout(self)

        self.h_layout = QtWidgets.QHBoxLayout(self)
        self.btn_to_select_photo = QtWidgets.QPushButton(self)
        self.btn_to_select_photo.setText("Select Photo")
        self.label_of_select_photo_btn = QtWidgets.QLabel(self)
        self.label_of_select_photo_btn.setText("")
        self.h_layout.addWidget(self.btn_to_select_photo)
        self.h_layout.addWidget(self.label_of_select_photo_btn)
        self.v_layout.addItem(self.h_layout)
        self.btn_to_select_photo.clicked.connect(self.show_select_photo)

        self.h_layout1 = QtWidgets.QHBoxLayout(self)
        self.btn_to_select_folder = QtWidgets.QPushButton(self)
        self.btn_to_select_folder.setText("Select Folder")
        self.label_of_select_folder_btn = QtWidgets.QLabel(self)
        self.label_of_select_folder_btn.setText("")
        self.h_layout1.addWidget(self.btn_to_select_folder)
        self.h_layout1.addWidget(self.label_of_select_folder_btn)
        self.v_layout.addItem(self.h_layout1)
        self.btn_to_select_folder.clicked.connect(self.show_select_folder)


        self.btn_to_execute = QtWidgets.QPushButton(self)
        self.btn_to_execute.setText("Run")
        self.btn_to_execute.clicked.connect(self.run)
        self.v_layout.addWidget(self.btn_to_execute)


        self.label = QtWidgets.QLabel(self)
        self.label.setText('Duplicate Image is at: ')
        self.v_layout.addWidget(self.label)

        self.listwidget = QtWidgets.QListWidget(self)
        self.v_layout.addWidget(self.listwidget)

        self.bar = QtWidgets.QProgressBar(self)
        self.bar.setRange(0, 100)
        self.v_layout.addWidget(self.bar)

    def show_select_photo(self):
        filePath , filterType = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select Photo')  # 選擇檔案對話視窗
        self.select_photo = ' '.join(filePath)
        self.label_of_select_photo_btn.setText(f"{self.select_photo}")

    def show_select_folder(self):
        filePath = str(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory'))  # 選擇檔案對話視窗
        self.select_folder = filePath
        self.label_of_select_folder_btn.setText(f"{filePath}")

    def run(self):
        if self.select_photo != '' and self.select_folder != '':
            self.listwidget.clear()
            self.thread_a = QThread()
            self.thread_a.run = self.detect_duplicate
            self.thread_a.start() 
            self.bar.setRange(0, 0)

    def detect_duplicate(self):
        self.listwidget.addItems(classifier.Classifier().classify(self.select_photo, self.select_folder))
        self.bar.setRange(0, 100)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = MyUI()
    Form.show()
    sys.exit(app.exec())