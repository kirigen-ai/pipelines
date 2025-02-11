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
from kirigen.pipelines import AudioProviderPipeline, ImageProviderPipeline
from kirigen.providers.imagination import SDXLProvider, FluxProvider
import kirigen.pipelines as kp

# Create your processing pipeline
pipeline = ImageProviderPipeline(
    instances=1,                    # start with 1
    scale_policy="never",           # never scale
    scale_to_zero=False,            # keep this pipeline always active
    providers=[
        kp.ConcurrentQueue(
            queue=4,
            provider=SDXLProvider(),                                             # Generation
            streams=[ kp.LoadBalancingQueue(2, 'round-robin', FluxProvider()) ]  # Enhancement (using load balancing)
        ),
    ]
)

# Process with full observability
async for request_id, result in pipeline.process_requests():
    metrics = pipeline.request_metrics[request_id]
    print(f"Request {request_id}:")
    print(f"├─ Queue: {metrics.queue_time}ms")
    print(f"├─ Process: {metrics.provider_processing_time}ms")
    print(f"└─ Total: {metrics.total_processing_time}ms")
```

## Things That Matter

### 📊 Complete Observability
```python
@dataclass
class PipelineRequestMetrics:
    start_time: float               # Request received
    queue_time: float               # Time in queue
    provider_processing_time: float # Processing time
    total_processing_time: float    # End-to-end time
    
    def complete(self):
        self.total_processing_time = time.time() - self.start_time

@dataclass
class ImagePipelineRequestMetrics(PipelineRequestMetrics):
    num_steps: int              # number of steps in the pipeline
    image_format: str           # format of the image
    image_size: tuple           # size of the image
    image_orientation: str      # orientation of the image
    image_aspect_ratio: float   # aspect ratio of the image
    provider_name: str          # name of the provider
    metadata: dict[str, str]    # image metadata
```

## Ready-to-Use Pipelines

### Speech Processing
```python
# Create speech pipeline
pipeline = AudioProviderPipeline(
    instances=2,                    # start with 2
    max_instances=12,               # scale to 12
    cooldown=300,                   # 5-min cooldown
    device="cuda:0",                # specify the device to load this pipeline on
    scale_policy="concurrent",      # scale on concurrency
    scale_to_zero=True,             # enable to_zero scaling, completely disabling this pipeline during low used
    enable_realtime=True,           # enable real-time streaming of audio in- and out    
    enable_telemetry=True,          # collect usage data and metrics to help improve your services
    providers=[
        kp.ConcurrentQueue(queue=4, provider=KokoroProvider(), streams=None),  # Synthesis
        kp.ConcurrentQueue(queue=4, provider=WhisperProvider(), streams=None), # Recognition
    ]
)

# speech recognition request
request_id = await pipeline.add_request(
    SpeechRecognitionRequest(file="voice-actor_take_001.wav")
)

# Monitor performance
async for id, result in pipeline.process_requests():
    if id == request_id:        
        metrics = pipeline.request_metrics[id]
        print(f"Time: {metrics.total_processing_time}ms")        

# speech generation request
request_id await pipeline.add_request(
    SpeechGenerationRequest(text="Hello, world!")
)

# Monitor performance
async for id, result in pipeline.process_requests():
    if id == request_id:        
        metrics = pipeline.request_metrics[id]
        print(f"Time: {metrics.total_processing_time}ms")
```

### Image Generation
```python
# Create image pipeline
pipeline = ImageProviderPipeline(
    instances=1,                    # start with 1
    max_instances=1,                # never scale
    cooldown=900,                   # 15-min cooldown
    device="cuda:0",                # specify the device to load this pipeline on
    scale_policy="never",           # never scale
    scale_to_zero=False,            # disable to_zero scaling, leaving this pipeline always active
    enable_realtime=False,          # disable real-time streaming
    enable_telemetry=True,          # collect usage data and metrics to help improve your services
    providers=[
        kp.ConcurrentQueue(
            queue=64, 
            provider=SDXLProvider(),                                               # Generation
            streams=[ kp.LoadBalancingQueue(2, 'round-robin', FluxProvider()) ]    # Enhancement (using load balancing)
        ),        
    ]
)

# Add request with tracking
request_id = await pipeline.add_request(
    ImageGenerationRequest(prompt="landscape")
)

# Monitor performance
async for id, result in pipeline.process_requests():
    if id == request_id:
        metrics = pipeline.request_metrics[id]
        print(f"Queue: {metrics.queue_time}ms")
        print(f"Process: {metrics.provider_processing_time}ms")
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

Our mission is to provide the foundational infrastructure that transforms experimental AI into dependable, cognitive-ai. By open sourcing Kirigen, we're making orchestration accessible to everyone, from individual developers to large organizations.

<div align="center">

---

[![Star History](https://img.shields.io/github/stars/kirigen-ai/pipelines?style=social)](https://github.com/kirigen-ai/pipelines/stargazers)

Built with 💜 by [Kirigen](https://kirigen.co) and the open source community.

</div>
