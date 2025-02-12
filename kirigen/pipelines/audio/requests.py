# Kirigen releases 'pipelines' as an open-source library for orchestrating and managing pipelines, 
# in the hope of enableing developers to create complex workflows with ease. see https://kirigen.co/opensource-initiatives
#
# This file (as part of the 'pipelines' library) is open-source and available under the MIT license
# For more information, see the project repository at https://github.com/kirigen-ai/pipelines
#
# Copyright (c) 2025 Kirigen, all rights reserved.


from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4

from .types import AudioFormat, AudioQuality

class BaseResult(BaseModel):
    id: uuid4       = Field(description="The ID of the response", default_factory=lambda: uuid4())
    created: float  = Field(description="The creation time of the response", default_factory=lambda: float(datetime.now().timestamp())) 

class SpeechRecognitionRequest(BaseModel): 
    uri: str                    = Field(description="The uri to use for recognition", default="")
    timecodes: Optional[bool]   = Field(description="Whether to include timecodes in the response", default=False)

class SpeechSynthesisRequest(BaseModel):
    text: str                       = Field(description="The text to use for generation", default="")  
    target: Optional[str]           = Field(description="The target voice to use for generation", default=None)
    speed: Optional[float]          = Field(description="The speed to use for generation", default=1.0)    
    format: Optional[AudioFormat]   = Field(description="The format of the audio to generate", default=AudioFormat.WAV)
    quality: Optional[AudioQuality] = Field(description="The quality to use for generation", default=AudioQuality.HIGH)
    source_uri: Optional[str]       = Field(description="The source audio to use for generation", default=None)

class SpeechRecognitionResult(BaseResult):     
    text: str             = Field(description="The text of the speech recognized", default="")

class SpeechSynthesisResult(BaseResult):     
    audio: bytes          = Field(description="The audio generated", default_factory=bytes)
    length: float         = Field(description="The length of the audio", default=0.0)
    format: AudioFormat   = Field(description="The format of the audio", default=AudioFormat.WAV)
