// const myMixin = {
//   data() {
//     return {
//       current: -1,
//       vals:
//         this.value && this.value.length > 0
//           ? JSON.parse(JSON.stringify(this.value))
//           : [{}],
//     };
//   },
//   created() {
//     if (this.value) {
//       this.current = this.value.map((e) => e.current).indexOf(true);
//     }
//   },

export function date_and_current(value) {
  if (!value.date && !value.current) return;
  let ret = "[";
  if (value.date) ret += value.date;
  if (value.date && value.current) ret += ", ";
  if (value.current) ret += this.$t("current");
  ret += "]";
  return ret;
}

export function mapChoices(choices, formfieldChoices) {
  let ret = "";
  if (choices instanceof Array) {
    ret += choices.map((v) => formfieldChoices[v]).join(", ");
  } else {
    ret += formfieldChoices[choices];
  }
  return ret;
}

export function parseValues(jsonval) {
  let ret = "";
  let choices = this.formfield.choices;

  if (jsonval.value instanceof Array) {
    if (choices) {
      ret += jsonval.value.map((v) => choices[v]).join(", ");
    } else ret += jsonval.value.join(", ");
  } else {
    if (choices) ret += choices[jsonval.value];
    else ret += jsonval.value;
  }
  return ret;
}

export function updateCurrent(i) {
  this.current = i;
  this.updateEntries();
}

export function updateEntries() {
  this.vals = this.vals.map((v, i) => {
    let current = i === this.current ? { current: true } : {};
    delete v.current;
    return { ...v, ...current };
  });
  this.$emit("input", this.filteredVals);
}
export function addEntry() {
  this.current = null;
  this.vals.push({});
  this.updateEntries();
}

export function removeEntry(index) {
  if (this.current === this.vals.length - 1) this.current = null;
  this.vals.splice(index, 1);
  this.updateEntries();
}
