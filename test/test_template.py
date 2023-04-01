import os
import filecmp
from jinja2 import Environment, FileSystemLoader, Template
from template import setup_generated_config_outfile, get_templates, write_generated_config

# this is as ugly as the tfvars file output tests
def test_setup_generated_config_outfile():
    pipepath = "env_test"
    outfile = "generated_config.yml"
    workflow = "continuation-generated-workflow"

    setup_generated_config_outfile(pipepath, outfile, workflow)
    assert os.path.isfile(os.path.join(pipepath, outfile))
    assert filecmp.cmp(os.path.join(pipepath, outfile), os.path.join("test", "generated_config_setup.yml"))

def test_get_templates():
    envpath = "env_test"
    je = Environment(loader=FileSystemLoader(f"{envpath}/"))

    pre, approve, post = get_templates(je, envpath)
    
    assert isinstance(pre, Template)
    assert isinstance(post, Template)
    assert isinstance(approve, Template)

# this is as ugly as the tfvars file output tests
def test_write_generated_config():
    pipepath = "env_test"
    envpath = "env_test"
    outfile = "generated_config.yml"
    environs = {"filter": "*on-push-main", "qa": {"qa-us-west-2": {"aws_region": "us-west-2"}, "qa-us-east-2": {"aws_region": "us-east-2"}}, "preview": {"preview-us-east-2": {"aws_region": "us-east-2"}, "preview-us-west-2": {"aws_region": "us-west-2"}}}
    workflow = workflow = "continuation-generated-workflow"

    write_generated_config(pipepath, outfile, envpath, environs, workflow)
    assert os.path.isfile(os.path.join(pipepath, outfile))
    assert filecmp.cmp(os.path.join(pipepath, outfile), os.path.join("test", outfile))
