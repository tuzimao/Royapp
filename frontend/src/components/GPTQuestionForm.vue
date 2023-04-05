<template>
  <div class="container">
    <h2 class="text-left">Chat with AI:</h2>
    <SystemRoleSelector
      v-if="showSystemRoleSelector"
      :disabled="disableRoleChange"
      @update-system-role="updateSystemRole"
      @role-selected="onRoleSelected"
    />
    <h3 v-else>Current Role: {{ currentRole }}</h3>
    <div class="chat-container p-3 mb-3 overflow-auto">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="`message ${message.type} p-2 mb-2 rounded text-black`"
      >
      <div v-if="message.type === 'gpt'" class="gpt-avatar">
        <!-- Add the robot SVG here -->
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 32 32"><g fill="none"><path fill="#F8312F" d="M5 3.5a1.5 1.5 0 0 1-1 1.415V12l2.16 5.487L4 23c-1.1 0-2-.9-2-1.998v-7.004a2 2 0 0 1 1-1.728V4.915A1.5 1.5 0 1 1 5 3.5Zm25.05.05c0 .681-.44 1.26-1.05 1.468V12.2c.597.347 1 .994 1 1.73v7.01c0 1.1-.9 2-2 2l-2.94-5.68L28 11.93V5.018a1.55 1.55 0 1 1 2.05-1.468Z"></path><path fill="#FFB02E" d="M11 4.5A1.5 1.5 0 0 1 12.5 3h7a1.5 1.5 0 0 1 .43 2.938c-.277.082-.57.104-.847.186l-3.053.904l-3.12-.908c-.272-.08-.56-.1-.832-.18A1.5 1.5 0 0 1 11 4.5Z"></path><path fill="#CDC4D6" d="M22.05 30H9.95C6.66 30 4 27.34 4 24.05V12.03C4 8.7 6.7 6 10.03 6h11.95C25.3 6 28 8.7 28 12.03v12.03c0 3.28-2.66 5.94-5.95 5.94Z"></path><path fill="#212121" d="M9.247 18.5h13.506c2.33 0 4.247-1.919 4.247-4.25A4.257 4.257 0 0 0 22.753 10H9.247A4.257 4.257 0 0 0 5 14.25a4.257 4.257 0 0 0 4.247 4.25Zm4.225 7.5h5.056C19.34 26 20 25.326 20 24.5s-.66-1.5-1.472-1.5h-5.056C12.66 23 12 23.674 12 24.5s.66 1.5 1.472 1.5Z"></path><path fill="#00A6ED" d="M10.25 12C9.56 12 9 12.56 9 13.25v2.5a1.25 1.25 0 1 0 2.5 0v-2.5c0-.69-.56-1.25-1.25-1.25Zm11.5 0c-.69 0-1.25.56-1.25 1.25v2.5a1.25 1.25 0 1 0 2.5 0v-2.5c0-.69-.56-1.25-1.25-1.25Z"></path></g></svg>
      </div>
      <div v-if="message.type === 'user'" class="user-avatar">
        <!-- Add the user SVG here -->
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="12" fill="#FFB74D" />
        <circle cx="8" cy="9" r="1.5" fill="#FFFFFF" />
        <circle cx="16" cy="9" r="1.5" fill="#FFFFFF" />
        <path d="M12,15c-2.7,0-4.4-1.47-4.4-2.75H16.4C16.4,13.53,14.7,15,12,15Z" fill="#FFFFFF" />
        </svg>
      </div>
        {{ message.content }}
      </div>
    </div>
    <div v-if="!isWaitingForResponse">
      <form @submit.prevent="submitQuestion" class="input-form d-flex mb-3">
        <textarea
          v-model="question"
          class="form-control me-2"
          placeholder="Type your question here..."
          required
          rows="1"
          style="resize: none;"
          @input="autoResizeTextArea"
          @keydown.enter.prevent="submitQuestion"
        ></textarea>
        <div class="button-container">
          <button type="submit" class="btn btn-primary">Submit</button>
          <button type="button" @click="resetChat" class="btn btn-secondary ms-2">
            Clear
          </button>
        </div>
      </form>
    </div>
    <div v-else class="ai-thinking-container">
      <div class="loader mr-2"></div>
      <span>While I am thinking...</span>
      <button @click="cancelRequest" class="btn btn-danger ms-2">Stop</button>
    </div>
  </div>
</template>

<script>
import SystemRoleSelector from "./SystemRoleSelector.vue";
import axios from "axios";

export default {
  computed: {
    disableRoleChange() {
      return this.messages.length > 0;
    },
  },
  components: {
    SystemRoleSelector,
  },
  data() {
    return {
      isWaitingForResponse: false,
      cancelSource: null,
      question: "",
      messages: [],
      currentRole: "Helpful Assistant",
      showSystemRoleSelector: true,
    };
  },
  methods: {
    updateSystemRole(newRole) {
      this.currentRole = newRole;
    },
    onRoleSelected() {
      this.showSystemRoleSelector = false;
    },
    async submitQuestion() {
      if (this.question.trim() === "") {
        return;
      }

      if (this.showSystemRoleSelector) {
        this.showSystemRoleSelector = false;
      }

      this.messages.push({ type: "user", content: this.question });

      try {
        this.isWaitingForResponse = true;
        this.cancelSource = axios.CancelToken.source();

        const prompt = this.messages
          .map((message, index) => `${index % 2 === 0 ? "User:" : "GPT:"} ${message.content}`)
          .join("\n") + `\nUser: ${this.question}`;

        const { data } = await axios.get("http://localhost:5000/api/gpt-response", {
          params: {
            prompt: prompt,
            systemRole: this.currentRole,
          },
          cancelToken: this.cancelSource.token,
        });
        this.messages.push({ type: "gpt", content: data.gpt_response });
      } catch (error) {
        if (!axios.isCancel(error)) {
          console.error("Failed to get response from GPT:", error);
          this.messages.push({ type: "gpt", content: "Error: Failed to get response from GPT." });
        }
      } finally {
        this.isWaitingForResponse = false;
        this.cancelSource = null;
        this.question = "";
      }
    },
    autoResizeTextArea(event) {
      event.target.style.height = "1px";
      event.target.style.height = event.target.scrollHeight + "px";
    },
    resetChat() {
      this.showSystemRoleSelector = true;
      this.messages = [];
    },
    cancelRequest() {
      if (this.cancelSource) {
        this.cancelSource.cancel("User stopped the request.");
      }
      this.isWaitingForResponse = false;
      this.question = "";
    },
  },
};
</script>

<style scoped>
.button-container {
  display: flex;
  align-items: self-start;
}
.container {
  max-width: 800px;
  margin: 0 auto;
}

.chat-container {
  max-height: 400px;
  
}

.message {
  word-wrap: break-word;
  display: flex;
  align-items: flex-start;
}

.message.user {
  background-color: #e0f3ff;
}
.user-avatar {
  margin-right: 8px;
  display: inline-flex;
}

.message.gpt {
  background-color: #f0e4ff;
}

.gpt-avatar {
  margin-right: 8px;
  display: inline-flex;
}

.ai-thinking-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.loader {
  display: inline-flex;
  margin-right: 10px;
  width: 24px;
  height: 24px;
  border: 2px solid rgba(0, 0, 0, 0.2);
  border-left-color: #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

</style>

