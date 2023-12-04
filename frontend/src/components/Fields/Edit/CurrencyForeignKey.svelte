<script lang="ts">
  import { gql } from "@urql/svelte"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import type { FormField } from "$components/Fields/fields"
  import VirtualListSelect from "$components/LowLevel/VirtualListSelect.svelte"

  export let value: number
  export let formfield: FormField

  type Currency = {
    id: number
    code: string
    name: string
  }

  let currencies: Currency[] = []

  async function getCurrencies() {
    const { error, data } = await $page.data.urqlClient
      .query<{ currencies: Currency[] }>(
        gql`
          query {
            currencies {
              id
              code
              name
            }
          }
        `,
        {},
      )
      .toPromise()

    if (error || !data) {
      console.error(error)
      return
    }
    currencies = data.currencies
  }

  onMount(() => getCurrencies())
</script>

{#if currencies}
  <VirtualListSelect
    bind:value
    items={currencies}
    placeholder={$_("Currency")}
    label="name"
    name={formfield.name}
  >
    <svelte:fragment slot="selection" let:selection>
      {selection.name} ({selection.code})
    </svelte:fragment>
    <svelte:fragment slot="item" let:item>
      {item.name} ({item.code})
    </svelte:fragment>
  </VirtualListSelect>
{/if}
