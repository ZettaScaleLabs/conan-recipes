#include <cstdlib>
#include <iostream>
#include "zenoh.hxx"
using namespace zenoh;

int main(int argc, char **argv) {
    (void)argc;
    (void)argv;

    Config config;
#ifdef ZENOHCXX_ZENOHC
    if (!config.insert_json(Z_CONFIG_LISTEN_KEY, "[\"tcp/0.0.0.0:7447\"]")) {
#elif ZENOHCXX_ZENOHPICO
        if (!config.insert(Z_CONFIG_CONNECT_KEY, locator))
#else
#error "Unknown zenoh backend"
#endif
        std::cout << "Failed to insert config";
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
