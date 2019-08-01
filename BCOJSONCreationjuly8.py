# import packages
import json
import datetime
import BCO_Conformance_Tool
import os



# The method is called to create a variable to make a dictionary
def createBaseDictionary():
    BaseBCODict = {
        "bco_id": "",
        "bco_spec_version": "",
        "checksum": ""
    }
    return BaseBCODict


# This asks users for the top level information and returns it as a list
def createTopLevel():
    # BCO ID
    bcoID = input("What is the BCO ID: ")

    # BCO Spec id
    bcoSpec = input("What is the BCO Spec Version (URL): ")
    return [bcoID, bcoSpec]


# provenance domain area
def createProvenanceDomain(inputBCODict):
    # establish key lists
    prov_reviewer_keys = ['name', 'affiliation', 'email', 'contribution']
    prov_review_keys = ['status', 'reviewer_comment', 'date', 'reviewer']
    prov_contributors_keys = ['name', 'affiliation', 'email', 'contribution']
    prov_domain_keys = ['name', 'version', 'review','derived_from', 'obsolete_after', 'embargo', 'created', 'modified', 'contributors', 'license']

    prov_domain_name = input("Input BCO name: ")
    prov_domain_version = input("Input Version Number: ")

    prov_review_values = []
    while True:
        prov_review_status = input("Input Status of BCO: ")
        while prov_review_status not in {"unreviewed", "in-review", "approved", "rejected", "suspended"}:
            print("Please input one of the following: unreviewed, in-review, approved, rejected or suspended")
            prov_review_status = input("Input Status of BCO: ")
        prov_review_comment = input("Leave any comment here: ")
        prov_review_date = datetime.datetime.now().isoformat()
        prov_reviewer_name = input("Input Reviewer Name: ")
        prov_reviewer_affiliation = input("Input reviewer affiliation: ")
        prov_reviewer_email = input("Input reviewer Email: ")
        prov_reviewer_contribution = input("Input contributions separated by ',' : ")
        prov_reviewer_contribution = prov_reviewer_contribution.split(",")
        prov_reviewer_contribution = [x.strip(' ') for x in prov_reviewer_contribution]
        continue_input = input("Do you wish to add another review? (Y/N) : ")
        while continue_input.upper() not in {"Y", "N"}:
            print("Invalid input. Input Y or N")
            continue_input = input("Do you wish to add another review? (Y/N) : ")
        if continue_input.upper() == "Y":
            temp_reviewer_values = [prov_reviewer_name, prov_reviewer_affiliation, prov_reviewer_email,
                                    prov_reviewer_contribution]
            temp_reviewer_dict = dict(zip(prov_reviewer_keys, temp_reviewer_values))
            temp_review_values = [prov_review_status, prov_review_comment, prov_review_date, temp_reviewer_dict]
            temp_review_dict = dict(zip(prov_review_keys, temp_review_values))
            prov_review_values.append(temp_review_dict)
        else:
            temp_reviewer_values = [prov_reviewer_name, prov_reviewer_affiliation, prov_reviewer_email,
                                    prov_reviewer_contribution]
            temp_reviewer_dict = dict(zip(prov_reviewer_keys, temp_reviewer_values))
            temp_review_values = [prov_review_status, prov_review_comment, prov_review_date, temp_reviewer_dict]
            temp_review_dict = dict(zip(prov_review_keys, temp_review_values))
            prov_review_values.append(temp_review_dict)
            break

    has_derived_from = input("Do you have a reference this BCO is derived from? (Y/N): ")
    while has_derived_from.upper() not in {"Y", "N"}:
        print("Invalid input. Input Y or N")
        has_derived_from = input("Do you have a reference this BCO is derived from? (Y/N): ")
    if has_derived_from.upper() == "Y":
        prov_derived_from = input("Please enter where this BCO is derived from: ")
    else:
        prov_derived_from = ""

    has_obsolete_after = input("Does this have an expiration date? (Y/N): ")
    while has_obsolete_after.upper() not in {"Y", "N"}:
        print("Invalid input. Input Y or N")
        has_obsolete_after = input("Does this have an expiration date? (Y/N): ")
    if has_obsolete_after.upper() == "Y":
        prov_obsolete_after = input("Input expiration Date: ")
    else:
        prov_obsolete_after = ""

    has_embargo = input("Does this have a time period it cannot be public? (Y/N): ")
    while has_embargo.upper() not in {"Y", "N"}:
        print("Invalid input. Input Y or N")
        has_embargo = input("Does this have a time period it cannot be public? (Y/N): ")
    if has_embargo.upper() == "Y":
        prov_embargo_keys = ['start_time', 'end_time']
        prov_embargo_start = input("Input Embargo Start Date: ")
        prov_embargo_end = input("Input Embargo End Date: ")
        prov_embargo_values = [prov_embargo_start, prov_embargo_end]
        embargo_dict = dict(zip(prov_embargo_keys, prov_embargo_values))
    else:
        embargo_dict = ""

    prov_domain_created = datetime.datetime.now().isoformat()
    prov_domain_modified = datetime.datetime.now().isoformat()

    prov_contributor_values = []
    while True:
        prov_contributor_name = input("Input contributor name: ")
        prov_contributor_affiliation = input("Input contributor affiliation: ")
        prov_contributor_email = input("Input contributor email: ")
        prov_contributor_contribution = input("Input contributor contributions spereated by a ',' : ")
        prov_contributor_contribution = prov_contributor_contribution.split(",")
        prov_contributor_contribution = [x.strip(' ') for x in prov_contributor_contribution]
        continue_input = input("Do you wish to add another contributor? (Y/N) : ")
        while continue_input.upper() not in {"Y", "N"}:
            print("Invalid input. Input Y or N")
            continue_input = input("Do you wish to add another review? (Y/N) : ")
        if continue_input.upper() == "Y":
            temp_contributor_values = [prov_contributor_name, prov_contributor_affiliation, prov_contributor_email,
                                       prov_contributor_contribution]
            temp_contributor_dict = dict(zip(prov_contributors_keys, temp_contributor_values))
            prov_contributor_values.append(temp_contributor_dict)
        else:
            temp_contributor_values = [prov_contributor_name, prov_contributor_affiliation, prov_contributor_email,
                                       prov_contributor_contribution]
            temp_contributor_dict = dict(zip(prov_contributors_keys, temp_contributor_values))
            prov_contributor_values.append(temp_contributor_dict)
            break

    prov_domain_license = input("Input License: ")

    # Create Prov Dictonary
    prov_domain_values = [prov_domain_name, prov_domain_version, prov_review_values,prov_derived_from,
                          prov_obsolete_after, embargo_dict, prov_domain_created,
                          prov_domain_modified, prov_contributor_values, prov_domain_license]
    prov_dict = dict(zip(prov_domain_keys, prov_domain_values))
    prov_dict = {"provenance_domain" : prov_dict}
    inputBCODict.update(prov_dict)
    return inputBCODict


