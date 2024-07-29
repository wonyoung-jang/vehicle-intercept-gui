from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QScatterSeries
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPen
from unit_converter import UnitConverter


class CarCollisionSimulation(QWidget):
    def __init__(self, speed_car_a, speed_car_b, initial_distance, units):
        """
        Initialize the window

        Parameters:
            speed_car_a (float): The speed of Car A in miles per hour.
            speed_car_b (float): The speed of Car B in miles per hour.
            initial_distance (float): The initial distance between the cars in miles.
            units (str): The unit system used for the simulation (currently only "mph" is supported).
        """
        super().__init__()
        self.speed_car_a = speed_car_a
        self.speed_car_b = speed_car_b
        self.initial_distance = initial_distance
        self.units = units
        self.time = 0
        self.init_ui()

    def init_ui(self):
        """
        Initialize the UI
        """
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle("Car Collision Simulation")

        # Chart view
        self.chart_view = QChartView()

        # Speed control
        speed_layout = QHBoxLayout()
        speed_label = QLabel("Simulation Speed:")
        self.speed_slider = QSlider(Qt.Horizontal)

        # Layout setup
        layout.addWidget(self.chart_view)
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_slider)
        layout.addLayout(speed_layout)

        # Chart initialization
        self.init_chart()

        # Speed slider initialization
        self.speed_slider.setRange(1, 100)
        self.speed_slider.setValue(50)

        # Timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(50)  # 20 fps

    def init_chart(self):
        """
        Initialize the chart
        """
        # Car A series
        self.car_a_series = QLineSeries()
        self.car_a_series.setName("Car A")
        self.car_a_series.setPen(QPen(QColor(Qt.blue), 2))

        # Car B series
        self.car_b_series = QLineSeries()
        self.car_b_series.setName("Car B")
        self.car_b_series.setPen(QPen(QColor(Qt.red), 2))

        # Set up axes
        self.axis_x = QValueAxis()
        self.axis_x.setTitleText("Time (hours)")
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText(f"Distance ({self.units})")
        self.car_a_series.attachAxis(self.axis_x)
        self.car_a_series.attachAxis(self.axis_y)
        self.car_b_series.attachAxis(self.axis_x)
        self.car_b_series.attachAxis(self.axis_y)

        # Chart setup
        self.chart = QChart()
        self.chart.setTitle("Car Collision Simulation")
        self.chart.addSeries(self.car_a_series)
        self.chart.addSeries(self.car_b_series)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        # Attach series to axes

        # Set chart to view
        self.chart_view.setChart(self.chart)

    def update_simulation(self):
        """
        Update the simulation
        """
        # Speed of simulation setup
        speed_factor = self.speed_slider.value() / 50.0  # 1.0 is normal speed
        self.time += (
            0.0001 * speed_factor
        )  # 0.0001 hours (0.36 seconds) per frame at normal speed

        # Update car positions
        car_a_position = self.speed_car_a * self.time
        car_b_position = self.initial_distance + self.speed_car_b * self.time

        # Update series
        self.car_a_series.append(self.time, car_a_position)
        self.car_b_series.append(self.time, car_b_position)

        # Adjust axes
        self.axis_x.setRange(0, self.time)
        self.axis_y.setRange(0, max(car_a_position, car_b_position))

        # Check for collision
        if car_a_position >= car_b_position:
            self.timer.stop()
            collision_point = QScatterSeries()
            collision_point.append(self.time, car_a_position)
            collision_point.setMarkerSize(10)
            collision_point.setColor(QColor(Qt.green))
            self.chart.addSeries(collision_point)
            collision_point.attachAxis(self.axis_x)
            collision_point.attachAxis(self.axis_y)
