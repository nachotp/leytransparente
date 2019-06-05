window.Vue = Vue;

var ParlamentariosForm = new Vue({
    el: '#ParlamentariosForm',
    delimiters: ['[[', ']]'],
    components: {

    },
    created: function() {
        this.$store.state.form_data = JSON.parse(document.getElementsByTagName('body')[0].getAttribute('data') || '{}');
    },
    store: declaracion_data,
    filters: {
        capitalize: function(value){
            value = value.toString().toLowerCase();
            return value.charAt(0).toUpperCase() + value.slice(1);
        },
    },
    computed: {
        editable(){
            return this.$store.state.editable
        },
        form_data(){
            return this.$store.state.form_data
        },
        form_base(){
            return this.$store.state.form_base.template
        },
        get_nombre(){
            var names = this.$store.state.form_data.Datos_del_Declarante.nombre.toLowerCase().split(' ')
            var name = names[0].charAt(0).toUpperCase() + names[0].slice(1) + ' ' +
                names[1].charAt(0).toUpperCase() + names[1].slice(1);

            var ApellidoP = this.$store.state.form_data.Datos_del_Declarante.Apellido_Paterno.toLowerCase();
            ApellidoP = ApellidoP.charAt(0).toUpperCase() + ApellidoP.slice(1);

            var ApellidoM = this.$store.state.form_data.Datos_del_Declarante.Apellido_Materno.toLowerCase();
            ApellidoM = ApellidoM.charAt(0).toUpperCase() + ApellidoM.slice(1);

            return name + ' ' + ApellidoP + ' ' + ApellidoM;
        },
        get_cargo(){
            return this.$store.state.form_data.Datos_Entidad_Por_La_Que_Declara.Cargo_Funcion.nombre
        },
        get_profesion(){
            return this.$store.state.form_data.Datos_del_Declarante.Profesion_Oficio.nombre;
        },
    },
});