<template>
  <div>
    <component
      :is="formfield.class"
      :formfield="formfield"
      :readonly="!!readonly"
      v-model="value"
      :file_not_public="file_not_public"
      v-if="!readonly || custom_is_null(value)"
      :narrow="!!narrow"
    />
  </div>
</template>

<script>
  import ArrayField from "/components/Fields/ArrayField";
  import BooleanField from "/components/Fields/BooleanField";
  import CharField from "/components/Fields/TextField";
  import DateField from "/components/Fields/TextField";
  import DecimalField from "/components/Fields/DecimalField";
  import EmailField from "/components/Fields/TextField";
  import FileField from "/components/Fields/FileField";
  import FloatField from "/components/Fields/DecimalField";
  import ForeignKey from "/components/Fields/ForeignKeyField";
  import IntegerField from "/components/Fields/DecimalField";
  import JSONField from "/components/Fields/JSONField";
  import NullBooleanField from "/components/Fields/BooleanField";
  import PointField from "/components/Fields/PointField";
  import TextField from "/components/Fields/TextField";
  import URLField from "/components/Fields/TextField";
  import { mapState } from "vuex";
  export default {
    name: "Field",
    props: ["fieldname", "model", "value", "readonly", "file_not_public", "narrow"],
    components: {
      ArrayField,
      BooleanField,
      CharField,
      DateField,
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
      formfield() {
        switch (this.model) {
          case "contract":
            return this.formfields.contract[this.fieldname];
          case "datasource":
            return this.formfields.datasource[this.fieldname];
          case "location":
            return this.formfields.location[this.fieldname];
          case "investor":
            return this.formfields.investor[this.fieldname];
          case "involvement":
            return this.formfields.involvement[this.fieldname];
          default:
            return this.formfields.deal[this.fieldname];
        }
      },
      ...mapState({
        formfields: (state) => state.formfields,
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
  @import "../../scss/colors";

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
