## Summary

This repository contains "templates" for Git repositories hosting 3rdParty Conan recipes and related files for setting up Continuous Integration services and GitHub. Please report questions or problems here:

https://github.com/bincrafters/community/issues/new  


## Getting Files
To get the templates you can use GitHub's templates feature or copy the files manually.

### Via GitHub Templates
Click on the following links to directly create new GitHub repositories with our templates:
  * [default](https://github.com/bincrafters/template-default/generate) - Used for typical packages ([repository](https://github.com/bincrafters/template-default))
  * [header_only](https://github.com/bincrafters/template-header_only/generate) - Used for header-only packages ([repository](https://github.com/bincrafters/template-header_only))
  * [installer_only](https://github.com/bincrafters/template-installer_only/generate) - Used for tools installers ([repository](https://github.com/bincrafters/template-installer_only))

alternatively, you can clone these repositories and manually copy all the files to a new repository.


## Adapt The Template
Thoroughly review the following files, and edit any lines necessary:
  1. README.md - Find/Replace `package_name` with your actual package name (3 places)
  2. conanfile.py - Virtually every line may need editing
  3. test_package/ - Write a test case


## Maintaining Templates

These templates will always contain some duplicate content. When a change is required, the most thorough and efficient approach is to use a mechanism which lets you search/find/replace all instances of a particular piece of text in all files at one time.  Most graphical text editors have a feature for this, and command-line tools like `sed` are also capable of doing this.  However, the differences between the templates are often subtle and intentional, so most changes should be considered separately in the context of the template.  Use your best judgement to avoid mistakes.
