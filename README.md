# 🚀 Pipelines
<div align="center"><br/>

### ⚠️ Early Access Alpha Release
Pipelines is currently in active development. While the core features are currently being production-tested, the change from a closed source to an open source project is still in progress. We are actively working on refactoring our platform using the new open source codebase. We are also working on improving the documentation and examples to help you get started quickly.
*Current Version: 0.1.0-alpha*

[![PyPI version](https://badge.fury.io/py/kirigen-pipelines.svg)](https://badge.fury.io/py/kirigen-pipelines) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Production Ready](https://img.shields.io/badge/Soon-blue?style=flat&label=Production
)](https://kirigen.co) [![Downloads](https://img.shields.io/pypi/dm/kirigen-pipelines)](https://pypi.org/project/kirigen-pipelines)
[![Discord](https://img.shields.io/badge/Coming_Soon-orange?style=flat&label=Community
)](https://discord.gg/kirigen)

[Quick Start](https://docs.kirigen.co/pipelines/quick-start) • [Documentation](https://docs.kirigen.co/pipelines/getting-started) • [Examples](https://github.com/kirigen/pipelines/examples) • [Newsletter](https://kirigen.co/latest-news)
<br/></div>

## Production-Grade Orchestration

```python
from kirigen import pipelines as kp
from kirigen.pipelines.audio import (
    SpeechSynthesisProvider, SpeechSynthesisRequest, SpeechSynthesisResult,
    SpeechRecognitionProvider, SpeechRecognitionRequest, SpeechRecognitionResult
)
from kirigen.pipelines.types import ScalingPolicy, BalancingPolicy
from kirigen.pipelines.metrics import PipelineRequestMetrics

async def main():
    # Create a generic speech pipeline
    pipeline = kp.Pipeline( 
        instances=1,                                    # initial number of instances
        max_instances=1,                                # disable horizontal scaling
        cooldown=300,                                   # 5-min cooldown
        scale_to_zero=True,                             # allow this pipeline to reduce resources when not in use
        enable_telemetry=True,                          # collect usage data and metrics to help improve your services
        scale_policy=ScalingPolicy.NONE,                # disable scaling
        streams=[
            kp.ConcurrentFlow(
                concurrency=4,                          # Maximum number of concurrent requests processed by the provider
                max_requests=64,                        # Maximum number of requests stored in the processing queue
                name='synthesis',                       # The name of the provider stream
                policy=BalancingPolicy.FIFO,            # the policy used when processing requests
                provider=SpeechSynthesisProvider(),     # the provider to use
                streams=None                            # child flows used during the request processing
            ),
            kp.SequentialFlow(
                max_requests=64,                        # Maximum number of requests stored in the processing queue
                name='recognition',                     # The name of the provider stream
                policy=BalancingPolicy.PRIORITY,        # the policy used when processing requests
                provider=SpeechRecognitionProvider(),   # the provider to use
                streams=None                            # child flows used during the request processing
            ), 
        ] 
    )  

    # add speech generation request
    synth_request = pipeline.add_request( SpeechSynthesisRequest( text="Hello, world!", target="default" ) )
    synth_result: SpeechSynthesisResult = None

    # add speech recognition request
    rec_request = pipeline.add_request( SpeechRecognitionRequest( uri="file://./voice-actor_take_001.wav", timecodes=True ) )
    rec_result: SpeechRecognitionResult = None

    # process requests in the pipeline
    while not(synth_request.is_complete() and rec_request.is_complete()):        
        async for request, response in await pipeline.process_requests():

            # check for telemetry capabilities and print metrics if available
            with pipeline.request_metrics(request.id) as metrics:
                if isinstance(metrics, PipelineRequestMetrics):
                    print(f"Request {request.id}:")
                    print(f"├─ Queue: {metrics.queue_time}ms")
                    print(f"├─ Process: {metrics.provider_processing_time}ms")
                    print(f"└─ Total: {metrics.total_processing_time}ms")

            # check for streaming capabilities
            if request.enable_streaming():
                if not request.is_complete(): pipeline.stream_response(request, response)
                else: pipeline.complete_request(response)

            # otherwise complete the request (if applicable)
            elif request.is_complete(): pipeline.complete_request(request, response)
```

## About Kirigen

At Kirigen, we're tackling some of AI's most critical challenges: making advanced cognitive systems reliable and production-ready at scale. 

While AI models have advanced dramatically, the infrastructure to deploy them reliably remains complex and fragmented. We're open sourcing our tech because we believe that: 

1. Shared knowledge amplifies AI's positive impact on society
2. Community-driven development creates better solutions faster
3. Transparent tools lead to more reliable systems

Our mission is to provide foundational cognitive systems that transforms experimental AI into dependable, cognitive-ai. By open sourcing pipelines, we're making orchestration accessible to everyone, from individual developers to large organizations.

<div align="center">

## Join Our Community

<div align="center">

[![Join Discord](https://img.shields.io/badge/Join-Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/kirigen)
[![View Examples](https://img.shields.io/badge/View-Examples-FF4B4B?style=for-the-badge&logo=github&logoColor=white)](https://github.com/kirigen-ai/pipelines/examples)
[![Read Docs](https://img.shields.io/badge/Read-Docs-0076D6?style=for-the-badge&logo=readthedocs&logoColor=white)](https://docs.kirigen.co/pipelines/getting-started)

</div>

---

[![Star History](https://img.shields.io/github/stars/kirigen-ai/pipelines?style=social)](https://github.com/kirigen-ai/pipelines/stargazers)

Built with 💜 by [Kirigen](https://kirigen.co) and the open source community.

</div>
