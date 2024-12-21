import json


def handle_field(field: str, inline: bool) -> dict[str, str]:
    kv = field.split("::")
    if len(kv) > 2:
        print("Each field must has only one `::` separator")
        exit(1)
    k = kv[0] if len(kv) > 1 else ""
    v = kv[1] if len(kv) > 1 else kv[0]

    ret = {"name": k.strip(), "value": v.strip(), "inline": inline}
    return ret


# handle_field("field1:: abc")
# handle_field("field1")


def handle_line(line: str):
    fields = line.strip().split(",")
    json_fields = []
    for field in fields:
        field = field.strip()
        handled_field = handle_field(field, len(fields) > 1)
        json_fields.append(handled_field)

    # json_fields = json.dumps(json_fields, indent=4)
    return json_fields


def serialize_fields(text: str):
    handled_lines = []
    lines = text.strip().splitlines()

    for line in lines:
        line = line.strip()
        fields = handle_line(line)
        handled_lines.extend(fields)

    # return json.dumps(handled_lines, indent=4)
    return handled_lines


# def split_fields(line: str):
#     fields = []
#     for field in line.strip().split(','):
#         field = field.strip()
#         print(field)
#         fields.append(field)
#     return fields

# def handle_lines(text: str):
#     handled_lines = []
#     lines = text.strip().splitlines()
#     # print(lines)

#     for line in lines:
#         line = line.strip()
#         fields = split_fields(line)
#         handled_lines.append(fields)

#     print(handled_lines)


# handle_lines("""
#         field1: abc, field2: cde
#         field3: sdf
#         field4: zzz
#         field5: qwe, field6: asd, field7: ef
#               """)
