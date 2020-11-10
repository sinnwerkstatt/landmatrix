<template>
  <b-tab :title="title" v-if="any_field_at_all(sections)" @click="$emit('activated')">
    <div>
      <div
        v-for="section in sections"
        class="panel-body"
        v-if="any_field_in_section(section)"
      >
        <h3>{{ section.name }}</h3>
        <Field
          :fieldname="fieldname"
          :readonly="!!readonly"
          v-model="deal[fieldname]"
          v-for="fieldname in section.fields"
        />
      </div>
    </div>
    <slot></slot>
  </b-tab>
</template>

<script>
  import Field from "/components/Fields/Field";

  export default {
    props: ["title", "sections", "deal", "readonly"],
    components: { Field },
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
          return this.custom_is_null(this.deal[field]);
        }).length;
      },
      any_field_at_all(sections) {
        return !!sections.filter((section) => this.any_field_in_section(section))
          .length;
      },
    },
  };
</script>
