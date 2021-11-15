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

<script lang="ts">
  import DisplayField from "$components/Fields/DisplayField.vue";
  import Vue from "vue";
  import { custom_is_null } from "$utils/data_processing";

  export default Vue.extend({
    components: { DisplayField },
    props: {
      deal: { type: Object, required: true },
      sections: { type: Array, required: true },
    },
    computed: {
      sections_with_filled_fields(): unknown {
        return this.sections.filter((section) => {
          return this.section_fields_with_values(section).length > 0;
        });
      },
    },
    methods: {
      any_field_in_sections(sections): boolean {
        return (
          sections.filter(
            (section) => this.section_fields_with_values(section).length > 0
          ).length > 0
        );
      },
      section_fields_with_values<T>(section: T[]): T[] {
        return section.fields.filter((field) => {
          return custom_is_null(this.deal[field]);
        });
      },
    },
  });
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
