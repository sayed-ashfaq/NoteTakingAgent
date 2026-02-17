# load the data from the markdown file 
# segregate the data into Headings, subheadings and text
## we can do this by reading each line and based on prefix we can assign it to a category.

# for example:
# # Heading 1
# ## Heading 2
# ``` some code` -> Code bloc
# - or * for bullet point
# 1. for numbered list
# > for quote


# =========================
# HELPER BLOCKS
# =========================

def rich(text):
    return [{"type": "text", "text": {"content": text}}]


def block(type_, text):
    return {
        "object": "block",
        "type": type_,
        type_: {"rich_text": rich(text)}
    }


def code_block(code, language="plain text"):
    return {
        "object": "block",
        "type": "code",
        "code": {
            "language": language,
            "rich_text": rich(code)
        }
    }

def divider():
    return {
        "object": "block",
        "type": "divider",
        "divider": {}
    }


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


import re


def parse_lines(lines):
    children = []
    in_code = False
    code_lines = []
    code_lang = "plain text"

    for raw in lines:
        line = raw.rstrip()

        # =====================
        # CODE BLOCK TOGGLE
        # =====================
        if line.startswith("```"):
            if not in_code:
                in_code = True
                code_lang = line.replace("```", "").strip() or "plain text"
                code_lines = []
            else:
                children.append(code_block("\n".join(code_lines), code_lang))
                in_code = False
            continue

        if in_code:
            code_lines.append(line)
            continue

        # =====================
        # HEADINGS
        # =====================
        if line.startswith("### "):
            children.append(block("heading_3", line[4:]))
            continue

        if line.startswith("## "):
            children.append(block("heading_2", line[3:]))
            continue

        if line.startswith("# "):
            children.append(block("heading_1", line[2:]))
            continue

        # =====================
        # BULLET LIST
        # =====================
        if line.startswith("- ") or line.startswith("*"):
            children.append(block("bulleted_list_item", line[2:]))
            continue

        # =====================
        # NUMBERED LIST
        # =====================
        if re.match(r"\d+\.\s", line):
            text = re.sub(r"^\d+\.\s", "", line)
            children.append(block("numbered_list_item", text))
            continue

        # =====================
        # QUOTE
        # =====================
        if line.startswith("> "):
            children.append(block("quote", line[2:]))
            continue

        if line.strip() == "---":
            children.append(divider())
            continue

        # =====================
        # PARAGRAPH
        # =====================
        if line.strip():
            children.append(block("paragraph", line.strip()))

    return children


def markdown_to_notion_blocks(path=None, content=None):
    if content:
        if isinstance(content, str):
            lines = content.splitlines()
        else:
            lines = content
    elif path:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    else:
        raise ValueError("Either path or content must be provided")
        
    return parse_lines(lines)



