import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget
from car_collision import CarCollisionWindow
from drone_intercept import DroneInterceptWindow


"""
Design Patterns:
    Composite: The MainWindow class acts as a composite, containing and
    managing multiple component windows (CarCollisionWindow and
    DroneInterceptWindow) through a QTabWidget. This allows treating
    individual windows and compositions of windows uniformly.
    
    Factory Method: The creation of specific window objects
    (CarCollisionWindow and DroneInterceptWindow) is delegated to
    their respective classes, adhering to the Factory Method pattern.
    This allows for easy extension if more simulation types are added
    in the future.
"""


class MainWindow(QMainWindow):
    def __init__(self):
        """
        Main window with two tabs for the two problems
        """
        super().__init__()
        self.setWindowTitle("Vehicle intercept simulator")

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