# Usability Domain Area
def createUsabilityDomain(inputBCODict):
    userInput = input("Please add one sentence on usability to increase searchability: ")
    use_values = [userInput]
    continueInput = input("Do you wish to add more? (Y/N): ")
    while True:
        if continueInput.upper() == 'Y':
            userInput = input("Please add one sentence on usability to increase searchability: ")
            use_values.append(userInput)
            continueInput = input("Do you wish to add more? (Y/N): ")
        elif continueInput.upper() == 'N':
            break
        else:
            print('Invalid input! Please Enter Y or N')
            continueInput = input("Do you wish to add more? (Y/N): ")
    # update the Dictionary
    inputBCODict.update({
        'usability_domain': use_values
    })
    return inputBCODict


# Description Domain Area
def createDescriptionDomain(inputBCODict):
    desc_domain_keys = ['keywords', 'xref', 'platform', 'pipeline_steps']
    desc_xref_keys = ['namespace', 'name', 'ids', 'access_time']
    desc_pipeline_keys = ['step_number', 'name', 'description', 'version', 'prerequisites', 'input_list', 'output_list']
    dsec_prereq_keys = ['name', 'uri']

    desc_keywords_value = input("Input pipeline keywords separated by a ',': ")
    desc_keywords_value = desc_keywords_value.split(",")
    desc_keywords_value = [x.strip(' ') for x in desc_keywords_value]

    isXref = input("Do you wish to add a Xref (Y/N): ")
    desc_xref_values = []
    while True:
        while isXref.upper() not in {"Y", "N"}:
            print("Invalid input. Input Y or N")
            isXref = input("Do you wish to add a Xref (Y/N): ")

        if isXref.upper() == "Y":
            desc_namespace_value = input("Input namespace: ")
            desc_name_value = input("Input name: ")
            desc_ids_value = input("Input Ids seperated by ',' : ")
            desc_ids_value = desc_ids_value.split(",")
            desc_ids_value = [x.strip(' ') for x in desc_ids_value]
            desc_accesstime_value = input("Input access time: ")
            temp_xref_values = [desc_namespace_value, desc_name_value, desc_ids_value,
                                    desc_accesstime_value]
            temp_xref_dict = dict(zip(desc_xref_keys, temp_xref_values))
            desc_xref_values.append(temp_xref_dict)

            isXref = input("Do you wish to add a Xref (Y/N): ")
        else:
            break

    desc_platform_values = input("Input platforms you are able to use separated by a ',': ")
    desc_platform_values = desc_platform_values.split(",")
    desc_platform_values = [x.strip(' ') for x in desc_platform_values]

    desc_pipline_values = []
    desc_prereq_values = []
    desc_prereq_input_values = []
    desc_prereq_output_values = []
    desc_prereq_key = ['name', 'uri']
    desc_pipelinestep_num = 0
    isContinue = "Y"
    while(isContinue.upper() == "Y"):
        desc_pipelinestep_num = desc_pipelinestep_num+1
        desc_pipe_step_value = desc_pipelinestep_num
        desc_pipe_name_value = input("Input name of pipeline step " + str(desc_pipe_step_value) + " : ")
        desc_pipe_description_value = input("Input description of pipeline step " + str(desc_pipe_step_value) + " : ")
        desc_pipe_ver_value = input("Input version of pipeline step " + str(desc_pipe_step_value) + " : ")
        haveprereq = input("Does pipeline step " + str(desc_pipe_step_value) + " have prerequisites? (Y/N): ")
        while haveprereq.upper() not in {"Y", "N"}:
            print("Invalid input. Input Y or N")
            haveprereq = input("Does pipeline step " + str(desc_pipe_step_value) + " have prerequisites? (Y/N): ")
        while(haveprereq.upper()=="Y"):
            desc_prereq_name_value = input("Input name of prerequisite: ")
            desc_prereq_uri_value = input("Input uri/urn: ")
            temp_prereq_uri_dict = {'uri': desc_prereq_uri_value}
            temp_prereq_value = [desc_prereq_name_value,temp_prereq_uri_dict]
            temp_desc_prereq_values = dict(zip(desc_prereq_key, temp_prereq_value))
            desc_prereq_values.append(temp_desc_prereq_values)
            haveprereq = input("Do you want to enter another prerequisites? (Y/N): ")
            while haveprereq.upper() not in {"Y", "N"}:
                print("Invalid input. Input Y or N")
                haveprereq = input("Do you want to enter another prerequisites? (Y/N): ")
        while True:
            desc_input_type_value = input("Input the Input type (URI/URN): ")
            while desc_input_type_value.upper() not in {"URI", "URN"}:
                print("Invalid input. Input URI or URN")
                desc_input_type_value = input("Input the Input type (URI/URN): ")
            if desc_input_type_value == "URI":
                uri_input = input("Input URI: ")
                temp_input_value = {'uri': uri_input}
                desc_prereq_input_values.append(temp_input_value)
            elif desc_input_type_value == "URN":
                urn_input = input("Input URN: ")
                temp_input_value = {'urn': urn_input}
                desc_prereq_input_values.append(temp_input_value)
            inputContinue = input("Do you wish to add another input? (Y/N)? : ")
            while inputContinue.upper() not in {"Y", "N"}:
                print("Invalid input. Input Y or N")
                inputContinue = input("Do you wish to add another input? (Y/N)? : ")
            if inputContinue.upper() == "N":
                break
        while True:
            desc_output_type_value = input("Input the Output type (URI/URN): ")
            while desc_input_type_value.upper() not in {"URI", "URN"}:
                print("Invalid input. Input URI or URN")
                desc_output_type_value = input("Input the Output type (URI/URN): ")
            if desc_output_type_value == "URI":
                uri_output = input("Output URI: ")
                temp_output_value = {'uri': uri_output}
                desc_prereq_output_values.append(temp_output_value)
            elif desc_output_type_value == "URN":
                urn_output = input("Output URN: ")
                temp_output_value = {'urn': urn_output}
                desc_prereq_output_values.append(temp_output_value)
            inputContinue = input("Do you wish to add another Output? (Y/N)? : ")
            while inputContinue.upper() not in {"Y", "N"}:
                print("Invalid input. Input Y or N")
                inputContinue = input("Do you wish to add another Output? (Y/N)? : ")
            if inputContinue.upper() == "N":
                break
        temp_desc_pipeline_value = [desc_pipe_step_value, desc_pipe_name_value, desc_pipe_description_value,
                               desc_pipe_ver_value, desc_prereq_values, desc_prereq_input_values,
                               desc_prereq_output_values]
        temp_pipeline_dict = dict(zip(desc_pipeline_keys, temp_desc_pipeline_value))
        desc_pipline_values.append(temp_pipeline_dict)

        isContinue = input("Do you wish to add another pipeline? (Y/N)? : ")
        while isContinue.upper() not in {"Y", "N"}:
            print("Invalid input. Input Y or N")
            isContinue = input("Do you wish to add another pipeline? (Y/N)? : ")


    desc_domain_values = [desc_keywords_value,desc_xref_values,desc_platform_values,desc_pipline_values]
    desc_domain_dict = dict(zip(desc_domain_keys, desc_domain_values))

    inputBCODict.update({
        'description_domain': desc_domain_dict
    })
    return inputBCODict

