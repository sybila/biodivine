# BEEP-2: BioChemical Space Language (BCSL) quantitative extension

**Maintainer:** Matej Troják (xtrojak@fi.muni.cz)

**Participants:** Lukrécia Mertová, Matej Troják

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

We will extend BCSL rules by possibility to define *rate law*, an expression describing the probability of the rule to happen and extend BCSgen tool by this functionality.

### Scope

A student project or part of a bigger project, it is work for 1-2 people for at most one semester.

### Challenges

Quantitative semantics for rule-based systems is still not a well-established field, might require non-trivial effort in studying the relevant literature.

## Specification

The goal of the task is to extend BCSL by the possibility to express rate law, define semantics for such extended models, and implement the extension to BCSgen tool. The task can be divided into three subtasks:

**(a)** Investigate possible solutions (for example, check other rule-based languages and their approach to solving this problem). The goal of this task is to choose an optimal solution such that (1) the following task is manageable, (2) BCSL keeps its human-readable feature, and (2) allows to express rate laws as general as possible.

**(b)** Define semantics for approach chosen in task (a). Generally, it means for an extended BCSL model to define a semantics function which describes the behaviour of the modelled system over time. There are multiple ways how to solve this task. We require a (1) stochastic semantics, which implies [Continuous-time Markov chain](https://en.wikipedia.org/wiki/Markov_chain#Continuous-time_Markov_chain) and (2) deterministic semantics, which models an average behaviour of the modelled system. In both cases, it is necessary to make sure the solution works for particular admissible rate laws. It was shown it works for [mass action](https://en.wikipedia.org/wiki/Law_of_mass_action) and (maybe) for enzymatic kinetics [Michaelis - Menten](http://www.cs.ucsb.edu/~cse/Files/stoch_2011.pdf), but other more general laws are questionable.

**(c)** The defined solution will be integrated into BCSgen (and its online version eBCSgen) such that it supports the development of such model (model editor extension) and analysis (simulation and other types).

### Outputs

The subtasks (a) and (b) will be written down and formalised in paper *Parameter Synthesis for Rule-Based Models in Biochemical Space Language* and will serve as base which enables the paramether synthesis for rule-based models. The paper will be published on a conference.

The subtask (c) will be implemented within BCSgen tool. It particularly means to extend its rule parser (by changing the language's grammar) and modify algorithms for transition system generating and enabling the simulation of the models (in both stochastic and deterministic settings).
 
## Reports
