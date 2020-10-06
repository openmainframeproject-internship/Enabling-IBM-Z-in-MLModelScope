# Installation guide for Tensorflow Agent

Use this guide to install Tensorflow agent on zLinux (s390x architecture). Tested on `Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-96-generic s390x)` [docker image](https://hub.docker.com/r/s390x/ubuntu/).

## Installing dependencies

### Installing other dependencies

1. Install the dependencies using the following command and create a soft link for python.

    ```
    apt-get update && \
    apt-get install -y wget zip unzip python3 git openjdk-11-jdk g++ libjpeg-dev libprotoc-dev go-dep make && \
    ln -sf /usr/bin/python3 /usr/bin/python
    ```

### Installing Go

1. Download the Go binary and install it on the system. Please note that we'll be using Go version 1.13.10 as it is verified to support mxnet agent on zLinux.`

    ```
    wget https://dl.google.com/go/go1.13.10.linux-s390x.tar.gz
    tar -C /usr/local -xzf go1.13.10.linux-s390x.tar.gz
    ```

2. Set the env variable GOPATH to point to your local directory of go projects. Also, add /usr/local/go/bin to the PATH environment variable. You can do this by adding the following lines to your /etc/profile (for a system-wide installation) or $HOME/.profile:

    ```
    export GOPATH=~/gopros
    export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin
    ```

### Installing Openblas, jemalloc and LAPACK

1. These packages are available in ubuntu repositories and can be installed with the following command.

    ```
    apt-get update
    apt-get install libopenblas-dev liblapack-dev libjemalloc-dev
    ```

2. These packages are installed in `/usr/lib/s390x-linux-gnu` directory by default but Tensorflow is not configured for s390x and so it requires the archive libraries and shared object files to be present in `/usr/lib`. Therefore, we need to create symbolic link for these files -

    ```
    ln -s /usr/lib/s390x-linux-gnu/libjemalloc.a /usr/lib/libjemalloc.a 
    ln -s  /usr/lib/s390x-linux-gnu/libjemalloc.so /usr/lib/libjemalloc.so
    ln -s  /usr/lib/s390x-linux-gnu/liblapack.a /usr/lib/liblapack.a
    ln -s  /usr/lib/s390x-linux-gnu/liblapack.so /usr/lib/liblapack.so
    ln -s  /usr/lib/s390x-linux-gnu/libopenblas.a /usr/lib/libopenblas.a
    ln -s  /usr/lib/s390x-linux-gnu/libopenblas.so /usr/lib/libopenblas.so
    ```

## Installing Tensorflow C library

The process to install and configure Tensorflow for s390x is documented by IBM [here](https://github.com/linux-on-ibm-z/docs/wiki/Building-TensorFlow). Taking reference from these [scripts](https://github.com/linux-on-ibm-z/scripts/tree/master/Tensorflow), we have tested the following instructions to install Tensorflow 1.15.3 successfully on Z.

1. A directory ``/<source_root>`` will be referred to in this section, it is a temporary writable directory anywhere you'd like to place it.

    ```
	export SOURCE_ROOT=/<source_root>
	cd $SOURCE_ROOT
    ```

2. Install bazel-0.26.1 

    ```
	mkdir bazel && cd bazel  
	wget https://github.com/bazelbuild/bazel/releases/download/0.26.1/bazel-0.26.1-dist.zip 
	unzip bazel-0.26.1-dist.zip  
	chmod -R +w .
	
	#Adding fixes and patches to the files
	sed -i "130s/-classpath/-J-Xms1g -J-Xmx1g -classpath/" scripts/bootstrap/compile.sh
	
	env EXTRA_BAZEL_ARGS="--host_javabase=@local_jdk//:jdk" bash ./compile.sh
	export PATH=$PATH:$SOURCE_ROOT/bazel/output/ 
    ```

3. Clone Tensorflow github repository and checkout branch 1.15.3

    ```
    cd $SOURCE_ROOT
    mkdir tensorflow && cd tensorflow

    git clone --single-branch --depth 1 --branch v1.15.3 --recursive https://github.com/tensorflow/tensorflow tensorflow && \
    cd tensorflow
    ```

4. Set required complation flags and install libtensorflow (Tensorflow C library) - 

    ```
	export PYTHON_BIN_PATH=/usr/bin/python3.6
  	export PYTHON_LIB_PATH=/usr/lib/python3.6/dist-packages
	export TF_NEED_GCP=0 
	export TF_NEED_HDFS=0 
	export TF_NEED_CUDA=0 
	export TF_NEED_MKL=0 
	export TF_NEED_OPENCL=0 
	export TF_NEED_VERBS=0 
	export TF_NEED_S3=0 
	export TF_NEED_KAFKA=0 
	export TF_NEED_AWS=0 
	export TF_ENABLE_XLA=0

	yes "" | ./configure || true
    
	bazel build --define=tensorflow_mkldnn_contraction_kernel=0 -c opt //tensorflow:libtensorflow.so
    ```

5. Create symlinks for Tensoflow binaries and shared object files

    ```
	ls -la bazel-bin/tensorflow
	cp bazel-bin/tensorflow/libtensorflow.so.1.15.3 /usr/local/lib/libtensorflow.so
	ln -s /usr/local/lib/libtensorflow.so /usr/local/lib/libtensorflow.so.1
	cp bazel-bin/tensorflow/libtensorflow_framework.so.1.15.3 /usr/local/lib/libtensorflow_framework.so.1
	mkdir /usr/local/include/tensorflow 
	cp -r bazel-tensorflow/tensorflow/c /usr/local/include/tensorflow

	export CGO_CFLAGS="${CGO_CFLAGS} -I /usr/local/include"
	export CGO_CXXFLAGS="${CGO_CXXFLAGS} -I /usr/local/include"
	export CGO_LDFLAGS="${CGO_LDFLAGS} -L /usr/local/lib"

	ldconfig
    ```

## Installing Tensorflow agent

MlModelScope uses chewxy/math32 package as a dependency but it fails to work on Z. So, we pushed a fix to make it work on s390x architecture. The details about this change is available here [here](https://github.com/openmainframeproject-internship/Enabling-IBM-Z-in-MLModelScope/tree/master/src/math32).

1. Get the latest Tensorflow Agent package

   ```
   export PKG=github.com/rai-project/tensorflow
   export WORKDIR=$GOPATH/src/$PKG
   mkdir -p $WORKDIR && cd $WORKDIR
   git clone https://$PKG.git .
   ```

2. Using the upstream vendors causes build failures. So, we tested different versions for these vendors to find the compatible ones and came up with the following configuration to be added into Gopkg.toml.

    ```
    [[constraint]]
      name = "github.com/tensorflow/tensorflow"
      version = "=1.15.3"
    
    [[override]]
      name = "github.com/chewxy/math32"
      version = "=1.0.6"

    [[override]]
      name = "github.com/ianlancetaylor/cgosymbolizer"
      revision = "be1b05b0b2790e3d9d080d29bd918304bbd35a2b"

    [[constraint]]
      name = "gorgonia.org/tensor"
      version = "=0.95"
    ```

3. Install the project dependencies using 

    ```
    dep ensure -v
    ```

4. Build and install the agent using the following commands

    ```
    export GO111MODULE=off
    cd tensorflow-agent
    go install -tags=nogpu
    ```

