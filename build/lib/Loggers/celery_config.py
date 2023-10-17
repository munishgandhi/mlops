from celery import Celery, shared_task
from MLOps.Loggers.setEnvForRedis import set_redis_url
from MLOps.Loggers.chain_logger.log_chain import ChainLogger
from MLOps.Loggers.dialog_logger.log_dialog import DialogLogger
from MLOps.Loggers.feedback_logger.log_feedback import FeedbackLogger
from MLOps.Loggers.usage_logger.log_usage import UsageLogger

broker_url = set_redis_url()
celery = Celery(__name__, broker="redis://localhost:6379")

@shared_task
def send_chain_signals(tool_info, app_name, conversation_id, message_id, request_data):
    logger = ChainLogger(request_data, "chain", 'chain_record_logging', list(tool_info.values())[0],'chain_log', list(tool_info.keys())[0], app_name, conversation_id, message_id)
    logger.send_chain_rails_api()

@shared_task
def send_dialog_signals(tool_info, tool, app_name, conversation_id, message_id, request_data):
    # Create an instance of the dialog logger class with the given parameters
    dialog_logger = DialogLogger(request_data, "dialog", 'dialog_record_logging', tool_info,'dialog_log', tool, app_name, conversation_id, message_id)
    # Call the create_dialog_api method with the conversation id
    dialog_logger.send_dialog_rails_api()

@shared_task
def send_feedback_signals(tool_info, tool, app_name, message_id, request_data):
    # Create an instance of the feedback logger class with the given parameters
    feedback_logger = FeedbackLogger(request_data, tool_info, 'feedback_record_logging', tool_info,
                                     'feedback_log', tool, app_name, message_id)
    # Call the create_feedback_api method with the message id
    feedback_logger.send_feedback_rails_api()

@shared_task
def send_usage_signals(tool_info, app_name, conversation_id, message_id, request_data):
    # Create an instance of the usage logger class with the given parameters
    usage_logger = UsageLogger(request_data, "usage", 'usage_record_logging', list(tool_info.values())[0],'usage_log', list(tool_info.keys())[0], app_name, conversation_id, message_id)
    # Call the create_usage_api method with the conversation id
    usage_logger.send_usage_rails_api()