from conans import ConanFile, tools, CMake
from conans.errors import ConanInvalidConfiguration
import os


class cpp11Conan(ConanFile):
    name = "cpp11"
    description = "cpp11 is a header-only R package that helps R package developers handle R objects with C++ code"
    topics = ("conan", "R")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/r-lib/cpp11/"
    license = ("MIT License",)
    generators = "cmake"
    settings = "os", "compiler", "arch"
    options = {}
    default_options = {}

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def config_options(self):
        pass

    def configure(self):
        pass

    def requirements(self):
        # for now on weskip this one
        #self.requires("r-cran/[>=4.0.3]@%s/%s" % (self.user, self.channel))
        pass

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "cpp11-{}".format(self.version)
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        pass

    def package(self):
        self.copy(pattern="*.hpp", dst="include", src='%s/inst/include' % self._source_subfolder)