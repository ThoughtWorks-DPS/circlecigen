
import json
import os, filecmp
from unittest.mock import patch, mock_open
from tfvars import write_tfvar_files

def test_write_tfvars_files():
    environs = {
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

    defaultparams = {
  "env_instance": "default-env-instance",
  "aws_region": "default-region",
  "aws_account_id": "default-account-id"
}

    envpath = "env_test"

    result = write_tfvar_files(envpath, environs, defaultparams)
    assert os.path.isfile(os.path.join(envpath, "qa-us-west-2.tfvars.json"))
    assert os.path.isfile(os.path.join(envpath, "qa-us-east-2.tfvars.json"))
    assert os.path.isfile(os.path.join(envpath, "preview-us-west-2.tfvars.json"))
    assert os.path.isfile(os.path.join(envpath, "preview-us-east-2.tfvars.json"))
    assert os.path.isfile(os.path.join(envpath, "generated_config.yml"))
    assert filecmp.cmp(os.path.join(envpath, "qa-us-west-2.tfvars.json"), os.path.join("test", "qa-us-west-2.tfvars.json"))
    assert filecmp.cmp(os.path.join(envpath, "qa-us-east-2.tfvars.json"), os.path.join("test", "qa-us-east-2.tfvars.json"))
    assert filecmp.cmp(os.path.join(envpath, "preview-us-west-2.tfvars.json"), os.path.join("test", "preview-us-west-2.tfvars.json"))
    assert filecmp.cmp(os.path.join(envpath, "preview-us-east-2.tfvars.json"), os.path.join("test", "preview-us-east-2.tfvars.json"))
    assert filecmp.cmp(os.path.join(envpath, "generated_config.yml"), os.path.join("test", "generated_config.yml"))
    assert result == f"4 tfvars created in {envpath}/"


    # tried various unittest.mock strategies to avoid writing anything, below one of them
    # but haven't yet figured it out. Thie one for example fails and then in the messages has the
    # expected and actual and they are the same so i don't get it.

    # with patch('json.dump') as mock_dump:
    #     write_tfvar_files(envpath, environs, defaultparams)

    #     mock_dump.assert_any_call(qa_us_west_result, mock_open(), indent=2)
    #     mock_dump.assert_any_call(qa_us_east_result, mock_open(), indent=2)
    #     mock_dump.assert_any_call(preview_us_west_result, mock_open(), indent=2)
    #     mock_dump.assert_any_call(preview_us_east_result, mock_open(), indent=2)


    # qa_us_west_result = {'env_instance': 'qa-us-west-2', 'aws_region': 'us-west-2', 'aws_account_id': 'default-account-id'}
    # qa_us_east_result = {'env_instance': 'qa-us-east-2', 'aws_region': 'us-east-2', 'aws_account_id': 'default-account-id'}
    # preview_us_east_result = {'env_instance': 'preview-us-east-2', 'aws_region': 'us-east-2', 'aws_account_id': 'default-account-id'}
    # preview_us_west_result = {'env_instance': 'preview-us-west-2', 'aws_region': 'us-west-2', 'aws_account_id': 'default-account-id'}
   
   
   
# class doubleQuoteDict(dict):
#     def __str__(self):
#         return json.dumps(self)

#     def __repr__(self):
#         return json.dumps(self)
   
# qa_us_west_result = doubleQuoteDict(qa_us_west_result)
# qa_us_east_result = doubleQuoteDict(qa_us_east_result)
# preview_us_east_result = doubleQuoteDict(preview_us_west_result)
# preview_us_west_result =  doubleQuoteDict(preview_us_east_result)

