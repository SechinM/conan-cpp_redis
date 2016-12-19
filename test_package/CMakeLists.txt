cmake_minimum_required(VERSION 3.0)
project(testproj)

if(CMAKE_COMPILER_IS_GNUCXX OR APPLE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
endif()

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(testproj test.cpp)

target_link_libraries(testproj ${CONAN_LIBS}
                                cpp_redis)
