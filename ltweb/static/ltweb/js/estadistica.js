const EstadisticasVue = {
    template: `
    <b-container style="max-width: 1450px">
        <b-row>
            <b-col md="3">
                <b-card>
                <h4>Gráficos</h4>
                    <b-tabs vertical pills fill nav-wrapper-class="w-100" v-on:input="metodo" lazy>
                        <b-tab v-for="(tab,index) in tabs" :key="index" title-item-class="h5" :title="tab" :class="isFirst(index)" ></b-tab>
                    </b-tabs>
                </b-card>
            </b-col>

            <b-col>
                <b-card>
                <h1 class="text-center">[[graph_title]]</h1>
                    <div class="ct-chart ct-golden-section" id="chart1"></div>
                </b-card>
            </b-col>
        </b-row>
    </b-container>
    `,
    data() {
        return {
            tabs: ['Conflictos según partido', 'Conflictos según Región'],
            graph_names: ["Conflictos detectados según partido político", "Conflictos detectados según Región"],
            curr_tab: 0,
        }
    },
    delimiters: ['[[', ']]'],
    filters: {
    },
    computed: {
        graph_title: function () {
            return this.graph_names[this.curr_tab];
        }
    },
    created: function (){
    },
    methods:{
        metodo: function (tab) {
            this.curr_tab = tab;
            if( tab === 0){
                // Partido Político
                new Chartist.Bar('#chart1', {
                    labels: stats.partidos,
                    series: [stats.partidos_total]
                    }
                    ,{
                    chartPadding: {
                        top: 20,
                        right: 0,
                        bottom: 30,
                        left: 20
                    },
                    axisY: {
                        onlyInteger: true
                      },
                    plugins: [
                    Chartist.plugins.ctAxisTitle({
                      axisX: {
                        axisTitle: 'Partido Político',
                        axisClass: 'ct-axis-title',
                        offset: {
                            x: 0,
                            y: 50
                        },
                        textAnchor: 'middle'
                      },
                      axisY: {
                        axisTitle: 'Total de Conflictos Detectados',
                        axisClass: 'ct-axis-title',
                        offset: {
                            x: 0,
                            y: -1
                        },
                        textAnchor: 'middle',
                        flip: true
                      }
                    })
                  ]
                });
            }       //Agregar otros valores de tab para hacer los gráficos
            else if( tab === 1){
                new Chartist.Bar('#chart1', {
                    labels: stats.region,
                    series: [stats.region_total]
                    },{
                    chartPadding: {
                        top: 20,
                        right: 0,
                        bottom: 30,
                        left: 20
                    },
                    axisY: {
                        onlyInteger: true
                      },
                    plugins: [
                    Chartist.plugins.ctAxisTitle({
                      axisX: {
                        axisTitle: 'Región Administrativa',
                        axisClass: 'ct-axis-title',
                        offset: {
                            x: 0,
                            y: 50
                        },
                        textAnchor: 'middle'
                      },
                      axisY: {
                        axisTitle: 'Total de Conflictos Detectados',
                        axisClass: 'ct-axis-title',
                        offset: {
                            x: 0,
                            y: -1
                        },
                        textAnchor: 'middle',
                        flip: true
                      }
                    })
                  ]
                });
            }
        },
            isFirst: function(index) {
            if(index === 0)
                return 'active';
        }
    },
};
