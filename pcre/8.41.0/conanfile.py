#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from conans import ConanFile, CMake, tools
import os


class PCREConan(ConanFile):
    name = "pcre"
    version = "8.41.0"
    url = "https://github.com/bincrafters/conan-pcre"
    homepage = "https://www.pcre.org"
    author = "Bincrafters <bincrafters@gmail.com>"
    description = "Perl Compatible Regular Expressions"
    license = "BSD"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_bzip2": [True, False],
        "with_zlib": [True, False],
        "with_jit": [True, False],
        "build_pcrecpp": [True, False],
        "build_pcregrep": [True, False],
        "with_utf": [True, False],
        "with_unicode_properties": [True, False]
    }
    default_options = {'shared': False, 'fPIC': True, 'with_bzip2': True, 'with_zlib': True, 'with_jit': False, 'build_pcrecpp': False, 'build_pcregrep': False, 'with_utf': False, 'with_unicode_properties': False}
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        if not self.options.build_pcrecpp:
            del self.settings.compiler.libcxx
        if self.options.with_unicode_properties:
            self.options.with_utf = True

    def patch_cmake(self):
        """Patch CMake file to avoid man and share during install stage
        """
        cmake_file = os.path.join(self._source_subfolder, "CMakeLists.txt")
        tools.replace_in_file(cmake_file, "INSTALL(FILES ${man1} DESTINATION man/man1)", "")
        tools.replace_in_file(cmake_file, "INSTALL(FILES ${man3} DESTINATION man/man3)", "")
        tools.replace_in_file(cmake_file, "INSTALL(FILES ${html} DESTINATION share/doc/pcre/html)", "")

    def source(self):
        version = self.version.split('.')
        source_url = "https://ftp.pcre.org"
        tools.get("{0}/pub/pcre/pcre-{1}.{2}.tar.gz".format(source_url, version[0], version[1]))
        extracted_dir = self.name + "-" + version[0] + '.' + version[1]
        os.rename(extracted_dir, self._source_subfolder)
        self.patch_cmake()

    def requirements(self):
        if self.options.with_bzip2:
            self.requires.add("bzip2/1.0.8@%s/%s" % (self.user, self.channel))
        if self.options.with_zlib:
            self.requires.add("zlib/1.2.11@%s/%s" % (self.user, self.channel))

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["PCRE_BUILD_TESTS"] = False
        cmake.definitions["PCRE_BUILD_PCREGREP"] = self.options.build_pcregrep
        cmake.definitions["PCRE_BUILD_PCRECPP"] = self.options.build_pcrecpp
        cmake.definitions["PCRE_SUPPORT_LIBZ"] = self.options.with_zlib
        cmake.definitions["PCRE_SUPPORT_LIBBZ2"] = self.options.with_bzip2
        cmake.definitions["PCRE_SUPPORT_JIT"] = self.options.with_jit
        cmake.definitions["PCRE_SUPPORT_UTF"] = self.options.with_utf
        cmake.definitions["PCRE_SUPPORT_UNICODE_PROPERTIES"] = self.options.with_unicode_properties
        cmake.definitions["PCRE_SUPPORT_LIBREADLINE"] = False
        cmake.definitions["PCRE_SUPPORT_LIBEDIT"] = False
        cmake.definitions["VERBOSE"]=True

        if self.options.with_bzip2:
            cmake.definitions["BZIP2_INCLUDE_DIR"] = "CONAN_INCLUDE_DIRS_BZIP2"

        if self.options.fPIC:
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = True
        
        if self.settings.os == "Windows" and self.settings.compiler == "Visual Studio":
            cmake.definitions["PCRE_STATIC_RUNTIME"] = not self.options.shared and "MT" in self.settings.compiler.runtime
        cmake.configure(build_folder=self._build_subfolder, source_folder=self._source_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENCE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        if self.settings.os == "Windows" and self.settings.build_type == 'Debug':
            self.cpp_info.libs = ['pcreposixd', 'pcred']
        else:
            self.cpp_info.libs = ['pcreposix', 'pcre']
        if not self.options.shared:
            self.cpp_info.defines.append("PCRE_STATIC=1")
