<template>
    <div class="cover">
        <div class="navbar">
            <h2> {{username}}'s Files </h2>
            <br>
            <div class="detail">
                <i class="material-icons">account_circle</i>
                <span> {{role}} </span>
            </div>
            <br>
            <br>
            <span class="label"> New file</span><br>
            <span class="label"> max 64 chars per file</span><br>
            <input type="text" class="name" v-model="name"/>
            <textarea v-model="text" class="new-file" type="text" :class="{ invalid: text.length > 64}"/>
                <span class="label red">{{postErr}}</span><br>
                <div class="action">
                    <button class="btn" type="button" @click="upload()" :class="{ invalid: text.length > 64}">Create</button>  
                </div>
                <br>
                <div class="detail red" @click="logout()">
                    <i class="material-icons">exit_to_app</i>
                    <span> Log out </span>
                </div>
        </div>
        <div class="files">
            <div class="folder" v-for="e in files" :key="e.name" @click="redirect(e.name)">
                <i class="material-icons">description</i>
                <span> {{e.name}} </span>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Home',
    props: {},
    data: () => {return {
        username: "carey",
        role: "User",
        files: [],
        text: "sample text",
        name: "new_file",
        postErr: ""
    }},
    mounted() {
        fetch("/me", {credentials: 'include'}).then(r=>r.json()).then(r=>{
            this.username = r.username;
            this.files = r.files;
            this.role = r.role;
        });
    },
    methods: {
        logout() {
            fetch("/logout",{method:"POST", credentials: 'include'}).then(this.$router.push('login'))
        },
        redirect(name) {
            fetch("/me", {credentials: 'include'}).then(r=>r.json()).then(r=>{
                window.location.href = `/document/${name}?r=${btoa(r.username)}`;
            })
        },
        upload() {
            if (this.text.length > 64) {
                return;
            }
            fetch("/upload",{
                method: "POST",
                credentials: 'include',
                body: JSON.stringify({name: this.name, text:this.text}),
                headers: {'Content-Type': 'application/json'}
            })
                .then((r) => {
                    if (r.status === 200) {
                        fetch("/me").then(r=>r.json()).then(r=>{
                            this.files = r.files;
                        });
                        this.postErr = "";
                    } else {
                        r.text().then((t)=>{
                            this.postErr = t;
                        });
                    }
                })
        }
    },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.name {
    width: calc(100% - 4rem);
    padding: 0.5rem 1rem 0.5rem 1rem;
    border-radius: 10px;
    border: 2px solid #EBEBEB;
    color: #444;
    margin: 1rem;
}
.name:focus {
    outline: none;
    border: 2px solid #42b983;
}

.cover {
    width: 100vw;
    height: 100vh;
    background: #FAFAFA;
    display: flex;
    align-items: center;
    justify-content: center;
}
.navbar {
    width: 300px;
    height: 100%;
    background: white;
    box-shadow:  0 3px 6px rgba(0,0,0,0.16);
    border-radius: 5px;
}

.files {
    width: calc(100% - 300px - 4rem);
    height: calc(100% - 4rem);
    padding: 2rem;
    display: flex;
    align-items: flex-start;
    flex-direction: row;
}

.navbar h2 {
    width: 80%;
    margin-left: 10%;
    margin-right: 10%;
    padding-bottom: 1rem;
    text-align: center;
    color: #444;
    font-family: 'Montserrat', sans-serif;
    font-weight: 400;
    margin-top: 2rem;
    border-bottom: 2px solid #EBEBEB;
}

.navbar .detail {
    margin-left: 10%;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    flex-direction: row;
}

.navbar .detail i {
    color: #BBB;
}

.navbar .detail span {
    margin-left: 1rem;
    font-family: 'Montserrat', sans-serif;
    color: #777;
}
.navbar .detail.red i{
    color: rgb(251, 75, 78);
    cursor: pointer;
}
.navbar .detail.red span{
    color: rgb(251, 75, 78);
    cursor: pointer;
}
.red {
    color: rgb(251, 75, 78) !important;
}
.files i {
    color: #BBB;
    font-size: 4rem;
    margin-left: 1rem;
    margin-right: 1rem;
    border-radius: 50%;
}
.folder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}
.folder i:hover {
    color: #42b983;
}
.folder i.disabled:hover {
    color: #BBB;
}
.folder span {
    font-family: 'Montserrat', sans-serif;
    color: #777;
    font-size: 0.8rem;
    margin-top: 0.5rem;
}
.v--modal-overlay {
    border-radius: 15px;
}

.wrapper {
    padding: 1rem;
}
.wrapper p {
    font-family: 'Montserrat', sans-serif;
    color: #777;
    width: 100%;
}
.new-file {
    width: calc(100% - 3rem);
    border: 2px solid #EBEBEB;
    height: 5rem;
    margin-left: 1rem;
    margin-right: 1rem;
    border-radius: 10px;
    padding: 0.5rem;
    color: #777;
    resize: none;
}

.new-file.invalid {
    border: 2px solid rgb(251, 75, 78);
}

.new-file:focus {
    outline: none;
}

.label {
    margin-left: 1.3rem;
    color: #BBB;
    font-family: 'Montserrat', sans-serif;
    font-size: 0.8rem;
    margin-top: 0.5rem;
    text-emphasis: em;
}
.action {
    width: calc(100% - 4rem);
    margin-top: 1rem;
    align-items: center;
    justify-content: flex-end;
    display: flex;
    margin-left: 2rem;
    margin-right: 2rem;
}
.btn {
    background: #42b983;
    color: white;
    border-radius: 15px;
    padding: 0.5rem 1rem 0.5rem 1rem;
    border: none;
    cursor: pointer;
}
.btn.invalid {
    background: #EBEBEB;
    cursor: default;
}
.btn:hover {
    box-shadow:  0 3px 6px rgba(0,0,0,0.16);
}
.btn.invalid:hover {
    box-shadow:  none;
}
.btn:focus {
    outline: none;
}
</style>
