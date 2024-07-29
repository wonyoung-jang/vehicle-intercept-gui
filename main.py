import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget
from car_collision import CarCollisionWindow
from drone_intercept import DroneInterceptWindow


class MainWindow(QMainWindow):
    def __init__(self):
        """
        Main window with two tabs for the two problems
        """
        super().__init__()
        self.setWindowTitle("Two problems")

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

# TODO implement: a more detailed results section
# TODO add: unit tests
