# Kirigen releases 'pipelines' as an open-source library for orchestrating and managing pipelines, 
# in the hope of enableing developers to create complex workflows with ease. see https://kirigen.co/opensource-initiatives
#
# This file (as part of the 'pipelines' library) is open-source and available under the MIT license
# For more information, see the project repository at https://github.com/kirigen-ai/pipelines
#
# Copyright (c) 2025 Kirigen, all rights reserved.


from abc import abstractmethod
import os, asyncio, time, uuid
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Set, Optional, Union, Generic, TypeVar, AsyncIterator

from .metrics import (
    # import the metrics from the metrics module
    PipelineRequestMetrics, ImagePipelineRequestMetrics, StoragePipelineRequestMetrics
)

from .types import ( 
    # import the types from the types module
    ScalingPolicy, BalancingPolicy, PipelineCapabilities
)

METRIC_TYPE = Union[PipelineRequestMetrics|ImagePipelineRequestMetrics|StoragePipelineRequestMetrics]
    
class Pipeline:
    """Base class for implementing provider pipelines with scaling capabilities.

    This class serves as a foundation for creating provider-specific pipeline implementations 
    that support dynamic instance scaling and telemetry collection.

    Args:
        instances (int): Number of initial pipeline instances. Minimum 1. Defaults to 1.
        max_instances (int): Maximum allowed instances. -1 for unlimited. Defaults to 1.
        scale_policy (ScalingPolicy): Instance scaling policy. Defaults to NONE.
        cooldown (int): Seconds between scaling operations. -1 disables cooldown. Defaults to -1.
        scale_to_zero (bool): Allow scaling to zero instances. Defaults to True.
        enable_telemetry (bool): Enable metrics collection. Defaults to True.
        streams (List[PipelineFlow]): Pipeline flows to distribute across instances.

    Properties:
        request_metrics: Gets metrics for a specific request by ID
        telemetry: Returns pipeline telemetry data
        capabilities: Returns set of supported pipeline capabilities

        The pipeline will maintain at least one instance unless scale_to_zero=True and both cooldown and max_instances are set to positive values.
    """
    def __init__(self, 
        instances: int = 1, 
        max_instances: int = 1,
        scale_policy: ScalingPolicy = ScalingPolicy.NONE, 
        cooldown: int = -1,
        scale_to_zero: bool = True, 
        enable_telemetry: bool = True,
        streams: List['PipelineFlow'] = None):

        # Initialize the pipeline with the given parameters.            
        self.instances = int(instances if instances > 0 else 1)                                                     # at least one instance is required
        self.max_instances = int(max(max_instances, 1) if max_instances > 0 else -1)                                # -1 means no limit (scale to zero is disabled)
        self.cooldown = int(cooldown if cooldown > 0 else -1)                                                       # -1 means no cooldown (scale to zero is disabled)
        self.scale_policy = ScalingPolicy.NONE if not isinstance(scale_policy, ScalingPolicy) else scale_policy     # default to no scaling policy if invalid policy is provided
        self.scale_to_zero = scale_to_zero and self.cooldown > 0 and self.max_instances > 0                         # scale to zero is only enabled if cooldown and max_instances are set
        self.enable_telemetry = enable_telemetry                                                                    # enable telemetry if requested

        # Initialize the pipeline flows and instances.
        self.instances: List[Pipeline] = [ ( stream for stream in streams ) for _ in range(instances) ]     # create the initial instances

        @property
        def request_metrics(self, request_id: str) -> Optional[PipelineRequestMetrics]:
            """Get the metrics for a specific request."""
            for stream in (s for streams in self.instances for s in streams):
                if metrics := stream.request_metrics(request_id): return metrics            
            return None
        
        @property
        def telemetry(self) -> Dict[str, Any]: pass

        @property
        def capabilities(self) -> Optional[ Set[PipelineCapabilities] ]: pass
        
        def start(self): pass        
        def add_request(self, request): pass
        async def process_requests(self): pass
        async def stream_response(self, request, response): pass
        async def complete_request(self, request, response): pass
        def stop(self): pass

        async def _scale_up(self): pass
        async def _scale_down(self): pass

