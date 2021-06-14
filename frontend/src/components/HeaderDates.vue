<template>
  <div class="meta-panel">
    <DisplayField
      :wrapper-classes="['inlinefield']"
      :label-classes="['inlinelabel']"
      :value-classes="['inlineval']"
      fieldname="created_at"
      :value="obj.created_at"
    />
    <DisplayField
      :wrapper-classes="['inlinefield']"
      :label-classes="['inlinelabel']"
      :value-classes="['inlineval']"
      fieldname="modified_at"
      :value="obj.modified_at"
    />
    <DisplayField
      v-if="obj.fully_updated_at"
      :wrapper-classes="['inlinefield']"
      :label-classes="['inlinelabel']"
      :value-classes="['inlineval']"
      fieldname="fully_updated_at"
      :value="obj.fully_updated_at"
    />
  </div>
</template>

<script>
  import DisplayField from "$components/Fields/DisplayField";

  export default {
    name: "HeaderDates",
    components: { DisplayField },
    props: {
      obj: { type: Object, required: true },
    },
  };
</script>

<style lang="scss">
  .meta-panel {
    text-align: left;
    display: inline-block;
    background-color: darken(white, 2);
    padding: 0.5em 1em;
    border-radius: 5px;
    font-size: 0.9rem;
    color: rgba(0, 0, 0, 0.25);

    .inlinefield {
      display: inline-block;

      &:not(:last-child) {
        margin-right: 1.5em;
      }

      .inlinelabel {
        display: inline-block;
        color: rgba(0, 0, 0, 0.3);
      }

      .inlineval {
        font-style: italic;
      }
    }
  }
</style>
