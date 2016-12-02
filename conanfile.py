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
    default_options = "shared=True"
       
    def source(self):
        self.run("git clone https://github.com/Cylix/cpp_redis.git")
        self.run("cd cpp_redis && git checkout 8f902dae91d87fa0be891d40e5c853762dae6060")  
	os.mkdir("cpp_redis/build")
    
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
                
        self.run("cd cpp_redis/build && sudo cmake -DCMAKE_INSTALL_PREFIX=/usr/local..")
        self.run("cd cpp_redis/build && sudo make")
        self.run("cd cpp_redis/build && sudo make install")

    
    def package(self):
        self.copy("*.h", dst="include", src="/install/include")
        self.copy("*.hpp", dst="include", src="/install/include")
        self.copy("*.a", dst="lib", src="/install/lib")
        self.copy("*.so", dst="lib", src="/install/lib")
 
    def package_info(self):
        self.cpp_info.libs = ["cpp_redis"]
