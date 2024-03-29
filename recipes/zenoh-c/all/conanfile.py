from conan import ConanFile
from conan.tools.files import apply_conandata_patches, get, copy, export_conandata_patches, rm, rmdir
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout, CMakeDeps
import os

required_conan_version = ">=1.53.0"

class ZenohCPackageConan(ConanFile):
    name = "zenohc"
    version = "0.10.1-rc"
    description = "Recipe to build zenoh-c with conan"    
    license = "Apache License 2.0"
    author = "ZettaScale Zenoh Team"

    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/eclipse-zenoh/zenoh-c"

    package_type = "library"
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "ZENOHC_BUILD_WITH_LOGGER_AUTOINIT":[True, False],
        "ZENOHC_BUILD_WITH_SHARED_MEMORY":[True, False],
        "ZENOHC_CARGO_CHANNEL":["stable", "nightly"],
        "ZENOHC_CARGO_FLAGS": ["ANY"],
    }

    default_options = {
        "shared": False,
        "fPIC": True,
        "ZENOHC_BUILD_WITH_LOGGER_AUTOINIT": True,
        "ZENOHC_BUILD_WITH_SHARED_MEMORY": True,
        "ZENOHC_CARGO_CHANNEL": "stable",
        "ZENOHC_CARGO_FLAGS": "",
    }

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        self.settings.rm_safe("compiler.cppstd")
        self.settings.rm_safe("compiler.libcxx")

    def layout(self):
        cmake_layout(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)            
        for opt, val in self.options.items():
            tc.variables[opt] = val
        tc.variables["ZENOHC_LIB_STATIC"] = "True" if tc.variables["shared"] == "False" else "False"
    
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE", self.source_folder, os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))
        rmdir(self, os.path.join(self.package_folder, "share"))
        rm(self, "*.la", os.path.join(self.package_folder, "lib"))
        rm(self, "*.pdb", os.path.join(self.package_folder, "lib"))
        rm(self, "*.pdb", os.path.join(self.package_folder, "bin"))

    def package_info(self):
        if self.settings.build_type == "Debug":
            self.cpp_info.libs = ["zenohcd"]
        else:
            self.cpp_info.libs = ["zenohc"]
