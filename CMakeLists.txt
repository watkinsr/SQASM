cmake_minimum_required(VERSION 3.19.7)

project(sqint)

add_executable(${PROJECT_NAME} src/main.cpp src/interpreter.cpp src/register.cpp src/engine.cpp)
