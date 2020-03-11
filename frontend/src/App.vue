<template>

  <div id="app">
    <div class="row">
      <div class="col-md-12">
        <h1><span>{{this.$store.state.title}}</span></h1>
      </div>
    </div>

    <router-view/>

  </div>
</template>

<style lang="scss">
  .logo {
    width: 300px;
    text-align: center;
  }
</style>
