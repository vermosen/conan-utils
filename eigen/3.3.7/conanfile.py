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

        #https://gitlab.com/libeigen/eigen/-/archive/3.3.8/eigen-3.3.8.tar.gz
        source_url = "https://gitlab.com/libeigen/eigen"
        tools.get("{0}/-/archive/{1}/eigen-{1}.tar.gz".format(source_url, self.version))
        shutil.move(glob("eigen-*")[0], self._source_subfolder)

        if self.settings.build_type == 'Debug':
            #s.makedirs('%s/%s/debug/gdb' % (self.build_folder, self._build_subfolder), exist_ok=True)
            shutil.copyfile( '%s/%s/debug/gdb/printers.py' % (self.source_folder, self._source_subfolder)
                           , '%s/%s/debug/gdb/eigen_printers.py' % (self.source_folder, self._source_subfolder)
                           , follow_symlinks = True)

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
        # the step could be completely disabled since eigen perform again the whole
        # setup on the install steps
        self.output.info('current working dir: %s' % os.getcwd())
        os.makedirs(self._build_subfolder)
        with tools.chdir(self._build_subfolder):
            cmake = self._configure_cmake()
            cmake.build()

    def package(self):
        with tools.chdir(os.path.join(self.build_folder, self._build_subfolder)):
            cmake = self._configure_cmake()
            cmake.install()

        # additional ressources
        if self.settings.build_type == 'Debug':
            self.copy('eigen_printers.py', src='src/debug/gdb', dst='gdb', keep_path=True)
            
    def package_info(self):
        self.cpp_info.includedirs = ['include/eigen3']

        if self.settings.build_type == 'Debug':
            # case sensitive in cmake
            self.user_info.GDB_PRINTER_FOLDER = 'gdb'
            self.user_info.GDB_PRINTER_FILE   = 'eigen_printers.py'
            self.user_info.GDB_IMPORT_CLASSES = 'register_eigen_printers, build_eigen_dictionary'
            self.user_info.GDB_PRINTER_CLASS  = 'register_eigen_printers'
