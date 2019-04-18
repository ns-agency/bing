<template>
  <div class="cover">
    <div class="flasher">
      <div class="circle" id="circle"></div>
    </div>
    <div class="login-card">
      <img src="./../assets/image.png"/>
      <div class="form">
        <div class="input">
          <i>{{usernameError}}</i>
          <input v-model="username" type="text" placeholder="Username"/>
        </div>
        <div class="input">
          <i>{{passwordError}}</i>
          <input v-model="password" type="password" placeholder="Password"/>
        </div>
      </div>
      <div class="action">
        <button type="button" @click="login()">Login</button>
        <button type="button" @click="register()">Register</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  props: {},
  data: () => {return {
    usernameError: "",
    passwordError: "",
    password: "",
    username: ""
  }},
  methods: {
    flash(type,msg) {
      if(type === 'success') document.getElementById("circle").style.background = "#42b983"
      else document.getElementById("circle").style.background = "rgb(251, 75, 78)"
      document.getElementById("circle").classList.add("expand");
      window.setTimeout(()=>{
        document.getElementById("circle").classList.remove("expand");
        this.usernameError = msg;
      },800);
    },
    login() {
      fetch("/login",{
        method: "POST",
        credentials: "include",
        body: JSON.stringify({username: this.username, password: this.password}),
        headers: {'Content-Type': 'application/json'}
      })
      .then((r) => {
        if (r.status === 200) {
          this.flash('success')
          window.setTimeout(()=>this.$router.push('/'),1000)
        } else {
          this.flash('error', 'Invalid username/password')
        }
      })
    },
    register() {
      fetch("/register",{
        method: "POST",
        credentials: "include",
        body: JSON.stringify({username: this.username, password: this.password}),
        headers: {'Content-Type': 'application/json'}
      })
      .then((r) => {
        if (r.status === 200) {
          this.flash('success')
          window.setTimeout(()=>this.$router.push('/'),1000)
        } else {
          this.flash('error', 'Username Taken')
        }
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.cover {
  width: 100vw;
  height: 100vh;
  background: #FAFAFA;
  display: flex;
  align-items: center;
  justify-content: center;
}
@keyframes blow {
  0% {
    width: 10px;
    height: 10px;
    opacity: 1;
  }
  100% {
    width: 1000px;
    height: 1000px;
    opacity: 0;
  }
}
.expand {
  width: 10px;
  height: 10px;
  opacity: 1;
  animation: blow 0.8s;
}

.circle {
  background: rgb(251, 75, 78);
  width: 10px;
  border-radius: 50%;
  z-index: 10;
}
.flasher {
  width: 100vw;
  height: 100vh;
  position: absolute;
  top: 0;
  left: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}
.login-card {
  width: 400px;
  height: 400px;
  border-radius: 10px;
  background: white;
  box-shadow:  0 3px 6px rgba(0,0,0,0.16);
  display: flex;
  padding: 1rem;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  z-index: 20;
}
.login-card img {
  width: 80%;
  opacity: 0.2;
}
a {
  color: #42b983;
}
.form {
  margin-top: 3rem;
  display: flex;
  flex-direction: column;
  height: 40%;
  width: 80%;
  align-items: center;
  justify-content: space-around;
}
.input {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.input i {
  margin-bottom: 0.5rem;
  text-align: left;
  width: 100%;
  font-size: 0.7rem;
  color: rgba(251, 75, 78, 0.8);  
  font-family: system-ui;
  height: 0.7rem;
}
.form input {
  width: 100%;
  padding: 0.5rem 1rem 0.5rem 1rem;
  border-radius: 10px;
  border: 2px solid #EBEBEB;
  color: #444;
}
.form input:focus {
  outline: none;
  border: 2px solid #42b983;
}
.action {
  width: 80%;
  margin-top: 2rem;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-around;
}
.action button {
  background: #42b983;
  color: white;
  border-radius: 15px;
  padding: 0.5rem 1rem 0.5rem 1rem;
  border: none;
  cursor: pointer;
}
.action button:hover {
  box-shadow:  0 3px 6px rgba(0,0,0,0.16);
}
.action button:focus {
  outline: none;
}
</style>
