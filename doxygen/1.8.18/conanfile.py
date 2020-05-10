from conans import ConanFile, tools, CMake


class DoxygenConan(ConanFile):
    name = "doxygen"
    version = "1.8.18"
    settings = "os", "compiler", "arch"
    description = "Doxygen is the de facto standard tool for generating documentation from annotated C++ sources"
    homepage = "https://github.com/doxygen/doxygen"
    license = "GNU General Public License v2.0: https://github.com/doxygen/doxygen/blob/master/LICENSE"
    url = "https://github.com/doxygen/doxygen"
    no_copy_sources = True
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    
    def source(self):
        tools.Version(self.version)
        tools.get("%s/archive/Release_%s_%s_%s.tar.gz" % (self.homepage, vers.major, vers.minor, vers.patch))

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self._source_subfolder, build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
