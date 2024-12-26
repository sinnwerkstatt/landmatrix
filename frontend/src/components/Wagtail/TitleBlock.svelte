<script lang="ts">
  interface Props {
    value: {
      url?: string
      value: string
      fa_icon: string
    }
  }

  let { value }: Props = $props()
</script>

<h3 data-block="heading">
  {#if value.url}
    <a href={value.url}>
      <i class="fa fa-{value.fa_icon}"></i>
      {value.value}
    </a>
  {:else}
    <i class="fa fa-{value.fa_icon}"></i>
    {value.value}
  {/if}
</h3>
