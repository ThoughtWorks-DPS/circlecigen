import os
import filecmp
from tfvars import nummber_of_files_to_generate, generate_environment_tfvar_files

mock_envpath = "env_test"

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

mock_defaultparams = {
  "aws_region": "default-region",
  "aws_account_id": "default-account-id"
}

mock_pipeline = 'release'

def test_nummber_of_files_to_generate():
    result = nummber_of_files_to_generate(mock_multi['release'])
    assert result == 4

# this is ugly, see notes below
def test_generate_environment_tfvar_files():

    _ = generate_environment_tfvar_files(mock_pipeline, mock_envpath, mock_multi, mock_defaultparams)
    assert os.path.isfile(os.path.join(mock_envpath, "nonprod-us-west-2.tfvars.json"))
    assert os.path.isfile(os.path.join(mock_envpath, "nonprod-us-east-2.tfvars.json"))
    assert os.path.isfile(os.path.join(mock_envpath, "prod-us-west-2.tfvars.json"))
    assert os.path.isfile(os.path.join(mock_envpath, "prod-us-east-2.tfvars.json"))
    assert filecmp.cmp(os.path.join(mock_envpath, "nonprod-us-west-2.tfvars.json"),
                                    os.path.join("test", "nonprod-us-west-2.tfvars.json"))
    assert filecmp.cmp(os.path.join(mock_envpath, "nonprod-us-east-2.tfvars.json"),
                                    os.path.join("test", "nonprod-us-east-2.tfvars.json"))
    assert filecmp.cmp(os.path.join(mock_envpath, "prod-us-west-2.tfvars.json"),
                                    os.path.join("test", "prod-us-west-2.tfvars.json"))
    assert filecmp.cmp(os.path.join(mock_envpath, "prod-us-east-2.tfvars.json"),
                                    os.path.join("test", "prod-us-east-2.tfvars.json"))
