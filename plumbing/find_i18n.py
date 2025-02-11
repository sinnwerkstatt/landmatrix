import re
import subprocess
from glob import glob

root_dir = "../frontend/src/"


def find_files():
    files = glob("**/*.svelte", recursive=True, root_dir=root_dir)
    files += glob("**/*.ts", recursive=True, root_dir=root_dir)

    return files


re_i18n_strings = re.compile(r"\$_\(\s*?\"(.*?)\"(?:,\s*?.*?)?,?\s*?\)")


def process():
    results = set()
    for file in find_files():
        with open(root_dir + file) as f:
            cntnt = f.read().replace("\n", "")
        if "$_(" in cntnt:
            # print(file)
            # for res in re_i18n_strings.findall(cntnt):
            #     if "i18nValues" in res:
            #         print(res)
            results |= set(re_i18n_strings.findall(cntnt))

    with open("../config/frontend_i18n_strings.py", "w") as f:
        f.write("from django.utils.translation import gettext as _\n\n")
        for string in sorted(results, key=lambda a: (a.lower(), a.swapcase())):
            f.write(f'_("{string}")\n')

    subprocess.run(["ruff", "format", "../config/frontend_i18n_strings.py"])  # noqa: S603, S607
    print("success. now check `frontend_i18n_strings.py` to see if it's fine")


process()
