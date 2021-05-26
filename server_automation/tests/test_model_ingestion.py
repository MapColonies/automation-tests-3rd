# pylint: disable=line-too-long, invalid-name, broad-except, duplicate-code
""" This module responsible of testing export tools - server side:"""
import json
import logging
import time
from datetime import datetime
from server_automation.functions import executors as exc
from server_automation.configuration import config
from mc_automation_tools import common as common
from server_automation.tests import request_sampels

# from conftest import ValueStorage

_log = logging.getLogger('server_automation.tests.3RD_ingestion_process')
Z_TIME = datetime.now().strftime('_%Y%m_%d_%H_%M_%S')


def test_upload_model():
    """
    This test validate and testing validate E2E process of ingesting new model into db via upload / ingestion api
    """
    _log.info('Start running test: %s', test_upload_model.__name__)
    request = request_sampels.get_request(request_sampels.RequestsPool.sanity.name)
    assert request, \
        f'Test: [{test_upload_model.__name__}] Failed: File not exist or failure on loading request json'
    identifier = "_".join(['test_upload_model', Z_TIME])
    request['metadata']['identifier'] = identifier

    # start ingestion
    s_code, content = exc.send_ingestion_request(request)
    assert s_code == config.ResponseCode.IngestionModelOk.value, \
        f'Test: [{test_upload_model.__name__}] Failed: Ingestion model api return status code [{s_code}]'

    # validating running ingestion process
    job_id = content['jobId']
    res = None
    try:
        err = 'unknown'
        res = exc.follow_ingestion_model_process(job_id)
    except Exception as e:
        err = str(e)
    assert res, \
        f'Test: [{test_upload_model.__name__}] Failed: on follow (ingestion job stage) with message: [{err}]'

    # validating metadata of new ingested model
    try:
        res, errors = exc.validate_ingested_model(identifier, request)
        err = errors
    except Exception as e:
        err = str(e)

    assert res, \
        f'Test: [{test_upload_model.__name__}] Failed: validation metadata (model on catalog db) with message: [{err}]'

    # validating new model on storage
    try:
        err = 'unknown'
        res = exc.validate_model_on_storage(identifier, job_id)
    except Exception as e:
        err = str(e)
    assert res, \
        f'Test: [{test_upload_model.__name__}] Failed: on Storage validation with message: [{err}]'

test_upload_model()