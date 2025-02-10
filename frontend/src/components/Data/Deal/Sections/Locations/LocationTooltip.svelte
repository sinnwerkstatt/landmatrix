<script lang="ts">
  import type { Feature } from "ol"
  import { _ } from "svelte-i18n"

  interface Props {
    feature: Feature
  }

  let { feature }: Props = $props()

  const fprops = $derived(feature.getProperties())
</script>

<div
  class="min-w-80 rounded-xl border bg-white p-4 text-sm drop-shadow-[4px_4px_5px_rgba(0,0,0,0.4)] dark:bg-gray-900"
>
  <div class="mb-2">
    <a class="font-mono text-lg" href="#{fprops.nid}">
      #{fprops.nid}
    </a>
  </div>
  <div>
    <b>{$_("Name")}</b>
    : {fprops.name}
  </div>
  <div>
    <b>{$_("Point")}</b>
    : {fprops.point}
  </div>
</div>
