from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "stable")
username = os.getenv("CONAN_USERNAME", "SechinM")

class RedisReuseConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "Redis/1.0.0@%s/%s" % (username, channel)
    generators = "cmake"

    def imports(self):
      self.copy("*.dll", dst="bin", src="bin")
      self.copy("*.dylib*", dst="bin", src="lib")

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def test(self):
        self.run("cd bin && .%stestproj" % os.sep)
