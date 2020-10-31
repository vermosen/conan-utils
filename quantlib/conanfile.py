#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil, os, sys
from conans import ConanFile, CMake, tools

class QuantLibConan(ConanFile):

    rawname = 'QuantLib'
    name = rawname.lower()
    license = "see package content"
    homepage = "https://www.quantlib.org/"
    url = "https://github.com/lballabio/QuantLib/"
    description = "The QuantLib C++ library"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    _source_subfolder = 'src'

    @property
    def is_msvc(self):
        return self.settings.compiler == 'Visual Studio'

    def requirements(self):
        self.requires("boost/[>=1.53.0]@%s/%s" % (self.user, self.channel))

    def source(self):
        version = self.version.split('.')
        # format: https://github.com/lballabio/QuantLib/archive/QuantLib-v1.13.zip
        filename = '{0}-{0}-v{1}.{2}'.format(self.rawname, version[0], version[1])
        tools.download('{0}archive/{1}-v{2}.{3}.tar.gz'.format(self.url, self.rawname, version[0], version[1]), '%s.tar.gz' % filename)
        tools.unzip('%s.tar.gz' % filename)
        shutil.move(filename, self._source_subfolder)

    def cmake_configure(self):
        cmake = CMake(self)

        if self.settings.compiler == 'gcc':
            if self.settings.compiler.libcxx == 'libstdc++11':
                cmake.definitions["CMAKE_CXX_FLAGS"] = "-D_GLIBCXX_USE_CXX11_ABI=1"
            else:
                cmake.definitions["CMAKE_CXX_FLAGS"] = "-D_GLIBCXX_USE_CXX11_ABI=0"

            # more logs
            cmake.definitions["CMAKE_VERBOSE_MAKEFILE"] = "ON"

        cmake.configure(source_folder="src", build_folder=self.build_dir)
        return cmake

    def build(self):
        self.build_dir = os.path.join(os.getcwd(), 'build')
        with tools.chdir(self._source_subfolder):
            cmake = self.cmake_configure()

            if not self.is_msvc:
                cmake.build(target='QuantLib')
            else:
                cmake.build()

    def package(self):
        self.build_dir = os.path.join(os.getcwd(), 'build')
        with tools.chdir(self.build_dir):
            self.output.info('running packaging in folder: %s' % os.getcwd())
            self.copy('*.hpp', src='src/ql', dst='include/ql')
            self.copy('*/*.a' , dst='lib', keep_path=False)
            self.copy('*/*.so' , dst='lib', keep_path=False)
            self.copy('*/*.lib', dst='lib', keep_path=False)
            self.copy('*/*.dll', dst='lib', keep_path=False)
            self.copy('*/*.pdb', dst='lib', keep_path=False)

        if self.settings.build_type == 'Debug':
            self.copy('ql/*/*.hpp', dst='src', src=self._source_subfolder)
            self.copy('ql/*/*.cpp', dst='src', src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs = ["QuantLib"]
