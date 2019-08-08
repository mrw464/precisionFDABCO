from bioblend.galaxy import GalaxyInstance
import json
import pprint


galaxyIP = 'https://usegalaxy.org/'
galaxyAPIkey = '8ef9404a83483288f5fbb07f18ef61a7'
#galaxyIP = str(input('What is the URL address of the Galaxy instance?\n'))
#galaxyAPIkey = str(input('What is the API key of the Galaxy instance?\n'))


gi = GalaxyInstance(galaxyIP, key=galaxyAPIkey)
libs = gi.libraries.get_libraries()


workflowID = '8d8e8927d63803ef'
#workflowID = str(input('What is the workflow ID to import?\n'))

gi.workflows.show_workflow(workflowID)

workflowDict = gi.workflows.export_workflow_dict(workflowID)

# getting the dictionary mapped/formatted to BCO-schema
def workflow_conversion(workflow):
    newworkflow = {}
    newworkflow['bco_id'] = workflow.pop('uuid', '')
    keywords = workflow.pop('tags', '')
    version = str(str(workflow['version']) + '.0')
    newworkflow['bco_id'] = workflow.pop('uuid', '')
    name = workflow.pop('name', '')
    newworkflow['provenance_domain'] = {"name": name, "version": version}


    # need to iterate through nested workflow steps for pipeline steps
    pipeline_steps = []

    # definiting sub-function for extracting step outputs (to be inputs for the next step)
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
            
            step_dict['input_list'] = {"uri": "urn:dataset:user_provided_dataset"}

            # extract output for next step
            output = output_extract(v)
            step_dict['output_list'] = output

        elif k >= 1:    # pull from previous step output for steps after first
            step_dict['input_list'] = output             
            output = output_extract(v)
            step_dict['output_list'] = output

        pipeline_steps.append(step_dict.copy()) 


    newworkflow['description_domain'] = {
        "keywords": [keywords],
        "platform": ["Galaxy"], 
        "pipeline_steps": pipeline_steps
    }

    software_preq = {}
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
            software_preq.update({"name": tool_name, "version": tool_version, "uri": tool_uri})

    script_name = str(name + '.ga')
    script_uri = str("file://localhost/" + script_name)
    script_uri_dict = {"uri": script_uri}
    newworkflow["execution_domain"] = {
        "script": script_uri_dict,
        "script_driver": "Galaxy",
        "software_prerequisites": software_preq

    }

    return newworkflow

#workflow_conversion(workflowDict)
workflowDict = workflow_conversion(workflowDict)

pprint.pprint(workflowDict)


'''
def remove_empties_from_dict(a_dict):
    new_dict = {}
    for k, v in a_dict.items():
        if isinstance(v, list):
            v = remove_empties_from_dict(v)
        if v is not “”:
            new_dict[k] = v
    return new_dict or None
'''
# dumping the dict to JSON
#with open('test_workflow.json', 'w', encoding='utf-8') as f:
#   json.dump(workflowDict, f, ensure_ascii=False, indent=4)





# test commands
#gi.workflows.export_workflow_to_local_path(workflowID,r"C:\Users\mwisinger\Documents\precisionFDA BCO\githubrepo",
#   use_default_filename=True)
#gi.workflows.run_workflow('workflow ID', input_dataset_map)