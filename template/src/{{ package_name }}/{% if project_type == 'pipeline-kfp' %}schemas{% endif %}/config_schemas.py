from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict


class ProjectSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    project_id: str
    location: str
    env: str
    bucket_name: str
    artifact_registry_repo: str


class PipelineConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    project_settings: ProjectSettings


def load_config(config_path: Path = Path("config/config.yaml")) -> PipelineConfig:
    with open(config_path) as f:
        data = yaml.safe_load(f)
    return PipelineConfig.model_validate(data)
