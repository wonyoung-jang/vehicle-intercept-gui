from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QScatterSeries
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPen
from unit_converter import UnitConverter


class DroneInterceptSimulation(QWidget):
    def __init__(self, drone_speed, radar_range, reaction_time):
        """
        Initialize the window

        Parameters:
            drone_speed (float): The speed of both drones in miles per hour.
            radar_range (float): The radar detection range in miles.
            reaction_time (float): The time it takes for the friendly drone to react and launch, in minutes.
        """
        super().__init__()
        self.drone_speed = drone_speed
        self.radar_range = radar_range
        self.reaction_time = reaction_time
        self.time = -reaction_time
        self.starting_y = self.radar_range + ((self.drone_speed / 60) * abs(self.time))

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

    def init_chart(self):
        """
        Initialize the chart
        """
        # Enemy drone series
        self.enemy_drone_series = QLineSeries()
        self.enemy_drone_series.setName("Enemy Drone")
        self.enemy_drone_series.setPen(QPen(QColor(Qt.darkMagenta), 2, Qt.DashLine))

        # Our drone series
        self.our_drone_series = QLineSeries()
        self.our_drone_series.setName("Our Drone")
        self.our_drone_series.setPen(QPen(QColor(Qt.darkBlue), 2, Qt.DashLine))
        
        # Radar range series
        self.radar_range_series = QLineSeries()
        self.radar_range_series.setName("Radar Range")
        self.radar_range_series.setPen(QPen(QColor(Qt.darkGreen), 2, Qt.DashLine))
        self.radar_range_series.append(-self.reaction_time, self.radar_range)
        self.radar_range_series.append(self.reaction_time * 2, self.radar_range)

        # Set up axes
        self.axis_x = QValueAxis()
        self.axis_x.setTitleText("Time (minutes)")
        self.axis_y = QValueAxis()
        self.axis_y.setTitleText("Distance (miles)")

        # Chart setup
        self.chart = QChart()
        self.chart.setTitle("Drone Intercept Simulation")
        self.chart.addSeries(self.radar_range_series)
        self.chart.addSeries(self.enemy_drone_series)
        self.chart.addSeries(self.our_drone_series)
        self.chart.addAxis(self.axis_x, Qt.AlignBottom)
        self.chart.addAxis(self.axis_y, Qt.AlignLeft)

        # Attach series to axes
        self.enemy_drone_series.attachAxis(self.axis_x)
        self.enemy_drone_series.attachAxis(self.axis_y)
        self.our_drone_series.attachAxis(self.axis_x)
        self.our_drone_series.attachAxis(self.axis_y)
        self.radar_range_series.attachAxis(self.axis_x)
        self.radar_range_series.attachAxis(self.axis_y)

        # Set chart to view
        self.chart_view.setChart(self.chart)

    def update_simulation(self):
        """
        Update the simulation
        """
        # Speed of simulation setup
        speed_factor = self.speed_slider.value() / 50.0
        self.time += 0.05 * speed_factor
        
        # Update drone positions
        if self.time > 0:
            enemy_drone_position = self.radar_range - ((self.drone_speed / 60) * self.time)

            our_drone_position = max(
                0, (self.drone_speed / 60) * (self.time - self.reaction_time)
            )
        else:
            enemy_drone_position = self.radar_range + ((self.drone_speed / 60) * abs(self.time))
            our_drone_position = 0
        
        # Update series
        self.enemy_drone_series.append(self.time, enemy_drone_position)
        self.our_drone_series.append(self.time, our_drone_position)

        # Adjust axes
        self.axis_x.setRange(-self.reaction_time, self.reaction_time * 2)
        self.axis_y.setRange(-self.radar_range, self.starting_y)
        
        # Check for detection
        if enemy_drone_position <= self.radar_range:
            self.radar_range_series.setPen(QPen(QColor(Qt.green), 3))
            self.enemy_drone_series.setPen(QPen(QColor(Qt.magenta), 3))
            
        # Check for our drone launch
        if our_drone_position > 0:
            self.our_drone_series.setPen(QPen(QColor(Qt.blue), 3))

        # Check for interception
        if our_drone_position >= enemy_drone_position:
            if our_drone_position > 0:
                self.timer.stop()
                intercept_point = QScatterSeries()
                intercept_point.setName("Intercept")
                intercept_point.append(self.time, enemy_drone_position)
                intercept_point.setMarkerSize(10)
                intercept_point.setColor(QColor(Qt.green))

                self.chart.addSeries(intercept_point)
                intercept_point.attachAxis(self.axis_x)
                intercept_point.attachAxis(self.axis_y)
            else:
                self.timer.stop()
                intercept_point = QScatterSeries()
                intercept_point.setName("Not intercepted")
                intercept_point.append(self.time, enemy_drone_position)
                intercept_point.setMarkerSize(10)
                intercept_point.setColor(QColor(Qt.red))

                self.chart.addSeries(intercept_point)
                intercept_point.attachAxis(self.axis_x)
                intercept_point.attachAxis(self.axis_y)
