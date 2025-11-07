import os
import subprocess
from typing import Optional
import tempfile

class GitManager:
    def __init__(self, repo_url: str, branch: str = "master"):
        self.repo_url = repo_url
        self.branch = branch
        self.repo_dir = None
    
    def clone_repository(self, target_dir: str) -> str:
        """Clone repository to target directory"""
        if os.path.exists(target_dir):
            self._update_repository(target_dir)
            return target_dir
        
        try:
            subprocess.run([
                'git', 'clone', 
                '--branch', self.branch,
                '--depth', '1',
                self.repo_url, 
                target_dir
            ], check=True, capture_output=True)
            
            self.repo_dir = target_dir
            return target_dir
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to clone repository: {e.stderr.decode()}")
    
    def _update_repository(self, repo_dir: str):
        """Update existing repository"""
        try:
            # Check if we're on the right branch
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                cwd=repo_dir, capture_output=True, text=True, check=True
            )
            current_branch = result.stdout.strip()
            
            subprocess.run(['git', 'reset','--hard', self.branch], cwd=repo_dir, check=True)
            if current_branch != self.branch:
                subprocess.run(['git', 'checkout', self.branch], cwd=repo_dir, check=True)
            
            # Pull latest changes
            subprocess.run(['git', 'pull'], cwd=repo_dir, check=True)
            
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to update repository: {e.stderr}")
    
    def get_commit_hash(self, repo_dir: str) -> str:
        """Get current commit hash"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=repo_dir, capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to get commit hash: {e.stderr}")
