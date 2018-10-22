# BEEP-2: BioChemical Space Language (BCSL) models relation to SBML-multi standard with automatic translation

**Maintainer:** Matej Troják (xtrojak@fi.muni.cz)

**Participants:** TBA

**Status:** Draft 

**Modules:** [BCSgen](https://github.com/sybila/BCSgen) 

**Tags:** extension, standards, BCSL, SBML, bachelor thesis, Python
 
## Proposal

### Background

BioChemical Space Language (BCSL) serves as description formalism for general BioChemical Space annotation format [[3](#literature)] of 
biological objects and processes. The type of the language is so-called *rule-based*, an abstraction above traditional 
reaction-based formalism. Instead of expressing interactions between particular objects, we talk about *types* of the objects. 
This way, the description is more concise. Moreover, the language is using several unique abstractions which fit for writing 
biochemical processing while trying to keep its syntax as readable as possible. 

### Problem

Despite advantages of particular abstractions of BCSL, it is very useful to relate such language to a standard 
notation for better sharing and processing options for other tools and researchers. There is a well-established standard 
for reaction-based systems - Systems Biology Markup Language (SBML) [4]. Recently, this standard was extended for rule-based 
systems by a package called SBML-multi. The automatic translation to this language is a crucial aspect for further usage of BCSL.

### Solution

We will define a formal relationship between these two languages and create a script which supports conversion 
from BCSL format to SBML-multi. The script will be created as a part of [BCSgen](https://github.com/sybila/BCSgen) project
(and its online version eBCSgen).

### Scope

The project can be used as a bachelor's thesis or a student project. Work is suitable for two semesters - 
approximately 2/3 of the first
semester is spent by studying the mandatory literature, by the end of the semester the formal relation of
languages should be in a state of finalisation. In the beginning of the second semester the relation is 
finished and implementation of the specified script is done followed by extension of eBCSgen user interface.

### Challenges

It is necessary to determine whether the SBML-multi covers all the features of BCSL.
In the negative case, an optimal way of encoding BCSL features in SBML-multi has to be discovered such that 
no information is lost during the translation. 

### Extensions

The module could be extended by a possibility to import SBML-multi files to eBCSgen, which would be automatically 
converted to a BCSL model according to the defined relation. This part can get tricky in the case when the relationship
is not direct and some features have to be encoded in a more complicated way. In that case, an SBML-multi file has to 
be first checked whether it satisfies requirements for model translation.

## Specification

The goal of this task is separated into two subtasks:

**(a)** Find a relation between BCSL model and SBML-multi standard:

Determine whether the SBML-multi covers all the features of BCSL. In the positive case, these features 
have to be formally related. In the negative case, an optimal way of encoding BCSL features in SBML-multi has 
to be discovered such that no information is lost during the translation.

**(b)** Implement automatic translation to this standard:

Implement a module to eBCSgen tool which automatically exports given BCSL model in SBML-multi using approach 
formally defined in subtask (a).

### Requirements

**(a)**: Understanding BCSL formal definition [[1](#literature)] and SBML-multi specification [[2](#literature)], basic knowledge of writing mathematical definitions.

**(b)**: Be familiar with eBCSgen implementation on the level of extending its functionality and re-usage of 
implemented parts. Knowledge of Python v.3+ and Galaxy framework are beneficial, but not mandatory.

### Literature

* [1] Executable Biochemical Space for Specification and Analysis of Biochemical Systems, accepted in SASB 2018 [:page_facing_up:](https://www.fi.muni.cz/~xtrojak/files/papers/2018,%20SASB,%20Executable%20Biochemical%20Space%20for%20Specification%20and%20Analysis%20of%20Biochemical%20Systems.pdf)
* [2] SBML Level 3 package: Multistate, Multicomponent and Multicompartment Species, Version 1, Release 1, 2018 [:page_facing_up:](https://www.degruyter.com/downloadpdf/j/jib.2018.15.issue-1/jib-2017-0077/jib-2017-0077.pdf)

(optional)

* [3] Biochemical Space: A Framework for Systemic Annotation of Biological Models, CS2Bio 2014 [:page_facing_up:](https://ac.els-cdn.com/S1571066114000590/1-s2.0-S1571066114000590-main.pdf?_tid=15e9629c-ff03-484b-afeb-f6a56da41022&acdnat=1540211331_65dbb0acf63aaec73d118deef15360ae)
* [4] SBML at 18: More Sophisticated, but with Room to Grow (2018 Version)

### Outputs

**(a)**: Report and formal description of the relation, preferably written in LaTex. The precise description of individual 
steps and encountered problems (prepared for publication purposes). 

**(b)**: A single callable Python 3 function with BCSL model as a parameter, returns a SBML-multi output file. 
The functionality can be divided into multiple scripts if needed, but entire functionality has to be callable by one 
function. The script will be integrated into the user interface of Pithya Galaxy framework as a separate callable job 
with the possibility to download the output.

## Reports

