# Rust Biodivine Developer Guide

Here, you can quickly learn what conventions should be used to implement Biodivine libraries in Rust. This document contains a `Technology` section which describes what tools/techniques should/can be used/considered when implementing the library. Then there is the `Conventions` section which lists some additional considerations about structuring and naming source code. Finally, there is a `Publishing` section which describes how to publish releases of Rust libraries and executables.

This repository contains a `rust-lib-template` that you can use to quickly initialize a library repository with a functioning project.

## Technology

### Cargo `make`

A lot of useful functionality is provided by [Cargo `make`](https://github.com/sagiegurari/cargo-make). Make sure you have it installed and up to date. Before each commit, make sure you run `cargo make`. This will run an automated formatter that will make the source code more readable. It also facilitates other nice features, like the rich documentation generator.

### Rich Documentation

The template project is set up to enable KaTeX (math) and Mermaid (markdown for diagrams) in documentation. Use `cargo make rich-doc` or `cargo make rich-doc-dev` to generate documentation (rich documentation should be also automatically enabled when using `docs.rs` to publish docs). To use KaTeX, wrap your math in $ ... $ or $$ ... $$ for block expressions. For mermaid, just use a code block with language set to mermaid (write mermaid after the initial \`\`\`).

### Code Coverage and CI

The template project is set up to use Travise and Codecov (via tarpaulin) to measure test code coverage. Tarpaulin is not cross platform so you probably can't use it locally unless 
you are running linux (even then there are some caveats). The best way to test coverage is usually to just push the code and let Travis build it. Note that cargo on travis is cached because it takes forever to compile tarpaulin - if something breaks, maybe it just needs updating - delete cache. Also, if your project requires `nightly` compiler, remove `stable` and `beta` targets from `.travis.yml`. Currently, this will disable code coverage (it only runs on stable). You can try to enable it on nightly as well at your own risk, just make sure it is enabled only for one of the three targets at a time (to avoid duplicate uploads).

### `shields_up` flag

Sometimes, you want to enable additional safety measures (like bounds check, invariant assertions, etc.) which should not be needed if the contract of your API is not violated. In production code, these measures can be disabled (since the production release should be well tested... right?!). We use a special feature called `shields_up` to enable such checks. Travis build script is automatically set up to run tests (and code coverage) with these checks. However, the feature is not enabled by default (so that dependent crates do not suffer the performance penalty by default). If you want to run with `shields_up` locally, add `--features shields_up` to the cargo command. There are also some aliases set up using cargo make to enable this (`cargo make build-release-safe`, `cargo make build-safe`, `cargo make test-safe`).

To use `shields_up` in your code, you can use `cfg` macro to conditionally include some code:

```rust
pub fn division(a: usize, b: usize) -> usize {
	if cfg!(shields_up) && b == 0 {	// a conditional code
		panic!("Dividion by zero.");
	}
	return a / b;
}

#[cfg(feature = "shields_up")]		// a conditional function
pub fn only_when_shields_up() {
	...
}
```

### Benchmarking and Profiling

Benchmarking in Rust currently requires a nightly compiler, so it is advised to keep benchmarks in a separate branch of the repository. In the readme of such branch, you should keep track of what benchmarks you are running (and why) as well as provide some reference results to compare with in the future. Of course, you can also use standard `time` utility and benchmark a separate binary. To create a new binary target in your library, add a Rust source file into the `./src/bin/` folder. This will create a binary target module for that file. 

Please make benchmarks as self-contained as possible. Ideally, each benchmark should have its own module. Also, if the benchmarks run for a long time, it might be useful to split them into smaller and larger benchmarks, using some kind of feature (as in `shilds_up`).

Before optimizing anything, it is best to first profile your application to ensure you are truly optimizing the hot spots in your code. For a nice Rust profiling helper utility on MacOS, see [Cargo Instruments](https://crates.io/crates/cargo-instruments). Another nice crate (multi platform even!) for visualising hot spots is [Flame Graph](https://github.com/ferrous-systems/flamegraph). You typically cannot use these tools on the `cargo bench` target directly, it is usually necessary to create a custom binary as described above.

Sometimes when doing micro-optimisations, it is also beneficial to see the actual assembly your code will compile to (however, this typically requires some well isolated instances of code). To quickly explore compiled code, see [Compiler Explorer](https://godbolt.org). However, remember to add the optimization flag `-O` to the compiler and make sure you consume the output values to ensure the whole benchmark is not just evaluated by the compiler.

