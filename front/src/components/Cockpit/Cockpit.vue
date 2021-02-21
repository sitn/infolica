<style src="./cockpit.css" scoped></style>
<template src="./cockpit.html"></template>


<script>
import Matdiff from "@/components/Cockpit/Matdiff/Matdiff.vue";

import { handleException } from '@/services/exceptionsHandler'
import { checkPermission, getOperateurs, stringifyAutocomplete, getCurrentUserRoleId } from '@/services/helper'

export default {
  name: "Cockpit",
  components: {
      Matdiff
  },
  data: () => {
    return {
        affaires: [],
        affaires_bk: [],
        affaireEtapes: [],
        affaireTypes: [],
        loadingAffaires: true,
        newAffaireAllowed: false,
        operateurs: [],
        searchAffaire: null,
        selectedOperateur: -1,
        selectedAffaireType: [1,3,6,10,11],
        showFinProcessus: false,
        showMatdiff: false,
    }
  },

  methods: {
    /**
     * Get permissions
     */
    getPermissions() {
        // set time out of 0.5 seconds. If not, local storage has not time to memorize user allowed functions
        setTimeout(() => {
            
            this.newAffaireAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_EDITION) || checkPermission(process.env.VUE_APP_AFFAIRE_PPE_EDITION) ||
                                     checkPermission(process.env.VUE_APP_AFFAIRE_REVISION_ABORNEMENT_EDITION) || checkPermission(process.env.VUE_APP_AFFAIRE_CADASTRATION_EDITION) ||
                                     checkPermission(process.env.VUE_APP_AFFAIRE_RETABLISSEMENT_PFP3_EDITION);
            
            //Check if role secretaire
            let role_id = getCurrentUserRoleId();
            if ( role_id && !isNaN(role_id) && Number(role_id) === Number(process.env.VUE_APP_SECRETAIRE_ROLE_ID)  || checkPermission(process.env.VUE_APP_FONCTION_ADMIN) ) {
                this.showMatdiff = true;
            }

        }, 500);
    },

    /**
     * get Affaires
     */
    async getAffaire() {
        await this.getAffaireEtapes();
        await this.getAffaireTypes();
        this.$http.get(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_COCKPIT_ENDPOINT,
            {
                withCredentials: true,
                headers: {Accept: "application/json"}
            }
        ).then(response => {
            if (response && response.data) {
                let tmp = JSON.parse(response.data);
                tmp.forEach(x => {
                    for (let i=0; i<this.affaireEtapes.length; i++) {
                        x["dashboard_" + i.toString()] = i === x.etape_ordre-1? (x.no_access? x.no_access: x.id): null;
                    }
                });
                this.affaires_bk = tmp;
                if (!this.affaires.length > 0) {
                    this.affaires = tmp;
                }

                this.updateTable();
            }
        }).catch(err => handleException(err, this));
    },

    /**
     * Get affaire etapes
     */
    async getAffaireEtapes() {
        this.$http.get(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_ETAPES_INDEX_ENDPOINT,
            {
                withCredentials: true,
                headers: {Accept: "application/json"}
            }
        ).then(response => {
            if (response && response.data) {
                this.affaireEtapes = response.data;
            }
        }).catch(err => handleException(err, this));
    },

    /**
     * Get affaire types
     */
    async getAffaireTypes() {
        this.$http.get(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_TYPES_AFFAIRES_ENDPOINT,
            {
                withCredentials: true,
                headers: {Accept: "application/json"}
            }
        ).then(response => {
            if (response && response.data) {
                let tmp = response.data;
                tmp.push({'id': 15, 'nom': 'Mat diff', 'ordre': 11, 'priorite': 1});
                this.affaireTypes = stringifyAutocomplete(tmp);
            }
        }).catch(err => handleException(err, this));
    },

    /**
     * open affaire
     */
    openAffaire(data) {
        let id = data.id;
        this.$router.push({ name: "AffairesDashboard", params: {id}});
    },

    /**
     * Update table and content to show or not FinProcessus step
     */
    updateTable() {
        this.loadingAffaires = true;

        // filter affaires by showing or not Fin Processus
        if (this.showFinProcessus) {
            this.affaires = this.affaires_bk;
        } else {
            this.affaires = this.affaires_bk.filter(x => x.etape_id !== Number(process.env.VUE_APP_FIN_PROCESSUS_ID));
        }
        
        // filter affaires by name if specified
        if (this.searchAffaire) {
            this.affaires = this.affaires.filter(x => x.no_access.toLowerCase().includes(this.searchAffaire.toLowerCase()) || x.id.toString().includes(this.searchAffaire));
        }

        // filter affaire by operateur if specified
        if (this.selectedOperateur && this.selectedOperateur > 0) {
            this.affaires = this.affaires.filter(x => x.operateur_id === this.selectedOperateur);
        }
        
        // filter affaire type
        this.affaires = this.affaires.filter(x => this.selectedAffaireType.includes(x.affaire_type_id));
        
        this.loadingAffaires = false;
    },

    /**
     * Get operateurs
     */
    async getOperateursList() {
        getOperateurs()
        .then(response => {
            if (response && response.data) {
                let tmp = response.data;
                tmp = tmp.filter(x => x.chef_equipe);
                tmp.forEach(x => x['nom_'] = [x.prenom, x.nom].filter(Boolean).join(' '));

                // set operateur by default if he is chef_equipe
                let currentUserID = JSON.parse(localStorage.getItem("infolica_user")).id;
                if (tmp.some(x => (x.id === currentUserID) && x.chef_equipe)) {
                    this.selectedOperateur = Number(currentUserID);
                }

                tmp = stringifyAutocomplete(tmp, "nom_");
                tmp.sort((a,b) => (a.nom > b.nom) ? 1 : ((b.nom > a.nom) ? -1 : 0));

                this.operateurs = tmp;
            }
        }).catch(err => handleException(err, this));
    }
  },

  mounted: function() {
    this.getAffaire();
    this.getOperateursList();
    this.getPermissions();

    setInterval(() => this.getAffaire(), 60000); // Recharge le tableau toutes les minutes


  }
};
</script>

