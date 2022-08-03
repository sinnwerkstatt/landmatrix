<script lang="ts">
  import { gql } from "@urql/svelte";
  import { _ } from "svelte-i18n";
  import Select from "svelte-select";
  import { page } from "$app/stores";
  import type { FormField } from "$components/Fields/fields";

  export let value: number;
  export let formfield: FormField;

  type Currency = {
    id: number;
    code: string;
    name: string;
  };

  let currencies: Currency[] = [];

  async function getCurrencies() {
    const { data } = await $page.stuff.urqlClient
      .query<{ currencies: Currency[] }>(
        gql`
          query {
            currencies {
              id
              code
              name
            }
          }
        `
      )
      .toPromise();
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
      inputAttributes={{ name: formfield.name }}
    />
  {/if}
</div>
