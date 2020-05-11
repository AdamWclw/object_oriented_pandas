from object_oriented_pandas import functions, Column
import pandas as pd


class DataFrame:

    # sort order
    _sort = []         # can be overwritten in child class

    # index
    _idx = None        # can be overwritten in child class

    # constructor
    def __init__(self, df: pd.DataFrame):

        # retrieve Column objects and safe to list
        self._cols = []
        for col in dir(self):
            if isinstance(getattr(self, col), Column):
                self._cols.append(getattr(self, col))

        # prepare DataFrame
        self.df = \
            functions.prepare_df(
                col_obj_lst=self._cols,
                idx_obj=self._idx,
                df=df,
                cl_name=self.__class__.__name__)

        # set index of DataFrame
        self.set_idx()

        # convert all columns with data units to SI units
        self.convert_to_si()

        # sort DataFrame
        self.sort()

    # sort DataFrame according to the order given by self._sort
    def sort(self) -> None:
        if len(self._sort) > 0:
            sort_lst = []
            for col in self._sort:
                sort_lst.append(col.get_name())
            self.df.sort_values(sort_lst, inplace=True)

    # get index of DataFrame
    def get_idx(self) -> Column:
        return self._idx

    # set index of DataFrame
    def set_idx(self) -> None:
        if self._idx is not None:
            if not self.is_idx_set():
                self.df.set_index(self._idx.get_name(), inplace=True)

    # reset index of DataFrame
    def reset_idx(self) -> None:
        if self._idx is not None:
            if self.is_idx_set():
                self.df.reset_index(inplace=True)

    # determine whether index of DataFrame is currently set
    def is_idx_set(self) -> bool:
        if self.get_idx() is not None:
            return self.get_idx().get_name() not in self.df.columns.tolist()
        else:
            return False

    # convert columns to SI unit
    def convert_to_si(self, col_obj: Column = None) -> None:
        if col_obj is None:
            for col_obj in self._cols:
                if col_obj.get_data_unit() is not None:
                    if not col_obj.is_data_unit_si():
                        col_obj._is_data_unit_si = True
                        self.df[col_obj.get_name()] *= col_obj.get_data_unit().get_con_2_si()
                        col_obj._default_value *= col_obj.get_data_unit().get_con_2_si()
        else:
            if col_obj.get_data_unit() is not None:
                if not col_obj.is_data_unit_si():
                    col_obj._is_data_unit_si = True
                    self.df[col_obj.get_name()] *= col_obj.get_data_unit().get_con_2_si()
                    col_obj._default_value *= col_obj.get_data_unit().get_con_2_si()

    # convert columns to conventional unit
    def convert_to_con(self, col_obj: Column = None) -> None:
        if col_obj is None:
            for col_obj in self._cols:
                if col_obj.get_data_unit() is not None:
                    t = col_obj.is_data_unit_si()
                    if col_obj.is_data_unit_si():
                        col_obj._is_data_unit_si = False
                        self.df[col_obj.get_name()] /= col_obj.get_data_unit().get_con_2_si()
                        col_obj._default_value /= col_obj.get_data_unit().get_con_2_si()
        else:
            if col_obj.get_data_unit() is not None:
                if col_obj.is_data_unit_si():
                    col_obj._is_data_unit_si = False
                    self.df[col_obj.get_name()] /= col_obj.get_data_unit().get_con_2_si()
                    col_obj._default_value /= col_obj.get_data_unit().get_con_2_si()

    # determine whether columns are currently in SI unit
    def is_data_unit_si(self, col_obj: Column = None) -> bool:
        if col_obj is None:
            is_si_lst = []
            for col_obj in self._cols:
                si = col_obj.is_data_unit_si()
                if si is not None:
                    is_si_lst.append(si)

            if len(is_si_lst) == 0:
                return False
            else:
                return all(is_si_lst)
        else:
            return col_obj.is_data_unit_si()




