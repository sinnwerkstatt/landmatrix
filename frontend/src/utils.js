export default function flatten_choices(choices) {
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
