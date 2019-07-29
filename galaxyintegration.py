from bioblend.galaxy import GalaxyInstance


galaxyIP = str(input('What is the URL address of the Galaxy instance?\n'))
galaxyAPIkey = str(input('What is the API key of the Galaxy instance?\n'))


gi = GalaxyInstance(galaxyIP, key=galaxyAPIkey)
libs = gi.libraries.get_libraries()

workflowID = str(input('What is the workflow ID to import?\n'))

gi.workflows.show_workflow(workflowID)

#gi.workflows.run_workflow('workflow ID', input_dataset_map)