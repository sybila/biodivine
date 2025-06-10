# Sybila Developer Guide

This document outlines some general recommendations towards developing *new* projects (old projects will be updated whenever possible, but it is a low priority task). This is not a *law*; use rational judgement to decide if these rules work for you. With that said, you should probably consult with the senior staff if you are going to diverge significantly.

The recommendations are not presented in any particular order. Some are more general "software quality" rules, some are very language or tool specific.

### Git

**[GIT 01] Use the right software** There is no point in flexing your CLI skills if it makes you unproductive, or worse yet, makes you skip useful code quality measures because they are hard to do from command line. If you are not already *very* comfortable with git, it is recommended to download [Sublime Merge](https://www.sublimemerge.com/) and use it. It does not provide any "special" functionality. Everything translates into existing git commands. It's just much easier to do complex stuff in it. Some notable things that you can easily do that's much more tiresome using CLI:

* Commit only a specific line of code among many existing code changes.
* Edit a commit message of an old commit.
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

In general, try to have only one person commit to a specific branch (they "own" this code). If you want to make changes to their in-progress code, create your new branch from their branch, and then deliver your changes using a pull request (PRs can be created for any branch, not just `main`). To enforce this ownership, you can add the owner nickname to the branch *after* the prefix (this is recommended on larger/busier projects). For example, `feature/xpastva/new-variable-format` is a feature branch, owned by `xpastva`, that proposes a new variable format. If `xhuvar` wants to propose changes into this branch, they fork it into a `feature/xhuvar/new-variable-format` branch, make the changes, and then propose a PR that merges these changes into `feature/xpastva/new-variable-format`.

**[GIT 05] On force pushing** You can use `git push --force` to overwrite the commit history stored on Github with you local version. This is good, actually. The convention is to have the `main` branch protected (no force pushing, everything that appears on `main` stays on `main`), but have other branches fully editable. In this case, if you make a mistake that you want to correct, you can actually go back and edit that specific commit, instead of fixing it with a new, unrelated commit. Then, force push allows you to publish that updated history. So, in general: (a) It is better to force push than to have a `fix` commit that resolves an issue introduced *in the same pull request* (of course, once the issue is merged into `main`, it has to be fixed using ` fix` commit). (b) Sometimes, it's even good to completely start over and reorder the changes into a new, clearer commit history (or remove stuff that ended up not working). (c) Only force push on branches where you are working alone, or after agreeing with the other developers on that branch (force push can make it hard for other people to merge their work afterwards). See above on enforcing "branch ownership".

**[GIT 06] Rebase all the things** Many novice users of git are not familiar with rebase (most often used as `git pull --rebase`, but essentially any merge operation can be applied with rebase). Rebase is a feature that allows you to reorder commits or even introduce completely new commits somewhere in the branch history. The most common situation where rebase is used is when you are pulling changes from the remote repository, but you also have some changes commited locally. Historically, this would result in a merge conflict, which would have to be resolved using a merge commit; but this solution is impractical because it alters or loses change history, plus it introduces unnecessary new merge commits. 

Instead, with rebase, git automatically "removes" all changes to the point where pulling safely is possible, and then it "re-commits" them as new commits into the updated (i.e. rebased) branch. This acts as a merge, but preserves the full history of both branches. However, do note that your local commits are still *re-created* from scratch based on the saved changes. This means that they are functionally the same, but technically new commits, meaning they have a new unique commit hash, and that any tags that you created for the local commits are not associated with the new commits. 

Finally, a merge conflict can still occur during rebase, asuming the local and remote changes do in fact conflict. In that case, git will prompt you to update your local commit changes while the commit is being recreated, essentially giving you the option to change your local history to adjust to the incoming remote changes.

**[GIT 07] On versions** We use semantic versioning, as almost everyone else. Generally, try to release often when possible, even for projects that haven't had a major release yet. However, we don't really do snapshots (automatic releases for every commit/PR), since they are usually a hassle to setup and eventually make people ignore versioning anyway. Releasing should be ideally automated using CI, and there should be a tag (e.g. `v1.2.3`) in the git repository, as well as an actual release with a changelog created on Github.

**[GIT 08] On pre-release projects** If the project has not had the first major release (we are still in the `v0.x.x` phase), we can be a bit more flexible about the commit conventions. In particular, breaking changes do not need to be announced using `BREAKING CHANGES:`, because there is no previous major version to break. Also larger, more complex pull requests are generally acceptable and code review can be somewhat more flexible. However, it is not ideal to stay too long in the pre-v1 phase, because it means other projects can't rely on your code. Ideally, we should make sure to have a clear path towards releasing a `v1` version as soon as possible.

**[GIT 09] On protections, checks and CI** We don't have a formal process that is enforced for every project (this will again depend on how "mature" the project is). However, in general, try to keep the main branch protected, and require both code review and CI checks to pass in order to merge. For pre-release or experimental projects, you can be a bit more lax on the code review side :) 

With regards to CI, you should set it up as soon as possible, and it should include at least the following:

- Code formatting and style checks. Don't reinvent the wheel, pick some default or recommended style and enforce it, otherwise formatting will degrade quickly.
- Linter or static analysis. Have some kind of static analysis tool set up for your language, even if it is not the most powerful one. Be as strict as you can be while staying reasonable. Having strict static analysis typically forces you to create code that is more "standard" and thus "readable" for the relevant language.
- Tests, including coverage where possible. Have some tests. They don't have to be super comprehensive, but figure out early how you are going to test the project, and do it. Enable code coverage where possible, but don't target any particular coverage level. *The point of code coverage is not to enforce quality of tests; code coverage tells you whether your tests actually work.* We use [Codecov](https://about.codecov.io/) to automate coverage reporting, but this is not required as long as you can somehow attach the coverage report to each pull request.
- Release. Early on, you should figure out how your project will be released and automate this. This enables you to release quickly and often. If you don't do this, you will be creating releases that are needlessly large and complex simply because you won't have time/resources to release often. Ideally, a release should automatically happen once a release tag is created.

*Performance tests:* Don't run performance tests on normal github CI, the runners are not nearly consistent enough for that. However, it is very easy to create a custom runner on our own dedicated hardware that can be used for this. If you want/need this, get in touch with the senior staff. Currently, we don't have a rigorous methodology for performance regression testing, but we are certainly building one.

*Why code coverage:* Measuring code coverage is often deemed unnecessary because it does not tell you much about the quality of the tests (tests with 100% code coverage can still be much worse than tests with 50% coverage). However, there are several advantages to code coverage that I think are very relevant, assuming we stop giving ourselves arbitrary coverage targets. First, coverage validates that the tests are working. Imagine a test is wrong and it does not actually execute the code that the developer expected, but it passes anyway. Then normally the only mechanism to catch this is code review. Code coverage is a second factor that validates that the test is doing what it is supposed to, because the uncovered lines will show up in the pull request. Second, coverage indicates which code is important (tested) and which code is biolerplate, unused, etc. (untested). This helps new developers to understand the project better and overall set priorities. 

**[GIT 10] On code review** We currently don't do that much code review because it is "expensive". However, in the future, it would be something that we should consider (and involve PhD students in this a bit more). Currently, I recommend reviewing at least the first few new features in depth on new projects to set the standards. Subsequently, the review can be a bit more relaxed. We may also try LLM reviews to speed up the process, but it's not yet clear how useful this will be.

## Rust

- Prefer `T::from(x)` against `x.into()`.
- Prefer `T::from(x)` against `x as T`.
- Use public-api in CI to check for public API changes (https://github.com/cargo-public-api/cargo-public-api)

## Web (JS/TS/HTML/CSS)

* TODO