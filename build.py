from pathlib import Path
import shutil
import argparse
from argparse import Namespace
import re
import json

# root path
root_directory = Path(__file__).parent

# input paths
src_directory = root_directory.joinpath("preview_reloader")
src_manifest = src_directory.joinpath("manifest.json")
src_license = root_directory.joinpath("LICENSE")

# build paths
build_directory = root_directory.joinpath("build")
build_manifest = build_directory.joinpath("manifest.json")
build_license = build_directory.joinpath("LICENSE")

# dist paths
dist_directory = root_directory.joinpath("dist")

def clean():
    print("Cleaning existing build output.")
    # Remove old builds
    if build_directory.exists():
        print(f"Cleaning build directory: {build_directory.absolute()}")
        shutil.rmtree(build_directory)

    # Remove old dist directory
    if dist_directory.exists():
        print(f"Cleaning dist directory: {dist_directory.absolute()}")
        shutil.rmtree(dist_directory)

def main(args: Namespace):

    # Check if version argument was set
    version: str | None = None
    if type(args.version) == str:
        if not re.match(r'^\d+\.\d+\.\d+', args.version):
            raise ValueError(f"Start of version '{args.version}' does not match the format '#.#.#'")
        version = args.version
        print(f"Building version: {version}")
    else:
        print("Building without version number")

    # Clean existing build output
    clean()

    # Copy addon files without py cache files to build folder
    print(f"Copying addon files to build directory: {build_directory.absolute()}")
    exclude_patterns = {
        "__pycache__",
        "meta.json"
    }
    if type(version) == str:
        exclude_patterns.add("manifest.json")
    
    # Copy files from addon source directory to build directory
    shutil.copytree(
        src_directory,
        build_directory,
        ignore=shutil.ignore_patterns(*exclude_patterns)
    )
    shutil.copy2(src_license, build_license)

    # Set version in build manifest.json
    if type(version) == str:
        manifest_dict: dict | None = None
        with open(src_manifest, "r") as manifest_input_file:
            manifest_dict = json.load(manifest_input_file)
        manifest_dict["human_version"] = version
        with open(build_manifest, "w") as manifest_output_file:
            json.dump(manifest_dict, manifest_output_file, indent=4)

    # Create zip archive of build folder content
    version_suffix = f"_{version}" if type(version) == str else ""
    dist_zip_base = dist_directory.joinpath(f"preview_reloader{version_suffix}")
    dist_zip = dist_directory.joinpath(f"preview_reloader{version_suffix}.zip")
    dist_addon = dist_directory.joinpath(f"preview_reloader{version_suffix}.ankiaddon")
    
    print(f"Creating zip file: {dist_zip.absolute()}")
    shutil.make_archive(dist_zip_base, "zip", build_directory)
    print(f"Creating ankiaddon file: {dist_addon.absolute()}")
    shutil.copy2(dist_zip, dist_addon)

    print("Build done.")

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(
        prog="Anki Preview Reloader - Build Script",
        description="Creates a build for the Anki Preview Reloader extension for Anki."
    )

    arg_parser.add_argument("-c", "--clean",
        type=bool,
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Only clean existing output, don't create new build.",
        dest="clean"
    )

    arg_parser.add_argument("-v", "--version",
        type=str,
        help="Optional version to set in manifest.json. Must start with a format matching a semantic version '#.#.#'",
        dest="version"
    )

    args = arg_parser.parse_args()

    if args.clean:
        clean()
    else:
        main(args)
