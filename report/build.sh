pandoc -S -N --template=report.template --bibliography=references.bib -o report.pdf report.md
open report.pdf
