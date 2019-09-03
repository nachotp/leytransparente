const ParlamentariosForm = {
    template: `
    <div class="container mw-75">
            <b-card no-body class="mb-4">
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
<!--            <b-list-group-item v-for="(item,key,index) in form_data" :key="key">[[key]]: [[item]]</b-list-group-item>-->
        
            <b-row
            align-h="center"
            class="text-center mw-100"
            style="margin-left: 0px;
            margin-right: 0px;">
            
                <b-col v-bind="multipleCols" :style="leftPad">
                    <b-card no-body>
                    
                        <b-card-title class="mb-1 mt-1"><h4>Bienes inmuebles situados en Chile</h4></b-card-title>
                        <b-list-group-item>
                            <div v-if="getBienesChile">Cantidad de bienes: [[ getBienesChile.length ]]<br>
                            Avalúo Fiscal total: $ [[AvaluoTotal(getBienesChile)|number]]</div>
                            <div v-else>No hay información</div>
                        </b-list-group-item>
                        
                        <b-button v-if="getBienesChile" variant="dark" v-b-modal.ModalBienesChile>Más info</b-button>
                        <b-button v-else variant="dark" disabled>Más info</b-button>
                        
                        <b-modal id="ModalBienesChile" scrollable size="lg" title="Bienes en Chile">
                        
                            <b-list-group flush >
                                <b-list-group-item v-for="(bien,index) in getBienesChile" :key="index">
                                    <h5>[[bien.Direccion|capitalize|capitalize]], [[bien.Comuna.nombre|capitalize]], Región [[bien.Region.nombre|capitalize]]</h5>
                                    Forma de la propiedad: [[bien.Forma_Propiedad.nombre|capitalize]]<br>
                                    Conservador bienes raices: [[bien.Conservador_Bienes_Raices.nombre|capitalize]]<br>
                                    Avalúo Fiscal: $[[bien.Avaluo_Fiscal|number]]<br>
                                    ¿Es su domicilio?: [[bien.Es_Su_Domicilio|yesNo]]<br>
                                    Año del inmueble: [[bien.Annio|number]]<br>
                                    Fecha de adquisición: [[bien.Fecha_Adquisicion|dateOnly]]<br>
                                </b-list-group-item>
                            </b-list-group>
                            
                            <template slot="modal-footer" slot-scope="{ok}">
                                <b-button size="lg" variant="dark" @click="ok()">
                                    Cerrar
                                </b-button>
                            </template>
                        </b-modal>
                        
                    </b-card>
                </b-col>
                
                <b-col v-bind="multipleCols" :style="rightPad">
                
                    <b-card no-body>
                        <b-card-title class="mb-1 mt-1"><h4>Vehiculos motorizados</h4></b-card-title>
                        <b-list-group-item>
                            <div v-if="getVehiculos">Cantidad de vehículos: [[ getVehiculos.length ]]<br>
                            Avalúo Fiscal total: $ [[AvaluoTotal(getVehiculos)|number]]</div>
                            <div v-else>No hay información</div>
                        </b-list-group-item>
                        
                        <b-button v-if="getVehiculos" variant="dark" v-b-modal.ModalVehiculos>Más info</b-button>
                        <b-button v-else variant="dark" disabled>Más info</b-button>
                        
                        <b-modal id="ModalVehiculos" scrollable size="lg" title="Vehiculos motorizados">
                        
                            <b-list-group flush>
                                <b-list-group-item v-for="(auto, index) in getVehiculos" :key="index">
                                    <h5>[[auto.Marca.nombre|capitalize]] [[auto.Modelo|capitalize]], [[auto.Annio_Fabricacion]]</h5>
                                    Avalúo Fiscal: $[[auto.Avaluo_Fiscal|number]]<br>
                                    Año de inscripción vehículo: [[auto.Annio_Inscripcion]]<br>
                                    Número de inscripción: [[auto.Numero_Inscripcion|reservado]]<br>
                                </b-list-group-item>
                            </b-list-group>
                            
                            <template slot="modal-footer" slot-scope="{ok}">
                                <b-button size="lg" variant="dark" @click="ok()">
                                    Cerrar
                                </b-button>
                            </template>
                            
                        </b-modal>
                    </b-card> 
                </b-col>
                
                <b-col v-bind="multipleCols" :style="leftPad">
                
                    <b-card no-body>
                        <b-card-title class="mb-1 mt-1"><h4>Derechos o acciones en Chile</h4></b-card-title>
                        <b-list-group-item>
                            <div v-if="getDerechos">Cantidad de derechos o acciones: [[ getDerechos.length ]]</div>
                            <div v-else>No hay información</div>
                        </b-list-group-item>
                        
                        <b-button v-if="getDerechos" variant="dark" v-b-modal.ModalDerechos>Más info</b-button>
                        <b-button v-else variant="dark" disabled>Más info</b-button>
                        
                        <b-modal id="ModalDerechos" scrollable size="lg" title="Derechos o acciones en Chile">
                        
                            <b-list-group flush>
                                <b-list-group-item v-for="(derecho,index) in getDerechos" :key="index">
                                    <h5>[[derecho.Nombre_Razon_Social|capitalize]]</h5>
                                    Tipo: [[derecho.Titulo_Derecho_Accion.nombre|capitalize]]<br>
                                    Porcentaje de pertenencia: [[derecho.Cantidad_Porcentaje]]%<br>
                                    Rut: [[derecho.RUT]]<br>
                                    Rubro: [[derecho.Giro_Registrado_SII|capitalize]]<br>
                                    Fecha de adquisición: [[derecho.Fecha_Adquisicion|dateOnly]]<br>
                                    ¿Calidad de Controlador?: [[derecho.Tiene_Calidad_Controlador|yesNo]]
                                </b-list-group-item>
                            </b-list-group>
                            
                            <template slot="modal-footer" slot-scope="{ok}">
                                <b-button size="lg" variant="dark" @click="ok()">
                                    Cerrar
                                </b-button>
                            </template>
                            
                        </b-modal>
                    </b-card>
                    </b-card>
                
                </b-col>
                <b-col v-bind="multipleCols" :style="rightPad">
                
                    <b-card no-body>
                        <b-card-title class="mb-1 mt-1"><h4>Datos de Parientes</h4></b-card-title>
                        <b-list-group-item>
                            <div v-if="form_data.Datos_Parientes">Cantidad de parientes: [[ form_data.Datos_Parientes.length ]]</div>
                            <div v-else>No hay información</div>
                        </b-list-group-item>
                        
                        <b-button v-if="form_data.Datos_Parientes" variant="dark" v-b-modal.ModalParientes>Más info</b-button>
                        <b-button v-else variant="dark" disabled>Más info</b-button>
                        
                        <b-modal id="ModalParientes" scrollable size="lg" title="Vehiculos motorizados">
                        
                            <b-list-group flush>
                                <b-list-group-item v-for="(pariente, index) in form_data.Datos_Parientes" :key="index">
                                    <h5>[[pariente.nombre|name]] [[pariente.Apellido_Paterno|capitalize]]</h5>
                                    Parentezco: [[pariente.Parentesco.nombre|capitalize]]<br>
                                    Fecha de nacimiento: [[pariente.Fecha_Nacimiento|dateOnly]]<br>
                                    RUN: [[pariente.RUN|reservado]]
                                </b-list-group-item>
                            </b-list-group>
                            
                            <template slot="modal-footer" slot-scope="{ok}">
                                <b-button size="lg" variant="dark" @click="ok()">
                                    Cerrar
                                </b-button>
                            </template>
                            
                        </b-modal>
                    </b-card>
                    
                </b-col>
                
                <b-col v-bind="multipleCols">
                
                    <b-card no-body class="mb-1 mt-1">
                        <b-card-title class="mb-1"><h4>Datos del conyuge</h4></b-card-title>
                        <b-list-group-item>
                            <div v-if="!(form_data.Datos_del_Declarante.Estado_Civil.id !== 2)">Nombre: [[ get_nombreConyuge ]]</div>
                            <div v-else>No hay información</div>
                        </b-list-group-item>
                        
                        <b-button v-if="form_data.Declara_Bienes_Conyuge !== 'false'" variant="dark" v-b-modal.ModalConyuge>Más info</b-button>
                        <b-button v-else variant="dark" disabled> No declara información adicional </b-button>
                        
                        <b-modal id="ModalConyuge" scrollable size="lg" title="Datos del conyuge">
                            
                            <b-list-group flush>
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
                            </b-list-group>
                            
                            <template slot="modal-footer" slot-scope="{ok}">
                                <b-button size="lg" variant="dark" @click="ok()">
                                    Cerrar
                                </b-button>
                            </template>
                            
                        </b-modal>
                    </b-card>
                
                </b-col>
            </b-row>
        </div>
    `,
    data() {
        return{
            leftPad:{
                'padding-left': "0px"
            },
            rightPad:{
                'padding-right': "0px"
            },
            multipleCols: {
                class: 'mb-4',
                cols: '6',
            }
        }
    },
    delimiters: ['[[', ']]'],
    created: function() {
        this.$store.state.form_data = JSON.parse(document.getElementsByTagName('body')[0].getAttribute('data') || '{}');
    },
    store: declaracion_data,
    filters: {
        capitalize: function (value) {
            if (value !== undefined){
                value = value.toString().toLowerCase();
                return value.charAt(0).toUpperCase() + value.slice(1);
            }
        },
        dateOnly: function (value) {
            if (value !== undefined)
                return value.split(' ')[0];
            else
                return "No hay información";
        },
        yesNo: function (value) {
            if (value !== undefined)
            return ((value === false || value === "No" || value === "false" || value === "False") ? 'No' : 'Si');
        },
        number: function (value) {
            if (value !== undefined)
            return parseInt(value, 10).toLocaleString('es');
            if (value === "RESERVADO")
            return "Reservado";
        },
        name: function (value) {
            if (value !== undefined){
            value = value.toLowerCase().split(' ')
            var name = '';
            for (let i = 0; i < value.length; i++) {
                    name += value[i].charAt(0).toUpperCase() + value[i].slice(1) + ' ';
                }
                return name;
            }
        },
        reservado: function (value) {
            return (value === "RESERVADO") ? "Reservado" : value;
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
    methods:{
        AvaluoTotal: function(lista) {
            var Avaluo = 0;
            for (const elem of lista ){
                Avaluo += parseInt(elem.Avaluo_Fiscal, 10)
            }
            return Avaluo
        }
    },
};
