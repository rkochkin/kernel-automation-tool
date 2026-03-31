import pytest
import tempfile
import os
from src.git_utils import GitManager

def test_git_manager_initialization():
    """Test GitManager initialization"""
    manager = GitManager("https://example.com/repo.git", "main")
    assert manager.repo_url == "https://example.com/repo.git"
    assert manager.branch == "main"

# Note: Actual git operations are not tested in unit tests
# as they require network access and external dependencies
