<script>
  let displayDealsCount;
  // export default {
  //   name: "DealDisplayToggle",
  //   computed: {
  //     displayDealsCount: {
  //       get() {
  //         return this.$store.state.displayDealsCount;
  //       },
  //       set(value) {
  //         this.$store.commit("setDisplayDealsCount", value);
  //       },
  //     },
  //   },
  // };
</script>

<div class="toggle-buttons">
  <button
    class:active={displayDealsCount}
    on:click|preventDefault={() => (displayDealsCount = true)}
  >
    No. of deals
  </button>
  <button
    class:active={!displayDealsCount}
    on:click|preventDefault={() => (displayDealsCount = false)}
  >
    Deal size
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
