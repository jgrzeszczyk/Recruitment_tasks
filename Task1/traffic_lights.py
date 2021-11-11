from datetime import datetime
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSignal


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
        # self.state_info()

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

    def run(self, args=None) -> None:
        """Runs state machine algorithm"""
        update_logs_func = args['update_logs_func']
        while True:
            self.run_time = (datetime.now() - self.init_time).seconds
            self.change_state(dst_state=2, delay=10)
            update_logs_func(data=self.state_info())
            self.change_state(dst_state=3, delay=20)
            update_logs_func(data=self.state_info())
            self.change_state(dst_state=1, delay=2)
            update_logs_func(data=self.state_info())

    def state_info(self) -> str:
        """Returns current state information"""
        return (f'{self.run_time} seconds | State {self.state} -> '
                f'Pedestrian light: {self.pedestrian_light}'
                f' | Car light: {self.car_light}')


def run_gui(engine):
    from lights_gui import LightsGUI
    ex = LightsGUI(engine=engine)


def main():
    engine = TrafficLight()
    app = QApplication([])
    run_gui(engine)
    app.exec()


if __name__ == "__main__":
    main()
