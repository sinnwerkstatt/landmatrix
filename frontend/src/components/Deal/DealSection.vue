<template>
  <b-tab
    v-if="any_field_in_sections(sections)"
    :title="$t(title)"
    :active="active"
    @click="$emit('activated')"
  >
    <div>
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
    </div>
    <slot />
  </b-tab>
</template>

<script>
  import DisplayField from "$components/Fields/DisplayField";

  export default {
    components: { DisplayField },
    props: {
      title: { type: String, required: true },
      sections: { type: Array, required: true },
      deal: { type: Object, required: true },
      active: { type: Boolean, default: false },
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
