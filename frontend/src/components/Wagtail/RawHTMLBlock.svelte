<script lang="ts">
  interface Props {
    value: string
  }

  let { value }: Props = $props()
</script>

<div data-block="html" class="html-block mx-auto max-w-[1200px] px-3 sm:px-6">
  {@html value}
</div>
