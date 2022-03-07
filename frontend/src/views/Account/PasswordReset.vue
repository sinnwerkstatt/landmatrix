<template>
  <div>
    <PageTitle>{{ $t("Reset password") }}</PageTitle>
    <div class="flex justify-center items-center h-full w-full mb-4">
      <div class="w-[clamp(300px,80%,600px)] p-6 rounded border-2 border-[#4b4b4b]">
        <div v-if="form_submitted">
          If your email-address is registered with LandMatrix you should receive an
          email shortly
        </div>
        <form v-else @submit.prevent="submit">
          <label class="mb-4 block">
            {{ $t("Email") }}
            <input
              v-model="email"
              autocomplete="email"
              class="form-control block"
              :placeholder="$t('Email')"
              type="email"
            />
          </label>
          <button class="btn btn-primary block" type="submit">
            {{ $t("Reset password") }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import Vue from "vue";
  import PageTitle from "$components/PageTitle.vue";
  import { apolloClient } from "$utils/apolloclient";
  import gql from "graphql-tag";

  export default Vue.extend({
    name: "PasswordReset",
    components: { PageTitle },
    data() {
      return {
        email: null,
        form_submitted: false,
      };
    },
    created() {
      if (this.$store.getters.userAuthenticated) {
        if (this.$route.query.next)
          this.$router.push(this.$route.query.next.toString());
      }
    },
    methods: {
      submit() {
        apolloClient
          .mutate({
            mutation: gql`
              mutation ($email: String!) {
                password_reset(email: $email)
              }
            `,
            variables: { email: this.email },
          })
          .then(({ data }) => {
            if (data.password_reset) {
              this.form_submitted = true;
            }
          });
      },
    },
  });
</script>
