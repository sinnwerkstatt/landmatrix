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
  }
  let st = status_map[status]
  if (draft_status) {
    return `${st} + ${draft_status_map[draft_status]}`;
  }
  return st;
}

export {flatten_choices, derive_status};
