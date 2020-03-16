<template>

  <div id="app">
    <div class="row">
      <div class="col-md-4">
        <ul class="breadcrumb">
          <li><a href="/">Home</a></li>
          <li v-for="bcrumb in this.$store.state.breadcrumbs" :key="bcrumb.name">
            <a v-if="bcrumb.href" :href="bcrumb.href">{{bcrumb.name}}</a>
            <template v-else>
              {{bcrumb.name}}
            </template>
          </li>
        </ul>
      </div>
      <div class="col-md-6 col-md-offset-2">
        <ul class="subnav nav nav-pills pull-right">
          <li role="presentation"><a href="/map/">
            <i class="fa fa-map-marker"></i> Map
          </a></li>
          <li role="presentation"><a href="/newdeal/">
            <i class="fa fa-table"></i> Data
          </a></li>
          <li role="presentation"><a href="/charts/">
            <i class="fa fa-bar-chart"></i> Charts
          </a></li>
          <li class="divider"></li>
          <li role="presentation">
          </li>
          <li role="presentation">
          </li>
        </ul>
      </div>
    </div>

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
