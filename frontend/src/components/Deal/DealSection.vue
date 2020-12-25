<template>
  <b-tab
    v-if="any_field_at_all(sections)"
    :title="title"
    :active="active"
    @click="$emit('activated')"
  >
    <div>
      <div
        v-for="section in sections"
        v-if="any_field_in_section(section)"
        :key="section.name"
        class="panel-body"
      >
        <h3>{{ section.name }}</h3>
        <DisplayField
          v-for="fieldname in section.fields"
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
  import DisplayField from "components/Fields/DisplayField";

  export default {
    components: { DisplayField },
    props: ["title", "sections", "deal", "active"],
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
