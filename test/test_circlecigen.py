from click.testing import CliRunner
from circlecigen import cli

def test_circlecigen_with_invalid_outfile_name():
  runner = CliRunner()
  result = runner.invoke(cli, ['--outfile', 'invalid:filename'])
  assert result.exit_code == 2
  assert "Invalid value for '--outfile'" in result.output

def test_circlecigen_with_unneccsary_argument_included():
  runner = CliRunner()
  result = runner.invoke(cli, ["argument"])
  assert "Got unexpected extra argument" in result.output
