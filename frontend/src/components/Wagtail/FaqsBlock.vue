<template>
  <div class="row">
    <div class="col-12">
      <div id="accordion" class="accordion">
        <div v-for="faq in value.faqs" :key="faq.slug" class="card">
          <div id="headingOne" class="card-header">
            <h5 class="mb-0">
              <button
                class="btn btn-link"
                data-toggle="collapse"
                :data-target="`#collapse-${faq.slug}`"
                aria-expanded="true"
                :aria-controls="`collapse-${faq.slug}`"
              >
                {{ faq.question }}
              </button>
            </h5>
          </div>
          <div
            :id="`collapse-${faq.slug}`"
            class="collapse"
            aria-labelledby="headingOne"
            data-parent="#accordion"
          >
            <div class="card-body" v-html="faq.answer" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    props: {
      value: { type: Object, required: true },
    },
  };
</script>

<style scoped></style>
