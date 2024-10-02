import os
from pypdf import PdfReader
from pathlib import Path


file_paths = [
    'C:\H5SH\other\projects\ML_projects\sql_bot\\assests\\cmsform.pdf'
]

output_dir = 'C:\H5SH\other\projects\ML_projects\sql_bot\\cms'

for file_path in file_paths:
    # page = next(iter())
    name = os.path.splitext(os.path.basename(file_path))[0]
    reader = PdfReader(file_path)
    print(len(reader.pages))
    page = reader.pages[0] 
    text = page.extract_text()

    cms_path = Path('cms')
    if not cms_path.exists():
        Path.mkdir(cms_path)
    
    with open(cms_path / f'{name}.txt', 'w') as fp:
        fp.write(text)
