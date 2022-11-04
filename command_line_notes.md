# Command Line Notes
I can insert code with `<code to insert>`. That makes me very happy.

I can do a block of code with three \` like so: `` ```code goes here``` ``.
```
code goes here
```

To display in Atom use `Shift + ctrl + m`.

### General
- `sudo` is used to run commands as the root user. This is useful in the case where we don't have the proper permissions to run them. Insert this before the command you want to run. `sudo <command>`.
- `less` is used to view text files in the terminal without altering them. This is useful for logs.
- `tail -F <file>` is used to view the end of a text file as the file is being written to. Useful for logs while a process is running.
- `apt` - Some kind of package installer????
- `systemctl` - I have no idea????
- `mkdir <directory>` - makes a directory
- `chown <username> <file or directory>` - Change the user to the owner of the file or directory.
- `cd <directory>` - change directory.
- `touch <filename>` - creates a file.
- `ln` - I believe this creates a link????
- `ls` - Lists files and directories in the current directory.
- `curl` - Something to do with urls and the web??????
- `cp` - copy file or directory
- `man <command>` - shows the manual description of that command with all flags and arguments. Very useful!!!
- `cat` - I think it's used to view a file??????????





### Git
List of git commands:
 - `git branch` - Shows all local branches in repository and which branch is the current working branch.
 - `git branch -D <branch name>` - Deletes a local branch.
 - `git checkout <branch name>` - Switches current working branch to the named branch. (Should commit changes before switching branches to avoid merge conflicts which are a huge pain).
 - `git checkout -B <branch name>` - Creates a local branch.
 - `git add <file name>` - Adds the file to be committed???
 - `git add --all` - Adds all files that have changed or been added that aren't in the `.gitignore` file.
 - `git commit -m <commit message in quotes>` - Commits all the changes that were added.
 - `git push origin <branch>` - Pushes the commits to the remote branch.
 - `git pull origin <branch>` - Pulls commits from the remote branch into the local branch.

Typical version control cycle when making changes to files:
1.  Create a branch from the most recent version of the main branch.
```
git pull origin main
git checkout -B <branch name>
```
2. Make changes to files.
3. Save changes to files.
4. Add, commit, and push changes.
```
git add <name of file>
git commit -m <commit message>
git push origin <branch name>
```
5. Repeat steps 1-4 until ready to merge branch into main.
6. Create a pull request on `github.com`.
7. Review changes.
8. Merge branch into main branch and delete remote branch.
9. Pull changes into local main branch.
```
git checkout main
git pull origin main
```
10. Delete local branch
```
git branch -D <branch name>
```

### .gitignore
The `.gitignore` file is used to make sure certain files aren't included in commits.

### Remote Digital Ocean Server
- Use `ssh caleb@calebleehill.com` to remote login. The password is: `hhs013454`
- Websites are found in directory `/var/www`. Each website has a subdirectory of it's own.
- Webpages should be built and then deployed into the respective directory.
- [Digital Ocean Installing Website BYU Instructions](./digital_ocean_install.md)


### Node Package Manager
`npm` is the Node Package Manager. It is used to manage JavaScript packages.
`nvm` is the Node Version Manager. It is used to manage versions of node.

### vue

### MongoDB

### Crontab
- `crontab -l` - View the crontab jobs.
- `crontab -e` - Edit the crontab jobs. This will be opened in vim or another command line text editor.

### Vim Controls
Vim has two modes: Command Mode and Insert Mode.
- `i` to enter insert mode.
- `esc` to enter command mode.
- Command: `:wq` - Save and quit.
- Command: `:q` - Quit without saving.

### View Currently Running Python Jobs
`ps aux | grep python`

### Run python script in the background
`nohup python3.6 <path to python module> <kwargs> &`


### Other Notes
```
ufw app list
ufw allow OpenSSH
ufw enable
ufw status
systemctl status nginx
sudo netstat -nlp
cd /etc/nginx/sites-available
python3 -m http.server
nvm use stable
npm install -g @vue/cli

# Create Vue for front-end
# run this command inside of the website folder
vue create front-end
# There is a true-byu-present

brew services start mongodb-community@5.0
brew services stop mongodb-community@5.0
mongod --config /usr/local/etc/mongod.conf --fork
nvm use stable
nvm use 16
node -v

mongosh
db.getCollection("students").find();
db.students.insertOne({  name: "Emma",
  age: 21,
  status: "active",
  clubs: ["Astronomy Students","Anime Monthly Movie"]
});
use university
npm install cookie-parser cookie-session
npm install readline-sync

# start main page
nvm use 16
npm run serve

# start server
nvm use 16
node server.js

# Change local timezone on server
sudo dpkg-reconfigure tzdata - follow the instructions to select Region/Country
sudo service cron restart
timedatectl - Verify your date settings

```
