export function flatten_choices(choices) {
  if (choices) {
    let newchoices = {};
    for (let [key, value] of Object.entries(choices)) {
      if (typeof value == "string") {
        newchoices[key] = value;
      } else {
        for (let [key, v] of Object.entries(value)) {
          newchoices[key] = v;
        }
      }
    }
    return newchoices;
  }
}

export function derive_status(status, draft_status) {
  let status_map = {
    1: "Draft",
    2: "Live",
    3: "Updated",
    4: "Deleted",
    5: "Rejected",
    6: "To Delete?",
  };
  let draft_status_map = {
    1: "Draft",
    2: "Review",
    3: "Activation",
  };
  let st = status_map[status];
  if (draft_status) {
    return `${st} + ${draft_status_map[draft_status]}`;
  }
  return st;
}

export function sortAnything(list, sortField, sortAscending) {
  function sortFunction(a, b) {
    let fieldx = sortAscending ? a[sortField] : b[sortField];
    let fieldy = sortAscending ? b[sortField] : a[sortField];

    if (fieldy === null) return -1;
    if (fieldx === null) return 1;

    switch (typeof fieldx) {
      case "number":
        return fieldy - fieldx;
      case "string":
        return fieldx.localeCompare(fieldy);
      case "object": {
        if (Array.isArray(fieldx)) {
          return fieldx.length - fieldy.length;
        }
        for (let key of ["name", "id"]) {
          if (key in fieldx && key in fieldy) return fieldy[key] - fieldx[key];
        }
        return Object.keys(fieldx).length - Object.keys(fieldy).length;
      }
    }
    return fieldy - fieldx;
  }
  return list.sort(sortFunction);
}
