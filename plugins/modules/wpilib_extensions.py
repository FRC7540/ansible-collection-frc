from pathlib import PosixPath
import json
import subprocess

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

DOCUMENTATION = r"""
---
module: wpilib_vscode_userconf

short_description: Configures vscode user data for a vscode install

version_added: "1.0.0"

description: >
    Configures vscode extensions within a users wpilib installation, usually
    ~/wpilib/<year>. It configures a vscode/data directory with all the
    extensions provided in vsCodeExtensions/ and listed in
    installUtils/vscodeConfig.json. Everything gets stored in
    ~/wpilib/<year>/vscode/data and requires the --extensions-dir.

options:
    path:
        description: the root path for the wpilib user installation
        required: true
        type: str

extends_documentation_fragment: []

author:
    - Shane Alvarez (@shanealv)
"""

EXAMPLES = r"""
- name: Configure VSCode for WPILib
  shanealv.frc.wpilib_vscode_userconf:
    path: /home/vagrant/wpilib/2022
"""

RETURN = r"""
extension_dir:
    description: The path of the extensions directory
    type: str
    returned: always
    sample: '/home/vagrant/wpilib/2022/vscode/data/extensions'
user_data_dir:
    description: The path of the user-data directory
    type: str
    returned: always
    sample: '/home/vagrant/wpilib/2022/vscode/data/user-data'
"""


class VSCode:
    def extensionStateFromSubprocessOutput(self, data):
        result = []
        for entry in data.split():
            (name, version) = entry.decode("utf-8").split("@")
            result.append(
                {
                    "name": name,
                    "version": version,
                }
            )
        return result

    def list_extensions(self, extension_dir: PosixPath):
        if not extension_dir.exists() or not extension_dir.is_dir():
            return []
        result = subprocess.check_output(
            [
                "code",
                "--extensions-dir",
                extension_dir,
                "--list-extensions",
                "--show-versions",
            ]
        )
        return self.extensionStateFromSubprocessOutput(result)

    def install_extension(
        self, extension_dir: PosixPath, extension_src_path: PosixPath
    ):
        subprocess.call(
            [
                "code",
                "--extensions-dir",
                extension_dir,
                "--install-extension",
                extension_src_path,
            ]
        )


class WpiExtensionInstaller:
    def __init__(self, wpilib_directory: PosixPath, vscode: VSCode):
        self.vscode = vscode
        self.dir = wpilib_directory
        self.vsix_dir = self.dir / "vsCodeExtensions"
        self.extension_dir = self.dir / "vscode" / "data" / "extensions"
        self.user_data_dir = self.dir / "vscode" / "data" / "user-data"
        self.config_file = self.dir / "installUtils" / "vscodeConfig.json"
        self.state = self._set_extension_state()

    def get_extension_state(self):
        return self.state

    def is_install_required(self):
        extsToInstall = [ext for ext in self.state if ext["state"] != "present"]
        return len(extsToInstall) > 0

    def install_extensions(self):
        ext_to_install = [ext for ext in self.state if ext["state"] != "present"]
        for ext in ext_to_install:
            vsix_path = self.vsix_dir / ext["vsix"]
            self.vscode.install_extension(self.extension_dir, vsix_path)

    def _check_if_extension_state(self, extension, all_extensions):
        matches = [ext for ext in all_extensions if ext["name"] == extension["name"]]
        if len(matches) == 0 or matches[0]["version"] != extension["version"]:
            return "absent"
        return "present"

    def _add_state(self, extension, installed_extensions):
        vsix_file: PosixPath = self.vsix_dir / extension["vsix"]
        if not vsix_file.is_file():
            raise RuntimeError("vsix file for extension is missing")
        return {
            "vsix": extension["vsix"],
            "name": extension["name"],
            "version": extension["version"],
            "state": self._check_if_extension_state(extension, installed_extensions),
        }

    def _set_extension_state(self):
        installed_exts = self.vscode.list_extensions(self.extension_dir)
        config = self._read_vscode_install_config()
        extensions = [config["wpilibExtension"]] + config["thirdPartyExtensions"]
        return list(map(lambda x: self._add_state(x, installed_exts), extensions))

    def _read_vscode_install_config(self):
        # read extensions from wpilib directory
        with self.config_file.open("r") as f:
            config = json.load(f)
        return config


def run_module():
    # boilerplate
    module_args = dict(
        path=dict(type="str", required=True),
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    vscode = VSCode()
    wpiConfig = WpiExtensionInstaller(PosixPath(module.params["path"]), vscode)
    result = {
        "changed": wpiConfig.is_install_required(),
        "extension_dir": str(wpiConfig.extension_dir),
        "user_data_dir": str(wpiConfig.user_data_dir),
    }

    if not module.check_mode:
        wpiConfig.install_extensions()

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
