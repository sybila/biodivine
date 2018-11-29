## BioDivine

BioDivine is a toolset for manipulation, analysis, validation, and verification of biological models. BioDivine provides three levels of functionality:
 - **Tools and tool integrations:** Designed for specific tasks with the user in mind, BioDivine tools provide graphical interfaces, input formats, and interactive visualisations suitable for "point-and-click" analysis.
 - **Interactive notebooks:** BioDivine integrates with the Jupyter notebook system, providing access to new or experimental features and allowing power users to easily combine, extend and modify its functionality.
 - **Libraries and frameworks:** All BioDivine functionality is implemented in a set of open source, extensible libraries. Well tested, high-performance, multiplatform code ready production.

Note that this repository serves mainly as container for internal BioDivine documentation, website source code and other resources. For more information about functionality provided by BioDivine, visit the [BioDivine homepage](http://biodivine.fi.muni.cz).

### Goals and design philosophy

BioDivine is aimed to be a multi-purpose toolbox with support for different model analysis techniques. This section outlines the overall goals and motivations behind BioDivine.

#### User friendly input/output and interoperability

BioDivine aims to provide the best possible user experience without sacrificing interoperability. To this end, BioDivine often provides custom input formats and even custom modelling languages. The goal of this approach is to support concise, human readable models with great editor support. However, presence of each such format in the toolbox should be justified and other standard options fully explored before a new format is introduced. Additionally, for each format, import/export to other standard alternatives should be available in order to foster interoperability with other toolsets. For more guidelines about introducing, designing and implementing input/output formats, see the TODO guide. For the list of custom biodivine formats, see TODO.

#### Model identification and validation

Each model design starts with a set of experimental data and assumptions about the studied system. In order to transform this knowledge into a working model, BioDivine supports model identification and validation. For more information about model identification and validation in BioDivine, see TODO.

#### Static analysis

Static analysis in the context of BioDivine is understood as investigation of the models properties using only the analytical description of the model (ODE, regulatory network, code) without explicit exploration of its behaviour (trajectories, runs). This type of analysis is usually quite cheap, but can quickly improve the models and simplify further analysis. It is also typically tightly coupled with the model editor as it is often the first type of analysis the user performs.

Some of the typical examples include:
 - Investigation of equilibria in an ODE model by examining zero derivatives.
 - Investigation of ODE models boundaries in order to guarantee the model is positive invariant.
 - Elimination of unreachable states in Petri net or reaction network using algebraic inequalities.
 - Elimination of unused or unnecessary elements of the model.

For more information about static analysis in BioDivine, see TODO.

#### Simulation and symbolic execution

Other important aspect of model analysis is simulation. Simulation allows to investigate specific runs or trajectories of the model without fully exploring the global behaviour of the model. It is thus often very efficient when parameters and initial conditions are already known. It can be an invaluable asset when "debuging" models and provide useful visualisations that support other types of analysis.

The disadvantage of simulation is that the system has to be fully known. If the system still contains some unknown elements, we often talk about symbolic execution (in continuous models, this approach can be viewed as flow-pipes). This approach allows us to investigate the evolution of the system even with some uncertainity. This often leads to techniques which introduce higher error rates in their results compared to single simulation. However, they are typically also much faster than simulation sampling methods, especially in higher dimensions (while one simulation can be inexpensive, running 1000 simulations to properly cover the uncertainity space can be quite demanding).

For more information about simulation and symbolic execution in BioDivine, see TODO.

#### Model verification

Compared to simulation or symbolic execution, verification typically provides global guarantees about the models behaviour. One can verify "simple" properties such as safety (something bad will never happen) or liveness (something good will repeatedly happen). A more general approach is model checking, which typically verifies validity of some temporal formula (for more about temporal logics, see CTL, LTL or HUCTL) over the studied system. These methods typically provide the strongest formal guarantees, but also require highest amount of computational resources. Suitable abstractions or reductions are often necessary to perform these types of analysis on large systems.

For more information about verification in BioDivine, see TODO.

#### Parameter synthesis

As mentioned earlier, models often come with some level of uncertainity — parameters. Parameter synthesis allows to reduce this uncertainty by identifying regions in the parameter space which satisfy the requirements imposed on the model (these can be specified in various forms, either as data or as properties, similar to the case of verification). Parameter synthesis can be also often used for model identification. A special computationally simpler subproblem - finding at least one satisfying parametrisation - can be also explored.

For more information about parameter synthesis in BioDivine, see TODO.

#### Bifurcation analysis

Bifurcation analysis provides qualitative characterisation of model behaviour with respect to models parameters. It can be often viewed as an alternative to parameter synthesis when there are no specific use-given properties, but more general qualitative behavioural properties need to be explored.

#### Other techniques: 
parameter identification (which is the best parameter), experimental design 
(give experiment to best update the results)

### Technology and development

BioDivine is developed at the Sybila laboratory at the Masaryk University in Brno, Czechia. However, we accept all external contributions and are happy to collaborate with other entities. The project is maintained in great part with the help of student contributions. This aspect necessitates a specific approach to project management, as the variance and flux of developers contributing to the project can be significant. 

The development of BioDivine is driven by two core units: modules and BioDivine extension or enhancement proposals. 

A module is a standalone piece of code with dedicated functionality (tool, library, visualisation widget, etc.). Each module should have one core maintainer which is responsible for its codebase. A module has one of the following states:
 - development: the module has a maintainer, an initial BEEP and there is active development, but it is not production ready
 - active: the module has a maintainer and a production ready version and the initial BEEP is closed (there can be experimental features and new development, but there is also a stable version)
 - unmaintained: module has a stable, documented version, but it does not have a maintainer, so there is noone to resolve issues and drive new development
 - abandoned: the module has no stable version and no maintainer, but can move back into development if new maintainer is found
 - deprecated: the module has a stable version, but no maintainer and the stable version is severely outdated and won't be fixed

On the other hand BEEP is a proposal document for new functionality or enhancement. It specifies new modules or enhancements to functionality of current modules. Thus each module can be associated with multiple BEEPs, but there is always at least one BEEP (the initial module proposal). Each BEEP has to be approved by all BioDivine maintainers and moves between the following states:
 - draft: BEEP is being prepared and can be freely modified. It typically has one core maintainer, but it does not have to be the core maintainer of the corresponding module which the BEEP is associated with. A beep in development can move back to draft mode if the maintainers/developers decide it is not feasible, but it has to be approved again if it wants to move back into development.
 - development: BEEP is approved by all maintainers and put into active development. It can't be edited, but it can be amended with new information.
 - completed: BEEP has been fully developed and all maintainers approved it as completed.
 - abandoned: BEEP is deemed unfeasible and is amended with information about why it will not be implemented.


## Developer guides

### BEEP template

### Input/Output format developer guide

### Visualisation widget developer guide

### Analytical tool developer guide



#### NewBioDiVinE

A historical version of BioDiVinE for parameter estimation in pice-wise multi-affine systems is available at https://github.com/sybila/NewBioDiVinE.


Poznamky:
- pointa beepu je mat moznost navrhovat funkcionalitu bez toho aby som ju implementoval: bakalarky, diplomky, etc. a zaroven mal presne specifikovane na zaciatku co od toho chcem a co nie
- beep musi schvalit cela "komisia" biodivinu
