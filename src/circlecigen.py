import click
from pathvalidate.click import validate_filename_arg, validate_filepath_arg
from tfvars import write_tfvar_files
from utils import read_json_file
from template import write_generated_config


@click.version_option()
@click.command()
@click.option("--outfile", default="generated_config.yml", help="Generated file. Default is generated_config.yml", callback=validate_filename_arg)
@click.option("--envpath", default="environments", help="Environment config folder. Default is environments/", callback=validate_filepath_arg)
@click.option("--multifile", default="multi.json", help="Multi-environment config file. Default is multi.json", callback=validate_filepath_arg)
@click.option("--defaultparams", default="default.json", help="Environment configuration default parameters file. Default is default.tfvars.json", callback=validate_filepath_arg)
@click.option("--tfvars", default=True, help="Generate tfvars.json files for all environments. Default is true")
@click.option("--workflow", default="continuation-generated-workflow", help="Name for generated_config workflow. Default is continuation-generated-workflow", callback=validate_filename_arg)
@click.option("--pipepath", default=".circleci", help="Override default config.yml location for testing", callback=validate_filepath_arg)
def cli(outfile, envpath, multifile, defaultparams, tfvars, workflow, pipepath):
    """Opinionated generation of continuation pipelines. See https://github.com/ThoughtWorks-DPS/circlecigen for detailed usage instructions.

    Inputs 

      .circleci/template.yml

      environments/

        default.tfvars.json

        [role].tfvars.json

        [instance].tfvars.json

    Outputs:

      .circleci/generated_config.yml

      environments/

        [for each instance].tfvars.json
    """
    result = write_tfvar_files(envpath, read_json_file(envpath, multifile), read_json_file(envpath, defaultparams)) if tfvars else click.echo("Not generating tfvars.json files")
    click.echo(result)
    write_generated_config(pipepath, outfile, envpath, multifile, workflow)
