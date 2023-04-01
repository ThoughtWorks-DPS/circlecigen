from os.path import isfile
from utils import read_json_file, merge, write_json_file

def generate_environment_tfvar_files(envpath, environs, defaultparams):
    """create and write instance.tfvars.json files for each multi-env instance"""
    for role in environs:
         # skip the filter key, this is used to specify the trigger for a generated pipeline
        if role == "filter":
            continue

        # start with an instance.tfvars.json dict made from the default environment parameters
        instance_vars = defaultparams

        # if there is a matching role.tfvars.json file, get the values to merge in the next step
        if isfile(f"{envpath}/{role}.tfvars.json"):
           instance_vars = merge(instance_vars,read_json_file(envpath, f"{role}.tfvars.json"))

        for instance in environs[role]:
            # merge any instance overrides in muilti.json into instance dict
            instance_vars = merge(instance_vars, environs[role][instance])
            # set the env_instance to the current instance
            instance_vars["env_instance"] = instance
            write_json_file(f"{envpath}/{instance}.tfvars.json", instance_vars)
    return nummber_of_files_to_generate(environs)

def nummber_of_files_to_generate(environs):
    """calculate the number of total number of instances within the multi-role definition"""
    instance_count = 0
    for role in environs:
        #instance_count = instance_count + role_instance_count_info(role)
        if isinstance(environs[role], dict):
            instance_count += len(environs[role])
        print(f"{role} role contains {instance_count} instance(s)")
    return instance_count
