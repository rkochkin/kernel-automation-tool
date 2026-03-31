import pytest
from unittest.mock import Mock, patch
from src.builder import KernelBuilder
from src.config import ProjectConfig, KernelConfig, BuildConfig, DeviceTreeConfig, ModulesConfig, EnvironmentConfig

@pytest.fixture
def mock_config():
    """Create a mock configuration for testing"""
    return ProjectConfig(
        kernel=KernelConfig(
            name="test-kernel",
            version="5.10",
            repository="https://example.com/repo.git",
            branch="test-branch"
        ),
        build=BuildConfig(
            arch="arm64",
            output_dir="./test-output",
            config_file="defconfig",
            make_target="all"
        ),
        device_trees=DeviceTreeConfig(dts_files=[]),
        modules=ModulesConfig(
            enabled=True,
            install_path="./test-modules"
        ),
        environment=EnvironmentConfig(
            make_jobs=4,
            cc="test-gcc",
            cross_compile="test-"
        ),
        patches=[]
    )

def test_builder_initialization(mock_config):
    """Test KernelBuilder initialization"""
    builder = KernelBuilder(mock_config)
    assert builder.config == mock_config
    assert builder.git_manager.repo_url == mock_config.kernel.repository

@patch('subprocess.run')
@patch('os.makedirs')
@patch('os.path.exists')
def test_prepare_source(mock_exists, mock_makedirs, mock_run, mock_config):
    """Test source preparation"""
    mock_exists.return_value = False
    mock_run.return_value = Mock(returncode=0)
    
    builder = KernelBuilder(mock_config)
    builder._prepare_source()
    
    mock_makedirs.assert_called()
    mock_run.assert_called()

@patch('subprocess.run')
@patch('os.path.exists')
def test_apply_patches(mock_exists, mock_run, mock_config):
    """Test patch application"""
    mock_exists.return_value = True
    mock_run.return_value = Mock(returncode=0)
    
    mock_config.patches = ["test.patch"]
    builder = KernelBuilder(mock_config)
    builder.source_dir = "/test/source"
    
    builder._apply_patches()
    
    mock_run.assert_called()
