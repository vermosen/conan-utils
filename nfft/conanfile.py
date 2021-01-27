import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration

class nfftConan(ConanFile):
    name = "nfft"
    url = "https://github.com/NFFT/nfft"
    homepage = "https://www-user.tu-chemnitz.de/~potts/nfft/"
    description = "The NFFT is a C subroutine library for computing the nonequispaced discrete Fourier transform (NDFT) in one or more dimensions, of arbitrary input size, and of complex data"
    topics = ("conan", "nfft", "fft", "signal")
    license = "Apache-2.0"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"

    options = { "fPIC": [True, False], "shared": [True, False] }
    default_options = { "fPIC": True, "shared": False }

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        self.requires("fftw/3.3.8@%s/%s" % (self.user, self.channel))

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)
        tools.mkdir(self._build_subfolder)
    
    def build(self):
        with tools.chdir(self._source_subfolder):
            self.output.info('cwd: %s' % os.getcwd())
            self.run('./bootstrap.sh')

        with tools.chdir(self._build_subfolder):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(configure_dir='../%s' % self._source_subfolder)
            autotools.make()
            autotools.install()
            
    def package(self):
        pass
    
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
