## Architecture and Design of the project

The architecture of MLModelScope is shown below - ![](https://github.com/openmainframeproject-internship/Enabling-IBM-Z-in-MLModelScope/blob/master/Documentation/mlmodelscope-arch.png)


The architecture is comprised of the following components -

1. Client — is either the web UI or command-line interface which users use to supply their inputs and initiate the model evaluation by sending a REST request to the CarML server.

2. Server — acts on the client requests and performs REST API handling, dispatching the model evaluation tasks to CarML agents, generating benchmark workloads based on benchmarking scenarios, and analyzing the evaluation results.

3. Agents — runs on different systems of interest and perform a model evaluation based on requests sent by the CarML server. An agent can be run within a container or as a local process and has the logic for downloading model assets, performing input pre-processing, using the framework predictor for inference, and performing post-processing. Aside from the framework predictor, all code in an agent is common across frameworks.

4. Framework Predictor — is a wrapper around a framework and provides a consistent interface across different DL frameworks. The wrapper is designed as a thin abstraction layer so that all DL frameworks can be easily integrated into CarML by exposing a limited number of common APIs.

5. Middleware — are a set of support services for CarML including a distributed registry (a key-value store containing entries of running agents and available models), an evaluation database (a database containing evaluation results), a tracing server (a server to publish profile events captured during an evaluation), and an artifact storage server (a data store repository containing model assets and datasets).


## Building and running different agents on zLinux

1. Building Tensorflow Agent on zLinux [Docs](https://github.com/openmainframeproject-internship/Enabling-IBM-Z-in-MLModelScope/blob/master/Documentation/docs-tensorflow-agent.md)

2. Building MXNet Agent on zLinux [Docs](https://github.com/openmainframeproject-internship/Enabling-IBM-Z-in-MLModelScope/blob/master/Documentation/docs-mxnet-agent.md)

3. Ensure all the DNN models are working inside framework [In Progress]


## Integrating ONNX Runtime with MLModelScope

### About ONNX Runtime

ONNX Runtime is a single inference engine that’s highly performant for multiple platforms and hardware. Using it is simple:

1. Train a model with any popular framework such as TensorFlow and PyTorch
2. Export or convert the model to ONNX format
3. Inference efficiently across multiple platforms and hardware (Windows, Linux, and Mac on both CPUs and GPUs) with ONNX Runtime


### How to create ONNX Agent?

To create ONNX Agent, we need to implement the framework wrapper and expose the framework as an MLModelScope predictor. The predictor interface is composed of three functions - 

1. Model Load - Opens the model
2. Model Unload - Close the model
3. Predict - Performs the inference for image classification, image object detection, and image predictor. 

The auxiliary code that forms an agent is common across frameworks and does not need to be modified.

### How to create Go bindings for ONNX Runtime?

In order to avoid any language-based latency, we plan to build Go bindings for ONNX Runtime C API. This would involve creating the following modules -

1. Predictor - Perform inferencing with ONNX Runtime. 
2. Profiler - Access the runtime profile data.
3. Utils - Utility functions to process arrays, tensors, allocate memory, etc.

To perform inferencing via the ONNX Runtime C API, do as follows - 

1. Call OrtCreateEnv
2. Create ONNX Session: OrtCreateSession(env, model_uri, nullptr,...)
3. Optionally add more execution providers (e.g. for CUDA use OrtSessionOptionsAppendExecutionProvider_CUDA)
4. Create ONNX Tensor 
    4.1 OrtCreateMemoryInfo
    4.2 OrtCreateTensorWithDataAsOrtValue
5. OrtRun

The ONNX Runtime C API is available [here](https://github.com/microsoft/onnxruntime/blob/master/include/onnxruntime/core/session/onnxruntime_c_api.h)

