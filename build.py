from pathlib import Path
import shutil
import sys

# root path
root_directory = Path(__file__).parent

# input paths
addon_directory = root_directory.joinpath("preview_reloader")

# build paths
build_directory = root_directory.joinpath("build")

# dist paths
dist_directory = root_directory.joinpath("dist")
dist_zip_base = dist_directory.joinpath("preview_reloader")
dist_zip = dist_directory.joinpath("preview_reloader.zip")
dist_addon = dist_directory.joinpath("preview_reloader.ankiaddon")

def clean():
    # Remove old builds
    if build_directory.exists():
        shutil.rmtree(build_directory)

    # Remove old dist directory
    if dist_directory.exists():
        shutil.rmtree(dist_directory)

def main():
    clean()

    # Copy addon files without py cache files to build folder
    print(f"Copying addon files to build directory: {build_directory.absolute()}")
    exclude_patterns = {
        "__pycache__"
    }
    shutil.copytree(
        addon_directory,
        build_directory,
        ignore=shutil.ignore_patterns(*exclude_patterns)
    )

    # Create zip archive of build folder content
    print(f"Creating zip file: {dist_zip.absolute()}")
    shutil.make_archive(dist_zip_base, "zip", build_directory)
    print(f"Creating ankiaddon file: {dist_addon.absolute()}")
    shutil.copy2(dist_zip, dist_addon)

    print("Build done.")

if __name__ == "__main__":
    if "clean" in sys.argv:
        clean()
    else:
        main()
