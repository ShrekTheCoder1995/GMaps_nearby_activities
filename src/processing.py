import googlemaps
import pandas as pd
from settings import settings, logger

def add_found_activities_to_dataframe(nearby_search_results_list: list, house_location_dict: dict, df: pd.DataFrame, type_activity: str,) -> pd.DataFrame:

    for nearby_search_result_dict in nearby_search_results_list:
        house_location_dict["Activity_company"] = [nearby_search_result_dict["name"]]
        house_location_dict["Activity_address"] = [nearby_search_result_dict["vicinity"]]
        house_location_dict["Activity_lat"] = [nearby_search_result_dict["geometry"]["location"]["lat"]]
        house_location_dict["Activity_lng"] = [nearby_search_result_dict["geometry"]["location"]["lng"]]
        house_location_dict["Activity_type"] = [type_activity]
        df = pd.concat([df, pd.DataFrame(house_location_dict)], ignore_index = True)

    return df

def find_activities_within_radius(house_location_dict: dict, type_activity: str, gmaps: googlemaps.client.Client) -> tuple:
    nearby_search_results_list: list = []
    activity_radius: int = 5000 #5 km

    while(len(nearby_search_results_list) <= 3):
        nearby_search_results_list: list = gmaps.places_nearby(location=(house_location_dict["House_lat"], house_location_dict["House_lng"]),radius = activity_radius, keyword = type_activity)["results"]
        activity_radius += 5000  # When there are less than 3 activities found within the radius, add 5 km to the radius.

    return nearby_search_results_list, activity_radius

def find_activities(type_activities: list, house_location_dict: dict, df: pd.DataFrame, gmaps: googlemaps.client.Client) -> pd.DataFrame:

    for type_activity in type_activities:

        activities_within_radius: tuple = find_activities_within_radius(house_location_dict, type_activity, gmaps)
        nearby_search_results_list: list = activities_within_radius[0]
        activity_radius: int = activities_within_radius[1]
        
        df = add_found_activities_to_dataframe(nearby_search_results_list, house_location_dict, df, type_activity)
        logger.info(f"Found {len(nearby_search_results_list)}x {type_activity} in a radius of {activity_radius / 1000} km")
        
    return df

def string_to_minutes(time_string: str) -> int:
    parts: list = time_string.split()
    total_minutes: int = 0

    for i in range(0, len(parts), 2):

        if parts[i + 1] == "hours" or parts[i + 1] == "hour":
            total_minutes += int(parts[i]) * 60

        elif parts[i + 1] == "mins" or parts[i + 1] == "min":
            total_minutes += int(parts[i])

    return total_minutes

def read_raw_data():
    df = pd.read_excel(settings.rawdir / settings.raw_processed_filename)
    df['Address'] = df['Address'] + ', ' + df['Residence']
    return df

def process():
    gmaps: googlemaps.client.Client = googlemaps.Client(key = settings.gmaps_api_key)
    raw_df: pd.DataFrame = read_raw_data()
    output_df: pd.DataFrame = pd.DataFrame(columns = settings.house_activity_columns)

    for index, _ in raw_df.iterrows():
        address: str = raw_df.at[index, 'Address']
        house_location_dict: dict = {}
        house_location_dict["House_address"] = address

        house_geocode: list = gmaps.geocode(address)
        house_lat_lon_dict: dict = house_geocode[0]["geometry"]["bounds"]["northeast"]

        house_location_dict["House_lat"] = house_lat_lon_dict["lat"]
        house_location_dict["House_lng"] = house_lat_lon_dict["lng"]
        
        output_df = find_activities(settings.type_activities, house_location_dict, output_df, gmaps)
        logger.info("=====================================")

    for index, _ in output_df.iterrows():
        house_coords: str = str(output_df.at[index, 'House_lat']) + ', ' + str(output_df.at[index, 'House_lng'])
        activity_coords: str = str(output_df.at[index, 'Activity_lat']) + ', ' + str(output_df.at[index, 'Activity_lng'])

        bicycling_time: str = gmaps.directions(house_coords, activity_coords, mode = 'bicycling')[0]['legs'][0]['duration']['text']
        driving_time: str = gmaps.directions(house_coords, activity_coords, mode = 'driving')[0]['legs'][0]['duration']['text']

        output_df.at[index, 'Bicycling_total_minutes'] = string_to_minutes(bicycling_time)
        output_df.at[index, 'Driving_total_minutes'] = string_to_minutes(driving_time)
    
    output_df = output_df.drop(['House_lat', 'House_lng', 'Activity_lat', 'Activity_lng'], axis = 1)
    output_df = output_df.set_index('House_address')
    output_df.to_excel(settings.outputdir / "Huisjes.xlsx", sheet_name = "Alle_huisjes")