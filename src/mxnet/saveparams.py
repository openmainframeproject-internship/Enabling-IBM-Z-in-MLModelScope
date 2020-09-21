import mxnet as mx
from mxnet.gluon.model_zoo import vision

resnet = vision.resnet50_v2(pretrained=True, ctx=ctx)
resnet.save_parameters('resnetparams')

