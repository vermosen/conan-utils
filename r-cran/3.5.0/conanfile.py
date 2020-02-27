#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from conans import ConanFile, AutoToolsBuildEnvironment, tools

class RConan(ConanFile):
    name = 'r-cran'
    version = '3.5.0'
    description = 'the R statistical launguage.'
    license = 'Apache License Version 2.0'
    url = 'https://cran.r-project.org/src/base'
    homepage = 'https://cran.r-project.org'
    author = 'vermosen@yahoo.com'

    settings = 'os', 'compiler', 'build_type', 'arch', 'cppstd'

    options = { "shared": [True, False],
                "fPIC": [True, False],
                "Rshlib": [True, False] }

    default_options = {
        "shared": True ,
        "fPIC": True ,
        "Rshlib": True
    }
    
    generators = "cmake"
    _source_subfolder = 'src'

    # info: build with conan create . r-cran/3.5.0@jvermosen/stable --pr=gcc73 --build=missing -ks -o pcre:with_utf=True
    def configure(self):
        # from https://cran.r-project.org/doc/manuals/r-release/R-admin.html
        self.options["pcre"].with_utf = True
        self.options["prce"].with_jit = True
        self.options["prce"].with_unicode_properties = True
        self.options["pcre"].build_pcrecpp = False

    def build_requirements(self):
        self.build_requires("libcurl/7.64.1@%s/%s" % (self.user, self.channel))
        self.build_requires("bzip2/1.0.6@%s/%s" % (self.user, self.channel))
        self.build_requires("lzma/5.2.4@%s/%s" % (self.user, self.channel))
        self.build_requires("pcre/8.41.0@%s/%s" % (self.user, self.channel))
        self.build_requires("zlib/1.2.11@%s/%s" % (self.user, self.channel))

    def source(self):
        #https://cran.r-project.org/src/base/R-3/R-3.5.0.tar.gz
        v = self.version.split('.')
        path = '%s/R-%s' % (self.url, v[0])
        filename = 'R-%s.%s.%s.tar.gz' % (v[0], v[1], v[2])
        url = '%s/%s' % (path, filename)
        
        self.output.info('retrieving archive from %s' % url)
        tools.download(url, filename)
        tools.unzip(filename)
        shutil.move("R-%s" % (self.version), self._source_subfolder)
        
    def build(self):
        libcurl = self.deps_cpp_info["libcurl"].rootpath

        self.output.info('curl directory set to %s'% libcurl)
        self.build_dir = os.path.join(os.getcwd(), self._source_subfolder)
        with tools.chdir(self._source_subfolder):
            env_build = AutoToolsBuildEnvironment(self)
            env_build_vars = env_build.vars # edit here

            args = ['--with-readline=no', '--with-x=no']

            if self.options.Rshlib:
                args += ['--enable-R-shlib=yes']
            else:
                args += ['--enable-R-shlib=no']
            if self.options.shared:
                args += ['--enable-R-static-lib=no']
            else:
                args += ['--enable-R-static-lib=yes']

            env_build.fpic = self.options.fPIC
            env_build.configure(vars=env_build_vars, args=args)
            env_build.make()

    def package(self):
        self.build_dir = os.path.join(os.getcwd(), self._source_subfolder)
        with tools.chdir(self.build_dir):
            #need to manually install
            self.copy('*.h' , dst='include', src='src/include', keep_path=True)
            self.copy('*.so' , dst='lib', src='src/lib', keep_path=False)
            self.copy('*.a' , dst='lib', src='src/lib', keep_path=False)
            self.copy('*' , dst='bin', src='src/bin', keep_path=True)

    def package_info(self):
        self.env_info.libs = tools.collect_libs(self)
