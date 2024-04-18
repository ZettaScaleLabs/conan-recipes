cmake_minimum_required(VERSION 3.16)
project(test_package LANGUAGES CXX)

find_package(zenohcpp REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.cxx)
if(${ZENOHCXX_LIB} STREQUAL "zenohc")
    target_link_libraries(${PROJECT_NAME} PRIVATE zenohcxx::zenohc::lib)
    add_compile_definitions(ZENOHCXX_ZENOHC)
elseif(${ZENOHCXX_LIB} STREQUAL "zenohpico")
    target_link_libraries(${PROJECT_NAME} PRIVATE zenohcxx::zenohpico)
    add_compile_definitions(ZENOHCXX_ZENOHPICO)
else()
    message(FATAL_ERROR "ZENOHCXX_LIB must be either 'zenohc' or 'zenohpico'")
endif()

target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_17)