import yaml

auth = None


def loadFile(path, defaultStruct, critical):
    # console.debug(f"configHandler.loadFile({path}, [defaultStruct], {critical})")
    try:
        file = open(path, "r")  # Open file for read
        yamlStruct = yaml.safe_load(file)  # Parse YAML
        file.close()  # Freeing file up for other use
        # console.info(f"configHandler.loadFile(...): Requested config \"{path}\" was successfully loaded!")
        return yamlStruct  # Return struct
    except FileNotFoundError:  # File doesn't exist
        # console.warning(f"configHandler.loadFile(...): Requested config \"{path}\" doesn't exist, creating...")
        file = open(path, "w")  # Create file
        yaml.dump(defaultStruct, file)  # Writing default struct to file
        file.close()
        if critical:  # Config is critical to be filled and can't use it's default values
            # console.error(f"configHandler.loadFile(...): Critical config \"{path}\" wasn't filled!")
            exit(1)  # Exiting with code 1 to stop execution
        else:
            return defaultStruct  # Return the default struct that was just written to the file


# Default configuration structure as Python dictionary
defaultAuth = {
    "clientid": "[YOUR CLIENTID HERE]",
    "oauth": "[YOUR OAUTH TOKEN HERE]"
}


def loadAuth():
    global auth
    auth = loadFile("auth.yml", defaultAuth, True)


def getAuth():
    global auth
    if auth is not None:
        return auth
    else:
        loadAuth()
        return auth
