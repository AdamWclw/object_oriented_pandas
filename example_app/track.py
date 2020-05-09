from object_oriented_pandas import Column, DataFrame, data_unit, data_type
import pandas as pd


class Track(DataFrame):

    # columns of track DataFrame
    ID = \
        Column(
            name='id',
            input_name='track_id',
            data_type=data_type.INT,
            data_unit=None,
            is_data_unit_si=None,
            default_value=0
        )

    PURPOSE = \
        Column(
            name='purpose',
            input_name='track_purpose',
            data_type=data_type.TrackPurpose,
            data_unit=None,
            is_data_unit_si=None,
            default_value=data_type.TrackPurpose.UNDEFINED.value
        )

    START_TIME = \
        Column(
            name='start_time',
            input_name='track_start_time',
            data_type=data_type.TIMESTAMP,
            data_unit=None,
            is_data_unit_si=None,
            default_value=pd.to_datetime(0)
        )

    STOP_TIME = \
        Column(
            name='stop_time',
            input_name='track_stop_time',
            data_type=data_type.TIMESTAMP,
            data_unit=None,
            is_data_unit_si=None,
            default_value=pd.to_datetime(0)
        )

    DISTANCE = \
        Column(
            name='distance',
            input_name='track_distance',
            data_type=data_type.FLOAT,
            data_unit=data_unit.DISTANCE,
            is_data_unit_si=False,
            default_value=0
        )

    ENERGY = \
        Column(
            name='energy',
            input_name='track_energy',
            data_type=data_type.FLOAT,
            data_unit=data_unit.ENERGY,
            is_data_unit_si=False,
            default_value=0
        )

    CONSUMPTION = \
        Column(
            name='consumption',
            input_name='',
            data_type=data_type.FLOAT,
            data_unit=None,
            is_data_unit_si=None,
            default_value=0
        )

    # sort order
    _sort = [PURPOSE, START_TIME]

    # index of df
    _idx = ID

    def __init__(self, df: pd.DataFrame):
        super().__init__(df=df)

    # function to calculate consumption per track
    def calculate_consumption(self) -> None:

        # select energy column
        energy = self.df[self.ENERGY.get_name()].copy()
        if not self.ENERGY.is_data_unit_si():  # convert energy column to SI unit, if it is not already
            energy *= data_unit.ENERGY.get_con_2_si()

        # select distance column
        distance = self.df[self.DISTANCE.get_name()].copy()
        if not self.DISTANCE.is_data_unit_si():  # convert distance column to SI unit, if it is not already
            distance *= data_unit.DISTANCE.get_con_2_si()

        # calculate consumption in kWh/100km
        self.df[self.CONSUMPTION.get_name()] = (energy / 1000 / 3600) / distance * 100 * 1000
