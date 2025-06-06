from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
db = client["VideoSurveillance"]

series_collection = db["series"]
events_collection = db["motion_events"]


def insert_series(data):
    return series_collection.insert_one(data).inserted_id


def get_all_series():
    return list(series_collection.find())


def get_series_by_name(name):
    return series_collection.find_one({"name": name})


def insert_motion_event(event_data):
    return events_collection.insert_one(event_data).inserted_id


def get_all_motion_events():
    return list(events_collection.find())
