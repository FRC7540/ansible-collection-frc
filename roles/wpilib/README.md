# Ansible Role: WPILib

Installs [WPILib] development tools for multiple users.

This presents at alternative to manually installation use the WPILib installer,
which is particularly useful when using shared workstations.

[wpilib]: https://wpilib.org/

## Requirements

These roles are only tested using Ubuntu/PopOS 20.04 Focal.

Experiments indicate that the most recent FRC tools (2022.04.1) is incompatible
with Ubuntu/PopOS 22.04 Jammy. The install is successful, but certain tools
won't work, e.g., the robot simulator. It's likely that support for more recent
distributions will come with FRC tools for the 2023 season.

This role has been tested for Java projects only. C++ projects may not work.

## Role Variables

| variable                 | description                                               | default/example                                   |
| ------------------------ | --------------------------------------------------------- | ------------------------------------------------- |
| `wpilib_release_version` | WPILib release version                                    | `2022.4.1`                                        |
| `wpilib_release_hash`    | WPILib release version hash (usually a sha256 or md5)     | `md5:fe77..`                                      |
| `wpilib_install_root`    | Directory to store WPILib archives prior to user installs | `/usr/local/wpilib`                               |
| `wpilib_users`           | A list of users that will get a WPILib installation       | `{{ ansible_env.USER }}` (i.e., the current user) |

You can find the latest WPILib release version and archive hashes
[here](https://github.com/wpilibsuite/allwpilib/releases).

## Dependencies

This role depends on [gantsign.visual-studio-code] for adding the microsoft
repos for installing Visual Studio Code, with the exeption of Pop! OS. No
special configruations are necessary.

[gantsign.visual-studio-code]:
  https://github.com/gantsign/ansible-role-visual-studio-code

## Example Playbook

```yaml
---
- hosts:
    - localhost
  roles:
    - frc7540.frc.wpilib
      wpilib_users:
        - jane
        - john
```

## Comparison to the WPILib Installers

The installation made by this role differes from the WPILib Linux installer in
several ways:

- the mono based installer is not used at all
- the system vscode installation is used
  - extensions still installed per-user in custom location
  - user data still installed per-user in custom location
- the desktop shortcut is slightly different
  - uses vscode flags to setting extensions and user-data

## Known Issues

- user install includes more directories than is strictly necessary
- user install task is slow when running playbooks a second time
- included gradle is not installed into cache location
