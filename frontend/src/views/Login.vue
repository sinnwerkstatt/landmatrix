<template>
  <div class="login-wrapper">
    <div class="login-container">
      <form @submit.prevent="dispatchLogin">
        <label>
          Username
          <input
            v-model="username"
            class="form-control"
            type="text"
            autocomplete="username"
            placeholder="Username"
          />
        </label>
        <label>
          Password
          <input
            v-model="password"
            class="form-control"
            type="password"
            autocomplete="current-password"
            placeholder="Password"
          />
        </label>
        <button type="submit" class="btn btn-primary">
          {{ $t("Login") }}
        </button>
        <p class="mt-3 text-danger small">{{ login_failed_message }}</p>
      </form>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Login",
    data() {
      return {
        username: null,
        password: null,
        login_failed_message: "",
      };
    },
    computed: {},
    methods: {
      dispatchLogin() {
        this.$store
          .dispatch("login", { username: this.username, password: this.password })
          .then(() => {
            this.$router.push(this.$route.query.next);
          })
          .catch((response) => {
            this.login_failed_message = response.error;
          });
      },
    },
  };
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
