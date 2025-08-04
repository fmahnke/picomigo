#ifndef types__types_h_INCLUDED
#define types__types_h_INCLUDED

#include <cstddef>
#include <cstdint>

typedef uint8_t u8;
/// Unsigned 16-bit integer
typedef uint16_t u16;
/// Unsigned 32-bit integer
typedef uint32_t u32;

/// Signed integer type of the result of subtracting two pointers
typedef ptrdiff_t isize;
/// Unsigned integer type of the result of the sizeof operator
typedef size_t usize;
/// Signed 8-bit integer
typedef int8_t i8;
/// Signed 16-bit integer
typedef int16_t i16;
/// Signed 32-bit integer
typedef int32_t i32;

#endif  // types__types_h_INCLUDED
