const conflictosVue = {
    template:`
<div class="container">
    
    <b-container v-if="conflictos" class="bv-example-row">
        <b-row>
            <b-col class="ml-auto">
            <h3>Conflictos Existentes</h3>
            </b-col>
        </b-row>
        
        <h2 class="text-center"><input class="m-md-2" v-model="searchName" placeholder="Buscar por nombre">
            <input class="m-md-2" v-model="searchLey" placeholder="Buscar por ley">
            <b-dropdown text="Partido político">
                <b-dropdown-item @click="searchPartido = ' '"> Ninguno</b-dropdown-item>
                <b-dropdown-item v-for="(conflicto, index) in conflictos" 
                            :key="index" 
                            :value="conflicto.partido"
                            @click="searchPartido = conflicto.partido">[[conflicto.partido]]
                </b-dropdown-item>
            </b-dropdown>
        </h2>
        
        <b-row>
            <b-col v-for="(conflicto, index) in filterConflictosLey" :key="index" class="cols-6">
                <b-card style="margin-top: 20px;" no-body header=" " :header-bg-variant="conflicto.grado == 'leve' ? 'warning' : 'danger' ">
    
                <b-card-body style="padding-bottom: 0px">
                    <a href="{% url 'Ver Declaracion' id=conflicto.id_parlamentario %}"><h4>[[ conflicto.parlamentario ]]</h4></a>
                    <h4>[[conflicto.partido]]</h4>
                    <b-card-text>
                        <b-list-group flush>
                            <b-list-group-item><b>Ley Nº : </b>[[conflicto.ley]]</b-list-group-item>
                            <b-list-group-item><b>Nombre de Ley : </b>[[conflicto.nombre_ley|capitalize]]</b-list-group-item>
                            <b-list-group-item><b>Motivo : </b>[[conflicto.prov_conf|capitalize]]</b-list-group-item>
                            <b-list-group-item><b>Patrimonio en conflicto : </b>[[conflicto.motivo|capitalize]]</b-list-group-item>
                            <b-list-group-item><b>Grado de Conflicto : </b>[[conflicto.grado|capitalize]]</b-list-group-item>
                        </b-list-group>
                    </b-card-text>
                </b-card-body>
            </b-card>
            </b-col>
        </b-row>
    </b-container>
</div>
    `,
    delimiters: ['[[', ']]'],
    data(){
        return{
            conflictos: [],
            searchName: '',
            searchLey: '',
            searchPartido: '',
        }
    },
    created: function() {
        this.conflictos = JSON.parse(document.getElementsByTagName('body')[0].getAttribute('data') || '{}');
    },
    computed: {
        filterConflictosName: function () {
            return this.conflictos.filter((conflicto) =>{
                var namesearch = conflicto.parlamentario.toLowerCase().indexOf( this.searchName.toLowerCase() ) > -1;
                return namesearch;
            });
        },
        filterConflictosPartido: function () {
            return this.filterConflictosName.filter((conflicto) =>{
                return conflicto.partido.toLowerCase().match(this.searchPartido.toLowerCase());
            });
        },
        filterConflictosLey: function () {
            return this.filterConflictosPartido.filter((conflicto) =>{
                return conflicto.ley.indexOf( this.searchLey ) > -1;
            });
        }
    },
    filters: {
        capitalize: function (value) {
            if (value !== undefined){
                value = value.toString().toLowerCase();
                return value.charAt(0).toUpperCase() + value.slice(1);
            }
        },
    }
}