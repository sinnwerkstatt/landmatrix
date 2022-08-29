<script lang="ts">
  export let showing = true;
  export let flipped = false;
</script>

<span
  class="absolute top-[calc(50%-100px)] -right-5 cursor-pointer"
  class:flipped
  on:click
>
  <svg viewBox="0 0 2 20" width="20px" class="text-black opacity-80">
    <path d="M0,0 L2,2 L2,18 L0,20z" fill="hsl(32, 97%, 55%)" />
    <text x="0.3" y="11" fill="white" style="font-size:4px">
      {showing ? "‹" : "›"}
    </text>
  </svg>
</span>

<style>
  .flipped {
    transform: rotateY(180deg);
    left: -20px;
    right: auto;
  }
</style>
