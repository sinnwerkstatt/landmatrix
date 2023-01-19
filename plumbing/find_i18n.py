import re
import subprocess
from glob import glob

root_dir = "../newfront/src/"


def find_files():
    files = glob("**/*.svelte", recursive=True, root_dir=root_dir)
    files += glob("**/*.ts", recursive=True, root_dir=root_dir)

    return files


re_i18n_strings = re.compile(r"\$_\(\s*?\"(.*?)\"(?:,\s*?\{.*?\})?,?\s*?\)")


def process():
    results = set()
    for file in find_files():
        with open(root_dir + file, "r") as f:
            cntnt = f.read().replace("\n", "")
        if "$_(" in cntnt:
            # print(file)
            # for res in re_i18n_strings.findall(cntnt):
            #     print(res)
            results |= set(re_i18n_strings.findall(cntnt))

    with open("../config/frontend_i18n_strings.py", "w") as f:
        f.write("from django.utils.translation import gettext as _\n\n")
        for string in sorted(results, key=lambda a: a.lower()):
            f.write(f'_("{string}")\n')

    subprocess.run(["black", "../config/frontend_i18n_strings.py"])
    print("success. now check `frontend_i18n_strings.py` to see if it's fine")


process()
