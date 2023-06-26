import os
import filecmp
from jinja2 import Environment, FileSystemLoader, Template
from src.template import setup_generated_config_outfile, get_templates, generate_config

mock_multi = {
  "sandbox": {
    "filter": "*on-push-main",
    "dev": {
      "dev-us-east-2": {
        "aws_region": "us-east-2",
        "aws_account_id": "10100000000"
      }
    }
  },
  "release": {
    "filter": "*on-tag-main",
    "nonprod": {
      "nonprod-us-west-2": {
        "aws_region": "us-west-2",
        "aws_account_id": "20100000000"
      },
      "nonprod-us-east-2": {
        "aws_region": "us-east-2",
        "aws_account_id": "20100000000"
      }
    },
    "prod": {
      "prod-us-west-2": {
        "aws_region": "us-west-2",
        "aws_account_id": "30100000000"
      },
      "prod-us-east-2": {
        "aws_region": "us-east-2",
        "aws_account_id": "30100000000"
      }
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

    pre, approve, post, custom = get_templates(je, envpath)
    
    assert isinstance(pre, Template)
    assert isinstance(post, Template)
    assert isinstance(approve, Template)


def test_get_custom_template():
    envpath = "env_test"
    custom_template = "custom.yml"
    je = Environment(loader=FileSystemLoader(f"{envpath}/"))

    pre, approve, post, custom = get_templates(je, envpath, custom_template)

    assert isinstance(pre, Template)
    assert isinstance(post, Template)
    assert isinstance(approve, Template)
    assert isinstance(custom, Template)


# this is as ugly as the tfvars file output tests
def test_generate_config():
    mock_pipeline = "release"
    mock_pipepath = "env_test"
    mock_envpath = "env_test"
    mock_outfile = "generated_config.yml"
    mock_workflow = "continuation-generated-workflow"
    mock_template = None

    generate_config(mock_pipeline, mock_pipepath, mock_outfile, mock_envpath, mock_multi, mock_workflow, mock_template)
    assert os.path.isfile(os.path.join(mock_pipepath, mock_outfile))
    assert filecmp.cmp(os.path.join(mock_pipepath,
                       mock_outfile),
                       os.path.join("test",
                       mock_outfile))


def test_generate_config_with_custom_template():
    mock_pipeline = "release"
    mock_pipepath = "env_test"
    mock_envpath = "env_test"
    mock_outfile = "template_generated_config.yml"
    mock_workflow = "continuation-generated-workflow"
    mock_template = "custom.yml"

    generate_config(mock_pipeline, mock_pipepath, mock_outfile, mock_envpath, mock_multi, mock_workflow, mock_template)
    assert os.path.isfile(os.path.join(mock_pipepath, mock_outfile))
    assert filecmp.cmp(os.path.join(mock_pipepath,
                                    mock_outfile),
                       os.path.join("test",
                                    mock_outfile))
