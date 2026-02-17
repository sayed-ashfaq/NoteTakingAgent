
import re

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

def parse_lines(lines):
    children = []
    in_code = False
    code_lines = []
    code_lang = "plain text"

    for raw in lines:
        line = raw.rstrip()

        # CODE BLOCK TOGGLE
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

        # HEADINGS
        if line.startswith("### "):
            children.append(block("heading_3", line[4:]))
            continue
        if line.startswith("## "):
            children.append(block("heading_2", line[3:]))
            continue
        if line.startswith("# "):
            children.append(block("heading_1", line[2:]))
            continue

        # BULLET LIST
        if line.startswith("- ") or line.startswith("*"):
            children.append(block("bulleted_list_item", line[2:]))
            continue
            
        # CHECKLIST (New for Tasks)
        if line.startswith("- [ ] "):
            children.append({
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": rich(line[6:]),
                    "checked": False
                }
            })
            continue
        if line.startswith("- [x] "):
            children.append({
                 "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": rich(line[6:]),
                    "checked": True
                }
            })
            continue

        # NUMBERED LIST
        if re.match(r"\d+\.\s", line):
            text = re.sub(r"^\d+\.\s", "", line)
            children.append(block("numbered_list_item", text))
            continue

        # QUOTE
        if line.startswith("> "):
            children.append(block("quote", line[2:]))
            continue

        if line.strip() == "---":
            children.append(divider())
            continue

        # PARAGRAPH
        if line.strip():
            children.append(block("paragraph", line.strip()))

    return children

def markdown_to_notion_blocks(content):
    if isinstance(content, str):
        lines = content.splitlines()
    else:
        lines = content
    return parse_lines(lines)
