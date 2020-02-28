#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil
from conans import ConanFile, tools, CMake
from glob import glob

class EigenConan(ConanFile):
    name = "eigen"
    version = "3.3.7"
    url = "https://github.com/conan-community/conan-eigen"
    homepage = "http://eigen.tuxfamily.org"
    description = "Eigen is a C++ template library for linear algebra: matrices, vectors, \
                   numerical solvers, and related algorithms."
    license = "Mozilla Public License Version 2.0"
    no_copy_source = True
    settings = 'arch', 'cppstd', 'compiler', 'build_type'

    options = {
        "test": [True, False]
    }

    default_options = "test=False"

    _build_subfolder  = 'build'
    _source_subfolder = 'src'

    def configure(self):
        pass

    def source(self):
        source_url = "http://bitbucket.org/eigen/eigen"
        tools.get("{0}/get/{1}.tar.gz".format(source_url, self.version))
        shutil.move(glob("eigen-eigen-*")[0], self._source_subfolder)

    def _configure_cmake(self):
        
        cmake = CMake(self)
        if self.settings.compiler=="gcc":
            if self.settings.arch=="broadwell":
                cmake.definitions["CMAKE_CXX_FLAGS"] = "-march=broadwell -tune=broadwell"

            else:
                cmake.definitions["CMAKE_CXX_FLAGS"] = "-mtune=generic"

        cmake.configure(build_folder=self._build_subfolder, source_folder=self._source_subfolder)
        return cmake

    def build(self):
        self.output.info('current working dir: %s' % os.getcwd())
        os.makedirs(self._build_subfolder)
        with tools.chdir(self._build_subfolder):
            cmake = self._configure_cmake()
            cmake.build()

    def package(self):
        with tools.chdir(os.path.join(self.build_folder, self._build_subfolder)):
            # do not reinvoke cmake here
            self.run("make install")

        # additional ressources
        if self.settings.build_type == 'Debug':
            self.copy('*.py', src='src/debug/gdb', dst='gdb/eigen', keep_path=True)
        
    def package_info(self):
        self.cpp_info.includedirs = ['include/eigen3']

        if self.settings.build_type == 'Debug':
            # case sensitive in cmake
            self.user_info.GDB_PRINTER = 'gdb'
