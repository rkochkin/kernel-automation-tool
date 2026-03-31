import pytest
import tempfile
import os
from src.config import ConfigLoader, ProjectConfig

def test_config_loading():
    """Test loading configuration from YAML"""
    config_content = """
kernel:
  name: "test-kernel"
  version: "5.10"
  repository: "https://example.com/repo.git"
  branch: "test-branch"

build:
  arch: "arm64"
  output_dir: "./test-output"
  config_file: "defconfig"
  make_target: "all"

device_trees:
  - "test1.dts"
  - "test2.dts"

modules:
  enabled: true
  install_path: "./test-modules"

environment:
  make_jobs: 4
  cc: "test-gcc"
  cross_compile: "test-"

patches:
  - "test.patch"
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(config_content)
        config_path = f.name
    
    try:
        config = ConfigLoader.load(config_path)
        
        assert config.kernel.name == "test-kernel"
        assert config.kernel.version == "5.10"
        assert config.build.arch == "arm64"
        assert config.device_trees.dts_files == ["test1.dts", "test2.dts"]
        assert config.modules.enabled == True
        assert config.environment.make_jobs == 4
        assert config.patches == ["test.patch"]
        
    finally:
        os.unlink(config_path)

def test_config_missing_file():
    """Test loading non-existent config file"""
    with pytest.raises(FileNotFoundError):
        ConfigLoader.load("non_existent.yaml")
