*!!! This is a template for definition of BioDivine Extension and Enhancement Proposals (BEEPs).* 

*!!! Format: BEEP is a standard markdown file extended with support of LaTeX-style mathematical formulas 
(enclosed in $ - support is provided by MathJaX, see their documentation for more info). It also supports
inline html. In the future, more features can be added (syntax highlighting in code blocks, live notebooks).* 

*!!! Additionally, this document contains "comments" marked with !!!. These are notes intended for BEEP authors and
should be completely removed from the file before publication.*

*!!! Each BEEP has a unique numeric ID and title. The title can change if needed, but the ID should stay the same.
While not required, it is recommended to choose ID as the next smallest available integer.*

*!!! BEEP files should follow the document structure and content recommendations described in this document. In some 
cases, exceptions to this rule can be allowed. However, all BEEP files must contain the following header with 
meta-information in order to be correctly processed by the static site generator! If the information is not present,
site build will fail and proposal can't be merged into master.*

# BEEP-{ID}: {Title}

*!!! The person responsible for this proposal. Other people can review, comment on and edit this document, 
but the final responsibility on reaching consensus about this proposal is that of the maintainer. An email contact
is highly appreciated!*

**Maintainer:** John Doe (some.email@gmail.com)

*!!! Other people working on the proposal. Consultants, developers, maintainers, etc. In alphabetical order, possibly 
with a list of responsibilities and contact information. Maintainer is usually also one of participants, 
but not necessarily.*

**Participants:** John Doe (proposal, theory, integration), Peter Smith (peters@mail.com, 
design, implementation, bachelor thesis)

*!!! Proposal status. Status can be: **Draft**, **Development**, **Completed** or **Abandoned**. All core BioDivine 
maintainers should be informed when the status of a proposal changes. This is to avoid development of drafts which 
collide with other components or completion of proposals which are incompatible with the rest of the toolset. 
However, no "rigorous" mechanism for this is in place. When you want to change the status of a proposal, simply email 
everyone at sybila@fi.muni.cz with subject "[BEEP] BEEP-{ID} {Status change, e.g. Draft->Development} {Title}".
The email body can contain more info about the status change. Please respect that any status change can be blocked 
by any core maintainer given reasonable objections (for example, maintainer of the notebook modules can reject
completion of a module which is incompatible with notebooks).*

TODO: Status should have a color. Draft - grey, Development - orange, Completed - green, Abandoned - red.

**Status:** Draft 

*!!! Modules contain names and links of BioDivine modules (git repositories) affected by this BEEP. 
If BEEP will not add/update any code, leave the field empty. If repository is not created yet, write its proposed name 
and supplement it with a link once it is available.*

**Modules:** [biodivine-model-toolkit](url), biodivine-playbooks 

*!!! Tags allow maintainers to quickly group BEEPs by arbitrary properties and give quick overview of the BEEPs 
contents. Tags are always in one paragraphs, separated using commas. Any other characters (including math) 
should be supported.*

*!!! Popular types of information which go into tags: type of proposal (enhancement - making existing stuff better 
vs. extension - adding new stuff), related student work (bachelors thesis, diploma thesis, student project, PhD thesis),
type of studied systems (differential equations, boolean networks, hybrid systems), used algorithms and tools,
types of analysis (simulation, model checking), etc. Consult the list of BEEPs for other examples of tags.*

**Tags:** extension, model checking, diploma thesis, LTL, boolean network, kotlin

*!!! Related projects are optional part of the header. They contain references to other projects this BEEP is in some
way related to. Usually, it is good to also include what type of relationship this is.*

**Related projects:** requires [BEEP-123](url), required by [BEEP-345](url), based on "That thing which is not a BEEP",
 grant number A12345B
 
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

*!!! OPTIONAL: Use this section to introduce the reader to your setting. It can be omitted if the project concerns
some well understood mechanism or technique, but in general, we recommend giving at least a set of useful references
for future readers. Example: Imagine a student of bio-informatics who never heard of model checking or temporal
logic. How would you quickly introduce him to the area? Or a student of computer science who has no idea about
modelling formalisms such as boolean networks. (Background section can be often copied from other BEEPs with
similar background)* 

### Problem

*!!! MANDATORY: Describe the motivation behind the problem you are trying to solve and give an informal definition
of the problem itself. If possible, give or reference some examples to support your case. Simplified example: In order 
to analyse the set of models available at the XY repository, BioDivine needs to support the format AB ([link]()).
Some interesting models from this set include A, B, or C. The format support must be compatible with repository
X and Y as these are the main analysis techniques we support regarding this type of models.*

### Solution

*!!! MANDATORY: Give an informal description of what is the proposal trying to achieve and how does it solve
the described problem. If applicable, you can split the proposal into sub-goals. The Outputs section is intended
to give formal specification of the expected results, so you don't have to be overly specific here.
Simplified example: We will create a new import script which supports conversion from AB format to BC format. 
BC format is already supported as an input of X and Y, so this type of conversion should be sufficient to provide 
necessary support. As a secondary goal, we will also create a script for conversion from BC to AB in order to allow 
BioDivine models to be submitted into XY repository. The scripts will be created as 
part of [BioDivine model toolkit](http://foo).*

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

*!!! Specification section contains all technical details of the project. You can define you own sections based on the
project you are proposing. The only mandatory section are outputs. However, we recommend you at least formally
define the problem you are solving (define inputs, expected properties, ), the proposed solution
 (algorithm pseudo-code, data relationships, chosen tools and technologies) and sketch some details of the solution implementation
(define interfaces)

The content in it is mostly optional 
(except for Outputs), but we recommend giving as much information as possible in order to fully specify
what, how and why should be implemented.*

### Preliminaries

*!!! OPTIONAL: List of formal definitions and notations which is used to describe the project. Example: Define
a boolean network, define *

### Outputs
 