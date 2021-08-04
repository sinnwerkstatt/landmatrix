<template>
  <div class="meta-panel" :class="{ draft: isVersion }">
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
      isVersion: { type: Boolean, default: false },
    },
  };
</script>

<style lang="scss">
  .meta-panel {
    position: relative;
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

    &.draft {
      //background-color: white !important;
      &:after {
        content: "DRAFT";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        letter-spacing: 1.5rem;
        transform: rotate(-5deg);
        color: black;
        opacity: 0.1;
        z-index: 0;
      }
    }
  }
</style>
