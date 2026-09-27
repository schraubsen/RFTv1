cmake_minimum_required(VERSION 3.16)
project(rft_electribe_tools CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

enable_testing()

add_subdirectory(electribe_core)
add_subdirectory(cli)
add_subdirectory(standalone)
