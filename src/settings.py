from pathlib import Path
from pydantic import BaseModel
from loguru import logger

class Settings(BaseModel):
    basedir: Path = Path.cwd()
    outputdir: Path = Path("processed_data")
    logdir: Path = basedir / "log"
    
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

    addresses: list = [
        "Oosteinde 14, Wapserveen",
        "Marktvelderweg, Haaksbergen",
        "Groenendries, Huijbergen",
        "Oldenzaalsestraat 135, Losser",
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