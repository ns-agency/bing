<template>
  <div class="cover">
    <h1> Prism Help Page </h1>
    <p> Welcome to bing drive valued NSA agents! This is the set up page for new agents who want to access bing drive files</p>
    <h2> Set up </h2>
    <p> We used to have jim down on level 4 confirm all new agents but due to donald trump hiring his own son
      to take over that office we've shifted to just having a unauthenticated end point you can hit to get staff access
    </p>
    <p> We've found it's more secure, simply execute</p>
    <code>/api/secret/no/really/give_staff_access?username=test</code>
    <p>but replace <code>test</code> with your own username </p>
    <h2> Api </h2>
    <p> As a staff member you'll now have elevated access :) </p>
  </div>
</template>

<script>
export default {
  name: 'Home',
  props: {},
  methods: {

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
  flex-direction: column;
  font-family: 'Montserrat', sans-serif;
}
p {
  width: 80%;
  margin-left: 5%;
  color: #777;
}
h1,h3 {
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
h2 {
  width: 80%;
  text-align: left;
  border-bottom: none;
}
code {
  color: #42b983;
}
</style>
