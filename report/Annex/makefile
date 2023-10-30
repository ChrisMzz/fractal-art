# from https://tex.stackexchange.com/a/40759/297129


.PHONY: frctl-art-annex.pdf all clean

all: frctl-art-annex.pdf

%.tex: %.raw
	./raw2tex $< > $@

%.tex: %.dat
		./dat2tex $< > $@

frctl-art-annex.pdf: frctl-art-annex.tex
		latexmk -pdf -pdflatex="pdflatex -interaction=nonstopmode" -use-make frctl-art-annex.tex

clean:
	latexmk -CA