<script lang="ts">
  export let value: {
    image?: { url: string };
    url: string;
    caption?: string;
    external?: boolean;
  };

  $: link = value.image ? value.url : null;
  $: path = value.image ? value.image.url : value.url;
  $: caption = value.image ? value.caption : null;
  $: externalLink = value.image ? value.external : false;
</script>

<div class="widget-image mb-5">
  {#if link}
    <a href={link} target={externalLink ? "_blank" : "_self"}>
      <img class="w-full max-w-full" src={path} alt="" />
    </a>
  {:else}
    <img class="w-full max-w-full" src={path} alt="" />
  {/if}
  {#if caption}
    <div class="mx-2 font-bold bg-[rgba(0,0,0,.75)] p-3">
      <p>{@html caption}</p>
    </div>
  {/if}
</div>
