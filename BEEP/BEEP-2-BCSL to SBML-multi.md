# BEEP-2: BioChemical Space Language (BCSL) models relation to SBML-multi standard with automatic translation

**Maintainer:** Matej Troják (xtrojak@fi.muni.cz)

**Participants:** Branislav Brozmann

**Status:** Draft 

**Modules:** [BCSgen](https://github.com/sybila/eBCSgen) 

**Tags:** extension, standards, BCSL, SBML, bachelor thesis, Python
 
## Proposal

### Background

BioChemical Space Language (BCSL) serves as description formalism for general BioChemical Space annotation format [[3](#literature)] of biological objects and processes. The type of the language is so-called *rule-based*, an abstraction above traditional reaction-based formalism. Instead of expressing interactions between particular objects, we talk about *types* of the objects. This way, the description is more concise. Moreover, the language is using several unique abstractions which fit for writing biochemical processing while trying to keep its syntax as readable as possible. 

### Problem

Despite advantages of particular abstractions of BCSL, it is very useful to relate such language to a standard notation for better sharing and processing options for other tools and researchers. There is a well-established standard for reaction-based systems - Systems Biology Markup Language (SBML) [[4](#literature)]. Recently, this standard was extended for rule-based systems by a package called SBML-multi [[2](#literature)]. The automatic translation to this language is a crucial aspect for further usage of BCSL.

### Solution

We will define a formal relationship between these two languages and create a script which supports conversion 
from BCSL format to SBML-multi. The script will be created as a part of [eBCSgen](https://github.com/sybila/eBCSgen) project.

### Scope

The project can be used as a bachelor's thesis or a student project. Work is suitable for two semesters - approximately 2/3 of the first semester is spent by studying the mandatory literature, by the end of the semester the formal relation of languages should be in a state of finalisation. Until the middle of the second semester the relation is finished and the specified script is implemented and deployed as an extension of eBCSgen functionality.

### Challenges

It is necessary to determine whether the SBML-multi covers all the features of BCSL. In the negative case, an optimal way of encoding BCSL features in SBML-multi has to be discovered such that no information is lost during the translation or the authors of SBML-multi might be contacted with the goal of language extension.

### Extensions

The module could be extended by a possibility to import SBML-multi files to eBCSgen, which would be automatically converted to a BCSL model according to the defined relation. This part can get tricky in the case when the relationship is not direct and some features have to be encoded in a more complicated way. In that case, an SBML-multi file has to be first checked whether it satisfies requirements for model translation.

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
implemented parts. Knowledge of Python 3+ and Galaxy framework are beneficial, but not mandatory.

### Literature

* [1] Executable Biochemical Space for Specification and Analysis of Biochemical Systems, accepted in SASB 2018 [:page_facing_up:](https://www.fi.muni.cz/~xtrojak/files/papers/sasb2018.pdf)
* [2] SBML Level 3 package: Multistate, Multicomponent and Multicompartment Species, Version 1, Release 1, 2018 [:page_facing_up:](http://co.mbine.org/specifications/sbml.level-3.version-1.multi.version-1.release-1.pdf)

(optional)

* [3] Biochemical Space: A Framework for Systemic Annotation of Biological Models, CS2Bio 2014 [:page_facing_up:](https://core.ac.uk/reader/81208710)
* [4] SBML at 18: More Sophisticated, but with Room to Grow (2018 Version)

### Outputs

**(a)**: Report and formal description of the relation, preferably written in LaTex. The precise description of individual 
steps and encountered problems (prepared for publication purposes). 

**(b)**: A single callable Python 3 function with BCSL model as a parameter, returns a SBML-multi output file. 
The functionality can be divided into multiple scripts if needed, but entire functionality has to be callable by one 
function. The script will be integrated into the user interface of Pithya Galaxy framework as a separate callable job 
with the possibility to download the output.

## Reports

* No particular reports are needed, yet frequent consultations with maintainer are required.
