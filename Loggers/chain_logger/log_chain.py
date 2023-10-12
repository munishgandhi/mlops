from datetime import datetime
import json
from celery import Celery, shared_task
from MLOps.Loggers.setEnvForRedis import set_redis_url
import constants
import requests
import os

broker_url = set_redis_url()
celery = Celery(__name__, broker="redis://localhost:6379")

def url():
    if os.environ["ENVIRONMENT"] == "dev" or os.environ["ENVIRONMENT"] == "staging":
        return constants.GRAPHQL_QA_URL
    elif '...':  # place  production port here
        return constants.GRAPHQL_PROD_URL

class ChainLogger:
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

    def create_logger_object(self):
        current_datetime = str(datetime.now())
        log_data = {
            "status": {
                "status_code": "200",
                "status_message": "Chain recorded successfully",
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
                              'input': self.tool_dict['in'],
                              'output': self.tool_dict['out'],
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
        return json.dumps(log_data)


    def send_chain_rails_api(self):
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
            "query": str(query).replace('\n', ''),
            "variables": variables
        }
        response = requests.post(url(), headers=constants.GRAPHQL_HEADER, json=query_data)
        if 'errors' in response.json():
            return print(f"Mutation failed: ", response.json())
        else:
            return
