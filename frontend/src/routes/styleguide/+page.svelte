<script>
  import ButtonStyles from "./ButtonStyles.svelte"
  import ColorStyles from "./ColorStyles.svelte"
  import TypographyStyles from "./TypographyStyles.svelte"
</script>

<svelte:head>
  <title>Styleguide | Land Matrix</title>
</svelte:head>


<div class="container mx-auto mb-32">
  <h1 class="heading2">Style guide</h1>

  <ColorStyles />
  <div class="p-28" />

  <TypographyStyles />
  <div class="p-28" />

  <ButtonStyles />
</div>
