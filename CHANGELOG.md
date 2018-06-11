# Release History

## v0.7.0 --- Pre-release 10

This release contains a great deal of folder level restructuring, renaming, and settings.
Additionally, I transcribed my notes on __The 100__ and started adapting them; I also made changes based on suggestions from TeX linters.

### Appendices
- Moved all the appendices to their own folder.
- some explanations re: the list of quotations

### philopre.tex -> pre.tex
Changed the name because I'm lazy and it's less to type.

### wc.py -> digress.py
- changed name to better reflect scope
- `build` command
- `tokei` command: counts code using `tokei` (removed)
- `check` command: runs `lacheck` on all files
- `ls` + `log` commands: path argument
    + allows one to check specific folders for TeX files
- sort command to `ls`

### 'The Void'
- transcribed notes on __The 100__
- started adapting __The 100__ notes to essay form

### Misc
- added to sublime-project file the settings previously set by TEX directives
    + makes those settings more centralized and less susceptible human (me) error
- fixed random typos
- CHANGELOG.md contains all previous release notes
- various little changes based on `lacheck` and `chktex` suggestions
- line spacing is now 1.5 (better readability)
- new semantic command: `\tv` (just an alias for `\tvshow`)
- margin notes are single spaced now
- sentence cased the footnotes

## v0.6.1 --- Pre-Release 9

This release contains, _inter alia_, an environment for (hopefully) temporary notes, improvements/additions to the Mike Schur discussion, a new source, better monospaced font scaling, and some custom commands.

### `somenotes` Environment
- creates an unmarked subsection title 'Some Notes On: <arg>'
- used to store notes
- several have been created
    + modernism
    + post-modernism
    + __Brooklyn 99__
    + __Parks and Recreation__
    + __Speed Racer__
        * mainly comments on Film Crit Hulk articles
    + __Short Term 12__
    + __The 100__  
        * transcriptions, to be adapted

### New Sources
- __Origins of Postmodernism__ as a source
- Film Crit Hulk
    + three articles on __Speed Racer__
    + one article on __Short Term 12__

### New Commands
- `\digsec`, `\digsubsec`, `digsubsubsec`
    + custom section, subsection, and subsubsection commands
    + mandatory date and label arguments
    + replaced most built-in commands with the custom ones

### New Sections
- Sincerity -> History -> 'The Word "Modern"'
    + a section that will contain discussions re: modern is a word with meanings beyond art and that can be confusing
- Empathy -> 'Sympathy'

### Misc
- transition into Mike Schur section improved
- the history lesson is starting to get to the point
- slightly changed chapter title page format
- started work on a new introduction to 'The Void'
- added a post-intro note on the visual elements of __Speed Racer__
- started keeping track of the number of quotes used
- `log` command in wc.py
    + does a word count and saves it to counts.json
- a CHANGELOG.md file (this file)
- started using the semantics commands more
- Hack
    + set Hack to scale based on Spectral
        * `\ttfamily` and `\texttt` text looks more normal now
    + added a description to the 'About the Typeface' page
- requirements.txt file (for wc.py)

## v0.5.1 --- Pre-release 8

- new dislaimer re: tone
- moved around some stuff
    + mike schur section is now in 'sincerity'
- added some explanations to my top ten movies
- more immutability talk, esp. about the scope
- deleted old (commented out) font commands
- started actually working on the watch script (it can print out the word counts for each doc)
- added a bunch of todo notes
- added metadata
- minor changes to watch.py
- new todo command
    + prints argument w/in <> and monospace (Hack)
- margin note type explanation in introduction
    + each margin note now has a command controlling style
    + in the intro, each explanation is colored and styled like the corresponding note type
- random stats page
    + totals for each margin note type
    + total number of footnotes, meant adding a new footnote command/counter
- work on the empathy section

## v0.4.1 --- Pre-release 7

This release features changes to the main and monospace font, a new helper Python script, macros to control margin note colors, and other changes and additions.

### Fonts
- Main font changed to Spectral
- Mono font changed to Hack

## v0.3.0 --- Pre-release 6

In this release, even more quotation marks were replaced with the `\say` macro and the citation style was modified.

## v0.2.0 --- Pre-release 5

This release contains formatting changes for the sub-chapter level headings (section, subsection, and subsubsection) along with additions to the 'Semiotics' section of 'Knowledge'

### Semiotics
- clarification regarding why the section even exists at all
- cited Umberto Eco (new source)
- finished (to be edited) an introduction to semiotics
- started to approach the heart of unconscious signification

## v0.1.0 --- Pre-release 4

In this release, a new subsection was added in 'Knowledge' for a discussion of semiotics.

## v0.0.3 --- Pre-release 3

In this release most uses of quotation marks were replaced with the `\say` macro, __The Myth of Sisyphus__ was added to sources, a section was created for __The 100__, and other miscellaneous tweaks were made.

### Misc
- new footnote in the intro
- fixed a date in 'The Void'
- clarification in footnote 3 in 'Sincerity'

## v0.0.2 --- Pre-release 2

- Last trip entry
    + notes to the final trip entry

## v0.0.1 --- Pre-release 1

- first release
    + when I started doing releases
    + stopped pushing the pdf

