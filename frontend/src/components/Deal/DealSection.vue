<template>
  <b-tab :title="title" v-if="!readonly || any_field_at_all(sections)">
    <div>
      <div
        v-for="section in sections"
        class="panel-body"
        v-if="!readonly || any_field_in_section(section)"
      >
        <h3>{{ section.name }}</h3>
        <component
          :is="formfield.class"
          :formfield="formfield"
          :readonly="!!readonly"
          v-model="deal[formfield.name]"
          v-for="formfield in section.fields"
          v-if="!readonly || custom_is_null(deal[formfield.name])"
        />
      </div>
    </div>
  </b-tab>
</template>

<script>
  import ArrayField from "/components/Fields/ArrayField";
  import BooleanField from "/components/Fields/BooleanField";
  import NullBooleanField from "/components/Fields/BooleanField";
  import CharField from "/components/Fields/TextField";
  import DecimalField from "/components/Fields/DecimalField";
  import FloatField from "/components/Fields/DecimalField";
  import IntegerField from "/components/Fields/DecimalField";
  import ForeignKey from "/components/Fields/ForeignKeyField";
  import TextField from "/components/Fields/TextField";
  import JSONField from "/components/Fields/JSONField";

  export default {
    props: ["title", "sections", "deal", "readonly"],
    components: {
      ArrayField,
      BooleanField,
      NullBooleanField,
      CharField,

      DecimalField,
      FloatField,
      IntegerField,
      ForeignKey,
      TextField,
      JSONField,
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
      any_field_in_section(section) {
        return !!section.fields.filter((field) => {
          return this.custom_is_null(this.deal[field.name]);
        }).length;
      },
      any_field_at_all(sections) {
        return !!sections.filter((section) => this.any_field_in_section(section))
          .length;
      },
    },
  };
</script>
