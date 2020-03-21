<template>
  <div>
    <p class="alert alert-warning">
      <input type="checkbox" id="id_set_default_filters" name="set_default_filters"
             class="pull-right">

      <strong>Default filters are disabled</strong>. You can see all data unfiltered.
      Please check the checkbox to use our global or national filter presets. <a
        href="/faq/#what-are-the-database-default-settings">Read more</a>
    </p>

    <div id="list-filters" class="row">
      <div class="col-md-10 col-auto">
        <span id="filterlist"><label>No active filters</label></span>
        <a class="toggle-filters toggle-text" role="button" data-toggle="collapse"
           href="#add-filter" aria-expanded="true"
           data-toggle-text="Cancel add filter" aria-controls="add-filter">
          <i class="fa fa-plus"></i> Add a filter
        </a>
      </div>
      <div class="col-md-2 ml-auto text-right">

        <a class="toggle-filters" role="button" data-toggle="collapse"
           href="#filter-settings" aria-expanded="true" aria-controls="filter-settings"
           name="List settings">
          <i class="fa fa-cog"></i>
        </a>

        <a href="#" class="toggle-tooltip noul" title=""
           data-original-title="You can create custom filters here. Filters are kept when changing entry point.">
          <i class="lm lm-question-circle"> </i></a>
      </div>
    </div>

  </div>
</template>

<script>
  export default {
    name: "FilterBar"
  }
</script>

<style scoped>

</style>
