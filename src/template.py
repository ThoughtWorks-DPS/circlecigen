from os.path import isfile
from jinja2 import Environment, FileSystemLoader
from src.utils import read_json_file

APPROVE_TEMPLATE="""      - approve {{role}} changes:
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

PRIOR_APPROVAL="""
          requires:
            - approve {} changes
"""

def generate_config(use_pipeline, pipepath, outfile, envpath, environs, workflow):
    """create generated_config.yaml for continuation orb"""

    # use the specified filter to generate a pipeline only for the desired trigger
    pipeline = environs[use_pipeline]

    # copy everything but the jobs and workflows from config.yml into generated_config.yml
    # pipepath = where to find config.yml, default .circleci
    # outfile  = where to write generated_config.yml, default .circleci
    # workflow = what to name the generated workflow, default continuation-generated-workflow
    setup_generated_config_outfile(pipepath, outfile, workflow)

    # setup the jinja templates
    je = Environment(loader=FileSystemLoader(f"{pipepath}/"), autoescape=True)
    pre, approve, post = get_templates(je, pipepath)

    # setup Dict for the approval job template 
    approve_vars = {}
    approve_vars["filter"] = pipeline["filter"]

    # all pre-approval jobs created accept for the first role must wait for
    # the prior role approval set this as blank to start then populate
    # with the list of all instance plans jobs in the role
    priorapprovalrequired = ""
    approvalrequiredjobs = ""

    # open the outfile for appeand and start processing roles/instances
    with open(f"{pipepath}/{outfile}", 'a', encoding="utf-8") as f:
        for role in pipeline:
            # skip the filter definition
            if role == "filter":
                continue

            # when the approval template is generate, it must be populated with
            # a list of all instances for which a pre-approval template is
            # generated. That is returned by this job.
            approvalrequiredjobs = generate_pre_approval_jobs(f, envpath, pre, pipeline, role, priorapprovalrequired)

            # generate approval job for the current role, a human will trigger the post- phase
            generate_approval_jobs(f, approve, approve_vars, approvalrequiredjobs, role)
            generate_post_approval_jobs(f, envpath, post, pipeline, role)

            # record the current role, to provide 'requires:' list in any subsequent pre- jobs
            priorapprovalrequired = role

def generate_pre_approval_jobs(f, envpath, pre, pipeline, role, priorapprovalrequired):
    # generate a pre-approval job for each instance in the role,
    # if a pre-approval.yml file exists
    if pre:
        approvalrequiredjobs = "requires:"
        for instance in pipeline[role]:
            instance_vars=read_json_file(envpath, f"{instance}.tfvars.json")
            instance_vars.update({
                "filters": pipeline["filter"],
                "role": role,
                "envpath": envpath
            })
            if priorapprovalrequired:
                instance_vars.update({
                    "priorapprovalrequired": PRIOR_APPROVAL.format(priorapprovalrequired)
                })
            approvalrequiredjobs += f"\n            - plan {instance} change"
            f.write(pre.render(instance_vars))
        return approvalrequiredjobs
    return None

def generate_approval_jobs(f, approve, approve_vars, approvalrequiredjobs, role):
    approve_vars.update ({
        "role": role,
        "approvalrequiredjobs": approvalrequiredjobs
    })
    f.write(approve.render(approve_vars))

def generate_post_approval_jobs(f, envpath, post, pipeline, role):
    # generate a post-approval job for each instance in the role,
    # if a post-approval.yml file exists
    if post:
        for instance in pipeline[role]:
            instance_vars=read_json_file(envpath, f"{instance}.tfvars.json")
            instance_vars.update({
                "filters": pipeline["filter"],
                "role": role,
                "envpath": envpath
            })
            f.write(post.render(instance_vars))

def get_templates(je, pipepath):
    """setup the jinja templates"""
    pre = je.get_template("pre-approve.yml") if isfile(f"{pipepath}/pre-approve.yml") else 0
    post = je.get_template("post-approve.yml") if isfile(f"{pipepath}/post-approve.yml") else 0
    approve = je.from_string(APPROVE_TEMPLATE)
    return pre, approve, post

def generate_config_lines(pipepath):
    """Read config.yml and yield lines that don't start with 'setup:' until it encounters a line starting with 'jobs:' or 'workflows:'"""
    config_file = f"{pipepath}/config.yml"
    with open(config_file, encoding="utf-8") as f:
        for line in _read_until_jobs_or_workflows(f):
            if not _line_starts_with_setup(line):
                yield line


def _read_until_jobs_or_workflows(f):
    """Generator that reads lines from file object f until it encounters a line starting with 'jobs:' or 'workflows:'"""
    for line in f:
        # initially, 
        if line.startswith("jobs:") or line.startswith("workflows:"):
            break
        yield line

def _line_starts_with_setup(line):
    """Return True if the given line starts with 'setup:', False otherwise"""
    return line.startswith("setup:")

def setup_generated_config_outfile(pipepath, outfile, workflow):
    """read .circleci/config.yml and write everything up to jobs: or workflows: into the outfile"""
    with open(f"{pipepath}/{outfile}", 'w', encoding="utf-8") as f:
        for line in generate_config_lines(pipepath):
            f.write(line)
        f.write(WORKFLOW_HEADING.format(workflow))
