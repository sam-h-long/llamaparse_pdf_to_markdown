import os
from pathlib import Path
from typing import List
from llama_parse import LlamaParse


def llama_parse_pdf_to_markdown(files: List[Path]):
    # Assert that the files are PDFs
    if not all(file.suffix == '.pdf' for file in files):
        raise ValueError('All files must be PDFs')

    # Check which markdown (.md) files already exist and which do not
    files_exist, files_not_exist = [], []
    for file_pdf in files:
        file_md = file_pdf.with_suffix('.md')
        if file_md.exists():
            files_exist.append(str(file_md))
        else:
            files_not_exist.append(str(file_pdf))

    print(f'These files have already been LlamaParsed: {files_exist}')

    if files_not_exist:
        # Configure LlamaParse
        parser = LlamaParse(api_key=os.environ['LLAMAPARSE_API_KEY'],  # can also be set in your env as LLAMA_CLOUD_API_KEY
                            result_type="markdown",  # "markdown" and "text" are available
                            split_by_page=False,
                            verbose=True)
        # Run LlamaParse
        documents_md = parser.load_data(file_path=files_not_exist)

        if len(documents_md) != len(files_not_exist):
            raise ValueError(f"Number of documents ({len(documents_md)}) does not match number of files ({len(files_not_exist)}). "
                             f"LlamaParse API is constantly changing so check version compatibility.")

        # Save documents
        for i, doc_md in enumerate(documents_md):
            # Save as markdown (.md)
            with open(Path(files_not_exist[i]).with_suffix('.md'), 'w') as f:
                f.write(doc_md.text)

        return documents_md

    return None


if __name__ == '__main__':
    # Add PDF files to extract
    files_pdf = ["NVIDIA-2023-Annual-Report.pdf"]

    # Create filepaths
    filepaths_pdf = [Path(Path(__file__).parent, 'files', f) for f in files_pdf]

    # Extract PDF files and convert to markdown using LlamaParse API
    llama_parse_pdf_to_markdown(files=filepaths_pdf)

    print("DONE")