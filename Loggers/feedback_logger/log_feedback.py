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

# Define a class for the feedback logger
class FeedbackLogger:

    # Initialize the class with the required attributes
    def __init__(self, request_data, event_type, activity, feedback_string, log_name, app_subsection, app_name, message_id):
        self.request_data = request_data
        self.event_type = event_type
        self.activity = activity
        self.feedback_string = feedback_string
        self.log_name = log_name
        self.app_subsection = app_subsection
        self.app_name = app_name
        self.message_id = message_id

    # Define a method to create the logger object
    def create_logger_object(self):
        current_datetime = str(datetime.now())
        log_data = {
            "status": {
                "status_code": "200",
                "status_message": "Feedback recorded successfully",
            },
            "app": {
                "environment": self.request_data.get("environment"),
                "app_url": self.request_data.get("app_url"),
                "app_name": self.app_name,
                "app_subsection": "",
                "app_section": ""
            },
            "action": {
                "bot_url": "",
                "api_call": self.request_data.get("api_call"),
                "priority": "High",
                "event_type": self.event_type,
                "activity": self.activity,
                "parameter": {
                              'feedback': self.feedback_string
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

    # Define a method to create the feedback api

    def send_feedback_rails_api(self):
        # status_message = 'Feedback has been recorded successfully'
        query = """mutation ($input: saveMessageFeedbackMutationInput!) {saveMessageFeedback(input: $input) {hayleyMessage{text feedback ownerType queryType propertyId propertyName orgId orgName conversation{id numberOfTokens messagesCount sessionId entryId}}}}"""
        variables = {
            'input': {
                "id": self.message_id,
                "log_object": self.create_logger_object(),
                "feedback": self.feedback_string
            }
        }
        query_data = {
            "query": query,
            "variables": variables
        }
        response = requests.post(url(), headers=constants.GRAPHQL_HEADER, json=query_data)
        if 'errors' in response.json():
            return print(f"Mutation failed: ", response.json())
        else:
            return

def send_feedback_signals(tool_info, tool, app_name, message_id, request_data):
    # Create an instance of the feedback logger class with the given parameters
    feedback_logger = FeedbackLogger(request_data, tool_info, 'feedback_record_logging', tool_info,'feedback_log', tool, app_name, message_id)
    # Call the create_feedback_api method with the message id
    feedback_logger.send_feedback_rails_api()
