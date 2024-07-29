from PySide6.QtWidgets import (
    QVBoxLayout,
    QMessageBox,
    QLabel,
    QDoubleSpinBox,
    QComboBox,
    QGroupBox,
    QFormLayout,
)
from PySide6.QtCharts import QChart, QLineSeries, QValueAxis, QScatterSeries
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen
from unit_converter import UnitConverter
from simulation_window import SimulationWindow
from drone_intercept_simulation import DroneInterceptSimulation


class DroneInterceptWindow(SimulationWindow):
    """
    Original problem wording: Drone intercept
    - Radar intercept capability is 2 miles
    - Drones (bad guys = them, good guys = us) both travel at 30 mph
    - It takes us 5 minutes to react and get our drone up in the air
    - How far away do we intercept the drone?
    - (Follow-up) What can we do to intercept the drone?
    """

    def __init__(self):
        """
        Initialize the window
        """
        super().__init__()

    def create_input_group(self, layout):
        """
        Create the input group with input fields for drone speed, radar range, and reaction time

        Parameters:
            layout (QVBoxLayout): The layout to add the input group box to.
        """
        # Input fields
        self.drone_speed = QDoubleSpinBox()
        self.drone_speed.setRange(1.0, 999999.0)

        self.radar_range = QDoubleSpinBox()
        self.radar_range.setRange(1.0, 999999.0)

        self.reaction_time = QDoubleSpinBox()
        self.reaction_time.setRange(0.0, 999999.0)

        self.speed_unit_combo = QComboBox()
        self.speed_unit_combo.addItems(
            ["mph", "km/h", "ft/h", "m/min", "km/min", "ft/min", "m/s", "km/s", "ft/s"]
        )

        self.distance_unit_combo = QComboBox()
        self.distance_unit_combo.addItems(["miles", "km", "feet"])

        # Layout setup
        input_group = QGroupBox("Input Parameters")
        input_layout = QFormLayout(input_group)
        input_layout.addRow("Drone speed:", self.drone_speed)
        input_layout.addRow("Speed units:", self.speed_unit_combo)
        input_layout.addRow("Radar range:", self.radar_range)
        input_layout.addRow("Distance units:", self.distance_unit_combo)
        input_layout.addRow("Reaction time (min):", self.reaction_time)
        layout.addWidget(input_group)

        # Set default values
        self.drone_speed.setValue(30)
        self.radar_range.setValue(2)
        self.reaction_time.setValue(5)
        self.speed_unit_combo.setCurrentIndex(0)
        self.distance_unit_combo.setCurrentIndex(0)

        # Signals and slots
        self.drone_speed.valueChanged.connect(self.validate_and_calculate)
        self.radar_range.valueChanged.connect(self.validate_and_calculate)
        self.reaction_time.valueChanged.connect(self.validate_and_calculate)
        self.speed_unit_combo.currentIndexChanged.connect(self.update_units)
        self.distance_unit_combo.currentIndexChanged.connect(self.update_units)

    def create_result_group(self, layout):
        """
        Create the result group with labels for the result and drone speed

        Parameters:
            layout (QVBoxLayout): The layout to add the result group box to.
        """
        # Result labels
        self.result_label = QLabel("Result will be shown here")
        self.drone_speed_label = QLabel("Drone speed (mph):")
        self.delay_distance_label = QLabel("Bad drone distance during delay:")
        self.suggestion_label = QLabel("Suggestions:")

        # Layout setup
        result_group = QGroupBox("Results")
        result_layout = QVBoxLayout(result_group)
        result_layout.addWidget(self.result_label)
        result_layout.addWidget(self.drone_speed_label)
        result_layout.addWidget(self.delay_distance_label)
        result_layout.addWidget(self.suggestion_label)
        layout.addWidget(result_group)

    def validate_and_calculate(self):
        """
        Validate the input fields and calculate the intercept distance
        """
        if not self.validate_input(self.drone_speed.value(), min_value=0):
            QMessageBox.warning(
                self, "Invalid Input", "Drone speed must be non-negative."
            )
            return
        if not self.validate_input(self.radar_range.value(), min_value=0):
            QMessageBox.warning(
                self, "Invalid Input", "Radar range must be non-negative."
            )
            return
        if not self.validate_input(self.reaction_time.value(), min_value=0):
            QMessageBox.warning(
                self, "Invalid Input", "Reaction time must be non-negative."
            )
            return
        self.calculate()

    def calculate(self):
        """
        Calculate the intercept distance and update the result labels
        """
        speed_unit = self.speed_unit_combo.currentText()
        distance_unit = self.distance_unit_combo.currentText()

        # Calculate drone speed in miles per hour
        drone_speed_mph = UnitConverter.to_miles_per_hour(
            self.drone_speed.value(), speed_unit
        )

        # Calculate radar range in miles
        radar_range_miles = UnitConverter.to_miles(
            self.radar_range.value(), distance_unit
        )

        # Calculate intercept distance
        mins_drone_speed = drone_speed_mph / 60
        self.drone_speed_label.setText(f"Drone speed (mph): {drone_speed_mph:.4f}")

        miles_delay_distance = mins_drone_speed * self.reaction_time.value()
        delay_distance = UnitConverter.from_miles_to_unit(
            miles_delay_distance, distance_unit
        )
        self.delay_distance_label.setText(
            f"Bad drone distance during delay ({distance_unit}): {delay_distance:.4f}"
        )

        intercept_distance = (radar_range_miles - miles_delay_distance) / 2
        intercept_time = (
            intercept_distance / mins_drone_speed
        ) + self.reaction_time.value()
        intercept_possible = miles_delay_distance < radar_range_miles

        if intercept_possible:
            results = [f"We intercept the drone."]
            results.append(f"Interception distance: {intercept_distance:.2f} miles away")
            results.append(f"Interception time: {intercept_time:.2f} minutes")
            self.result_label.setText("\n".join(results))
            self.suggestion_label.setText("")
        else:
            suggestions = self.generate_suggestions(
                drone_speed_mph, intercept_distance, distance_unit
            )
            self.result_label.setText("We can't intercept the drone")
            self.suggestion_label.setText("\n".join(suggestions))

        self.update_chart(
            mins_drone_speed, intercept_distance, intercept_time, intercept_possible, distance_unit
        )

    def generate_suggestions(self, drone_speed_mph, intercept_distance, distance_unit):
        """
        Generate suggestions for intercepting the drone

        Parameters:
            drone_speed_mph (float): The drone speed in miles per hour.
            intercept_distance (float): The calculated intercept distance in miles.
            distance_unit (str): The unit of distance used for the suggestions (e.g., "miles", "km").

        Returns:
            list: A list of suggestions for intercepting the drone.
        """
        suggestions = ["Suggestions:"]

        # Decrease drone speed
        required_drone_speed = (
            self.radar_range.value() / self.reaction_time.value()
        ) * 60
        suggestions.append(
            f"Decrease drone speed to less than {required_drone_speed:.2f} {self.speed_unit_combo.currentText()}"
        )

        # Decrease reaction time
        required_reaction_time = self.radar_range.value() / (drone_speed_mph / 60)
        suggestions.append(
            f"Decrease reaction time to less than {required_reaction_time:.2f} minutes"
        )

        # Increase radar range
        required_radar_range = UnitConverter.from_miles_to_unit(
            abs(intercept_distance), distance_unit
        )
        suggestions.append(
            f"Increase radar range to more than {required_radar_range:.2f} {distance_unit}"
        )

        return suggestions

    def update_chart(
        self, mins_drone_speed, intercept_distance, intercept_time, intercept_possible, distance_unit
    ):
        """
        Update the chart with the new intercept distance

        Parameters:
            mins_drone_speed (float): The drone speed in miles per minute.
            intercept_distance (float): The calculated intercept distance in miles.
            intercept_possible (bool): True if interception is possible, False otherwise.
            distance_unit (str): The unit of distance used for the chart (e.g., "miles", "km").
        """
        chart = QChart()
        chart.setTitle("Drone Intercept Visualization")
        max_time = max(
            self.reaction_time.value() * 2, self.radar_range.value() * 2 / mins_drone_speed
        )

        # Series for radar range
        radar_series = QLineSeries()
        radar_series.setName("Radar Range")
        radar_series.append(0, self.radar_range.value())
        radar_series.append(max_time, self.radar_range.value())

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
            intercept_series.append(intercept_time, self.radar_range.value())

        # Set colors based on intercept possibility
        radar_color = QColor(Qt.cyan) if intercept_possible else QColor(Qt.magenta)
        radar_pen = QPen(radar_color)
        drone_color = QColor(Qt.blue) if intercept_possible else QColor(Qt.red)
        drone_pen = QPen(drone_color)
        radar_pen.setWidth(3)
        drone_pen.setWidth(3)
        radar_series.setPen(radar_pen)
        drone_series.setPen(drone_pen)
        intercept_series.setColor(QColor(Qt.green))
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
        # Reset input fields
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
        drone_speed_mph = UnitConverter.to_miles_per_hour(
            self.drone_speed.value(), speed_unit
        )
        radar_range_miles = UnitConverter.to_miles(
            self.radar_range.value(), distance_unit
        )

        # Create and show simulation window
        self.sim_window = DroneInterceptSimulation(
            drone_speed_mph, radar_range_miles, self.reaction_time.value()
        )
        self.sim_window.show()
