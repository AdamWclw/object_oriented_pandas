import pandas as pd
import numpy as np
from object_oriented_pandas.error import InputError
from object_oriented_pandas import data_type, Column
from enum import EnumMeta


# ----------------------------------------------------------------------------------------------------------------------
# PREPARE DF
def prepare_df(col_obj_lst: list, idx_obj: Column, df: pd.DataFrame, cl_name: str):

    # do nothing, if col_obj_lst is empty
    if not is_empty(col_obj_lst):

        df_in = df.copy()
        res_df = pd.DataFrame(index=df_in.index)

        try:

            # loop cols
            for col_obj in col_obj_lst:

                col_data = None

                # rename col to model convention
                if (col_obj.get_input_name() in df_in.columns.tolist()) & \
                        (col_obj.get_input_name() != col_obj.get_name()):
                    df_in.rename(columns={col_obj.get_input_name(): col_obj.get_name()}, inplace=True)

                # create col with default value, if col is not in df and is not required and is not temporary
                if col_obj.get_name() not in df_in.columns.tolist():
                    col_data = \
                        prepare_col(
                            col_obj=col_obj,
                            col_data=col_obj.get_default_value(),
                            df_index=df_in.index,
                            col_name=col_obj.get_name(),
                            cl_name=cl_name)

                # update type of col, if col is in df
                if col_obj.get_name() in df_in.columns.tolist():
                    col_data = \
                        prepare_col(
                            col_obj=col_obj,
                            col_data=df_in[col_obj.get_name()],
                            df_index=df_in.index,
                            col_name=col_obj.get_name(),
                            cl_name=cl_name)

                # update df
                res_df[col_obj.get_name()] = col_data

            # check if idx is unique
            if idx_obj is not None:
                if res_df[idx_obj.get_name()].duplicated().any():
                    idx_col = res_df[idx_obj.get_name()]

                    msg = 'Duplicated index values: ' + \
                          str(idx_col[idx_col.duplicated()].tolist())
                    raise InputError(msg)
                else:
                    return res_df

            else:
                return res_df

        except InputError:
            raise


def is_idx_unique(idx_series):
    return not idx_series.duplicated().any()


def is_empty(data):
    if data is None:
        return True
    else:
        if len(data) == 0:
            return True
        else:
            return False


