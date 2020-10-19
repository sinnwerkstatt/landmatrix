<template>
  <div class="filter-collapse">
    <div @click="shown = !shown">
      <i class="fas" :class="[shown ? 'fa-chevron-down' : 'fa-chevron-right']"></i>
      {{ title }}
      <i
        v-if="clearable"
        class="delete-button fas fa-times fa-xs float-right text-primary"
        @click.stop="$emit('click')"
      />
    </div>
    <div v-if="shown">
      <slot></slot>
    </div>
  </div>
</template>
<script>
export default {
  name: "FilterCollapse",
  props: ["title", "clearable"],
  data() {
    return {
      shown: false,
    };
  },
};
</script>

<style lang="scss">
.filter-collapse {
  padding-top: 5px;
  padding-bottom: 5px;
  border-top: 1px solid #bbbbbb;
  border-bottom: 1px solid #bbbbbb;

  &:hover {
    cursor: pointer;
  }
  .delete-button {
    font-weight: bold;
    font-size: 14px;
    &:hover {
      font-size: 15px;
    }
  }
}
</style>
