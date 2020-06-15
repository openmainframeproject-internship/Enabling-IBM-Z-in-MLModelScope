# Installation guide for MXNet Agent

Use this guide to install MXNet agent on zLinux (s390x architecture). Tested on `Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-96-generic s390x)`

## Installing dependencies

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

2. These packages are installed in `/usr/lib/s390x-linux-gnu` directory by default but MXNet is not configured for s390x and requires the archive libraries and shared object files to be present in `/usr/lib`. So, we need to create symbolic link for these files -

    ```
    ln -s /usr/lib/s390x-linux-gnu/libjemalloc.a /usr/lib/libjemalloc.a 
    ln -s  /usr/lib/s390x-linux-gnu/libjemalloc.so /usr/lib/libjemalloc.so
    ln -s  /usr/lib/s390x-linux-gnu/liblapack.a /usr/lib/liblapack.a
    ln -s  /usr/lib/s390x-linux-gnu/liblapack.so /usr/lib/liblapack.so
    ln -s  /usr/lib/s390x-linux-gnu/libopenblas.a /usr/lib/libopenblas.a
    ln -s  /usr/lib/s390x-linux-gnu/libopenblas.so /usr/lib/libopenblas.so
    ```


### Installing other dependencies

1. Install the dependencies using the following command

    ```
    apt-get install g++ godep make
    ```


## Installing MXNet C++ library

1. Clone MXNet github repository

    ```
    git clone --single-branch --depth 1 --branch $FRAMEWORK_VERSION --recursive https://github.com/apache/incubator-mxnet mxnet
    ```

2. We'll be using `make` to compile the library. This requires setting the multiple configuration options avaliable under make/config.mk. Use the following command to install the library

    ```
    cd mxnet && \
    mkdir -p /opt/mxnet &&  \
    cp make/config.mk . && \
    echo "USE_BLAS=openblas" >>config.mk && \
    echo "USE_CPP_PACKAGE=0" >>config.mk && \
    echo "USE_OPENCV=0" >>config.mk && \
    echo "USE_PROFILER=1" >>config.mk && \
    echo "USE_PYTHON=1" >>config.mk && \
    echo "USE_CUDA=0" >>config.mk && \
    echo "USE_SSE=0" >>config.mk && \
    echo "ADD_CFLAGS=-I/usr/include/openblas -Wno-strict-aliasing -Wno-sign-compare -ftrack-macro-expansion=0 -Wno-misleading-indentation" >>config.mk && \
    make PREFIX=/opt/mxnet &&  \
    cp -r include /opt/mxnet/ && \
    cp -r lib /opt/mxnet/ && \
    rm -r build
    ```

3. Create symbolic link for MXNet C++ binary.

    ```
    ln -s /opt/mxnet/lib/libmxnet.so /usr/lib/libmxnet.so
    ```

4. Export the `LD_LIBRARY_PATH` and `LIBRARY_PATH` environment variables for MXNet library

    ```
    export LD_LIBRARY_PATH=/opt/mxnet/lib:$LD_LIBRARY_PATH
    export LIBRARY_PATH=/opt/mxnet/lib:$LIBRARY_PATH
    ```


## Configuring rai-project/go-mxnet

1. There is a header file missing in `mxnet/error.go`, `mxnet/predictor.go`, `mxnet/ndarray.go` that causes multiple build failures. To avoid them, add the following header in these files

    ```
    #include <mxnet/c_api.h>
    ```

2. Update the following vendors in Gopkg.lock

    ```
    [[projects]]
    name = "github.com/chewxy/math32"
    packages = ["."]
    revision = "9dce16d45cb597191760b8e08fad92d39615a4d0"
    version = "1.01"

    [[projects]]
    branch = "master"
    name = "github.com/ianlancetaylor/cgosymbolizer"
    packages = ["."]
    revision = "be1b05b0b2790e3d9d080d29bd918304bbd35a2b"

    [[projects]]
    name = "gorgonia.org/tensor"
    packages = [".","internal/execution","internal/serialization/fb","internal/serialization/pb","internal/storage"]
    revision = "6848ca2e9a6c44d93bec0814b30ded143c75ca94"
    version = "v0.95"

    [[projects]]
    name = "gorgonia.org/vecf32"
    packages = ["."]
    revision = "50ea049a9000a9d51e09929ee39572ff2ba68b59"
    version = "v0.9.0"

    [[projects]]
    name = "gorgonia.org/vecf64"
    packages = ["."]
    revision = "1a1e7411aed011ba757953c004380fa32cce0293"
    version = "v0.9.0"
    ```

4. Install the project dependencies using 

    ```
    dep ensure -vendor-only -v
    ```

5. Test the build with the following command

    ```
    go build -tags=nogpu -a -installsuffix cgo
    ```


## Installing MXNet agent

1. Use the files `go-mxnet/mxnet/error.go`, `go-mxnet/mxnet/predictor.go`, `go-mxnet/mxnet/ndarray.go` that we fixed earlier while building go-mxnet and update them in vendor/github.com/rai-project/go-mxnet/mxnet/ directory.

2. Update the following vendors in Gopkg.lock

    ```
    [[projects]]
    name = "github.com/chewxy/math32"
    packages = ["."]
    revision = "9dce16d45cb597191760b8e08fad92d39615a4d0"
    version = "1.01"

    [[projects]]
    branch = "master"
    name = "github.com/ianlancetaylor/cgosymbolizer"
    packages = ["."]
    revision = "be1b05b0b2790e3d9d080d29bd918304bbd35a2b"

    [[projects]]
    name = "gorgonia.org/tensor"
    packages = [".","internal/execution","internal/serialization/fb","internal/serialization/pb","internal/storage"]
    revision = "6848ca2e9a6c44d93bec0814b30ded143c75ca94"
    version = "v0.95"

    [[projects]]
    name = "gorgonia.org/vecf32"
    packages = ["."]
    revision = "50ea049a9000a9d51e09929ee39572ff2ba68b59"
    version = "v0.9.0"

    [[projects]]
    name = "gorgonia.org/vecf64"
    packages = ["."]
    revision = "1a1e7411aed011ba757953c004380fa32cce0293"
    version = "v0.9.0"
    ```

3. Install the project dependencies using 

    ```
    dep ensure -vendor-only -v
    ```

4. Build and install the agent using the following commands

    ```
    go build -tags=nogpu -a -installsuffix cgo
    go install -tags=nogpu
    ```
