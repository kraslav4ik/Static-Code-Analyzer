# Static Code Analyzer
Tool for searching the most common syntax mistakes:
* Indentation
* TODO comments
* Blank lines
* Variable, functions, class names
* Mutable variables in function args
* Default arguments values

Program takes path to directory, containing python files or path to python file and checks if ".py" files has the most wide-spread syntax mistakes

Works with: Python 3.8

```bash
Static-Code-Analyzer/> pip install -r ./requrements.txt
```

Run analyzer:

```bash
Static-Code-Analyzer/> python ./analyzer/code-analyzer.py
```

Run tests:

```bash
Static-Code-Analyzer/> python ./test/tests.py
```

Tests are provided by JetBrains Academy

Project made as a part of JetBrains Academy course 

https://hyperskill.org/projects/112?category=1&track=2 
