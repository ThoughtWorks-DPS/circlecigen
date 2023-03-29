<div align="center">
	<p>
		<img alt="Thoughtworks Logo" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/thoughtworks_flamingo_wave.png?sanitize=true" width=200 />
    <br />
		<img alt="DPS Title" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/EMPCPlatformStarterKitsImage.png?sanitize=true" width=350/>
	</p>
  <br />
  <h3>iam-credential-rotation</h3>
    <a href="https://app.circleci.com/pipelines/github/ThoughtWorks-DPS/circlecigen"><img src="https://dl.circleci.com/status-badge/img/gh/ThoughtWorks-DPS/circlecigen/tree/main.svg?style=shield"></a> <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
</div>
<br />

Opinionated generation of continuation pipelines


### Assumptions and requirements

* for terraform pipelines using the twdps/terraformorb
* muilti.json has a required format
* manages dynamic deployment pipelines
* all deployment confignuration must be managed via the terra orb jobs. E.g., any post testing must be managed by pipeline  `commands` that are included via the `after-terraform` step parameter
* the generated_config.yml will include the contents of config.yml except for jobs: and workflows: (or the setup: directive of course)
* the pre-approval job template must be in the same folder as config.yaml and be named pre-approval.yml
* the post-approval job template must be in the same folder as config.yaml and be named post-approval.yml
* a default.tfvars.json exists that contains all the tfvar variables used by the terraform code for a single instance
* you can override any of the default.tfvars.json values for a entire Role within a file named "your role".tfvars.json
* you can override any of the default.tfvars.json values for a specific instance by adding the unique vales to the multi.json file
* Where there is more than a single role (such as a release deployment), after the first role each subsequent pre processing will include a requires dependency on the previous approval job
* the following additional values are available within the pre and post templates
* * filters (from multi.json)
* * role (current role being processed)
* * envpath (path folder containing tfvars files)