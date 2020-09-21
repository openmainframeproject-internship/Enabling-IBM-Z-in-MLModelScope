# MXNet

This folder contains the fix that we created in MXNet to make it run on IBM Z.

## Problem
It was not possible to use models that were pretrained on x86 machine or any other little-endian machine for inference on IBM Z. The gluon model files were just a memory dump which made their endianness same as the endianness of the machine on which they were dumped out. So, due to being trained on X86 machine (having little-endian architecture), the gluon models crashed when they were loaded on IBM Z (big-endian architecture). 

// TODO - Add code snippets for detailed description

## Fix
We created a fix to make the serialization format of MXNet Gluon model endian independent. This means that the models can be trained on machine having any endianness (big or little) and can be loaded on machine having any endianness (big or little). We did this by using the numpy serialization format .npz for Gluon model serialization.

# Files
| Folder | Description |
|---|---|
| MXNet_Fix.ipynb | Python notebook to install MXNet package from source and applying our patch to it |
| bigendian.patch | Patch file for making MXNet serialization ednian independent |
| docs-mxnet-agent.md | Documentation to install MXNet package, MlModelScope MXNet agent on Z |