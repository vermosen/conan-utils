#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import stat
from conans import ConanFile, tools, CMake, AutoToolsBuildEnvironment

class ZlibConan(ConanFile):
    name = "zlib"
    version = "1.2.11"
    homepage = "https://zlib.net/fossils"
    author = "Jean-Mathieu Vermosen"
    license = "Zlib"
    description = ("A Massively Spiffy Yet Delicately Unobtrusive Compression Library "
                  "(Also Free, Not to Mention Unencumbered by Patents)")
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    exports = "LICENSE"
    exports_sources = ["CMakeLists.txt"]
    generators = ["cmake", "compiler_args"]
    _source_subfolder  = "src"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        tools.get("{}/{}-{}.tar.gz".format(self.homepage, self.name, self.version))
        os.rename("{}-{}".format(self.name, self.version), self._source_subfolder )
        if not tools.os_info.is_windows:
            configure_file = os.path.join(self._source_subfolder , "configure")
            st = os.stat(configure_file)
            os.chmod(configure_file, st.st_mode | stat.S_IEXEC)
        else:
            pass


    def build(self):
        with tools.chdir(self._source_subfolder ):
            for filename in ['zconf.h', 'zconf.h.cmakein', 'zconf.h.in']:
                tools.replace_in_file(filename,
                                      '#ifdef HAVE_UNISTD_H    /* may be set to #if 1 by ./configure */',
                                      '#if defined(HAVE_UNISTD_H) && (1-HAVE_UNISTD_H-1 != 0)')
                tools.replace_in_file(filename,
                                      '#ifdef HAVE_STDARG_H    /* may be set to #if 1 by ./configure */',
                                      '#if defined(HAVE_STDARG_H) && (1-HAVE_STDARG_H-1 != 0)')
            tools.mkdir("_build")
            with tools.chdir("_build"):
                if not tools.os_info.is_windows:
                    env_build = AutoToolsBuildEnvironment(self)
                    if self.settings.arch in ["x86", "x86_64", "broadwell"] and self.settings.compiler in ["clang", "gcc"]:
                        env_build.flags.append('-mstackrealign')

                        if self.settings.arch == "broadwell":
                            env_build.flags.append('-mavx2')

                    # configure passes CFLAGS to linker, should be LDFLAGS
                    tools.replace_in_file("../configure", "$LDSHARED $SFLAGS", "$LDSHARED $LDFLAGS")
                    # same thing in Makefile.in, when building tests/example executables
                    tools.replace_in_file("../Makefile.in", "$(CC) $(CFLAGS) -o", "$(CC) $(LDFLAGS) -o")

                    env_build_vars = env_build.vars

                    # we need to build only libraries without test example and minigzip
                    if self.options.shared:
                        make_target = "libz.so.%s" % self.version
                    else:
                        make_target = "libz.a"
                    env_build.configure("../", build=False, host=False, target=False, vars=env_build_vars)
                    env_build.make(target=make_target)
                else:
                    cmake = CMake(self)
                    self.output.info("sources %s" % self.source_folder)
                    self.output.info("build %s" % self.build_folder)
                    cmake.configure(source_folder=os.path.join(self.source_folder, self._source_subfolder), build_folder=os.getcwd())
                    # we need to build only libraries without test example/example64 and minigzip/minigzip64
                    if self.options.shared:
                        make_target = "zlib"
                    else:
                        make_target = "zlibstatic"
                    print(os.getcwd())
                    cmake.build(target=make_target)

    def package(self):
        self.output.warn("local cache: %s" % self.in_local_cache)
        self.output.warn("develop: %s" % self.develop)
        # Extract the License/s from the header to a file
        with tools.chdir(os.path.join(self.source_folder, self._source_subfolder )):
            tmp = tools.load("zlib.h")
            license_contents = tmp[2:tmp.find("*/", 1)]
            tools.save("LICENSE", license_contents)

        # Copy the license files
        self.copy("LICENSE", src=self._source_subfolder , dst="licenses")

        # Copy pc file
        self.copy("*.pc", dst="", keep_path=False)

        # Copy headers
        # HAP tweak: gzguts.h is supposed to be an internal header
        for header in ["*zlib.h", "*zconf.h", "gzguts.h"]:
            self.copy(pattern=header, dst="include", src=self._source_subfolder , keep_path=False)
            self.copy(pattern=header, dst="include", src="_build", keep_path=False)

        # Copying static and dynamic libs
        build_dir = os.path.join(self._source_subfolder , "_build")
        lib_path = os.path.join(self.package_folder, "lib")
        suffix = "d" if self.settings.build_type == "Debug" else ""
        if self.settings.os == "Windows":
            if self.options.shared:
                self.output.warning("Not tested, probably bugged...")
                build_dir = os.path.join(self._source_subfolder , "_build")
                self.copy(pattern="*.dll", dst="bin", src=build_dir, keep_path=False)
                build_dir = os.path.join(self._source_subfolder , "_build/lib")
                self.copy(pattern="*zlibd.lib", dst="lib", src=build_dir, keep_path=False)
                self.copy(pattern="*zlib.lib", dst="lib", src=build_dir, keep_path=False)
                self.copy(pattern="*zlib.dll.a", dst="lib", src=build_dir, keep_path=False)
                current_lib = os.path.join(lib_path, "zlib%s.lib" % suffix)
                os.rename(current_lib, os.path.join(lib_path, "zlib.lib"))
            else:
                build_dir = os.path.join(os.getcwd(), self._source_subfolder)
                build_dir = os.path.join(build_dir, "_build")
                build_dir = os.path.join(build_dir, str(self.settings.build_type))
                self.copy(pattern="zlibstaticd.lib", dst="lib", src=build_dir, keep_path=False)
                self.copy(pattern="zlibstatic.lib", dst="lib", src=build_dir, keep_path=False)
                current_lib = os.path.join(lib_path, "zlibstatic%s.lib" % suffix)
                os.rename(current_lib, os.path.join(lib_path, "zlib.lib"))
        else:
            if self.options.shared:
                self.copy(pattern="*.so*", dst="lib", src=build_dir, keep_path=False, symlinks=True)
            else:
                self.copy(pattern="*.a", dst="lib", src=build_dir, keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows" and not tools.os_info.is_linux:
            self.cpp_info.libs.append('zlib')
        else:
            self.cpp_info.libs.append('z')        
