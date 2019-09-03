Vue.use(window.VueResource);

var app1 = new Vue({
      el: '#dropdown-1',
      methods: {
          onChange(event) {
              console.log(event.target.value);
              var value = event.target.value
              alert(value)
              $("#myDIV *").filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
              })
          }
      }
    })