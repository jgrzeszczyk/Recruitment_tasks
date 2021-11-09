from datetime import datetime
from PyQt5.QtWidgets import QApplication, QPushButton, QButtonGroup, QMainWindow
from PyQt5.QtCore import QObject, QThread, pyqtSignal


class Worker(QObject):
    def __init__(self, func, **kwargs):
        super().__init__()
        self.func = func
        self.func_kwargs = kwargs

    finished = pyqtSignal()

    def run(self):
        """Long-running task."""
        self.func(self.func_kwargs)
        self.finished.emit()


class TrafficLight:
    def __init__(self):
        self.state = 1
        self.pedestrian_btn = False
        self.car_light = 'red'
        self.pedestrian_light = 'green'
        self.run_time = 0
        self.init_time = datetime.now()
        self.worker = Worker(func=self.run)

    def change_lights(self, state) -> None:
        """Changes lights' colors according to current state"""
        lights_states = {
            1: {'pedestrian_light': 'green',
                'car_light': 'red'},
            2: {'pedestrian_light': 'red',
                'car_light': 'green'},
            3: {'pedestrian_light': 'red',
                'car_light': 'yellow'}
        }
        self.state = state
        self.car_light = lights_states[self.state]['car_light']
        self.pedestrian_light = lights_states[self.state]['pedestrian_light']
        self.update_state_info()

    def change_state(self, dst_state: int, delay: int) -> None:
        """Changes state to dst_state after passed delay time"""
        current_delay = 0
        timer = datetime.now()
        while current_delay < delay:
            passed_time = datetime.now() - timer
            current_delay = passed_time.seconds
            if self.state == 2 and self.pedestrian_btn:
                self.pedestrian_btn = False
                print('Pedestrian btn clicked!')
                break
        self.state = dst_state
        self.run_time = (datetime.now() - self.init_time).seconds
        self.change_lights(state=self.state)

    def run(self) -> None:
        """Runs state machine algorithm"""
        while True:
            self.run_time = (datetime.now() - self.init_time).seconds
            self.change_state(dst_state=2, delay=10)
            self.change_state(dst_state=3, delay=20)
            self.change_state(dst_state=1, delay=2)

    def update_state_info(self) -> None:
        """Prints current state information"""
        print(f'{self.run_time} seconds | State {self.state} -> '
              f'Pedestrian light: {self.pedestrian_light}'
              f' | Car light: {self.car_light}')


class LightsGUI(QMainWindow):
    def __init__(self, engine: TrafficLight):
        super().__init__()
        self.setGeometry(30, 30, 400, 200)
        self.init_ui()
        self.engine = engine

    def init_ui(self) -> None:
        """GUI initialization"""
        self.button1 = QPushButton(self)
        self.button1.setGeometry(40, 40, 120, 50)
        self.button1.setText("Start")

        self.button2 = QPushButton(self)
        self.button2.setGeometry(200, 40, 120, 50)
        self.button2.setText("Pedestrian btn")

        self.btn_grp = QButtonGroup()
        self.btn_grp.setExclusive(True)
        self.btn_grp.addButton(self.button1)
        self.btn_grp.addButton(self.button2)

        self.btn_grp.buttonClicked.connect(self.on_click)

        # TODO: Add text box for logs inside GUI

        self.show()

    def on_click(self, btn: QPushButton) -> None:
        if btn.text() == 'Start':
            print('System started!')
            self.button1.setEnabled(False)
            self.run_state_machine()
        elif btn.text() == 'Pedestrian btn':
            self.engine.pedestrian_btn = True

    def run_state_machine(self) -> None:
        """Threading to avoid GUI freezing"""

        # Create a QThread object
        self.thread = QThread()
        #  Create a worker object
        self.worker = self.engine.worker
        # Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Start the thread
        self.thread.start()


def main():
    light = TrafficLight()
    app = QApplication([])
    ex = LightsGUI(engine=light)
    app.exec()


if __name__ == "__main__":
    main()
