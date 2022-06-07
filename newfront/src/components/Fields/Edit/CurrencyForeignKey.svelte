<script lang="ts">
  import { gql } from "@apollo/client/core";
  import { _ } from "svelte-i18n";
  import Select from "svelte-select";
  import { client } from "$lib/apolloClient";

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
</script>

<div class="currency_foreignkey_field">
  {#if currencies}
    <!-- removing "code" here, for "has deal changed" logic -->
    <Select
      items={currencies}
      {value}
      on:select={(x) => (value = { ...x.detail, code: undefined })}
      placeholder={$_("Currency")}
      optionIdentifier="id"
      labelIdentifier="name"
      getOptionLabel={(o) => `${o.name} (${o.code})`}
      getSelectionLabel={(o) => `${o.name} (${o.code})`}
      showChevron
    />
  {/if}
</div>
