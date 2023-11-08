<script lang="ts">
  import { navigating } from "$app/stores"

  import { loading } from "$lib/stores"
</script>

{#if $navigating || $loading}
  <div class="fixed left-0 right-0 top-0 z-[1000000] h-1 w-full">
    <div class="relative h-1 w-full overflow-hidden bg-orange-100">
      <div class="inc absolute h-1 bg-orange" />
      <div class="dec absolute h-1 bg-orange-600" />
    </div>
  </div>
{/if}

<style>
  /* kudos https://codepen.io/shalimano/pen/wBmNGJ */
  .inc {
    animation: increase 2s ease-in-out infinite;
  }

  .dec {
    animation: decrease 2s 0.9s ease-in-out infinite;
  }

  @keyframes increase {
    from {
      left: -5%;
      width: 5%;
    }
    to {
      left: 130%;
      width: 150%;
    }
  }

  @keyframes decrease {
    from {
      left: -90%;
      width: 90%;
    }
    to {
      left: 110%;
      width: 10%;
    }
  }
</style>
