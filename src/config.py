import yaml
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class KernelConfig:
    name: str
    version: str
    repository: str
    branch: str

@dataclass
class BuildConfig:
    arch: str
    output_dir: str
    config_file: str
    make_target: str

@dataclass
class DeviceTreeConfig:
    dts_files: List[str]

@dataclass
class ModulesConfig:
    enabled: bool
    install_path: str

@dataclass
class EnvironmentConfig:
    make_jobs: int
    cc: Optional[str] = None
    cross_compile: Optional[str] = None

@dataclass
class ProjectConfig:
    kernel: KernelConfig
    build: BuildConfig
    device_trees: DeviceTreeConfig
    modules: ModulesConfig
    environment: EnvironmentConfig
    patches: List[str]

class ConfigLoader:
    @staticmethod
    def load(config_path: str) -> ProjectConfig:
        """Load configuration from YAML file"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        return ConfigLoader._parse_config(config_data)
    
    @staticmethod
    def _parse_config(data: Dict[str, Any]) -> ProjectConfig:
        """Parse configuration data into structured objects"""
        kernel_config = KernelConfig(
            name=data['kernel']['name'],
            version=data['kernel']['version'],
            repository=data['kernel']['repository'],
            branch=data['kernel']['branch']
        )
        
        build_config = BuildConfig(
            arch=data['build']['arch'],
            output_dir=data['build']['output_dir'],
            config_file=data['build']['config_file'],
            make_target=data['build']['make_target']
        )
        
        device_trees_config = DeviceTreeConfig(
            dts_files=data['device_trees']
        )
        
        modules_config = ModulesConfig(
            enabled=data['modules']['enabled'],
            install_path=data['modules']['install_path']
        )
        
        environment_config = EnvironmentConfig(
            make_jobs=data['environment']['make_jobs'],
            cc=data['environment'].get('cc'),
            cross_compile=data['environment'].get('cross_compile')
        )
        
        patches = data.get('patches', [])
        
        return ProjectConfig(
            kernel=kernel_config,
            build=build_config,
            device_trees=device_trees_config,
            modules=modules_config,
            environment=environment_config,
            patches=patches
        )
