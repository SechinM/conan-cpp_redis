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
    short_paths = True
    options = {"shared": [True, False]}
    default_options = "shared=False"
    
    #def source(self):
    #    tools.download("http://download.redis.io/redis-stable.tar.gz", "redis-stable.tar.gz")
    #    tools.untargz("redis-stable.tar.gz", "redis-stable")           
        
    def build(self):          
        tools.download("http://download.redis.io/redis-stable.tar.gz", "redis-stable.tar.gz")
        tools.untargz("redis-stable.tar.gz", "redis-stable")   
        
        self.run("cd redis-stable")      
        
        cmake = CMake(self.settings)

        cmake_options = []
        for option_name in self.options.values.fields:
            activated = getattr(self.options, option_name)
            the_option = "%s=" % option_name.upper()
            if option_name == "shared":
                the_option = "REDIS_STATIC_LIB=OFF" if activated else "REDIS_STATIC_LIB=ON"
            else:
                the_option += "ON" if activated else "OFF"
            cmake_options.append(the_option)

        cmake_cmd_options = " -D".join(cmake_options)
                
        cmake_conf_command = 'cd redis-stable && make install %s' % (self.conanfile_directory, cmake.command_line, cmake_cmd_options)
        self.output.warn(cmake_conf_command)
        self.run(cmake_conf_command)
        self.run("cd redis-stable && make install %s" % cmake.build_config)
                
    
    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def package(self):
        self.copy("*.h", dst="include", src="install/include")
        self.copy("*.dll", dst="bin", src="install/bin")
        self.copy("*.lib", dst="lib", src="install/lib")
        self.copy("*.a", dst="lib", src="install/lib")
        self.copy("*.so*", dst="lib", src="install/lib")
        self.copy("*.dylib", dst="lib", src="install/lib")
        self.copy("nanocat*", dst="bin", src="install/bin")
        self.copy("*.*", dst="lib/pkgconfig", src="install/lib/pkgconfig")

    def package_info(self):
        self.cpp_info.libs = ["redis"]

        if not self.options.shared:
            self.cpp_info.defines.extend(["NN_STATIC_LIB=ON"])
