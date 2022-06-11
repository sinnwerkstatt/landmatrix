<script lang="ts">
  export let value: number;
  export let model: string;
  export let targetBlank = false;
  export let objectVersion: number;

  let href = (model === "deal" ? "/deal/" : "/investor/") + value;
  if (objectVersion) href += "/" + objectVersion;
</script>

<div class="auto_field">
  <a
    class="inline py-1 px-2 text-white text-xs font-bold text-center whitespace-nowrap align-baseline {model ===
    'deal'
      ? 'bg-orange hover:bg-orange-600'
      : 'bg-pelorous hover:bg-pelorous-600'}"
    {href}
    target={targetBlank ? "_blank" : "_self"}
  >
    {value}
  </a>
</div>
