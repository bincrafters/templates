## Summary

This repository contains "templates" for Git repositories hosting 3rdParty Conan recipes and related files for setting up Continuous Integration services and GitHub. Please report questions or problems here:

https://github.com/bincrafters/community/issues/new  


## Using Templates Via GitHub
Click on the following links to directly create new GitHub repositories with our templates:
  * [default](https://github.com/bincrafters/template-default/generate) - Used for typical packages
  * [header_only](https://github.com/bincrafters/template-header_only/generate) - Used for header-only packages
  * [installer_only](https://github.com/bincrafters/template-installer_only/generate) - Used for tools installers


## Using Templates Manually

The workflow is intended to be as simple as possible for users to setup a repository based on these templates.  The general steps are:

1. For a new Conan recipe, create an empty git repository
2.  Copy and paste the following folders into your repository root as-is, no changes are necessary:
	1. .github
	2. .ci
3.  Copy and paste all the contents from ONE the template folders into your repository root:
    1. default - Used for typical packages
    2. header_only - Used for header-only packages
    3. installer_only - Used for tools installers
4.  Thoroughly review the following files, and edit any lines necessary:
	1. README.md - Find/Replace `package_name` with your actual package name (3 places)
	2. conanfile.py - Virtually every line may need editing


## Maintaining Templates

These templates will always contain some duplicate content. When a change is required, the most thorough and efficient approach is to use a mechanism which lets you search/find/replace all instances of a particular piece of text in all files at one time.  Most graphical text editors have a feature for this, and command-line tools like `sed` are also capable of doing this.  However, the differences between the templates are often subtle and intentional, so most changes should be considered separately in the context of the template.  Use your best judgement to avoid mistakes.
