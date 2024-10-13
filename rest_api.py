from fastapi import FastAPI, Response
import datetime
import math
from db import get_record_count, get_logs
import yaml

config = yaml.safe_load(open("config.yml"))
DB_NAME = config["DB_NAME"]

app = FastAPI()

def date_formatting(date):
    result = ""
    try:
        result = datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
        result = result.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        result = ""
    return result

@app.get("/logs")
async def get_logs_api(response: Response, user_id: int = 0, page: int = 1, page_size: int = 5, date_from: str = "", date_to: str = ""):
    response_obj = {}
    if(user_id >= 0):
        formatted_date_from = date_formatting(date_from)
        formatted_date_to = date_formatting(date_to)
        if(date_from != "" and formatted_date_from == ""):
            response.status_code = 400
            response_obj = {"Error":"incorrect date_from format. The date have folowing format - \"YYYY-MM-DD HH:mm:ss\"."}
        elif(date_to != "" and formatted_date_to == ""):
            response.status_code = 400
            response_obj = {"Error":"incorrect date_from format. The date have folowing format - \"YYYY-MM-DD HH:mm:ss\"."}
        else:
            record_count = await get_record_count(DB_NAME, user_id, formatted_date_from, formatted_date_to)
            page_count = int(math.ceil(record_count / page_size))
            if(page_count < page and record_count != 0):
                response.status_code = 400
                response_obj = {"Error":"page goes beyond page count. Try using default parameters to find out the correct values for pagination."}
            else:
                logs = await get_logs(DB_NAME, user_id, page, page_size, formatted_date_from, formatted_date_to)
                response_obj = {"logs":logs}
                response_obj["page"] = page
                response_obj["page_size"] = page_size
                response_obj["record_count"] = record_count
                response_obj["page_count"] = page_count
    else:
        response.status_code = 400
        response_obj = {"Error":"user id cannot be negative."}
    return response_obj
