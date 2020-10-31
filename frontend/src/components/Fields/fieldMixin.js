export const fieldMixin = {
  props: ["formfield", "value", "readonly", "file_not_public", "narrow"],
  data() {
    return {
      val: this.value,
    };
  },
  methods: {
    emitVal() {
      this.$emit("input", this.val);
    },
  },
  computed: {
    labelClasses() {
      if (this.narrow) {
        return ["col-md-6"];
      } else {
        return ["col-md-5 col-lg-4"];
      }
    },
    valClasses() {
      if (this.narrow) {
        return ["col-md-6"];
      } else {
        return ["col-md-7 col-lg-8"];
      }
    },
  },
};
