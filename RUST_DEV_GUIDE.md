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
you are running linux (even then there are some caveats). The best way to test coverage is usually to just push the code and let Travis build it. Note that cargo on travis is cached because it takes forever to compile tarpaulin - if something breaks, maybe it just needs updating - delete cache. Also, if your project requires `nightly` compiler, remove `stable` and `beta` targets from `.travis.yml`. Currently, this will disable code coverage (it only runs on stable). You can try to enable it on nightly as well at your own risk, just make sure it is enable only for one of the three targets at a time (to avoid duplicate uploads).

### `shields_up` flag

There is a special feature which you can use to enable additional pre/post
condition checks. It is on by default, so make sure to disable it when
running benchmarks or public releases. Internal releases should probably
have `shields_up` enabled since they are often used to test and expose problems.

Remember that performance impact of `shields_up` does not have to be very
big - depends on the task. But it can also be significant, so if the code is 
taking a really long time to run, you can also try a build where the feature 
is disabled (assuming you trust the code).



