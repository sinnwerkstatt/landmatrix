interface Choi {
  [key: string | number]: string | { [key: string | number]: string };
}
export function flatten_choices(
  choices: Choi,
  append_group = false
): { [key: string]: string } {
  if (choices) {
    const newchoices: { [key: string]: string } = {};
    for (const [key, value] of Object.entries(choices)) {
      if (typeof value === "string") {
        newchoices[key] = value;
      } else {
        for (const [k, v] of Object.entries(value)) {
          newchoices[k] = append_group ? `${key} (${v})` : v;
        }
      }
    }
    return newchoices;
  }
  return {};
}

export function sortAnything<T extends { [key: string | number]: any }>(
  list: Array<T>,
  sortField: string,
  sortAscending: boolean
): Array<T> {
  function sortFunction(a: T, b: T) {
    let fieldx;
    let fieldy;
    // NOTE: Nasty hack just to accomodate management.vue
    if (sortField.startsWith("current_draft.")) {
      const field = sortField.replace("current_draft.", "");
      fieldx = sortAscending ? a.current_draft?.[field] : b.current_draft?.[field];
      fieldy = sortAscending ? b.current_draft?.[field] : a.current_draft?.[field];
    } else {
      fieldx = sortAscending ? a[sortField] : b[sortField];
      fieldy = sortAscending ? b[sortField] : a[sortField];
    }

    if (fieldx === null || fieldx === undefined) return -1;
    if (fieldy === null || fieldy === undefined) return 1;

    switch (typeof fieldx) {
      case "number":
        return fieldy - fieldx;
      case "string":
        return fieldx.localeCompare(fieldy);
      case "object": {
        if (Array.isArray(fieldx)) return fieldx.length - fieldy.length;

        if ("username" in fieldx && "username" in fieldy)
          return fieldy.username
            .toLocaleLowerCase()
            .localeCompare(fieldx.username.toLocaleLowerCase());

        if ("name" in fieldx && "name" in fieldy)
          return fieldy.name.localeCompare(fieldx.name);

        if ("id" in fieldx && "id" in fieldy) return fieldy.id - fieldx.id;

        return Object.keys(fieldx).length - Object.keys(fieldy).length;
      }
    }
    return fieldy - fieldx;
  }
  return list.sort(sortFunction);
}

export function removeEmptyEntries<T extends { [key: string]: string }>(
  objectlist: T[]
): T[] {
  // this function throws out any entries that have only an ID field and otherwise empty values.
  return objectlist.filter((con) => {
    return Object.entries(con)
      .filter(([k, v]) => (k === "id" ? false : !!v))
      .some((x) => !!x);
  });
}
