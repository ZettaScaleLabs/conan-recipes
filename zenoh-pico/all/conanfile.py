from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import apply_conandata_patches, get, copy, export_conandata_patches
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout, CMakeDeps
import os

required_conan_version = ">=1.53.0"

class ZenohPicoPackageConan(ConanFile):
    name = "zenohpico"
    description = "Eclipse zenoh for pico devices: Zero Overhead Pub/sub, Store/Query and Compute protocol"
    tags = ["iot", "networking", "robotics", "messaging", "ros2", "edge-computing", "micro-controller"]
    license = "EPL-2.0 OR Apache-2.0"
    author = "ZettaScale Zenoh Team <zenoh@zettascale.tech>"

    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/eclipse-zenoh/zenoh-pico"

    package_type = "library"
    settings = "os", "compiler", "build_type", "arch"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],

        "WITH_ZEPHYR": [True, False],
        "WITH_FREERTOS_PLUS_TCP": [True, False],
        "ZENOH_DEBUG": ["ANY"],
        "FRAG_MAX_SIZE": ["ANY"],
        "BATCH_UNICAST_SIZE": ["ANY"],

        "Z_FEATURE_PUBLICATION": ["0", "1"],
        "Z_FEATURE_SUBSCRIPTION": ["0", "1"],
        "Z_FEATURE_QUERY": ["0", "1"],
        "Z_FEATURE_QUERYABLE": ["0", "1"],
        "Z_FEATURE_RAWETH_TRANSPORT": ["0", "1"],
    }

    default_options = {
        "shared": False,
        "fPIC": True,

        "WITH_ZEPHYR": False,
        "WITH_FREERTOS_PLUS_TCP": False,
        "ZENOH_DEBUG": "0",
        "FRAG_MAX_SIZE": "0",
        "BATCH_UNICAST_SIZE": "0",

        "Z_FEATURE_PUBLICATION": "1",
        "Z_FEATURE_SUBSCRIPTION": "1",
        "Z_FEATURE_QUERY": "1",
        "Z_FEATURE_QUERYABLE": "1",
        "Z_FEATURE_RAWETH_TRANSPORT": "0",
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

    def validate(self):
        pass

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.13 <4]")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        for opt, val in self.options.items():
            tc.variables[opt] = val
        tc.variables["BUILD_SHARED_LIBS"] = str(self.options.shared)
        # disable packaging, building examples, tools and tests
        tc.variables["PACKAGING"] = "False"
        tc.variables["BUILD_EXAMPLES"] = "False"
        tc.variables["BUILD_TOOLS"] = "False"
        tc.variables["BUILD_TESTING"] = "False"
        tc.variables["BUILD_INTEGRATION"] = "False"
        
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

    def package_info(self):
        self.cpp_info.libs = ["zenohpico"]
        
        self.cpp_info.set_property("cmake_file_name", "zenohpico")
        self.cpp_info.set_property("cmake_target_name", "zenohpico")

        # if self.settings.os == "Windows":
        #     self.cpp_info.system_libs = ["ws2_32", "crypt32", "secur32", "bcrypt", "ncrypt", "userenv", "ntdll", "iphlpapi", "runtimeobject"]
        # elif self.settings.os == "Linux":
        #     self.cpp_info.system_libs = ["rt", "pthread", "m", "dl"]
        # elif self.settings.os == "Macos":
        #     self.cpp_info.frameworks = ["Foundation", "Security"]
