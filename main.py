import sys
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox, QPushButton, QTabWidget

class DroneInterceptWindow(QMainWindow):
    """
    1) Drone intercept problem
    - Radar intercept capability is 2 miles
    - Drones (bad guys = them, good guys = us) both travel at 30 mph
    - It takes us 5 minutes to react and get our drone up in the air
    - How far away do we intercept the drone?
    - What can we do to intercept the drone?
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Drone intercept problem')

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Input fields
        input_layout = QHBoxLayout()
        layout.addLayout(input_layout)
        
        self.drone_speed = QDoubleSpinBox()
        self.drone_speed.setValue(30)
        
        self.radar_range = QDoubleSpinBox()
        self.radar_range.setValue(2)
        
        self.reaction_time = QDoubleSpinBox()
        self.reaction_time.setValue(5)

        # Set ranges for input fields
        self.drone_speed.setRange(1, 1000)
        self.reaction_time.setRange(0, 60)
        self.radar_range.setRange(1, 100)
        
        # Drone
        input_layout.addWidget(QLabel('Drone speed (mph):'))
        input_layout.addWidget(self.drone_speed)

        # Radar range
        input_layout.addWidget(QLabel('Radar range (miles):'))
        input_layout.addWidget(self.radar_range)
        
        # Reaction time
        input_layout.addWidget(QLabel('Reaction time (min):'))
        input_layout.addWidget(self.reaction_time)

        # Result label
        self.result_label = QLabel('Result will be shown here')
        layout.addWidget(self.result_label)

        self.drone_speed_label = QLabel('Drone speed (mile per minute):')
        layout.addWidget(self.drone_speed_label)
        
        self.delay_distance_label = QLabel('Delay distance (miles):')
        layout.addWidget(self.delay_distance_label)
        
        # Signals and slots
        self.drone_speed.valueChanged.connect(self.calculate)
        self.radar_range.valueChanged.connect(self.calculate)
        self.reaction_time.valueChanged.connect(self.calculate)

    def calculate(self):
        """        
        Calculate the intercept point based on input parameters.
        Updates the UI with the result.
        """        
        mins_drone_speed = self.drone_speed.value() / 60
        
        self.drone_speed_label.setText(f'Drone speed (mile per minute): {mins_drone_speed}')
        
        miles_delay_distance = mins_drone_speed * self.reaction_time.value()
        self.delay_distance_label.setText(f'Bad drone distance during delay (miles): {miles_delay_distance}')
        intercept_distance = self.radar_range.value() - miles_delay_distance
        
        # If delay distance < radar range  → intercept
        if miles_delay_distance < self.radar_range.value():
            self.result_label.setText(f'Delay: We intercept the drone {intercept_distance} miles away')
        else:
            self.result_label.setText(f'We can\'t intercept the drone')
            
            # Suggestions
            suggestions = ['Suggestions']
            
            # Decrease drone speed
            required_drone_speed = self.radar_range.value() / self.reaction_time.value()
            required_drone_speed *= 60
            suggestions.append(f'Decrease drone speed to less than {required_drone_speed} mph')
            
            # Decrease reaction time
            required_reaction_time = self.radar_range.value() / mins_drone_speed
            suggestions.append(f'Decrease reaction time to less than {required_reaction_time} minutes')
            
            # Increase radar range
            required_radar_range = miles_delay_distance
            suggestions.append(f'Increase radar range to more than {required_radar_range} miles')
            
            self.result_label.setText(self.result_label.text() + '\n' + '\n'.join(suggestions))        
        
class CarCollisionWindow(QWidget):
    """
    2) Car collision problem
    - Car A is traveling 45 mph
    - Car B is traveling 27 mph
    - Car B is traveling in the same lane 200 feet in front of Car A
    - How long until the cars collide?    
    """
    
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Input fields
        input_layout = QHBoxLayout()
        layout.addLayout(input_layout)
        
        self.speed_car_a = QDoubleSpinBox()
        self.speed_car_a.setValue(45)
        self.speed_car_a.setRange(0, 200)
        
        self.speed_car_b = QDoubleSpinBox()
        self.speed_car_b.setValue(27)
        self.speed_car_b.setRange(0, 200)
        
        self.initial_distance = QDoubleSpinBox()
        self.initial_distance.setValue(200)
        self.initial_distance.setRange(0, 1000)

        # Car A speed
        input_layout.addWidget(QLabel('Car A speed (mph):'))
        input_layout.addWidget(self.speed_car_a)

        # Car B speed
        input_layout.addWidget(QLabel('Car B speed (mph):'))
        input_layout.addWidget(self.speed_car_b)
        
        # Initial distance
        input_layout.addWidget(QLabel('Initial distance (feet):'))
        input_layout.addWidget(self.initial_distance)

        # Result label
        self.result_label = QLabel('Result will be shown here')
        layout.addWidget(self.result_label)
        
        # Signals and slots
        self.speed_car_a.valueChanged.connect(self.calculate)
        self.speed_car_b.valueChanged.connect(self.calculate)
        self.initial_distance.valueChanged.connect(self.calculate)

    def calculate(self):
        speed_difference = self.speed_car_a.value() - self.speed_car_b.value()
        
        if speed_difference <= 0:
            self.result_label.setText("The cars will never collide.")
            return
        
        # Convert speeds to feet per hour
        speed_difference_ft_per_hour = speed_difference * 5280
        
        # Calculate time to collision in hours
        time_to_collision_hours = self.initial_distance.value() / speed_difference_ft_per_hour
        
        # Convert time to minutes and seconds
        total_seconds = time_to_collision_hours * 3600
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        
        self.result_label.setText(f"The cars will collide in {minutes} minutes and {seconds} seconds.")

class MainWindow(QMainWindow):
    def __init__(self):
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