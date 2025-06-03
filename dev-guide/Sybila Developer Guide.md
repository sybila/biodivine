# Sybila Developer Guide

This document outlines some general recommendations towards developing *new* projects (old projects will be updated whenever possible, but it is a low priority task). This is not a *law*; use rational judgement to decide if these rules work for you. With that said, you should probably consult with the senior staff if you are going to diverge significantly. Also, most of this is general, but some of it applies to Rust only. We will probably split this up in the future into multiple documents.

The recommendations are not presented in any particular order. Some are more general "software quality" rules, some are rather Rust specific.

### Git

**[GIT 01] Use the right software** There is no point in flexing your CLI skills if it makes you unproductive, or worse yet, makes you skip useful code quality measures because they are hard to do from command line. If you are not already *very* comfortable with git, it is recommended to download [Sublime Merge](https://www.sublimemerge.com/) and use it. It does not provide any "special" functionality. Everything translates into existing git commands. It's just much easier to do complex stuff in it. Some notable things that you can easily do that's much more tiresome using CLI:

* Commit only a specific line of code among many existing code changes.
* Edit a commit message of an existing commit.
* Reset a branch to a specific commit while either (a) keeping everything as uncommited changes or (b) removing everything.
* Stash current changes to a temporary storage area without commiting them (e.g. while switching to another branch or performing some other unrelated change).

Importantly, *you cannot delete code that is already pushed unless you are using force push (see below), so don't be afraid to experiment and learn*. If you are not sure and fear losing local changes, make another copy of the repository to test the operation first.

Another useful hint; Github has a built-in diff tool that can be used to compare any two branches/tags/commits. You can access it by adding `/compare/` to the repository URL (e.g. `https://github.com/sybila/biodivine-lib-sbml/compare/`). 

**[GIT 02] Commit and push often, even unfinished work** Make sure you have a git repository set up from the very beginning. Push work into said repository, *at the very least whenever you are done for the day*. Nobody is going to judge you based on some unfinished work (or typically even read it). Why we need to do it: (a) if your machine dies, that unfinished work dies with it; (b) if you are stuck, someone can come in and help right away, without waiting for you to get everything up and running; (c) it gives a clear sense of progress in case we run into issues later. This holds even if you are starting a new project, prototyping or working on something that noone else is expected to use. *If you don't have the rights to create a new repository or change some necessary settings on Github, contact senior staff.*

**[GIT 03] On commits** Currently, *we do not enforce a particular commit standard*. However, it is strongly recommended to use [Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) at least on already established projects, because it allows us to generate changelogs semi-automatically. Personally, the author prefers whole sentences as commit messages, but this is not required. Also, notice that you can use backticks in commit messages and most tools will render this correctly as code (the same way markdown does).

Overall, make sure to at least use the following conventions:

```
--- 
	This is a fix commit message. Use these for changes 
	that change code behavior, but do not add new functionality.
---
fix: Some description of what was fixed. Possibly longer text consisting of multiple sentences.

---
	This is a feature commit message. Use these to indicate
	that the change adds new functionality or significantly alters
	the behavior of an existing functionality in a backwards
	compatible way.
---
feat: Some description of what was added. Possibly longer text consisting of multiple sentences.

---
	If the commit introduces breaking changes (removal/change
	of existing public API), it needs to be marked with `!`.
	In such case, both `fix` and `feat` are valid, depending
	on the nature of the change.
	
	If the change is complex, it is recommended to add a footer
	with `BREAKING CHANGE:` to describe the breakage.
---
fix!: Resolves issues with variable naming.

BREAKING CHANGE: Having `$` in variable names breaks compatibility with PHP. The supported variable format was updated to exclude `$`.

---
	Other types of message prefixes that you can use:
---
build: Something changed in the project configuration or CI/CD. (you can also use `ci:`, but `build:` is generally fine for everything)
refactor: Something changed in the code, but the code should still behave the same as before.
docs: Improving or updating documentation only.
test: Improving or updating tests only.
chore: Any other maintenance task that does not fit other labels.
```

**[GIT 04] On branches** In general, you want the `main` branch to be protected (developers can't directory modify `main`). Everything is then developed in separate developer-specific branches and delivered using pull requests. As with commits, use [Conventional Branch](https://conventional-branch.github.io/) names wherever possible. Here, it's a bit simpler compared to commits, because we generally only consider `feature/`, `bugfix/` , `release/` and `chore/` prefixes (with that said, `release/` should be only used when truly necessary; ideally, new features go into `main` directly). 

In general, try to have only one person commit to a specific branch (they "own" this code). If you want to make changes to their in-progress code, create your new branch from their branch, and then deliver your changes using a pull request (PRs can be created for any branch, not just `main`). To enforce this ownership, you can add the owner nickname to the branch *after* the prefix (this is recommended on larger/busier projects). For example, `feature/xpastva/new-variable-format` is a feature branch, owned by `xpastva`, that proposes a new variable format. If `xhuvar` wants to propose changes into this branch, they fork it into a `feature/xhuvar/new-variable-format` branch, make the changes, and then propose a PR that goes into `feature/xpastva/new-variable-format`.

**[GIT 05] On force pushing** You can use `git push --force` to overwrite the commit history stored on Github with you local version. This is good, actually. The convention is to have the `main` branch protected (no force pushing, everything that appears on `main` stays on `main`), but have other branches fully editable. In this case, if you make a mistake that you want to correct, you can actually go back and edit that specific commit, instead of fixing it with a new, unrelated commit. Then, force push allows you to publish that updated history. So, in general: (a) It is better to force push than to have a `fix` commit that resolves an issue introduced a few commits before. Assuming it is delivered within one pull request. (b) Sometimes, it's even good to completely start over and reorder the changes into a new, clearer commit history (or remove stuff that ended up not working). (c) Only force push on branches where you are working alone, or after agreeing with the other developers on that branch (force push can make it hard for other people to merge their work afterwards). See above on enforcing "branch ownership".

**[GIT 06] On versions** We use semantic versioning, as almost everyone else. Generally, try to release often when possible, even for projects that haven't had a major release yet. However, we don't really do snapshots (automatic releases for every commit/PR), since they are usually a hassle to setup and eventually make people ignore versioning anyway. Releasing should be ideally automated using CI, and there should be a tag (e.g. `v1.2.3`) in the git repository, as well as an actually release with a changelog created on Github.

**[GIT 07] On pre-release projects** If the project has not had the first major release (we are still in the `v0.x.x` phase), we can be a bit more flexible about the commit conventions. In particular, breaking changes do not need to be announced using `BREAKING CHANGES:`, because there is no previous version to break. Also larger, more complex pull requests are generally acceptable and code review can be somewhat more flexible. However, it is not ideal to stay too long in the pre-v1 phase, because it means other projects can't rely on your code. Ideally, we should make sure to have a clear path towards releasing a `v1` version as soon as possible.

**On protections and checks** In general, we require that CI passed. Approvals may be needed for larger projects.

**On code review**