# BEEP-1: Binary Decision Diagram (BDD) Solver

*// The person responsible for this proposal. Other people can review, comment on and edit this document, 
but the final responsibility on reaching consensus about this proposal is that of the maintainer. An email contact
is highly appreciated!*

**Maintainer:** Samuel Pastva (daemontus@gmail.com)

*// Other people working on the proposal. Consultants, developers, maintainers, etc. In alphabetical order, possibly 
with a list of responsibilities and contact information.*

**Participants:** Samuel Pastva (proposal, theory, integration), Jakub Poláček (XXXX@mail.muni.cz, 
design, implementation, bachelor thesis)

*// Proposal status. Status can be: Draft, Development, Completed, Abandoned. All core biodivne maintainers should be 
involved when status of a proposal changes. This is to avoid development of drafts which collide with other components
or completion of proposals which are incompatible with rest of the toolset. However, no "rigorous" process for this
is in place. When you want to change the status of a proposal, simply email everyone that they should review 
the changes.*

**Status:** Draft // TODO: This should have a color. Draft - grey, Development - orange, Completed - green, Abandoned - red.

*// If applicable, reference to other proposals which need to be completed before this proposal can be finished.*

**Depends on:**

*// If applicable, reference to other proposals which are enabled by completion of this proposal.*

**Required by:** [BEEP-2: Boolean network generator for Pithya](TODO)

UPDATE: Relationships to related projects and proposals as one section. Can be divided into depends on and required by, 
does not have to.

## General section

### Background

### Problem 

### Goals

### ? Risks and limitations

### ? Scope (time, tasks, etc.)

### ? Extensions

## Technical section

### ? Preliminaries

### Specification

#### requirements
#### problem definition
#### solution...

### Outputs

## Final Report

### Problem Statement

*// Here, write motivation and informal problem description of the issues this proposal is trying to address. You don't 
have to be overly technical or formal, this section should be readable to people with as little prior knowledge as
possible. If possible, include simple examples to support and illustrate your case.*

In order to represent discrete parameters in models, a suitable symbolic representation is necessary, as explicit 
representations fail even for smaller models. For example, while a simple bit set representation of a parameter space with
16 parameters is only about 8kB, 32 boolean parameters need more than 500mB. If multiplied by the number of states
in the system, this number quickly becomes unreasonable.

Sets of discrete elements can be also used in other situations, such as compact state space representation or 
efficient transition generators. 

### Solution proposal

*// A simple, informal proposal of your solution. As in the previous section, try to include examples and be as 
human readable as possible.*

A traditional approach to this problem is to use Binary Decision Diagrams (BDD) or some other similar variant (ZDD,
ADD, etc.). These data structures allow easy representation of binary functions by the means of acyclic graphs. 

TODO: Add picture of BDD representing a binary function.

Asymptotically, the worst case complexity is the same as for explicit representations (the size of the graph can be
still exponential in the number of input variables). However, on average, a significant improvement in size and 
space can be achieved.

BDDs are already implemented in a number of open source libraries. The goal of this proposal is thus to use one of
these libraries in order to implement biodivine [solver interface](TODO) which can be later used by other tools.

The implementation should provide reasonable performance and reusability, thus a set of benchmarks should be included
before the proposal is completed.

### Risks and challenges

*// Describe how can the proposal fail to solve the problem, what will be the toughest challenges or what
 can make the proposal obsolete, where are the limits of the solution, etc.*
 
 * BDDs are not asymptotically better than explicit representation. Hence for some models, the proposed solution might
 not provide any speed-up. This aspect should be explored in the benchmark aspect of the project.
 
 * Ordering of variables in BDDs can often drastically influence their effectiveness. Currently, no efficient algorithms
 for producing optimal ordering are known (worst case, you have to test all orderings). However, for specific types
 of models, heuristics can be devised to tackle this issue. This is not directly the concern of this project, as
 it should be model agnostic. However, one can explore some general optimisation/reordering strategies.
 
 * The project only considers boolean parameters. Multi-valued parameters can be also encoded into this structure
 as bit-vectors, however, more efficient representations are possible there. Also, no continuous values are possible.
 This can be addressed in future proposals by uniting the notion of interval, algebraic and boolean decision diagrams
 into one hybrid data structure.
 
 * From the technical standpoint, the project should not be very challenging as most of the functionality is readily
 available. The toughest part is to asses the performance and capabilities of different BDD libraries in order
 to decide which is the best suitable (requires documentation reading and small experiments).

### State of the art

*//Describe existing solutions related to your problem*

List of BDD libraries...

List of BDD model checking tools...

### Technical specification

*// This is the important part, here you describe the problem formally/in detail. Then you describe what is expected
from the solution and how it should be evaluated. Be as exact as possible, use formal definitions, references,
algorithm pseudo-code.*

TODO

### Final Report

*// When the proposal is finished, here you have a place to sum up the outputs, evaluate the solution and overall 
convince the other maintainers that the proposal is completed. Also link to source code, documentation, publications 
or other external materials.*