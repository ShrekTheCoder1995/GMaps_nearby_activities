import googlemaps
import pandas as pd
from settings import settings, logger

def add_found_activities_to_dataframe(nearby_search_results_list: list, df_dict: dict, df: pd.DataFrame, type_activity: str,) -> pd.DataFrame:

    for nearby_search_result_dict in nearby_search_results_list:
        df_dict["Activity_company"] = [nearby_search_result_dict["name"]]
        df_dict["Activity_address"] = [nearby_search_result_dict["vicinity"]]
        df_dict["Activity_lat"] = [nearby_search_result_dict["geometry"]["location"]["lat"]]
        df_dict["Activity_lng"] = [nearby_search_result_dict["geometry"]["location"]["lng"]]
        df_dict["Activity_type"] = [type_activity]
        df = pd.concat([df, pd.DataFrame(df_dict)], ignore_index=True)

    return df

def find_activities_within_radius(df_dict: dict, type_activity: str, gmaps: googlemaps.client.Client) -> tuple:
    nearby_search_results_list: list = []
    activity_radius: int = 5000

    while(len(nearby_search_results_list) <= 3):
        nearby_search_results_list: list = gmaps.places_nearby(location=(df_dict["House_lat"], df_dict["House_lng"]),radius = activity_radius, keyword = type_activity)["results"]
        activity_radius += 5000  # When there are less than 3 activities found within the radius, add 5 km to the radius.

    return nearby_search_results_list, activity_radius

def find_activities(type_activities: list, df_dict: dict, df: pd.DataFrame, gmaps: googlemaps.client.Client) -> pd.DataFrame:

    for type_activity in type_activities:

        activities_within_radius: tuple = find_activities_within_radius(df_dict, type_activity, gmaps)
        nearby_search_results_list: list = activities_within_radius[0]
        activity_radius: int = activities_within_radius[1]

        print(f"Radius {type_activity}: {activity_radius}")
        df = add_found_activities_to_dataframe(nearby_search_results_list, df_dict, df, type_activity)

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

def process():
    gmaps: googlemaps.client.Client = googlemaps.Client(key = "AIzaSyCMhlhc38k2F_3l4lhNafmV8r6lzRXP2-8")
    df: pd.DataFrame = pd.DataFrame(columns = settings.house_activity_columns)

    for address in settings.addresses:
        df_dict: dict = {}
        df_dict["House_address"] = address

        house_geocode: list = gmaps.geocode(address)
        house_lat_lon_dict: dict = house_geocode[0]["geometry"]["bounds"]["northeast"]
        df_dict["House_lat"] = house_lat_lon_dict["lat"]
        df_dict["House_lng"] = house_lat_lon_dict["lng"]

        df = find_activities(settings.type_activities, df_dict, df, gmaps)
        print("=====================================")

    for index, row in df.iterrows():
        house_coords: str = str(df.at[index, 'House_lat']) + ', ' + str(df.at[index, 'House_lng'])
        activity_coords: str = str(df.at[index, 'Activity_lat']) + ', ' + str(df.at[index, 'Activity_lng'])

        bicycling_time: str = gmaps.directions(house_coords, activity_coords, mode = 'bicycling')[0]['legs'][0]['duration']['text']
        driving_time: str = gmaps.directions(house_coords, activity_coords, mode = 'driving')[0]['legs'][0]['duration']['text']
    
        df.at[index, 'Bicycling_total_minutes'] = string_to_minutes(bicycling_time)
        df.at[index, 'Driving_total_minutes'] = string_to_minutes(driving_time)
    
    df = df.drop(['House_lat', 'House_lng', 'Activity_lat', 'Activity_lng'], axis = 1)
    df = df.set_index('House_address')
    df.to_excel("Huisjes.xlsx", sheet_name = "Alle_huisjes")