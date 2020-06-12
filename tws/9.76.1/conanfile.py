#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, shutil
from conans import ConanFile, CMake, tools
from conans.model.version import Version
from conans.errors import ConanInvalidConfiguration


class TwsConan(ConanFile):
    """ 
    Adapted from https://github.com/bincrafters/conan-gtest
    """
    name = "tws"
    version = "9.76.1"
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
        if self.settings.os == "Linux":
            pass
        elif self.settings.os == "Windows":
            del self.options.fPIC
            pass
        else:
            raise ConanInvalidConfiguration("os not supported")
            pass
            
    def source(self):
    
        vers = Version(self.version).as_list

        sha256 = "9bf1fe5182a604b4135edc1a425ae356c9ad15e9b23f9f12a02e80184c3a249c"
        
        if self.settings.os == "Windows":
            tools.get("%s/downloads/twsapi_macunix.%s%s.%02d.zip" % (self.homepage, vers[0], vers[1], vers[2]))
            #provided there's a way to handle msi installers...
            #tools.download("%s/downloads/TWS API Install %s%s.%02d.msi" % (self.homepage, vers[0], vers[1], vers[2]))

        elif self.settings.os == "Linux":
            tools.get("%s/downloads/twsapi_macunix.%s%s.%02d.zip" % (self.homepage, vers[0], vers[1], vers[2]))
        
        extracted_dirs = {"IBJts/source/cppclient":"tws"}
        
        # create a client and a sample folder
        for k, v in extracted_dirs.items():
           shutil.move(k, v)
        
        # create the cmake file
        f = open('CMakeLists.txt', 'w+')
        f.writelines(
            ['cmake_minimum_required(VERSION 2.8.9)\r\n',
             'project(tws)\r\n',
             'include_directories(tws)\r\n',
             'SET(CMAKE_CXX_STANDARD 11)\r\n'
             'file(GLOB SOURCES "tws/client/*.cpp")\r\n',
             'file(GLOB PUBLIC_HEADER "tws/client/*.h")\r\n'
            ])
    
        if self.options.shared:
            f.writelines('add_library(tws SHARED ${SOURCES} ${PUBLIC_HEADER})\r\n')
        else:
            f.writelines('add_library(tws STATIC ${SOURCES} ${PUBLIC_HEADER})\r\n')
            f.writelines(['install(TARGETS tws ARCHIVE DESTINATION lib PUBLIC_HEADER DESTINATION include)'])    
            f.close()
        
    def _configure_cmake(self):
        cmake = CMake(self, set_cmake_flags=True)
        return cmake

    def build(self):
        if self.settings.os == "Linux":
            cmake = self._configure_cmake()
            cmake.configure()
            cmake.build()

    def package(self):
        if self.settings.os == "Linux":
            cmake = self._configure_cmake()
            cmake.install()

        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*.pdb", dst="bin", src=".", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=True)
        self.copy(pattern="*.h", dst="include/tws", src="tws/client", keep_path=True)
        self.copy(pattern="*.cpp", dst="include/tws", src="tws/client", keep_path=True)

        
    def package_id(self):
        pass

    def package_info(self):
        self.cpp_info.libs = ["tws"]
        pass


