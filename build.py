import platform
from conan.packager import ConanMultiPackager, os, re

    
if __name__ == "__main__":
    reponame_a = os.getenv("APPVEYOR_REPO_NAME","")
    repobranch_a = os.getenv("APPVEYOR_REPO_BRANCH","")

    reponame_t = os.getenv("TRAVIS_REPO_SLUG","")
    repobranch_t = os.getenv("TRAVIS_BRANCH","")

    username, repo = reponame_a.split("/") if reponame_a else reponame_t.split("/")
    channel, version = repobranch_a.split("/") if repobranch_a else repobranch_t.split("/")
    
    with open("conanfile.py", "r") as conanfile:
        contents = conanfile.read()
        name = re.search(r'name\s*=\s*"(\S*)"', contents).groups()[0]
    
    os.environ["CONAN_USERNAME"] = username
    os.environ["CONAN_CHANNEL"] = channel
    os.environ["CONAN_REFERENCE"] = "{0}/{1}".format(name, version)
    os.environ["CONAN_UPLOAD"]="https://api.bintray.com/conan/{0}/public-conan".format(username)
    os.environ["CONAN_REMOTES"]="https://api.bintray.com/conan/conan-community/conan"
    builder = ConanMultiPackager(args="--build missing")
    builder.add_common_builds(shared_option_name=name+":shared")
    filtered_builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        # XXX (uilian.ries): MTd could not link
        if settings["compiler"] == "Visual Studio" and settings["compiler.runtime"] == "MTd":
            continue
        # XXX (uilian.ries): libstdc++ could not link on Linux
        if settings["compiler"] == "clang" and platform.system() == "Linux":
            settings["compiler.libcxx"] = "libc++"
        filtered_builds.append([settings, options, env_vars, build_requires])
    builder.builds = filtered_builds
    builder.run()
