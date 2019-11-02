const patronesVue = {
    delimiters: ['[[', ']]'],
    data(){
        return{
            patrones: [],
            ready: false,
        }
    },
    created: function() {
        const Http = new XMLHttpRequest();
        const url = 'http://127.0.0.1:8000/api/patrones/';

        var response = Http.responseText;

        Http.onreadystatechange=(e)=>{
            if(Http.status === 200 && Http.readyState === 4){
                this.patrones = JSON.parse(Http.responseText);
                this.ready = true;
            }
        };

        Http.open("GET", url);
        Http.send(null);
    },
    computed: {

    },
    method: {
    },
    //Ajusta la frase para que la primera letra sea mayúscula
    filters: {
        capitalize: function (value) {
            if (value !== undefined){
                value = value.toString().toLowerCase();
                return value.charAt(0).toUpperCase() + value.slice(1);
            }
        },
    },
    template:`
<div v-if="ready">
    <b-container v-if="patrones.length > 0" class="mw-100">
    
        <h1>Patrones</h1>
        <h5>Los siguientes patrones son agrupaciones de conflictos, que son semejantes en el giro del Servicio Impuestos Interno, o en el "Motivo" listado</h5>
        <b-col v-for="(patron, index) in patrones" :key="index" sm="12" class="mt-4">
    
            <b-row>
                <b-card :header="'Patrón ' + index"
                        header-bg-variant="dark"
                        header-text-variant="white"
                        header-class="h2"
                        border-variant="dark">
                     <b-card-group >
                        <b-col v-for="(conflicto, index) in patron" :key="index"  cols="4" style="padding-left: 0px;  padding-right: 0px;">
                            <b-card class="rounded-0" :title="conflicto.parlamentario" :sub-title="conflicto.partido">
                                <b-card-text>
                                    <b-list-group flush>
                                        <b-list-group-item><b>Nombre Ley: </b>[[ conflicto.nombre_ley|capitalize ]]</b-list-group-item>
                                        <b-list-group-item><b>Razón conflicto: </b>[[ conflicto.razon.prov_conf|capitalize ]]</b-list-group-item>
                                        <b-list-group-item><b>Motivo: </b>[[ conflicto.razon.motivo|capitalize ]]</b-list-group-item>
                                    </b-list-group>
                                </b-card-text>
                            </b-card>
                        </b-col>
                    </b-card-group>
                </b-card>
            </b-row>
        </b-col>
    </b-container>

    <b-container style="max-width: 1450px" v-else>
        <h3>No se han encontrado patrones en los conflictos de interés.</h3>
    </b-container>
</div>

<div v-else>
    <b-container style="max-width: 1450px">
        <h3>Cargando información...</h3>
    </b-container>
</div>
    `,
}