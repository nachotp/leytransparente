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
        getLey: function () {

            clusters = [];
            for (const patron of this.patrones){
                var counting = {};
                alto = 0;
                newmax = '';
                //Contamos las leyes diferentes que hay y nos quedamos con la más alta
                for (const conflicto of patron){

                    //Si la ley ya está, sumamos 1, si no, iniciamos el dict con un 1
                    if(conflicto.nombre_ley in Object.keys(counting))
                        counting[conflicto.nombre_ley] += 1;
                    else
                        counting[conflicto.nombre_ley] = 1;

                    //Se encuentra el mayor
                    if(counting[conflicto.nombre_ley] > alto){
                        alto = counting[conflicto.nombre_ley];
                        newmax = conflicto.nombre_ley;
                    }
                }
                mayorPartido = [];
                others = [];
                //Se separan en la ley dominante y el resto
                for (const conflicto of patron){

                    if (conflicto.nombre_ley === newmax)
                        mayorPartido.push(conflicto);
                    else
                        others.push(conflicto);
                }
                //Se agrega a la lista

                clusters.push({"most": mayorPartido, "least": others});
            }
            return clusters;
        },
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
        Patron: function (value) {
            return "Patrón " + value;
        },
        isNull: function (value) {
            if(value === undefined || value === null || value === ''){
                return "N/A";
            }
            else
                return value;
        }
    },
    template:`
<div v-if="ready">
    <b-container v-if="patrones.length > 0" class="mw-100">
        
        <h1>Patrones</h1>
        <h5>Los siguientes patrones son agrupaciones de conflictos, que son semejantes en el giro del Servicio Impuestos Interno, o en el "Motivo" listado</h5>
        <b-col v-for="(patron, index) in getLey" :key="index" sm="12" class="mt-4">
    
                <b-card :header="index + 1|Patron"
                        header-bg-variant="dark"
                        header-text-variant="white"
                        header-class="h2"
                        border-variant="dark">
                     <b-card-group >
                        <b-col cols="12">
                            <b-card :header="'Ley: ' + patron['most'][0].nombre_ley|capitalize"
                                    header-bg-variant="light"
                                    header-class="h3"
                                    border-variant="dark">
                                <b-card-text>
                                    <b-list-group flush>
                                        <b-list-group-item v-for="(conflicto, index) in patron['most']" :key="index">
                                            <h5>[[conflicto.parlamentario]] ([[conflicto.partido|isNull]])</h5>
                                            <b>Razón conflicto: </b>[[conflicto.razon.motivo|capitalize]]<br>
                                            <b>Motivo: </b>[[conflicto.razon.prov_conf|capitalize]]<br>
                                        </b-list-group-item>
                                    </b-list-group>
                                </b-card-text>
                            </b-card>
                        </b-col>
                        
                        <b-col cols="12" class="mt-4">
                            <b-card header="Otras leyes"
                                    header-bg-variant="light"
                                    header-class="h3"
                                    border-variant="dark"
                                    v-if="patron['least'].length > 0" >
                        
                                <b-card-text>
                                    <b-list-group flush>
                                        <b-list-group-item v-for="(conflicto, index) in patron['least']" :key="index">
                                            <h5>[[conflicto.parlamentario]] ([[conflicto.partido|isNull]])</h5>
                                            <b>Nombre Ley: </b>[[conflicto.nombre_ley|capitalize]]<br>
                                            <b>Razón conflicto: </b>[[conflicto.razon.motivo|capitalize]]<br>
                                            <b>Motivo: </b>[[conflicto.razon.prov_conf|capitalize]]<br>
                                        </b-list-group-item>
                                    </b-list-group>
                                </b-card-text>
                            </b-card>
                        </b-col>
                        
                    </b-card-group>
                </b-card>
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