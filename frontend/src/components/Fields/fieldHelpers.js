import { flatten_choices } from "../../utils";
import dayjs from "dayjs";

const MODELS = ["contract", "datasource", "location", "investor", "involvement"];

export const getFormField = function (formFields, fieldName, model) {
  if (model && MODELS.includes(model)) {
    return formFields[model][fieldName];
  } else {
    return formFields.deal[fieldName];
  }
};

export const getFieldLabel = function (formFields, fieldName, model) {
  let formField = getFormField(formFields, fieldName, model);
  return formField.label;
};

export const getFieldValue = function (obj, formFields, fieldName, model) {
  let formField = getFormField(formFields, fieldName, model);
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
