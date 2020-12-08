<template>
  <div class="row">
    <div class="col-12">
      <div id="accordion" class="accordion">
        <div v-for="faq in value.faqs" class="card">
          <div class="card-header" id="headingOne">
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
    props: ["value"],
  };
  // TODO: Richtext in answer not evaluated yet.
</script>

<style scoped></style>
