# Kirigen releases 'pipelines' as an open-source library for orchestrating and managing pipelines, 
# in the hope of enableing developers to create complex workflows with ease. see https://kirigen.co/opensource-initiatives
#
# This file (as part of the 'pipelines' library) is open-source and available under the MIT license
# For more information, see the project repository at https://github.com/kirigen-ai/pipelines
#
# Copyright (c) 2025 Kirigen, all rights reserved.


from ..metrics import PipelineRequestMetrics

class SpeechPipelineRequestMetrics(PipelineRequestMetrics):
    provider_name: str              # name of the provider 
    bandwidth_used: float           # total bandwidth used in MB 
    handled_requests: int           # number of requests handled by the provider 
    max_concurrent_requests: int    # peak number of concurrent requests 
    total_generated_audio: float    # total number of seconds of audio generated 
    total_audio_processed: float    # total number of seconds of audio processed 