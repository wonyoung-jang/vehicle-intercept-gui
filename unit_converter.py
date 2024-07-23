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
