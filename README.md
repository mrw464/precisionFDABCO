# precisionFDABCO
This is the Deloitte submission to the precisionFDA App-a-Thon BCO Challenge:
https://github.com/biocompute-objects/PrecisionFDA_App-a-thon/tree/master/

This submission adheres to the following version of the BCO specification;
https://github.com/biocompute-objects/PrecisionFDA_App-a-thon/tree/master/base_schema

**Requirements:

* Docker (Container is built using a Linux image)
* Python 3.7+

**Additional Python libraries:

* bioblend==0.12.0
* jsonschema==3.0.1
* Pygments==2.4.2
* beautifulsoup4==4.8.0

**Tools included:

* BCO Conformance Tool - This tool validates JSON files against the BCO Schema and displays the result via HTML.
* BCO Writer Tool - This tool assists with the creation of a BCO JSON file (including importing a Galaxy workflow). This tool also can leverage the Conformance Tool to validate and display the created BCO file.

**Instructions:

- Build the docker image using the dockerfile
- The docker container will open 



