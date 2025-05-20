import os
import re


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
IGNORED_PATTERN = re.compile(r"^\..*|.*\.md$")
TEMPLATE_PATH = "TEMPLATE.md"
ROOT_DIR = "./wallpapers/"
MAIN_README = "README.md"
AUTOMATED_BLOCK_START = "<!-- AUTOMATED BLOCK START -->"
AUTOMATED_BLOCK_END = "<!-- AUTOMATED BLOCK END -->"


def load_template(path):
    """Load the markdown template from a file."""
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def is_valid_image(filename):
    """Check if the file is a valid image and not ignored."""
    ext = os.path.splitext(filename)[1].lower()
    return ext in IMAGE_EXTENSIONS and not IGNORED_PATTERN.match(filename)


def rename_images(directory, images):
    """
    Rename images to a sequential format (001.jpg, 002.png, etc.).
    Returns a list of new filenames.
    """
    renamed = []
    for index, image in enumerate(sorted(images), 1):
        ext = os.path.splitext(image)[1]
        new_name = f"{index:03d}{ext}"
        os.rename(os.path.join(directory, image), os.path.join(directory, new_name))
        renamed.append(new_name)
    return renamed


def create_readme(directory, template, image_filenames):
    """Create a README.md in the directory using the template and image links."""
    readme_path = os.path.join(directory, "README.md")
    with open(readme_path, "w", encoding="utf-8") as file:
        file.write(template + "\n")
        for image in image_filenames:
            file.write(f"![]({image})\n")


def format_readme_list(readme_names):
    """Convert readme folder names to markdown list items."""
    return [
        f"- [{name.replace('_', ' ').title()}](./{name}/README.md)"
        for name in readme_names
    ]


def update_main_readme(readme_path, new_entries):
    """Replace the automated block in the main README.md with new entries."""
    with open(readme_path, "r+", encoding="utf-8") as file:
        content = file.read()

        # Clear the automated block
        content = re.sub(
            rf"{AUTOMATED_BLOCK_START}.*?{AUTOMATED_BLOCK_END}",
            f"{AUTOMATED_BLOCK_START}\n\n{AUTOMATED_BLOCK_END}",
            content,
            flags=re.DOTALL,
        )

        # Insert new entries
        block_content = (
            f"{AUTOMATED_BLOCK_START}\n\n"
            + "\n".join(new_entries)
            + f"\n\n{AUTOMATED_BLOCK_END}"
        )
        content = re.sub(
            rf"{AUTOMATED_BLOCK_START}\n\n{AUTOMATED_BLOCK_END}",
            block_content,
            content,
        )

        # Write back
        file.seek(0)
        file.write(content)
        file.truncate()


def main():
    template = load_template(TEMPLATE_PATH)
    created_readmes = []

    for dirpath, _, filenames in os.walk(ROOT_DIR):
        image_files = [f for f in filenames if is_valid_image(f)]
        if not image_files:
            continue

        renamed = rename_images(dirpath, image_files)
        create_readme(dirpath, template, renamed)
        created_readmes.append(os.path.basename(dirpath))

    if created_readmes:
        md_list = format_readme_list(created_readmes)
        update_main_readme(MAIN_README, md_list)


if __name__ == "__main__":
    main()
