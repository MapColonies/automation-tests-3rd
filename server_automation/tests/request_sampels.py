# pylint: disable=line-too-long, raise-missing-from, trailing-comma-tuple
"""This module provide generation of several request json files for testing purpose"""
import json
import enum
from server_automation.configuration import config


# class BoxSize(enum.Enum):
#     """ Size of bbox """
#     Sanity = 1,
#     Small = 10,
#     Medium = 50,
#     Big = 150


# class ZoomLevels(enum.Enum):
#     """
#     Types of zoom levels
#     """
#     default = 18
#     med = 15


_sanity_request = {
  "modelPath": "/mo",
  "metadata": {
    "identifier": "string",
    "typename": "string",
    "schema": "string",
    "mdSource": "string",
    "xml": "string",
    "anytext": "string",
    "insertDate": "2021-05-10T10:34:23.385Z",
    "creationDate": "2021-05-10T10:34:23.385Z",
    "validationDate": "2021-05-10T10:34:23.385Z",
    "wktGeometry": "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))",
    "title": "string",
    "producerName": "IDFMU",
    "description": "string",
    "type": "string",
    "classification": "string",
    "srs": "string",
    "projectName": "string",
    "version": "string",
    "centroid": "string",
    "footprint": "string",
    "timeBegin": "2021-05-10T10:34:23.385Z",
    "timeEnd": "2021-05-10T10:34:23.385Z",
    "sensorType": "string",
    "region": "string",
    "nominalResolution": "string",
    "accuracyLE90": "string",
    "horizontalAccuracyCE90": "string",
    "relativeAccuracyLE90": "string",
    "estimatedPrecision": "string",
    "measuredPrecision": "string",
    "links": [
      {
        "name": "string",
        "description": "string",
        "protocol": "string",
        "url": "string"
      }
    ]
  }
}







