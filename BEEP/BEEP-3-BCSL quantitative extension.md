# BEEP-2: BioChemical Space Language (BCSL) quantitative extension

**Maintainer:** Matej Troják (xtrojak@fi.muni.cz)

**Participants:** TBA

**Status:** Draft 

**Modules:** [BCSgen](https://github.com/sybila/BCSgen) 

**Tags:** extension, BCSL, bachelor thesis, Python, quantitative semantics, rate
 
## Proposal

### Background

BioChemical Space Language (BCSL) serves as description formalism for general BioChemical Space annotation format [[3](#literature)] of 
biological objects and processes. The type of the language is so-called *rule-based*, an abstraction above traditional 
reaction-based formalism. Instead of expressing interactions between particular objects, we talk about *types* of the objects. 
This way, the description is more concise. Moreover, the language is using several unique abstractions which fit for writing 
biochemical processing while trying to keep its syntax as readable as possible. 

### Problem

In currect version of the language (October 2018), only qualitative semantics are enabled. It allows BCSL models to describe
whether some biochemical processes are possible, but do not specify the probability of such event. This way, the 
processes (in this case *rules*) have assigned overall probability of occurrence compared to uniform distribution 
in the case of the qualitative setting.

### Solution

We will extend BCSL rules by possibility to define *rate law*, an expression describing the probability of the rule to happen.
Then, it is necessary to define how such extended model behaves, i.e. define its semantics. Particularly, we would like to 
define stochastic and deterministic simulation....

TBA

### Scope

*!!! OPTIONAL: Describe how much work is expected for this proposal. How complicated are the sub-tasks or how
suited is it for student work. Simplified example: The project can be used as a simple bachelors thesis. However,
the implementation should be fairly simple as parsers for both formats are already available. The core of the work 
is to understand both formats and decide on the exact form of translation.*

### Challenges

*!!! OPTIONAL: List the possible risks and challenges of this proposal. What can make the project fail, what
can make it obsolete, what are the most complicated/risky parts of the proposal. Outline how you plan to proceed
if some problems arise (plan B). The purpose of this section is for the authors to also fully explore
the disadvantages/problems of their solution, as most authors tend to initially "oversell" their solutions. Example:
Format AB can represent FG, which we currently do not support in BC. We plan to find a way to encode FG in BC.
If no such way can be found, we will either restrict the functionality to models which do not contain FG, 
or given enough time, propose a modification of BC to support FG (as a new BEEP or as modification of
this BEEP).*

### Extensions

*!!! OPTIONAL: Possible secondary goals and objectives. Example: Format AB contains redundant information
which we usually don't want to include into BC. Design static analysis which can identify this redundant data 
in the BC structure and exclude it after the conversion. This approach can be also used to exclude redundant data
from other sources, as it works for a general BC model.*

### Related work

*!!! OPTIONAL: Give references to other tools, papers or libraries which try to solve similar problem or which can be
helpful when implementing the proposal. Example: The are two parsers for the AB format, [Foo]() and [Goo](). 
AB format can be also converted to GH using [Lorem Ipsum](). Format BC can be processed using utilities
provided in [some repository]().*

## Specification

*!!! MANDATORY: Specification section contains all technical details of the project. You can define your own sections based on the project you are proposing. The only mandatory section is Outputs. However, we recommend you at least formally define the problem you are solving (define inputs, expected properties), the proposed solution (algorithm pseudo-code, data relationships, chosen tools and technologies) and sketch some details of the solution implementation (define interfaces).*
 
 *!!! Examples of OPTIONAL sections: Requirements (what have to be satisfied in order to declare the task as successfully finished), Preliminaries (list of formal definitions and notations which is used to describe the project), Problem definition (explain the problem formally/in detail), Solution (what is expected from the solution and how it should be evaluated - be as exact as possible, use formal definitions, references, algorithm pseudo-code).*

### Outputs

*!!! MANDATORY: Describe how exactly the outputs should look like. Be as specific as possible or give a list of possible alternatives. Example: formal definition of the proposed problem written in a LaTex document; a standalone script written in Python with a model in XY format as a parameter, returns a model in format AB; visualisation of XY will be integrated into online platform AB.*
 
## Reports

### Interim

*!!! OPTIONAL: In case of partial accomplishment or suspension of the project, it is suitable to write a short report about the current state of the proposal, what has been already achieved and what haven't been. This helps to keep track of the progress of the proposal. It is possible to write multiple interim reports. If possible, a particular commit in a repository or another form of progress should be attached.*

### Final

*!!! MANDATORY: When the proposal is finished, here you have a place to sum up the outputs, evaluate the solution and overall convince the other maintainers that the proposal is completed. Also link to source code, documentation, publications or other external materials.*
