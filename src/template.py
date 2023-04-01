from os.path import isfile
from jinja2 import Environment, FileSystemLoader
import click
from utils import read_json_file

APPROVE_TEMPLATE = """      - approve {{role}} changes:
          type: approval
          {{approvalrequiredjobs}}
          filters: {{filter}}


"""

WORKFLOW_HEADING="""
workflows:
  version: 2

  {}:
    jobs:
"""

PRIOR_APPROVAL = """
          requires:
            - approve {} changes
"""

def write_generated_config(pipepath, outfile, envpath, multifile, workflow):
    """create generated_config.yaml for continuation orb"""
    environs = read_json_file(envpath, multifile)
    jobfilter = environs["filter"]

    # copy everything but the jobs and workflows from config.yml into generated_config.yml
    setup_generated_config_outfile(pipepath, outfile, workflow)

    # setup the jinja templates
    je = Environment(loader=FileSystemLoader(f"{pipepath}/"))
    pre, approve, post = get_templates(je, pipepath)

    # setup Dict for the approval job template 
    approve_vars = {}
    approve_vars["filter"] = jobfilter

    # all pre-approval jobs created accept for the first role must wait for the prior role approval
    # set this blank to start then populate with each complete role
    priorapprovalrequired = ""

    # open the outfile for appeand and start processing roles/instances
    with open(f"{pipepath}/{outfile}", 'a', encoding="utf-8") as f:
        for role in environs:
            # skip the filter definition
            if role == "filter":
                continue

            # when the approval template is generate, it must be populated with a list of all instances for which
            # a pre-approval template is generated. Setup a string for this config
            approvalrequiredjobs = "requires:"

            # generate a pre-approval job for each instance in the role, if a pre-approval.yml file exists
            if pre:
                for instance in environs[role]:
                    # fetch the assoicated tfvar file or error
                    if isfile(f"{envpath}/{instance}.tfvars.json"):
                        instance_vars=read_json_file(envpath, f"{instance}.tfvars.json")
                        # additional values available to template
                        instance_vars["filters"] = jobfilter
                        instance_vars["role"] = role
                        instance_vars["envpath"] = envpath
                        # include the 'requires:' information after the first role
                        instance_vars["priorapprovalrequired"] = PRIOR_APPROVAL.format(priorapprovalrequired) if priorapprovalrequired else ""
                        # build the list of required jobs for the approval template
                        approvalrequiredjobs += f"\n            - {instance} change plan"
                    else:
                        raise click.UsageError(f"{envpath}/{instance}.tfvars.json not found")
                    # write the instance pre- template to the outfile
                    f.write(pre.render(instance_vars))

            # generate approval job for the current role, a hunman will trigger the post- phase
            approve_vars["role"] = role
            approve_vars["approvalrequiredjobs"] = approvalrequiredjobs if approvalrequiredjobs != "requires:" else ""
            f.write(approve.render(approve_vars))

             # generate a post-approval job for each instance in the role, if a post-approval.yml file exists
            if post:
                for instance in environs[role]:
                    # fetch the assoicated tfvar file or error
                    if isfile(f"{envpath}/{instance}.tfvars.json"):
                        instance_vars=read_json_file(envpath, f"{instance}.tfvars.json")
                        # additional values available to template
                        instance_vars["filters"] = jobfilter
                        instance_vars["role"] = role
                        instance_vars["envpath"] = envpath
                    else:
                        raise click.UsageError(f"{envpath}/{instance}.tfvars.json not found")
                    # write the instance post- template to the outfile
                    f.write(post.render(instance_vars))
            # record the current role, to enable 'requires' info in subsequent pre- jobs
            priorapprovalrequired = role

def get_templates(je, pipepath):
    """setup the jinja templates"""
    pre = je.get_template("pre-approve.yml") if isfile(f"{pipepath}/pre-approve.yml") else 0
    post = je.get_template("post-approve.yml") if isfile(f"{pipepath}/post-approve.yml") else 0
    approve = je.from_string(APPROVE_TEMPLATE)
    return pre, approve, post

def generate_config_lines(pipepath):
    with open(f"{pipepath}/config.yml", encoding="utf-8") as f:
        for line in f:
            if line.startswith("jobs:") or line.startswith("workflows:"):
                break
            if not line.startswith("setup:"):
                yield line

def setup_generated_config_outfile(pipepath, outfile, workflow):
    """read .circleci/config.yml and write everything up to jobs: or workflows: into the outfile"""
    with open(f"{pipepath}/{outfile}", 'w', encoding="utf-8") as f:
        for line in generate_config_lines(pipepath):
            f.write(line)
        f.write(WORKFLOW_HEADING.format(workflow))
