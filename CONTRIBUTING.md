# Contributing

When contributing to this repository, preferably first discuss the change you wish to make via issue: 
either open a new one (if needed) or comment in open ones.

## To Keep In mind

- **Always** run "[black](https://github.com/psf/black)" before committing your changes. Taking a look at "pylint" and "mypy" is also welcome.
- It is expected that your changes won't break/stop the rest of the app from working.
- Please follow the Code of Conduct in all your interactions with the project (tldr: be nice).

## Pull Request Process

### Set it up:

0. Fork the repository and clone your fork to your local machine (if you haven't already);
    - Make sure you have installed everything in `requirements.txt`: `pip install -r requirements.txt`;
    - Make sure you have downloaded u2net_human_seg.pth [here](https://github.com/xuebinqin/U-2-Net) and placed it in the correct folder.
1. Make sure your fork is up to date with the original project;
    - Take a look at your fork's GH page: GH will let you know if your fork isn't up-to-date.
2. Make sure your local copy is up-to-date with your fork/original project.
    - `git log --oneline`: compare your latest commits to your fork's;
    - `git pull` any new changes to your local machine.

### Work on it:

1. Start a new branch locally;
2. Make your changes;
3. Push your branch to your fork;
4. Start your Pull Request (PR) from your branch to the original project's target branch (e.g. main);
    - Preferably always link your PR to an issue and explain a bit of what you did (in the PR);
5. Your PR will be reviewed and more changes/explanations might be asked (if necessary);
6. If your changes are accepted they'll be merged;
7. After you changes are merged, make sure to update your fork and local copy before making new changes.

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, gender identity and expression, level of experience,
nationality, personal appearance, race, religion, or sexual identity and
orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment
include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or
advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic
  address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

### Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at [http://contributor-covenant.org/version/1/4][version]

[homepage]: http://contributor-covenant.org
[version]: http://contributor-covenant.org/version/1/4/
