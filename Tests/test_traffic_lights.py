import unittest
from Task1.traffic_lights import TrafficLight
import time


class TestTrafficLight(unittest.TestCase):
    def test_change_lights(self):
        """Tests if lights are being changed correctly"""
        traffic_lights = TrafficLight()

        traffic_lights.change_lights(2)
        self.assertEqual(traffic_lights.state, 2)
        self.assertEqual(traffic_lights.car_light, 'green')
        self.assertEqual(traffic_lights.pedestrian_light, 'red')

        traffic_lights.change_lights(3)
        self.assertEqual(traffic_lights.state, 3)
        self.assertEqual(traffic_lights.car_light, 'yellow')
        self.assertEqual(traffic_lights.pedestrian_light, 'red')

        traffic_lights.change_lights(1)
        self.assertEqual(traffic_lights.state, 1)
        self.assertEqual(traffic_lights.car_light, 'red')
        self.assertEqual(traffic_lights.pedestrian_light, 'green')

    def test_change_state(self):
        """Tests if state is being changed correctly including delay time"""
        traffic_lights = TrafficLight()

        start_time = time.time()
        traffic_lights.change_state(dst_state=2, delay=10)
        exec_time = time.time() - start_time
        self.assertEqual(traffic_lights.state, 2)
        self.assertAlmostEqual(exec_time, 10, places=2)

        start_time = time.time()
        traffic_lights.change_state(dst_state=3, delay=20)
        exec_time = time.time() - start_time
        self.assertEqual(traffic_lights.state, 3)
        self.assertAlmostEqual(exec_time, 20, places=2)

        start_time = time.time()
        traffic_lights.change_state(dst_state=1, delay=2)
        exec_time = time.time() - start_time
        self.assertEqual(traffic_lights.state, 1)
        self.assertAlmostEqual(exec_time, 2, places=2)

