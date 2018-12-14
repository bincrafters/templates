## Summary

This repository contains "templates" for Git repositories hosting 3rdParty conan recipes and related files for setting up Continuous Integration services and Github. Please report questions or problems here: 

https://github.com/bincrafters/community/issues/new  

## Using Templates

The workflow is intended to be as simple as possible for users to setup a repository based on these templates.  The general steps are: 

1. For a new Conan recipe, create an empty git repository 
2.  Copy and paste the following folders into your repository root as-is, no changes are necessary: 
	1. .github
	2. .ci
3.  Copy and paste all the contents from ONE the template folders into your repository root:
    1. default - Used for typical packages
    2. header_only - Used for header-only packages
    3. installer - Used for tools installers
	
## Maintaining Templates

These templates will always contain some duplicate content. When a change is required, the most thorough and efficient approach is to use a mechanism which lets you search/find/replace all instances of a particular piece of text in all files at one time.  Most graphical text editors have a feature for this, and command-line tools like `sed` are also capable of doing this. 
