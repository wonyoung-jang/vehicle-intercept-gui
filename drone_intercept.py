from PySide6.QtWidgets import (QWidget, QVBoxLayout, 
                               QLabel, QDoubleSpinBox, QPushButton,
                               QComboBox, QGroupBox, QFormLayout)
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QScatterSeries
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen
from unit_converter import UnitConverter
from drone_intercept_simulation import DroneInterceptSimulation

class DroneInterceptWindow(QWidget):
    """
    1) Drone intercept problem
    - Radar intercept capability is 2 miles
    - Drones (bad guys = them, good guys = us) both travel at 30 mph
    - It takes us 5 minutes to react and get our drone up in the air
    - How far away do we intercept the drone?
    - What can we do to intercept the drone?
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

        self.drone_speed = QDoubleSpinBox()
        self.drone_speed.setValue(30)
        self.drone_speed.setRange(1, 1000)

        self.radar_range = QDoubleSpinBox()
        self.radar_range.setValue(2)
        self.radar_range.setRange(1, 100)

        self.reaction_time = QDoubleSpinBox()
        self.reaction_time.setValue(5)
        self.reaction_time.setRange(0, 60)
        
        self.speed_unit_combo = QComboBox()
        self.speed_unit_combo.addItems(["mph", "km/h", "ft/h", "m/min", "km/min", "ft/min", "m/s", "km/s", "ft/s"])
        self.speed_unit_combo.currentIndexChanged.connect(self.update_units)

        self.distance_unit_combo = QComboBox()
        self.distance_unit_combo.addItems(["miles", "km", "feet"])
        self.distance_unit_combo.currentIndexChanged.connect(self.update_units)
        
        input_layout.addRow("Drone speed:", self.drone_speed)
        input_layout.addRow("Speed units:", self.speed_unit_combo)
        input_layout.addRow("Radar range:", self.radar_range)
        input_layout.addRow("Distance units:", self.distance_unit_combo)
        input_layout.addRow("Reaction time (min):", self.reaction_time)

        layout.addWidget(input_group)
        
        # Result labels
        self.result_label = QLabel('Result will be shown here')
        self.drone_speed_label = QLabel('Drone speed (mph):')
        self.delay_distance_label = QLabel('Delay distance (miles):')

        result_group = QGroupBox("Results")
        result_layout = QVBoxLayout(result_group)
        result_layout.addWidget(self.result_label)
        result_layout.addWidget(self.drone_speed_label)
        result_layout.addWidget(self.delay_distance_label)

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
        self.drone_speed.valueChanged.connect(self.calculate)
        self.radar_range.valueChanged.connect(self.calculate)
        self.reaction_time.valueChanged.connect(self.calculate)
        
        self.calculate()

    def calculate(self):
        """
        Calculate the intercept distance and update the result labels
        """
        speed_unit = self.speed_unit_combo.currentText()
        distance_unit = self.distance_unit_combo.currentText()
        
        drone_speed_mph = UnitConverter.to_miles_per_hour(self.drone_speed.value(), speed_unit)
        radar_range_miles = UnitConverter.to_miles(self.radar_range.value(), distance_unit)
        
        mins_drone_speed = drone_speed_mph / 60
        self.drone_speed_label.setText(f'Drone speed (mph): {drone_speed_mph:.4f}')
        
        miles_delay_distance = mins_drone_speed * self.reaction_time.value()
        delay_distance = UnitConverter.from_miles_to_unit(miles_delay_distance, distance_unit)
        self.delay_distance_label.setText(f'Bad drone distance during delay ({distance_unit}): {delay_distance:.4f}')
        
        intercept_distance = radar_range_miles - miles_delay_distance
        intercept_possible = miles_delay_distance < radar_range_miles

        if intercept_possible:
            intercept_distance_in_unit = UnitConverter.from_miles_to_unit(intercept_distance, distance_unit)
            self.result_label.setText(f'We intercept the drone {intercept_distance_in_unit:.2f} {distance_unit} away')
        else:
            suggestions = self.generate_suggestions(drone_speed_mph, intercept_distance, distance_unit)
            self.result_label.setText('We can\'t intercept the drone\n\n' + '\n'.join(suggestions))

        self.update_chart(mins_drone_speed, intercept_distance, intercept_possible, distance_unit)

    def generate_suggestions(self, drone_speed_mph, intercept_distance, distance_unit):
        """
        Generate suggestions for intercepting the drone
        """
        suggestions = ['Suggestions:']
        required_drone_speed = (self.radar_range.value() / self.reaction_time.value()) * 60
        suggestions.append(f'Decrease drone speed to less than {required_drone_speed:.2f} {self.speed_unit_combo.currentText()}')

        required_reaction_time = self.radar_range.value() / (drone_speed_mph / 60)
        suggestions.append(f'Decrease reaction time to less than {required_reaction_time:.2f} minutes')

        required_radar_range = UnitConverter.from_miles_to_unit(abs(intercept_distance), distance_unit)
        suggestions.append(f'Increase radar range to more than {required_radar_range:.2f} {distance_unit}')

        return suggestions
                    
    def update_chart(self, mins_drone_speed, intercept_distance, intercept_possible, distance_unit):
        """
        Update the chart with the new intercept distance
        """
        chart = QChart()
        chart.setTitle("Drone Intercept Visualization")
        max_time = max(self.reaction_time.value() * 2, self.radar_range.value() / mins_drone_speed)

        # Series for radar range
        radar_series = QLineSeries()
        radar_series.setName("Radar Range")
        radar_series.append(0, self.radar_range.value())
        radar_series.append(self.reaction_time.value() * 2, self.radar_range.value())

        # Series for drone position
        drone_series = QLineSeries()
        drone_series.setName("Drone Position")
        drone_series.append(0, 0)
        drone_series.append(max_time, max_time * mins_drone_speed)
        max_distance = max(self.radar_range.value(), mins_drone_speed * max_time)

        # Intercept point
        intercept_series = QScatterSeries()
        intercept_series.setName("Intercept Point")
        if intercept_possible:
            intercept_time = (self.radar_range.value() - intercept_distance) / mins_drone_speed
            intercept_series.append(intercept_time, self.radar_range.value())

        # Set colors based on intercept possibility
        color = QColor(Qt.green) if intercept_possible else QColor(Qt.red)
        pen = QPen(color)
        pen.setWidth(3)
        radar_series.setPen(pen)
        drone_series.setPen(pen)
        intercept_series.setColor(QColor(Qt.blue))
        intercept_series.setMarkerSize(15)

        chart.addSeries(radar_series)
        chart.addSeries(drone_series)
        chart.addSeries(intercept_series)
        
        # Create and configure x-axis
        axis_x = QValueAxis()
        axis_x.setTitleText("Time (minutes)")
        axis_x.setRange(0, max_time)
        axis_x.setTickCount(10)
        axis_x.setGridLineVisible(True)

        # Create and configure y-axis
        axis_y = QValueAxis()
        axis_y.setTitleText(f"Distance ({distance_unit})")
        axis_y.setRange(0, max_distance)
        axis_y.setTickCount(10)
        axis_y.setGridLineVisible(True)

        # Add axes to the chart
        chart.addAxis(axis_x, Qt.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignLeft)
        
        # Attach series to the axes
        radar_series.attachAxis(axis_x)
        radar_series.attachAxis(axis_y)
        drone_series.attachAxis(axis_x)
        drone_series.attachAxis(axis_y)
        intercept_series.attachAxis(axis_x)
        intercept_series.attachAxis(axis_y)

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
        self.drone_speed.setValue(30)
        self.radar_range.setValue(2)
        self.reaction_time.setValue(5)
        self.speed_unit_combo.setCurrentIndex(0)
        self.distance_unit_combo.setCurrentIndex(0)
        self.calculate()
        
    def start_simulation(self):
        """
        Start the drone intercept simulation
        """
        # Get current values
        speed_unit = self.speed_unit_combo.currentText()
        distance_unit = self.distance_unit_combo.currentText()
        drone_speed_mph = UnitConverter.to_miles_per_hour(self.drone_speed.value(), speed_unit)
        radar_range_miles = UnitConverter.to_miles(self.radar_range.value(), distance_unit)

        # Create and show simulation window
        self.sim_window = DroneInterceptSimulation(drone_speed_mph, radar_range_miles, self.reaction_time.value(), "mph")
        self.sim_window.show()
