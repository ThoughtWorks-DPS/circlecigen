<div align="center">
	<p>
		<img alt="Thoughtworks Logo" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/thoughtworks_flamingo_wave.png?sanitize=true" width=200 />
    <br />
		<img alt="DPS Title" src="https://raw.githubusercontent.com/ThoughtWorks-DPS/static/master/EMPCPlatformStarterKitsImage.png?sanitize=true" width=350/>
	</p>
  <br />
  <h3>circlecigen</h3>
    <a href="https://app.circleci.com/pipelines/github/ThoughtWorks-DPS/circlecigen"><img src="https://dl.circleci.com/status-badge/img/gh/ThoughtWorks-DPS/circlecigen/tree/main.svg?style=shield"></a> <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
</div>
<br />

Opinionated generation of CircleCI [dynamic configuration](https://circleci.com/docs/using-dynamic-configuration/) _continuation_ pipelines.

### Installation

```bash
pip install circlecigen
```

### How it works

The circleci [continuation orb](https://circleci.com/developer/orbs/orb/circleci/continuation) is somewhat limited in terms of flexability in use, but when you automate the creation of the resulting new pipeline you open up some interesting opportunities. 

The primary inspiration for this package is in automatically generating terraform deployment pipelines for multi-regional environment infrastructure. Imagine you support a globally-available microservice architecure that runs on EKS. This means you must create multiple EKS instances, spanning the supported regions, for potentially more than a single _environment_ role. What if Production required eks clusters in 3 localities around the world, with additionally 2 regions per locality where traffic is geo-location routed to the closest in proximity. This results in six (6) clusters, that together actually make up just one platform _environment_ - Production. While this is approaching a scale where a more robust infrastructre control-plane is required, a common intermediate step is to simply increase the dynamic deployment capabilities of the release pipeline.  

In order to maintain DRYness in the terraform code, avoiding duplication of multiple instances of otherwise identical pipeline workflow jobs for each environment, what if instead you could define all the instances of a particular environment category in a single json file and the deployment pipeline is then generated to match at runtime?

That is what this tool enables.  

Let's call the multi-instance environments `Roles`.  

In simplest terms, you define templates of _pre-approval_ and _post-approval_ circleci workflow jobs that include jinja2 style variable-substitution formatting. 

For all instances of each desired Role, circlecigen will generate a deployment pipeline that has:  
* a pre-approve job for each instance, followed by
* an approval step, followed by
* a post-approve job for each instance

#### Setup example for a terraform EKS pipeline

Let's stay with the EKS example mentioned above. Assume that Production requires six (6) clusters in six different regions, Nonproduction likewise requires cluster in each of the same six regions, and an additional three clusters spanning nearby global localities are required to support the software-defined lifecycle of this infrastructure. Therefore we have three environment Roles: infra-dev role that is deployed on git-push, and the nonprod and prod roles that release consequtively upon git-tag.  

Given the output of the actual deployment pipelines, this tool also supports generating the tfvar files for each cluster deployment.  

First, let's define the top level pipelines, roles, and instances definition.   

**environments/multi.json**  

The top-level json definition groups roles by the circleci filter that will trigger the deployment of the associated Roles. Within each Role, define the instances that should exist. And finally list any particular settings associated with an individual instances.  

This multi-environment definition also defines the top-level pipeline structure for other pipelines with the same infrastructure path to production and should probably be maintained in a globally accessible location rather than duplicating the file in multiple repositories. For this example we assume this configuration has already been added locally as a file.  

```json
{
  "infradev": {
    "filter": "*on-push-main",
    "infradev": {
      "infradev-us-east-2": {
        "aws_region": "us-east-2",
        "aws_account_id": "10100000000"
      },
      "infradev-eu-west-3": {
        "aws_region": "us-east-2",
        "aws_account_id": "10100000000"
      },
      "infradev-ap-southeast-3": {
        "aws_region": "eu-west-1",
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
      },
      "nonprod-eu-west-1": {
        "aws_region": "eu-west-1",
        "aws_account_id": "20100000000"
      },
      "nonprod-eu-central-1": {
        "aws_region": "eu-central-1",
        "aws_account_id": "20100000000"
      },
      "nonprod-ap-southeast-2": {
        "aws_region": "ap-southeast-2",
        "aws_account_id": "20100000000"
      },
      "nonprod-ap-southwest-1": {
        "aws_region": "ap-southwest-1",
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
      },
      "prod-eu-west-1": {
        "aws_region": "eu-west-1",
        "aws_account_id": "30100000000"
      },
      "prod-eu-central-1": {
        "aws_region": "eu-central-1",
        "aws_account_id": "30100000000"
      },
      "prod-ap-southeast-2": {
        "aws_region": "ap-southeast-2",
        "aws_account_id": "30100000000"
      },
      "prod-ap-southwest-1": {
        "aws_region": "ap-southwest-1",
        "aws_account_id": "30100000000"
      }
    }
  }
}
```

**environments/default.json**   


Now, define the default values. These are settings to be applied to all instances of all roles:  
```json
{
  "cluster_eks_version": "1.25",
  "cluster_enabled_log_types": ["api", "audit", "authenticator", "controllerManager", "scheduler"],
  "aws_efs_csi_driver_chart_version": "2.4.0",
  "metrics_server_chart_version": "6.2.14",
  "kube_state_metrics_chart_version": "3.3.4",
  "cluster_autoscaler_chart_version": "9.26.0",

  "AL2_x86_64_instance_types": [
    "t2.2xlarge",
    "t3.2xlarge",
    "t3a.2xlarge",
    "m5n.2xlarge",
    "m5.2xlarge",
    "m4.2xlarge"
  ],
  "BOTTLEROCKET_ARM_64_instance_types": [
    "m7g.2xlarge",
    "m6g.2xlarge",
    "t4g.2xlarge"
  ],

  "management_node_group_name": "management-x86-al2-mng",
  "management_node_group_role": "management",
  "management_node_group_ami_type": "AL2_x86_64",
  "management_node_group_platform": "linux",
  "management_node_group_disk_size": "50",

  "baseline_node_group_name": "baseline-arm-rkt-mng",
  "baseline_node_group_role": "baseline",
  "baseline_node_group_ami_type": "BOTTLEROCKET_ARM_64",
  "baseline_node_group_platform": "bottlerocket",
  "baseline_node_group_disk_size": "50",

  "surge_node_group_name": "surge-arm-rkt-mng",
  "surge_node_group_role": "surge",
  "surge_node_group_ami_type": "BOTTLEROCKET_ARM_64",
  "surge_node_group_platform": "bottlerocket",
  "surge_node_group_disk_size": "50",
  
}
```

Next, define Role overrides.

**environments/infradev.json**  

```json
{
  "cluster_log_retention": "10",
  "alert_channel": "dev",

  "management_node_group_capacity_type": "SPOT",
  "management_node_group_desired_size": "3",
  "management_node_group_max_size": "5",
  "management_node_group_min_size": "3",

  "baseline_node_group_capacity_type": "SPOT",
  "baseline_node_group_desired_size": "3",
  "baseline_node_group_max_size": "5",
  "baseline_node_group_min_size": "3",

  "surge_node_group_capacity_type": "SPOT",
  "surge_node_group_desired_size": "0",
  "surge_node_group_max_size": "0",
  "surge_node_group_min_size": "0"
}
```

**environments/nonprod.json**  
   
```json
{
  "cluster_log_retention": "30",
  "alert_channel": "nonprod",

  "management_node_group_capacity_type": "ON_DEMAND",
  "management_node_group_desired_size": "8",
  "management_node_group_max_size": "12",
  "management_node_group_min_size": "8",

  "baseline_node_group_capacity_type": "ON_DEMAND",
  "baseline_node_group_desired_size": "30",
  "baseline_node_group_max_size": "32",
  "baseline_node_group_min_size": "30",

  "surge_node_group_capacity_type": "SPOT",
  "surge_node_group_desired_size": "1",
  "surge_node_group_max_size": "100",
  "surge_node_group_min_size": "1"
}
```

**environments/prod.json**  

```json
{
  "cluster_log_retention": "90",
  "alert_channel": "prod",

  "management_node_group_capacity_type": "ON_DEMAND",
  "management_node_group_desired_size": "5",
  "management_node_group_max_size": "12",
  "management_node_group_min_size": "5",

  "baseline_node_group_capacity_type": "ON_DEMAND",
  "baseline_node_group_desired_size": "15",
  "baseline_node_group_max_size": "17",
  "baseline_node_group_min_size": "15",

  "surge_node_group_capacity_type": "SPOT",
  "surge_node_group_desired_size": "1",
  "surge_node_group_max_size": "100",
  "surge_node_group_min_size": "1"
}
```

From the above files, circlecigen will generate each specific _instance_.tfvars.json file for use as a -var-file by terraform.  

Next, the pipeline files.  

**.circleci/config.yml**  
Of course you must have the regular circleci pipeline file that responds to triggers and actually forms the basis of the generated pipeline. Everything in this file up through the Jobs: or workflow: directive (whichever comes first) forms the starting point for the generated pipeline.  

**.circleci/pre-approve.yml**  

This file is a template that will be populate with instance specific info when the pipeline is generated from within the config.yml pipeline. All values in the env_instance.tfvars.json configuration are avaliable to be used in the jinja template. Keep in mind that the same yaml template is used for each role so it will not work to have a value that ONLY exists in a single instance or role if the value appears in the yaml template.    

```yaml
      - terraform/plan:
          name: {{env_instance}} change plan
          context: << pipeline.parameters.context >>
          workspace: {{env_instance}}
          var-file: {{envpath}}/{{env_instance}}.tfvars.json
          before-terraform:
            - set-environment
          filters: {{filters}}{{priorapprovalrequired}}
```

The indenting is important. This example is using the [twdps/terraform orb](https://circleci.com/developer/orbs/orb/twdps/terraform). Note that in the before-terraform parameter you can pass any pipeline command found in any orb you have included, but more importantly from the config.yaml itself.  

So, for the infra-dev role, circlecigen will create a workflow that runs a terraform plan job using the specific, associated _instance_.tfvar.json var-file. Each such instance runs in parallel.

**.circleci/post-approve.yml**  

Then specify the job to be run if the above plans are approved.  
```yaml
      - terraform/apply:
          name: apply {{env_instance}} change plan
          context: << pipeline.parameters.context >>
          workspace: {{env_instance}}
          var-file: {{envpath}}/{{env_instance}}.tfvars.json
          before-terraform:
            - set-environment
          after-terraform:
            - after-deployment-commands
          requires:
            - approve {{role}} changes
          filters: {{filters}}
```
As you can see, this template will run terraform apply, and in addition to running the set-environment command before the terraaform plan, it will also run an after-deployment-commands after a successful apply. In a real use-case, the after-terraform commands are typical integration and functional tests.  

#### The primary config.yml pipeline

Below is the basic layout of config.yml where the circlecigen package is used to create deployment pipelines used by the continuation orb. In this case, as is common in trunk-based development, git-push results in deployment to an initial development environment, whereas tagging the repository expected to launch a full release pipeline that will push the new code version all the way the production. The example demonstrates usage in a terraform-oriented pipeline but it is not exclusive to such.  

```yaml
version: 2.1

setup: true

orbs:
  continuation: circleci/continuation@0.3.1

on-push-main: &on-push-main
  branches:
    only: /main/
  tags:
    ignore: /.*/

on-tag-main: &on-tag-main
  branches:
    ignore: /.*/
  tags:
    only: /.*/

commands:

  setup-commands:
    parameters:
      ...
    steps:
      ...

  static-code-test-commands:
    parameters:
      ...
    steps:
      ...

  before-deployment-commands:
    parameters:
      ...
    steps:
      ...

  after-deployment-commands:
    parameters:
      ...
    steps:
      ...

jobs:

  my-pre-deploy-jobs:
    parameters:
      ...
    docker:
      - image: ...
    steps:
      - setup-commands:
          parameters: << parameters... >>
      - static-code-test-commands:
          parameters: << parameters... >>

  launch-dynamic-pipeline:
    parameters:
      workflow-name:
        description: Custom name for the resulting workflow within the generated_config.yml
        type: string
      multi-config:
        description: name of the multi-environment definition/configuration file to use
        type: string
        default: multi.json
    executor: continuation/default
    steps:
      - checkout
      - run:
          name: generate continuation pipeline
          command: circlecigen --workflow << parameters.workflow-name >>
      - continuation/continue:
          configuration_path: .circleci/generated_config.yml

workflows:
  my deploy workflow:
    jobs:

      # you may have multple jobs prior to the continuation.
      # Examples might include static code analysis, basically things that
      # you need to run with each git-push but that do not run as part of
      # deployment to any downstream environments.
      - my-pre-deploy-jobs:
          name: could be one or more first jobs
          parameter: required parameters
          filters: *on-push-main

      # the continuation launch will use the dev-deploy.json so as to only
      # deploy to infra-dev instances.
      - launch-dynamic-pipeline:
          name: dev-build
          workflow-name: dev-environment-deployment
          multi-config: dev-deploy.json
          requires:
            - first job 
          filters: *on-push-main

      # this continutation is only called when the repo is tagged and 
      # passes the release.json to generate the full release pipeline
      - launch-dynamic-pipeline:
          name: release candidate
          workflow-name: release-pipeline
          multi-config: release.json
          filters: *on-tag-main
```

Below is a notional example of the resulting pipeline from a git-tag trigger, which is labeled `release` in out multi.json. As you can see, this level of complexity in an infrastructure release pipeline already is likely to inspire the evolution towards a more sophisticated infrastructure management release process. The keyword being evolve. Let actual need be the cause of adoption of the more elaborate release system, but as is nearly always the case, the need to deploy will have deadlines that will be sooner than such an adoption.

```yaml
version: 2.1

orbs:
  continuation: circleci/continuation@0.3.1

on-push-main: &on-push-main
  branches:
    only: /main/
  tags:
    ignore: /.*/

on-tag-main: &on-tag-main
  branches:
    ignore: /.*/
  tags:
    only: /.*/

commands:

  setup-commands:
    parameters:
      ...
    steps:
      ...

  static-code-test-commands:
    parameters:
      ...
    steps:
      ...

  before-deployment-commands:
    parameters:
      ...
    steps:
      ...

  after-deployment-commands:
    parameters:
      ...
    steps:
      ...


workflows:
  version: 2

  release-pipeline:
    jobs:
      - terraform/plan:
          name: nonprod-us-west-2 change plan
          context: << pipeline.parameters.context >>
          workspace: nonprod-us-west-2 
          var-file: env_test/nonprod-us-west-2.tfvars.json
          before-terraform:
            - set-environment
          filters: *on-tag-main

      - terraform/plan:
          name: nonprod-us-east-2 change plan
          context: << pipeline.parameters.context >>
          workspace: nonprod-us-east-2 
          var-file: env_test/nonprod-us-east-2.tfvars.json
          before-terraform:
            - set-environment
          filters: *on-tag-main

      - terraform/plan:
          name: nonprod-eu-west-1 change plan
          ...
          filters: *on-tag-main

      - terraform/plan:
          name: nonprod-eu-central-1 change plan
          ...
          filters: *on-tag-main

      - terraform/plan:
          name: nonprod-ap-southeast-2 change plan
          ...
          filters: *on-tag-main

      - terraform/plan:
          name: nonprod-ap-southwest-1 change plan
          ...
          filters: *on-tag-main

      - approve nonprod changes:
          type: approval
          requires:
            - nonprod-us-west-2 change plan
            - nonprod-us-east-2 change plan
            - nonprod-eu-west-1 change plan
            - nonprod-eu-central-1 change plan
            - nonprod-ap-southeast-2 change plan
            - nonprod-ap-southwest-1 change plan
          filters: *on-tag-main

      - terraform/apply:
          name: apply nonprod-us-west-2 change plan
          context: << pipeline.parameters.context >>
          workspace: nonprod-us-west-2
          var-file: env_test/nonprod-us-west-2.tfvars.json
          before-terraform:
            - set-environment
          after-terraform:
            - after-deployment-commands
          requires:
            - approve nonprod changes
          filters: *on-tag-main

      - terraform/apply:
          name: apply nonprod-us-east-2 change plan
          ...
          filters: *on-tag-main

      - terraform/apply:
          name: apply nonprod-eu-west-1 change plan
          ...
          filters: *on-tag-main

      - terraform/apply:
          name: apply nonprod-eu-central-1 change plan
          ...
          filters: *on-tag-main

      - terraform/apply:
          name: apply nonprod-ap-southeast-2 change plan
          ...
          filters: *on-tag-main

      - terraform/apply:
          name: apply nonprod-ap-southwest-1 change plan
          ...
          filters: *on-tag-main

      - terraform/plan:
          name: prod-us-west-2 change plan
          context: << pipeline.parameters.context >>
          workspace: prod-us-west-2 
          var-file: env_test/prod-us-west-2.tfvars.json
          before-terraform:
            - set-environment
          filters: *on-tag-main
          requires:
            - approve nonprod changes

      - terraform/plan:
          name: nonprod-us-east-2 change plan
          ...
          filters: *on-tag-main
          requires:
            - approve nonprod changes

      - terraform/plan:
          name: nonprod-eu-west-1 change plan
          ...
          filters: *on-tag-main
          requires:
            - approve nonprod changes

      - terraform/plan:
          name: nonprod-eu-central-1 change plan
          ...
          filters: *on-tag-main
          requires:
            - approve nonprod changes

      - terraform/plan:
          name: nonprod-ap-southeast-2 change plan
          ...
          filters: *on-tag-main
          requires:
            - approve nonprod changes

      - terraform/plan:
          name: nonprod-ap-southwest-1 change plan
          ...
          filters: *on-tag-main
          requires:
            - approve nonprod changes

      - approve prod changes:
          type: approval
          requires:
            - prod-us-west-2 change plan
            - prod-us-east-2 change plan
            - prod-eu-west-1 change plan
            - prod-eu-central-1 change plan
            - prod-ap-southeast-2 change plan
            - prod-ap-southwest-1 change plan
          filters: *on-tag-main

      - terraform/apply:
          name: apply nonprod-us-west-2 change plan
          context: << pipeline.parameters.context >>
          workspace: nonprod-us-west-2
          var-file: env_test/nonprod-us-west-2.tfvars.json
          before-terraform:
            - set-environment
          after-terraform:
            - after-deployment-commands
          requires:
            - approve nonprod changes
          filters: *on-tag-main

      - terraform/apply:
          name: apply nonprod-us-east-2 change plan
          ...
          filters: *on-tag-main

      - terraform/apply:
          name: apply nonprod-eu-west-1 change plan
          ...
          filters: *on-tag-main

      - terraform/apply:
          name: apply nonprod-eu-central-1 change plan
          ...
          filters: *on-tag-main

      - terraform/apply:
          name: apply nonprod-ap-southeast-2 change plan
          ...
          filters: *on-tag-main

      - terraform/apply:
          name: apply nonprod-ap-southwest-1 change plan
          ...
          filters: *on-tag-main
```