# ----------------------------------------------------------------------------------------------------------------------
# PREPARE COL
def prepare_col(col_obj, col_data, df_index, col_name, cl_name):

    try:

        # if input is a pandas series
        if isinstance(col_data, pd.Series):

            # fill None/nan values
            is_nan = False
            if any(col_data.isnull()):
                is_nan = True
                col_data = fill_nan_series(col_obj=col_obj, col_data=col_data, col_name=col_name, cl_name=cl_name)

            # if col_obj is of type ENUM
            if isinstance(col_obj.get_data_type(), EnumMeta):

                # validate data type
                if (col_data.dtype not in (data_type.get_permitted_enum())) & \
                            (not (is_nan & (col_data.dtype == object))):

                    msg = 'Prohibited input data type=' + str(col_data.dtype) + ' for column of type ENUM'
                    raise InputError(msg)

                # create pandas categorical type
                cat_type = pd.api.types.CategoricalDtype(categories=[e.value for e in col_obj.get_data_type()],
                                                         ordered=True)
                # convert to data type
                col_data = col_data.astype(cat_type)

                return col_data

            # if col_obj is of type TIMESTAMP
            elif col_obj.get_data_type() == data_type.TIMESTAMP:

                # validate data type
                if (col_data.dtype not in (data_type.get_permitted_timestamp())) & \
                        (not (is_nan & (col_data.dtype == object))):

                    msg = 'Prohibited input data type=' + str(col_data.dtype) + ' for column of type TIMESTAMP'
                    raise InputError(msg)

                # convert to data type
                col_data = pd.to_datetime(col_data)

            # if col_obj is of type TIMEDELTA
            elif col_obj.get_data_type() == data_type.TIMEDELTA:

                # validate data type
                if (col_data.dtype not in (data_type.get_permitted_timedelta())) & \
                            (not (is_nan & (col_data.dtype == object))):

                    msg = 'Prohibited input data type=' + type(col_data).__name__ + ' for column of type TIMEDELTA'
                    raise InputError(msg)

                # convert to data type
                col_data = pd.to_timedelta(col_data, unit='s')

            # if col_obj is of type PRIMITIVE
            else:

                # validate data type
                if col_obj.get_data_type() == data_type.INT:
                    if (col_data.dtype not in (data_type.get_permitted_int())) & \
                            (not (is_nan & (col_data.dtype == object))):

                        msg = 'Prohibited input data type=' + str(col_data.dtype) + ' for column of type INT'
                        raise InputError(msg)

                elif col_obj.get_data_type() == data_type.FLOAT:
                    if (col_data.dtype not in (data_type.get_permitted_float())) & \
                            (not (is_nan & (col_data.dtype == object))):

                        msg = 'Prohibited input data type=' + str(col_data.dtype) + ' for column of type FLOAT'
                        raise InputError(msg)

                else:

                    msg = 'Prohibited input data type=' + str(col_data.dtype) + ' for column'
                    raise InputError(msg)

                # convert to data type
                col_data = col_data.astype(col_obj.get_data_type())

                return col_data

        # if input is a single value
        elif isinstance(col_data, tuple(data_type.get_permitted())):

            # fill None/nan values
            col_data = fill_nan_value(col_obj=col_obj, value=col_data, col_name=col_name, cl_name=cl_name)

            # if col_obj is of type ENUM
            if isinstance(col_obj.get_data_type(), EnumMeta):

                # validate data type
                if not isinstance(col_data, tuple(data_type.get_permitted_enum())):

                    msg = 'Prohibited input data type=' + type(col_data).__name__ + ' for column of type ENUM'
                    raise InputError(msg)

                # convert to series
                col_data = pd.Series(index=df_index, data=col_data)

                # create pandas categorical type
                cat_type = \
                    pd.api.types.CategoricalDtype(categories=[e.value for e in col_obj.get_data_type()], ordered=True)

                # convert to data type
                col_data = col_data.astype(dtype=cat_type)

                # fill None/nan values, if input does not match categorical type
                col_data = fill_nan_series(col_obj=col_obj, col_data=col_data, col_name=col_name, cl_name=cl_name)

                return col_data

            # if col_obj is of type TIMESTAMP
            elif col_obj.get_data_type() == data_type.TIMESTAMP:

                # validate data type
                if not isinstance(col_data, tuple(data_type.get_permitted_timestamp())):

                    msg = 'Prohibited input data type=' + type(col_data).__name__ + ' for column of type TIMESTAMP'
                    raise InputError(msg)

                # convert to series
                col_data = pd.Series(index=df_index, data=col_data)

                # convert to data type
                col_data = pd.to_datetime(col_data)

            # if col_obj is of type TIMEDELTA
            elif col_obj.get_data_type() == data_type.TIMEDELTA:

                # validate data type
                if not isinstance(col_data, tuple(data_type.get_permitted_timedelta())):

                    msg = 'Prohibited input data type=' + type(col_data).__name__ + ' for column of type TIMEDELTA'
                    raise InputError(msg)

                # convert to series
                col_data = pd.Series(index=df_index, data=col_data)

                # convert to data type
                col_data = pd.to_timedelta(col_data, unit='s')

            # if col_obj is of type PRIMITIVE
            else:

                # validate data type
                if col_obj.get_data_type() == data_type.INT:
                    if not isinstance(col_data, tuple(data_type.get_permitted_int())):

                        msg = 'Prohibited input data type=' + type(col_data).__name__ + ' for column of type INT'
                        raise InputError(msg)

                elif col_obj.get_data_type() == data_type.FLOAT:
                    if not isinstance(col_data, tuple(data_type.get_permitted_float())):

                        msg = 'Prohibited input data type=' + type(col_data).__name__ + ' for column of type FLOAT'
                        raise InputError(msg)

                else:

                    msg = 'Prohibited input data type=' + type(col_data).__name__ + ' for column'
                    raise InputError(msg)

                # convert to series
                col_data = pd.Series(index=df_index, data=col_data)

                # convert to data type
                col_data = col_data.astype(dtype=col_obj.get_data_type())

                return col_data

        # else it is a prohibited data type
        else:

            msg = 'Prohibited input data type=' + type(col_data).__name__ + ' for a column'
            raise InputError(msg)

        return col_data

    except InputError:
        raise


