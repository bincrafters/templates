#!/usr/bin/env bash

set -e

if [ -z "$template" ]; then
  echo "Please set var template first";
  return -1;
fi

tmpdir="travis-tmp"

# Create or new create a temporary directory
if [ -d "${tmpdir}" ]; then
  rm -rfv "travis-tmp";
fi

# Get specific template repository ready
git clone "https://github.com/bincrafters/template-${template}.git" "${tmpdir}"

cd "${tmpdir}"
rm -rv !(".git"|"."|"..") || true
cd ..

# Copy generic files to tmp dir
cp -v "conandata.yml" "${tmpdir}"
cp -rv ".ci" "${tmpdir}"
cp -rv ".github" "${tmpdir}"

# Move specific files to tmp dir
cp -rv "${template}/." "${tmpdir}"

cd "${tmpdir}"

if [ -z "$GITHUB_TOKEN" ] || [ -z "$GITHUB_BOT_NAME" ] || [ -z "$GITHUB_BOT_EMAIL" ] ; then
  echo "Please set vars GITHUB_BOT_NAME, GITHUB_BOT_EMAIL, GITHUB_TOKEN first";
  return -1;
fi

git config user.name ${GITHUB_BOT_NAME}
git config user.email ${GITHUB_BOT_EMAIL}

# Check if repository is new
git checkout master || git checkout -b master

TARGET_REPOSITORY="https://github.com/bincrafters/template-${template}"
TOKEN_REPO=${TARGET_REPOSITORY/github.com/$GITHUB_BOT_NAME:$GITHUB_TOKEN@github.com}

git add -A .
# true for the case of no change, we don't want to let CI fail due to this
git commit -am "Automatic update from central templates repository for ${template}" || true

# Push changes
git push ${TOKEN_REPO} || git push -u origin master ${TOKEN_REPO}
