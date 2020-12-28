<template>
  <div>
    <component
      :is="formfield.class"
      v-if="!readonly || custom_is_null(value)"
      v-model="value"
      :formfield="formfield"
      :readonly="!!readonly"
      :file_not_public="file_not_public"
    />
  </div>
</template>

<script>
  import ArrayField from "components/Fields/ArrayField";
  import BooleanField from "components/Fields/BooleanField";
  import NullBooleanField from "components/Fields/BooleanField";
  import CharField from "components/Fields/TextField";
  import DateField from "components/Fields/TextField";
  import EmailField from "components/Fields/TextField";
  import TextField from "components/Fields/TextField";
  import URLField from "components/Fields/TextField";
  import DecimalField from "components/Fields/DecimalField";
  import FloatField from "components/Fields/DecimalField";
  import IntegerField from "components/Fields/DecimalField";
  import FileField from "components/Fields/FileField";
  import ForeignKey from "components/Fields/ForeignKeyField";
  import JSONField from "components/Fields/JSONField";
  import PointField from "components/Fields/PointField";
  import { mapState } from "vuex";

  export default {
    name: "Field",
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
    props: ["fieldname", "model", "value", "readonly", "file_not_public"],
    computed: {
      formfield() {
        return this.formfields[this.model][this.fieldname];
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
  @import "../../../scss/colors";

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
