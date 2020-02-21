#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil
from conans import ConanFile, AutoToolsBuildEnvironment, tools


class Bzip2Conan(ConanFile):
    name     = "bzip2"
    version  = "1.0.6"
    homepage = "http://www.bzip.org"
    url     = 'https://sourceware.org/pub/bzip2'
    author  = "Conan Community"
    license = "bzip2-1.0.6"
    description = "bzip2 is a free and open-source file compression program that uses the Burrows–Wheeler algorithm."
    topics   = ("conan", "bzip2", "data-compressor", "file-compression")
    settings = "os", "compiler", "arch", "build_type"
    options  = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    exports = "LICENSE"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _source_subfolder = 'source_subfolder'
    _build_subfolder  = 'build_subfolder'

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        folder_name = "%s-%s" % (self.name, self.version)
        arch_name = "%s.tar.gz" % folder_name
        print("%s/%s" % (self.url, arch_name))
        tools.download(url="%s/%s" % (self.url, arch_name), filename=arch_name)
        tools.untargz(arch_name, destination='.', pattern=None)
        shutil.move(folder_name, self._source_subfolder)

    def build(self):
        with tools.chdir(self._source_subfolder):
            env_build = AutoToolsBuildEnvironment(self)
            env_build.make()
        pass
    
    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy("bzlib.h", dst="include", src=self._source_subfolder)
        self.copy("*.a", dst="lib", src=self._source_subfolder)
        self.copy("*.so", dst="lib", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs = ['bz2']
