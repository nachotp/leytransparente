const EstadisticasVue = {
    template: `
    <b-container style="max-width: 1450px">
        <b-row>
            <b-col md="3">
                <b-card>
                <h4>Gráficos</h4>
                <h5>Partido Político</h5>
                    <b-tabs vertical pills fill nav-wrapper-class="w-100" v-on:input="metodo" lazy>
                        <b-tab v-for="(tab,index) in tabs" :key="index" title-item-class="h5 dummytab" :title="tab" :class="isFirst(index)" ></b-tab>
                    </b-tabs>
                </b-card>
            </b-col>

            <b-col>
                <b-card>
                <h2 class="text-center">[[graph_title]]</h2>
                    <div class="ct-chart ct-golden-section" id="chart1"></div>
                </b-card>
            </b-col>
        </b-row>
    </b-container>
    `,
    data() {
        return {
            tabs: [
                'Total de Conflictos',
                'Tipos de Conflicto',
                'Total de Conflictos',
                'Tipos de Conflicto'
            ],
            graph_names: [
                "Conflictos detectados según partido político",
                "Conflictos detectados por partido político según tipo",
                "Conflictos detectados según Región",
                "Conflictos detectados por Región según tipo"
            ],
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
    mounted: function (){
        this.$nextTick(function () {
            var lis = document.getElementsByClassName('dummytab');
            for (var i = 0; i < lis.length; i++){
                if (i === 1) {
                    lis[i].insertAdjacentHTML('afterend', "<h5>Región</h5>");
                }
            }
        });
    },
    methods:{
        metodo: function (tab) {
            this.curr_tab = tab;
            var elements = document.getElementsByClassName('ct-legend');
            while(elements.length > 0){
                elements[0].parentNode.removeChild(elements[0]);
            }
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
            }
            else if (tab === 1) {
                new Chartist.Bar('#chart1', {
                    labels: stats.partidos,
                    series: [
                        stats.partidos_graves,
                        stats.partidos_leves,
                        stats.partidos_directos,
                        stats.partidos_indirectos,
                        ]
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
                        Chartist.plugins.legend({
                            legendNames: ['Graves', 'Leves', 'Directos', 'Indirectos'],
                        }),
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
            }//Agregar otros valores de tab para hacer los gráficos
            else if( tab === 2){
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
            else if (tab === 3) {
                new Chartist.Bar('#chart1', {
                    labels: stats.region,
                    series: [
                        stats.region_graves,
                        stats.region_leves,
                        stats.region_directos,
                        stats.region_indirectos,
                        ]
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
                        Chartist.plugins.legend({
                            legendNames: ['Graves', 'Leves', 'Directos', 'Indirectos'],
                        }),
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
