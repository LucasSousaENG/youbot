# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "youbot_manual_operation: 0 messages, 1 services")

set(MSG_I_FLAGS "-Istd_msgs:/opt/ros/kinetic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(youbot_manual_operation_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/lucas/catkin_ws/src/youbot/youbot_manual_operation/srv/executeTrajectory.srv" NAME_WE)
add_custom_target(_youbot_manual_operation_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "youbot_manual_operation" "/home/lucas/catkin_ws/src/youbot/youbot_manual_operation/srv/executeTrajectory.srv" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages

### Generating Services
_generate_srv_cpp(youbot_manual_operation
  "/home/lucas/catkin_ws/src/youbot/youbot_manual_operation/srv/executeTrajectory.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/youbot_manual_operation
)

### Generating Module File
_generate_module_cpp(youbot_manual_operation
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/youbot_manual_operation
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(youbot_manual_operation_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(youbot_manual_operation_generate_messages youbot_manual_operation_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/lucas/catkin_ws/src/youbot/youbot_manual_operation/srv/executeTrajectory.srv" NAME_WE)
add_dependencies(youbot_manual_operation_generate_messages_cpp _youbot_manual_operation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(youbot_manual_operation_gencpp)
add_dependencies(youbot_manual_operation_gencpp youbot_manual_operation_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS youbot_manual_operation_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages

### Generating Services
_generate_srv_eus(youbot_manual_operation
  "/home/lucas/catkin_ws/src/youbot/youbot_manual_operation/srv/executeTrajectory.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/youbot_manual_operation
)

### Generating Module File
_generate_module_eus(youbot_manual_operation
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/youbot_manual_operation
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(youbot_manual_operation_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(youbot_manual_operation_generate_messages youbot_manual_operation_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/lucas/catkin_ws/src/youbot/youbot_manual_operation/srv/executeTrajectory.srv" NAME_WE)
add_dependencies(youbot_manual_operation_generate_messages_eus _youbot_manual_operation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(youbot_manual_operation_geneus)
add_dependencies(youbot_manual_operation_geneus youbot_manual_operation_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS youbot_manual_operation_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages

### Generating Services
_generate_srv_lisp(youbot_manual_operation
  "/home/lucas/catkin_ws/src/youbot/youbot_manual_operation/srv/executeTrajectory.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/youbot_manual_operation
)

### Generating Module File
_generate_module_lisp(youbot_manual_operation
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/youbot_manual_operation
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(youbot_manual_operation_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(youbot_manual_operation_generate_messages youbot_manual_operation_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/lucas/catkin_ws/src/youbot/youbot_manual_operation/srv/executeTrajectory.srv" NAME_WE)
add_dependencies(youbot_manual_operation_generate_messages_lisp _youbot_manual_operation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(youbot_manual_operation_genlisp)
add_dependencies(youbot_manual_operation_genlisp youbot_manual_operation_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS youbot_manual_operation_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages

### Generating Services
_generate_srv_nodejs(youbot_manual_operation
  "/home/lucas/catkin_ws/src/youbot/youbot_manual_operation/srv/executeTrajectory.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/youbot_manual_operation
)

### Generating Module File
_generate_module_nodejs(youbot_manual_operation
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/youbot_manual_operation
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(youbot_manual_operation_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(youbot_manual_operation_generate_messages youbot_manual_operation_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/lucas/catkin_ws/src/youbot/youbot_manual_operation/srv/executeTrajectory.srv" NAME_WE)
add_dependencies(youbot_manual_operation_generate_messages_nodejs _youbot_manual_operation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(youbot_manual_operation_gennodejs)
add_dependencies(youbot_manual_operation_gennodejs youbot_manual_operation_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS youbot_manual_operation_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages

### Generating Services
_generate_srv_py(youbot_manual_operation
  "/home/lucas/catkin_ws/src/youbot/youbot_manual_operation/srv/executeTrajectory.srv"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/youbot_manual_operation
)

### Generating Module File
_generate_module_py(youbot_manual_operation
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/youbot_manual_operation
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(youbot_manual_operation_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(youbot_manual_operation_generate_messages youbot_manual_operation_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/lucas/catkin_ws/src/youbot/youbot_manual_operation/srv/executeTrajectory.srv" NAME_WE)
add_dependencies(youbot_manual_operation_generate_messages_py _youbot_manual_operation_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(youbot_manual_operation_genpy)
add_dependencies(youbot_manual_operation_genpy youbot_manual_operation_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS youbot_manual_operation_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/youbot_manual_operation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/youbot_manual_operation
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(youbot_manual_operation_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/youbot_manual_operation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/youbot_manual_operation
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(youbot_manual_operation_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/youbot_manual_operation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/youbot_manual_operation
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(youbot_manual_operation_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/youbot_manual_operation)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/youbot_manual_operation
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(youbot_manual_operation_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/youbot_manual_operation)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/youbot_manual_operation\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/youbot_manual_operation
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(youbot_manual_operation_generate_messages_py std_msgs_generate_messages_py)
endif()
