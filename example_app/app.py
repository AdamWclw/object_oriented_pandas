import pandas as pd
from example_app.track import Track
from object_oriented_pandas import data_type


# read example track data
track_df = pd.read_pickle('track_df.pkl')

# get data types
track_raw_dt = track_df.dtypes

# create track object
track_obj = Track(df=track_df)

# get data types
track_processed_dt = track_obj.df.dtypes

# calculate consumption
track_obj.calculate_consumption()

# sort
track_obj.sort()

# reset index
track_obj.reset_idx()

# set index
track_obj.set_idx()

# set index (without effect, since index is already set)
track_obj.set_idx()

# set index (without effect, since index is already set)
track_obj.set_idx()

# convert to conventional unit
track_obj.convert_to_con()

# convert to SI unit
track_obj.convert_to_si()

# convert distance column to SI unit
track_obj.convert_to_con(col_obj=track_obj.DISTANCE)

# convert all column to SI unit
track_obj.convert_to_si()

# determine whether columns are currently in SI unit
if track_obj.is_data_unit_si():
    print('columns are currently in SI unit')
else:
    print('columns are currently in conventional unit')

# select consumption of freight transport tracks
consumption_of_freight_transport_tracks = \
    track_obj.df.loc[
        track_obj.df[track_obj.PURPOSE.get_name()] == data_type.TrackPurpose.FREIGHT_TRANSPORT.value,
        track_obj.CONSUMPTION.get_name()]

print('sdf')

