from pathlib import Path
import json
import pytest

from wpilib_vscode_userconf import *


@pytest.fixture
def mock_vscode(mocker):
    return mocker.MagicMock()


@pytest.fixture
def vscode_config() -> dict:
    return {
        "wpilibExtension": {
            "vsix": "WPILib.vsix",
            "name": "wpilibsuite.vscode-wpilib",
            "version": "2022.4.1",
        },
        "thirdPartyExtensions": [
            {"vsix": "Cpp.vsix", "name": "ms-vscode.cpptools", "version": "1.7.1"},
        ],
    }


@pytest.fixture
def basedir(tmpdir: Path) -> Path:
    return Path(tmpdir)


@pytest.fixture
def vscodeconfigpath(basedir: Path, vscode_config: dict) -> Path:
    install_utils_dir = basedir / "installUtils"
    install_utils_dir.mkdir()
    vscode_config_file = install_utils_dir / "vscodeConfig.json"
    with vscode_config_file.open("w") as f:
        json.dump(vscode_config, f)


@pytest.fixture
def vsixpath(basedir: Path) -> Path:
    vsix_dir = basedir / "vsCodeExtensions"
    vsix_dir.mkdir()
    return vsix_dir


@pytest.fixture
def wpilibextpath(vsixpath: Path, vscode_config: dict) -> Path:
    wpilib_vsix_path: Path = vsixpath / vscode_config["wpilibExtension"]["vsix"]
    wpilib_vsix_path.touch()
    return wpilib_vsix_path


@pytest.fixture
def cppextpath(vsixpath: Path, vscode_config: dict) -> Path:
    cpp_vsix_path: Path = vsixpath / vscode_config["thirdPartyExtensions"][0]["vsix"]
    cpp_vsix_path.touch()
    return cpp_vsix_path

@pytest.fixture
def vsix_extensions(wpilibextpath: Path, cppextpath: Path):
    return

@pytest.fixture
def wpilibdirectory(basedir: Path, vscodeconfigpath: Path, vsix_extensions: Path) -> Path:
    return basedir


def test_UninitializedDirectory_SummarizesExtensions(wpilibdirectory, mock_vscode):
    wpilib_config = WpiExtensionInstaller(wpilibdirectory, mock_vscode)
    actual_config = wpilib_config.get_extension_state()
    expected_config = [
        {
            "vsix": "WPILib.vsix",
            "name": "wpilibsuite.vscode-wpilib",
            "version": "2022.4.1",
            "state": "absent",
        },
        {
            "vsix": "Cpp.vsix",
            "name": "ms-vscode.cpptools",
            "version": "1.7.1",
            "state": "absent",
        },
    ]
    assert expected_config == actual_config
    assert wpilib_config.is_install_required() == True


def test_InitializedDirectory_ExtensionsPresent(wpilibdirectory, mock_vscode):
    mock_vscode.list_extensions.return_value = [
        {
            "name": "wpilibsuite.vscode-wpilib",
            "version": "2022.4.1",
        },
        {
            "name": "ms-vscode.cpptools",
            "version": "1.7.1",
        },
    ]
    wpilib_config = WpiExtensionInstaller(wpilibdirectory, mock_vscode)
    actual_config = wpilib_config.get_extension_state()
    expected_config = [
        {
            "vsix": "WPILib.vsix",
            "name": "wpilibsuite.vscode-wpilib",
            "version": "2022.4.1",
            "state": "present",
        },
        {
            "vsix": "Cpp.vsix",
            "name": "ms-vscode.cpptools",
            "version": "1.7.1",
            "state": "present",
        },
    ]
    assert expected_config == actual_config
    assert wpilib_config.is_install_required() == False


def test_OneMismatchedVersion_ExtensionAbsent(wpilibdirectory, mock_vscode):
    mock_vscode.list_extensions.return_value = [
        {
            "name": "wpilibsuite.vscode-wpilib",
            "version": "2022.4.1",
        },
        {
            "name": "ms-vscode.cpptools",
            "version": "1.7.2",
        },
    ]
    wpilib_config = WpiExtensionInstaller(wpilibdirectory, mock_vscode)
    actual_config = wpilib_config.get_extension_state()
    expected_config = [
        {
            "vsix": "WPILib.vsix",
            "name": "wpilibsuite.vscode-wpilib",
            "version": "2022.4.1",
            "state": "present",
        },
        {
            "vsix": "Cpp.vsix",
            "name": "ms-vscode.cpptools",
            "version": "1.7.1",
            "state": "absent",
        },
    ]
    assert expected_config == actual_config
    assert wpilib_config.is_install_required() == True


def test_UnmatchedExtension_ExtensionAbsent(wpilibdirectory, mock_vscode):
    mock_vscode.list_extensions.return_value = [
        {
            "name": "wpilibsuite.vscode-wpilib",
            "version": "2022.4.1",
        },
    ]
    wpilib_config = WpiExtensionInstaller(wpilibdirectory, mock_vscode)
    actual_config = wpilib_config.get_extension_state()
    expected_config = [
        {
            "vsix": "WPILib.vsix",
            "name": "wpilibsuite.vscode-wpilib",
            "version": "2022.4.1",
            "state": "present",
        },
        {
            "vsix": "Cpp.vsix",
            "name": "ms-vscode.cpptools",
            "version": "1.7.1",
            "state": "absent",
        },
    ]
    assert expected_config == actual_config
    assert wpilib_config.is_install_required() == True


def test_NoChangesNeeded_DoesNotTryInstall(wpilibdirectory, mock_vscode, mocker):
    mock_vscode.list_extensions.return_value = [
        {
            "name": "wpilibsuite.vscode-wpilib",
            "version": "2022.4.1",
        },
        {
            "name": "ms-vscode.cpptools",
            "version": "1.7.1",
        },
    ]
    mock_vscode.install_extension = mocker.MagicMock()
    wpilib_config = WpiExtensionInstaller(wpilibdirectory, mock_vscode)
    wpilib_config.install_extensions()
    assert mock_vscode.install_extension.call_count == 0


def test_OneChangeNeeded_InstallOneExtension(wpilibdirectory, mock_vscode, mocker):
    mock_vscode.list_extensions.return_value = [
        {
            "name": "wpilibsuite.vscode-wpilib",
            "version": "2022.4.1",
        },
        {
            "name": "ms-vscode.cpptools",
            "version": "1.7.2",
        },
    ]
    wpilib_config = WpiExtensionInstaller(wpilibdirectory, mock_vscode)
    wpilib_config.install_extensions()
    assert mock_vscode.install_extension.call_count == 1


def test_BadDirectory_RaisesError(basedir, mock_vscode):
    with pytest.raises(Exception):
        WpiExtensionInstaller(basedir, mock_vscode)

def test_MissingVSIX_RaisesError(basedir, vscodeconfigpath, mock_vscode):
    with pytest.raises(Exception):
        WpiExtensionInstaller(basedir, mock_vscode)

def test_readExtensionsFromString():
    data = b'esbenp.prettier-vscode@9.9.0\nms-python.python@2022.16.1\n'
    vscode = VSCode()
    actual = vscode.extensionStateFromSubprocessOutput(data)
    expected = [
        {
            "name": "esbenp.prettier-vscode",
            "version": "9.9.0",
        },
        {
            "name": "ms-python.python",
            "version": "2022.16.1",
        },
    ]
    assert expected == actual

