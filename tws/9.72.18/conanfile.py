#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil
from conans import ConanFile, CMake, tools
from conans.model.version import Version
from conans.errors import ConanInvalidConfiguration


class TwsConan(ConanFile):
    """ Adapted from https://github.com/bincrafters/conan-gtest
    """
    name = "tws"
    version = "9.72.18"
    description = "Interactive Broker TWS C++ framework"
    homepage = "http://interactivebrokers.github.io"
    topics = ("conan", "tws", "interface")
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "samples": [True, False]}

    default_options = {"shared": False,
                       "fPIC": True,
                       "samples": False}

    _source_subfolder = "source_subfolder"

    def configure(self):
        if self.settings.os != "Macos":
            raise ConanInvalidConfiguration("os not supported")

    def source(self):
        #http://interactivebrokers.github.io/downloads/twsapi_macunix.972.18.zip
        vers = tools.Version(self.version) 
        sha256 = "9bf1fe5182a604b4135edc1a425ae356c9ad15e9b23f9f12a02e80184c3a249c"
        tools.get("{0}/downloads/twsapi_macunix.{1}{2}.{3}.zip".format(self.homepage, vers.major, vers.minor, vers.patch))
        extracted_dirs = {"IBJts/source/CppClient":"client", "IBJts/samples/Cpp":"samples"}
        
        # create a client and a sample folder
        for k, v in extracted_dirs.items():
            shutil.move(k, v)
        
        # create the cmake file
        f = open('CMakeLists.txt', 'w+')
        f.writelines(
            ['cmake_minimum_required(VERSION 2.8.9)\r\n',
             'project(tws)\r\n',
             'include_directories(client)\r\n',
             'SET(CMAKE_CXX_STANDARD 11)\r\n'
             'file(GLOB SOURCES "client/client/*.cpp" "client/ssl/*.cpp")\r\n',
             'file(GLOB PUBLIC_HEADER "client/client/*.h" "client/ssl/*.h")\r\n'])
        
        if self.options.shared:
            f.writelines('add_library(tws SHARED ${SOURCES} ${PUBLIC_HEADER})\r\n')
        else:
            f.writelines('add_library(tws STATIC ${SOURCES} ${PUBLIC_HEADER})\r\n')
        f.close()
        
    def _configure_cmake(self):
        cmake = CMake(self, set_cmake_flags=True)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*.pdb", dst="bin", src=".", keep_path=False)
        cmake = self._configure_cmake()
        cmake.install()

    def package_id(self):
        del self.info.options.no_main

    def package_info(self):
        if self.options.build_gmock:
            gmock_libs = ['gmock', 'gtest'] if self.options.no_main else ['gmock_main', 'gmock', 'gtest']
            self.cpp_info.libs = ["{}{}".format(lib, self._postfix) for lib in gmock_libs]
        else:
            gtest_libs = ['gtest'] if self.options.no_main else ['gtest_main' , 'gtest']
            self.cpp_info.libs = ["{}{}".format(lib, self._postfix) for lib in gtest_libs]

        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")

        if self.options.shared:
            self.cpp_info.defines.append("GTEST_LINKED_AS_SHARED_LIBRARY=1")

        if self.settings.compiler == "Visual Studio":
            if Version(self.settings.compiler.version.value) >= "15":
                self.cpp_info.defines.append("GTEST_LANG_CXX11=1")
                self.cpp_info.defines.append("GTEST_HAS_TR1_TUPLE=0")