class PipelineProvider:
    """
    An abstract base class for pipeline providers that handle API-based generation services.
    This class serves as a template for implementing specific pipeline providers,
    defining the core interface and common attributes required for API interaction
    and resource management.
    
    Attributes:
        api_url (str, optional): The base URL endpoint for the generation API service.
            Defaults to an empty string.
        api_key (str, optional): Authentication key required for API access.
            Defaults to an empty string.
        model_id (str, optional): Identifier for the specific model to be used within
            the provider's service. Defaults to an empty string.
        capabilities (Set[PipelineCapabilities], optional): A set of supported
            capabilities indicating the provider's features and limitations.
            Defaults to an empty set.
    
    Example:
        ```python
        class CustomProvider(PipelineProvider):
            async def initialize(self):
                # Setup implementation
                return True
            async def health_check(self):
                # Health check implementation
                return True
            async def cleanup(self):
                # Cleanup implementation
                pass
        ```
    Note:
        - All providers must implement the initialize(), health_check(), and cleanup() methods
        - The class is designed to be asynchronous to handle concurrent operations efficiently
        - Providers should properly manage their resources through the lifecycle methods

    Raises:
        NotImplementedError: When abstract methods are not implemented by child classes
    """
    
    api_url: Optional[str]                              = Field(description="The API URL to use for generation", default="")
    api_key: Optional[str]                              = Field(description="The API key to use for generation", default="")
    model_id: Optional[str]                             = Field(description="The model ID to use for generation", default="")
    capabilities: Optional[Set[PipelineCapabilities]]   = Field(description="The capabilities of the provider", default_factory=set)    

    @abstractmethod
    async def initialize(self) -> bool:
        """Setup provider resources"""
        raise NotImplementedError()

    @abstractmethod
    async def health_check(self) -> bool:
        """Verify provider status"""
        raise NotImplementedError()

    @abstractmethod
    async def process_request(self, request: Any) -> Any:
        """Process a request"""
        raise NotImplementedError()

    @abstractmethod
    async def cleanup(self) -> None:
        """Release resources"""
        raise NotImplementedError()    

    @abstractmethod
    def get_metrics(self) -> Union[PipelineRequestMetrics, Any]:
        """Get metrics for the provider"""
        raise NotImplementedError()

class PipelineFlow:
    """    
    A sophisticated pipeline flow controller that manages request queues, load balancing,
    and metrics tracking for distributed pipeline operations.
    This class implements a robust pipeline management system with configurable request 
    handling policies, async support, and comprehensive metrics tracking. It serves as 
    the core orchestrator for managing multiple pipeline streams and their associated 
    request flows.

    Args:
        max_requests (int, optional): Maximum number of concurrent requests the pipeline
            can handle. Defaults to 64.
        name (str, optional): Custom identifier for the pipeline flow. If not provided,
            a UUID-based name will be generated.
        policy (BalancingPolicy, optional): Load balancing strategy for request distribution.
            Defaults to BalancingPolicy.FIFO.
        provider (PipelineProvider, optional): Provider instance that handles pipeline 
            operations. Defaults to None.
        streams (List[Pipeline], optional): List of pipeline instances to be managed by 
            this flow controller. Defaults to None.
    
    Attributes:
        policy (BalancingPolicy): Active load balancing policy.
        name (str): Unique identifier for this pipeline flow.
        provider (PipelineProvider): Associated pipeline provider instance.
        streams (List[Pipeline]): Managed pipeline streams.
        queue (asyncio.Queue): Asynchronous request queue.
        semaphore (asyncio.Semaphore): Access control for concurrent operations.
        _request_metrics (Dict[str, METRIC_TYPE]): Internal storage for request metrics.
    
    Properties:
        request_metrics: Retrieves metrics for a specific request ID.
            Args:
                request_id (str): The ID of the request to fetch metrics for.
            Returns:
                Optional[PipelineRequestMetrics]: Metrics data for the specified request,
                or None if not found.
    
    Example:
        >>> flow = PipelineFlow(
        ...     max_requests=100,
        ...     name="inference-pipeline",
        ...     policy=BalancingPolicy.ROUND_ROBIN
        ... )
        >>> # Configure and use the pipeline flow
        >>> metrics = flow.request_metrics("request-123")
    
    Notes:
        - The pipeline flow implements thread-safe operations using asyncio primitives
        - Request metrics are maintained throughout the request lifecycle
        - The flow controller automatically generates a unique name if none is provided
        - Supports multiple load balancing policies for different use cases
    
    See Also:
        - Pipeline: Individual pipeline implementation
        - PipelineProvider: Provider interface
        - BalancingPolicy: Available load balancing strategies
    """

    def __init__(self, 
        max_requests: int = 64,
        name: Optional[str] = None,
        policy: BalancingPolicy = BalancingPolicy.FIFO, 
        provider: 'PipelineProvider' = None,
        streams: List['Pipeline'] = None):

        # Initialize the pipeline flow with the given parameters.        
        self.policy   = policy
        self.name     = f"pipeline-{uuid.uuid4()}" + ( "" if not name else f":{name}")
        self.provider = provider if provider else None
        self.streams: List[Pipeline] = streams

        # Initialize the request queue and semaphore.
        self.load = 0 
        self.queue = asyncio.Queue() 
        self.semaphore = asyncio.Semaphore() 

        # Initialize the request metrics.
        self._request_metrics: Dict[str, METRIC_TYPE] = []

    @property
    def request_metrics(self, request_id: str) -> Optional[PipelineRequestMetrics]:
        id = request_id.strip() if request_id else None        
        return self._request_metrics.get(id, None) if id else None