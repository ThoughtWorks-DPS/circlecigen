from os.path import isfile
import json
from utils import read_json_file, merge

def write_tfvar_files(envpath, environs, defaultparams):
    """create and write instance.tfvars.json files for each multi-env instance"""
    files_generated=0
    for role in environs:
        # skip the filter key, this is used to specify the trigger for a generated pipeline
        if role == "filter":
            continue

        # start with an instance.tfvars.json dict made from the default vars
        instance_vars = defaultparams
        role_vars = {}
        
        # if there is a matching role.tfvars.json file, get the values to merge in the next step
        if isfile(f"{envpath}/{role}.tfvars.json"):
            role_vars=read_json_file(envpath, f"{role}.tfvars.json")
            
        for instance in environs[role]:
            # if there were role vars, merge into instance dict
            if role_vars:
              instance_vars = merge(instance_vars,role_vars)

            # if there are muilti.json instance overrides, merge into instance dict
            if len(environs[role][instance]):
              instance_vars = merge(instance_vars, environs[role][instance])

            # set the env_instance to the current instance
            instance_vars["env_instance"] = instance
            with open(f"{envpath}/{instance}.tfvars.json", 'w', encoding="utf-8") as f:
              json.dump(instance_vars, f, indent=2)
            files_generated += 1

    return f"{files_generated} tfvars created in {envpath}/"
