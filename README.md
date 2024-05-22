Copr repository for git builds of gamescope, commits are fetched every hour.

The packages in this repo should work on Fedora 39 and Fedora 40+.



## Installation 

Activate the repo with `sudo dnf copr enable jackgreiner/gamescope-git` and then run `sudo dnf update --refresh`.

To revert this, remove the copr repository with `sudo dnf copr remove jackgreiner/gamescope-git` and then run `sudo dnf distro-sync` to download your distro's version of the gamescope package.


## Issues

Feel free to open issues when there are build issues I haven't fixed for a few days: https://github.com/ProjectSynchro/copr-gamescope-git/issues

If you'd like me to attempt to package this for other RPM based distros like SUSE, open an issue and I'll see what I can do :)