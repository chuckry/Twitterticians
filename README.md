# Twitterticians
Repository for our SI 301 Group Project

Hey guys,

This is most likely where we're going to be organizing, restructuring, and editing the code (or even other files) necessary for our project. I know that some of you are less familiar with git than others, so I'll try to summarize as best I can how to use this.

Since we'll all be working on the same set of files, it's important to keep track of who last edited each file so we don't end up with 5 copies of the same file. The way git works is that files are initialized to this repository (basically a remote overarching folder of files for this project), and when anyone wants to edit a file, they can "pull" down the latest copy from the repos(itory) and edit it.

Once you have finished editing a file, you would "commit" your file with a brief description of the changes you made. It's kind of like hitting Save on a Word document; the latest version of the file is officially saved on YOUR computer. Now, you just need to share it with everyone else. Once all the files you've worked on have been committed to your local repository (your own computer), you can "push" it to the remote repository with a git push. This aligns the remote changes with your current local changes, so the next person to pull down files will receive your changes.

A few notes:
1) Get started by copying the clone URL, navigating to some directory on your computer, and typing "git clone <clone URL>". This initializes your local repos by copying the remote repos data.

2) Anytime you want to add a new file that is not in the remote repos, use "git add <filename>". This says "this file is now a part of the project."

3) In fact, the main commands you'll use are:
- git add (Add file to local repos)
- git commit (Save changes to a file locally; you will be prompted to enter a short message describing the changes you made)
- git push (Make remote repos match your local repos)
- git pull (Make local repos match the remote repos)

4) Always git pull at the beginning of any work you do. Otherwise, you may begin working on a file only to realize later that someone else in the group already edited that file.

5) A possibility in git is to work on multiple "branches" if certain members of the group are working on something completely different than other members of the group. Branches typically denote parallel components of work. For example, I could be working on a powerpoint presentation for some project, and other people in my group could be simultaneously working on a word document summarizing our project to turn into our professor. In this case, I could make a different branch for each of these two components, as they don't necessarily depend on one another. Making these two branches means half my group works on the powerpoint and half works on the Word doc; there's no need to wait for one to be completed before starting the other.

All this stuff probably sounds fairly complicated, and I'm sure there are parts that I missed. If you google anything git related, you will definitely find resources that will better help you understand the process. Overall, we'll mostly just be using add, commit, push, and pull, so I wouldn't worry too much. I also realize that git may mostly seem unnecessary, but I guarantee we will be changing code multiple times over the course of this project. No alternative will be more efficient than git; I've done the old email-files-back-and-forth deal and have learned my lesson. Let me know if you have any questions!

* Also, I'm not sure how some of the mechanics of the command line work on Windows computers. I'm sure resources online will help.
