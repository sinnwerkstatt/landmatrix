<template>
  <div class="container">
    <div class="my-5">
      {{
        $t(
          "The page you are looking for appears to have been moved, deleted or does not exist."
        )
      }}
    </div>
  </div>
</template>

<script>
  export default {
    name: "NotFound",
    metaInfo() {
      return { title: "404 - Page not found." };
    },
  };
</script>
