# Notice of deprecation

This repository is no longer actively maintained.

# Conan Recipes

This repo regroups [conan](https://conan.io/) recipes for Zenoh C/CPP bindings and implementations: [Zenoh-C](https://github.com/eclipse-zenoh/zenoh-c), [Zenoh-CPP](https://github.com/eclipse-zenoh/zenoh-cpp) and [Zenoh-Pico](https://github.com/eclipse-zenoh/zenoh-pico).

All Zenoh Conan recipes are maintained in this repository. They will be updated with new Zenoh releases as they come, as well as some new features depending on identified use-cases. **Always use the latest commit from the main branch**.

## Recipes in this repo

- zenoh-c: Builds Zenoh-C from source. Requires Rust Toolchain preinstalled on the target system in order to compile the library.
- zenoh-c-prebuilt: Pulls the Zenoh-C pre-compiled release artefacts for the target system (if supported in the release). Does not require Rust Toolchain.
- zenoh-pico: Builds Zenoh-Pico from source.
- zenoh-cpp: Installs the Zenoh-CPP header-library. Depending on which backend library to be used, installation will require one of Zenoh-Pico or Zenoh-C Conan packages to be installed beforehand.

## Installation

Building the recipes requires Conan. Please visit the official Conan website for installation instructions.

Below are examples for building `zenoh-c 0.10.1-rc` with different versions of Conan. In case of issues with a dependency's installation (namely CMake), add the `--build=missing` parameter to the command (or `--build missing` on v1).

### Using Conan v2

```shell
conan create zenoh-c/all/conanfile.py --version 0.10.1-rc
```

### Using Conan v1

```shell
conan create zenoh-c/all/conanfile.py zenohc/0.10.1-rc@eclipse-zenoh/release
```

## Usage

To use the installed Zenoh project in your Conan package, you first need to add it to your recipe's `requirements` function. Below is an example to add `zenoh-c 0.10.1-rc` as a dependency.

```python
from conan import ConanFile
# other imports

class MyPackage(ConanFile):
    
    # other conan recipe attributes and functions
    
    def requirements(self):
        self.requires("zenohc/0.10.1-rc")

    # rest of the recipe
```

It is also possible to configure options for the dependency. For more details, please refer to the offical Conan documentation for the respective version you are using, or read further below for an example with Zenoh-CPP.

**Note:** Depending on the project you wish to use, you will probably also need to setup a `CMakeLists` file for your package. Please refer to the recipe's respective `test_package/CMakeLists.txt` for a basic template.

## Specifying a backend for Zenoh-CPP

Depending on which backend you choose between zenoh-c and zenoh-pico, you will have to install the library through its respective Conan recipe. Make sure the installed version matches exactly with the Zenoh-CPP version you wish to install. Finally, update the `ZENOH_LIB` option in the `requirements` function of your package's recipe (default value is `zenohc`).

```python
    def requirements(self):
        self.requires("zenohcpp/0.10.1-rc", options={"ZENOH_LIB":"zenohpico"})
```
