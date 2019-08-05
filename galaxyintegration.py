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
    newworkflow['keywords'] = workflow.pop('tags', '')
    newworkflow['platform'] = 'Galaxy'
    newworkflow['version'] = str(str(workflow['version']) + '.0')
    newworkflow['bco_id'] = workflow.pop('uuid', '')

    # need to iterate through nested workflow steps for pipeline steps
    pipeline_steps = []

    # definiting sub-function for extracting step outputs (to be inputs for the next step)
    def output_extract(v):
        output = []
        if v.pop('outputs', '') != '':
            output_list = v.pop('outputs', '')
            for i in output_list:
                output_item = str(output_list['name'] + '.' + output_list['type'])
                output_item = {"uri":output_item}
                output = output.append(output_item.copy())
        return output

    for k, v in workflow['steps'].items():
        # k is a str, v is a dict
        step_dict = {}

        print(f'k: {k}')
        print(f'v: {v}')
        k = int(k)
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

    newworkflow['pipeline_steps'] = pipeline_steps

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