def fill_nan_value(col_obj, value, col_name, cl_name):

    if is_value_nan(value=value):
        if col_obj.get_default_value() is not None:
            return col_obj.get_default_value()
        else:

            msg = 'Column contain None/nan row values and default value is undefined'
            raise InputError(msg)
    else:
        return value


def fill_nan_series(col_obj, col_data, col_name, cl_name):

    col_data = col_data.copy()

    if col_obj.get_default_value() is not None:
        for idx in col_data.index:

            # fill_nan_value
            col_data[idx] = fill_nan_value(col_obj=col_obj, value=col_data[idx], col_name=col_name, cl_name=cl_name)

        return col_data
    else:
        msg = 'Column contain None/nan row values and default value is undefined'
        raise InputError(msg)


def is_value_nan(value):
    if value is None:
        return True
    else:
        return False


def remove_nan_from_list(lst):
    res_lst = []
    for item in lst:
        if not is_value_nan(value=item):
            res_lst.append(item)
    return res_lst


def remove_list_nesting(lst):
    res_lst = []

    def r(l):
        for i in l:
            if type(i) == list:
                r(i)
            else:
                res_lst.append(i)
    r(lst)
    return res_lst


# ----------------------------------------------------------------------------------------------------------------------
# VALIDATE COL DATA TYPE
def validate_col_data_type(col_data, col_name, cl_name):

    try:
        # if input is a single column entry
        if isinstance(col_data, tuple(data_type.get_permitted())):
            return validate_data_type(data=col_data, col_name=col_name, cl_name=cl_name)
        elif isinstance(col_data, pd.Series):
            for idx in col_data.index:
                col_data[idx] = validate_data_type(data=col_data[idx], col_name=col_name, cl_name=cl_name)
            return col_data
        elif isinstance(col_data, np.ndarray):
            if col_data.ndim == 1:
                for idx in range(len(col_data)):
                    col_data[idx] = validate_data_type(data=col_data[idx], col_name=col_name, cl_name=cl_name)
                return col_data
            else:

                msg = 'Unknown data type=' + type(col_data).__name__
                raise InputError(msg)
        else:

            msg = 'Unknown data type=' + type(col_data).__name__
            raise InputError(msg)

    except InputError as e:
        raise


def validate_data_type(data, col_name, cl_name):
    if not isinstance(data, tuple(data_type.get_permitted())):
        msg = 'Unknown data type=' + type(data).__name__
        raise InputError(msg)
    return data


# ----------------------------------------------------------------------------------------------------------------------
# CONVERT TO DATA TYPE
def convert_col_to_data_type(col_obj, col_data, cl_name):
    if isinstance(col_obj.get_data_type(), EnumMeta):
        col_data.fillna(value=col_obj.get_default_value(), inplace=True)
        cat_type = pd.api.types.CategoricalDtype(categories=[e.value for e in col_obj.get_data_type()], ordered=True)
        return col_data.astype(cat_type).copy()
    else:
        return col_data.astype(col_obj.get_data_type())


def is_col_list(sr):
    return sr.apply(lambda x: isinstance(x, list)).all()


def get_default_col_data(col_obj, cl_name):
    return validate_col_data_type(col_data=col_obj.get_default_value(), col_name=col_obj.get_name(), cl_name=cl_name)


def get_col_names(cols):
    return [col.get_name() for col in cols]


def get_enum_values(en):
    return [e.value for e in en]


def convert_value_to_current_unit(val, col):
    if not col.is_data_unit_si:
        return val / col.get_data_unit.con_2_si
    else:
        return val









