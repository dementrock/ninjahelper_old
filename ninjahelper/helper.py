def rlistdir(rootdir='.'):
    import os
    import sys
    fileList = []
    for root, subFolders, files in os.walk(rootdir):
        for file in files:
            fileList.append(os.path.join(root,file))
    return fileList
