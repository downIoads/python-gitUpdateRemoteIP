import os

def getGitFolderPathsRecursively(directory):
    git_folders = []
    for dirpath, dirnames, filenames in os.walk(directory):
        if ".git" in dirnames:
            git_folders.append(os.path.join(dirpath, ".git"))
    return git_folders

def main():
    OLD_IP = "192.168.100.89"
    NEW_IP = "192.168.100.96"

    REPLACE_HTTP_WITH_SSH = True # False: http will stay http, True: http will become git (so no username + pw input necessary)
    GITLAB_PORT = "8084" # useful to make replacing http with ssh easier

    # 1. get git folders
    rootdir = "."
    gitFolderList = getGitFolderPathsRecursively(rootdir)
    if len(gitFolderList) == 0:
        print("Did not find any .git folder in any subdir")
        return
    #print(gitFolderList)

    # 2. fix URL for each git folder (OLD_IP gets replaced with NEW_IP)
    counter = 0
    for folder in gitFolderList:
        # ensure config file exists
        configLocation = os.path.join(folder, "config")
        if not os.path.exists(configLocation):
            print(configLocation, "does not exist. Skipping this folder.")
            continue
        
        # read config file and get new config
        newConfigContent = ""
        with open(configLocation, "r", encoding="utf-8") as f:
            newConfigContent = f.read().replace(OLD_IP, NEW_IP)
       
        # if REPLACE_HTTP_WITH_SSH is True more work is necessary:
        if REPLACE_HTTP_WITH_SSH:
            #       1. replace http:// with git@
            newConfigContent = newConfigContent.replace("http://", "git@")
            #       2. remove <ip>:<port> becomes <ip>:
            newConfigContent = newConfigContent.replace(NEW_IP + ":" + GITLAB_PORT, NEW_IP + ":")

        # write new config
        with open(configLocation, "w", encoding="utf-8") as f:
            f.write(newConfigContent)
            counter += 1

    # 3. done
    print(f"Successfully updated {counter} .git folders.")

main()
# USAGE:    Put this script at the root folder that contains all your git projects,
#           adjust OLD_IP and NEW_IP, set value REPLACE_HTTP_WITH_SSH and set GITLAB_PORT and run it.
