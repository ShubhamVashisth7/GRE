#include "./benchmark.h"

int main(int argc, char **argv) {
    Benchmark <uint64_t, std::string> bench;
    bench.parse_args(argc, argv);
    bench.run_benchmark();
}