def createExecutionDomain(inputBCODict):
    exec_domain_keys = ['script', 'script_driver', 'software_prerequisites', 'external_data_endpoints',
                          'environment_variables']
    exec_software_prereq_keys = ['name', 'version', 'uri']
    exec_external_keys = ['name', 'url']
    exec_enviromental_keys = ['type', 'value']

    exec_script_values = []
    while True:
        exec_script_type = input("Input the Script type (URI/URN): ")
        while exec_script_type.upper() not in {"URI", "URN"}:
            print("Invalid input. Input URI or URN")
            exec_script_type = input("Input the Script type (URI/URN): ")
        if exec_script_type.upper() == "URI":
            uri_input = input("Input URI: ")
            temp_script_value = {'uri': uri_input}
            exec_script_values.append(temp_script_value)
        elif exec_script_type.upper() == "URN":
            urn_input = input("Input URN: ")
            temp_script_value = {'urn': urn_input}
            exec_script_values.append(temp_script_value)
        inputContinue = input("Do you wish to add another script? (Y/N)? : ")
        while inputContinue.upper() not in {"Y", "N"}:
            print("Invalid input. Input Y or N")
            inputContinue = input("Do you wish to add another script? (Y/N)? : ")
        if inputContinue.upper() == "N":
            break

    exec_driver_value = input("Input script driver: ")

    exec_prereq_values = []
    exec_prereq_uri_values = []
    while True:
        exec_software_name_value = input("Input name of software: ")
        exec_software_ver_value = input("Input version of software: ")
        exec_software_type = input("Input the Software type (URI/URN): ")
        while exec_software_type.upper() not in {"URI", "URN"}:
            print("Invalid input. Input URI or URN")
            exec_software_type = input("Input the Script type (URI/URN): ")
        if exec_software_type.upper() == "URI":
            uri_input = input("Input URI: ")
            exec_prereq_uri_values = {'uri': uri_input}
        elif exec_software_type.upper() == "URN":
            urn_input = input("Input URN: ")
            exec_prereq_uri_values = {'urn': urn_input}

        temp_software_prereq_values = [exec_software_name_value, exec_software_ver_value, exec_prereq_uri_values]
        temp_software_prereq_values = dict(zip(exec_software_prereq_keys, temp_software_prereq_values))
        exec_prereq_values.append(temp_software_prereq_values)
        inputContinue = input("Do you wish to add another software prereq? (Y/N)? : ")
        while inputContinue.upper() not in {"Y", "N"}:
            print("Invalid input. Input Y or N")
            inputContinue = input("Do you wish to add another software prereq? (Y/N)? : ")
        if inputContinue.upper() == "N":
            break

    exec_external_values = []
    while True:
        exec_external_name = input("Input name of external endpoint: ")
        exec_external_url = input("Input url to external endpoint: ")
        temp_external_val = [exec_external_name, exec_external_url]
        temp_pipeline_dict = dict(zip(exec_external_keys, temp_external_val))
        exec_external_values.append(temp_pipeline_dict)
        inputContinue = input("Do you wish to add another external data endpoint? (Y/N)? : ")
        while inputContinue.upper() not in {"Y", "N"}:
            print("Invalid input. Input Y or N")
            inputContinue = input("Do you wish to add another external data endpoint? (Y/N)? : ")
        if inputContinue.upper() == "N":
            break

    exec_env_type_value = input("Input type of environmental variable: ")
    exec_env_val_value = input("Input value of environmental variable: ")
    exec_env_values_temp = {exec_env_type_value : exec_env_val_value}
    exec_env_values = {"environmental_variables": exec_env_values_temp}

    exec_domain_values = [exec_script_values, exec_driver_value, exec_prereq_values, exec_external_values,
                          exec_env_values]
    exec_domain_dict = dict(zip(exec_domain_keys, exec_domain_values))
    inputBCODict.update({
        'execution_domain': exec_domain_dict
    })
    return inputBCODict

