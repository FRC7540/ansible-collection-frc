# Ansible Role: Vision Tools

Installs [Balena Etcher] and [GRIP] system wide.

Balena Etcher is used for flashing coprocessors using in FRC, such as Raspberry
Pis and Limelights. Keep in mind that root permissions are required to flash
devices.

GRIP is a vision processing prototyping/code-generation tool for basic vision
processing compatible with the RoboRio, Rasberry Pis, and Limelights.

[balena etcher]: https://www.balena.io/etcher/
[grip]: https://wpiroboticsprojects.github.io/GRIP/#/

## Requirements

These roles are only tested using Ubuntu/PopOS 20.04 Focal and 22.04 Jammy. Only
Debian OSs will work with this role.

An internet connection is required for this role.

## Role Variables

| variable                | description                          | default/example |
| ----------------------- | ------------------------------------ | --------------- |
| `balena_etcher_version` | Balena Etcher GitHub release version | `1.13.3`        |
| `grip_version`          | GRIP GitHub release version          | `1.5.2`         |

You can find the latest Etcher releases
[here](https://github.com/balena-io/etcher/releases).

## Example Playbook

```yaml
---
- hosts:
    - localhost
  roles:
    - frc7540.frc.vision_tools
```
