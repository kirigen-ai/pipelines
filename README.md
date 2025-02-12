# 🚀 Pipelines

<div align="center">

[![PyPI version](https://badge.fury.io/py/kirigen-pipelines.svg)](https://badge.fury.io/py/kirigen-pipelines)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Production Ready](https://img.shields.io/badge/Production-Ready-success.svg)](https://kirigen.co)
[![Downloads](https://img.shields.io/pypi/dm/kirigen-pipelines)](https://pypi.org/project/kirigen-pipelines)
[![Discord](https://img.shields.io/discord/1234567890?label=Join%20Community&color=5865F2)](https://discord.gg/kirigen)

<br/>

### ⚠️ Early Access Alpha Release
Pipelines is currently in active development. While core features are production-tested, we're rapidly adding new capabilities:
Advanced provider management
Extended metrics and monitoring
Enhanced scaling capabilities
New provider types

**[Join our developer community](https://kirigen.co/newsletter)** to:
Get notified when v1.0 launches
Access early feature previews
Shape the future of cognitive orchestration
Receive technical deep-dives

*Current Version: 0.1.0-alpha*

**The engine that makes cognitive systems reliable.**

[Quick Start](https://docs.kirigen.co/quick-start) •
[Documentation](https://docs.kirigen.co) •
[Examples](https://github.com/kirigen/pipelines/examples) •
[Discord](https://discord.gg/kirigen)

<br/>

<img src="https://kirigen.co/pipeline-demo.gif" alt="Pipelines in action" width="600px" />

</div>

## Production-Grade Orchestration

```python
from kirigen.pipelines import AudioProviderPipeline, ImageProviderPipeline, PipelineRequestMetrics
from kirigen.providers.audio import SpeechSynthesisProvider, SpeechRecognitionProvider
import kirigen.pipelines as kp

async def main():
    # Create a generic speech pipeline
    pipeline = AudioProviderPipeline(    
        instances=1,                                    # initial number of instances
        max_instances=1,                                # disable horizontal scaling
        cooldown=300,                                   # 5-min cooldown 
        scale_policy=ScalingPolicy.CONCURRENT,          # scale on concurrency 
        scale_to_zero=True,                             # allow this pipeline to reduce resources when not in use
        enable_telemetry=True,                          # collect usage data and metrics to help improve your services
        streams=[
            kp.ConcurrentFlow(
                max_requests=64,                        # Maximum number of requests stored in the processing queue
                name='synthesis',                       # The name of the provider stream
                policy=BalancingPolicy.FIFO,            # the policy used when processing requests
                provider=SpeechSynthesisProvider(),     # the provider to use
                streams=None                            # child flows used during the request processing
            ),
            kp.ConcurrentFlow(
                max_requests=64,                        # Maximum number of requests stored in the processing queue
                name='recognition',                     # The name of the provider stream
                policy=BalancingPolicy.FIFO,            # the policy used when processing requests
                provider=SpeechRecognitionProvider(),   # the provider to use
                streams=None                            # child flows used during the request processing
            ),
        ]
    )

    # add speech recognition request
    pipeline.add_request( SpeechRecognitionRequest(file="voice-actor_take_001.wav") )

    # add speech generation request
    pipeline.add_request( SpeechGenerationRequest( text="Hello, world!", voice="default" ) )

    # Monitor performance
    async for request, response in pipeline.process_requests():
        with pipeline.request_metrics(request.id) as metrics:
            if isinstance(metrics, PipelineRequestMetrics):
                print(f"Request {request.id}:")
                print(f"├─ Queue: {metrics.queue_time}ms")
                print(f"├─ Process: {metrics.provider_processing_time}ms")
                print(f"└─ Total: {metrics.total_processing_time}ms")

        # check for streaming capabilities
        if request.enable_streaming():
            if not request.is_complete(): pipeline.stream_response(response)
            else: pipeline_complete_request(response)

        # otherwise complete the request (if applicable)
        elif request.is_complete(): 
            pipline.complete_request(response)
```

## Things That Matter

### 📊 Observability
```python

class PipelineRequestMetrics(BaseModel):
    start_time: float               # Request received
    queue_time: float               # Time in queue
    provider_processing_time: float # Processing time
    total_processing_time: float    # End-to-end time
    
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
```

## Ready-to-Use Pipelines

### Speech Processing
```python
# Create a generic speech pipeline
pipeline = AudioProviderPipeline(    
    instances=1,                                    # initial number of instances
    max_instances=1,                                # disable horizontal scaling
    cooldown=300,                                   # 5-min cooldown 
    scale_policy=ScalingPolicy.CONCURRENT,          # scale on concurrency 
    scale_to_zero=True,                             # allow this pipeline to reduce resources when not in use
    enable_telemetry=True,                          # collect usage data and metrics to help improve your services
    streams=[
        kp.ConcurrentFlow(
            max_requests=64,                        # Maximum number of requests stored in the processing queue
            name='synthesis',                       # The name of the provider stream
            policy=BalancingPolicy.FIFO,            # the policy used when processing requests
            provider=SpeechSynthesisProvider(),     # the provider to use
            streams=None                            # child flows used during the request processing
        ),
        kp.ConcurrentFlow(
            max_requests=64,                        # Maximum number of requests stored in the processing queue
            name='recognition',                     # The name of the provider stream
            policy=BalancingPolicy.FIFO,            # the policy used when processing requests
            provider=SpeechRecognitionProvider(),   # the provider to use
            streams=None                            # child flows used during the request processing
        ),
    ]
)
```

## Join Our Community

<div align="center">

[![Join Discord](https://img.shields.io/badge/Join-Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/kirigen)
[![View Examples](https://img.shields.io/badge/View-Examples-FF4B4B?style=for-the-badge&logo=github&logoColor=white)](https://github.com/kirigen-ai/pipelines/examples)
[![Read Docs](https://img.shields.io/badge/Read-Docs-0076D6?style=for-the-badge&logo=readthedocs&logoColor=white)](https://kirigen.co/docs/en-us/getting-started)

</div>

## About Kirigen

At Kirigen, we're tackling one of AI's most critical challenges: making advanced cognitive systems reliable and production-ready at scale. While AI models have advanced dramatically, the infrastructure to deploy them reliably remains complex and fragmented. We're open sourcing our tech because we believe that: 

1. Shared knowledge amplifies AI's positive impact on society
2. Community-driven development creates better solutions faster
3. Transparent tools lead to more reliable systems

Our mission is to provide foundational cognitive systems that transforms experimental AI into dependable, cognitive-ai. By open sourcing pipelines, we're making orchestration accessible to everyone, from individual developers to large organizations.

<div align="center">

---

[![Star History](https://img.shields.io/github/stars/kirigen-ai/pipelines?style=social)](https://github.com/kirigen-ai/pipelines/stargazers)

Built with 💜 by [Kirigen](https://kirigen.co) and the open source community.

</div>
