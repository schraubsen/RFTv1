add_library(electribe_core STATIC
    src/sysex7.cpp
    src/schema.cpp
    src/pattern_file.cpp
)

target_include_directories(electribe_core PUBLIC include)
target_compile_features(electribe_core PUBLIC cxx_std_17)

add_executable(test_sysex7 tests/test_sysex7.cpp)
target_link_libraries(test_sysex7 PRIVATE electribe_core)
add_test(NAME test_sysex7 COMMAND test_sysex7)

add_executable(test_schema tests/test_schema.cpp)
target_link_libraries(test_schema PRIVATE electribe_core)
add_test(NAME test_schema
    COMMAND test_schema "${CMAKE_SOURCE_DIR}/schema/esx1.def")
