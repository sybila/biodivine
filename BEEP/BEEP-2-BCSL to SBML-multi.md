# BEEP-2: BioChemical Space Language (BCSL) models relation to SBML-multi standard with automatic translation

**Maintainer:** Matej Troják (xtrojak@fi.muni.cz)

**Participants:** TBA

**Status:** Draft 

**Modules:** [BCSgen](https://github.com/sybila/BCSgen) 

**Tags:** extension, standards, BCSL, SBML, bachelor thesis, Python
 
## Proposal

*!!! This section is intended to give an overview of the proposal to any interested party. In order to make
the proposal accessible (proposals are often read by students or members of other teams), try to be informal 
and keep the technical information and formal definitions in the Specification section.*

*!!! While the proposal and specification should be largely self contained, it is recommended to reference available
definitions, algorithms or specifications from literature instead of rewriting them into the proposal.*

*!!! BEEP does not impose any restrictions regarding literature or references. If you want
to reference a website (for example some documentation), we recommend using standard markdown notation for links.
If you are referencing printed materials, we recommend using some standard reference format with all references
listed either at the end of the section or at the end of the document. If possible, you should also include a link to 
a website where the printed material is available. If you reference a specific part of text or a figure, make sure to
include a page number or a link to the specific part.*

*!!! The proposal section has several mandatory and optional subsections, each outlined below.*

### Background

BioChemical Space Language (BCSL) serves as description formalism for general BioChemical Space annotation format of 
biological objects and processes. It is a type of so called *rule-based* language, an abstraction above traditional 
reaction-based formalism. Instead of expressing interactions between particular objects, we talk about *types* of the objects. 
This way, the description is more concise. Moreover, the language is using several unique abstractions which fit for writing 
biochemical processing while trying to keep its syntax is readable as possible. 

### Problem

Despite advantages of particular abstractions of BCSL, it is very useful to relate such language to a standard 
notation for better sharing and processing options for other tools and researchers. There is a well-established standard 
for reaction-based systems - Systems Biology Markup Language (SBML). Recently, this standard was extended for rule-based 
systems by a package called SBML-multi. The automatic translation to this language is crucial aspect for further usage of BCSL.

### Solution

We will define a formal relation between these two languages and create a script which supports conversion 
from BCSL format to BC SBML-multi. The script will be created as a part of [BCSgen](https://github.com/sybila/BCSgen) project
(and its online version eBCSgen).

### Scope

The project can be used as a simple bachelors thesis or a student project. Work is suitable for two semesters - 
approximatelly 2/3 of the first
semester is spend by studying the mandatory literature, by the end of the semester the formal relation of
languages should be in a state  of finalisation. In the begining of the second semester the relation is 
finished and implementation of the specified script is done followed by extension of eBCSgen user interface.

### Challenges

It is necceasry to determine whether the SBML-multi covers all the features of BCSL.
In the negative case, an optimal way of encoding BCSL features in SBML-multi has to be discovered such that 
no information is lost during the translation. 

### Extensions

The module could be extended by possibility to import SBML-multi files to eBCSgen, which would be automatically 
converted to a BCSL model according to defined relation. This part can get tricky in case when the relation 
is not direct and some features has to be encoded in a more complicated way. In that case, an SBML-multi has to 
be first checked whether it satisfies requirements for model translation.

## Specification

The goal of this task is separated to two subtasks: (a) find a relation between BCSL model and SBML-multi standard and 
(b) implement automatic translation to this standard.

**(a)**: determine whether the SBML-multi covers all the features of BCSL. In the positive case, these features 
have to be formally related. In the negative case, an optimal way of encoding BCSL features in SBML-multi has 
to be discovered such that no information is lost during the translation. 

**(b)**: implement a module to eBCSgen tool which automatically exports given BCSL model in SBML-multi using approach 
formally defined in subtask (a). 

### Requirements

**(a)**: understanding BCSL formal definition and SBML-multi specification, basic knowledge of writing mathematical definitions.
**(b)**: be familiar with eBCSgen implementation on the level of extending its functionality and reusage of 
implemented parts. Knowledge of Python v.3+ and Galaxy framework are beneficial, but not mandatory.

### Literature

* BCSL and static analysis, SASB 2018
* SBML-multi specification, 2018

(optional)

* BCS paper, SASB 2015
* SBML manuscript, 2018

### Outputs

**(a)**: report and formal description of the relation, preferably written in LaTex. Precise description of individual 
steps and encountered problems.
**(b)**: a single callable Python function with BCSL model as a parameter, returns a SBML-multi output file. 
The functionality can be divided in multiple scripts if needed, but entire functionality has to be callable by one 
function. The script will be inteegrated in user interface of Pithya Galaxy framework as a separate callable job/task 
with possibility to download the outp

## Reports

