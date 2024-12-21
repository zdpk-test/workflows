import re
import sys


def _convert_markdown_links(text: str) -> str:
    # [name](url) 형태의 링크를 <url|name> 형식으로 변환
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"<\2|\1>", text)


def _serialize_field(field: str, inline: bool, platform: str) -> dict[str, str]:
    kv = field.split("::")
    if len(kv) > 2:
        print("Each field must has only one `::` separator")
        exit(1)
    k = kv[0] if len(kv) > 1 else ""
    v = kv[1] if len(kv) > 1 else kv[0]

    if platform == "discord":
        return {"name": k.strip(), "value": v.strip(), "inline": inline}
    if platform == "slack":
        v = _convert_markdown_links(v.strip())
        return {"title": k.strip(), "value": v, "short": inline}

    print("Invalid platform - must be either 'discord' or 'slack'")
    sys.exit(1)


def _serialize_slack_field(field: str, short: bool) -> dict[str, str]:
    kv = field.split("::")
    if len(kv) > 2:
        print("Each field must has only one `::` separator")
        exit(1)
    k = kv[0] if len(kv) > 1 else ""
    v = kv[1] if len(kv) > 1 else kv[0]
    v = _convert_markdown_links(v)

    return {"name": k.strip(), "value": v.strip(), "short": short}


def _serialize_line(line: str, platform: str) -> list[dict[str, str]]:
    fields = line.strip().split(",")
    serialized_fields = []
    for field in fields:
        field = field.strip()
        serialized_field = _serialize_field(field, len(fields) > 1, platform)
        serialized_fields.append(serialized_field)

    return serialized_fields


def serialize_fields(text: str, platform: str) -> list[dict[str, str]]:
    serialized_lines = []
    lines = text.strip().splitlines()

    for line in lines:
        line = line.strip()
        fields = _serialize_line(line, platform)
        serialized_lines.extend(fields)

    return serialized_lines
