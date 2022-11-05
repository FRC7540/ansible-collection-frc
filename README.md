# Ansible Collection for FRC

This collection contains roles related to FIRST Robotics Competition (FRC),
specifically for WPILib related tools.

The following roles are included:

- [wpilib]: manages installations of WPILib development environments

[wpilib]: ./roles/wpilib/README.md

## Installation

Use [ansible-galaxy] to install the collection.

```bash
ansible-galaxy collection install git+https://github.com/FRC7540/ansible-collection-frc.git
```

[ansible-galaxy]:
  https://docs.ansible.com/ansible/devel/collections_guide/collections_installing.html

## Quick Start

If you just want to install wpilib for the current user, create a playbook
`site.yml` with the following content.

```yaml
---
- hosts:
    - localhost
  roles:
    - frc7540.frc.wpilib
```

Run it using:

```bash
ansible-playbook site.yml -bK
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

Please make sure to update tests as appropriate.
