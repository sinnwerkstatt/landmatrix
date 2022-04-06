<script lang="ts">
  import type { FormField } from "$components/Fields/fields";
  import { _ } from "svelte-i18n";

  export let formfield: FormField;
  export let value: string;
  export let model: string;
  export let fileNotPublic: boolean;

  // export default Vue.extend({
  //
  //   data() {
  //     return { media_url: import.meta.env.VITE_MEDIA_URL };
  //   },
</script>

<div class="file_field">
  <a href="{media_url}{value}" target="_blank">
    {#if fileNotPublic}
      <p class="fas fa-eye-slash mr-1 italic" />
      <p class="far fa-file-pdf" />

      {() => {
        value.replace("uploads/", "");
      }}
    {/if}
  </a>
</div>
