<template>
  <div class="login-wrapper">
    <div v-if="$store.getters.userAuthenticated">
      {{ $t("You are already logged in.") }}
    </div>
    <div v-else class="login-container">
      <form @submit.prevent="dispatchLogin">
        <label>
          Username
          <input
            v-model="username"
            autocomplete="username"
            class="form-control"
            placeholder="Username"
            type="text"
          />
        </label>
        <label>
          Password
          <input
            v-model="password"
            autocomplete="current-password"
            class="form-control"
            placeholder="Password"
            type="password"
          />
        </label>
        <button class="btn btn-primary" type="submit">
          {{ $t("Login") }}
        </button>
        <p class="mt-3 text-danger small">{{ login_failed_message }}</p>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
  import Vue from "vue";

  export default Vue.extend({
    name: "Login",
    data() {
      return {
        username: null,
        password: null,
        login_failed_message: "",
      };
    },
    created() {
      if (this.$store.getters.userAuthenticated) {
        if (this.$route.query.next)
          this.$router.push(this.$route.query.next.toString());
      }
    },
    methods: {
      dispatchLogin() {
        this.$store
          .dispatch("login", { username: this.username, password: this.password })
          .then(() => this.$router.push(this.$route.query.next.toString() || "/"))
          .catch((response) => (this.login_failed_message = response.error));
      },
    },
  });
</script>

<style scoped>
  .login-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 60vh;
  }

  .login-container {
    width: 350px;

    background: #4b4b4b;
    color: white;
    padding: 1rem;
    border-radius: 3px;
  }

  label {
    display: block;
    margin-bottom: 1rem;
  }

  input {
    display: block;
  }
</style>
