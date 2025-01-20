<script lang="ts">
  interface Props {
    value: string
  }

  let { value }: Props = $props()
</script>

<a class="font-mono" href="#{value}">
  {value}
</a>
