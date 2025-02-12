# Kirigen releases 'pipelines' as an open-source library for orchestrating and managing pipelines, 
# in the hope of enableing developers to create complex workflows with ease. see https://kirigen.co/opensource-initiatives
#
# This file (as part of the 'pipelines' library) is open-source and available under the MIT license
# For more information, see the project repository at https://github.com/kirigen-ai/pipelines
#
# Copyright (c) 2025 Kirigen, all rights reserved.

from typing import List, Union

from .base import (
    # import the base classes from the base module
    Pipeline, PipelineFlow, PipelineProvider
)

from .types import ( 
    # import the types from the types module
    BalancingPolicy
)

# Queues
QUEUE_TYPES = Union['BatchFlow', 'ConcurrentFlow', 'LoadBalancedFlow', 'ParallelFlow', 'PriorityFlow', 'SequentialFlow']

class BatchFlow(PipelineFlow):
    def __init__(self, name: str, max_requests:int = 1, policy:BalancingPolicy = BalancingPolicy.FIFO, provider: PipelineProvider = None, streams: List[QUEUE_TYPES] = None):
        super().__init__( name=name, max_requests=max_requests, policy=policy, provider=provider, streams=streams)

class ConcurrentFlow(PipelineFlow):
    def __init__(self, name: str, max_requests:int = 1, policy:BalancingPolicy = BalancingPolicy.FIFO, provider: PipelineProvider = None, streams: List[QUEUE_TYPES] = None):
        super().__init__( name=name, max_requests=max_requests, policy=policy, provider=provider, streams=streams)

class LoadBalancedFlow(PipelineFlow):
    def __init__(self, name: str, max_requests:int = 1, policy:BalancingPolicy = BalancingPolicy.LEAST_LOADED, provider: PipelineProvider = None, streams: List[QUEUE_TYPES] = None):
        super().__init__( name=name, max_requests=max_requests, policy=policy, provider=provider, streams=streams)

class ParallelFlow(PipelineFlow):
    def __init__(self, name: str, max_requests:int = 1, policy:BalancingPolicy = BalancingPolicy.PRIORITY, provider: PipelineProvider = None, streams: List[QUEUE_TYPES] = None):
        super().__init__( name=name, max_requests=max_requests, policy=policy, provider=provider, streams=streams)

class PriorityFlow(PipelineFlow):
    def __init__(self, name: str, max_requests:int = 1, policy:BalancingPolicy = BalancingPolicy.PRIORITY, provider: PipelineProvider = None, streams: List[QUEUE_TYPES] = None):
        super().__init__( name=name, max_requests=max_requests, policy=policy, provider=provider, streams=streams)

class SequentialFlow(PipelineFlow):
    def __init__(self, name: str, max_requests:int = 1, policy:BalancingPolicy = BalancingPolicy.FIFO, provider: PipelineProvider = None, streams: List[QUEUE_TYPES] = None):
        super().__init__( name=name, max_requests=max_requests, policy=policy, provider=provider, streams=streams)

__all__ = [
    # Base
    "Pipeline"

    # Queues
    "BatchFlow", "ConcurrentFlow", "LoadBalancedFlow", "ParallelFlow", "PriorityFlow", "SequentialFlow",
]