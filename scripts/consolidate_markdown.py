import os
import glob

def consolidate_markdown(input_dir, output_file):
    """
    Consolidate markdown files in a directory into a single file,
    updating headings to have one more '#' character.
    """
    # Get all markdown files in the directory
    md_files = sorted(glob.glob(os.path.join(input_dir, "*.md")))

    with open(output_file, "w") as outfile:
        for md_file in md_files:
            with open(md_file, "r") as infile:
                for line in infile:
                    # If it's a heading, add an extra `#`
                    if line.startswith("#"):
                        outfile.write("#" + line)
                    else:
                        outfile.write(line)
                outfile.write("\n")  # Add a newline between files for separation

# Directory containing markdown files and output file
input_directory = "./docs/tooling/grafana-loki/"
output_markdown = f"{input_directory}/using-centralized-logging.md"

consolidate_markdown(input_directory, output_markdown)
print(f"Markdown files consolidated into {output_markdown}")
