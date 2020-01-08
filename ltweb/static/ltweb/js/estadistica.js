const EstadisticasVue = {
    template: `
    <b-container style="max-width: 1450px">
        <b-row>
            <b-col md="3">
                <b-card>
                    <b-tabs content-class="" vertical pills fill nav-wrapper-class="w-100" v-on:input="metodo">
                        <b-tab title-item-class="h1"  title="First" ></b-tab>
                        <b-tab title-item-class="h1" title="Second" active></b-tab>
                        <b-tab title-item-class="h1" title="Disabled" disabled></b-tab>
                    </b-tabs>
                </b-card>
            </b-col>

            <b-col>
                <b-card>
                    <div class="ct-chart ct-golden-section" id="chart1"></div>
                </b-card>
            </b-col>
        </b-row>
    </b-container>
    `,
    data() {
        return {

        }
    },
    delimiters: ['[[', ']]'],
    filters: {
    },
    computed: {
    },
    methods:{
        metodo: function (tab) {
            if( tab === 0){
                new Chartist.Line('#chart1', {
                  labels: [1, 2, 3, 4],
                  series: [[1,2,3,4]]
                });
            }       //Agregar otros valores de tab para hacer los gráficos
            else if( tab === 1){
                new Chartist.Line('#chart1', {
                  labels: [1, 2, 3, 4],
                  series: [[4,3,2,1]]
                });
            }
        }
    },
};
