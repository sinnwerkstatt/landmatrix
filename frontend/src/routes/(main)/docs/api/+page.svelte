<script lang="ts">
  import { page } from "$app/stores"
</script>

{#if $page.url.searchParams.get("from_graphql")}
  <div
    class="container mx-auto my-8 rounded border border-orange bg-orange-100 px-4 py-2"
  >
    <div class="heading4">GraphQL has been deprecated.</div>

    <p>
      We're sorry for the inconvenience. GraphQL turned out to be a bad idea for this
      project so we moved back to a normal REST API.
    </p>
  </div>
{/if}

<svelte:head>
  <title>API Documentation | Land Matrix</title>
</svelte:head>

<div class="container mx-auto mt-6">
  <h1 class="heading1">API Documentation</h1>

  <p>The current API is a normal OpenAPI based REST API.</p>

  <p>
    You will find interfaces here: <a data-sveltekit-reload href="/api/schema/redoc/">
      ReDOC
    </a>
    and here:
    <a data-sveltekit-reload href="/api/schema/swagger-ui/">Swagger</a>
  </p>

  <p>
    The schema is here: <a data-sveltekit-reload href="/api/schema.yaml">schema.yml</a>
    or
    <a data-sveltekit-reload href="/api/schema.json">schema.json</a>
  </p>

  <p>
    All paths and corresponding filter options should be defined within the specs,
    <br />
    e.g.
    <code>/api/deals/</code>
    has the option to be filtered by
    <code>country_id</code>
    as seen in the spec here:
    <a data-sveltekit-reload href="/api/schema/swagger-ui/#/deals/deals_list">
      deal list filters
    </a>
  </p>
</div>
