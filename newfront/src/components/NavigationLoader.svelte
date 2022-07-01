<script lang="ts">
  import { navigating } from "$app/stores";
  import { loading } from "$lib/data";
</script>

{#if $navigating || $loading}
  <div class="h-1 fixed top-0 left-0 right-0 w-full z-[1000000]">
    <div class="w-full h-1 bg-orange-100 overflow-hidden relative">
      <div class="bg-orange h-1 absolute inc" />
      <div class="bg-orange-600 h-1 absolute dec" />
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
