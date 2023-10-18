# from https://tex.stackexchange.com/a/40759/297129


.PHONY: fractal-art.pdf all clean

all: fractal-art.pdf

%.tex: %.raw
	./raw2tex $< > $@

%.tex: %.dat
		./dat2tex $< > $@

fractal-art.pdf: fractal-art.tex
		latexmk -pdf -pdflatex="pdflatex -interaction=nonstopmode" -use-make fractal-art.tex

clean:
	latexmk -CA