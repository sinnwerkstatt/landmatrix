import json


def nasty_i18n_frontend_hack_for_english(infile, outfile):

    with open(infile) as inf:
        input_msgs = json.load(inf)
    output_msgs = {}
    for key in input_msgs.keys():
        if "{" in key:
            output_msgs[key] = key

    with open(outfile, "w") as outp:
        json.dump(output_msgs, outp, indent=2)


if __name__ == "__main__":
    nasty_i18n_frontend_hack_for_english(
        "frontend/src/i18n_messages.es.json", "frontend/src/i18n_messages.en.json"
    )
