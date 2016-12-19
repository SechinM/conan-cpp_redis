from conans import ConanFile, CMake, tools
from conans.tools import replace_in_file
import os
import shutil

class redisConan(ConanFile):
    name = "redis"
    version = "1.0.0"
    url="https://github.com/SechinM/conan-redis.git"
    generators = "cmake", "txt"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
       
    def source(self):
        self.run("git clone https://github.com/Cylix/cpp_redis.git")
#        self.run("cd cpp_redis && git checkout 8f902dae91d87fa0be891d40e5c853762dae6060")  
#	self.run("cd cpp_redis")    

    def build(self): 
	tools.replace_in_file("cpp_redis/CMakeLists.txt", "add_library(${PROJECT} STATIC ${SOURCES})", '''add_library(${PROJECT} SHARED ${SOURCES})''')

        cmake = CMake(self.settings)

        cmake_options = []
        for option_name in self.options.values.fields:
            activated = getattr(self.options, option_name)
            the_option = "%s=" % option_name.upper()
            if option_name == "shared":
                the_option = "CPP_REDIS_STATIC_LIB=OFF" if activated else "CPP_REDIS_STATIC_LIB=ON"
            else:
                the_option += "ON" if activated else "OFF"
            cmake_options.append(the_option)

       	cmake_cmd_options = " -D".join(cmake_options)
                
        cmake_conf_command = 'cmake %s/cpp_redis %s -DCMAKE_INSTALL_PREFIX:PATH=install -D%s' % (self.conanfile_directory, cmake.command_line, cmake_cmd_options)
        self.output.warn(cmake_conf_command)
        self.run(cmake_conf_command)
	self.run("cmake --build . %s" % cmake.build_config)
	self.run("cmake --build . --target install %s" % cmake.build_config)


#	self.run("cd cpp_redis && mkdir build")
#	self.run("cd cpp_redis/build && cmake ..")	
#	self.run("make")
#	self.run("make install")
    
    def package(self):
        self.copy("*", dst="usr/include/cpp_redis", src="install/include/cpp_redis")
        self.copy("*", dst="usr/include/cpp_redis/builders", src="install/include/cpp_redis/builders")
        self.copy("*", dst="usr/include/cpp_redis/network", src="install/include/cpp_redis/network")
        self.copy("*", dst="usr/include/cpp_redis/replies", src="install/include/cpp_redis/replies")	
        self.copy("*", dst="usr/bin", src="install/bin")
        self.copy("*.a*", dst="usr/lib", src="install/lib")
        self.copy("*.so*", dst="usr/lib", src="install/lib")
 
    def package_info(self):
        self.cpp_info.libs = ["cpp_redis"]
