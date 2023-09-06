from PyQt6 import QtWidgets

class SelectButton(QtWidgets):
    def __init__(self) -> None:
        super.__init__(self)
        self.h_layout = QtWidgets.QHBoxLayout(self)
        self.btn_to_select_photo = QtWidgets.QPushButton(self)
        self.btn_to_select_photo.setText("Select Photo")
        self.label_of_select_photo_btn = QtWidgets.QLabel(self)
        self.label_of_select_photo_btn.setText("")
        self.h_layout.addWidget(self.btn_to_select_photo)
        self.h_layout.addWidget(self.label_of_select_photo_btn)
        self.v_layout.addItem(self.h_layout)
        self.btn_to_select_photo.clicked.connect(self.show_select_photo)