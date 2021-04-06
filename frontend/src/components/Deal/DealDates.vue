<template>
  <div class="meta-panel">
    <DisplayField
      :wrapper-classes="['inlinefield']"
      :label-classes="['inlinelabel']"
      :value-classes="['inlineval']"
      fieldname="created_at"
      :value="deal.created_at"
    />
    <DisplayField
      :wrapper-classes="['inlinefield']"
      :label-classes="['inlinelabel']"
      :value-classes="['inlineval']"
      fieldname="modified_at"
      :value="deal.modified_at"
    />
    <DisplayField
      :wrapper-classes="['inlinefield']"
      :label-classes="['inlinelabel']"
      :value-classes="['inlineval']"
      fieldname="fully_updated_at"
      :value="deal.fully_updated_at"
      :visible="!!deal.fully_updated_at"
    />
  </div>
</template>

<script>
  import DisplayField from "$components/Fields/DisplayField";
  export default {
    name: "DealDates",
    components: { DisplayField },
    props: {
      deal: { type: Object, required: true },
    },
  };
</script>

<style scoped></style>
