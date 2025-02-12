# Kirigen releases 'pipelines' as an open-source library for orchestrating and managing pipelines, 
# in the hope of enableing developers to create complex workflows with ease. see https://kirigen.co/opensource-initiatives
#
# This file (as part of the 'pipelines' library) is open-source and available under the MIT license
# For more information, see the project repository at https://github.com/kirigen-ai/pipelines
#
# Copyright (c) 2025 Kirigen, all rights reserved.

from enum import Enum

class AudioQuality(str, Enum):
    LOW     = "low" 
    MEDIUM  = "medium" 
    HIGH    = "high" 

class AudioFormat(str, Enum):
    WAV     = "wav" 
    MP3     = "mp3" 
    OGG     = "ogg" 
    FLAC    = "flac" 
    