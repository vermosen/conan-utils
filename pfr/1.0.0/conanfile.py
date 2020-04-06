# The MIT License (MIT)
#
# Copyright (c) 2017 Mateusz Pusz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from conans import ConanFile, CMake, tools

class GoogleBenchmarkConan(ConanFile):
    name = "pfr"
    version = "1.0.0"
    description = "Precise and Flat Reflection"
    homepage = "https://github.com/apolukhin/magic_get"
    url = "https://github.com/apolukhin/magic_get"
    exports_sources = "include/*"
    no_copy_source = True
    
    scm = {
        "type": "git",
        "url": "https://github.com/apolukhin/magic_get.git",
        "revision": "%s" % version,
    }

    def source(self):
        pass

    def build(self):
        pass

    def package(self):
        self.copy("*.hpp", dst="include", src="include", keep_path=True)

    def package_info(self):
        pass

    def package_id(self):
        self.info.header_only()
