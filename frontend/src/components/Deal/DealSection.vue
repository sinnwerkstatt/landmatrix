<template>
  <section v-if="any_field_in_sections(sections)">
    <div
      v-for="section in sections_with_filled_fields"
      :key="section.name"
      class="panel-body"
    >
      <h3>{{ $t(section.name) }}</h3>
      <DisplayField
        v-for="fieldname in section_fields_with_values(section)"
        :key="fieldname"
        :fieldname="fieldname"
        :value="deal[fieldname]"
      />
    </div>
    <slot />
  </section>
</template>

<script>
  import DisplayField from "$components/Fields/DisplayField";

  export default {
    components: { DisplayField },
    props: {
      deal: { type: Object, required: true },
      sections: { type: Array, required: true },
    },
    computed: {
      sections_with_filled_fields() {
        return this.sections.filter((section) => {
          return this.section_fields_with_values(section).length > 0;
        });
      },
    },
    methods: {
      any_field_in_sections(sections) {
        return (
          sections.filter(
            (section) => this.section_fields_with_values(section).length > 0
          ).length > 0
        );
      },
      section_fields_with_values(section) {
        return section.fields.filter((field) => {
          return !this.custom_is_null(this.deal[field]);
        });
      },
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

<style lang="scss" scoped>
  .panel-body > h3 {
    margin-top: 1em;
    margin-bottom: 0.5em;
  }

  .panel-body:first-child > h3 {
    margin-top: 0.3em;
  }
</style>
