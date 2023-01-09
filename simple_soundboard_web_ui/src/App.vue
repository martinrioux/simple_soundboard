<template>
  <div id="app">
    <div class="main-section">
      <b-navbar toggleable="lg" class="navbar-dark navbar-custom">
        <b-navbar-brand style="margin-left: 15px" href="#">Simple Soundboard</b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
          <b-collapse id="nav-collapse" is-nav>
            <b-navbar-nav>
              <b-nav-item class="nav-link" :to="{name: 'Soundboard'}" exact exact-active-class="active">
                Soundboard
              </b-nav-item>
            </b-navbar-nav>
          </b-collapse>
        </b-navbar>
        <p/>
        <div class="container">
          <main>
            <router-view/>
          </main>
          <div class="by_whom">By <a href="https://martinrioux.github.io">Martin Rioux</a></div>
        </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'app',
  data: function() {
    return {
    }
  },
  created() {
    this.$store.dispatch('getConfig');
  },
}
</script>
<style>

body {
  background-image: url('./assets/wood.jpg');
  background-color: #cccccc;
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: cover;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

.navbar {
  padding: 0px !important;
}

.container {
  min-width: 90% !important;
}

.navbar-custom {
  background-color:#2b5199;
}/* change the brand and text color */

.navbar-custom .navbar-brand,
.navbar-custom .navbar-text {
    color: rgba(255,255,255,.8);
}/* change the link color */

.navbar-custom .nav-item.active .nav-link .nav-link,
.navbar-custom .nav-item:hover .nav-link .nav-link {
    color: #ffffff;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}


.by_whom {
  color: rgba(216, 216, 216, 0.8);
  margin-right: 15px;
  float: left;
}

.by_whom a {
  color: rgb(255, 255, 255);
}

.by_whom a:hover {
  color: rgb(167, 157, 255);
}


div .container {
  width: 100% !important;
}
main {
  width: 100% !important;
}

</style>
