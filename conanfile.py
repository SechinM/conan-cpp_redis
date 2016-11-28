from conans import ConanFile, CMake
from conans.tools import replace_in_file
import os
import shutil

class nanomsgConan(ConanFile):
    name = "redis"
    version = "1.0.0"
    url="https://github.com/SechinM/conan-redis.git"
    generators = "cmake", "txt"
    settings = "os", "compiler", "build_type", "arch"
    short_paths = True
    options = {"shared": [True, False],
               "enable_doc": [True, False],
               "enable_getaddrinfo_a": [True, False],
               "enable_tests": [True, False],
               "enable_tools": [True, False],
               "enable_nanocat": [True, False],
               }
    default_options = "shared=False", \
        "enable_doc=False", \
        "enable_getaddrinfo_a=True", \
        "enable_tests=False", \
        "enable_tools=True", \
        "enable_nanocat=True"
    
    def source(self):
        tools.download("http://download.redis.io/redis-stable.tar.gz", "redis-stable.tar.gz")
        tools.untargz("redis-stable.tar.gz", "redis-stable")        
        self.run("cd redis-stable")
        
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
