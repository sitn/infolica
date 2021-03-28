<style src="./cockpit.css" scoped></style>
<template src="./cockpit.html"></template>


<script>
import Matdiff_secr from "@/components/Cockpit/Matdiff_secr/Matdiff_secr.vue";
import Matdiff_mo from "@/components/Cockpit/Matdiff_mo/Matdiff_mo.vue";
import PPE from "@/components/Cockpit/PPE/PPE.vue";

import { handleException } from '@/services/exceptionsHandler'
import { checkPermission, getOperateurs, stringifyAutocomplete, getCurrentUserRoleId, adjustColumnWidths } from '@/services/helper'

export default {
  name: "Cockpit",
  components: {
      Matdiff_secr,
      Matdiff_mo,
      PPE
  },
  data: () => {
    return {
        affaires: [{}],
        affaires_bk: [],
        affaireEtapes: [],
        affaireTypes: [],
        loadingAffaires: true,
        newAffaireAllowed: false,
        operateurs: [],
        refreshAffaire: null,
        searchAffaire: null,
        selectedOperateur_id: -1,
        selectedAffaireTypes_id: [],
        showFinProcessus: false,
        showMatdiff_secr: false,
        showMatdiff_mo: false,
        showPPE: false,
        role: {
            secretaire: Number(process.env.VUE_APP_SECRETAIRE_ROLE_ID),
            mo: Number(process.env.VUE_APP_MO_ROLE_ID),
            ppe: Number(process.env.VUE_APP_PPE_ROLE_ID)
        },
    };
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
                                     checkPermission(process.env.VUE_APP_AFFAIRE_RETABLISSEMENT_PFP3_EDITION) || checkPermission(process.env.VUE_APP_AFFAIRE_PCOP_EDITION) ||
                                     checkPermission(process.env.VUE_APP_AFFAIRE_AUTRE_EDITION);
            
            //Check if role secretaire
            let role_id = getCurrentUserRoleId();
            if ( role_id && !isNaN(role_id) && Number(role_id) === this.role.secretaire  || checkPermission(process.env.VUE_APP_FONCTION_ADMIN) ) {
                this.showMatdiff_secr = true;
            } 
            
            //Check if role MO
            if ( role_id && !isNaN(role_id) && Number(role_id) === this.role.mo  || checkPermission(process.env.VUE_APP_FONCTION_ADMIN) ) {
                this.showMatdiff_mo = true;
            }
            
            //Check if role PPE
            if ( role_id && !isNaN(role_id) && Number(role_id) === this.role.ppe  || checkPermission(process.env.VUE_APP_FONCTION_ADMIN) ) {
                this.showPPE = true;
            }

        }, 500);
    },

    /**
     * get Affaires
     */
    async getAffaire() {
        if (this.affaireEtapes.length === 0) {
            await this.getAffaireEtapes();
        }
        if (this.affaireTypes.length === 0) {
            await this.getAffaireTypes();
        }

        this.$http.get(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_AFFAIRES_COCKPIT_ENDPOINT,
            {
                withCredentials: true,
                headers: {Accept: "application/json"}
            }
        ).then(response => {
            if (response && response.data) {
                let tmp = JSON.parse(response.data);

                tmp = tmp.filter(x => x.etape_id !== Number(process.env.VUE_APP_ETAPE_CHEZ_CLIENT_ID));

                tmp.forEach(x => {
                    for (let i=0; i<this.affaireEtapes.length; i++) {
                        x["dashboard_" + i.toString()] = i === x.etape_ordre-1? (x.no_access? x.no_access: String(x.id)): null;
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
                
                this.selectedAffaireTypes_id = [];
                tmp.forEach(x => this.selectedAffaireTypes_id.push(x.id));

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
            this.affaires = this.affaires.filter(x => {
                let text = [x.no_access + x.id].filter(Boolean).join(' - ');
                return text.toLowerCase().includes(this.searchAffaire.toLowerCase());
            });
        }

        // filter affaire by operateur if specified
        if (this.selectedOperateur_id && this.selectedOperateur_id > 0) {
            this.affaires = this.affaires.filter(x => x.operateur_id === this.selectedOperateur_id);
        }
        
        // filter affaire type
        this.affaires = this.affaires.filter(x => this.selectedAffaireTypes_id.includes(x.affaire_type_id));
        
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
                let currentUserRoleID = getCurrentUserRoleId();
                if (tmp.some(x => (x.id === currentUserID) && x.chef_equipe) && (currentUserRoleID && [this.role.mo, this.role.ppe].includes(currentUserRoleID))) {
                    this.selectedOperateur_id = Number(currentUserID);
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
    adjustColumnWidths();
  },
  
  created() {
    this.refreshAffaire = setInterval(this.getAffaire, 60000); // Recharge le tableau toutes les minutes  
  },

  beforeDestroy() {
    clearInterval(this.refreshAffaire);
  }
};
</script>

