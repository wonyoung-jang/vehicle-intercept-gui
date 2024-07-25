class UnitConverter:
    """
    Utility class for unit conversion
    """
    
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
    
    @staticmethod
    def to_miles_per_hour(value, unit):
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
        if unit == "miles":
            return value
        elif unit == "km":
            return value / 1.60934
        elif unit == "feet":
            return value / 5280

    @staticmethod
    def from_miles_to_unit(value, unit):
        if unit == "miles":
            return value
        elif unit == "km":
            return value * 1.60934
        elif unit == "feet":
            return value * 5280
