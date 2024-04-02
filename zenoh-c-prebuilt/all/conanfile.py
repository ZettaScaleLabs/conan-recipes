from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import copy, get
import os

required_conan_version = ">=1.53.0"

class ZenohCPackageConan(ConanFile):
    name = "zenohc"
    version = "0.10.1-rc"
    description = "C-API for Eclipse Zenoh: Zero Overhead Pub/Sub, Store/Query and Compute protocol"
    tags = ["iot", "networking", "robotics", "messaging", "ros2", "edge-computing", "micro-controller", "pre-built"]
    license = "Apache License 2.0"
    author = "ZettaScale Zenoh Team"

    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/eclipse-zenoh/zenoh-c"

    package_type = "library"
    settings = "os", "compiler", "build_type", "arch"

    @property
    def _supported_platforms(self):
        return [
            ("Windows", "x86_64"),
            ("Linux", "x86_64"),
            ("Linux", "armv6"),
            ("Linux", "armv7hf"),
            ("Linux", "armv8"),
            ("Macos", "x86_64"),
            ("Macos", "armv8"),
        ]

    def layout(self):
        pass

    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.build_type

    def validate(self):
        if (self.settings.os, self.settings.arch) not in self._supported_platforms:
            raise ConanInvalidConfiguration("{}/{} target is not supported".format(self.settings.os, self.settings.arch))

    def source(self):
        pass

    def build(self):
        if self.settings.os == "Windows" and self.settings.compiler == "msvc":
            get(
                self,
                **self.conan_data["sources"][self.version][str(self.settings.os)]["{}_msvc".format(str(self.settings.arch))],
                strip_root=True,
            )
        else:
            get(
                self,
                **self.conan_data["sources"][self.version][str(self.settings.os)][str(self.settings.arch)],
                strip_root=True,
            )

    def package(self):
        copy(self, "LICENSE", self.source_folder, os.path.join(self.package_folder, "licenses"))
        copy(self, "lib/", self.source_folder, self.package_folder)
        copy(self, "include/", self.source_folder, self.package_folder)

    def package_info(self):
        self.cpp_info.libs = ["zenohc"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]
