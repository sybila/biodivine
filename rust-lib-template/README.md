## Biodivine Library Template

This is a template project for a general Rust based Biodivine library. It comes with a few useful features pre-enabled. 

Provided features:
 - Travis integration pre-configured with Codecov code coverage.
 - `LICENSE` and `.gitignore` files.
 - Run `cargo make rich-doc` and `cargo make rich-doc-dev` to generate documentation with Mermaid and KaTeX enabled (`dev` variant includes also internal functions).
 - Run `cargo make` to run standard test process and compile basic docs, but also run automatic formatting tool of source code (make sure you apply formatting every time before commit).
 - There is a `shields_up` feature flag that can be used to include extra safety checks (invariants, pre-/post-conditions) that should not be needed but may be useful for testing. For usage examples, see the Biodivine Rust developer guide. The flag is off by default, but is enabled during tests on Travis. We provide variants of basic commands with the 
 
To fully initialize the template, perform the following steps:

 - In `Cargo.toml`, specify package name, author, dependencies (if needed, use dev-dependencies for dependencies used only for tests).
 - Enable continuous builds on Travis and code coverage on Codecov. Remember to set Codecov token environment variable to enable coverage reports.
 - Rewrite this readme :) 