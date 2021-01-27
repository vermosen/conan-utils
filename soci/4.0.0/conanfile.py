import subprocess
from conans import ConanFile, CMake, tools


class SociConan(ConanFile):
    name = "soci"
    description = """SOCI is a database access library for C++ that makes the illusion
    of embedding SQL queries in the regular C++ code, staying entirely
    within the Standard C++."""
    version = "4.0.0"
    license = "Boost Software License - Version 1.0"
    url = "https://github.com/laeknaromur/conan-soci"
    settings = "os", "compiler", "build_type", "arch", "cppstd"

    # note: LTO option will be enabled only in 4.0.2
    options = {"lto": [True, False],
               "fPIC": [True, False],
               "shared": [True, False],
               "with_db2": [True, False],
               "with_firebird": [True, False],
               "with_mysql": [True, False],
               "with_odbc": [True, False],
               "with_oracle": [True, False],
               "with_postgresql": [True, False],
               "with_sqlite3": [True, False],
               "with_system_boost": [True, False]
               }
    
    default_options = "lto=False", "fPIC=True", \
        "shared=False", "with_db2=False", "with_firebird=False",\
        "with_mysql=False", "with_odbc=False", "with_oracle=False",\
        "with_postgresql=False", "with_sqlite3=False", "with_system_boost=False"
    generators = "cmake"
    build_dir = "./"

    def requirements(self):

        if self.options.with_sqlite3:
            self.requires("sqlite3/[>3.29.0]@%s/%s" % (self.user, self.channel))

        if self.options.with_system_boost:
            pass
        else:
            self.requires("boost/[>1.71.0]@%s/%s" % (self.user, self.channel))
            
    def source(self):

        tools.download(
            "https://github.com/SOCI/soci/archive/{}.tar.gz".format(self.version),
            "source.tar.gz")
        tools.unzip("source.tar.gz", ".")
        tools.replace_in_file("soci-{}/CMakeLists.txt".format(self.version),
                              "project(SOCI)", '''project(SOCI)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)

        # not sure the gnuXX flags would be handled here...
        cmake.definitions["CMAKE_CXX_STANDARD"] = self.settings.cppstd
        
        cmake.definitions["WITH_DB2"] = "ON" if self.options.with_db2 else "OFF"
        cmake.definitions["WITH_FIREBIRD"] = "ON" if self.options.with_firebird else "OFF"
        cmake.definitions["WITH_MYSQL"] = "ON" if self.options.with_mysql else "OFF"
        cmake.definitions["WITH_ODBC"] = "ON" if self.options.with_odbc else "OFF"
        cmake.definitions["WITH_ORACLE"] = "ON" if self.options.with_oracle else "OFF"
        cmake.definitions["WITH_POSTGRESQL"] = "ON" if self.options.with_postgresql else "OFF"

        # boost
        if self.options.with_system_boost:
            pass
        else:
            cmake.definitions["BOOST_INCLUDEDIR"] = self.deps_cpp_info["boost"].include_paths[0]
            cmake.definitions["BOOST_LIBRARYDIR"] = self.deps_cpp_info["boost"].lib_paths[0]
        
        if self.options.with_sqlite3:
            self.output.info("adding dependency to %s and %s" % (self.deps_cpp_info["sqlite3"].include_paths[0], self.deps_cpp_info["sqlite3"].lib_paths[0]))
            cmake.definitions["WITH_SQLITE3"] = "ON"
            cmake.definitions["SQLITE3_INCLUDE_DIR"] = self.deps_cpp_info["sqlite3"].include_paths[0]
            cmake.definitions["SQLITE3_LIBRARIES"] = "%s/libsqlite3.a" % self.deps_cpp_info["sqlite3"].lib_paths[0]
        else:
            cmake.definitions["WITH_SQLITE3"] = "OFF"

        # shared/static
        cmake.definitions["SOCI_SHARED"] = "ON" if self.options.shared else "OFF"
        cmake.definitions["SOCI_STATIC"] = "OFF" if self.options.shared else "ON"

        # build type
        cmake.definitions["CMAKE_BUILD_TYPE"] = self.settings.build_type
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "{}/install".format(self.build_dir)

        # enable lto (TODO: check on version)
        cmake.definitions["SOCI_LTO"] = "ON" if self.options.lto else "OFF"

        # PIC
        cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = "ON" if self.options.fPIC else "OFF" 


        cmake.configure(source_dir="soci-{}".format(self.version),
                        build_dir=self.build_dir)
        cmake.build(target="install")

    def package(self):
        self.copy("*.h", dst="include", src="install/include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so.*", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = ["include", "include/soci"]
        self.cpp_info.libs = ["soci_core",
                              "soci_empty"]

        if self.settings.os != "Windows":
            self.cpp_info.libs.append("dl")

        if self.options.with_db2:
            self.cpp_info.libs.append("soci_db2")

        if self.options.with_firebird:
            self.cpp_info.libs.append("soci_firebird")

        if self.options.with_mysql:
            self.cpp_info.libs.append("soci_mysql")

        if self.options.with_odbc:
            self.cpp_info.libs.append("soci_odbc")

        if self.options.with_oracle:
            self.cpp_info.libs.append("soci_oracle")

        if self.options.with_postgresql:
            self.output.info("Using system-wide PostgreSQL")
            libpq_cflags = subprocess.check_output(
                ["pkg-config", "--cflags", "libpq"]).strip().decode("utf-8")
            self.cpp_info.includedirs.append(libpq_cflags[2:])
            self.cpp_info.libs.append("soci_postgresql")
            self.cpp_info.libs.append("pq")

        if self.options.with_sqlite3:
            self.cpp_info.libs.insert(0, "soci_sqlite3")

    def system_requirements(self):
        pack_names = []
        if tools.os_info.is_linux and self.options.with_postgresql:
            pack_names.append("libpq-dev")

        if pack_names:
            installer = tools.SystemPackageTool()
            installer.install(pack_names)
