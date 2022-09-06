DOCS := $(patsubst %.md,%.pdf,$(wildcard *.md))

all : $(DOCS)

%.pdf : %.md
	pandoc $^ -t latex --top-level-division=section --number-sections -s -o $@

#%.tex : %.md
#	pandoc $^ -t latex --top-level-division=section --number-sections -s -o $@

#%.pdf : %.tex
#	pdflatex development.tex 

clobber :
	rm -f $(DOCS)
