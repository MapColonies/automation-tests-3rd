# pylint: disable=line-too-long, invalid-name, fixme
"""This module provide test full functionality """
import json
import logging
import os
import time
from datetime import datetime, timedelta
from server_automation.ingestion_api import model_ingestion
from server_automation.configuration import config
from mc_automation_tools import common as common
from mc_automation_tools import base_requests as br
from mc_automation_tools import s3storage as s3

_logger = logging.getLogger("server_automation.function.executors")


def send_ingestion_request(request, request_name=None):
    """
    This method use ingestion api wrapping class to start new ingestion process
    """
    if request_name:
        request['metadata']['identifier'] = request_name

    _logger.info('Send request: %s to export ', request['metadata']['identifier'])
    # request = json.dumps(request)
    im = model_ingestion.IngestionModel()
    resp = im.post_model_ingestion_job(request)
    status_code, content = common.response_parser(resp)
    _logger.info('Response of trigger returned with status: %d', status_code)
    return status_code, content


def follow_ingestion_model_process(job_id):
    """
    This method follow the ingestion job and return result on finish
    :param job_id: current job id
    """
    im = model_ingestion.IngestionModel()

    retry_completed = 0
    if not isinstance(job_id, str):
        raise Exception("uuid param type should be string (str)! ")

    t_end = time.time() + config.MAX_INGESTION_RUNNING_TIME
    running = True
    while running:

        resp = im.get_single_job_status(job_id)
        status_code = resp.status_code
        content = json.loads(resp.text)
        percentage = content['percentage']
        status = content['status']
        if config.ResponseCode.Ok.value != status_code:
            raise RuntimeError(f'Error on ingestion job status service with error {status_code}:{resp.text}')

        if status == config.INGESTION_STATUS_FAILED:
            raise Exception("Failed on ingestion on task %s" % job_id)
        if not status == config.INGESTION_STATUS_COMPLITED:
            time.sleep(10)
            # retry_completed += 1
            # if retry_completed > 2:
            #     raise Exception("Error on closing task %s" % uuid)

        current_time = time.time()
        # running = not (progress == 100 and status == config.EXPORT_STATUS_COMPLITED) and current_time < t_end
        running = not (status == config.INGESTION_STATUS_COMPLITED) and current_time < t_end

        _logger.info(
            f'Received from job(id): {job_id} ,with status code: {status_code}, status: {status} and percentage: {percentage}')

        if current_time > t_end:
            _logger.error("Got timeout and will stop running progress validation")
            raise Exception("got timeout while following task running")



    # _logger.info(
    #     'Finish exporter job according status index service and file should be places on: %s', (response_dict['link']))
    # results = {
    #     'taskId': response_dict['taskId'],
    #     'fileName': response_dict['fileName'],
    #     'directoryName': response_dict['directoryName'],
    #     'fileURI': response_dict['link'],
    #     'expirationTime': response_dict['expirationTime']
    #
    # }
    return content
