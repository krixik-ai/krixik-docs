from nbconvert import MarkdownExporter, TagRemovePreprocessor
import nbformat


def convert_notebook_to_md(notebook_path: str) -> None:
    # Load the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = f.read()

    notebook = nbformat.reads(notebook_content, as_version=4)

    # Define the configuration for the exporter
    exporter = MarkdownExporter()
    exporter.remove = {'remove_cell'}
    exporter.exclude_output_tags = {'remove_output'}

    # Export the notebook to Markdown
    output, _ = exporter.from_filename(notebook)

    # Save the Markdown output to a file
    markdown_output_path = notebook_path.replace(".ipynb", ".md")
    with open(markdown_output_path, 'w', encoding='utf-8') as f:
        f.write(output)
