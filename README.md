# Ansible Roles: FRC7540 WPILib

A set of Ansible roles that manage WPILib FRC Development Tools.

## Installation

Use [ansible-galaxy] to install the collection.

```bash
ansible-galaxy collection install git+https://github.com/FRC7540/frc-ansible.git
```

[ansible-galaxy]:
  https://docs.ansible.com/ansible/devel/collections_guide/collections_installing.html

## Example Playbook

```yaml
---
- hosts:
    - localhost
  roles:
    - frc7540.wpilib.workstation
```

## Requirements

These roles are only tested using Ubuntu/PopOS 20.04 Focal.

Experiments indicate that the most recent FRC tools (2022.04.1) is incompatible
with Ubuntu/PopOS 22.04 Jammy. The install is successful, but certain tools
won't work, e.g., the robot simulator. It's likely that support for more recent
distributions will come with FRC tools for the 2023 season.

## Roles

| roles         | synopsis                       |
| ------------- | ------------------------------ |
| [workstation] | installs frc development tools |

[workstation]: ./roles/workstation/README.md

## License

MIT
