<script lang="ts">
  import { _ } from "svelte-i18n"

  export let value: string

  export let extras = {
    url: false,
    ocid: false,
    email: false,
    investorNameUnknown: false,
  }

  const safeGetHostname = (value: string): string => {
    try {
      return new URL(value).hostname
    } catch (e) {
      // console.error("error", e)
      return value
    }
  }
</script>

{#if extras.url}
  <a href={value} target="_blank" rel="noreferrer" class="break-all">
    {safeGetHostname(value)}
  </a>
  <!--{:else if extras.email}-->
  <!--  <a href="mailto://{value}">{value}</a>-->
{:else if extras.ocid}
  <a
    href="https://www.openlandcontracts.org/contract/{value}/view#/pdf"
    target="_blank"
    rel="noreferrer"
  >
    {$_("Access more information about this contract on OpenLandContracts.org")}
  </a>
{:else if extras.investorNameUnknown}
  <span class="italic text-gray-600">[{$_("unknown investor")}]</span>
{:else}
  <div class="whitespace-pre-wrap break-words">
    {value ?? "—"}
  </div>
{/if}
