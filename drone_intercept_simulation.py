from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QScatterSeries
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPen
from unit_converter import UnitConverter

class DroneInterceptSimulation(QWidget):
    def __init__(self, drone_speed, radar_range, reaction_time, units):
        """
        Initialize the window
        """
        super().__init__()
        self.drone_speed = drone_speed
        self.radar_range = radar_range
        self.reaction_time = reaction_time
        self.units = units
        self.time = 0
        self.init_ui()

    def init_ui(self):
        """
        Initialize the UI
        """
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle("Drone Intercept Simulation")

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
        """
        Initialize the chart
        """
        self.chart = QChart()
        self.chart.setTitle("Drone Intercept Simulation")

        # Enemy drone series
        self.enemy_drone_series = QLineSeries()
        self.enemy_drone_series.setName("Enemy Drone")
        self.enemy_drone_series.setPen(QPen(QColor(Qt.red), 2))

        # Our drone series
        self.our_drone_series = QLineSeries()
        self.our_drone_series.setName("Our Drone")
        self.our_drone_series.setPen(QPen(QColor(Qt.blue), 2))

        self.chart.addSeries(self.enemy_drone_series)
        self.chart.addSeries(self.our_drone_series)

        # Set up axes
        self.axis_x = QValueAxis()
        self.axis_x.setTitleText("Time (minutes)")
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("Distance (miles)" if self.units == "mph" else "Distance (km)")
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        self.enemy_drone_series.attachAxis(self.axis_x)
        self.enemy_drone_series.attachAxis(self.axis_y)
        self.our_drone_series.attachAxis(self.axis_x)
        self.our_drone_series.attachAxis(self.axis_y)

        self.chart_view.setChart(self.chart)

    def update_simulation(self):
        """
        Update the simulation
        """
        speed_factor = self.speed_slider.value() / 50.0  # 1.0 is normal speed
        self.time += 0.05 * speed_factor

        # Update drone positions
        if self.units == "mph":
            enemy_drone_position = self.radar_range - UnitConverter.mph_to_mpm(self.drone_speed) * self.time
            our_drone_position = max(0, UnitConverter.mph_to_mpm(self.drone_speed) * (self.time - self.reaction_time))
        else:
            enemy_drone_position = self.radar_range - UnitConverter.kmh_to_kpm(self.drone_speed) * self.time
            our_drone_position = max(0, UnitConverter.kmh_to_kpm(self.drone_speed) * (self.time - self.reaction_time))

        self.enemy_drone_series.append(self.time, enemy_drone_position)
        self.our_drone_series.append(self.time, our_drone_position)

        # Adjust axes
        self.axis_x.setRange(0, self.time * 2)
        self.axis_y.setRange(0, self.radar_range * 2)

        # Check for interception
        if our_drone_position >= enemy_drone_position:
            self.timer.stop()
            intercept_point = QScatterSeries()
            intercept_point.append(self.time, enemy_drone_position)
            intercept_point.setMarkerSize(10)
            intercept_point.setColor(QColor(Qt.green))
            self.chart.addSeries(intercept_point)
            intercept_point.attachAxis(self.axis_x)
            intercept_point.attachAxis(self.axis_y)
