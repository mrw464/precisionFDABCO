# -*- coding: utf-8 -*-
# version 0.7 - 7/18/19
# import the neccessary libraries
# required libraries: sys, json, jsonschema, hashlib, os, re, pygments, beautifulsoup version 4

import sys
import json
import jsonschema
from jsonschema import validate
import hashlib
import os
import re
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from pygments.formatters import TerminalFormatter
from bs4 import BeautifulSoup
import webbrowser

def validate_BCO(BCO_filename):
    with open('BCOSchema_modified.json') as schema_file:  
        schema = json.load(schema_file)
        try:
            with open(BCO_filename) as json_file:
                try:
                    print(f'Testing {json_file.name} for BCO conformance...')
                    data = json.load(json_file)
                    url_name = createHTMLOutput(BCO_filename[:-5], data)
                    try:
                        validate(data, schema)
                        JSONCheckSUM(data, BCO_filename, True)
                        print("Valid BCO")
                        return True, data
                    except jsonschema.exceptions.ValidationError as ve:
                        print('Checkpoint validation error as vs')
                        errorHandle(ve, url_name)
                        return False, data
                        
                except ValueError as err:
                    print(f"JSON formatting error:\n{err}")
                    return False, None
        except:
            print(f'{BCO_filename} not found.')
            return False, None

def windowDressing(soup):
    heading_string = '''The BCO Display Tool displays the 
    BCO-schema JSON file below. Errors are highlighted in yellow, if present.'''

    tag = soup.find('h2')
    tag.string = 'Biocompute Objects (BCO) Display'
    description_tag = soup.new_tag('span')
    description_tag.string = heading_string
    tag.insert_after(description_tag)

    tag = soup.find(text=heading_string)
    break_tag = soup.new_tag('br')
    status_tag = soup.new_tag('span')
    status_tag.attrs['class'] = 'success'
    status_tag.string = 'BCO COMPLIANCE: SUCCESS'
    tag.insert_after(break_tag)
    break_tag2 = soup.new_tag('br')
    break_tag.insert_after(break_tag2)
    break_tag2.insert_after(status_tag)

    
    return soup

def additionalPropCheck(ve):            
    i = re.compile(r"(?:').*(?:')")
    p = re.search(i, ve.message)
    p = p[0]
    p = p[1:-1]
    return p

def patternFailLookup(ve):            
    i = re.compile(r"'(\w+)'")
    p = re.search(i, ve.message)
    p = p[0]
    p = p[1:-1]
    return p

def JSONCheckSUM(data, BCO_filename, validation):
    if validation == True:
        providedCheckSUM = data['checksum']
    data.pop('checksum', None)
    data.pop('bco_id', None)
    data.pop('bco_spec_version', None)
    temp_json_name = 'tempjson_' + BCO_filename
    with open(temp_json_name,"w") as f:
        json.dump(data,f,indent=4)
    f.close()
    sha256_hash = hashlib.sha256()

    with open(temp_json_name,"rb") as f:
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
    f.close()
    os.remove(temp_json_name)

    if validation == True:
        print(f'Provided SHA-256 Hash: {providedCheckSUM}')
        print(f'Calculated SHA-256 Hash: {sha256_hash.hexdigest()}')
        if providedCheckSUM == sha256_hash.hexdigest():
            print('SHA 256 checksum is valid.')
        else:
            print('SHA 256 checksum is invalid.')
    else:
        return sha256_hash.hexdigest()



def main(json_file=None):

    if json_file is not None:
        validate_BCO(json_file)
        url = json_file[:-5] + '_output.html'
        webbrowser.open(url)

    else:
        BCO_to_validate = input('What is the name of the BCO json file to validate? (ex. BCOfile.json)\n')
        validate_BCO(BCO_to_validate)
        url = BCO_to_validate[:-5] + '_output.html'
        webbrowser.open(url)


