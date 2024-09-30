import json, pymupdf, re
from itertools import islice

HEADER_REGEX = "(?:\d\.)+[a-zA-Z]"
PDF_PATH = '2024_Altered_TCG_Comprehensive_Rules_1.0_EN.pdf'
OUTPUT_PATH = 'output.json'

START_PAGE = 7
END_PAGE = 72

def add_current_entry_to_result(result, current_header, current_text):
    if len(current_text) > 0 and len(current_header) > 0:
        result[current_header] = current_text

doc = pymupdf.open(PDF_PATH)

text = ""
for page in islice(doc, START_PAGE, END_PAGE):
    text += page.get_text()
doc.close()

result = {}
current_header = ""
current_text = ""
for line in text.splitlines():
    if re.match(HEADER_REGEX, line):
        add_current_entry_to_result(result, current_header, current_text)
        current_header = line
        current_text = ""
    else:
        if len(current_header) > 0:
            if line.endswith("-"):
                line = line[:-1]
            current_text += line
            
add_current_entry_to_result(result, current_header, current_text)

with open(OUTPUT_PATH, 'w') as f:
    json.dump(result, f, indent=4)
