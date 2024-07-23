import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QLabel, QDoubleSpinBox, QPushButton, QTabWidget,
                               QComboBox, QGroupBox, QFormLayout)
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QScatterSeries
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen

class UnitConverter:
    @staticmethod
    def mph_to_mpm(mph):
        return mph / 60
    
    @staticmethod
    def kmh_to_kpm(kmh):
        return kmh / 60
    
    @staticmethod
    def feet_to_km(feet):
        return feet * 0.0003048

    @staticmethod
    def feet_to_miles(feet):
        return feet / 5280

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
        
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["mph", "km/h"])
        self.unit_combo.currentIndexChanged.connect(self.update_units)

        input_layout.addRow("Drone speed:", self.drone_speed)
        input_layout.addRow("Radar range:", self.radar_range)
        input_layout.addRow("Reaction time (min):", self.reaction_time)
        input_layout.addRow("Units:", self.unit_combo)


        layout.addWidget(input_group)
        
        # Result labels
        self.result_label = QLabel('Result will be shown here')
        self.drone_speed_label = QLabel('Drone speed (mile per minute):')
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
        
        # Signals and slots
        self.drone_speed.valueChanged.connect(self.calculate)
        self.radar_range.valueChanged.connect(self.calculate)
        self.reaction_time.valueChanged.connect(self.calculate)
        
        self.calculate()

    def calculate(self):
        """
        Calculate the distance to intercept the drone
        """
        units = self.unit_combo.currentText()
        if units == "mph":
            mins_drone_speed = UnitConverter.mph_to_mpm(self.drone_speed.value())
            self.drone_speed_label.setText(f'Drone speed (mile per minute): {mins_drone_speed:.4f}')
            miles_delay_distance = mins_drone_speed * self.reaction_time.value()
            self.delay_distance_label.setText(f'Bad drone distance during delay (miles): {miles_delay_distance:.4f}')
            intercept_distance = self.radar_range.value() - miles_delay_distance
            intercept_possible = miles_delay_distance < self.radar_range.value()
            distance_unit = "miles"
        else:
            mins_drone_speed = UnitConverter.kmh_to_kpm(self.drone_speed.value())
            self.drone_speed_label.setText(f'Drone speed (kilometer per minute): {mins_drone_speed:.4f}')
            km_delay_distance = mins_drone_speed * self.reaction_time.value()
            self.delay_distance_label.setText(f'Bad drone distance during delay (kilometers): {km_delay_distance:.4f}')
            intercept_distance = self.radar_range.value() - km_delay_distance
            intercept_possible = km_delay_distance < self.radar_range.value()
            distance_unit = "kilometers"

        if intercept_possible:
            self.result_label.setText(f'We intercept the drone {intercept_distance:.2f} {distance_unit} away')
        else:
            suggestions = self.generate_suggestions(mins_drone_speed, intercept_distance, distance_unit)
            self.result_label.setText('We can\'t intercept the drone\n\n' + '\n'.join(suggestions))

        self.update_chart(mins_drone_speed, intercept_distance, intercept_possible, distance_unit)

    def generate_suggestions(self, mins_drone_speed, intercept_distance, distance_unit):
        """
        Generate suggestions for intercepting the drone
        """
        suggestions = ['Suggestions:']
        units = self.unit_combo.currentText()
        if units == "mph":
            required_drone_speed = (self.radar_range.value() / self.reaction_time.value()) * 60
            suggestions.append(f'Decrease drone speed to less than {required_drone_speed:.2f} mph')
        else:
            required_drone_speed = (self.radar_range.value() / self.reaction_time.value()) * 60
            suggestions.append(f'Decrease drone speed to less than {required_drone_speed:.2f} km/h')

        required_reaction_time = self.radar_range.value() / mins_drone_speed
        suggestions.append(f'Decrease reaction time to less than {required_reaction_time:.2f} minutes')

        required_radar_range = intercept_distance
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
        units = self.unit_combo.currentText()
        if units == "mph":
            self.drone_speed.setValue(self.drone_speed.value() * 1.60934)
            self.radar_range.setValue(self.radar_range.value() * 1.60934)
            self.drone_speed_label.setText('Drone speed (mile per minute):')
            self.delay_distance_label.setText('Delay distance (miles):')
        else:
            self.drone_speed.setValue(self.drone_speed.value() / 1.60934)
            self.radar_range.setValue(self.radar_range.value() / 1.60934)
            self.drone_speed_label.setText('Drone speed (kilometer per minute):')
            self.delay_distance_label.setText('Delay distance (kilometers):')
        self.calculate()
        
    def reset_to_default(self):
        """
        Reset input fields to default values
        """
        self.drone_speed.setValue(30)
        self.radar_range.setValue(2)
        self.reaction_time.setValue(5)
        self.calculate()
        
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

        self.unit_combo = QComboBox()
        self.unit_combo.addItems(["mph", "km/h"])
        self.unit_combo.currentIndexChanged.connect(self.update_units)

        input_layout.addRow("Car A speed:", self.speed_car_a)
        input_layout.addRow("Car B speed:", self.speed_car_b)
        input_layout.addRow("Initial distance (feet):", self.initial_distance)
        input_layout.addRow("Units:", self.unit_combo)

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
        
        # Signals and slots
        self.speed_car_a.valueChanged.connect(self.calculate)
        self.speed_car_b.valueChanged.connect(self.calculate)
        self.initial_distance.valueChanged.connect(self.calculate)
        
        self.calculate()

    def calculate(self):
        """
        Calculate the time until the cars collide
        """
        units = self.unit_combo.currentText()
        if units == "mph":
            speed_difference = self.speed_car_a.value() - self.speed_car_b.value()
            initial_distance_miles = UnitConverter.feet_to_miles(self.initial_distance.value())
            distance_unit = "miles"
        else:
            speed_difference = (self.speed_car_a.value() * 1.60934) - (self.speed_car_b.value() * 1.60934)
            initial_distance_miles = UnitConverter.feet_to_km(self.initial_distance.value())
            distance_unit = "kilometers"

        if speed_difference <= 0:
            self.result_label.setText("The cars will never collide.")
            self.update_chart(0, distance_unit)
            return

        # Convert speeds to feet per hour
        speed_difference_ft_per_hour = speed_difference * 5280

        # Calculate time to collision in hours
        time_to_collision_hours = initial_distance_miles / speed_difference_ft_per_hour

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
        initial_b_position = UnitConverter.feet_to_miles(self.initial_distance.value())
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
        units = self.unit_combo.currentText()
        if units == "mph":
            self.speed_car_a.setValue(self.speed_car_a.value() * 1.60934)
            self.speed_car_b.setValue(self.speed_car_b.value() * 1.60934)
            self.initial_distance.setValue(self.initial_distance.value() * 0.3048)
            self.result_label.setText('Result will be shown here')
        else:
            self.speed_car_a.setValue(self.speed_car_a.value() / 1.60934)
            self.speed_car_b.setValue(self.speed_car_b.value() / 1.60934)
            self.initial_distance.setValue(self.initial_distance.value() / 0.3048)
            self.result_label.setText('Result will be shown here')
        self.calculate()
        
    def reset_to_default(self):
        """
        Reset input fields to default values
        """
        self.speed_car_a.setValue(45)
        self.speed_car_b.setValue(27)
        self.initial_distance.setValue(200)
        self.calculate()
        
class MainWindow(QMainWindow):
    def __init__(self):
        """
        Main window with two tabs for the two problems
        """
        super().__init__()
        self.setWindowTitle('Two problems')

        # Create tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Create and add 'Drone intercept' tab
        drone_tab = DroneInterceptWindow()
        self.tab_widget.addTab(drone_tab, "Drone intercept")

        # Create and add 'Car collision' tab
        car_tab = CarCollisionWindow()
        self.tab_widget.addTab(car_tab, "Car collision")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())