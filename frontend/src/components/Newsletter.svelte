<script lang="ts">
  import { _ } from "svelte-i18n"

  const listId = "cb4e9fb08e"
  const u = "93aa5e8fafa0f5b66b2a051cc"
</script>

<div id="mc_embed_signup">
  <form
    action="https://landmatrix.us5.list-manage.com/subscribe/post"
    method="post"
    id="mc-embedded-subscribe-form"
    name="mc-embedded-subscribe-form"
    class="validate"
    target="_blank"
  >
    <input type="hidden" name="u" value={u} />
    <input type="hidden" name="id" value={listId} />
    <input type="text" name="honeypot" id="honeypot" style="display:none;" />
    <input
      type="email"
      name="EMAIL"
      placeholder={$_("Enter your email")}
      required
      class=" mx-2 w-[300px] rounded p-2 text-black"
    />
    <button class="btn btn-orange mx-2 mt-2 sm:mt-0" type="submit">
      {$_("Subscribe")}
    </button>
  </form>
</div>
