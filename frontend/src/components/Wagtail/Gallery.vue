<template>
  <div class="row widget-gallery" :class="galleryColumns">
    <div
      v-for="(image, index) in value.images"
      :key="index"
      class="col"
      :class="[colSize]"
    >
      <wagtail-image :value="image" />
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      value: { type: Object, required: true },
    },
    computed: {
      galleryColumns() {
        let cols = parseInt(this.value.columns);
        if (cols > 6) cols = 1;
        return `widget-gallery-columns-${cols}`;
      },
      colSize() {
        let cols = parseInt(this.value.columns);
        let sm;
        let xs = 12;
        if (cols === 2) xs = 6;
        if (cols === 3) xs = 4;
        if (cols === 4) xs = 3;
        if (cols === 6) xs = 4;
        if (cols === 5) {
          xs = 4;
          sm = 2;
        }
        //,(index%5===0)?('col-sm-offset-'+('')):null  // TODO I guess
        if (cols === 6) {
          xs = 4;
          sm = 2;
        }
        let retval = [`col-xs-${xs}`];
        if (sm) {
          retval.push(`col-sm-${sm}`);
        }
        return retval;
      },
    },
  };
</script>

<style scoped></style>
