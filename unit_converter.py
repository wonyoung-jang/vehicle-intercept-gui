import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
)


class UnitConverter:
    """
    Utility class for unit conversion
    """

    # Log initialization
    logging.info("UnitConverter initialized")

    @staticmethod
    def to_miles_per_hour(value, unit) -> float:
        """
        Converts a speed value from various units to miles per hour (mph).

        Parameters:
            value (float): The speed value to convert.
            unit (str): The unit of the speed value (e.g., "km/h", "m/s").

        Returns:
            float: The speed value in miles per hour.
        """
        logging.debug(f"to_miles_per_hour called with value={value}, unit={unit}")

        if unit == "mph":
            return value
        elif unit == "km/h":
            return value / 1.60934
        elif unit == "m/h":
            return value / 1609.34
        elif unit == "yd/h":
            return value / 1760
        elif unit == "ft/h":
            return value / 5280
        elif unit == "mpm":
            return value * 60
        elif unit == "km/min":
            return value * 60 / 1.60934
        elif unit == "m/min":
            return value * 60 / 1609.34
        elif unit == "yd/min":
            return value * 60 / 1760
        elif unit == "ft/min":
            return value * 60 / 5280
        elif unit == "mps":
            return value * 3600
        elif unit == "km/s":
            return value * 3600 / 1.60934
        elif unit == "m/s":
            return value * 3600 / 1609.34
        elif unit == "yd/s":
            return value * 3600 / 1760
        elif unit == "ft/s":
            return value * 3600 / 5280
        else:
            raise ValueError(f"Invalid unit: {unit}")

    @staticmethod
    def from_miles_per_hour(value, unit) -> float:
        """
        Converts a speed value from miles per hour (mph) to various units.

        Parameters:
            value (float): The speed value to convert.
            unit (str): The unit of the speed value (e.g., "km/h", "m/s").

        Returns:
            float: The speed value in given unit.
        """
        logging.debug(f"from_miles_per_hour called with value={value}, unit={unit}")

        if unit == "mph":
            return value
        elif unit == "km/h":
            return value * 1.60934
        elif unit == "m/h":
            return value * 1609.34
        elif unit == "yd/h":
            return value * 1760
        elif unit == "ft/h":
            return value * 5280
        elif unit == "mpm":
            return value / 60
        elif unit == "km/min":
            return value / 60 * 1.60934
        elif unit == "m/min":
            return value / 60 * 1609.34
        elif unit == "yd/min":
            return value / 60 * 1760
        elif unit == "ft/min":
            return value / 60 * 5280
        elif unit == "mps":
            return value / 3600
        elif unit == "km/s":
            return value / 3600 * 1.60934
        elif unit == "m/s":
            return value / 3600 * 1609.34
        elif unit == "yd/s":
            return value / 3600 * 1760
        elif unit == "ft/s":
            return value / 3600 * 5280
        else:
            raise ValueError(f"Invalid unit: {unit}")
    
    @staticmethod
    def to_miles(value, unit) -> float:
        """
        Converts a distance value from various units to miles.

        Parameters:
            value (float): The distance value to convert.
            unit (str): The unit of the distance value (e.g., "km", "feet").

        Returns:
            float: The distance value in miles.
        """
        logging.debug(f"to_miles called with value={value}, unit={unit}")

        if unit == "miles":
            return value
        elif unit == "kilometers":
            return value / 1.60934
        elif unit == "meters":
            return value / 1609.34
        elif unit == "yards":
            return value / 1760
        elif unit == "feet":
            return value / 5280
        else:
            raise ValueError(f"Invalid unit: {unit}")

    @staticmethod
    def from_miles(value, unit) -> float:
        """
        Converts a distance value from miles to various units.

        Parameters:
            value (float): The distance value in miles.
            unit (str): The target unit for conversion (e.g., "km", "feet").

        Returns:
            float: The distance value in the specified unit.
        """
        logging.debug(f"from_miles called with value={value}, unit={unit}")

        if unit == "miles":
            return value
        elif unit == "kilometers":
            return value * 1.60934
        elif unit == "meters":
            return value * 1609.34
        elif unit == "yards":
            return value * 1760
        elif unit == "feet":
            return value * 5280
        else:
            raise ValueError(f"Invalid unit: {unit}")
