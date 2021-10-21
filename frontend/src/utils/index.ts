interface Choi {
  [key: string | number]: string | { [key: string | number]: string };
}
export function flatten_choices(choices: Choi, append_group = false): Choi {
  if (choices) {
    const newchoices: Choi = {};
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
    const fieldx = sortAscending ? a[sortField] : b[sortField];
    const fieldy = sortAscending ? b[sortField] : a[sortField];

    if (fieldx === null) return -1;
    if (fieldy === null) return 1;

    switch (typeof fieldx) {
      case "number":
        return fieldy - fieldx;
      case "string":
        return fieldx.localeCompare(fieldy);
      case "object": {
        if (Array.isArray(fieldx)) return fieldx.length - fieldy.length;

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
