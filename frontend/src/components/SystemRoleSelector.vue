<template>
    <div>
      <button :disabled="disabled" @click="toggleRoleSelection">Add System Role</button>
      <div v-if="showRoleSelection" class="role-selection">
        <h5>Select a predefined role:</h5>
        <select v-model="systemRole" @change="hideRoleSelector">
          <option value="">--Select a role--</option>
          <option value="Vancouver Real Estate Advisor">Vancouver Real Estate Advisor</option>
          <option value="Doctor">Doctor</option>
          <option value="Scientist">Scientist</option>
        </select>
        <h5>Or enter a custom role:</h5>
        <input v-model="systemRole" @blur="hideRoleSelector" placeholder="Enter a custom role..." />
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      disabled: {
        type: Boolean,
        default: false,
      },
    },
    data() {
      return {
        systemRole: "Helpful Assistant",
        showRoleSelection: false,
      };
    },
    methods: {
    toggleRoleSelection() {
      this.showRoleSelection = !this.showRoleSelection;
    },
    hideRoleSelector() {
      this.showRoleSelection = false;
      this.$emit('role-selected');
    },
  },
    watch: {
      systemRole(newRole) {
        this.$emit("update-system-role", newRole);
      },
    },
  };
  </script>
  
  <style scoped>
  .role-selection {
    display: flex;
    flex-direction: column;
    margin-bottom: 10px;
  }
  </style>
  