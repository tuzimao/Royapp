<template>
    <div class="role-selection-wrapper">
     <div>
      <button
          :disabled="disabled"
          @click="toggleRoleSelection"
          class="role-toggle-btn"
        >
        {{ showRoleSelection ? "- Back" : "+ Advance Options" }}
      </button>
        <div v-if="showRoleSelection" class="role-selection">
          <span class="predefine-role-text">Select a predefined role:</span>
          <div class="tag-container">
            <div
              v-for="role in predefinedRoles"
              :key="role"
              class="tag"
              :class="{ selected: systemRole === role }"
              @click="selectRole(role)"
            >
              {{ role }}
            </div>
          </div>
          <span class="predefine-role-text">Or enter a custom role:</span>
          <div class="set-container">
            <input v-model="systemRole" @change="hideRoleSelector" class="custom-role-input" placeholder="Enter a custom role..." />
            <button @click="setSystemRole" class="set-container-btn">Set</button>
          </div>
        </div>
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
          predefinedRoles: [
            "Vancouver Real Estate Advisor",
            "Doctor",
            "Scientist",
            "My Angry Girlfriend!",
          ],
        };
      },
      methods: {
        toggleRoleSelection() {
          this.showRoleSelection = !this.showRoleSelection;
        },
        hideRoleSelector() {
          this.showRoleSelection = false;
          this.$emit("update-system-role", this.systemRole);
          this.$emit("role-selected");
        },
        selectRole(role) {
          console.log("Role selected:", role);
          this.systemRole = role;
          this.hideRoleSelector();
        },
        setSystemRole() {
          this.hideRoleSelector();
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
  
  .role-toggle-btn {
      background-color: transparent;
      color: #3498db;
      border: none;
      cursor: pointer;
      outline: none;
    }
    .predefine-role-text {
      margin-bottom: 10px;
    }
    .role-selection {
      display: flex;
      flex-direction: column;
      margin-bottom: 10px;
      margin-top: 20px;
      align-items: flex-start;
    }
    .role-selection-wrapper {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      margin-left: 0;
    }
    .tag-container {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 10px;
    }
    .tag {
      background-color: #3498db;
      color: #ffffff;
      padding: 4px 8px;
      border-radius: 5px;
      cursor: pointer;
      user-select: none;
      transition: background-color 0.3s;
    }
    .tag.selected {
      background-color: #2980b9;
    }
    .tag:hover {
      background-color: #2980b9;
    }
    .set-container {
      display: flex-start;
      gap: 8px;
      text-align: center;
      align-items: center;
    }
  
    .set-container input {
      height: 32px;
    }
  
    .set-container-btn {
      margin-left: 8px;
      color: #3498db;
      background-color: #ffffff;
      padding: 4px 8px;
      border-radius: 5px;
      cursor: pointer;
      user-select: none;
      transition: background-color 0.3s;
      border: none;
    }
    .set-container-btn:hover {
      color: #2980b9;
    }
    .custom-role-input {
      text-align: center;
      border-top: none;
      border-left: none;
      border-right: none;
      outline: none;
    }
    
    </style>
    