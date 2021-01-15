import { flatten_choices } from "utils";

const myMixin = {
  props: {
    formfield: { type: Object, required: true },
    value: { type: [Array, Object], required: true },
    model: { type: String, required: true },
  },
  methods: {
    date_and_current(value) {
      if (!value.date && !value.current) return;
      let ret = "[";
      if (value.date) ret += value.date;
      if (value.date && value.current) ret += ", ";
      if (value.current) ret += this.$t("current");
      ret += "]";
      return ret;
    },
    mapChoices(choices) {
      let choices_i18n = flatten_choices(this.formfield.choices);
      let ret = "";
      if (choices instanceof Array) {
        ret += choices.map((v) => choices_i18n[v]).join(", ");
      } else {
        ret += choices_i18n[choices];
      }
      return ret;
    },
    parseValues: function (jsonval) {
      let ret = "";
      let choices = flatten_choices(this.formfield.choices);

      if (jsonval.value instanceof Array) {
        if (choices) {
          ret += jsonval.value.map((v) => choices[v]).join(", ");
        } else ret += jsonval.value.join(", ");
      } else {
        if (choices) ret += choices[jsonval.value];
        else ret += jsonval.value;
      }
      return ret;
    },
  },
};
export default myMixin;
