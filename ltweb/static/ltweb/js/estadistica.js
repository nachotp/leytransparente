const EstadisticasVue = {
    template: `
    <b-container style="max-width: 1450px">
        <b-row>
            <b-col md="3">
                <b-card>
                <h4>Gráficos</h4>
                    <b-tabs content-class="" vertical pills fill nav-wrapper-class="w-100" v-on:input="metodo">
                        <b-tab v-for="(tab,index) in tabs" :key="index" title-item-class="h5" :title="tab" :class="isFirst(index)" ></b-tab>
                    </b-tabs>
                </b-card>
            </b-col>

            <b-col>
                <b-card>
                <h1>[[graph_title]]</h1>
                    <div class="ct-chart ct-golden-section" id="chart1"></div>
                </b-card>
            </b-col>
        </b-row>
    </b-container>
    `,
    data() {
        return {
            tabs: ['First', 'Second'],
            graph_names: ["meeemes", "Beefs"],
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
    methods:{
        metodo: function (tab) {
            this.curr_tab = tab;
            if( tab === 0){
                new Chartist.Line('#chart1', {
                    labels: [1, 2, 3, 4],
                    series: [[1,2,3,4]]
                    }
                    ,{
                    chartPadding: {
                        top: 20,
                        right: 0,
                        bottom: 30,
                        left: 0
                    },
                    axisY: {
                        onlyInteger: true
                      },
                    plugins: [
                    Chartist.plugins.ctAxisTitle({
                      axisX: {
                        axisTitle: 'Time (mins)',
                        axisClass: 'ct-axis-title',
                        offset: {
                            x: 0,
                            y: 50
                        },
                        textAnchor: 'middle'
                      },
                      axisY: {
                        axisTitle: 'Goals',
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
                    labels: ["Beef","Chris"],
                    series: [[3,2],[4, 6]]},{
                    chartPadding: {
                        top: 20,
                        right: 0,
                        bottom: 30,
                        left: 0
                    },
                    axisY: {
                        onlyInteger: true
                      },
                    plugins: [
                    Chartist.plugins.ctAxisTitle({
                      axisX: {
                        axisTitle: 'Time (mins)',
                        axisClass: 'ct-axis-title',
                        offset: {
                            x: 0,
                            y: 50
                        },
                        textAnchor: 'middle'
                      },
                      axisY: {
                        axisTitle: 'Goals',
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
