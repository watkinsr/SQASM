cmake_minimum_required(VERSION 3.7)

project(sqint)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -w -Wextra -g")
set(CMAKE_BUILD_TYPE Debug)

include_directories(${PROJECT_SOURCE_DIR}/include)

add_executable(${PROJECT_NAME} src/main.cpp src/interpreter.cpp src/register.cpp src/engine.cpp)
