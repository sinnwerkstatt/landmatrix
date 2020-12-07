import { flatten_choices } from "/utils";

export const getFieldValue = function (obj, formFields, fieldName, model = "deal") {
  let formField = formFields[model][fieldName];
  let val = obj[fieldName];

  if (val) {
    let choices = flatten_choices(formField.choices);
    return choices ? choices[val] : val;
  }
  return "n/a";
};
