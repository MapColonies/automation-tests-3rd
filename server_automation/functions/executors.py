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
    try:
        _logger.info(f'Will load model from directory: {request["modelPath"]}')
        resp = im.post_model_ingestion_job(request)
        status_code, content = common.response_parser(resp)
        _logger.info('Response of [3d model ingestion service] returned with status: %d', status_code)
    except Exception as e:
        status_code = config.ResponseCode.ServerError.value
        content = str(e)
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
            raise Exception(f"Failed on ingestion on task {job_id}:{content['reason']}")
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

        if status == config.INGESTION_STATUS_FAILED:
            raise RuntimeError(f'Ingestion job {job_id} failed [status={status}] with content:\n{content}')
        if current_time > t_end:
            _logger.error("Got timeout and will stop running progress validation")
            raise Exception("got timeout while following task running")

    _logger.info(f'Finish following ingestion process, with status: {status}')
    return content


def compare_model_metadata(metadata_1, metadata_2):
    """This method execute validation of 2 3rd model metadata according configurable key list"""
    none_equal = []
    not_exists_metadata_1 = []
    not_exists_metadata_2 = []
    is_equal = True
    for key in config.INGESTION_MANDATORY_METADATA:
        val_1 = metadata_1.get(key)
        val_2 = metadata_2.get(key)
        if not val_1:
            not_exists_metadata_1.append(key)
        if not val_2:
            not_exists_metadata_2.append(key)
        if not val_1 or not val_2:
            continue
        if val_1 != val_2:
            none_equal.append({key: [val_1, val_2]})

    if not_exists_metadata_1:
        _logger.info(f'ingested model not contain metadata keys:\n {not_exists_metadata_1}')
        is_equal = False

    if not_exists_metadata_2:
        _logger.info(f'request metadata for model not contain metadata keys:\n {not_exists_metadata_2}')
        is_equal = False

    if none_equal:
        _logger.info(f'Metadata of ingested model not equal to request metadata:\n {none_equal}')
        is_equal = False

    result_dict = {'none_equal': none_equal, 'not_exists_metadata_1': not_exists_metadata_1,
                   'not_exists_metadata_2': not_exists_metadata_2}
    return is_equal, result_dict


def validate_ingested_model(identifier, request):
    """
    This method validating the model exists and ingested to system - both s3 and catalog db according provided identifier id
    :param identifier: id of ingested model
    :param request: original ingestion request for model
    """
    im = model_ingestion.IngestionModel()
    _logger.info(f'Validating job:{identifier} placed on catalog db')
    if im.is_model_on_catalog(identifier):
        _logger.info(f'[OK] job:{identifier} placed on catalog db')
        _logger.info(f'Validating metadata of job:{identifier}')
        res = im.get_single_3rd_metadata(identifier)
        status_code = res.status_code
        if status_code == config.ResponseCode.Ok.value:
            content = json.loads(res.text)
            res, res_dict = compare_model_metadata(content, request['metadata'])
            _logger.info(f'Metadata of job:{identifier} validation ok {[res]}')
            return res, res_dict

        else:
            _logger.error(f'Model with identifier:{identifier} return status: {status_code} from service catalog ')
            raise Exception(f'Model with identifier:{identifier} return status: {status_code} from service catalog ')

    else:
        _logger.error(f'Model with identifier:{identifier} not exists on catalog db ')
        raise Exception(f'Model with identifier:{identifier} not exists on catalog db ')


def get_tileset_from_s3(identifier, job_id):
    """
    This method download relevant tileset.json directly from s3 by identifier
    """
    try:
        s3_client = s3.S3Client(config.S3_END_POINT, config.S3_ACCESS_KEY, config.S3_SECRET_KEY)
        bucket_exists = s3_client.is_bucket_exists(config.S3_BUCKET_NAME)
        source = common.combine_url(job_id, 'tileset.json')

        destination_dir = os.path.join(config.TMP_DIR, job_id)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        dest = os.path.join(config.TMP_DIR, source)
        if bucket_exists[0]:
            try:
                s3_client.download_from_s3(config.S3_BUCKET_NAME, source, dest)
                return os.path.join(config.TMP_DIR, job_id,'tileset.json')
            except Exception as e:
                _logger.error(f'Failed on downloading {identifier}/tileset.json from S3 with error: {str(e)}')
                raise Exception(f'Failed on downloading {identifier}/tileset.json from S3 with error: {str(e)}')

        else:
            _logger.error(f'Failed on connecting to bucket with error: {bucket_exists[2]}')
            raise Exception(f'Failed on connecting to bucket with error: {bucket_exists[2]}')

    except Exception as e:
        _logger.error(f'Failed on connecting S3 with error: {str(e)}')
        raise Exception(f'Failed on connecting S3 with error: {str(e)}')


def validate_model_on_storage(identifier, job_id):
    """
    This method validate uploaded model on storage OS / FS based on provided url from catalog db
    :param identifier: model's identifier
    :param job_id: uuid represent the ingestion id for the specific model
    """
    tileset = None
    im = model_ingestion.IngestionModel()
    _logger.info(f'Validating job:{identifier} placed on storage according tileset.json file')
    res = im.get_single_3rd_metadata(identifier)
    content = json.loads(res.text)
    url = content['links'].split(',')[3]
    if config.S3_TILE_LINK_SOURCE:
        tileset = get_tileset_from_s3(identifier, job_id)
        tileset = json.load(open(tileset))
    else:
        try:
            tileset = br.send_get_request(url)
        except Exception as e:
            _logger.error(f'Failed on downloading tileset.json file!\n'
                          f'Given url {url}\n'
                          f'With error: {str(e)}')

    _logger.info(f'New model placed OK on storage ')

    return tileset