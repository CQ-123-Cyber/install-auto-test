from action.windows import WindowsInstallTools

if __name__ == "__main__":
    tools = WindowsInstallTools()
    # tools.get_verify_code()
    tools.delete_install_path()
    tools.delete_registry_key()
    # tools.download()
    # tools.unzip_package()
    tools.change_check_config()
    # tools.run_as_admin()
    install_window = tools.get_install_window()
    tools.install_steps(install_window)
