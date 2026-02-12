# load the data from the markdown file 
# segregate the data into Headings, subheadings and text
## we can do this by reading each line and based on prefix we can assign it to a category.

# for example:
## Heading 1, content
### Subheading 1, content
### Subheading 2, content
## Heading 2, content

def text_block(type, text):
    return {
        "object":"block",
        "type":type,
        type:{
            "rich_text":[{"type":"text","text":{"content":text}}]
        }
    }



# =========================
# PARSING
# =========================
def parse_data(path):
    children = []
    in_code_block = False
    code_buffer = []

    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n")

            # =========================
            # CODE BLOCK START / END
            # =========================
            if line.startswith("```"):
                if not in_code_block:
                    in_code_block = True
                    code_buffer = []
                else:
                    # closing ```
                    children.append({
                        "object": "block",
                        "type": "code",
                        "code": {
                            "language": "plain text",
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": "\n".join(code_buffer)
                                    }
                                }
                            ]
                        }
                    })
                    in_code_block = False
                continue

            if in_code_block:
                code_buffer.append(line)
                continue

            # =========================
            # HEADINGS (ORDER MATTERS)
            # =========================
            if line.startswith("### "):
                children.append(text_block("heading_3", line[4:]))

            elif line.startswith("## "):
                children.append(text_block("heading_2", line[3:]))

            elif line.startswith("# "):
                children.append(text_block("heading_1", line[2:]))

            # =========================
            # NORMAL TEXT
            # =========================
            elif line.strip():
                children.append(text_block("paragraph", line.strip()))

    return children


if __name__ == "__main__":
    children = parse_data("data//test_data.md")
    print(children)
