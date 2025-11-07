import os
import subprocess
import shutil
from typing import List
from .config import ProjectConfig
from .git_utils import GitManager


class KernelBuilder:
    def __init__(self, config: ProjectConfig):
        self.config = config
        self.git_manager = GitManager(config.kernel.repository, config.kernel.branch)
        self.source_dir = None

    def build(self) -> bool:
        """Main build method"""
        try:
            print(
                f"Building kernel {self.config.kernel.name} version {self.config.kernel.version}"
            )

            # Step 1: Prepare source
            self._prepare_source()

            # Step 2: Apply patches
            self._apply_patches()

            # Step 3: Configure kernel
            self._configure_kernel()

            # Step 4: Build kernel
            self._build_kernel()

            # Step 5: Build modules if enabled
            if self.config.modules.enabled:
                self._build_modules()

            # Step 6: Build device trees
            self._build_device_trees()

            print("Build completed successfully!")
            return True

        except Exception as e:
            print(f"Build failed: {e}")
            return False

    def _prepare_source(self):
        """Clone or update kernel source"""
        os.makedirs("kernels", exist_ok=True)
        source_dir = os.path.join("kernels", self.config.kernel.name)

        print(f"Cloning repository: {self.config.kernel.repository}")
        self.source_dir = self.git_manager.clone_repository(source_dir)
        print(f"Source prepared at: {self.source_dir}")

    def _apply_patches(self):
        """Apply patches to kernel source"""
        if not self.config.patches:
            print("No patches to apply")
            return

        for patch_path in self.config.patches:
            if not os.path.exists(patch_path):
                print(f"Warning: Patch file not found: {patch_path}")
                continue

            print(f"Applying patch: {patch_path}")
            try:
                subprocess.run(
                    [
                        "patch",
                        "-p1",
                        "-d",
                        self.source_dir,
                        "-i",
                        os.path.abspath(patch_path),
                    ],
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError as e:
                raise RuntimeError(
                    f"Failed to apply patch {patch_path}: {e.stderr.decode()}"
                )

    def _configure_kernel(self):
        """Configure kernel using specified config"""
        print(f"Configuring kernel with {self.config.build.config_file}")

        env = os.environ.copy()
        if self.config.environment.cc:
            env["CC"] = self.config.environment.cc
        if self.config.environment.cross_compile:
            env["CROSS_COMPILE"] = self.config.environment.cross_compile

        env["ARCH"] = self.config.build.arch

        try:
            # Use specified defconfig
            subprocess.run(
                [
                    "make",
                    f"ARCH={self.config.build.arch}",
                    self.config.build.config_file,
                ],
                cwd=self.source_dir,
                env=env,
                check=True,
                capture_output=True,
            )

            # Optional: Manual configuration
            # subprocess.run(['make', 'menuconfig'], cwd=self.source_dir, env=env, check=True)

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Kernel configuration failed: {e.stderr.decode()}")

    def _build_kernel(self):
        """Build kernel image"""
        print("Building kernel...")

        env = os.environ.copy()
        if self.config.environment.cc:
            env["CC"] = self.config.environment.cc
        if self.config.environment.cross_compile:
            env["CROSS_COMPILE"] = self.config.environment.cross_compile

        env["ARCH"] = self.config.build.arch

        try:
            process = subprocess.Popen(
                [
                    "make",
                    "-j",
                    str(self.config.environment.make_jobs),
                    f"ARCH={self.config.build.arch}",
                    self.config.build.make_target,
                ],
                cwd=self.source_dir,
                env=env,
                stdout=None,
                stderr=None,
                text=True,
                bufsize=1,  # построчная буферизация
                universal_newlines=True,
            )
            process.wait()

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Kernel build failed: {e.stderr.decode()}")

    def _build_modules(self):
        """Build kernel modules"""
        print("Building kernel modules...")

        env = os.environ.copy()
        if self.config.environment.cc:
            env["CC"] = self.config.environment.cc
        if self.config.environment.cross_compile:
            env["CROSS_COMPILE"] = self.config.environment.cross_compile

        env["ARCH"] = self.config.build.arch

        try:
            # Build modules
            subprocess.run(
                [
                    "make",
                    "-j",
                    str(self.config.environment.make_jobs),
                    f"ARCH={self.config.build.arch}",
                    "modules",
                ],
                cwd=self.source_dir,
                env=env,
                check=True,
                capture_output=True,
            )

            # Install modules
            modules_path = os.path.abspath(self.config.modules.install_path)
            os.makedirs(modules_path, exist_ok=True)

            subprocess.run(
                [
                    "make",
                    f"ARCH={self.config.build.arch}",
                    f"INSTALL_MOD_PATH={modules_path}",
                    "modules_install",
                ],
                cwd=self.source_dir,
                env=env,
                check=True,
                capture_output=True,
            )

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Modules build failed: {e.stderr.decode()}")

    def _build_device_trees(self):
        """Build device tree blobs"""
        if not self.config.device_trees.dts_files:
            print("No device trees specified")
            return

        print("Building device trees...")

        env = os.environ.copy()
        if self.config.environment.cc:
            env["CC"] = self.config.environment.cc
        if self.config.environment.cross_compile:
            env["CROSS_COMPILE"] = self.config.environment.cross_compile

        env["ARCH"] = self.config.build.arch

        for dts in self.config.device_trees.dts_files:
            print(f"Building DTB: {dts}")
            try:
                # Build individual device tree
                dtb_file = dts.replace(".dts", ".dtb")
                subprocess.run(
                    ["make", f"ARCH={self.config.build.arch}", dtb_file],
                    cwd=self.source_dir,
                    env=env,
                    check=True,
                    capture_output=True,
                )

            except subprocess.CalledProcessError as e:
                print(f"Warning: Failed to build DTB {dts}: {e.stderr.decode()}")

    def clean(self):
        """Clean build artifacts"""
        if self.source_dir and os.path.exists(self.source_dir):
            print("Cleaning build...")
            env = os.environ.copy()
            env["ARCH"] = self.config.build.arch

            subprocess.run(["make", "clean"], cwd=self.source_dir, env=env)

            # Clean output directory
            if os.path.exists(self.config.build.output_dir):
                shutil.rmtree(self.config.build.output_dir)
