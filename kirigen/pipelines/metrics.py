# Kirigen releases 'pipelines' as an open-source library for orchestrating and managing pipelines, 
# in the hope of enableing developers to create complex workflows with ease. see https://kirigen.co/opensource-initiatives
#
# This file (as part of the 'pipelines' library) is open-source and available under the MIT license
# For more information, see the project repository at https://github.com/kirigen-ai/pipelines
#
# Copyright (c) 2025 Kirigen, all rights reserved.


import os, asyncio, time
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Union, Generic, TypeVar, AsyncIterator

class PipelineRequestMetrics(BaseModel):
    start_time: float               # Time the request was received
    queue_time: float               # Time spent in the queue
    provider_processing_time: float # Time spent processing the request by the provider
    total_processing_time: float    # Total time spent processing the request (queue + provider)
    
    def complete(self):
        self.total_processing_time = time.time() - self.start_time

class ImagePipelineRequestMetrics(PipelineRequestMetrics):
    provider_name: str          # name of the provider
    num_steps: int              # number of steps taken to generate the image
    image_format: str           # format of the image
    image_size: tuple           # size of the image
    image_orientation: str      # orientation of the image
    image_aspect_ratio: float   # aspect ratio of the image
    metadata: dict[str, str]    # image metadata

class StoragePipelineRequestMetrics(PipelineRequestMetrics):    
    provider_name: str                      # name of the provider    
    operations: Dict[str, int]              # operations performed by the provider
    avg_operation_time: Dict[str, float]    # average time per operation