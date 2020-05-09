import pandas as pd
import numpy as np
from enum import Enum, EnumMeta

# DATA TYPES
INT = np.int64
FLOAT = np.double
TIMESTAMP = np.datetime64
TIMEDELTA = np.timedelta64


class TrackPurpose(Enum):
    FREIGHT_TRANSPORT = 'freight_transport'
    PASSENGER_TRANSPORT = 'passenger_transport'
    TECHNICAL_SERVICE = 'technical_service'
    OTHER_SERVICE = 'other_service'
    UNDEFINED = ''


# ----------------------------------------------------------------------------------------------------------------------
# private variables
_local_vars = locals()
_all = None
_primitive = None
_enum = None

_permitted_int = [INT, int]
_permitted_float = [FLOAT, float]
_permitted_timestamp = [TIMESTAMP, str, pd.Timestamp, 'datetime64[ns]']
_permitted_timedelta = [TIMEDELTA, str, pd.Timedelta, 'timedelta64[ns]'] + _permitted_int + _permitted_float
_permitted_numerical_data_types = _permitted_int + _permitted_float
_permitted_enum = [str]


def get_permitted():
    return _permitted_int + _permitted_float + _permitted_enum + \
        _permitted_timedelta + _permitted_timestamp


def get_enums():
    global _enum
    if _enum is None:
        _enum = []
        local_vars = list(_local_vars.values())
        for local_var in local_vars:
            if isinstance(local_var, EnumMeta):
                if (local_var != Enum) & (local_var != EnumMeta):
                    _enum.append(local_var)
        return _enum
    else:
        return _enum


def get_permitted_int():
    return _permitted_int + _permitted_float


def get_permitted_float():
    return _permitted_int + _permitted_float


def get_permitted_timestamp():
    return _permitted_timestamp


def get_permitted_timedelta():
    return _permitted_timedelta


def get_permitted_enum():
    permitted_enums = get_enums()
    return permitted_enums + _permitted_enum
