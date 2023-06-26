from click.testing import CliRunner
from src.circlecigen import cli

def test_circlecigen_with_invalid_outfile_name():
  runner = CliRunner()
  result = runner.invoke(cli, ['sandbox', '--outfile', 'invalid:filename'])
  assert result.exit_code == 2
  assert "Invalid value for '--outfile'" in result.output

def test_circlecigen_with_invalid_envpath_name():
  runner = CliRunner()
  result = runner.invoke(cli, ['sandbox', '--envpath', 'invalid:pathname'])
  assert result.exit_code == 2
  assert "Invalid value for '--envpath'" in result.output

def test_circlecigen_with_invalid_multifile_name():
  runner = CliRunner()
  result = runner.invoke(cli, ['sandbox', '--multifile', 'invalid:filename'])
  assert result.exit_code == 2
  assert "Invalid value for '--multifile'" in result.output

def test_circlecigen_with_invalid_defaultparams_name():
  runner = CliRunner()
  result = runner.invoke(cli, ['sandbox', '--defaultparams', 'invalid:filename'])
  assert result.exit_code == 2
  assert "Invalid value for '--defaultparams'" in result.output

def test_circlecigen_with_invalid_tfvars_value():
  runner = CliRunner()
  result = runner.invoke(cli, ['sandbox', '--tfvars', 'invalid'])
  assert result.exit_code == 2
  assert "Invalid value for '--tfvars'" in result.output

def test_circlecigen_with_invalid_workflow_value():
  runner = CliRunner()
  result = runner.invoke(cli, ['sandbox', '--workflow', 'invalid:workflow'])
  assert result.exit_code == 2
  assert "Invalid value for '--workflow'" in result.output

def test_circlecigen_with_invalid_pipepath_name():
  runner = CliRunner()
  result = runner.invoke(cli, ['sandbox', '--pipepath', 'invalid:pathname'])
  assert result.exit_code == 2
  assert "Invalid value for '--pipepath'" in result.output

def test_circlecigen_with_invalid_template_name():
  runner = CliRunner()
  result = runner.invoke(cli, ['sandbox', '--template', 'invalid:template'])
  assert result.exit_code == 2
  assert "Invalid value for '--template'" in result.output

def test_circlecigen_help():
  runner = CliRunner()
  result = runner.invoke(cli, ["--help"])
  assert "Usage:" in result.output

def test_circlecigen_with_missing_pipeline_argument():
  runner = CliRunner()
  result = runner.invoke(cli)
  assert "Missing argument" in result.output

def test_circlecigen_with_test_env_values():
  runner = CliRunner()
  result = runner.invoke(cli, ["release", "--envpath", "env_test", "--pipepath", "env_test", "--template", "custom.yml"])
  assert "4 tfvars created in env_test/" in result.output
