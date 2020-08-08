<template>
  <div class="">
    blablabla
  </div>
</template>

<script>
  import store from "/store";

  export default {
    name: "Charts",
    beforeRouteEnter(to, from, next) {
      let title = "Web of transnational deals";
      store.dispatch("setPageContext", {
        title: title,
        breadcrumbs: [
          { link: { name: "wagtail" }, name: "Home" },
          { link: { name: "charts" }, name: "Charts" },
          { name: title },
        ],
      });
      next();
    },
  };
</script>

<style scoped></style>
