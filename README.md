# Robotont demos

This is a repository that contants **ROS2 Jazzy** demo packages for Robotont. Note that the repository contains Git **submodules**, which are links to other Git repositories. To clone the repository with submodules use:
``` bash
# move to home directory
cd ~/

# clone git repository with submodules
git clone --recurse-submodules https://github.com/robotont-demos/jazzy_demos.git
```

In order to run the demos, you first have to build them. This is done via `colcon`, which is a command-line tool used to build ROS2 packages and manage their dependencies within a workspace.

The root of a `colcon` workspace must contain a `src/` directory, which holds the ROS  packages to be built. If you cloned the repository into a directory that does not already follow this structure, create a workspace and move the repository into its src/ directory. The correct structure is:
```text
workspace/
└── src/
	├── package1/
	├── package2/
	└── package3/
```

Before building the packages, make sure that ROS2 Jazzy is installed and sourced. This makes the ROS2 tools and environment available in your terminal. Then, navigate to the root of your workspace and build the packages:
``` bash
# source ROS2
source /opt/ros/jazzy/setup.bash

# move to demo repository
cd ~/jazzy_demos

# build the workspace 
colcon build
```

After a successful build, three directories are created in the workspace root:
* `build/` - contains intermediate build files for each package.
* `install/` - contains the installed packages and setup scripts needed to use them.
* `log/` - contains build logs that can help diagnose errors.

Once the build is complete, source the workspace to make the newly built packages available in your current terminal:
```bash
# source built packages
source install/setup.bash
```