# DATA UNIT CLASS
class _Unit:
    def __init__(self, name, con_2_si, con_unit, si_unit):
        self._name = name
        self._con_2_si = con_2_si
        self._con_unit = con_unit
        self._si_unit = si_unit

    def get_name(self):
        return self._name

    def get_con_2_si(self):
        return self._con_2_si

    def get_con_unit(self):
        return self._con_unit

    def get_si_unit(self):
        return self._si_unit


# DATA UNITS
ENERGY = _Unit(name='Energy', con_2_si=1000 * 3600, con_unit='kWh', si_unit='Ws')
DISTANCE = _Unit(name='Distance', con_2_si=1000, con_unit='km', si_unit='m')


