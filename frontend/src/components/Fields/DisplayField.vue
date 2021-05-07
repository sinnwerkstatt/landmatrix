<template>
  <div v-if="_visible" :class="wrapperClasses">
    <FieldLabel
      v-if="showLabel"
      :fieldname="fieldname"
      :label-classes="labelClasses"
      :model="model"
    />
    <div :class="valueClasses">
      <component
        :is="formfield.class"
        v-if="!custom_is_null(value)"
        :value="value"
        :formfield="formfield"
        :model="model"
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
  import AutoField from "./Display/AutoField";
  import DecimalField from "./Display/DecimalField";
  import EmailField from "./Display/TextField";
  import FileField from "./Display/FileField";
  import FloatField from "./Display/DecimalField";
  import ForeignKey from "./Display/ForeignKeyField";
  import ManyToManyField from "./Display/ManyToManyField";
  import LengthField from "./Display/LengthField";
  import IntegerField from "./Display/DecimalField";
  import JSONField from "./Display/JSONField.vue";
  import JSONActorsField from "./Display/JSONActorsField";
  import JSONDateAreaField from "./Display/JSONDateAreaField";
  import JSONDateChoiceField from "./Display/JSONDateChoiceField";
  import JSONDateAreaChoicesField from "./Display/JSONDateAreaChoicesField";
  import JSONExportsField from "./Display/JSONExportsField";
  import JSONJobsField from "./Display/JSONJobsField";
  import JSONLeaseField from "./Display/JSONLeaseField";
  import NullBooleanField from "./Display/BooleanField";
  import PointField from "./Display/PointField";
  import TextField from "./Display/TextField";
  import URLField from "./Display/TextField";
  import OCIDField from "./Display/OCIDField";
  import FieldLabel from "./FieldLabel";
  import LocationGoogleField from "./Display/TextField";

  export default {
    name: "DisplayField",
    components: {
      ArrayField,
      AutoField,
      BooleanField,
      CharField,
      DateField,
      DateTimeField,
      DecimalField,
      EmailField,
      FieldLabel,
      FileField,
      FloatField,
      ForeignKey,
      IntegerField,
      JSONActorsField,
      JSONDateAreaChoicesField,
      JSONDateAreaField,
      JSONDateChoiceField,
      JSONExportsField,
      JSONField,
      JSONJobsField,
      JSONLeaseField,
      LengthField,
      LocationGoogleField,
      ManyToManyField,
      NullBooleanField,
      PointField,
      TextField,
      URLField,
      OCIDField,
    },
    props: {
      fieldname: { type: String, required: true },
      // eslint-disable-next-line vue/require-prop-types
      value: { required: true },
      model: { type: String, default: "deal" },
      showLabel: { type: Boolean, default: true },
      wrapperClasses: {
        type: Array,
        default: () => ["display-field-wrapper", "form-field", "row"],
      },
      labelClasses: {
        type: Array,
        default: () => ["display-field-label", "col-md-5", "col-lg-4"],
      },
      valueClasses: {
        type: Array,
        default: () => ["display-field-value", "col-md-7", "col-lg-8"],
      },
      fileNotPublic: { type: Boolean, default: false },
      visible: { type: Boolean, default: true },
    },
    computed: {
      _visible() {
        if (!this.visible) return false;
        if (this.formfield.class === "FileField") {
          return !this.fileNotPublic || this.$store.getters.userAuthenticated;
        }
        return true;
      },
      formfield() {
        return {
          name: this.fieldname,
          ...this.$store.state.formfields[this.model][this.fieldname],
        };
      },
    },
    methods: {
      custom_is_null(field) {
        return (
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

  .display-field-wrapper {
    margin-bottom: 0.7em;
    line-height: 1.2;
  }
  .display-field-label {
    font-weight: 500;
  }
  .display-field-value {
    line-height: 1.2;
    color: $lm_dark;
  }
</style>
