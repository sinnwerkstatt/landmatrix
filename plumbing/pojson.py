import sys

import polib
import simplejson


def po2dict(po):
    # result = {"": po.metadata.copy()} # for metadata?
    result = {}

    for entry in po:
        if entry.obsolete:
            continue

        if entry.msgctxt:
            key = "{0}\x04{1}".format(entry.msgctxt, entry.msgid)
        else:
            key = entry.msgid

        if entry.msgstr:
            result[key] = entry.msgstr
        elif entry.msgstr_plural:
            plural = [entry.msgid_plural]
            result[key] = plural
            ordered_plural = sorted(entry.msgstr_plural.items())
            for order, msgstr in ordered_plural:
                plural.append(msgstr)
    return result


data = po2dict(polib.pofile(sys.argv[1]))
# result = simplejson.dumps(data, sort_keys=True, indent=2, ensure_ascii=False)
resjson = simplejson.dumps(data, indent=2, ensure_ascii=False)
print(resjson)
