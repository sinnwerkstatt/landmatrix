export const fieldMixin = {
  props: ["formfield", "value", "readonly", "file_not_public"],
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
      return ["col-md-5 col-lg-4"];
    },
    valClasses() {
      return ["col-md-7 col-lg-8"];
    },
  },
};
