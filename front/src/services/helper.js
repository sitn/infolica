import { handleException } from "@/services/exceptionsHandler";
import axios from 'axios';
const moment = require('moment')

/**
 * Check if the user is logged in
 */
export const checkLogged = function () {
    var session_user = JSON.parse(localStorage.getItem('infolica_user')) || null;
    
    //Set current user functions
    if(session_user)
        setCurrentUserFunctions();
    
    return session_user !== null;
};


/**
 * Check permission
 */
export const checkPermission = function (fonction) {
    var session_user = JSON.parse(localStorage.getItem('infolica_user')) || null;

    if(session_user && session_user.fonctions && session_user.fonctions.indexOf(fonction) > -1){
        return true;
    }

    return false;
};


/**
 * Get current user role id
 */
export const getCurrentUserRoleId = function () {
    var session_user = JSON.parse(localStorage.getItem('infolica_user')) || null;
    return (session_user && session_user.role_id) ? session_user.role_id : null;
};

/*
 * Set current user functions
 */
export const setCurrentUserFunctions = async function () {    
    axios.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_CURRENT_USERS_FUNCTIONS_ENDPOINT,
        {
            withCredentials: true,
            headers: {"Accept": "application/json"}
        })
        .then(response =>{
            if(response && response.data){
                var session_user = JSON.parse(localStorage.getItem('infolica_user')) || null;
    
                if(session_user){
                    session_user.fonctions = response.data.fonctions;
                    session_user.role_id = response.data.role_id;
                    localStorage.setItem('infolica_user', JSON.stringify(session_user));
                }
            }
            })
        .catch(() => {
            //To do message
        });
};

/*
 * Get Cadastres
 */
export const getCadastres = async function () {
    return new Promise((resolve, reject) => {
        axios.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_CADASTRES_ENDPOINT,
            {
              withCredentials: true,
              headers: {"Accept": "application/json"}
            })
            .then(response => resolve(response))
            .catch(() => reject);
    });
};

/*
 * Get Types Numeros
 */
export const getTypesNumeros = async function () {
    return new Promise((resolve, reject) => {
        axios.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_TYPES_NUMEROS_ENDPOINT,
            {
              withCredentials: true,
              headers: {"Accept": "application/json"}
            })
            .then(response => resolve(response))
            .catch(() => reject);
    });
};

/*
 * Get Types Affaires
 */
export const getTypesAffaires = async function () {
    return new Promise((resolve, reject) => {
        axios.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_TYPES_AFFAIRES_ENDPOINT,
            {
              withCredentials: true,
              headers: {"Accept": "application/json"}
            })
            .then(response => resolve(response))
            .catch(() => reject);
    });
};

/*
 * Get Etats Numeros
 */
export const getEtatsNumeros = async function () {
    return new Promise((resolve, reject) => {
        axios.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_ETATS_NUMEROS_ENDPOINT,
            {
              withCredentials: true,
              headers: {"Accept": "application/json"}
            })
            .then(response => resolve(response))
            .catch(() => reject);
    });
};

/*
 * Get clients
 */
export const getClients = async function () {
    return new Promise((resolve, reject) => {
        axios.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_CLIENTS_ENDPOINT,
            {
              withCredentials: true,
              headers: {"Accept": "application/json"}
            })
            .then(response => {
                response.data = setClientsAdresse_(response.data);
                resolve(response);
            })
            .catch(() => reject);
    });
};

export const setClientsAdresse_ = function(clients, sep=", ") {
    let isArray = true;
    if (!Array.isArray(clients)) {
        isArray = false;
        clients = [clients];        
    }
    
    clients.forEach(x => {
        x.adresse_ = [
            x.entreprise,
            [x.titre, x.prenom, x.nom].filter(Boolean).join(" "),
            x.co,
            x.adresse,
            x.case_postale !== null? "Case postale " + x.case_postale: null,
            [x.npa, x.localite].filter(Boolean).join(" ")
        ].filter(Boolean).join(sep);
    });

    if (!isArray) {
        clients = clients.pop();
    }

    return clients;
}

/*
 * Get Operateurs
 */
export const getOperateurs = async function () {
    return new Promise((resolve, reject) => {
        axios.get(process.env.VUE_APP_API_URL + process.env.VUE_APP_OPERATEURS_ENDPOINT,
            {
              withCredentials: true,
              headers: {"Accept": "application/json"}
            }
        )
        .then(response => resolve(response))
        .catch(err => reject(err));
    });
};

/**
 * Get date of the day in good format for BD
 */
