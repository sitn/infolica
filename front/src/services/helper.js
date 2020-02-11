/**
 * Check if the user is logged in
 */
export const checkLogged = function() {
    var session_user = JSON.parse(localStorage.getItem('infolica_user')) || null;

    if (!session_user) {
        window.location.href = "/login"
    }
};

/*
 * Get Cadastres
 */
export const getCadastres = async function() {
    return this.$http.get(
        process.env.VUE_APP_API_URL + process.env.VUE_APP_CADASTRES_ENDPOINT
    ).then(response => {
        if (response && response.data) {
            this.cadastre_liste = response.data.map(function(obj) {
                return obj.nom;
            });
        }
    }).catch(err => {
        alert("error: " + err.message);
    });
};

/*
 * Get Types Numeros
 */
export const getTypesNumeros = async function() {
    return this.$http.get(
        process.env.VUE_APP_API_URL +
        process.env.VUE_APP_TYPES_NUMEROS_ENDPOINT
    ).then(response => {
        if (response && response.data) {
            this.types_numeros = response.data.map(function(obj) {
                return obj.nom;
            });
        }
    }).catch(err => {
        alert("error: " + err.message);
    });
};


/*
 * Get Etats Numeros
 */
export const getEtatsNumeros = async function() {
    return this.$http
        .get(
            process.env.VUE_APP_API_URL +
            process.env.VUE_APP_ETATS_NUMEROS_ENDPOINT
        ).then(response => {
            if (response && response.data) {
                this.etats_numeros = response.data.map(function(obj) {
                    return obj.nom;
                });
            }
        }).catch(err => {
            alert("error: " + err.message);
        });
};