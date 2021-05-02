import os, shutil
from pathlib import Path

from conans import ConanFile, tools, CMake
from conans.errors import ConanInvalidConfiguration

class YwyuConan(ConanFile):
    name = "iwyu"
    longname = "include-what-you-use"
    description = "include what you use is a tool to check include in C++ code"
    topics = (
        "conan",
        "cplusplus",
        "utility"
    )
    url = "https://github.com/include-what-you-use/include-what-you-use"
    homepage = "https://include-what-you-use.org"
    license = "MIT"
    settings = "compiler"

    _source_subfolder = 'source_subfolder'
    _build_subfolder = 'build_subfolder'
    root = None

    def configure(self):
        if self.settings.compiler in ['clang', 'apple-clang']:
            return
        else:
            raise AttributeError('compiler not supported !')

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        vv = self.version.split('.')
        extracted_dir = self.longname + "-" + '%s.%s' % (vv[0], vv[1])
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        cmake = CMake(self)
        self.root = Path('%s' % os.environ['CXX']) # points to bin
        self.root = self.root.parent.parent.absolute()

        self.output.info('clang root file set to %s' % self.root)
        cmake.definitions['Clang_DIR'] = '%s/lib/cmake/clang' % self.root
        cmake.definitions['LLVM_DIR'] = '%s/lib/cmake/llvm' % self.root
        cmake.definitions['CMAKE_VERBOSE_MAKEFILE'] = False # for debugging
        cmake.definitions['CMAKE_CXX_FLAGS'] = '-fno-rtti'

        cmake.configure(source_dir=self._source_subfolder
        #, build_dir=self._build_subfolder
        )
        cmake.build(target="install")

    def package(self):
        self.copy("include/*", src=self._source_subfolder)
        self.copy("LICENSE", dst="licenses" , src=self._source_subfolder)

    def package_id(self):
        self.info.header_only()

    def package_info(self):
        self.cpp_info.includedirs = '%s/lib/clang/%s.0/include' % (self.root, self.settings.compiler.version)
