# precisionFDABCO

This is the Deloitte submission to the precisionFDA App-a-Thon BCO Challenge:
https://github.com/biocompute-objects/PrecisionFDA_App-a-thon/tree/master/

This submission adheres to the following version of the BCO specification;
https://github.com/biocompute-objects/PrecisionFDA_App-a-thon/tree/master/base_schema

**This software is licensed under the MIT License:**
Copyright 2019 Deloitte Consulting

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



**Requirements:**

* Docker (Container is built using a Linux image)
* Python 3.7+

**Additional Python libraries:**

* bioblend==0.12.0
* jsonschema==3.0.1
* Pygments==2.4.2
* beautifulsoup4==4.8.0

**Tools included:**

* BCO Conformance Tool - This tool validates JSON files against the BCO Schema and displays the result via HTML.
* BCO Writer Tool - This tool assists with the creation of a BCO JSON file (including importing a Galaxy workflow). This tool also can leverage the Conformance Tool to validate and display the created BCO file.

**General Instructions:**

- Build the docker image using the dockerfile
- The docker container will open the Conformance Tool and Writer Tool by default. Otherwise, start the BCO_Writer_Tool.py via the terminal/command-line to initiate the BCO writer tool or start the BCO_Conformance_Tool.py to validate/display a BCO JSON file.

**Writer Tool Instructions:**

- Use the command line to provide inputs for the BCO Writer Tool
- The Writer Tool may import a Galaxy Workflow:
  - Provide the Galaxy instance URL (e.g. "https://usegalaxy.org/" including closing brackets) as well as an API key and the specific workflow ID number
- The Writer Tool will provide the option at the final prompt to validate/display the BCO. This will create a BCO_Output_Output.html file that will be automatically opened by the default web browser, if one is available.
- The Writer Tool will generate a BCO_Output.json as an output

**Conformance Tool Instructions:**

- The Conformance Tool may be run independently via the command line by running the BCO_Conformance_Tool.py script
- Place a BCO-schema JSON file in the same directory as the BCO_Conformance_Tool.py script
- Input the name of the BCO file to be tested (e.g. 'test.json')
- The Conformance Tool will provide some error feedback via the command line and if there are no basic JSON formatting errors, will launch an HTML page displaying the BCO's as well as information regarding the validation (either Success or Fail)
  - If the file does not pass BCO conformance, the tool attempts to provide the location of the error highlighted in yellow with an error message
- The Conformance Tool will provide an HTML output if there are no JSON formatting errors - the HTML output is named (BCO_Name)_Output.html where BCO_Name is the provided BCO filename (i.e. test_Output.html)


