var FormParlamentarios = {
    'Nombre': 'N/A',
    'Id_Declaracion': 0,
    'Fecha_de_la_Declaracion': "N/A",
    'Tipo_Declaracion': {},
    'Region': {},
    'Comuna': {},
    'Datos_del_Declarante': {},
    'Datos_del_Conyuge': {},
    'Declara_Bienes_Conyuge': "N/A",
    'Datos_Entidad_Por_La_Que_Declara': {},
    'Datos_Parientes': [],
    'Bienes_Inmuebles_Situados_En_Chile': [],
    'Vehiculos_Motorizados': [],
    'Naves_Artefactos_Navales': [],
    'Derechos_Acciones_Chile': [],
    'Pasivos': {},
    'Otros_Antecedentes': [],
    'Sujeto_Obligado': 0,
    'Actividades_Profesionales_Ultimos_12_Meses': [],
    'Actividades_Profesionales_A_La_Fecha': [],
    'Actividades_Profesionales_Conyuge': [],
    'Otros_Bienes_Muebles ': [],
    'Instrumentos_Valor_TransableChile': [],
    'Patrimonio_Conyuge': []
};

var FormContent = {

    // language=HTML
    template:
    `
    <form>
        <label for="title" class="col-sm-2 col-form-label">Title: <span class="text-danger">*</span></label>
    </form>
    `
};

Vue.use(window.VueResource);

var declaracion_data = new Vuex.Store({
    state: {
        editable: false,
        form_data: FormParlamentarios,
        form_base: FormContent,
    },
    actions: {

    },
    mutations: {
        updateEditable: state => {
            state.editable = true;
        },
        updateForm: (state, dic) => {
            state.form_data = dic;
        }
    },
    getters: {
    },
});