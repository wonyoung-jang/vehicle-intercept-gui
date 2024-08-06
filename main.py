from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget
from car_collision import CarCollisionWindow
from drone_intercept import DroneInterceptWindow
import configparser
import logging
import sys
import test
import unittest

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
)

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
    # Log initialization
    logging.info("MainWindow initialized")

    def __init__(self) -> None:
        """
        Main window with two tabs for the two problems
        """
        super().__init__()
        self.setWindowTitle("Vehicle intercept simulator")

        # Load configuration from file
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

        # Create tab widget
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Create and add 'Drone intercept' tab
        drone_tab = DroneInterceptWindow(self.config)
        self.tab_widget.addTab(drone_tab, "Drone intercept")

        # Create and add 'Car collision' tab
        car_tab = CarCollisionWindow(self.config)
        self.tab_widget.addTab(car_tab, "Car collision")


def run_tests() -> bool:
    # Create a test suite
    test_suite = unittest.TestLoader().loadTestsFromModule(test)

    # Run the tests
    test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)

    # Return True if all tests passed, False otherwise
    return test_result.wasSuccessful()


if __name__ == "__main__":
    if run_tests():
        logging.info("All tests passed.")
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    else:
        # logging.debug("Some tests failed.")
        sys.exit(1)
