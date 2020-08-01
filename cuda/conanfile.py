import os
from conans import ConanFile, CMake, tools

class ConanCuda(ConanFile):
    name = "cuda"
    description = ""
    url = ""
    homepage = ""
    topics = ("conan", "cuda")
    license = ""
    generators = "cmake"
    settings = "os", "compiler", "arch", "build_type"

    options = {}
    
    default_options = {}

    def configure(self):

        v = tools.Version(self.version)
        if self.settings.compiler == "gcc":

            if v == tools.Version("11.0"):
                
                if self.settings.compiler.version >= tools.Version("10.0"):
                    # version not handled
                    raise 
            elif v == "10.1":

                if self.settings.compiler.version >= tools.Version("9.0"):
                    raise


    def source(self):
        url = self.conan_data["sources"][self.version]["url"]
        archive_name = os.path.basename(url)
        archive_name = os.path.splitext(archive_name)[0]
        sha = self.conan_data["sources"][self.version]["sha256"]
        tools.download(url, archive_name, sha256=sha)

    def build(self):
        return

    def package(self):
        self.output.info('target folder is %s' % self.package_folder)

        if self.settings.os != "Windows":
            url = self.conan_data["sources"][self.version]["url"]
            archive_name = os.path.basename(url)
            archive_name = os.path.splitext(archive_name)[0]

            #  sh ${CUDA_ARCHIVE} --silent --toolkit --toolkitpath=${ARG_PREFIX}
            self.run("sh %s --silent --toolkit --toolkitpath=%s" % (archive_name, self.package_folder))
        
    def package_info(self):
        return
        #self.cpp_info.libs = tools.collect_libs(self)
        #if self.settings.os == "Linux":
        #    if self.options.threadsafe:
        #        self.cpp_info.system_libs.append("pthread")
        #    if not self.options.omit_load_extension:
        #        self.cpp_info.system_libs.append("dl")
        #if self.options.build_executable:
        #    bin_path = os.path.join(self.package_folder, "bin")
        #    self.output.info("Appending PATH env var with : {}".format(bin_path))
        #    self.env_info.PATH.append(bin_path)

        #self.cpp_info.names["cmake_find_package"] = "SQLite3"
        #self.cpp_info.names["cmake_find_package_multi"] = "SQLite3"
