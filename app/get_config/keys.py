from yaml import safe_load

with open("config.yaml", 'r') as file:
    data_from_file = safe_load(file)

weather_token = data_from_file["Weather_token"]
time_live = data_from_file["TimeToLive"]