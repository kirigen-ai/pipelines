# Kirigen releases 'pipelines' as an open-source library for orchestrating and managing pipelines, 
# in the hope of enableing developers to create complex workflows with ease. see https://kirigen.co/opensource-initiatives
#
# This file (as part of the 'pipelines' library) is open-source and available under the MIT license
# For more information, see the project repository at https://github.com/kirigen-ai/pipelines
#
# Copyright (c) 2025 Kirigen, all rights reserved.

from .. import PipelineProvider
from ..types import PipelineCapabilities
from .metrics import SpeechPipelineRequestMetrics
from .requests import SpeechSynthesisRequest, SpeechRecognitionRequest, SpeechSynthesisResult, SpeechRecognitionResult

class SpeechSynthesisProvider(PipelineProvider):
    """
    This abstract class defines the interface for speech synthesis services that can
    convert text to speech. It handles common functionality like API authentication
    and retry logic while requiring implementations to define core TTS operations.
    
    Attributes:
        api_key (str): Authentication key for the speech service API
        model_id (str): Identifier for the specific TTS model to use
        api_url (str): Base URL for the speech service API endpoints
        retries (int): Number of retry attempts for failed API calls (default: 3)
        retry_delay (float): Delay in seconds between retry attempts (default: 1.0)
    
    Example:
        ```python
        class MyTTSProvider(SpeechSynthesisProvider):
            async def initialize(self):
                # Setup provider-specific resources
                return True
            async def process_request(self, request):
                # Implement TTS logic
                return SpeechSynthesisResult(...)
        ```
    The provider implements the PipelineCapabilities.SYNTHETIC_SPEECH capability
    and requires concrete implementations to handle:
    - Resource initialization and cleanup
    - Health status verification
    - Text-to-speech processing
    - Performance metrics collection
    
    Note:
        Implementations should handle API rate limiting, authorization,
        and error handling appropriately for their specific service.
        The retry mechanism helps handle transient failures gracefully.
    
    Raises:
        NotImplementedError: When abstract methods are not implemented by subclass
    """

    def __init__(self, api_key: str, model_id: str, api_url: str, retries: int = 3, retry_delay: float = 1.0):
        super().__init__(api_key=api_key, model_id=model_id, api_url=api_url, capabilities=[PipelineCapabilities.SYNTHETIC_SPEECH])
        self.retries = retries              # Maximum number of retry attempts for failed pipeline initializations
        self.retry_delay = retry_delay      # Time to wait between retry attempts in seconds

    async def initialize(self) -> bool:
        """Setup provider resources"""
        raise NotImplementedError()
    
    async def health_check(self) -> bool:
        """Verify provider status"""
        raise NotImplementedError()

    async def process_request(self, request: SpeechSynthesisRequest) -> SpeechSynthesisResult:
        """Process a request"""
        raise NotImplementedError()
    
    async def cleanup(self) -> None:
        """Release resources"""
        raise NotImplementedError()
    
    def get_metrics(self) -> SpeechPipelineRequestMetrics:
        """Return provider metrics"""
        raise NotImplementedError()

class SpeechRecognitionProvider(PipelineProvider):
    """
    This abstract class defines the interface for speech recognition services that can
    transcribe audio into text. It provides a standardized way to handle speech recognition
    requests across different provider implementations.

    Args:
        api_key (str): Authentication key for the provider's API
        model_id (str): Identifier for the specific model to use
        api_url (str): Base URL for the provider's API endpoint
        retries (int, optional): Number of retry attempts for failed requests. Defaults to 3
        retry_delay (float, optional): Delay in seconds between retries. Defaults to 1.0
    
    Attributes:
        retries (int): Maximum number of retry attempts for failed requests
        retry_delay (float): Time to wait between retry attempts in seconds
    
    Methods:
        initialize(): Sets up necessary resources and connections for the provider
        health_check(): Verifies the provider service is operational
        process_request(request): Processes a speech recognition request and returns results
        cleanup(): Releases any allocated resources
        get_metrics(): Returns performance and usage metrics for the provider
    
    Example:
        ```python
        provider = CustomSpeechProvider(
            api_key="your-api-key",
            model_id="model-123",
            api_url="https://api.provider.com"
        )
        await provider.initialize()
        result = await provider.process_request(speech_request)
        await provider.cleanup()
        ```
    Notes:
        - Implements PipelineProvider base class
        - Specifically handles SPEECH_RECOGNITION capability
        - All provider implementations must override the abstract methods
        - Includes built-in retry mechanism for fault tolerance
        - Follows async/await pattern for non-blocking operations
    Raises:
        NotImplementedError: When abstract methods are not implemented by subclass
    """

    def __init__(self, api_key: str, model_id: str, api_url: str, retries: int = 3, retry_delay: float = 1.0):
        super().__init__(api_key=api_key, model_id=model_id, api_url=api_url, capabilities=[PipelineCapabilities.SPEECH_RECOGNITION])
        self.retries = retries              # Maximum number of retry attempts for failed pipeline initializations
        self.retry_delay = retry_delay      # Time to wait between retry attempts in seconds

    async def initialize(self) -> bool:
        """Setup provider resources"""
        raise NotImplementedError()
    
    async def health_check(self) -> bool:
        """Verify provider status"""
        raise NotImplementedError()

    async def process_request(self, request: SpeechRecognitionRequest) -> SpeechRecognitionResult:
        """Process a request"""
        raise NotImplementedError()
    
    async def cleanup(self) -> None:
        """Release resources"""
        raise NotImplementedError()
    
    def get_metrics(self) -> SpeechPipelineRequestMetrics:
        """Return provider metrics"""
        raise NotImplementedError()



__all__ = [ "SpeechSynthesisProvider", "SpeechRecognitionProvider" ]