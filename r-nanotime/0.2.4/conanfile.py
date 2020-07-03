import subprocess, os
from conans import ConanFile, CMake, tools


class SociConan(ConanFile):
    name = "r-nanotime"
    description = """Nanosecond Time Resolution for R"""
    version = "0.2.4"
    license = "GNU GENERAL PUBLIC LICENSE - version 2, June 1991"
    url = "https://github.com/eddelbuettel/nanotime"
    settings = "os", "compiler", "build_type", "arch"

    generators = "cmake"
    _source_subfolder = 'source'


    def build_requirements(self):
        self.build_requires("r-cran/[>=3.5.0]@%s/%s" % (self.user, self.channel))
        self.build_requires("cctz/[>=2.3]@%s/%s" % (self.user, self.channel))
            
    def source(self):
        tools.download(
            "https://github.com/eddelbuettel/nanotime/archive/master.tar.gz",
            "archive.tar.gz")
        tools.unzip("archive.tar.gz", ".")
        os.rename("nanotime-master", self._source_subfolder)

    def build(self):
        # TODO ? useful ?
        pass

    def package(self):
        self.copy("*.h", dst="include/nanotime", src="source/inst/include")
        self.copy("*.hpp", dst="include/nanotime", src="source/inst/include")

    def package_info(self):
        pass
