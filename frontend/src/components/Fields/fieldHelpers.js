import { flatten_choices } from "/utils";
import dayjs from "dayjs";

export const getFieldValue = function (obj, formFields, fieldName, model = "deal") {
  let formField = formFields[model][fieldName];
  let val = obj[fieldName];
  return parseFormFieldValue(formField, val);
};

export const parseFormFieldValue = function (formField, val) {
  if (val) {
    let choices = flatten_choices(formField.choices);
    if (choices) return choices[val];
    else if (["DateField", "DateTimeField"].includes(formField.class))
      return dayjs(val).format("YYYY-MM-DD");
    else return val;
  } else {
    return "n/a";
  }
};
