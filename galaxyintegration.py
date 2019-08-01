from bioblend.galaxy import GalaxyInstance
import json

galaxyIP = str(input('What is the URL address of the Galaxy instance?\n'))
galaxyAPIkey = str(input('What is the API key of the Galaxy instance?\n'))


gi = GalaxyInstance(galaxyIP, key=galaxyAPIkey)
libs = gi.libraries.get_libraries()

workflowID = str(input('What is the workflow ID to import?\n'))

gi.workflows.show_workflow(workflowID)

workflowDict = gi.workflows.export_workflow_dict(workflowID)

# getting the dictionary mapped/formatted to BCO-schema
def workflow_conversion(workflow):
    workflow['bco_id'] = workflow.pop('uuid', '')
    workflow['keywords'] = workflow.pop('tags', '')
    workflow['platform'] = 'Galaxy'
    workflow['version'] = str(str(workflow['version']) + '.0')
    workflow['bco_id'] = workflow.pop('uuid', '')

    # need to iterate through nested workflow steps for pipeline steps

    for k, v in workflow['steps'].items():
        # k is a str, v is a dict
        for k, v in k.items():
            k['description'] = k.pop('label', '')
            k['version'] = k.pop('tool_version', '')
            
            k['input_list'] = dict(k.pop('')) # pull from previous step output?

        

workflow_conversion(workflowDict)

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