from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# can be defined with the workflow or in an outisde JSON file
class Parameter(BaseModel):
    key: str
    name: str
    type: any
    default_value: any
    unit: Optional[str]


class AutoExecution(BaseModel):
    module_url_template: str
    submodule_url_template: str


class Resource(BaseModel):
    name: str
    display_name: str
    resource_key_selectors: list[str]


class SubModule(BaseModel):
    name: str
    display_name: str
    type: str
    can_skip: Optional[bool]
    required_parameters: Optional[Parameter]
    url_template: Optional[str]
    auto_execution: Optional[AutoExecution]
    #is the dataset type related to the resource type or is something else
    input_dataset_types: list[str]
    output_dataset_type: list[str]
    input_resources: list[Resource]
    output_resources: list[Resource]


class Module(BaseModel):
    name: str
    submodules: list[SubModule]
    # All modules will have the following attributes or they depend on dynamic or static configuration
    base_url: str
    required_parameters: list[Parameter]


class Step(BaseModel):
    name: str
    display_name: str
    modules: list[Module]
    step_options: Optional[str]


class WorkflowType(BaseModel):
    id: str
    name: str
    # are they in order?
    steps: list[Step]
    # static or dynamic, can be made an enum
    type: str


class Profile(BaseModel):
    id: str
    workflow_type: WorkflowType
    # is it the default profile for ^^ workflow type
    default: bool
    parameters: list[Parameter]


class Workflow:
    type: WorkflowType
    # initial value = created for this profile only, from default profile of the workflow type, can be overwritten from outside
    profile: Profile


class Dataset(BaseModel):
    id: str
    # can be invalid or overwritten by a workflow type passed from outside
    # their system can search workflow types and pass a valid one. Static ones have priority?
    target_workflow_type: WorkflowType


class Audit(BaseModel):
    # identifier for audit, might not be needed in SQLModel or Mongo translation
    id: str
    # identifier for dataset, can be the DB id of a dateset, an alias or a file name/path
    dataset: Dataset
    date_created: datetime
    workflow: Workflow
    parameters: list[Parameter]
    # from document, clarify if needed
#     import_job_id: str

# Qs
# what is the relation between a profile and a workflow ? is it directed, do each have a default
# same question for workflow type and steps
# relation between resources for steps and parameters