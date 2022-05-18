<template>
  <div v-if="_visible" :class="wrapperClasses">
    <FieldLabel
      v-if="showLabel"
      :fieldname="fieldname"
      :label-classes="getLabelClasses"
      :model="model"
    />
    <div :class="getValueClasses">
      <component
        :is="formfield.class"
        v-model="_value"
        :formfield="formfield"
        :model="model"
        :disabled="disabled"
      />
    </div>
  </div>
</template>

<script lang="ts">
  import ManyToManyField from "./Display/ManyToManyField.vue";
  import SimpleArrayField from "./Edit/ArrayField.vue";
  import ArrayField from "./Edit/ArrayField.vue";
  import BooleanField from "./Edit/BooleanField.vue";
  import NullBooleanField from "./Edit/BooleanField.vue";
  import CountryForeignKey from "./Edit/CountryForeignKeyField.vue";
  import DateField from "./Edit/DateField.vue";
  import DecimalField from "./Edit/DecimalField.vue";
  import FloatField from "./Edit/DecimalField.vue";
  import IntegerField from "./Edit/DecimalField.vue";
  import FileField from "./Edit/FileField.vue";
  import ForeignKey from "./Edit/ForeignKeyField.vue";
  import CurrencyForeignKey from "./Edit/ForeignKeyField.vue";
  import ModelChoiceField from "./Edit/ForeignKeyField.vue";
  import InvestorForeignKey from "./Edit/InvestorForeignKeyField.vue";
  import JSONActorsField from "./Edit/JSONActorsField.vue";
  import JSONDateAreaChoicesField from "./Edit/JSONDateAreaChoicesField.vue";
  import JSONDateAreaField from "./Edit/JSONDateAreaField.vue";
  import JSONDateChoiceField from "./Edit/JSONDateChoiceField.vue";
  import JSONExportsField from "./Edit/JSONExportsField.vue";
  import JSONField from "./Edit/JSONField.vue";
  import JSONJobsField from "./Edit/JSONJobsField.vue";
  import JSONLeaseField from "./Edit/JSONLeaseField.vue";
  import PointField from "./Edit/PointField.vue";
  import CharField from "./Edit/TextField.vue";
  import EmailField from "./Edit/TextField.vue";
  import TextField from "./Edit/TextField.vue";
  import URLField from "./Edit/TextField.vue";
  import OCIDField from "./Edit/TextField.vue";
  import TypedChoiceField from "./Edit/TypedChoiceField.vue";
  import FieldLabel from "./FieldLabel.vue";
  import Vue from "vue";

  export default Vue.extend({
    name: "EditField",
    components: {
      // AutoField,
      FieldLabel,
      ArrayField,
      SimpleArrayField,
      ModelChoiceField,
      TypedChoiceField,
      BooleanField,
      CharField,
      DateField,
      CurrencyForeignKey,
      // DateTimeField,
      DecimalField,
      EmailField,
      FileField,
      FloatField,
      ForeignKey,
      CountryForeignKey,
      InvestorForeignKey,
      ManyToManyField,
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
      value: { required: true },
      model: { type: String, default: "deal" },
      showLabel: { type: Boolean, default: true },
      wrapperClasses: {
        type: Array,
        default: () => ["display-field-wrapper", "form-field", "row"],
      },
      labelClasses: { type: Array },
      valueClasses: { type: Array },
      fileNotPublic: { type: Boolean, default: false },
      visible: { type: Boolean, default: true },
      disabled: { type: Boolean, default: false },
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
      getLabelClasses() {
        if (!this.labelClasses) {
          if (this.isShortField) {
            return ["display-field-label", "col-md-6", "col-xl-3"];
          } else {
            return ["display-field-label", "col-12"];
          }
        } else {
          return this.labelClasses;
        }
      },
      getValueClasses() {
        if (!this.valueClasses) {
          if (this.isShortField) {
            return ["display-field-value", "col-md-6", "col-xl-3"];
          } else {
            return ["display-field-value", "col-12"];
          }
        } else {
          return this.valueClasses;
        }
      },
      isShortField() {
        return (
          [
            "IntegerField",
            "DecimalField",
            "DateField",
            "LowLevelDecimalField",
            "BooleanField",
            "NullBooleanField",
          ].includes(this.formfield.class) ||
          (["TextField", "CharField"].includes(this.formfield.class) &&
            this.formfield.choices)
        );
      },
    },
    methods: {},
  });
</script>

<style lang="scss">
  .display-field-wrapper {
    margin-bottom: 0.7em;
    line-height: 1.2;
  }

  .display-field-label {
    font-weight: 500;
    align-self: center;
    color: var(--color-lm-dark);

    &.col-12 {
      margin-bottom: 0.5em;
    }
  }

  .display-field-value {
    line-height: 1.2;
    color: var(--color-lm-dark);

    .select {
      width: 100%;
    }

    .form-control.is-valid {
      border-color: lightgrey;
    }

    textarea:focus::placeholder {
      color: lightgrey;
      opacity: 1;
      font-weight: normal;
    }

    th {
      text-align: center;
      font-weight: 500;
      font-size: 0.8em;
      opacity: 0.8;
      padding-bottom: 5px;
    }

    td {
      padding: 0.25em;

      &.buttons {
        white-space: nowrap;

        a {
          padding: 7px;

          &:first-child {
            padding-left: 0;
          }
        }
      }

      .form-check-inline {
        margin-right: 0;
      }
    }

    tr.is-current {
      $radius: 5px;
      border-radius: $radius;

      td {
        background: var(--color-lm-orange-light-10);

        &:first-child {
          border-top-left-radius: $radius;
          border-bottom-left-radius: $radius;
        }

        &:last-child {
          border-top-right-radius: $radius;
          border-bottom-right-radius: $radius;
        }
      }
    }

    select[multiple] {
      appearance: none;
      -moz-appearance: none;
      -webkit-appearance: none;

      option:checked {
        background: var(--color-lm-orange-light);
        // WTF: Only works when setting a gradient!!!
        background: linear-gradient(hsl(32, 97%, 65%), hsl(32, 97%, 65%));
      }
    }
  }
</style>
