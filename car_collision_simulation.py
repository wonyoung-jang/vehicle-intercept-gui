from PySide6.QtWidgets import QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QScatterSeries
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPen
from simulation import Simulation
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
)


class CarCollisionSimulation(Simulation):
    # Log initialization
    logging.info("CarCollisionSimulation initialized")

    def __init__(self, problem, speed_car_a, speed_car_b, initial_distance) -> None:
        """
        Initialize the window

        Parameters:
            speed_car_a (float): The speed of Car A in miles per hour.
            speed_car_b (float): The speed of Car B in miles per hour.
            initial_distance (float): The initial distance between the cars in miles.
        """
        super().__init__(problem, speed_car_a, speed_car_b, initial_distance)
        self.problem = problem
        self.speed_car_a = speed_car_a
        self.speed_car_b = speed_car_b
        self.initial_distance = initial_distance
        self.time = 0

    def init_ui(self) -> None:
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
        self.timer.start(50)

    def init_chart(self) -> None:
        """
        Initialize the chart
        """
        # Car A series
        self.car_a_series = QLineSeries()
        self.car_a_series.setName("Car A")
        self.car_a_series.setPen(QPen(QColor(Qt.blue), 2, Qt.DashLine))

        # Car B series
        self.car_b_series = QLineSeries()
        self.car_b_series.setName("Car B")
        self.car_b_series.setPen(QPen(QColor(Qt.red), 2, Qt.DashLine))

        # Set up axes
        self.axis_x = QValueAxis()
        self.axis_x.setTitleText("Time (hours)")
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText(f"Distance (miles)")

        # Chart setup
        self.chart = QChart()
        self.chart.setTitle("Car Collision Simulation")
        self.chart.addSeries(self.car_a_series)
        self.chart.addSeries(self.car_b_series)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        # Attach series to axes
        self.car_a_series.attachAxis(self.axis_x)
        self.car_a_series.attachAxis(self.axis_y)
        self.car_b_series.attachAxis(self.axis_x)
        self.car_b_series.attachAxis(self.axis_y)

        # Set chart to view
        self.chart_view.setChart(self.chart)

    def update_simulation(self) -> None:
        """
        Update the simulation
        """
        
        # Speed of simulation setup
        speed_factor = self.speed_slider.value() / 50.0
        self.time += 0.005 * speed_factor

        # Update car positions
        car_a_position = (self.speed_car_a / 60) * self.time
        car_b_position = ((self.speed_car_b / 60) * self.time) + self.initial_distance

        # Update series
        self.car_a_series.append(self.time, car_a_position)
        self.car_b_series.append(self.time, car_b_position)

        # Adjust axes
        self.axis_x.setRange(0, self.time * 2)
        self.axis_y.setRange(0, self.initial_distance + car_a_position)

        # Check for collision
        if car_a_position >= car_b_position:
            self.timer.stop()
            self.car_a_series.setPen(QPen(QColor(Qt.blue), 3))
            self.car_b_series.setPen(QPen(QColor(Qt.red), 3))
            collision_point = QScatterSeries()
            collision_point.setName("Collision")
            collision_point.append(self.time, car_a_position)
            collision_point.setMarkerSize(10)
            collision_point.setColor(QColor(Qt.green))
            self.chart.addSeries(collision_point)
            collision_point.attachAxis(self.axis_x)
            collision_point.attachAxis(self.axis_y)
