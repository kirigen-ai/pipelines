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

class ScalingPolicy(str, Enum):
    NONE            = "none"
    CONCURRENT      = "concurrent"
    CONNECTIONS     = "connections"
    LATENCY         = "latency"
    MEMORY          = "memory"
    PROCESSING      = "processing"

class BalancingPolicy(str, Enum):
    FIFO            = "fifo"
    RANDOM          = "random"
    ROUND_ROBIN     = "round_robin"
    LEAST_LOADED    = "least_loaded"
    PRIORITY        = "priority"

class PipelineCapabilities(str, Enum): 
    AUDIO_RECOGNITION   = "audio:recognition"     
    DATA_RECOGNITION    = "data:recognition"     
    IMAGE_RECOGNITION   = "image:recognition"     
    MODEL_RECOGNITION   = "model:recognition"     
    SONG_RECOGNITION    = "song:recognition" 
    SPEECH_RECOGNITION  = "speech:recognition"
    TEXT_RECOGNITION    = "text:recognition"     
    VIDEO_RECOGNITION   = "video:recognition"
    
    SYNTHETIC_AUDIO     = "audio:synthesis" 
    SYNTHETIC_DATA      = "data:synthesis" 
    SYNTHETIC_IMAGE     = "image:synthesis" 
    SYNTHETIC_MODEL     = "model:synthesis" 
    SYNTHETIC_SONG      = "song:synthesis" 
    SYNTHETIC_SPEECH    = "speech:synthesis"  
    SYNTHETIC_TEXT      = "text:synthesis" 
    SYNTHETIC_VIDEO     = "video:synthesis" 