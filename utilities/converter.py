from nbconvert import NotebookExporter
import nbformat

# Load the notebook
notebook_path = "docs/modules/summarize.ipynb"
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook_content = f.read()

notebook = nbformat.reads(notebook_content, as_version=4)

# Define the configuration for the exporter
exporter = NotebookExporter()
exporter.exclude_input_tags = {'remove_convert'}
exporter.exclude_output_tags = {'remove_output'}

# Export the notebook to Markdown
output, _ = exporter.from_notebook_node(notebook)

# Save the Markdown output to a file
markdown_output_path = "summarize.md"
with open(markdown_output_path, 'w', encoding='utf-8') as f:
    f.write(output)
