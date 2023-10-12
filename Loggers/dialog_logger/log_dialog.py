from datetime import datetime
import json
from celery import Celery, shared_task
from MLOps.Loggers.setEnvForRedis import set_redis_url
import constants
import requests
import os
import time

broker_url = set_redis_url()
celery = Celery(__name__, broker="redis://localhost:6379")

def calculate_total_time(start_time, end_time):
    total_time_seconds = end_time - start_time
    total_time = f"{total_time_seconds:.2f}s" if total_time_seconds < 60 else \
        f"{total_time_seconds / 60:.2f} minutes"
    return total_time

def url():
    if os.environ["ENVIRONMENT"] == "dev" or os.environ["ENVIRONMENT"] == "staging":
        return constants.GRAPHQL_QA_URL
    elif '...':  # place  production port here
        return constants.GRAPHQL_PROD_URL

# Define a class for the dialog logger
class DialogLogger:

    # Initialize the class with the required attributes
    def __init__(self, request_data, event_type, activity, tool_dict, log_name, app_subsection, app_name, conversation_id, message_id):
        self.request_data = request_data
        self.event_type = event_type
        self.activity = activity
        self.tool_dict = tool_dict
        self.log_name = log_name
        self.app_subsection = app_subsection
        self.app_name = app_name
        self.conversation_id = conversation_id
        self.message_id = message_id

    # Define a method to create the logger object
    def create_logger_object(self):
        create_log_object_start_chk = time.time()
        current_datetime = str(datetime.now())
        log_data = {
            "status": {
                "status_code": "200",
                "status_message": "Dialog recorded successfully",
            },
            "app": {
                "environment": self.request_data.get("environment"),
                "app_url": self.request_data.get("app_url"),
                "app_name": self.app_name,
                "app_subsection": self.app_subsection,
                "app_section": ""
            },
            "action": {
                "bot_url": "",
                "api_call": self.request_data.get("api_call"),
                "priority": "High",
                "event_type": self.event_type,
                "activity": self.activity,
                "parameter": {'input': self.tool_dict['input'],
                              'output': self.tool_dict['output'],
                              'duration': self.tool_dict['duration']
                             },
            },
            "statistics": {
                "num_prospects": "null",
                "response_time": ""
            },
            "severity": "INFO",
            "logName": self.log_name,
            "receiveTimestamp": current_datetime,
            "signal_dt": current_datetime,
            "timestamp": current_datetime
        }
        create_log_object_end_chk = time.time()
        create_log_object_duration_chk = calculate_total_time(create_log_object_start_chk, create_log_object_end_chk)
        print("create_log_object_duration_chk: ", create_log_object_duration_chk)
        return json.dumps(log_data)

    # Define a method to create the dialog api

    def send_dialog_rails_api(self):
        send_dialog_rails_api_start_chk = time.time()
        # status_message = 'Dialog has been recorded successfully'
        query = """mutation ($input: createHayleyMessageMutationInput!) {createHayleyMessage(input: $input) {hayleyMessage{id text feedback ownerType queryType propertyId propertyName orgId orgName toolName conversation{id numberOfTokens messagesCount}}}}"""
        variables = {
            'input': {
                       "coversationId": self.conversation_id,
                       "message_id": self.message_id,
                       "text": "tool name testing m2",
                       "ownerType": "prospect",
                       "toolName": self.app_subsection,
                       "log_object": self.create_logger_object()
            }
        }
        query_data = {
            "query": query,
            "variables": variables
        }
        response = requests.post(url(), headers=constants.GRAPHQL_HEADER, json=query_data)
        if 'errors' in response.json():
            send_dialog_rails_api_end_chk = time.time()
            send_dialog_rails_api_duration_chk = calculate_total_time(send_dialog_rails_api_start_chk, send_dialog_rails_api_end_chk)
            print("send_dialog_rails_api_duration_chk: ", send_dialog_rails_api_duration_chk)
            return print(f"Mutation failed: ", response.json())
        else:
            send_dialog_rails_api_end_chk = time.time()
            send_dialog_rails_api_duration_chk = calculate_total_time(send_dialog_rails_api_start_chk, send_dialog_rails_api_end_chk)
            print("send_dialog_rails_api_duration_chk: ", send_dialog_rails_api_duration_chk)
            return



