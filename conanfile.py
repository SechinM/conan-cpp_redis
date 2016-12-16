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
        self.run("cd cpp_redis && git checkout 8f902dae91d87fa0be891d40e5c853762dae6060")  
    
    def build(self): 
        cmake = CMake(self.settings)

        cmake_options = []
        for option_name in self.options.values.fields:
            activated = getattr(self.options, option_name)
            the_option = "%s=" % option_name.upper()
            if option_name == "shared":
                the_option = "CPP_REDIS_SHARED_LIB=OFF" if activated else "CPP_REDIS_SHARED_LIB=ON"
            else:
                the_option += "ON" if activated else "OFF"
            cmake_options.append(the_option)

        cmake_cmd_options = " -D".join(cmake_options)
                
	cmake_conf_command = 'cmake %s/cpp_redis %s -DCMAKE_INSTALL_PREFIX:PATH=install -D%s' % (self.conanfile_directory, cmake.command_line, cmake_cmd_options)
        self.output.warn(cmake_conf_command)
        self.run(cmake_conf_command)

	self.run("cmake --build . --target install %s" % cmake.build_config)


        #self.run("cd cpp_redis/build && sudo cmake -DCMAKE_INSTALL_PREFIX=/usr/local ..")
        #self.run("cd cpp_redis/build && sudo make")
        #self.run("cd cpp_redis/build && sudo make install")

    
    def package(self):
        self.copy("*", dst="include/cpp_redis", src="install/include/cpp_redis")
        self.copy("*", dst="include/cpp_redis/builders", src="install/include/cpp_redis/builders")
        self.copy("*", dst="include/cpp_redis/network", src="install/include/cpp_redis/network")
        self.copy("*", dst="include/cpp_redis/replies", src="install/include/cpp_redis/replies")	
        self.copy("*.a", dst="lib", src="install/lib")
        self.copy("*.so*", dst="lib", src="install/lib")
 
    def package_info(self):
        self.cpp_info.libs = ["cpp_redis"]
