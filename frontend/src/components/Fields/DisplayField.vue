<template>
  <div :class="wrapper_classes" v-if="visible">
    <FieldLabel
      v-if="show_label"
      :fieldname="fieldname"
      :label_classes="label_classes"
      :model="model"
    />
    <div :class="value_classes">
      <component
        :is="formfield.class"
        :formfield="formfield"
        v-model="value"
        v-if="custom_is_null(value)"
      />
    </div>
  </div>
</template>

<script>
  import ArrayField from "./Display/ArrayField";
  import BooleanField from "./Display/BooleanField";
  import CharField from "./Display/TextField";
  import DateField from "./Display/DateField";
  import DateTimeField from "./Display/DateField";
  import DecimalField from "./Display/DecimalField";
  import EmailField from "./Display/TextField";
  import FileField from "./Display/FileField";
  import FloatField from "./Display/DecimalField";
  import ForeignKey from "./Display/ForeignKeyField";
  import IntegerField from "./Display/DecimalField";
  import JSONField from "./Display/JSONField";
  import NullBooleanField from "./Display/BooleanField";
  import PointField from "./Display/PointField";
  import TextField from "./Display/TextField";
  import URLField from "./Display/TextField";
  import { mapState } from "vuex";
  import FieldLabel from "./FieldLabel";

  export default {
    name: "DisplayField",
    props: {
      fieldname: { type: String, required: true },
      value: { required: true },
      model: { type: String, default: "deal" },
      show_label: { type: Boolean, default: true },
      label_classes: { type: Array },
      value_classes: { type: Array, default: () => ["val", "col-md-7", "col-lg-8"] },
      wrapper_classes: { type: Array, default: () => ["form-field", "row"] },
      file_not_public: { type: Boolean, default: false },
    },
    components: {
      FieldLabel,
      ArrayField,
      BooleanField,
      CharField,
      DateField,
      DateTimeField,
      DecimalField,
      EmailField,
      FileField,
      FloatField,
      ForeignKey,
      IntegerField,
      JSONField,
      NullBooleanField,
      PointField,
      TextField,
      URLField,
    },
    computed: {
      visible() {
        if (this.formfield.class === "FileField") {
          return !this.file_not_public || this.user.is_authenticated;
        }
        return true;
      },
      formfield() {
        return this.formfields[this.model][this.fieldname];
      },
      ...mapState({
        formfields: (state) => state.formfields,
        user: (state) => state.page.user,
      }),
    },
    methods: {
      custom_is_null(field) {
        return !(
          field === undefined ||
          field === null ||
          field === "" ||
          (Array.isArray(field) && field.length === 0)
        );
      },
    },
  };
</script>

<style lang="scss">
  @import "src/scss/colors";

  .form-field {
    margin-bottom: 0.7em;
    line-height: 1.2;

    .label {
      font-weight: 500;
    }

    .val {
      line-height: 1.2;
      color: $lm_dark;
    }
  }
</style>
