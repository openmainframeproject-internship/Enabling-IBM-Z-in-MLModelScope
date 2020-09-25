## Math32
The package [chewxy/math32](https://github.com/chewxy/math32) is a float32 version of Go's math package. It is a dependency for MlModelScope. 

## Fix for s390x architecture
To make the package work on IBM Z (s390x architecture) I proposed a [fix](https://github.com/chewxy/math32/commits/master/stubs_s390x.s) to chewxy/math32 package (which is now merged in the master branch). The fix involved creating [stub_s390x.s](https://github.com/openmainframeproject-internship/Enabling-IBM-Z-in-MLModelScope/blob/master/src/math32/stub_s390x.s) stub file containing the definition of some math operations for s390x arch in assembly language. 
