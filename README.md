# Templates for Conan

This repository contains "templates" for Git repositories hosting Conan recipes and related files for setting up Continuous Integration services and GitHub. Please report questions or problems here:

https://github.com/bincrafters/community/issues/new


## Getting Files

Click on the following link to directly create a new GitHub repository with our templates:
  * [Generate new repository](https://github.com/bincrafters/templates/generate)

alternatively, you can clone this repository and manually copy all the files to a new repository.


## Adapt The Template

Thoroughly review the following files, and edit any lines necessary:
  1. Choose the right folder in `recipes/` - depending on the type of software you want to package - a regular library, a header-only project or an executable/installer-only project
  2. Rename the respective folder to the name of your new package (e.g. rename `default` to `sdl`) - delete the other unused folders
  3. Now edit the files in your new folder as described in the following steps
  4. `config.yml` - Replace the version
  5. `conandata.yml` - Replace version, download url and the SHA256 checksum ([explanation](https://github.com/conan-io/conan-center-index/blob/master/docs/how_to_add_packages.md#the-conandatayml))
  6. `conanfile.py` - Virtually every line may need editing
  7. `test_package/` - Write a minimal test case
  8. Test your recipe locally by running e.g. `conan create . <libname>/<version>@<your-name>/stable`
  9. `README.md` - You probably want to edit this Readme to tell your users what they can find in your repository
  10. Commit your work to git

If you want to add more Conan recipes in the future, copy the fitting `recipes/` subfolder again in your repository and repeat the steps above. You can have an arbitrary amount of recipes in a single repository.


## Maintaining Templates

These templates will always contain some duplicate content. When a change is required, the most thorough and efficient approach is to use a mechanism which lets you search/find/replace all instances of a particular piece of text in all files at one time.  Most graphical text editors have a feature for this, and command-line tools like `sed` are also capable of doing this.  However, the differences between the templates are often subtle and intentional, so most changes should be considered separately in the context of the template.  Use your best judgement to avoid mistakes.
