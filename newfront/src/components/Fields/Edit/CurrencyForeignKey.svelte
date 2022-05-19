<script lang="ts">
  import { gql } from "@apollo/client/core";
  import Select from "svelte-select";
  import { client } from "$lib/apolloClient";
  import type { FormField } from "../fields";

  export let formfield: FormField;
  export let value: number;

  type Currency = {
    id: number;
    code: string;
    name: string;
  };

  let currencies: Currency[] = [];

  async function getCurrencies() {
    const { data } = await $client.query<{ currencies: Currency[] }>({
      query: gql`
        query {
          currencies {
            id
            code
            name
          }
        }
      `,
    });
    currencies = data.currencies;
  }
  getCurrencies();

  //       set(v) {
  //         let em = v ? { id: v.id, name: v.name, code: v.code } : null;
  //         this.$emit("input", em);
  //       },
  //     },
  //   },
  // };
</script>

<div class="currency_foreignkey_field">
  {#if currencies}
    <Select
      items={currencies.map((c) => ({ value: c.id, label: `${c.name} (${c.code})` }))}
      bind:value
      placeholder="Currency"
      showChevron
    />
  {/if}
</div>
