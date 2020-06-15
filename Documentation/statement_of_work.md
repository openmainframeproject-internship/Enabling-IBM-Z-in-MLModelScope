## Project Description - 

MLModelScope (https://mlmodelscope.org/) is a playground that allows people to try ML tasks with various model types, frameworks, and hardware backends. It is jointly developed by IBM and the University of Illinois. It is currently one of the platforms that collaborate with MLPerf for ML benchmark workload validation. (IBM participates in MLPerf as a founding member, including the contribution from Z). MLModelScope enables multiple backends for model training, execution, and performance study. Currently, IBM Z is enabled. Our main goal is to validate the support of zLinux as a backend for MLModelScope.


## State of the project - 

MLModelScope currently -

1. Has support for TensorFlow, TFLite, PyTorch, Caffe2, MXNet, Caffe, CNTK, and TensorRT ( + "same-stack" docker images)
2. Runs on ARM, PowerPC, and X86 with CPU, GPU, and FPGA
3. Runs on macOS, Linux, and Windows
4. Common ML models and datasets (around 300 models and 10 datasets)
5. Integration with MLPerf evaluation methodology
6. Built-in framework, library, and hardware profilers


## Value of MLModelScope - 

1. A playground for people to evaluate and compare ML models.
2. A model hub for model authors to easily share/deploy their trained models.
3. A benchmarking tool to consistently collect runtime traces of ML models.
4. A profiling tool to gain a deep understanding of models’ performance.


## Project Requirements 

We have divided the project requirements into primary and secondary requirements.

The primary requirements are as follows -

1. Build and install the Tensorflow agent and MXNet agent on zLinux. 
2. Ensure all the DNN models are working inside the framework.

After the primary requirements are satisfied, we plan to work on the secondary requirements, which are as follows -

1. Extending the framework to ONNX runtime. This involves creating an ONNX agent and Go bindings to ONNX Runtime C++ API.
3. Support MLPerf models to run on IBM Z across the multiple frameworks (ONNX, TF, and MxNet) 
4. Do extensive benchmarking on IBM Z
