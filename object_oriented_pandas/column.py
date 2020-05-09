from object_oriented_pandas.data_unit import _Unit


class Column:

    def __init__(self,
                 name: str,
                 data_type,
                 default_value,
                 data_unit: _Unit = None,
                 is_data_unit_si: bool = None,
                 input_name: str = None):

        self._name = name
        self._input_name = input_name
        self._data_type = data_type
        self._data_unit = data_unit
        self._is_data_unit_si = is_data_unit_si
        self._default_value = default_value

    def get_name(self) -> str:
        return self._name

    def get_input_name(self) -> str:
        return self._input_name

    def get_data_type(self):
        return self._data_type

    def get_data_unit(self) -> _Unit:
        return self._data_unit

    def is_data_unit_si(self) -> bool:
        return self._is_data_unit_si

    def get_default_value(self):
        return self._default_value





