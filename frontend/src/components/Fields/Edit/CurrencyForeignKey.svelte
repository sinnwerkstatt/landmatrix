<script lang="ts">
  import { gql, Client } from "@urql/svelte"
  import { _ } from "svelte-i18n"
  import { onMount } from "svelte"

  import { page } from "$app/stores"

  import VirtualListSelect from "$components/LowLevel/VirtualListSelect.svelte"
  import type { FormField } from "$components/Fields/fields"

  export let value: number
  export let formfield: FormField

  type Currency = {
    id: number
    code: string
    name: string
  }

  let currencies: Currency[] = []

  async function getCurrencies() {
    const { error, data } = await ($page.data.urqlClient as Client)
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
