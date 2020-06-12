#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from conans import ConanFile, tools

class RCppConan(ConanFile):
    name = 'rcpp'
    version = '1.0.4'
    description = 'the rcpp R-package.'
    license = 'Apache License Version 2.0'
    url = 'https://github.com/RcppCore/Rcpp'
    homepage = 'https://github.com/RcppCore/Rcpp'
    author = 'vermosen@yahoo.com'

    # header only - TODO: check on the compiler/abi
    #settings = 'os', 'compiler', 'arch', 'cppstd'

    generators = "cmake"
    _source_subfolder = 'src'

    def configure(self):
        pass

    def build_requirements(self):
        self.build_requires("r-cran/[>=3.5.0]@%s/%s" % (self.user, self.channel))
        pass

    def source(self):
        #https://github.com/RcppCore/Rcpp/archive/1.0.1.tar.gz
        # becomes Rcpp-1.0.1 folder
        archive = '%s.tar.gz' % self.version
        tools.download('%s/archive/%s' % (self.url, archive), '%s.tar.gz' % self.version)
        tools.unzip('%s.tar.gz' % self.version)
        folder = 'Rcpp-%s' % self.version
        shutil.move(folder, self._source_subfolder)
        
    def build(self):
        pass

    def package(self):
        self.copy('*.h' , dst='include/Rcpp', src='src/inst/include/Rcpp', keep_path=True)
        self.copy('*.hpp' , dst='include/Rcpp', src='src/inst/include/Rcpp', keep_path=True)
        self.copy('Rcpp.h', dst='include', src='src/inst/include')
        self.copy('RcppCommon.h', dst='include', src='src/inst/include')

    def package_info(self):
        self.env_info.libs = tools.collect_libs(self)
