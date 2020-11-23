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
  };
  let draft_status_map = {
    1: "Draft",
    2: "Review",
    3: "Activation",
    4: "Rejected",
    5: "To Delete",
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

    if (fieldx === null) return -1;
    if (fieldy === null) return 1;

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

export function arraysAreEqual(array1, array2) {
  // if the other array1 is a falsy value, return
  if (!array1) return false;

  // compare lengths - can save a lot of time
  if (array2.length != array1.length) return false;

  for (var i = 0, l = array2.length; i < l; i++) {
    // Check if we have nested array1s
    if (array2[i] instanceof Array && array1[i] instanceof Array) {
      // recurse into the nested array1s
      if (!array2[i].equals(array1[i])) return false;
    } else if (array2[i] != array1[i]) {
      // Warning - two different object instances will never be equal: {x:20} != {x:20}
      return false;
    }
  }
  return true;
}
