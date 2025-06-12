# Developer contribution guide
Contribute to the repository by opening a pull request.

## Local
Develop code locally by cloning the source code, creating a development environment and installing it.

1. Install [mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html), then launch the `Miniforge Prompt`.

2. Clone the `main` branch of `Qt-collaboration` locally, and navigate into where it has been cloned:
```sh
# Clone (download) source code
git clone git@github.com:TomographicImaging/Qt-collaboration.git
cd Qt-collaboration
```

3. Create the mamba environment using the following command:
```sh
# Create environment
mamba env create -f recipe/Qt-collab_env.yml
```

`Qt-collaboration` uses the [`qtpy`](https://github.com/spyder-ide/qtpy) abstraction layer for Qt bindings, meaning that it works with either PySide or PyQt bindings. Thus, `Qt-collab_env` does not depend on either. The environment can be updated with either `pyside2` or `pyqt5`, as follows.
```sh
mamba env update --name Qt-collab_env --file pyside2_env.yml
```
or
```sh
mamba env update --name Qt-collab_env --file pyqt5_env.yml
```

4. Activate the environment:
```sh
mamba activate Qt-collab_env
```

5. Install the dependencies:
```sh
pip install .
```

### Merge the `main` branch
Conflicts may exist if your branch is behind the `main` branch. To resolve conflicts between branches, merge the `main` branch into your current working branch:
```sh
git merge main
```

### Changelog
Located in [`CHANGELOG.md`](./CHANGELOG.md).

#### Changelog style
TBC
- Be concise by explaining the overall changes in only a few words.
- Mention the relevant PR in brackets.

