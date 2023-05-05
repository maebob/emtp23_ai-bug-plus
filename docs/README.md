# Generate the Docummentation

This submodule contains Sphinx documentation. To generate the necessary `.rst` files and build the HTML documentation, please follow the instructions below.

## Prerequisites

Make sure you have Sphinx installed. If not, you can install it using `pip`:

```bash
pip install sphinx
```


## Generate .rst Files

To generate the necessary `.rst` files for the documentation, run the following command from the root directory of the submodule:

```bash
sphinx-apidoc -o docs/ .
```

This command will scan the source code in the current directory and create `.rst` files in the `docs/` directory.

## Build HTML Documentation

After generating the `.rst` files, build the HTML documentation using the following command:

```bash
cd docs
make html
```

This command will generate the HTML documentation in the `_build/html` directory within the `docs` folder.

## View Documentation

To view the generated documentation, open the `index.html` file located in the `_build/html` directory using a web browser.


