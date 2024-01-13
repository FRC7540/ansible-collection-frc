# Ansible Role: WPILib

Installs [WPILib] development tools for multiple users.

This presents at alternative to manually installation use the WPILib installer,
which is particularly useful when using shared workstations.

[wpilib]: https://wpilib.org/

## Requirements

These roles are only tested using Ubuntu/PopOS 20.04 Focal and 22.04 Jammy.

This role has been tested for Java projects only. C++ projects may not work.

## Role Variables

| variable                 | description                                               | default/example                                   |
| ------------------------ | --------------------------------------------------------- | ------------------------------------------------- |
| `wpilib_release_version` | WPILib release version                                    | `2023.1.1`                                        |
| `wpilib_release_hash`    | WPILib release version hash (usually a sha256 or md5)     | `md5:07c3..`                                      |
| `wpilib_install_root`    | Directory to store WPILib archives prior to user installs | `/opt/wpilib`                                     |
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

The installation made by this role differs from the WPILib Linux installer in
several ways:

- the mono based installer is not used at all
- the system vscode installation is used
  - extensions still installed per-user in custom location
  - user data still installed per-user in custom location
- the desktop shortcut is slightly different
  - uses vscode flags to setting extensions and user-data
- most content is installed globally instead of per-user:
  - gradle is installed into `/opt/gradle`
  - java is installed into `/opt/java`
  - docs are installed into `/opt/wpilib/docs`
