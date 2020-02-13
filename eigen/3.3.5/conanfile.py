#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil
from conans import ConanFile, tools, CMake
from glob import glob

class EigenConan(ConanFile):
    name = "eigen"
    version = "3.3.5"
    url = "https://github.com/conan-community/conan-eigen"
    homepage = "http://eigen.tuxfamily.org"
    description = "Eigen is a C++ template library for linear algebra: matrices, vectors, \
                   numerical solvers, and related algorithms."
    license = "Mozilla Public License Version 2.0"
    no_copy_source = True
    settings = 'arch', 'cppstd', 'compiler'

    options = {"EIGEN_USE_BLAS":           [True, False]
             , "EIGEN_USE_LAPACKE":        [True, False]
             , "EIGEN_USE_LAPACKE_STRICT": [True, False]
             , "EIGEN_USE_MKL_VML":        [True, False]
             , "EIGEN_USE_MKL_ALL":        [True, False]
    }

    default_options = "EIGEN_USE_BLAS=False",\
        "EIGEN_USE_LAPACKE=False",\
        "EIGEN_USE_LAPACKE_STRICT=False",\
        "EIGEN_USE_MKL_VML=False",\
        "EIGEN_USE_MKL_ALL=False"

    _build_subfolder = 'build'
    _source_subfolder = 'src'

    def configure(self):

        if self.options.EIGEN_USE_BLAS == True:
            self.requires("lapack/3.8.0@%s/%s" % (self.user, self.channel))

        if self.options.EIGEN_USE_LAPACKE == True:
            self.requires("lapack/3.8.0@%s/%s" % (self.user, self.channel))

        if self.options.EIGEN_USE_LAPACKE_STRICT == True:
            self.requires("lapack/3.8.0@%s/%s" % (self.user, self.channel))

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
            cmake.install()
    def package(self):
        pass
        #with tools.chdir(self._build_subfolder):
        #    cmake = self._configure_cmake()
        #    cmake.install()


    def package_info(self):
        self.cpp_info.includedirs = ['include/eigen3']

        # maybe too intrusive to set here...
        if self.options.EIGEN_USE_BLAS:
            self.cpp_info.defines.append("EIGEN_USE_BLAS")

        if self.options.EIGEN_USE_LAPACKE:
            self.cpp_info.defines.append("EIGEN_USE_LAPACKE")

        if self.options.EIGEN_USE_LAPACKE_STRICT:
            self.cpp_info.defines.append("EIGEN_USE_LAPACKE_STRICT")

        if self.options.EIGEN_USE_MKL_VML:
            self.cpp_info.defines.append("EIGEN_USE_MKL_VML")

        if self.options.EIGEN_USE_MKL_ALL:
            self.cpp_info.defines.append("EIGEN_USE_MKL_ALL")
