
# getting the dictionary mapped/formatted to BCO-schema

def workflow_conversion(galaxyIP, galaxyAPIkey, workflowID):
    from bioblend.galaxy import GalaxyInstance
    import json
    import pprint
    from pathlib import Path
    import pathlib




    gi = GalaxyInstance(galaxyIP, key=galaxyAPIkey)
    libs = gi.libraries.get_libraries()




    gi.workflows.show_workflow(workflowID)

    workflow = gi.workflows.export_workflow_dict(workflowID)

    newworkflow = {}
    newworkflow['bco_id'] = workflow.pop('uuid', '')
    keywords = workflow.pop('tags', '')
    version = str(str(workflow['version']) + '.0')
    name = workflow.pop('name', '')
    newworkflow['provenance_domain'] = {"name": name, "version": version}


    pipeline_steps = []

    # defining sub-function for extracting step outputs (to be inputs for the next step)
    def output_extract(v):
        output = []
        if v.get('outputs', None) != None:

            output_list = v.get('outputs', None)
            if len(output_list) == 0:
                return                 

            if output_list == None:
                return
            for i in range(len(output_list)):
                output_item = output_list[i]
                output_item = str(output_item['name'] + '.' + output_item['type'])
                output_item = "file://localhost/" + output_item
                output_item = {"uri":output_item}               
                output = dict(output_item)
        return output

    for k, v in workflow['steps'].items():
        # k is a str, v is a dict
        step_dict = {}
        k = int(k)
        step_dict['name'] = v.pop('name', '')
        step_dict['description'] = v.pop('label', '')
        step_dict['version'] = v.pop('tool_version', '')
        step_dict['step_number'] = int(v.pop('id', ''))

        if k == 0:
            # the first step in a galaxy workflow always seems to be a user-defined dataset input
            # which is never provided in the workflow. So will have to have a placeholder URN here...
            # along the lines of urn:dataset:user_provided_dataset
            
            step_dict['input_list'] = [{"uri": "user_dataset"}]

            # extract output for next step
            output = output_extract(v)
            if output is not None:
                output = [output]
            elif output is None:
                output=[]
            step_dict['output_list'] = output

        elif k >= 1:    # pull from previous step output for steps after first
            step_dict['input_list'] = output             
            output = output_extract(v)
            if output is not None:
                output = [output]
            elif output is None:
                output = []    
            step_dict['output_list'] = output

        pipeline_steps.append(step_dict.copy()) 


    newworkflow['description_domain'] = {
        "keywords": [keywords],
        "platform": ["Galaxy"], 
        "pipeline_steps": pipeline_steps
    }

    software_preq = []
    for k, v in workflow['steps'].items():
        if v.get('tool_id', None) is not None:
            tool_shed = v.get('tool_shed_repository', '')
            if tool_shed != '':
                tool_name = tool_shed['name']
            tool_version = v.get('tool_version', '')
            tool_url = v.get('tool_id', '')
            if tool_url != '':
                if "http://" or "https://" not in str.startswith(tool_url, beg=0, end=7):
                    tool_url = "http://" + tool_url
                
            tool_uri = {"uri": tool_url}
            software_preq.append({"name": tool_name, "version": tool_version, "uri": tool_uri})

    script_name = str(name + '.ga')
    script_uri = str("file://localhost/" + script_name)
    script_uri_dict = {"uri": script_uri}
    newworkflow["execution_domain"] = {
        "script": script_uri_dict,
        "script_driver": "Galaxy",
        "software_prerequisites": software_preq

    }

    input_subdomain = {"uri": ""}
    output_subdomain = {"uri": "", "mediatype": ""}
    overall_input = dict(newworkflow['description_domain']["pipeline_steps"][0]['input_list'][0])
    input_subdomain['uri'] = overall_input['uri']
    step_length = int(len(newworkflow['description_domain']["pipeline_steps"]))
    step_length = step_length - 1
    overall_output = dict(newworkflow['description_domain']["pipeline_steps"][step_length]['output_list'][0])
    output_subdomain['uri'] = overall_output['uri']
    media_type_dict = {
    ".txt": "text/plain",
    ".json": "application/json",
    ".html": "text/html",
    ".tabular": "text/x-tabular",
    ".fasta": "text/x-fasta",
    ".input": "text/x-input",
    }

    file_extension = Path(overall_output["uri"]).suffix
    if file_extension in media_type_dict.keys():            
        media_type = media_type_dict[file_extension]
        output_subdomain['mediatype'] = media_type
    else:
        output_subdomain['mediatype'] = ''
    

    newworkflow["io_domain"] = {"input_subdomain": [input_subdomain], "output_subdomain": [output_subdomain]}


    return newworkflow
