var ParlamentariosForm = {
    template: `
    <div class="container">
            <b-card no-body>
                <b-card-body>
                    <b-card-title><h2>[[get_nombre]]</h2></b-card-title>
                    <b-card-sub-title class="mb-2"><h4>[[get_cargo|capitalize]]</h4></b-card-sub-title>
                    <b-card-text>Asume el cargo : [[get_fechacargo]]<br>
                        Región: [[get_region|capitalize]]<br>
                        Comuna: [[get_comuna|capitalize]]</b-card-text>
                </b-card-body>

                <b-list-group flush>
                    <b-list-group-item>Profesión: [[get_profesion|capitalize]]<br>
                    Estado Civil: [[get_estadoc|capitalize]]<br>
                    Regimen Patrimonial: [[get_regimenp|capitalize]] </b-list-group-item>
                </b-list-group>
            </b-card>
            <p></p>
            <b-card no-body>
                <b-card-body>
                    <b-card-title><h2>Declaración de patrimonio</h2></b-card-title>
                    <b-card-sub-title class="mb-2"><h4>Fecha de declaración: [[get_fechadecla]]</h4></b-card-sub-title>
                </b-card-body>

                <b-list-group flush>
                    <b-list-group-item>Tipo de declaración: [[form_data.Tipo_Declaracion.nombre|capitalize]]<br>
                    Region: [[form_data.Datos_Entidad_Por_La_Que_Declara.Region_Desempeno_Chile.nombre|capitalize]]<br>
                    Comuna: [[form_data.Datos_Entidad_Por_La_Que_Declara.Comuna_Desempeno_Chile.nombre|capitalize]]<br>
                    Renta Mensual: [[form_data.Datos_Entidad_Por_La_Que_Declara.Grado_Renta_Mensual|capitalize]]</b-list-group-item>
                    <!--b-list-group-item v-for="(item,key,index) in form_data" :key="key">[[key]]: [[item]]</b-list-group-item-->
                    
                    <b-card no-body class="mb-1">
                        <b-card-header header-tag="header" class="p-1" role="tab">
                            <b-button block href="#" v-b-toggle.Derechos_o_acciones variant="info">Derechos o acciones en Chile</b-button>
                        </b-card-header>
                        <b-collapse id="Derechos_o_acciones" accordion="AccDerechos" role="tabpanel">
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
                     
                    <b-card no-body class="mb-1">
                        <b-card-header header-tag="header" class="p-1" role="tab">
                            <b-button block href="#" v-b-toggle.Bienes_Inmuebles_Situados_En_Chile variant="info">Bienes inmuebles situados en Chile</b-button>
                        </b-card-header>
                        <b-collapse id="Bienes_Inmuebles_Situados_En_Chile" accordion="AccBienes" role="tabpanel">
                            <b-list-group flush v-for="(bien,index) in getBienesChile" :key="index">
                                <b-list-group-item>
                                    <h5>
                                    [[bien.Direccion|capitalize|capitalize]], [[bien.Comuna.nombre|capitalize]], Región [[bien.Region.nombre|capitalize]]<br></h5>
                                    Forma de la propiedad: [[bien.Forma_Propiedad.nombre|capitalize]]<br>
                                    Conservador bienes raices: [[bien.Conservador_Bienes_Raices.nombre|capitalize]]<br>
                                    Avalúo Fiscal: $[[bien.Avaluo_Fiscal|number]]<br>
                                    ¿Es su domicilio?: [[bien.Es_Su_Domicilio|yesNo]]<br>
                                    Año del inmueble: [[bien.Annio|number]]<br>
                                    Fecha de adquisición: [[bien.Fecha_Adquisicion|dateOnly]]<br>
                                </b-list-group-item>
                            </b-list-group>
                        </b-collapse>
                     </b-card>
                     
                    <b-card no-body class="mb-1">
                        <b-card-header header-tag="header" class="p-1" role="tab">
                            <b-button block href="#" v-b-toggle.Vehiculos_motorizados variant="info">Vehículos motorizados</b-button>
                        </b-card-header>
                        <b-collapse id="Vehiculos_motorizados" accordion="VehiculosMotorizados" role="tabpanel">
                            <b-list-group flush v-for="(auto, index) in getVehiculos" :key="index">
                                <b-list-group-item>
                                    <h5>[[auto.Marca.nombre|capitalize]] [[auto.Modelo|capitalize]], [[auto.Annio_Fabricacion]]</h5>
                                    Avalúo Fiscal: $[[auto.Avaluo_Fiscal|number]]<br>
                                    Año de inscripción vehículo: [[auto.Annio_Inscripcion]]<br>
                                    Número de inscripción: [[auto.Numero_Inscripcion]]<br>
                                </b-list-group-item>
                            </b-list-group>
                        </b-collapse>
                     </b-card>
                     
                    <b-card no-body class="mb-1">
                        <b-card-header header-tag="header" class="p-1" role="tab">
                            <b-button block href="#" v-b-toggle.Datos_Conyuge variant="info">Datos del Conyuge</b-button>
                        </b-card-header>
                        <b-collapse id="Datos_Conyuge" accordion="DatosConyuge" role="tabpanel">
                            <b-list-group flush>
                                <b-list-group-item>
                                    <div v-for="actividad in form_data.Actividades_Profesionales_Conyuge">
                                    <h5>[[get_nombreConyuge]]</h5>
                                    <b-list-group-item>
                                    Tipo de actividad: [[actividad.Tipo_Actividad.nombre|capitalize]]<br>
                                    Rubro: [[actividad.Rubro.nombre|capitalize]]<br>
                                    Fecha de inicio: [[actividad.Fecha_Inicio|dateOnly]]<br>
                                    Clasificación: [[actividad.Clasificacion.nombre|capitalize]]<br>
                                    Nombre Razón Social: [[actividad.Nombre_Razon_Social|capitalize]]
                                    </b-list-group-item>
                                    </div>
                                </b-list-group-item>
                            </b-list-group>
                        </b-collapse>
                     </b-card>
                     
                    <b-card no-body class="mb-1">
                        <b-card-header header-tag="header" class="p-1" role="tab">
                            <b-button block href="#" v-b-toggle.Parientes variant="info">Parientes</b-button>
                        </b-card-header>
                        <b-collapse id="Parientes" accordion="Parientes" role="tabpanel">
                            <b-list-group flush v-for="(pariente, index) in form_data.Datos_Parientes" :key="index">
                                <b-list-group-item>
                                    <h5>[[pariente.nombre|name]] [[pariente.Apellido_Paterno|capitalize]]</h5>
                                    Parentezco: [[pariente.Parentesco.nombre|capitalize]]<br>
                                    Fecha de nacimiento: [[pariente.Fecha_Nacimiento|dateOnly]]
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
        capitalize: function (value) {
            if (value !== undefined)
                value = value.toString().toLowerCase();
                return value.charAt(0).toUpperCase() + value.slice(1);
        },
        dateOnly: function (value) {
            if (value !== undefined)
                return value.split(' ')[0];
            else
                return "No hay información";
        },
        yesNo: function (value) {
            return (value || value === "Si") ? 'Si' : 'No'
        },
        number: function (value) {
            return parseInt(value, 10).toLocaleString('es')
        },
        name: function (value) {
            value = value.toLowerCase().split(' ')
            var name = '';
            for (let i = 0; i < value.length; i++) {
                name += value[i].charAt(0).toUpperCase() + value[i].slice(1) + ' ';
            }
            return name;
        },
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
            var name = '';
            for (let i = 0; i < names.length; i++) {
                name += names[i].charAt(0).toUpperCase() + names[i].slice(1) + ' ';
            }
            var ApellidoP = this.$store.state.form_data.Datos_del_Declarante.Apellido_Paterno.toLowerCase();
            ApellidoP = ApellidoP.charAt(0).toUpperCase() + ApellidoP.slice(1);

            var ApellidoM = this.$store.state.form_data.Datos_del_Declarante.Apellido_Materno.toLowerCase();
            ApellidoM = ApellidoM.charAt(0).toUpperCase() + ApellidoM.slice(1);

            return name + ' ' + ApellidoP + ' ' + ApellidoM;
        },
        get_nombreConyuge(){
            var names = this.$store.state.form_data.Datos_del_Conyuge.nombre.toLowerCase().split(' ')
            var name = '';
            for (let i = 0; i < names.length; i++) {
                name += names[i].charAt(0).toUpperCase() + names[i].slice(1) + ' ';
            }
            var ApellidoP = this.$store.state.form_data.Datos_del_Conyuge.Apellido_Paterno.toLowerCase();
            ApellidoP = ApellidoP.charAt(0).toUpperCase() + ApellidoP.slice(1);

            var ApellidoM = this.$store.state.form_data.Datos_del_Conyuge.Apellido_Materno.toLowerCase();
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
        getBienesChile(){
            return this.$store.state.form_data.Bienes_Inmuebles_Situados_En_Chile;
        },
        getVehiculos(){
            return this.$store.state.form_data.Vehiculos_Motorizados;
        }
    },
};