# broken
def createParametricDomain(inputBCODict):
    para_domain_keys = ['param', 'value', 'step']
    para_values = []
    while True:
        para_param_value = input("Input param value: ")
        para_val_value = input("Input value: ")
        para_step_value = input("Input step value: ")
        temp_para_values = [para_param_value, para_val_value, para_step_value]
        temp_dict = dict(zip(para_domain_keys, temp_para_values))
        para_values.append(temp_dict)
        inputContinue = input("Do you wish to add another parameter? (Y/N)? : ")
        while inputContinue.upper() not in {"Y", "N"}:
            print("Invalid input. Input Y or N")
            inputContinue = input("Do you wish to add another parameter? (Y/N)? : ")
        if inputContinue.upper() == "N":
            break

    inputBCODict.update({
        'parametric_domain': para_values
    })
    return inputBCODict

def createIODomain(inputBCODict):
    IO_domain_keys = ["input_subdomain", "output_subdomain"]
    IO_out_subdom_keys = ["mediatype", "uri"]

    IO_in_subdom_values = []
    while True:
        IO_in_subdom_type = input("Input the IO sub domain type (URI/URN): ")
        while IO_in_subdom_type.upper() not in {"URI", "URN"}:
            print("Invalid input. Input URI or URN")
            IO_in_subdom_type = input("Input the IO sub domain type (URI/URN): ")

        if IO_in_subdom_type.upper() == "URI":
            uri_input = input("Input URI: ")
            IO_value = {'uri': uri_input}
        elif IO_in_subdom_type.upper() == "URN":
            urn_input = input("Input URN: ")
            IO_value = {'urn': urn_input}
        IO_in_subdom_values_temp = {'uri': IO_value}
        IO_in_subdom_values.append(IO_in_subdom_values_temp)
        inputContinue = input("Do you wish to add another? (Y/N)? : ")
        while inputContinue.upper() not in {"Y", "N"}:
            print("Invalid input. Input Y or N")
            inputContinue = input("Do you wish to add another? (Y/N)? : ")
        if inputContinue.upper() == "N":
            break



    IO_out_subdom_values = []
    while True:
        IO_out_mediatype = input("Input mediatype: ")

        IO_in_subdom_type = input("Input the IO sub domain type (URI/URN): ")
        while IO_in_subdom_type.upper() not in {"URI", "URN"}:
            print("Invalid input. Input URI or URN")
            IO_in_subdom_type = input("Input the IO sub domain type (URI/URN): ")
        if IO_in_subdom_type.upper() == "URI":
            uri_input = input("Input URI: ")
            IO_value = {'uri': uri_input}
        elif IO_in_subdom_type.upper() == "URN":
            urn_input = input("Input URN: ")
            IO_value = {'urn': urn_input}

        IO_out_val = [IO_out_mediatype, IO_value]
        IO_out_subdom__dict = dict(zip(IO_out_subdom_keys, IO_out_val))
        IO_out_subdom_values.append(IO_out_subdom__dict)

        inputContinue = input("Do you wish to add another? (Y/N)? : ")
        while inputContinue.upper() not in {"Y", "N"}:
            print("Invalid input. Input Y or N")
            inputContinue = input("Do you wish to add another? (Y/N)? : ")
        if inputContinue.upper() == "N":
            break

    IO_domain_values = [IO_in_subdom_values, IO_out_subdom_values]
    IO_out_dict = dict(zip(IO_domain_keys, IO_domain_values))
    inputBCODict.update({
        'io_domain': IO_out_dict
    })
    return inputBCODict

