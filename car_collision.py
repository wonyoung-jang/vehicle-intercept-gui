from PySide6.QtWidgets import (QWidget, QVBoxLayout, 
                               QLabel, QDoubleSpinBox, QPushButton,
                               QComboBox, QGroupBox, QFormLayout)
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QScatterSeries
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen
from unit_converter import UnitConverter
from car_collision_simulation import CarCollisionSimulation

class CarCollisionWindow(QWidget):
    """
    2) Car collision problem
    - Car A is traveling 45 mph
    - Car B is traveling 27 mph
    - Car B is traveling in the same lane 200 feet in front of Car A
    - How long until the cars collide?    
    """
    def __init__(self):
        """
        Initialize the window
        """
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        Initialize the UI
        """
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Input fields
        input_group = QGroupBox("Input Parameters")
        input_layout = QFormLayout(input_group)

        self.speed_car_a = QDoubleSpinBox()
        self.speed_car_a.setValue(45)
        self.speed_car_a.setRange(0, 200)

        self.speed_car_b = QDoubleSpinBox()
        self.speed_car_b.setValue(27)
        self.speed_car_b.setRange(0, 200)

        self.initial_distance = QDoubleSpinBox()
        self.initial_distance.setValue(200)
        self.initial_distance.setRange(0, 1000)

        self.speed_unit_combo = QComboBox()
        self.speed_unit_combo.addItems(["mph", "km/h", "ft/h", "m/min", "km/min", "ft/min", "m/s", "km/s", "ft/s"])
        self.speed_unit_combo.currentIndexChanged.connect(self.update_units)

        self.distance_unit_combo = QComboBox()
        self.distance_unit_combo.addItems(["miles", "km", "feet"])
        self.distance_unit_combo.currentIndexChanged.connect(self.update_units)

        input_layout.addRow("Car A speed:", self.speed_car_a)
        input_layout.addRow("Car B speed:", self.speed_car_b)
        input_layout.addRow("Initial distance (feet):", self.initial_distance)
        input_layout.addRow("Speed units:", self.speed_unit_combo)
        input_layout.addRow("Initial distance:", self.initial_distance)
        input_layout.addRow("Distance units:", self.distance_unit_combo)

        layout.addWidget(input_group)

        # Result label
        self.result_label = QLabel('Result will be shown here')
        result_group = QGroupBox("Results")
        result_layout = QVBoxLayout(result_group)
        result_layout.addWidget(self.result_label)

        layout.addWidget(result_group)
        
        # Chart
        self.chart_view = QChartView()
        layout.addWidget(self.chart_view)
        
        # Reset button
        reset_button = QPushButton("Reset to Default")
        reset_button.clicked.connect(self.reset_to_default)
        layout.addWidget(reset_button)
        
        # Simulation button
        self.start_simulation_button = QPushButton("Start Simulation")
        self.start_simulation_button.clicked.connect(self.start_simulation)
        layout.addWidget(self.start_simulation_button)
        
        # Signals and slots
        self.speed_car_a.valueChanged.connect(self.calculate)
        self.speed_car_b.valueChanged.connect(self.calculate)
        self.initial_distance.valueChanged.connect(self.calculate)
        
        self.calculate()

    def calculate(self):
        """
        Calculate the time to collision and update the result label
        """
        speed_unit = self.speed_unit_combo.currentText()
        distance_unit = self.distance_unit_combo.currentText()
        
        speed_car_a_mph = UnitConverter.to_miles_per_hour(self.speed_car_a.value(), speed_unit)
        speed_car_b_mph = UnitConverter.to_miles_per_hour(self.speed_car_b.value(), speed_unit)
        initial_distance_miles = UnitConverter.to_miles(self.initial_distance.value(), distance_unit)

        speed_difference = speed_car_a_mph - speed_car_b_mph

        if speed_difference <= 0:
            self.result_label.setText("The cars will never collide.")
            self.update_chart(0, distance_unit)
            return

        # Calculate time to collision in hours
        time_to_collision_hours = initial_distance_miles / speed_difference

        # Convert time to minutes and seconds
        total_seconds = time_to_collision_hours * 3600
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)

        self.result_label.setText(f"The cars will collide in {minutes} minutes and {seconds} seconds.")
        self.update_chart(time_to_collision_hours, distance_unit)
        
    def update_chart(self, time_to_collision, distance_unit):
        """
        Update the chart with the new time to collision
        """
        chart = QChart()
        chart.setTitle("Car Collision Visualization")
        max_time = time_to_collision * 1.5 if time_to_collision > 0 else 1

        # Series for Car A
        series_a = QLineSeries()
        series_a.setName("Car A")
        series_a.append(0, 0)
        series_a.append(max_time, self.speed_car_a.value() * max_time)

        # Series for Car B
        series_b = QLineSeries()
        series_b.setName("Car B")
        initial_b_position = UnitConverter.from_miles_to_unit(self.initial_distance.value(), distance_unit)
        series_b.append(0, initial_b_position)
        series_b.append(max_time, initial_b_position + self.speed_car_b.value() * max_time)
        max_distance = max(self.speed_car_a.value() * max_time, 
            initial_b_position + self.speed_car_b.value() * max_time)

        # Collision point
        collision_series = QScatterSeries()
        collision_series.setName("Collision Point")
        if time_to_collision > 0:
            collision_series.append(time_to_collision, self.speed_car_a.value() * time_to_collision)
        
        # Set colors
        series_a.setPen(QPen(QColor(Qt.blue), 2))
        series_b.setPen(QPen(QColor(Qt.red), 2))
        collision_series.setColor(QColor(Qt.green))
        collision_series.setMarkerSize(15)
        
        chart.addSeries(series_a)
        chart.addSeries(series_b)
        chart.addSeries(collision_series)
        
        # Create and configure x-axis
        axis_x = QValueAxis()
        axis_x.setTitleText("Time (hours)")
        axis_x.setRange(0, max_time)
        axis_x.setTickCount(10)
        axis_x.setGridLineVisible(True)

        chart.addAxis(axis_x, Qt.AlignBottom)

        # Create and configure y-axis
        axis_y = QValueAxis()
        axis_y.setTitleText(f"Distance ({distance_unit})")
        axis_y.setRange(0, max_distance)
        axis_y.setTickCount(10)
        axis_y.setGridLineVisible(True)

        chart.addAxis(axis_y, Qt.AlignLeft)
        
        # Attach series to the axes
        series_a.attachAxis(axis_x)
        series_b.attachAxis(axis_x)
        collision_series.attachAxis(axis_x)
        series_a.attachAxis(axis_y)
        series_b.attachAxis(axis_y)
        collision_series.attachAxis(axis_y)

        self.chart_view.setChart(chart)
        
    def update_units(self):
        """
        Update the units of the input fields and result labels
        """
        self.calculate()
        
    def reset_to_default(self):
        """
        Reset input fields to default values
        """
        self.speed_car_a.setValue(45)
        self.speed_car_b.setValue(27)
        self.initial_distance.setValue(200)
        self.speed_unit_combo.setCurrentIndex(0)
        self.distance_unit_combo.setCurrentIndex(0)
        self.calculate()
    
    def start_simulation(self):
        """
        Start the car collision simulation
        """
        # Get current values
        speed_unit = self.speed_unit_combo.currentText()
        distance_unit = self.distance_unit_combo.currentText()
        speed_car_a_mph = UnitConverter.to_miles_per_hour(self.speed_car_a.value(), speed_unit)
        speed_car_b_mph = UnitConverter.to_miles_per_hour(self.speed_car_b.value(), speed_unit)
        initial_distance_miles = UnitConverter.to_miles(self.initial_distance.value(), distance_unit)

        # Create and show simulation window
        self.sim_window = CarCollisionSimulation(speed_car_a_mph, speed_car_b_mph, initial_distance_miles, "mph")
        self.sim_window.show()
