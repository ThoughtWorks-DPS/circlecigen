from os.path import isfile
from utils import read_json_file, merge, write_json_file

def generate_environment_tfvar_files(use_pipeline, envpath, environs, defaultparams):
    """create and write instance.tfvars.json files for each multi-env instance"""

    # use the specified filter to generate a pipeline only for the desired trigger
    pipeline = environs[use_pipeline]

    for role in pipeline:
         # skip the filter key, this is used to specify the trigger for a generated pipeline
        if role == "filter":
            continue

        # start with an instance.tfvars.json dict made from the default environment parameters
        role_vars = defaultparams

        # if there is a matching role.json file, get the values to merge in the next step
        if isfile(f"{envpath}/{role}.json"):
           role_vars = merge(role_vars,read_json_file(envpath, f"{role}.json"))

        for instance in pipeline[role]:
            instance_vars = role_vars

            # merge matching instance.json
            if isfile(f"{envpath}/{instance}.json"):
                instance_vars = merge(instance_vars,read_json_file(envpath, f"{instance}.json"))
            
            # merge any instance overrides in muilti.json into instance dict, intended to overwrite conflicts out of multi.json
            instance_vars = merge(instance_vars, pipeline[role][instance])

            # set the env_instance to the current instance
            instance_vars.update({
                "env_instance": instance
            })
            write_json_file(f"{envpath}/{instance}.tfvars.json", instance_vars)
    return nummber_of_files_to_generate(pipeline)

def nummber_of_files_to_generate(pipeline):
    """calculate the number of total number of instances within the multi-role definition"""
    instance_count = 0
    for role in pipeline:
        if role == "filter":
            continue
        print(f"{role} role contains {len(pipeline[role])} instance(s)")
        if isinstance(pipeline[role], dict):
            instance_count += len(pipeline[role])
    return instance_count