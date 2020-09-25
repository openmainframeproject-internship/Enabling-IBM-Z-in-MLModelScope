## Math32
The package [chewxy/math32](https://github.com/chewxy/math32) is a float32 version of Go's math package. It is a dependency for MlModelScope. 

## Fix for s390x architecture
To make the package work on IBM Z (s390x architecture) I proposed a fix which is now merged in the project. The fix involved creating [this](https://github.com/chewxy/math32/blob/master/stubs_s390x.s) stub containing the definition of some math operations for s390x arch in assembly language.
