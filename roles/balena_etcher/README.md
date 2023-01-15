# Ansible Role: Balena Etcher

Installs [Balena Etcher] system wide.

Balena Etcher is used for flashing coprocessors using in FRC, such as Raspberry
Pis and Limelights. Keep in mind that root permissions are required to flash
devices.

[balena etcher]: https://www.balena.io/etcher/

## Requirements

These roles are only tested using Ubuntu/PopOS 20.04 Focal and 22.04 Jammy.

An internet connection is required for this role.

## Role Variables

| variable                | description                          | default/example |
| ----------------------- | ------------------------------------ | --------------- |
| `balena_etcher_version` | Balena Etcher GitHub release version | `1.13.3`        |

You can find the latest Etcher releases
[here](https://github.com/balena-io/etcher/releases).

## Example Playbook

```yaml
---
- hosts:
    - localhost
  roles:
    - frc7540.frc.balena_etcher
```
