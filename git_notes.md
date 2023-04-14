### Helpful Links
- https://medium.com/@praveenmuth2/learn-how-git-works-internally-with-simple-diagrams-a9349dc32831

## Creating a repository
I created my repository on github. Following that, I wanted to have the repository match on my local machine. Github recommends running the following code on your local machine in the newly created folder that will be the repository.

```
echo "# personal-development" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/calebleehill1993/personal_development.git
git push -u origin main
```

`echo "# personal-development" >> README.md` places the text `# personal-development` inside a file called `README.md` and creates that file if it doesn't exist.

`git init` adds the `.git` directory to the current directory and initializes the folder as a git repository.

`git add README.md` adds the readme file that was created to the index of files to be committed.

`git commit -m "first commit"` commits the changes with the message `first commit`.

`git branch -M main` renames the branch to `main`.

`git remote add origin <url>` connects the remote repository on GitHub with the local repository we created. It also gives the shorthand name `origin` to the remote repository so that we can push and pull from it.

`git push -u origin main` sends all the changes from the local branch `main` to a branch in the remote repo (using the shorthand name "origin") called `main`. The `-u` is used when first connecting to the new remote branch to let it know we want these branches connected.