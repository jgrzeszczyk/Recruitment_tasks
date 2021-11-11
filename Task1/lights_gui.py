from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QButtonGroup, QVBoxLayout, QGroupBox, QGridLayout, QDialog, QTextEdit
from traffic_lights import TrafficLight
from Utils.utils import Worker, CustomThread


class LightsGUI(QDialog):
    def __init__(self, engine: TrafficLight):
        super().__init__()
        self.setGeometry(30, 30, 400, 200)
        self.title = 'Traffic lights system'
        self.init_ui()
        self.engine = engine
        self.worker = Worker(func=self.engine.run, update_logs_func=self.update_console_logs)
        self.threading = CustomThread(worker=self.worker)

    def init_ui(self) -> None:
        """GUI initialization"""
        self.setWindowTitle(self.title)
        self.setGeometry(500, 500, 400, 200)
        self.layout = QVBoxLayout()

        self.button_box = QGroupBox('Control Panel')
        control_box_layout = QGridLayout()

        # Start button
        self.start_btn = QPushButton(self)
        self.start_btn.setGeometry(40, 40, 120, 50)
        self.start_btn.setText("Start")

        # Pedestrian button
        self.pedestrian_btn = QPushButton(self)
        self.pedestrian_btn.setGeometry(200, 40, 120, 50)
        self.pedestrian_btn.setText("Pedestrian btn")

        self.btn_grp = QButtonGroup()
        self.btn_grp.setExclusive(True)
        self.btn_grp.addButton(self.start_btn)
        self.btn_grp.addButton(self.pedestrian_btn)

        control_box_layout.addWidget(self.start_btn, 0, 0)
        control_box_layout.addWidget(self.pedestrian_btn, 0, 1)
        self.button_box.setLayout(control_box_layout)
        self.layout.addWidget(self.button_box, alignment=Qt.AlignBottom)
        self.btn_grp.buttonClicked.connect(self.on_click)

        # Text area for console logs
        self.info_area = QTextEdit()
        self.info_area.setObjectName('Console logs')
        self.info_area.setReadOnly(True)
        self.layout.addWidget(self.info_area, alignment=Qt.AlignTop)

        self.setLayout(self.layout)
        self.show()

    def on_click(self, btn: QPushButton) -> None:
        if btn.text() == 'Start':
            print('System started!')
            self.start_btn.setEnabled(False)
            self.threading.run_task()  # runs state machine
        elif btn.text() == 'Pedestrian btn':
            self.engine.pedestrian_btn = True

    def update_console_logs(self, data):
        self.info_area.append(data)
        self.info_area.ensureCursorVisible()
