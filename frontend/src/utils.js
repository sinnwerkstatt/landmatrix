function flatten_choices(choices) {
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

function derive_status(status, draft_status) {
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

function sortAnything(list, sortField, sortAscending) {
  const objCompareAttribs = ['name', 'id'];
  function sortFunction(a, b) {
    let fieldx = sortAscending ? a[sortField] : b[sortField];
    let fieldy = sortAscending ? b[sortField] : a[sortField];

    let field_type = typeof fieldx;
    if (fieldy === null) return true;
    if (fieldx === null) return false;
    if (field_type === typeof "") {
      return fieldx.localeCompare(fieldy);
    } else if (Array.isArray(fieldx)) {
      return fieldx.length < fieldy.length;
    } else if (field_type === "object") {
      for (let key of objCompareAttribs) {
        if (key in fieldx && key in fieldy) {
          return fieldy[key] < fieldx[key];
        }
      }
      return Object.keys(fieldx).length < Object.keys(fieldy).length;
    }
    return fieldy < fieldx;
  }
  return list.sort(sortFunction);
}

export { flatten_choices, derive_status, sortAnything };
