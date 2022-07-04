# How to Start Contributing to Project Nebulus!


## Table of Contents



- [Setting Up Your Coding Environment](#setting-up-your-coding-environment)

- [Setting Up MongoDB](#setting-up-mongodb)
 
- [Using Git](#using-git)

- [Contributing](#contributing)


---


## Setting Up Your Coding Environment


### Step 1: Get the IDEs

1) Go to [https://www.jetbrains.com/shop/eform/students](https://www.jetbrains.com/shop/eform/students) and make a new application. If you already have the [GitHub developer pack](https://education.github.com/pack), you may choose the GitHub tab. This will give you premium for all JetBrains IDEs.

2) Wait for an email from `JetBrains Sales` with an email titled `License Certificate for your JetBrains Educational Pack`. Give it 2 minutes, if its not there wait another 2 minutes. It's usually very quick!

3) Download required Nebulus IDEs. `PyCharm Professional` (Don't get PyCharm CE/Community Edition), `WebStorm`, `DataGrip`. Optional IDEs include `IntelliJ Ultimate` and `CLion`


#### Download Links:

- [PyCharm Professional](https://www.jetbrains.com/pycharm/download/)


> Make sure to download Professional, not Community Edition



- [WebStorm](https://www.jetbrains.com/webstorm/download/)
- [DataGrip](https://www.jetbrains.com/datagrip/download/)
- [CLion](https://www.jetbrains.com/clion/download/) (optional)
- [IntelliJ Ultimate](https://www.jetbrains.com/idea/download) (optional)


> Make sure to download Ultimate, not Community Edition





### Step 2: Get the GitHub Repository on Your Device


#### Clone the Repository


```
$ git clone https://github.com/ProjectNebulus/ProjectNebulus.git [optional directory]
```



### Step 3: Installing Dependencies


#### Install Python 3.10 from [python.org](https://www.python.org/downloads/release/python-3100/)


##### MacOS ([homebrew](https://brew.sh/))





```bash
$ brew install python@3.10
```


##### Linux

```bash 
$ sudo apt install software-properties-common -y
$ sudo add-apt-repository ppa:deadsnakes/ppa -y
$ sudo apt install python3.10
```


#### Instal dependencies with [Poetry](https://python-poetry.org/docs/#installation")

```
$ poetry install
```


### Step 4: Configure Username and Password (Optional)


> ⚠ WARNING: If you haven't created a Personal Access Token yet, please make one! It is basically your password when using the github API.

> To create one go to Settings > Developer Settings > Personal access tokens


#### Set Username

```
$ git config --global user.name "your username"
```



#### Set Password (Personal Access Token)


##### 1. Caching Credentials With Keychain Access (MacOS ONLY)



1. Open Keychain Access (You can search "Keychain" in spotlight) 

![image](https://user-images.githubusercontent.com/76001641/149199644-91155da4-2cff-46cd-87fa-dd115a459e79.png)
2. In Keychain, search for "github"
3. There will be a few results, click on the one that says "Internet Password"
4. Click the "Show Password" option and enter your computer password to let Keychain have access.
5. Enter Your Personal Access Token in the area where it shows your password.


### 2. Caching Credentials (Github CLI)

- There are quite a few ways to install the Github CLI

- You can see them all [here](https://cli.github.com/manual/installation)

**Caching Credentials**


```
$ gh auth login
```




* When asked which account you want to login with, choose `Github.com`
* When prompted for your preferred protocol for Git operations, select `HTTPS`.
* When asked if you would like to authenticate to Git with your GitHub credentials, enter `Y`.
* When asked how you would like to authenticate choose `Paste an authentication token` then paste your `Personal Access Token`


---


## Setting Up MongoDB


### Creating a .env file

A .env file stores environmental variables.

Environmental variables can be thought of as secrets since they are used to store confidential information.


#### .env File Syntax

The syntax of .env files are shown as the following:


```
key=value
```


In our case, we reference the `MONGO` key and the `MONGOPASS` key to connect to our MongoDB Database.



- `MONGO` - the full connection URI
- `MONGOPASS` - the database user's password. 
    * The database user allows us to select certain scopes for connecting to the database.

In our case, this user, called `MainUser` has admin permissions

Right now the `MONGO` key is equal to `mongodb+srv://MainUser:fk6hRm3j3ks0ryLr@cluster0.yknnf.mongodb.net/Nebulus?retryWrites=true&w=majority` and the `MONGOPASS` key is equal to `fk6hRm3j3ks0ryLr`

So the completed .env file becomes


```
MONGO=mongodb+srv://MainUser:fk6hRm3j3ks0ryLr@cluster0.yknnf.mongodb.net/Nebulus?retryWrites=true&w=majority

MONGOPASS=fk6hRm3j3ks0ryLr
```


This file is not stored might not be stored in the Github repository for security reasons, so if it’s not there you will have to create it on your own and paste the contents.


---


## Using Git


### Git workflow


#### Why do we need a git workflow?

Just committing to the main branch can be really disorganized, it makes commit history bad, and when deployment comes around, it’s not good.


### The workflow


#### Main branch

Branch that is being deployed, only merge branches with this. The only branches that can be merged directly with main are either hotfixes, or the development branch (as follow) for a new release.


#### __Development branch__

The only branch that is never deleted. This is for development and it only gets merged with the main branch once all the features are in it, tested, and ready for deployment.


#### Feature Branches

Branched off the development branches. Let's say I want to implement another kind of Oath. I branch it off development, commit over the course of a few weeks, and then merge it back with the development branch. These should be named with the prefix `feat-`


#### Hotfix Branches

Branches that can be branched directly off the main branch or can be branched off the development branch. If it's off the main branch, it means that there’s a bug after deployment that we did not catch in testing. It's off development, it's just a generic bug that may need to be fixed immediately for future development of the project. These should be named with the prefix `hotfix-`


### Essential Git commands



* `Git add *` or `git add .` - stages all the files for a commit
    * You can specify what files to stage with `Git add &lt;file path>`
* `Git commit -m "commit message goes here" - `create a commit
* `Git push` - push your local commits
* `Git pull` - pull from github


### Working with branches


- [https://www.nobledesktop.com/learn/git/git-branches](https://www.nobledesktop.com/learn/git/git-branches)


### More Commands


- [https://education.github.com/git-cheat-sheet-education.pdf](https://education.github.com/git-cheat-sheet-education.pdf)


### Situations

Let's say you wanna help with a bug fix but you don’t know if a branch has been created, well just use the command and find out

Whenever you start, list all branches and make sure its good, try to use the most concentrated chat for questions


### Some other rules

For chats, try to be really to that channel because we don’t want stuff to get buried under random stuff

Let's get the development of this up and running!!!


---


## Contributing


### Code Style

Use our project-specific conventions for code formatting. For example, we use [prettier](https://prettier.io) for JavaScript (and related), [black](https://github.com/psf/black) for Python, etc. There should be scripts already written to do this, such as npm run format (prettier) or npm run format:py (python formatters).


### Commit Messages

Although not required, please try to follow the [conventional commits specification](https://www.conventionalcommits.org/en/v1.0.0/) for your commits. If not, **write a meaningful commit message to explain what the commit changes.**
