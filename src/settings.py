from pathlib import Path
from loguru import logger

class Settings():
    basedir: Path = Path.cwd()
    rawdir: Path = basedir / "data" / "raw"
    outputdir: Path = basedir / "data" / "processed"
    raw_processed_filename: str = "Huisjes.xlsx"
    logdir: Path = basedir / "log"
    gmaps_api_key: str = open('gmaps_api_key.txt').read()
    
    house_activity_columns: list = [
        "House_address",
        "House_lat",
        "House_lng",
        "Activity_company",
        "Activity_address",
        "Activity_lat",
        "Activity_lng",
        "Activity_type",
    ]

    type_activities: list = [
        "Supermarkt",
        "Zwembad",
        "Klimbos",
        "VR Game",
        "Lasergame",
        "Escaperoom",
        "Pretpark",
        "Basic Fit"
    ]

settings = Settings()
logger.add("logfile.log")