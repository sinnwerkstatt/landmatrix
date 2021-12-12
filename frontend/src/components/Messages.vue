<template>
  <div v-if="msg" class="messages-overlay" @click="removeMessage(msg)">
    <div class="scroll-container">
      <div class="message-container" @click.stop>
        <div role="alert" class="alert" :class="map_level(msg)">
          <button
            type="button"
            class="close"
            aria-label="Close"
            @click="removeMessage(msg)"
          >
            <span aria-hidden="true">&times;</span>
          </button>
          <h1 class="title">
            {{ msg.title }}
          </h1>
          <div v-html="msg.text"></div>
          <div v-if="msg.allow_users_to_hide" class="actions">
            <div class="custom-control custom-checkbox">
              <input
                id="acc-checkbox"
                ref="acc-checkbox"
                type="checkbox"
                class="form-check-input custom-control-input"
              />
              <label for="acc-checkbox" class="form-check-label custom-control-label">
                Don't show this message again
              </label>
            </div>
            <button
              type="button"
              class="btn btn-primary acknowledge"
              @click="acknowledgeMessage(msg)"
            >
              Ok
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script lang="ts">
  import Cookies from "js-cookie";
  import Vue from "vue";

  export default Vue.extend({
    name: "Messages",
    data() {
      return {
        acknowledgedMessages: JSON.parse(Cookies.get("acknowledgedMessages") || "[]"),
      };
    },
    computed: {
      messages() {
        if (
          document.referrer &&
          document.referrer.startsWith(
            window.location.protocol + "//" + window.location.hostname
          )
        ) {
          // dont display messages when coming from internal referer
          return [];
        } else {
          return this.$store.state.messages.filter(
            (x) => !this.acknowledgedMessages.includes(x.id)
          );
        }
      },
      msg() {
        return this.messages.length > 0 ? this.messages[0] : null;
      },
    },
    methods: {
      map_level(msg) {
        if (!msg.level) return "alert-info";
        if (msg.level === "error") return "alert-danger";
        return `alert-${msg.level}`;
      },
      removeMessage(msg) {
        this.$store.commit(
          "setMessages",
          this.messages.filter((m) => m.id !== msg.id)
        );
      },
      acknowledgeMessage(msg) {
        if (msg.allow_users_to_hide && this.$refs["acc-checkbox"].checked) {
          this.$refs["acc-checkbox"].checked = false;
          this.acknowledgedMessages.push(msg.id);
          Cookies.set("acknowledgedMessages", this.acknowledgedMessages, {
            sameSite: "lax",
            expires: 365,
          });
        } else {
          this.removeMessage(msg);
        }
      },
    },
  });
</script>
<style lang="scss" scoped>
  .messages-overlay {
    position: fixed;
    top: 0;
    width: 100vw;
    height: 100vh;
    z-index: 9999;
    background-color: rgba(black, 0.3);
    backdrop-filter: blur(3px);
    overflow-y: auto;
  }

  .scroll-container {
    min-height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: transparent;
  }

  .message-container {
    background-color: transparent;
    width: 70vw;
    max-width: 800px;
    min-width: 300px;
    top: 0;

    @media screen and (max-width: 768px) {
      width: 85vw;
    }
    @media screen and (max-width: 600px) {
      width: 100vw;
    }

    .alert {
      margin: 0;
      padding: 1.8em;
      box-shadow: 0 0 15px rgba(black, 0.5);

      h1 {
        font-size: 2rem;
        font-weight: normal !important;
        color: black;
        text-align: left;
        text-transform: none;

        &:before {
          content: none;
        }
      }

      button.close {
        margin-top: -2rem;
        margin-right: -1.4rem;
        font-size: 2.7rem;
      }

      .actions {
        margin-top: 1.5em;
        display: flex;
        justify-content: space-between;

        button.btn-primary {
          flex-grow: 0;
          color: white;
          margin-left: auto;

          &:hover {
            background-color: transparent;
            color: var(--color-lm-orange);
            border-color: var(--color-lm-orange);
            opacity: 1;
          }
        }
      }

      &.alert-info {
        color: var(--color-lm-dark);
        border-color: var(--color-lm-orange);
        background-color: white;

        button.close {
          color: var(--color-lm-dark);
        }
      }

      &.alert-danger {
        color: black;
        border-color: var(--color-lm-orange);
        background-color: #fff;

        h1 {
          color: var(--color-lm-orange);
        }

        button.close {
          color: var(--color-lm-orange);
        }
      }

      &.alert-warning {
        background-color: #fff;
        color: var(--color-lm-dark);
      }
    }
  }
</style>
