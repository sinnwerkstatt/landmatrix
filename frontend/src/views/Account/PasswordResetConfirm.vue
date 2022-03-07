<template>
  <div>
    <PageTitle>{{ $t("Enter new password") }}</PageTitle>
    <div class="flex justify-center items-center h-full w-full mb-4">
      <div class="w-[clamp(300px,80%,600px)] p-6 rounded border-2 border-[#4b4b4b]">
        <div v-if="form_submitted">
          If your email-address is registered with LandMatrix you should receive an
          email shortly
        </div>
        <form v-else @submit.prevent="submit">
          <label class="block">
            {{ $t("Password") }}
            <input
              v-model="new_password1"
              class="form-control"
              autocomplete="new-password"
              :placeholder="$t('Password')"
              type="password"
            />
          </label>
          <label class="block">
            {{ $t("Password confirmation") }}
            <input
              v-model="new_password2"
              class="form-control"
              autocomplete="new-password"
              :placeholder="$t('Password confirmation')"
              type="password"
            />
          </label>
          <button class="btn btn-primary block" type="submit">
            {{ $t("Set password") }}
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
    name: "PasswordResetConfirm",
    components: { PageTitle },
    props: {
      token: { type: [String], required: true },
    },
    data() {
      return {
        new_password1: "",
        new_password2: "",
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
              mutation ($token: String!, $np1: String!, $np2: String!) {
                password_reset_confirm(
                  token: $token
                  new_password1: $np1
                  new_password2: $np2
                )
              }
            `,
            variables: {
              token: this.token,
              np1: this.new_password1,
              np2: this.new_password2,
            },
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
