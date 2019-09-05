const conflictosVue = {
    template:`
<div class="container">
    
    <!--Si hay conflictos-->
    <b-container v-if="conflictos" class="bv-example-row">
        <b-row>
            <b-col class="ml-auto">
            <h3>Conflictos Existentes</h3>
            </b-col>
        </b-row>
        
        <!--Herramientras de filtrado-->
        
        <b-row class="mt-3">
            <b-col>
                <label for="namesearch" style="display: block"><h5>Nombre parlamentario</h5></label>
            </b-col>
            
            <b-col>
                <label for="leysearch" style="display: block"><h5>Número o nombre Ley</h5></label>
            </b-col>
            
            <b-col>
                <label for="partidosearch" style="display: block"><h5>Partido político</h5></label>
            </b-col>
        </b-row>
        
        <b-row>
            <b-col v-bind="filterCols">
                <b-form-input  id="namesearch" size="lg" v-model="searchName" placeholder="Buscar por nombre"></b-form-input>
            </b-col>
            
            <b-col v-bind="filterCols">
                <b-form-input id="leysearch" size="lg" v-model="searchLey" placeholder="Buscar por ley"></b-form-input>
            </b-col>
        
            <b-col v-bind="filterCols">
            
                <b-dropdown id="partidosearch" size="lg" variant="outline-dark" style="width:100%" :text="fillDropdown">
                    <b-dropdown-item @click="searchPartido = ''"> Todos</b-dropdown-item>
                    <b-dropdown-item v-for="(conflicto, index) in conflictos" 
                                :key="index" 
                                :value="conflicto.partido"
                                @click="searchPartido = conflicto.partido">[[conflicto.partido]]
                    </b-dropdown-item>
                </b-dropdown>
                
            </b-col>
        
        </b-row>

        
        <b-row>
            <!--Se muestran todos los conflictos-->
            <b-col v-for="(conflicto, index) in filterConflictosLey" :key="index" cols="6">
                <b-card style="margin-top: 20px;" no-body header=" " :header-bg-variant="conflicto.grado == 'leve' ? 'warning' : 'danger' ">
    
                <b-card-body style="padding-bottom: 0px; padding-top: 12px">
                    <a href="/'Ver Declaracion' id=conflicto.id_parlamentario %}"><h4>[[ conflicto.parlamentario ]]</h4></a>
                    <h4>[[conflicto.partido]]</h4>
                    <b-card-text>
                        <b-list-group flush>
                            <b-list-group-item v-bind="listItem"><b>Ley Nº : </b>
                            <b-link class="card-link">[[conflicto.ley]]</b-link>
                            </b-list-group-item>
                            <b-list-group-item v-bind="listItem"><b>Nombre de Ley : </b>[[conflicto.nombre_ley|capitalize]]</b-list-group-item>
                            <b-list-group-item v-bind="listItem"><b>Motivo : </b>[[conflicto.prov_conf|capitalize]]</b-list-group-item>
                            <b-list-group-item v-bind="listItem"><b>Patrimonio relacionado : </b>[[conflicto.motivo|capitalize]]</b-list-group-item>
                            <b-list-group-item v-bind="listItem"><b>Grado de Conflicto : </b>[[conflicto.grado|capitalize]]</b-list-group-item>
                        </b-list-group>
                    </b-card-text>
                </b-card-body>
            </b-card>
            </b-col>
        </b-row>
    </b-container>
    
    <b-container v-else>
        <b-row>
            <b-col class="ml-auto">
            <h3>No hay conflictos</h3>
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
            filterCols: {
                cols: '4',
                style:{
                    'display': 'flex',
                    'justify-content': 'center',
                    'align-items': 'center',
                }
            },
            listItem: {
                style: {
                    'padding-left': '0px'
                }
            }
        }
    },
    created: function() {
        this.conflictos = JSON.parse(document.getElementsByTagName('body')[0].getAttribute('data') || '{}');
    },
    computed: {
        //Filtra los conflictos, tal que sólo se muestran los que calzan parcialmente con el texto en searchName
        filterConflictosName: function () {
            return this.conflictos.filter((conflicto) =>{
                var namesearch = conflicto.parlamentario.toLowerCase().indexOf( this.searchName.toLowerCase() ) > -1;
                return namesearch;
            });
        },
        //Filtra los conflictos, tal que calza con el partido
        filterConflictosPartido: function () {
            return this.filterConflictosName.filter((conflicto) =>{
                return conflicto.partido.toLowerCase().match(this.searchPartido.toLowerCase());
            });
        },
        //Filtra los conflictos, tal que calza parcial con el número de ley
        filterConflictosLey: function () {
            return this.filterConflictosPartido.filter((conflicto) =>{
                var numberSearch = conflicto.ley.indexOf( this.searchLey ) > -1;
                var textSearch = conflicto.nombre_ley.toLowerCase().indexOf( this.searchLey.toLowerCase() ) > -1;
                return numberSearch || textSearch;
            });
        },
        fillDropdown: function () {
            return (this.searchPartido === '') ? "Todos" : this.searchPartido;
        }
    },
    //Ajusta la frase para que la primera letra sea mayúscula
    filters: {
        capitalize: function (value) {
            if (value !== undefined){
                value = value.toString().toLowerCase();
                return value.charAt(0).toUpperCase() + value.slice(1);
            }
        },
    }
}