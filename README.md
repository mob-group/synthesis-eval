# synthesis-eval
Collection of synthesis tools and results, benchmarked against each other.

## Build Environment

Environment variables that should be exported in `env.sh` (not checked in):
* `IDL_ROOT`: the install directory for IDL. Should have `lib/cmake/llvm` in it.
* `SY_CC`, `SY_CXX`: the C and C++ compilers that were used to build IDL above
  (or are at least compatible).

## Notes

* It's hard to express everything completely the same between every
  implementation - e.g. some things like linear interpolation between vectors
  you just can't express at all without floats.
