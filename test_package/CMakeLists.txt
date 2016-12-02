cmake_minimum_required(VERSION 3.5)
project(testproj)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(testproj test.cpp)

target_link_libraries(testproj cpp_redis)
