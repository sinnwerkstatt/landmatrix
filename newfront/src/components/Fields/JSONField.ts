import { flatten_choices } from "$utils";

const myMixin = {
  props: {
    formfield: { type: Object, required: true },
    value: { type: [Array, Object], required: false, default: null },
    model: { type: String, required: true },
  },
  data() {
    return {
      current: -1,
      vals:
        this.value && this.value.length > 0
          ? JSON.parse(JSON.stringify(this.value))
          : [{}],
    };
  },
  created() {
    if (this.value) {
      this.current = this.value.map((e) => e.current).indexOf(true);
    }
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
    updateCurrent(i) {
      this.current = i;
      this.updateEntries();
    },
    updateEntries() {
      this.vals = this.vals.map((v, i) => {
        let current = i === this.current ? { current: true } : {};
        delete v.current;
        return { ...v, ...current };
      });
      this.$emit("input", this.filteredVals);
    },
    addEntry() {
      this.current = null;
      this.vals.push({});
      this.updateEntries();
    },
    removeEntry(index) {
      if (this.current === this.vals.length - 1) this.current = null;
      this.vals.splice(index, 1);
      this.updateEntries();
    },
  },
};
export default myMixin;
