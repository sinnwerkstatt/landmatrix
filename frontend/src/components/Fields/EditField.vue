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
        v-model="_value"
        :formfield="formfield"
        :model="model"
      />
    </div>
  </div>
</template>

<script>
  import JSONActorsField from "./Edit/JSONActorsField";
  import JSONDateAreaChoicesField from "./Edit/JSONDateAreaChoicesField";
  import JSONDateAreaField from "./Edit/JSONDateAreaField";
  import JSONDateChoiceField from "./Edit/JSONDateChoiceField";
  import JSONExportsField from "./Edit/JSONExportsField";
  import JSONJobsField from "./Edit/JSONJobsField";
  import JSONLeaseField from "./Edit/JSONLeaseField";

  // import AutoField from "./Display/AutoField";
  import ArrayField from "./Edit/ArrayField";

  import BooleanField from "./Edit/BooleanField";
  import NullBooleanField from "./Edit/BooleanField";

  import DateField from "./Edit/DateField";
  // import DateTimeField from "./Display/DateField";

  import DecimalField from "./Edit/DecimalField";
  import FloatField from "./Edit/DecimalField";
  import IntegerField from "./Edit/DecimalField";

  import FileField from "./Edit/FileField";
  import ForeignKey from "./Edit/ForeignKeyField";

  import JSONField from "./Edit/JSONField.vue";

  import CharField from "./Edit/TextField";
  import EmailField from "./Edit/TextField";
  import TextField from "./Edit/TextField";
  import URLField from "./Edit/TextField";
  import OCIDField from "./Edit/TextField";

  import ManyToManyField from "./Display/ManyToManyField";
  import LengthField from "./Display/LengthField";
  import PointField from "./Display/PointField";

  import FieldLabel from "./FieldLabel";
  import LocationGoogleField from "./Edit/LocationGoogleField";

  export default {
    name: "EditField",
    components: {
      // AutoField,
      FieldLabel,
      ArrayField,
      BooleanField,
      CharField,
      DateField,
      // DateTimeField,
      DecimalField,
      EmailField,
      FileField,
      FloatField,
      ForeignKey,
      LocationGoogleField,
      ManyToManyField,
      LengthField,
      IntegerField,
      JSONActorsField,
      JSONDateAreaChoicesField,
      JSONDateAreaField,
      JSONDateChoiceField,
      JSONExportsField,
      JSONField,
      JSONJobsField,
      JSONLeaseField,
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
        default: () => ["display-field-label", "col-md-3", "col-lg-3"],
      },
      valueClasses: {
        type: Array,
        default: () => ["display-field-value", "col-md-9", "col-lg-9"],
      },
      fileNotPublic: { type: Boolean, default: false },
      visible: { type: Boolean, default: true },
    },
    computed: {
      _value: {
        get() {
          return this.value;
        },
        set(v) {
          this.$emit("input", v);
        },
      },
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
    methods: {},
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
