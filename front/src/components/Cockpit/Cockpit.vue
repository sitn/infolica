<style src="./cockpit.css" scoped></style>
<template src="./cockpit.html"></template>


<script>
import { handleException } from '@/services/exceptionsHandler'
import { checkPermission, getOperateurs, stringifyAutocomplete } from '@/services/helper'


export default {
  name: "Cockpit",
  data: () => {
    return {
        affaires: [],
        affaires_bk: [],
        affaireEtapes: [],
        loadingAffaires: true,
        newAffaireAllowed: false,
        operateurs: [],
        searchAffaire: null,
        selectedOperateur: -1,
        showFinProcessus: false,
    }
  },

  methods: {
    /**
     * Get permissions
     */
    getPermissions() {
        this.newAffaireAllowed = checkPermission(process.env.VUE_APP_AFFAIRE_EDITION);
    },

    /**
     * get Affaires
     */
    async getAffaire() {
        await this.getAffaireEtapes();
        this.$http.get(
            // process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRE_TELE_ENDPOINT,
            process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_COCKPIT_ENDPOINT,
            {
                withCredentials: true,
                headers: {Accept: "application/json"}
            }
        ).then(response => {
            if (response && response.data) {
                let tmp = JSON.parse(response.data);
                // tmp = tmp.slice(0,30); // to remove !!!
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

                tmp = stringifyAutocomplete(tmp, "nom_");
                tmp.sort((a,b) => (a.nom > b.nom) ? 1 : ((b.nom > a.nom) ? -1 : 0));

                this.operateurs = tmp;
            }
        }).catch(err => handleException(err, this));
    }
  },

  mounted: function() {
    this.getPermissions();
    this.getAffaire();
    this.getOperateursList();

    setInterval(() => this.getAffaire(), 60000); // Recharge le tableau toutes les minutes


  }
};
</script>
