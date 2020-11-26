<template>
  <div>
    <h2 class="bar-title">Dynamics Overview Charts</h2>
    <p>Show segmentation by number of deals or deal size: </p>
    <DealDisplayToggle />
  </div>
</template>

<script>
  import DealDisplayToggle from "../Shared/DealDisplayToggle";

  export default {
    components: { DealDisplayToggle },
  };
</script>

<style lang="scss">
</style>
