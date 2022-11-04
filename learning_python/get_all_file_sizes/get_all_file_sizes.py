import os
print(os.getcwd())
for path, subdirs, files in os.walk('/Users/calebhill/Documents/personal_development'):
    for name in files:
        print(os.path.getsize(os.path.join(path, name)), os.path.join(path, name))