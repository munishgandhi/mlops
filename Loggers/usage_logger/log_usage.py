from datetime import datetime
import json
from celery import Celery, shared_task
from setEnvForRedis import set_redis_url
import constants
import requests
import os

broker_url = set_redis_url()
celery = Celery(__name__, broker=f'{broker_url}/0')

def url():
    if os.environ["ENVIRONMENT"] == "dev" or os.environ["ENVIRONMENT"] == "staging":
        return constants.GRAPHQL_QA_URL
    elif '...':  # place  production port here
        return constants.GRAPHQL_PROD_URL

# Define a class for the usage logger
class UsageLogger:

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
        current_datetime = str(datetime.now())
        log_data = {
            "status": {
                "status_code": "200",
                "status_message": "Usage recorded successfully",
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
                "parameter": {
                              'duration': self.tool_dict['total_time'],
                              'total_cost': self.tool_dict['total_cost'],
                              'prompt_tokens': self.tool_dict['prompt_tokens'],
                              'completion_tokens': self.tool_dict['completion_tokens'],
                              'total_tokens': self.tool_dict['total_tokens'],
                              'thread_id': self.tool_dict['thread_id']
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
        return json.dumps(log_data)

    # Define a method to create the usage api

    def send_usage_rails_api(self):
        # status_message = 'Usage has been recorded successfully'
        query = """
              mutation ($input: createMessageMutationInput!) { 
                  createMessage(input: $input) { 
                      message
                  }
              }
              """
        variables = {
            'input': {
                "coversationId": self.conversation_id,
                "message_id": self.message_id,
                "log_object": self.create_logger_object(),
                "toolName": self.app_subsection,
                "queryType": "usage",
                "ownerType": "prospect"
                     }
                    }
        query_data = {
            "query": query,
            "variables": variables
        }
        response = requests.post(url(), headers=constants.GRAPHQL_HEADER, json=query_data)
        if 'errors' in response.json():
            print(response.json())
            return print(f"Mutation failed with status code {response.status_code}")
        else:
            return
def send_usage_signals(tool_info, app_name, conversation_id, message_id, request_data):
    # Create an instance of the usage logger class with the given parameters
    usage_logger = UsageLogger(request_data, "usage", 'usage_record_logging', list(tool_info.values())[0],'usage_log', list(tool_info.keys())[0], app_name, conversation_id, message_id)
    # Call the create_usage_api method with the conversation id
    usage_logger.send_usage_rails_api()
