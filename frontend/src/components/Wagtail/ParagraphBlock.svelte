<script lang="ts">
  export let value: string
</script>

<div
  data-block="paragraph"
  class="paragraph mx-auto mb-6 max-w-[1200px] break-words px-3 sm:px-6"
  data-sveltekit-reload
>
  {@html value}
</div>
