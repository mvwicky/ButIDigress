# Release History

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
