import os
import filecmp
from tfvars import nummber_of_files_to_generate, generate_environment_tfvar_files

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

mock_defaultparams = {
  "env_instance": "default-env-instance",
  "aws_region": "default-region",
  "aws_account_id": "default-account-id"
}

def test_nummber_of_files_to_generate():
    result = nummber_of_files_to_generate(mock_environs)
    assert result == 4

# this is ugly, see notes below
def test_generate_environment_tfvar_files():
    mock_envpath = "env_test"

    _ = generate_environment_tfvar_files(mock_envpath, mock_environs, mock_defaultparams)
    assert os.path.isfile(os.path.join(mock_envpath, "qa-us-west-2.tfvars.json"))
    assert os.path.isfile(os.path.join(mock_envpath, "qa-us-east-2.tfvars.json"))
    assert os.path.isfile(os.path.join(mock_envpath, "preview-us-west-2.tfvars.json"))
    assert os.path.isfile(os.path.join(mock_envpath, "preview-us-east-2.tfvars.json"))
    assert filecmp.cmp(os.path.join(mock_envpath, "qa-us-west-2.tfvars.json"),
                                    os.path.join("test", "qa-us-west-2.tfvars.json"))
    assert filecmp.cmp(os.path.join(mock_envpath, "qa-us-east-2.tfvars.json"),
                                    os.path.join("test", "qa-us-east-2.tfvars.json"))
    assert filecmp.cmp(os.path.join(mock_envpath, "preview-us-west-2.tfvars.json"),
                                    os.path.join("test", "preview-us-west-2.tfvars.json"))
    assert filecmp.cmp(os.path.join(mock_envpath, "preview-us-east-2.tfvars.json"),
                                    os.path.join("test", "preview-us-east-2.tfvars.json"))