def errorHandle(ve, url_name):

    print(f"Error message validator: {ve.validator}")
    print(f"Error message validator value: {ve.validator_value}")
    print(f"Invalid BCO.\nError:\n{ve.message}")
    print(f"Error relative path: {ve.relative_path}\n")
    if ve.validator_value is not False:
        checkForErrorMessage(ve.validator_value)
    relativePathLength = len(ve.relative_path)
    print(f'relativepathlength: {relativePathLength}')
    if relativePathLength > 1:
        if 'is not of type' in ve.message:
            errorOutput(ve.relative_path[-1], ve, url_name, ve.relative_path[-2])
        elif 'does not match' in ve.message:
            look_up = patternFailLookup(ve)
            errorOutput(look_up, ve, url_name)
        elif ve.validator == 'additionalProperties':
            look_up = additionalPropCheck(ve)
            errorOutput(look_up, ve, url_name)
        else:
            for i in ve.validator_value:
                if i in ve.message:
                    instance_number = ve.relative_path[-1]
                    errorOutput(i, ve, url_name, instance_number)
    elif relativePathLength == 1:
        print('relative path lengh DOES equal 1')
        print(f'lookup word for this: {ve.relative_path[0]}')
        errorOutput(ve.relative_path[0], ve, url_name)
        
    else:
        if 'does not match' in ve.message:
            look_up = patternFailLookup(ve)
            errorOutput(look_up, ve, url_name)
        elif ve.validator == 'additionalProperties':
            look_up = additionalPropCheck(ve)
            errorOutput(look_up, ve, url_name)

        else:    
            for i in ve.validator_value:
                if i in ve.message:
                    index = ve.validator_value.index(i)
                    index += 1
                    if index > len(ve.validator_value):
                        index = -1
                    next_item_for_root_level = ve.validator_value[index]
                    errorOutput(next_item_for_root_level, ve, url_name) 

    


    print('\n-----------\n')



def createHTMLOutput(BCO_filename, jsondata):
    formatted_json = json.dumps(jsondata, indent=4)
    url_name = BCO_filename + '_output.html'
    with open(url_name,"w") as p:
        highlight(formatted_json, JsonLexer(), HtmlFormatter(style='tango', full=True), outfile=p)
        p.close()
    with open(url_name) as p:
        soup = BeautifulSoup(p.read(), features='html.parser')
        soup = windowDressing(soup)
    
    success_highlight_css = '.success {background-color: lime;}'

    soup.style.string = soup.style.string + success_highlight_css

    new_text = soup.prettify()

    with open(url_name, mode='w') as new_html_file:
        new_html_file.write(new_text)

    return url_name



def errorOutput(lookup_word, ve, url_name, instance_number=None):

    print('entering error output test')
    print(f'lookup word: {lookup_word}')
    print(f've: {ve}')
    print(f'url name: {url_name}')
    print(f've.message: {ve.message}')
    print(f'instance_number: {instance_number}')

    def createErrorTag(error):
        new_tag = soup.new_tag("b")
        new_tag.attrs['class'] = 'error'
        error = "ERROR: " + error + ' --> '
        new_tag.string=error
        return new_tag

    def appendTag(error, currentTag):
        errorTag = createErrorTag(error)
        currentTag.insert_before(errorTag)
        


    with open(url_name) as html_file:
        soup = BeautifulSoup(html_file.read(), features='html.parser')

        if instance_number is not None and isinstance(instance_number, int):

            tag = soup.find_all(text=re.compile(lookup_word))

            if tag == []:

                for tag in soup.find_all(text=re.compile(ve.relative_path[-2])):
                    tag = tag.parent
                    tag['class'] = 'error'
                    appendTag(ve.message, tag)


            else:
                tag = tag[instance_number]
                tag = tag.parent
                tag['class'] = 'error'
                appendTag(ve.message, tag)
        else:
            for tag in soup.find_all(text=re.compile(lookup_word)):
                tag = tag.parent
                tag['class'] = 'error'
                appendTag(ve.message, tag)
                

                

    error_highlight_css = '.error {background-color: yellow;}'

    soup.style.string = soup.style.string + error_highlight_css

    status_tag = soup.find("span", {"class": "success"})
    status_tag.attrs['class'] = 'error'
    status_tag.string.replace_with('BCO COMPLIANCE: FAILED')
    
    new_text = soup.prettify()

    with open(url_name, mode='w') as new_html_file:
        new_html_file.write(new_text)
        new_html_file.close()
    




     


def checkForErrorMessage(validator_value):
    if len(validator_value[0]) == 1:
        valueToCheck = ''.join(str(v) for v in validator_value)
    else:
        valueToCheck = validator_value[0]
    if valueToCheck in errorMessages:
        print(errorMessages[valueToCheck])

# dictionary of error messages
errorMessages = {
    '^((h|H)(t|T)(t|T)(p|P)(s?|S?)://)|((u|U)(r|R)(n|N):(u|U)(u|U)(i|I)(d|D):)' : 
        'URI not in HTTP(s):// or URN:UUID: format',
    '^((h|H)(t|T)(t|T)(p|P)(s?|S?)://)' :
        'URL does not follow the proper format. (Does not begin with http:// or https://)',
    '[a-zA-Z].*:(/?/?).*' :
        'URI does not conform to the URI standard (prefix:location)'
}



if __name__== "__main__":
  main()


