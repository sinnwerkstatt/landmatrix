<template>
  <div>
    <PageTitle>{{ $t("Register") }}</PageTitle>

    <div
      v-if="registration_successful"
      class="flex justify-center items-center h-full w-full mb-4"
    >
      Registration successful. You can now close this window and check your emails.
    </div>
    <div v-else class="flex justify-center items-center h-full w-full mb-4">
      <div v-if="$store.getters.userAuthenticated">
        {{ $t("You are already logged in.") }}
      </div>
      <div
        v-else
        class="w-[clamp(300px,80%,900px)] p-6 rounded border-2 border-[#4b4b4b]"
      >
        {{
          $t(
            "Your contact information will help our researchers get in touch with you for additional information. We respect and protect your privacy and anonymity, and will never share or publish your personal information. You can also write us directly at data@landmatrix.org."
          )
        }}

        <form class="grid md:grid-cols-2 gap-4 my-6" @submit.prevent="register">
          <label>
            {{ $t("Username") }}
            <input
              v-model="username"
              autocomplete="username"
              class="form-control"
              placeholder="Username"
              type="text"
              required
            />
          </label>
          <label>
            {{ $t("Email") }}
            <input
              v-model="email"
              class="form-control"
              autocomplete="email"
              :placeholder="$t('Email')"
              type="email"
              required
            />
          </label>
          <label>
            {{ $t("First name") }}
            <input
              v-model="first_name"
              class="form-control"
              :placeholder="$t('First name')"
              type="text"
              required
            />
          </label>
          <label>
            {{ $t("Last name") }}
            <input
              v-model="last_name"
              class="form-control"
              :placeholder="$t('Last name')"
              type="text"
              required
            />
          </label>

          <label>
            {{ $t("Phone") }}
            <input
              v-model="phone"
              class="form-control"
              :placeholder="$t('Phone')"
              type="text"
            />
          </label>
          <label>
            {{ $t("User information") }}
            <textarea
              v-model="information"
              class="form-control"
              :placeholder="
                $t(
                  'Write something about yourself and your company. This won\'t be published.'
                )
              "
              type="text"
            />
          </label>

          <label>
            {{ $t("Password") }}
            <input
              v-model="password"
              class="form-control"
              autocomplete="new-password"
              :placeholder="$t('Password')"
              type="password"
            />
          </label>
          <label>
            {{ $t("Password confirmation") }}
            <input
              v-model="password_confirm"
              class="form-control"
              autocomplete="new-password"
              :placeholder="$t('Password confirmation')"
              type="password"
            />
          </label>
          <vue-hcaptcha
            ref="hcaptcha"
            :re-captcha-compat="false"
            :sitekey="VITE_HCAPTCHA_SITEKEY"
            @verify="captchaVerified"
          />

          <button class="btn btn-primary" type="submit" :disabled="submit_disabled">
            {{ $t("Register") }}
          </button>
          <p class="mt-3 text-danger small">{{ register_failed_message }}</p>
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
  import VueHcaptcha from "@hcaptcha/vue-hcaptcha";

  export default Vue.extend({
    name: "Register",
    components: { PageTitle, VueHcaptcha },
    data() {
      return {
        username: "",
        first_name: "",
        last_name: "",
        email: "",
        phone: "",
        information: "",
        password: "",
        password_confirm: "",
        token: "",
        submit_disabled: true,
        register_failed_message: "",
        registration_successful: false,
        VITE_HCAPTCHA_SITEKEY:
          import.meta.env.VITE_HCAPTCHA_SITEKEY ||
          "10000000-ffff-ffff-ffff-000000000001",
      };
    },
    created() {
      if (this.$store.getters.userAuthenticated) {
        if (this.$route.query.next)
          this.$router.push(this.$route.query.next.toString());
        else this.$router.push("/");
      }
    },
    methods: {
      captchaVerified(token: string) {
        this.token = token;
        this.submit_disabled = false;
      },

      async register() {
        apolloClient
          .mutate({
            mutation: gql`
              mutation Register(
                $username: String!
                $first_name: String!
                $last_name: String!
                $email: String!
                $phone: String
                $information: String!
                $password: String!
                $token: String!
              ) {
                register(
                  username: $username
                  first_name: $first_name
                  last_name: $last_name
                  email: $email
                  phone: $phone
                  information: $information
                  password: $password
                  token: $token
                ) {
                  ok
                  message
                }
              }
            `,
            variables: {
              username: this.username,
              first_name: this.first_name,
              last_name: this.last_name,
              email: this.email,
              phone: this.phone,
              information: this.information,
              password: this.password,
              token: this.token,
            },
          })
          .then(({ data }) => {
            if (data.register.ok) {
              this.registration_successful = true;
            } else {
              this.register_failed_message = data.register.message;
            }
          });
      },
    },
  });
</script>

<style scoped>
  label {
    display: block;
    margin-bottom: 1rem;
  }

  input {
    display: block;
  }
</style>
