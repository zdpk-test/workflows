def _serialize_field(field: str, inline: bool) -> dict[str, str]:
    kv = field.split("::")
    if len(kv) > 2:
        print("Each field must has only one `::` separator")
        exit(1)
    k = kv[0] if len(kv) > 1 else ""
    v = kv[1] if len(kv) > 1 else kv[0]

    ret = {"name": k.strip(), "value": v.strip(), "inline": inline}
    return ret


def _serialize_line(line: str):
    fields = line.strip().split(",")
    json_fields = []
    for field in fields:
        field = field.strip()
        handled_field = _serialize_field(field, len(fields) > 1)
        json_fields.append(handled_field)

    # json_fields = json.dumps(json_fields, indent=4)
    return json_fields


def serialize(text: str):
    handled_lines = []
    lines = text.strip().splitlines()

    for line in lines:
        line = line.strip()
        fields = _serialize_line(line)
        handled_lines.extend(fields)

    return handled_lines