def createErrDomain(inputBCODict):
    Err_domain_keys = ['empirical_error','algorithmic_error']
    emp_err_input = input("Input empirical Error: ")
    emp_dict = {'comment' : emp_err_input}
    alg_err_input = input("Input algorithmic error: ")
    alg_dict = {'log_filename' : alg_err_input}
    Err_domain_vals = [emp_err_input,alg_err_input]
    errDomain_dict = dict(zip(Err_domain_keys, Err_domain_vals))
    inputBCODict.update({
        'error_domain': errDomain_dict
    })
    return inputBCODict

# delete empty keys
#def remove_empties_from_dict(a_dict):
#    new_dict = {}
#   for k, v in a_dict.items():
#        if isinstance(v, list):
#            v = remove_empties_from_dict(v)
#        if v is not "":
#           new_dict[k] = v
#    return new_dict or None


# Main program to call other functions
def main():
    # This is the creation of the Dictionary
    BCODict = createBaseDictionary()
    # We grab this list so we can first make the checksum the recompile with this information
    topLevelList = createTopLevel()
    BCODict = createProvenanceDomain(BCODict)
    BCODict = createUsabilityDomain(BCODict)
    BCODict = createDescriptionDomain(BCODict)
    BCODict = createExecutionDomain(BCODict)
    includepara = input("Do you have a Parametric Domain to include? (Y/N): ")
    while includepara.upper() not in {"Y", "N"}:
        print("Invalid input. Input Y or N")
        includepara = input("Do you have a Parametric Domain to include? (Y/N): ")
    if includepara.upper() == "Y":
        BCODict = createParametricDomain(BCODict)
    BCODict = createIODomain(BCODict)
    BCODict = createErrDomain(BCODict)
    # This makes printable string from dictonary
#    BCODict = remove_empties_from_dict(BCODict)

    app_json = json.dumps(BCODict)
    print(app_json)

    # write to JSON  - I MODIFIED THIS TO MAKE IT A TEMPORARY FILE
    with open('BCO_Test.json', 'w') as json_file:
        json.dump(BCODict, json_file, indent=4)


    # this is additional code to
    filename = 'BCO_Test.json'
    with open(filename, 'r') as f:
        json_data = json.load(f)
    checksum = BCO_Conformance_Tool.JSONCheckSUM(json_data, 'BCO_Test', False)
    BCODict['checksum'] = checksum
    
    # write final JSON with checksum
    with open('BCO_Test.json', 'w') as json_file:
        json.dump(BCODict, json_file, indent=4)

    validate_status = input('Validate and Display BCO? (Y/N): ')

    if validate_status.upper() == 'Y':
        BCO_Conformance_Tool.main('BCO_Test.json')

# Run the python code
if __name__ == "__main__":
    main()
