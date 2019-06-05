window.Vue = Vue;

var ParlamentariosForm = new Vue({
    el: '#ParlamentariosForm',
    delimiters: ['[[', ']]'],
    components: {

    },
    store: declaracion_data,
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
        edit_form(form){
            updateForm(this.$store.state, form)
        },
    },
});