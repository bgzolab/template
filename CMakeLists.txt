# cmake version
cmake_minimum_required (VERSION 3.2)

# project name
project (makeDemo)

# head file path
# INCLUDE_DIRECTORIES (.)

# source path
# AUX_SOURCE_DIRECTORY (. DIR_SRCS)

# file (GLOB SOURCES)

aux_source_directory(./src/ DIR_SRCS)
# 添加编译文件
# add_executable( mylib.h mylib.c text.c)

# add link library
#TARGET_LINK_LIBRARIES(${PROJECT_NAME} m)

# CMakeLists.txt refer to https://www.hahack.com/codes/cmake/