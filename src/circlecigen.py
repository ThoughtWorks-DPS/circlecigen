import click
from pathvalidate.click import validate_filename_arg, validate_filepath_arg
from src.tfvars import generate_environment_tfvar_files
from src.utils import read_json_file, validate_filepath
from src.template import generate_config

@click.version_option()
@click.command()
@click.option("--outfile",
    default="generated_config.yml",
    help="Generated file. Default is generated_config.yml",
    callback=validate_filename_arg)
@click.option("--envpath", default="environments",
    help="Environment config folder. Default is environments/",
    callback=validate_filepath_arg)
@click.option("--multifile", default="multi.json",
    help="Multi-environment config file. Default is multi.json",
    callback=validate_filepath_arg)
@click.option("--defaultparams", default="default.json",
    help="Default parameters file. Default is default.tfvars.json",
    callback=validate_filepath_arg)
@click.option("--tfvars", default=True,
    help="Generate tfvars.json files for all role/instances. Default is true")
@click.option("--workflow", default="continuation-generated-workflow",
    help="Name for generated config. Default continuation-generated-workflow",
    callback=validate_filename_arg)
@click.option("--pipepath", default=".circleci",
    help="Override default config.yml location for testing",
    callback=validate_filepath_arg)
@click.argument('pipeline', nargs=1)
def cli(pipeline, outfile, envpath, multifile, defaultparams, tfvars, workflow, pipepath):
    """

    Inputs 

      .circleci/pre_approve.yml
      .circleci/post_approve.yml

      environments/

        muilti.json
        default.json

        [role].json (optional)

        [instance].json (optional)

    Outputs:

      .circleci/generated_config.yml

      environments/

        [for each instance].tfvars.json

    Opinionated generation of continuation pipelines.
    See https://github.com/ThoughtWorks-DPS/circlecigen
    for detailed usage instructions.
    """
    validate_filepath(envpath, "envpath")
    validate_filepath(pipepath, "pipepath")

    if tfvars:
        result = generate_environment_tfvar_files(pipeline, envpath,
                 read_json_file(envpath, multifile),
                 read_json_file(envpath, defaultparams))
        click.echo(f"{result} tfvars created in {envpath}/")
    else:
        click.echo("Not generating tfvars.json files")
    generate_config(pipeline, 
                    pipepath,
                    outfile,
                    envpath,
                    read_json_file(envpath, multifile),
                    workflow)