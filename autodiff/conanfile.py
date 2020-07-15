import os
from conans import ConanFile, CMake, tools

class ConanSqlite3(ConanFile):
    name = "autodiff"
    description = "autodiff is a C++17 library that uses modern and advanced programming techniques to enable automatic computation of derivatives in an efficient and easy way."
    url = "https://github.com/autodiff/autodiff/tree/master"
    homepage = "https://github.com/autodiff/autodiff/tree/master"
    topics = ("conan", "automatic differentiation", "calculus")
    license = "MIT Licence, Copyright (c) 2018–2020 Allan Leal"
    generators = "cmake"
    settings = "os", "compiler", "arch", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }

    default_options = {
        "shared": False,
        "fPIC": True
    }

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def build_requirements(self):
        self.build_requires("eigen/[>=3.3.7]@%s/%s" % (self.user, self.channel))

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        pass
        
    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        url = self.conan_data["sources"][self.version]["url"]
        archive_name = '%s-%s' %(self.name, self.version)
        os.rename(archive_name, self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        else:
            self._cmake = CMake(self)

            #set Cmake options here
            self._cmake.definitions["Eigen3_DIR"] = '%s/share/eigen3/cmake' % self.deps_cpp_info["eigen"].rootpath
            self._cmake.configure(source_dir=self._source_subfolder)
            return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "autodiff"
        self.cpp_info.names["cmake_find_package_multi"] = "autodiff"
