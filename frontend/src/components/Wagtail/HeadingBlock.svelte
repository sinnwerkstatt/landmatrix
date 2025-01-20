<script lang="ts">
  interface Props {
    value: string
  }

  let { value }: Props = $props()
</script>

<h3 class="heading4 mx-auto mb-3 mt-6 w-fit xl:mb-6 xl:mt-12" data-block="heading">
  {value}
</h3>