export const getCurrentDate = function () {
    var today = new Date();
    var date =
        ("0" + today.getDate()).slice(-2) + "." + ("0" + (today.getMonth() + 1)).slice(-2) + "." + today.getFullYear();
    return date;
};

/**
 * Prépare la liste pour le md-complete
 */
export const stringifyAutocomplete = function(liste, nom="nom", id="id") {
    return liste.map(x => ({
        id: x[id],
        nom: String(x[nom]),
        toLowerCase: () => String(x[nom]).toLowerCase(),
        toString: () => String(x[nom])
    }));
};

/**
 * Générer les documents à partir des modèles
 */
export const saveDocument = async function(formData) {
    return new Promise((resolve, reject) => {
        axios.post(process.env.VUE_APP_API_URL + process.env.VUE_APP_SAVE_DOCUMENT_ENDPOINT,
            formData,
            {
                withCredentials: true,
                headers: { Accept: "application/html" }
            }
        ).then(response => resolve(response))
        .catch(err => reject(err));
    });
};

/**
 * Générer les documents à partir des modèles
 */
export const getDocument = async function(formData) {
    return new Promise((resolve, reject) => {
        axios.post(process.env.VUE_APP_API_URL + process.env.VUE_APP_COURRIER_TEMPLATE_ENDPOINT,
            formData,
            {
                withCredentials: true,
                headers: { Accept: "application/html" }
            }
        ).then(response => {
            if (response && response.data) {
                const filename = response.data.filename;

                downloadGeneratedDocument(filename)
                .then(response => {
                    deleteGeneratedDocument(response)
                    .then(() => resolve(filename))
                    .catch(err => reject(err));
                })
            }
        })
        .catch(err => reject(err));
    });
};

/**
 * Download GeneratedDocument
 */
const downloadGeneratedDocument = async function(filename) {
    return new Promise(resolve => {
        let url =
        process.env.VUE_APP_API_URL +
        process.env.VUE_APP_COURRIER_TEMPLATE_ENDPOINT +
        "?filename=" +
        filename;
        window.open(url, "_blank");
        resolve(filename)
    });
};

/**
 * Delete generated document
 */
const deleteGeneratedDocument = async function(filename) {
    return new Promise((resolve, reject) => {
        new Promise(r => setTimeout(r, 200)).then(() => {

            axios.delete(process.env.VUE_APP_API_URL + process.env.VUE_APP_COURRIER_TEMPLATE_ENDPOINT +
                "?filename=" + filename,
                {
                    withCredentials: true,
                    headers: { Accept: "application/html" }
                }
            )
            .then(response => resolve(response))
            .catch(err => reject(err));
        });
    });    
};

/**
 * Search in list after n letters
 */
export const filterList = function(list, searchTerm, nLetters=0) {
    let result = [];

    if (typeof searchTerm !== "string") {
        return [];
    }

    if (searchTerm !== null) {
        let searchTerm_ = searchTerm.split(" ");

        let idx = searchTerm_.indexOf("");
        if (idx > -1) {
            searchTerm_.splice(idx, 1);
        }

        if (searchTerm.length >= nLetters) {
            result = list.filter(x => {
                return !searchTerm_.some(y => {
                    return !x.nom.toLowerCase().includes(y.toLowerCase());
                });
            });
        }
    }
    return result.slice(0,20);
};

/**
 * Set date format 
 */
export const setDateFormatClient = function(obj) {
    // test dates to set them to client format
    const dateRegex = /^\d{4}-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01])$/;
    for (const property in obj) {
      if (dateRegex.test(obj[property])) {
        obj[property] = moment(obj[property], process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
      }
    }
    return obj;
}

/**
 * Log new step
 */
export const logAffaireEtape = async function(affaire_id, etape_id, remarque=null, chef_equipe_id=null) {
    let formData = new FormData();
    formData.append("affaire_id", affaire_id);
    formData.append("etape_id", etape_id);
    formData.append("operateur_id", JSON.parse(localStorage.getItem("infolica_user")).id);
    formData.append("datetime", moment(new Date()).format(process.env.VUE_APP_DATETIMEFORMAT_WS));
    if (remarque) {
        formData.append("remarque", remarque);
    }
    if (chef_equipe_id) {
        formData.append("chef_equipe_id", chef_equipe_id);
    }

    return new Promise(resolve => {
        axios.post(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_ETAPES_ENDPOINT,
            formData,
            {
              withCredentials: true,
              headers: {"Accept": "application/json"}
            }
        ).then(response => resolve(response))
        .catch(err => handleException(err));
    });
}


