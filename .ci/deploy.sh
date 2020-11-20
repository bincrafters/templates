#!/usr/bin/env bash

set -e

if [ -z "$TEMPLATE" ]; then
  echo "Please set var TEMPLATE first";
  return -1;
fi

tmpdir="gha-tmp"

# Create or re-create a temporary directory
if [ -d "${tmpdir}" ]; then
  rm -rfv "${tmpdir}";
fi

# Get specific template repository ready
git clone "https://github.com/bincrafters/template-${TEMPLATE}.git" "${tmpdir}"

cd "${tmpdir}"
rm -rv * || true
cd ..


# Copy generic files to tmp dir
cp -v "conandata.yml" "${tmpdir}"
cp -v ".editorconfig" "${tmpdir}"
cp -v --parents ".github/settings.yml" "${tmpdir}"
cp -v --parents ".github/workflows/conan.yml.disabled" "${tmpdir}"
mv "${tmpdir}/.github/workflows/conan.yml.disabled" "${tmpdir}/.github/workflows/conan.yml"
cp -v ".gitignore" "${tmpdir}"
cp -v ".gitattributes" "${tmpdir}"

# Move specific files to tmp dir
cp -rv "${TEMPLATE}/." "${tmpdir}"

cd "${tmpdir}"

if [ -z "$BOT_GITHUB_TOKEN" ] || [ -z "$BOT_GITHUB_NAME" ] || [ -z "$BOT_GITHUB_EMAIL" ] ; then
  echo "Please set vars BOT_GITHUB_NAME, BOT_GITHUB_EMAIL, BOT_GITHUB_TOKEN first";
  return -1;
fi

git config user.name ${BOT_GITHUB_NAME}
git config user.email ${BOT_GITHUB_EMAIL}

# Check if repository is new
git checkout main || git checkout -b main

TARGET_REPOSITORY="https://github.com/bincrafters/template-${TEMPLATE}"
BOT_GITHUB_TOKEN=${TARGET_REPOSITORY/github.com/$BOT_GITHUB_NAME:$BOT_GITHUB_TOKEN@github.com}

git add -A .
# true for the case of no change, we don't want to let CI fail due to this
git commit -am "Automatic update from central templates repository for ${TEMPLATE}" || true

# Push changes
git push ${BOT_GITHUB_TOKEN} || git push -u origin main ${BOT_GITHUB_TOKEN}
