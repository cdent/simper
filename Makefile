
clean:
	find . -name "*.pyc" -exec rm {} \;

realclean: clean
	rm content.db

