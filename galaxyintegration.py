from bioblend.galaxy import GalaxyInstance
import json

galaxyIP = str(input('What is the URL address of the Galaxy instance?\n'))
galaxyAPIkey = str(input('What is the API key of the Galaxy instance?\n'))


gi = GalaxyInstance(galaxyIP, key=galaxyAPIkey)
libs = gi.libraries.get_libraries()

workflowID = str(input('What is the workflow ID to import?\n'))

gi.workflows.show_workflow(workflowID)

workflowDict = gi.workflows.export_workflow_dict(workflowID)


with open('test_workflow.json', 'w', encoding='utf-8') as f:
    json.dump(workflowDict, f, ensure_ascii=False, indent=4)





# test commands
#gi.workflows.export_workflow_to_local_path(workflowID,r"C:\Users\mwisinger\Documents\precisionFDA BCO\githubrepo",
#   use_default_filename=True)
#gi.workflows.run_workflow('workflow ID', input_dataset_map)