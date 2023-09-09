from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal
import classifier
import sys

class MyUI(QtWidgets.QWidget):
    work_requested = pyqtSignal(str, str) 

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

        # Select Photo Button
        self.h_layout = QtWidgets.QHBoxLayout(self)
        self.btn_to_select_photo = QtWidgets.QPushButton(self)
        self.btn_to_select_photo.setText("Select Photo")
        self.label_of_select_photo_btn = QtWidgets.QLabel(self)
        self.label_of_select_photo_btn.setText("")
        self.h_layout.addWidget(self.btn_to_select_photo)
        self.h_layout.addWidget(self.label_of_select_photo_btn)
        self.v_layout.addItem(self.h_layout)
        self.btn_to_select_photo.clicked.connect(self.show_select_photo)

        # Select Folder Button
        self.h_layout1 = QtWidgets.QHBoxLayout(self)
        self.btn_to_select_folder = QtWidgets.QPushButton(self)
        self.btn_to_select_folder.setText("Select Folder")
        self.label_of_select_folder_btn = QtWidgets.QLabel(self)
        self.label_of_select_folder_btn.setText("")
        self.h_layout1.addWidget(self.btn_to_select_folder)
        self.h_layout1.addWidget(self.label_of_select_folder_btn)
        self.v_layout.addItem(self.h_layout1)
        self.btn_to_select_folder.clicked.connect(self.show_select_folder)

        # Run Button
        self.btn_to_execute = QtWidgets.QPushButton(self)
        self.btn_to_execute.setText("Run")
        self.btn_to_execute.clicked.connect(self.start_find_duplicate_image)
        self.v_layout.addWidget(self.btn_to_execute)

        # "Duplicate" Label
        self.label = QtWidgets.QLabel(self)
        self.label.setText('Duplicate Image is at: ')
        self.v_layout.addWidget(self.label)

        # List
        self.listwidget = QtWidgets.QListWidget(self)
        self.v_layout.addWidget(self.listwidget)

        # Progress Bar
        self.bar = QtWidgets.QProgressBar(self)
        self.bar.setRange(0, 100)
        self.v_layout.addWidget(self.bar)

        # QThread
        self.worker = classifier.Classifier()
        self.worker_thread = QThread()
        self.worker.process.connect(self.progress_bar_update)
        self.worker.found.connect(self.image_find)
        self.work_requested.connect(self.worker.classify)
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()

    def show_select_photo(self):
        filePath , filterType = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select Photo')
        self.select_photo = ' '.join(filePath)
        self.label_of_select_photo_btn.setText(f"{self.select_photo}")

    def show_select_folder(self):
        filePath = str(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory'))
        self.select_folder = filePath
        self.label_of_select_folder_btn.setText(f"{filePath}")

    def start_find_duplicate_image(self):
        if self.select_photo != '' and self.select_folder != '':
            self.listwidget.clear()
            self.work_requested.emit(self.select_photo, self.select_folder)

    def progress_bar_update(self, value):
        self.bar.setValue(value)

    def image_find(self, image):
        self.listwidget.addItem(image)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = MyUI()
    Form.show()
    sys.exit(app.exec())