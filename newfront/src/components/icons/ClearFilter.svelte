<script lang="ts">
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();
</script>

<svg
  xmlns="http://www.w3.org/2000/svg"
  class={$$props.class ?? "h-4 w-4 inline"}
  fill="none"
  viewBox="0 0 24 24"
  stroke="currentColor"
  stroke-width="2"
  on:click|stopPropagation={() => dispatch("click")}
>
  <path
    stroke-linecap="round"
    stroke-linejoin="round"
    d="m 18.747867,17.128735 h -3.265395 m 6.53079,0 a 4.8980919,4.8980919 0 1 1 -9.796183,0 4.8980919,4.8980919 0 0 1 9.796183,0 z"
    stroke-width="1.4"
    stroke="currentColor"
  />
  <path
    fill-rule="evenodd"
    d="M 0.75726297,2.4728982 A 1.1628317,1.1628317 0 0 1 1.9200945,1.3100666 H 15.874074 a 1.1628317,1.1628317 0 0 1 1.162832,1.1628316 v 3.4884949 a 1.1628317,1.1628317 0 0 1 -0.34071,0.8221219 l -5.473449,5.473449 v 4.169914 a 1.1628317,1.1628317 0 0 1 -0.34071,0.822123 L 8.5563751,19.574662 A 1.1628317,1.1628317 0 0 1 6.571421,18.752541 V 12.256964 L 1.0979725,6.783515 A 1.1628317,1.1628317 0 0 1 0.75726297,5.9613931 Z"
    clip-rule="evenodd"
    fill="currentColor"
    stroke-width="0.218"
    style="fill-opacity:1;stroke:none;stroke-width:0.218013;stroke-miterlimit:4;stroke-dasharray:none"
  />
</svg>
