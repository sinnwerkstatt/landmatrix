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
        :file-not-public="fileNotPublic"
        :target-blank="targetBlank"
        :object-id="objectId"
        :object-version="objectVersion"
      />
    </div>
  </div>
</template>

<script lang="ts">
  import type { FormField } from "$components/Fields/fields";
  import { custom_is_null } from "$utils/data_processing";
  import ArrayField from "./Display/ArrayField.vue";
  import SimpleArrayField from "./Display/ArrayField.vue";
  import AutoField from "./Display/AutoField.vue";
  import BooleanField from "./Display/BooleanField.vue";
  import NullBooleanField from "./Display/BooleanField.vue";
  import DateField from "./Display/DateField.vue";
  import DateTimeField from "./Display/DateField.vue";
  import DecimalField from "./Display/DecimalField.vue";
  import FloatField from "./Display/DecimalField.vue";
  import IntegerField from "./Display/DecimalField.vue";
  import FileField from "./Display/FileField.vue";
  import ForeignKey from "./Display/ForeignKeyField.vue";
  import ModelChoiceField from "./Display/ForeignKeyField.vue";
  import CurrencyForeignKey from "./Display/ForeignKeyField.vue";
  import CountryForeignKey from "./Display/ForeignKeyField.vue";
  import InvestorForeignKey from "./Display/ForeignKeyField.vue";
  import JSONActorsField from "./Display/JSONActorsField.vue";
  import JSONDateAreaChoicesField from "./Display/JSONDateAreaChoicesField.vue";
  import JSONDateAreaField from "./Display/JSONDateAreaField.vue";
  import JSONDateChoiceField from "./Display/JSONDateChoiceField.vue";
  import JSONExportsField from "./Display/JSONExportsField.vue";
  import JSONField from "./Display/JSONField.vue";
  import JSONJobsField from "./Display/JSONJobsField.vue";
  import JSONLeaseField from "./Display/JSONLeaseField.vue";
  import LengthField from "./Display/LengthField.vue";
  import ManyToManyField from "./Display/ManyToManyField.vue";
  import OCIDField from "./Display/OCIDField.vue";
  import PointField from "./Display/PointField.vue";
  import StatusField from "./Display/StatusField.vue";
  import CharField from "./Display/TextField.vue";
  import EmailField from "./Display/TextField.vue";
  import TextField from "./Display/TextField.vue";
  import URLField from "./Display/TextField.vue";
  import TypedChoiceField from "./Display/TypedChoiceField.vue";
  import WorkflowInfosField from "./Display/WorkflowInfosField.vue";
  import FieldLabel from "./FieldLabel.vue";
  import Vue from "vue";

  export default Vue.extend({
    name: "DisplayField",
    components: {
      TypedChoiceField,
      SimpleArrayField,
      ModelChoiceField,
      CurrencyForeignKey,
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
      CountryForeignKey,
      InvestorForeignKey,
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
      ManyToManyField,
      NullBooleanField,
      PointField,
      StatusField,
      TextField,
      URLField,
      OCIDField,
      WorkflowInfosField,
    },
    props: {
      fieldname: { type: String, required: true },
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
      targetBlank: { type: Boolean, default: false },
      objectId: { type: Number, default: null, required: false },
      objectVersion: { type: Number, default: null, required: false },
    },
    data() {
      return { custom_is_null };
    },
    computed: {
      _visible(): boolean {
        if (!this.visible) return false;
        if (this.fieldname === "file_not_public") return false;
        if (this.formfield.class === "FileField") {
          return !this.fileNotPublic || this.$store.getters.userAuthenticated;
        }
        return true;
      },
      formfield(): FormField {
        return {
          name: this.fieldname,
          ...this.$store.state.formfields[this.model][this.fieldname],
        };
      },
    },
  });
</script>

<style lang="scss">
  .display-field-wrapper {
    margin-bottom: 0.7em;
    line-height: 1.2;
  }
  .display-field-label {
    font-weight: 500;
  }
  .display-field-value {
    line-height: 1.2;
    color: var(--color-lm-dark);
  }
</style>
