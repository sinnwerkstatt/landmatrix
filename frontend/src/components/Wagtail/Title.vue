<template>
  <h3>
    <a v-if="value.url" :href="value.url">
      <i :class="['fa', `fa-${value.fa_icon}`]"></i> {{ value.value }}
    </a>
    <template v-else>
      <i :class="['fa', `fa-${value.fa_icon}`]"></i> {{ value.value }}
    </template>
  </h3>
</template>

<script>
  export default {
    props: ["value"],
  };
</script>
