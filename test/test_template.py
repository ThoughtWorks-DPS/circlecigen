import os
import filecmp
from jinja2 import Environment, FileSystemLoader, Template
from template import setup_generated_config_outfile, get_templates, generate_config

mock_environs = {
  "filter": "*on-push-main",
  "qa": {
    "qa-us-west-2": {
      "aws_region": "us-west-2"
    },
    "qa-us-east-2": {
      "aws_region": "us-east-2"
    }
  },
  "preview": {
    "preview-us-east-2": {
      "aws_region": "us-east-2"
    },
    "preview-us-west-2": {
      "aws_region": "us-west-2"
    }
  }
}

# this is as ugly as the tfvars file output tests
def test_setup_generated_config_outfile():
    mock_pipepath = "env_test"
    mock_outfile = "generated_config.yml"
    mock_workflow = "continuation-generated-workflow"

    setup_generated_config_outfile(mock_pipepath, mock_outfile, mock_workflow)
    assert os.path.isfile(os.path.join(mock_pipepath, mock_outfile))
    assert filecmp.cmp(os.path.join(mock_pipepath,
                       mock_outfile),
                       os.path.join("test", "generated_config_setup.yml"))

def test_get_templates():
    envpath = "env_test"
    je = Environment(loader=FileSystemLoader(f"{envpath}/"))

    pre, approve, post = get_templates(je, envpath)
    
    assert isinstance(pre, Template)
    assert isinstance(post, Template)
    assert isinstance(approve, Template)

# this is as ugly as the tfvars file output tests
def test_generate_config():
    mock_pipepath = "env_test"
    mock_envpath = "env_test"
    mock_outfile = "generated_config.yml"
    mock_workflow = "continuation-generated-workflow"

    generate_config(mock_pipepath, mock_outfile, mock_envpath, mock_environs, mock_workflow)
    assert os.path.isfile(os.path.join(mock_pipepath, mock_outfile))
    assert filecmp.cmp(os.path.join(mock_pipepath,
                       mock_outfile),
                       os.path.join("test",
                       mock_outfile))
