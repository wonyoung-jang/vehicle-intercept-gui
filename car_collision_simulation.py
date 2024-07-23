from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QScatterSeries
from PySide6.QtCore import Qt, QTimer
from unit_converter import UnitConverter

class CarCollisionSimulation(QWidget):
    def __init__(self, speed_car_a, speed_car_b, initial_distance, units):
        super().__init__()
        self.speed_car_a = speed_car_a
        self.speed_car_b = speed_car_b
        self.initial_distance = initial_distance
        self.units = units
        self.time = 0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle("Car Collision Simulation")

        # Chart view
        self.chart_view = QChartView()
        layout.addWidget(self.chart_view)

        # Speed control
        speed_layout = QHBoxLayout()
        speed_label = QLabel("Simulation Speed:")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 100)
        self.speed_slider.setValue(50)
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_slider)
        layout.addLayout(speed_layout)

        # Initialize chart
        self.init_chart()

        # Timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(50)  # 20 fps

    def init_chart(self):
        self.chart = QChart()
        self.chart.setTitle("Car Collision Simulation")

        # Car A series
        self.car_a_series = QLineSeries()
        self.car_a_series.setName("Car A")

        # Car B series
        self.car_b_series = QLineSeries()
        self.car_b_series.setName("Car B")

        self.chart.addSeries(self.car_a_series)
        self.chart.addSeries(self.car_b_series)

        # Set up axes
        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        self.car_a_series.attachAxis(self.axis_x)
        self.car_a_series.attachAxis(self.axis_y)
        self.car_b_series.attachAxis(self.axis_x)
        self.car_b_series.attachAxis(self.axis_y)

        self.chart_view.setChart(self.chart)

    def update_simulation(self):
        speed_factor = self.speed_slider.value() / 50.0  # 1.0 is normal speed
        self.time += 0.05 * speed_factor  # 0.05 seconds per frame at normal speed

        # Update car positions
        if self.units == "mph":
            car_a_position = UnitConverter.mph_to_mpm(self.speed_car_a) * self.time
            car_b_position = UnitConverter.feet_to_miles(self.initial_distance) + UnitConverter.mph_to_mpm(self.speed_car_b) * self.time
        else:
            car_a_position = UnitConverter.kmh_to_kpm(self.speed_car_a) * self.time
            car_b_position = UnitConverter.feet_to_km(self.initial_distance) + UnitConverter.kmh_to_kpm(self.speed_car_b) * self.time

        self.car_a_series.clear()
        self.car_a_series.append(self.time, car_a_position)

        self.car_b_series.clear()
        self.car_b_series.append(self.time, car_b_position)

        # Adjust axes
        self.axis_x.setRange(0, self.time)
        self.axis_y.setRange(0, max(car_a_position, car_b_position))

        # Check for collision
        if car_a_position >= car_b_position:
            self.timer.stop()
            collision_point = QScatterSeries()
            collision_point.append(self.time, car_a_position)
            self.chart.addSeries(collision_point)
            collision_point.attachAxis(self.axis_x)
            collision_point.attachAxis(self.axis_y)
