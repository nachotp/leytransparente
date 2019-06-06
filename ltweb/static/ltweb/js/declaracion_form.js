var ParlamentariosForm = {
    template: `
    <div class="container">
            <b-card no-body>
                <b-card-body>
                    <b-card-title><h2>[[get_nombre]]</h2></b-card-title>
                    <b-card-sub-title class="mb-2"><h4>[[get_cargo|capitalize]]</h4></b-card-sub-title>
                    <b-card-text>
                        <h6>Asume el cargo : [[get_fechacargo]]<br>
                        Región: [[get_region|capitalize]]<br>
                        Comuna: [[get_comuna|capitalize]]<br>
                        </h6>
                    </b-card-text>
                </b-card-body>

                <b-list-group flush>
                    <b-list-group-item>Profesión: [[get_profesion|capitalize]]</b-list-group-item>
                    <b-list-group-item>Estado Civil: [[get_estadoc|capitalize]]</b-list-group-item>
                    <b-list-group-item>Regimen Patrimonial: [[get_regimenp|capitalize]] </b-list-group-item>
                </b-list-group>
            </b-card>
            <p></p>
            <b-card no-body>
                <b-card-body>
                    <b-card-title><h2>Declaración de patrimonio</h2></b-card-title>
                    <b-card-sub-title class="mb-2"><h4>Fecha de declaración: [[get_fechadecla]]</h4></b-card-sub-title>
                </b-card-body>

                <b-list-group flush>
                    <b-list-group-item>Tipo de declaración: [[form_data.Tipo_Declaracion.nombre|capitalize]]</b-list-group-item>
                    <b-list-group-item>Region: [[form_data.Datos_Entidad_Por_La_Que_Declara.Region_Desempeno_Chile.nombre|capitalize]]</b-list-group-item>
                    <b-list-group-item>Comuna: [[form_data.Datos_Entidad_Por_La_Que_Declara.Comuna_Desempeno_Chile.nombre|capitalize]]</b-list-group-item>
                    <b-list-group-item>Renta Mensual: [[form_data.Datos_Entidad_Por_La_Que_Declara.Grado_Renta_Mensual|capitalize]]</b-list-group-item>
                    <!--b-list-group-item v-for="(item,key,index) in form_data">[[key]]: [[item]]</b-list-group-item-->
                    
                    <b-card no-body class="mb-1">
                        <b-card-header header-tag="header" class="p-1" role="tab">
                            <b-button block href="#" v-b-toggle.Derechos_o_acciones variant="info">Derechos o acciones en Chile</b-button>
                        </b-card-header>
                        <b-collapse id="Derechos_o_acciones" accordion="my-accordion" role="tabpanel">
                            <b-list-group flush v-for="(derecho,index) in getDerechos" :key="index">
                                <b-list-group-item>
                                    <h5>[[derecho.Nombre_Razon_Social|capitalize]]</h5>
                                    Tipo: [[derecho.Titulo_Derecho_Accion.nombre|capitalize]]<br>
                                    Porcentaje de pertenencia: [[derecho.Cantidad_Porcentaje]]%<br>
                                    Rut: [[derecho.RUT]]<br>
                                    Rubro: [[derecho.Giro_Registrado_SII|capitalize]]<br>
                                    Fecha de adquisición: [[derecho.Fecha_Adquisicion|dateOnly]]<br>
                                    ¿Calidad de Controlador?: [[derecho.Tiene_Calidad_Controlador|yesNo]]
                                </b-list-group-item>
                            </b-list-group>
                        </b-collapse>
                     </b-card>

                </b-list-group>
            </b-card>
        </div>
    `,
    delimiters: ['[[', ']]'],
    data: function() {
        return {}
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
        dateOnly: function (value) {
            return value.split(' ')[0];
        },
        yesNo: function (value) {
            return (value || value === "Si") ? 'Si' : 'No'
        }
    },
    computed: {
        get_editable(){
            return this.$store.state.editable;
        },
        form_data(){
            return this.$store.state.form_data;
        },
        form_base(){
            return this.$store.state.form_base.template;
        },
        get_state(){
            return this.$store.state;
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
        get_estadoc(){
            return this.$store.state.form_data.Datos_del_Declarante.Estado_Civil.nombre;
        },
        get_regimenp(){
            return this.$store.state.form_data.Datos_del_Declarante.Regimen_Patrimonial.nombre;
        },
        get_fechacargo(){
            return this.$store.state.form_data.Datos_Entidad_Por_La_Que_Declara.Fecha_Asuncion_Cargo.split(' ')[0];
        },
        get_regiondesempeno(){
            return this.$store.state.form_data.Datos_Entidad_Por_La_Que_Declara.Region_Desempeno_Chile.nombre;
        },
        get_region(){
            return this.$store.state.form_data.Region.nombre;
        },
        get_comuna(){
            return this.$store.state.form_data.Comuna.nombre;
        },
        get_fechadecla(){
            return this.$store.state.form_data.Fecha_de_la_Declaracion.split(' ')[0];
        },
        getDerechos(){
            return this.$store.state.form_data.Derechos_Acciones_Chile;
        },
        getFechaAdquisicionDerecho(){
            return this.$store.state.form_data.Derechos_Acciones_Chile.Fecha_Adquisicion;
        },
    },
};