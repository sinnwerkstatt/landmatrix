<script lang="ts">
  import { _ } from "svelte-i18n";
  import { displayDealsCount } from "$components/Map/map_helper";

  $: displayDeals = $displayDealsCount ? "bg-orange text-white" : "bg-white border";
  $: displaySize = $displayDealsCount ? "bg-white border" : "bg-orange text-white";
</script>

<div class="text-center flex justify-center mt-8 ">
  <button
    class:active={$displayDealsCount}
    on:click|preventDefault={() => displayDealsCount.set(true)}
    class={`font-bold hover:underline my-2 py-2 px-3 transform duration-100 ${displayDeals}`}
  >
    {$_("No. of deals")}
  </button>
  <button
    class:active={!$displayDealsCount}
    on:click|preventDefault={() => displayDealsCount.set(false)}
    class={`font-bold hover:underline my-2 py-2 px-3 transform duration-100 ${displaySize}`}
  >
    {$_("Deal size")}
  </button>
</div>

<!--<style lang="scss" scoped>-->
<!--  .toggle-buttons {-->
<!--    margin-top: 1.5em;-->
<!--    margin-bottom: 5px;-->
<!--    width: 100%;-->
<!--    text-align: center;-->
<!--    display: flex;-->
<!--    justify-content: center;-->

<!--    a {-->
<!--      padding: 0.3em 0.5em;-->
<!--      background-color: white;-->
<!--      border: 1px solid var(&#45;&#45;color-lm-light);-->
<!--      color: black;-->
<!--      font-weight: bold;-->
<!--      font-size: 14px;-->

<!--      &.active {-->
<!--        background-color: var(&#45;&#45;color-lm-orange);-->
<!--        color: white;-->
<!--      }-->
<!--    }-->
<!--  }-->
<!--</style>-->
