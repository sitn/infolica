<style src="./quittancePCOP.css" scoped></style>
<template src="./quittancePCOP.html"></template>


<script>
import { handleException } from "@/services/exceptionsHandler";
import {
  getCurrentDate,
  getCadastres,
  stringifyAutocomplete
} from "@/services/helper";
import moment from "moment";

export default {
  name: "quittancePCOP",
  props: {
    affaire: { type: Object },
    affaire_numeros_anciens: { type: Array },
    affaire_numeros_nouveaux: { type: Array }
  },
  components: {},
  data: () => ({
    form: {
      titre: null,
      nom_prenom: null,
      adresse: null,
      npa: null,
      localite: null,
      nref: null,
      vref: null,
      dateEnvoi: null,
      civilite: null,
      dateDemande: null,
      numerosReserves: null,
      nombreNumerosReserves: null,
      bfBase: null,
      cadastre: null
    },
    showQuittancePCOPDialog: false,
    cadastres_liste: [],
    numeros_pcop: [],
    numeros_base: []
  }),

  methods: {
    /**
     * Ouvrir le dialog
     */
    openQuittancePCOPDialog() {
      this.showQuittancePCOPDialog = true;
      this.getNumerosReservesPCOP();
    },

    /**
     * get cadastres
     */
    initCadastresListe() {
      getCadastres()
        .then(
          response =>
            (this.cadastres_liste = stringifyAutocomplete(response.data))
        )
        .catch(err => handleException(err, this));
    },

    /***
     * Get client from affaire.client_commande_id
     */
    async getClientAffaire() {
      this.$http.get(
        process.env.VUE_APP_API_URL +
        process.env.VUE_APP_CLIENTS_ENDPOINT +
        "/" + this.affaire.client_commande_id,
        {
          withCredentials: true,
          headers: { Accept: "application/json" }
        }
      ).then(response => {
        if (response && response.data) {
          const client = response.data;
          this.form.titre = client.titre;
          this.form.nom_prenom = client.prenom === null? client.nom : client.nom +  " "  + client.prenom;
          this.form.adresse = client.adresse;
          this.form.npa = client.npa;
          this.form.localite = client.localite;
        }
      });
    },

    /**
     * Récupère les nouveaux numéros de type PCOP
     */
    getNumerosReservesPCOP() {
      this.numeros_pcop = this.affaire_numeros_nouveaux.filter(x => x.numero_type_id===Number(process.env.VUE_APP_NUMERO_TYPE_PCOP) && x.active);
      this.numeros_base = [];
      let tmp = [];
      // Get set of unique BF base
      this.affaire_numeros_nouveaux.map(x => {
        if (!tmp.includes(x.numero_base_id) && x.numero_base_id !== null && x.active){
          tmp.push(x.numero_base_id);
          this.numeros_base.push({numero_base: x.numero_base, numero_base_id: x.numero_base_id});
        }
      });
    },

    /**
     * Update les numéros de et à en fonction du BF de base
     */
    updateNumerosPCOP() {
      const tmp = [];
      this.affaire_numeros_nouveaux.filter(x => x.numero_base === this.form.bfBase).map(x => {if (x.active) tmp.push(x.numero)});
      this.form.numeros_de = Math.min(...tmp);
      this.form.numeros_a = Math.max(...tmp);
    },


    /**
     * Initialiser le formulaire Dialog
     */
    initForm() {
      this.getClientAffaire();
      this.form = {
        nref: "",
        vref: this.affaire.vref,
        dateEnvoi: getCurrentDate(),
        civilite: "",
        dateDemande: moment(this.affaire.date_ouverture, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT),
        numeros_de: "",
        numeros_a: "",
        nombreNumerosReserves: "",
        bfBase: "",
        cadastre: this.affaire.cadastre
      };
    },

    /**
     * Créer la quittance de création de parts de copropriétés
     */
    callCreateQuittancePCOP() {
      let formData = new FormData();

      formData.append("template", "QuittancePCOP");
      formData.append(
        "values",
        JSON.stringify({
          TITRE: this.form.titre,
          NOMPRENOM: this.form.nom_prenom,
          ADRESSE: this.form.adresse,
          NPALOCALITE: this.form.npa + " " + this.form.localite,
          NREF: this.form.nref === "" ? String(this.affaire.id) : String(this.affaire.id) + "-" + this.form.nref,
          VREF: String(this.form.vref),
          DATEENVOI: String(this.form.dateEnvoi),
          CIVILITE: this.form.titre,
          DATEDEMANDE: String(this.form.dateDemande),
          NUMEROSRESERVES: String(this.form.numeros_de) + " à " + String(this.form.numeros_a),
          NOMBRENUMEROS: String(Number(this.form.numeros_a)-Number(this.form.numeros_de)+1),
          BIENFONDSBASE: String(this.form.bfBase),
          CADASTRE: this.form.cadastre
        })
      );

      this.$http
        .post(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_COURRIER_TEMPLATE_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: { Accept: "application/html" }
          }
        )
        .then(response => {
          if (response && response.data) {
            this.downloadQuittancePCOP(response.data.filename);
            this.deleteQuittancePCOP(response.data.filename);
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Download QuittancePCOP
     */
    downloadQuittancePCOP(filename) {
      let url =
        process.env.VUE_APP_API_URL +
        process.env.VUE_APP_COURRIER_TEMPLATE_ENDPOINT +
        "?filename=" +
        filename;
      window.open(url, "_blank");
    },

    /**
     * Delete quittancePCOP
     */
    deleteQuittancePCOP(filename) {
      this.$http
        .delete(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_COURRIER_TEMPLATE_ENDPOINT +
            "?filename=" +
            filename,
          {
            withCredentials: true,
            headers: { Accept: "application/html" }
          }
        )
        .then(response => {
          if (response && response.data) {
            this.$root.$emit(
              "ShowMessage",
              "Le fichier '" +
                filename +
                "' se trouve dans le dossier 'Téléchargement'"
            );
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    }
  },
  mounted: function() {
    this.initForm();
    this.initCadastresListe();
  }
};
</script>



