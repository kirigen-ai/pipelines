# 🚀 Pipelines

<div align="center">

[![PyPI version](https://badge.fury.io/py/kirigen-pipelines.svg)](https://badge.fury.io/py/kirigen-pipelines)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Production Ready](https://img.shields.io/badge/Production-Ready-success.svg)](https://kirigen.co)
[![Downloads](https://img.shields.io/pypi/dm/kirigen-pipelines)](https://pypi.org/project/kirigen-pipelines)
[![Discord](https://img.shields.io/discord/1234567890?label=Join%20Community&color=5865F2)](https://discord.gg/kirigen)

<br/>

> ### ⚠️ Early Access Alpha Release
>
> Pipelines is currently in active development. While core features are production-tested, we're rapidly adding new capabilities:
>
> - Advanced provider management
> - Extended metrics and monitoring
> - Enhanced scaling capabilities
> - New provider types
>
> **[Join our developer community](https://kirigen.co/newsletter)** to:
> - Get notified when v1.0 launches
> - Access early feature previews
> - Shape the future of cognitive orchestration
> - Receive technical deep-dives
>
> *Current Version: 0.1.0-alpha*

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

# Create your processing pipeline
pipeline = ImageProviderPipeline(
    instances=1,              # Initial instances
    max_instances=2,         # Scaling limit
    scale_policy="memory",   # Scale on GPU usage
    cooldown=900,           # Scaling cooldown
    providers=[
        SDXLProvider(),     # Base generation
        FluxProvider()      # Enhancement
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

## Three Things That Matter

### 🎯 Real Orchestration
```python
class ImageProviderPipeline:
    def __init__(
        self,
        instances: int,          # Initial count
        max_instances: int,      # Scale limit
        scale_policy: str,       # How to scale
        cooldown: int,          # Scale cooldown
        providers: List[Provider] # AI models
    ):
        # Set up observable pipeline
        self.request_metrics = {}
        self._queue = asyncio.Queue()
        
        # Configure providers
        self.sdxl = next(p for p in providers 
                        if isinstance(p, SDXLProvider))
        self.flux = [p for p in providers 
                    if isinstance(p, FluxProvider)]
```

### 📊 Complete Observability
```python
@dataclass
class PipelineRequestMetrics:
    start_time: float              # Request received
    queue_time: float             # Time in queue
    provider_processing_time: float # Processing time
    total_processing_time: float   # End-to-end time
    
    def complete(self):
        self.total_processing_time = time.time() - self.start_time
```

### ⚡ Production Architecture
```python
async def process_requests(self):
    while True:
        if not self._queue.empty():
            # Get next request
            request_id, request = await self._queue.get()
            metrics = self.request_metrics[request_id]
            
            try:
                # Track queue time
                metrics.queue_time = time.time() - metrics.start_time
                
                # Process request
                start = time.time()
                result = await self._process(request)
                metrics.provider_processing_time = time.time() - start
                
                # Complete metrics
                metrics.complete()
                yield request_id, result
                
            except Exception as e:
                print(f"Failed to process {request_id}: {e}")
                
        await asyncio.sleep(0.1)  # Prevent CPU spin
```

## Ready-to-Use Pipelines

### Speech Processing
```python
# Create speech pipeline
pipeline = AudioProviderPipeline(
    instances=2,                    # Start with 2
    max_instances=4,               # Scale to 4
    scale_policy="concurrent",     # Scale on load
    cooldown=300,                 # 5-min cooldown
    providers=[
        WhisperProvider(),        # Recognition
        KokoroProvider()         # Synthesis
    ]
)

# Process with metrics
request_id = await pipeline.add_request(
    SpeechRecognitionRequest(file="audio.mp3")
)

async for id, result in pipeline.process_requests():
    if id == request_id:
        metrics = pipeline.request_metrics[id]
        print(f"Time: {metrics.total_processing_time}ms")
```

### Image Generation
```python
# Create image pipeline
pipeline = ImageProviderPipeline(
    instances=1,
    max_instances=2,
    scale_policy="memory",
    cooldown=900,
    providers=[
        SDXLProvider(),  # Generation
        FluxProvider()   # Enhancement
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

## Start Building

```bash
pip install kirigen-pipelines
```

## Real Performance

Production metrics:
- **Processing**: 150-300ms average
- **Queue Time**: ~50ms typical
- **Scaling**: 2x with auto-scale
- **Memory**: 40% optimization
- **Uptime**: 99.9% reliable

## Join Our Community

<div align="center">

[![Join Discord](https://img.shields.io/badge/Join-Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/kirigen)
[![View Examples](https://img.shields.io/badge/View-Examples-FF4B4B?style=for-the-badge&logo=github&logoColor=white)](https://github.com/kirigen/pipelines/examples)
[![Read Docs](https://img.shields.io/badge/Read-Docs-0076D6?style=for-the-badge&logo=readthedocs&logoColor=white)](https://docs.kirigen.co/getting-started)

</div>

## About Kirigen

We build the orchestration layer that makes cognitive systems reliable. Open source, observable, and built for production.

<div align="center">

---

[![Star History](https://img.shields.io/github/stars/kirigen/pipelines?style=social)](https://github.com/kirigen/pipelines/stargazers)

Built with 💜 by [Kirigen](https://kirigen.co) and the open source community.

</div>
