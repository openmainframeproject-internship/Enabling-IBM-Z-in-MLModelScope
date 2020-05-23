**Student's Name:**  Priyanshu Khandelwal

**Mentor:**  Hong Min, Jinjun Xiong, Petr Novotny

**Project:**  Enabling IBM Z in MLModelScope

**Project Description:**  MLModelScope (https://mlmodelscope.org/) is a playground that allows people to try ML tasks with various model types, frameworks and hardware backends. It is jointly developed by IBM and University of Illinois. It is currently one of the platforms that collaborate with MLPerf for ML benchmark workload validation. (IBM participates in MLPerf as a founding members, including contribution from z). MLModelScope enables multiple backends for model training, execution and performance study. Currently IBM Z is enabled.

**Problem Definition:** Enabling zLinux as one of the backend for MLModelScope. 

**Deliverables:** Validate the support of zLinux as a backend for MLModelScope for two frameworks (TF, Pytorch/MXNet). Ensure all the DNN models are working inside the framework.

**Coding Plan:**

Our main goal is to validate the support of zLinux as a backend for MLModelScope for two frameworks (TF, PyTorch/MxNet). After it's completion, we aim to work on extending the framework to ONNX runtime and start working on a conference paper.


| Week | Tasks | Goals |
|------|-------|-------|
Week 1 (Start 24th April) | Go through the documentation for with MLModelscope and set up the development environment | Get familiar with the project
Week 2 | Try to set up the Tensorflow agent on Z | Analyze the libraries that block the installation of the Pytorch/MxNet agent on Z
Week 3-4 | Identify any libraries which are a dependency in Tensorflow agent but are not compatible with s390x architecture | Analyze the libraries that block the installation of the agent on Z.
Week 5-6 | Develop possible fixes for the identified packages and build the binary for the Tensorflow agent | Ensure the Tensorflow agent is able to build on Z
Week 7 | Try to set up the PyTorch/MxNet agent on Z, identify blockers in the installation of PyTorch/MxNet | Analyze the libraries that block the installation of the PyTorch/MxNet agent on Z
Week 8 | Work on documenting the design for the project | Complete the midterm deliverables
Week 9 | Identify and resolve any runtime errors in the Tensorflow agent | Ensure the Tensorflow agent is able to run on Z
Week 10-11 | Develop possible fixes for the packages that cause build failure in PyTorch/MxNet agent, work on resolving any runtime errors in the agent | Ensure the PyTorch/MxNet agent is able to build and run on Z
Week 12-13 | Work on extending the framework to ONNX runtime | Analyze how ONNX runtime can be supported
Week 14-16 | Support MLPerf models to run on Z across all the supporting frameworks (ONNX, TF, PyTorch, and MxNet) | Support MLPerf models to run on Z across all the supporting frameworks
Week 17-19 | Do extensive benchmarking on Z and start writing the paper | Benchmarking should be completed, the paper writing should be in progress
Week 20 (End 31st September) | Complete the documentation for the project, create the project presentation and video demonstration | Complete the internship
