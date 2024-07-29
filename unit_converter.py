class UnitConverter:
    """
    Utility class for unit conversion
    """

    @staticmethod
    def mph_to_mpm(mph):
        """
        Converts miles per hour (mph) to miles per minute (mpm).

        Parameters:
            mph (float): Speed in miles per hour.

        Returns:
            float: Speed in miles per minute.
        """
        return mph / 60

    @staticmethod
    def to_miles_per_hour(value, unit):
        """
        Converts a speed value from various units to miles per hour (mph).

        Parameters:
            value (float): The speed value to convert.
            unit (str): The unit of the speed value (e.g., "km/h", "m/s").

        Returns:
            float: The speed value in miles per hour.
        """
        if unit == "mph":
            return value
        elif unit == "km/h":
            return value / 1.60934
        elif unit == "ft/h":
            return value / 5280
        elif unit == "m/min":
            return value * 60
        elif unit == "km/min":
            return value * 60 / 1.60934
        elif unit == "ft/min":
            return value * 60 / 5280
        elif unit == "m/s":
            return value * 3600
        elif unit == "km/s":
            return value * 3600 / 1.60934
        elif unit == "ft/s":
            return value * 3600 / 5280

    @staticmethod
    def to_miles(value, unit):
        """
        Converts a distance value from various units to miles.

        Parameters:
            value (float): The distance value to convert.
            unit (str): The unit of the distance value (e.g., "km", "feet").

        Returns:
            float: The distance value in miles.
        """
        if unit == "miles":
            return value
        elif unit == "km":
            return value / 1.60934
        elif unit == "feet":
            return value / 5280

    @staticmethod
    def from_miles_to_unit(value, unit):
        """
        Converts a distance value from miles to various units.

        Parameters:
            value (float): The distance value in miles.
            unit (str): The target unit for conversion (e.g., "km", "feet").

        Returns:
            float: The distance value in the specified unit.
        """
        if unit == "miles":
            return value
        elif unit == "km":
            return value * 1.60934
        elif unit == "feet":
            return value * 5280
