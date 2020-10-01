# Nuclear - poc

An ArkScript Package Manager

## Instructions to Run

* Pre-Requisites
    - Python3.6 or above

* Directions to install
    - Clone the repo
    ```bash
    git clone https://github.com/ArkScript-lang/nuclear
    ```
    - Navigate into the repo
    ```bash
    cd nuclear
    ```
    - Activate a virtual env
    ```shell
    python3 -m venv ./venv
    # windows
    .\venv\Scripts\activate.bat
    # linux
    source ./venv/bin/activate
    ```
    - Install the requirements 
    ```bash
    pip3 install -r requirements.txt
    ```

## Commands

* To see the help command

    ```python
    nuclear -h
    ```

    ```python
    nuclear --help
    ```

* To Install an ArkScript Package from Github
    ```python
    nuclear install [-h] [-v VERSION] package
    ```
    - Positional Arguments
    format of the package: 
    ```bash
    user/repo
    ```
    - Optional Arguments
        - show this help message and exit
        ```bash
        -h, --help            
        ```
        - Specify a version for the package
        ```bash
        -v VERSION, --version VERSION
        ```

* To Remove an ArkScript Package
    ```python
    nuclear remove [-h] [-v VERSION] [-g GLOBALLY] package
    ```
    - Positional Arguments:
    format of the package: 
    ```bash
    user/repo
    ```
    - Optional Arguments

        - show this help message and exit
        ```bash
        -h, --help            
        ```
        - Specify a version for the package
        ```bash
        -v VERSION, --version VERSION
        ```
        - Remove a package from the local repositories. If not specified, remove a package from the current project packages list
        ```bash
        -g GLOBALLY, --globally GLOBALLY
        ```




## Launching tests

```shell
python3 -m tests
```