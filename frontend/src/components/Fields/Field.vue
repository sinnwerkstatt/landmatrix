<template>
  <component
    :is="formfield.class"
    :formfield="formfield"
    :readonly="!!readonly"
    v-model="value"
    :file_not_public="file_not_public"
    v-if="!readonly || custom_is_null(value)"
  />
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
  export default {
    name: "Field",
    props: ["formfield", "value", "readonly", "file_not_public"],
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
