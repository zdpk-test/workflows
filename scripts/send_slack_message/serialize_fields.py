def handle_field(field: str, inline: bool) -> dict:
    kv = field.split("::")
    if len(kv) > 2:
        print("Each field must have only one `::` separator")
        exit(1)
    k = kv[0] if len(kv) > 1 else ""
    v = kv[1] if len(kv) > 1 else kv[0]

    ret = {"title": k.strip(), "value": v.strip(), "short": inline}
    return ret


def handle_line(line: str):
    fields = line.strip().split(",")
    json_fields = []
    for field in fields:
        field = field.strip()
        handled_field = handle_field(field, len(fields) > 1)
        json_fields.append(handled_field)

    return json_fields


def serialize_fields(text: str):
    handled_lines = []
    lines = text.strip().splitlines()

    for line in lines:
        line = line.strip()
        fields = handle_line(line)
        handled_lines.extend(fields)

    return handled_lines
