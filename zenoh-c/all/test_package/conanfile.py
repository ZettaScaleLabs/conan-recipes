import os
from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.build import can_run


class ZenohCPackageTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain", "VirtualRunEnv"
    test_type = "explicit"

    def build_requirements(self):
        self.tool_requires("cmake/[>=3.16 <4]")

    def requirements(self):
        self.requires(self.tested_reference_str)

    def layout(self):
        cmake_layout(self)

    def configure(self):
        self.settings.rm_safe("compiler.cppstd")
        self.settings.rm_safe("compiler.libcxx")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if can_run(self):
            cmd = os.path.join(self.cpp.build.bindir, "test_package")
            self.run(cmd, env="conanrun")