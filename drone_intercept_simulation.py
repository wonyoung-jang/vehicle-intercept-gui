from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QScatterSeries
from PySide6.QtCore import Qt, QTimer
from unit_converter import UnitConverter

class DroneInterceptSimulation(QWidget):
    def __init__(self, drone_speed, radar_range, reaction_time, units):
        super().__init__()
        self.drone_speed = drone_speed
        self.radar_range = radar_range
        self.reaction_time = reaction_time
        self.units = units
        self.time = 0
        self.init_ui()

    def init_ui(self):
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
        self.chart = QChart()
        self.chart.setTitle("Drone Intercept Simulation")

        # Radar range line
        self.radar_series = QLineSeries()
        self.radar_series.setName("Radar Range")
        self.radar_series.append(0, self.radar_range)
        self.radar_series.append(self.reaction_time * 2, self.radar_range)

        # Drone position series
        self.drone_series = QLineSeries()
        self.drone_series.setName("Drone Position")

        # Our drone series
        self.our_drone_series = QLineSeries()
        self.our_drone_series.setName("Our Drone")

        self.chart.addSeries(self.radar_series)
        self.chart.addSeries(self.drone_series)
        self.chart.addSeries(self.our_drone_series)

        # Set up axes
        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        self.radar_series.attachAxis(self.axis_x)
        self.radar_series.attachAxis(self.axis_y)
        self.drone_series.attachAxis(self.axis_x)
        self.drone_series.attachAxis(self.axis_y)
        self.our_drone_series.attachAxis(self.axis_x)
        self.our_drone_series.attachAxis(self.axis_y)

        self.chart_view.setChart(self.chart)

    def update_simulation(self):
        speed_factor = self.speed_slider.value() / 50.0  # 1.0 is normal speed
        self.time += 0.05 * speed_factor  # 0.05 seconds per frame at normal speed

        # Update drone positions
        if self.units == "mph":
            drone_position = UnitConverter.mph_to_mpm(self.drone_speed) * self.time
            our_drone_position = max(0, UnitConverter.mph_to_mpm(self.drone_speed) * (self.time - self.reaction_time))
        else:
            drone_position = UnitConverter.kmh_to_kpm(self.drone_speed) * self.time
            our_drone_position = max(0, UnitConverter.kmh_to_kpm(self.drone_speed) * (self.time - self.reaction_time))

        self.drone_series.clear()
        self.drone_series.append(self.time, drone_position)

        self.our_drone_series.clear()
        self.our_drone_series.append(self.time, our_drone_position)

        # Adjust axes
        self.axis_x.setRange(0, max(self.time, self.reaction_time * 2))
        self.axis_y.setRange(0, max(self.radar_range, drone_position, our_drone_position))

        # Check for interception
        if our_drone_position >= drone_position and drone_position <= self.radar_range:
            self.timer.stop()
            intercept_point = QScatterSeries()
            intercept_point.append(self.time, drone_position)
            self.chart.addSeries(intercept_point)
            intercept_point.attachAxis(self.axis_x)
            intercept_point.attachAxis(self.axis_y)
