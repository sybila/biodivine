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

### WASM support

TBD;

## Conventions

All conventions are meant to be followed except when they are not:

 - Make sure privete/internal functions are also documented. Publish developer docs as well as official docs (for example to `biodivine.fi.muni.cz/docs`). Always write why the thing is implemented the way it is implemented rather than what it is doing. Use `**(internal)**` when documenting private/internal items so in the dev docs it is clear these are not public.
 
 - Prefer longer, self contained module descriptions (ideally with usage example) instead of spreading the information accross the whole API of the module/struct/etc. This will enable us to quickly catch up to what the component is actually doing and how it should be used. Bottom line: If the method docs are more than one paragraph, they should probably be part of the module documentation instead.
 
 - Make parent modules as simple as possible. For example, declare a struct in the root module, but create a separate sub-module where you actually implement the methods of that struct or test the functionality (if the tests are complex). The goal is to make sure you can understand the "data layout" (structs) of each module by opening the root directory and its functionality by going through the names of the submodules. Also, the main part of the documentation should be in the root module, so that is why we keep it as clean as possible (so that the overview docs do not obscure the code). Use the following naming conventions for such modules:

   * `impl_<my_struct>`: general implementation of a struct. If the implementation is still too long, you can split it into more submodules named according to the functionality they provide.  
   * `impl_<trait_name>_<my_struct>`: implementation of a trait for a struct (can be included in `impl_` module if it is simple enough, but for larger implementations, for example with helper function, definitely split it into separate submodule). If the trait is generic (e.g. `TryFrom`), you can also include the specific variant you are implementing, for example `impl_try_from_string_my_custom_collection`. If you have a structured `impl_` module, you can add it as a submodule as well.
   * `macro_<my_macro>`: declaration of a macro.
   * `test_<my_test>`: a test-only module that implements specific type of test. You can also use `test_<my_struct>` if you have a lot of tests for a specific struct.
   * `fun_<my_function>`: if all you need to provide is a function, but a complex one, please also separate it into a special module (very small/simple functions can be part of the root module).

 - Remebmer that integration tests should go into the `tests` directory (each is a separate crate).
 
 - You can also document different `impl` blocks to describe the functionality that is provided in these blocks.
 
 - Adding explicit tutorials into docs is quite cumbersome. To avoid this, create a special `tutorial` module with no code and make each submodule there a tutorial article. Use module-level docs to write the tutorials.
 
 - Remember that you can scope things as `pub(crate)` or `pub(super)` if you need to share some internal implementation aspects. Just don't overuse this.
 
 - If you are using something like locks or mutexes, prefer non-blocking functions (or at least provide non blocking variants). If the function can block (especially for some non-trivial amount of time), add a `_blocking` suffix to its name. For example, for getting data guarded by a mutex, I should have two options: `let r: Option<T> = data.get(...)` or `let r: T = data.get_blocking(...)` (`Option` can be also a `Result` if there can be other reasons why the method failed). 
 
 - Passing by value/reference: In general, if something implements Copy, default decision should be to pass it by value. In case of a non-copy struct, use pass by reference. Of course, sometimes pass by reference is necessary for Copy types as well, but in general, by implementing Copy, you indicate that this type should be treated as "atomic" value. Also, please make sure to implement Copy only for types where this is reasonable - small, flat types.

## Publishing

To use project internally, you don't have to publish it anywhere, cargo can import dependencies from git: `my-lib = { git = "https://url.to/my-lib.git" }`. However, once the library reaches certain level of maturity, it is recommended to also publish it to `crates.io`. When publishing, please make sure to follow these steps:

 - Make sure everything is properly tested (coverage) and continuous integration does not fail.
 - Consider these conventions as well as `https://rust-lang.github.io/api-guidelines/`.
 - Create a github release with an appropriate version tag.
 - Generate developer documentation, make sure everything is documented and that there are some tutorials to cover the most important functionality. Publish the developer docs to `biodivine.fi.muni.cz/docs/my-lib/<version_tag>/...`. 
 - See `https://doc.rust-lang.org/cargo/reference/publishing.html` for details on how to create and publish the artefact.  