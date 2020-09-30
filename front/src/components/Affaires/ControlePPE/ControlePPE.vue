<style src="./controlePPE.css" scoped></style>
<template src="./controlePPE.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler';
import {checkPermission,
        stringifyAutocomplete} from '@/services/helper';

const moment = require('moment')

export default {
  name: "ControlePPE",
  props: {},
  data: () => ({
    showNewControlePPEBtn: false,
    affaireReadonly: true,
    needToCreateControlePPE: false,
    operateurs_liste: [],
    showCreatedControlePPE: false,
    controlePPE: {},
    controlePPE_all: [],
  }),

  methods: {
    /*
     * SEARCH AFFAIRE-ControlePPE
     */
    async searchControlePPE() {
      await this.searchOperateurs();
      this.$http
        .get(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_AFFAIRE_CONTROLE_PPE_ENDPOINT +
          this.$route.params.id,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        )
        .then(response => {
          if (response && response.data) {
            this.controlePPE_all = response.data; // keep in memory all controles PPE
            this.controlePPE = this.controlePPE_all[this.controlePPE_all.length - 1] // only show the last one

            if (this.controlePPE.operateur_id) {
              this.controlePPE.operateur = this.operateurs_liste.filter(x => x.id === this.controlePPE.operateur_id)[0];
            }
            if (this.controlePPE.date) {
              this.controlePPE.date = moment(this.controlePPE.date, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
            }
          } else {
            // Il n'existe pas encore de suivi de mandat pour cette affaire
            this.needToCreateControlePPE = true;
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * Cherche les opérateurs
     */
    async searchOperateurs() {
      return new Promise((resolve, reject) => {
        this.$http
          .get(
            process.env.VUE_APP_API_URL + process.env.VUE_APP_OPERATEURS_ENDPOINT,
            {
              withCredentials: true,
              headers: {"Accept": "application/json"}
            }
          )
          .then(response => {
            if (response.data) {
              let tmp = response.data;
              tmp.forEach(x => x.nom_ = [x.prenom, x.nom].filter(Boolean).join(" "));
              this.operateurs_liste = stringifyAutocomplete(tmp, "nom_");
              resolve();
            }
          })
          .catch(() => reject);
      })
    },

    /**
     * Création d'un nouveau suivi
     */
    newControlePPE() {
      var formData = new FormData();
      formData.append("affaire_id", this.$route.params.id);
      formData.append("operateur_id", JSON.parse(localStorage.getItem("infolica_user")).id);
      formData.append("date", moment(new Date()).format(process.env.VUE_APP_DATEFORMAT_WS));

      this.$http
        .post(
          process.env.VUE_APP_API_URL +
            process.env.VUE_APP_CONTROLE_PPE_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        )
        .then(response => {
          if (response) {
            this.$root.$emit("ShowMessage", "Le formulaire de contrôle a été créé avec succès")
            this.searchControlePPE();
            this.needToCreateControlePPE = false;
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    onCancelEditControlePPE() {
      this.searchControlePPE();
    },

    onConfirmEditControlePPE() {
      var formData = new FormData();
      formData.append("id", this.controlePPE.id);
      formData.append("affaire_id", this.controlePPE.affaire_id);
      if (this.controlePPE.operateur && this.controlePPE.operateur.id) {formData.append("operateur_id", this.controlePPE.operateur.id)}
      if (this.controlePPE.date) {formData.append("date", this.controlePPE.date)}
      if (this.controlePPE.gen_1) {formData.append("gen_1", this.controlePPE.gen_1)}
      if (this.controlePPE.gen_2) {formData.append("gen_2", this.controlePPE.gen_2)}
      if (this.controlePPE.gen_3) {formData.append("gen_3", this.controlePPE.gen_3)}
      if (this.controlePPE.gen_4) {formData.append("gen_4", this.controlePPE.gen_4)}
      if (this.controlePPE.gen_5) {formData.append("gen_5", this.controlePPE.gen_5)}
      if (this.controlePPE.gen_6) {formData.append("gen_6", this.controlePPE.gen_6)}
      if (this.controlePPE.gen_7) {formData.append("gen_7", this.controlePPE.gen_7)}
      if (this.controlePPE.gen_8) {formData.append("gen_8", this.controlePPE.gen_8)}
      if (this.controlePPE.gen_9) {formData.append("gen_9", this.controlePPE.gen_9)}
      if (this.controlePPE.gen_remarque) {formData.append("gen_remarque", this.controlePPE.gen_remarque)}
      if (this.controlePPE.dos_a) {formData.append("dos_a", this.controlePPE.dos_a)}
      if (this.controlePPE.dos_b) {formData.append("dos_b", this.controlePPE.dos_b)}
      if (this.controlePPE.dos_c) {formData.append("dos_c", this.controlePPE.dos_c)}
      if (this.controlePPE.dos_d) {formData.append("dos_d", this.controlePPE.dos_d)}
      if (this.controlePPE.dos_e) {formData.append("dos_e", this.controlePPE.dos_e)}
      if (this.controlePPE.dos_f) {formData.append("dos_f", this.controlePPE.dos_f)}
      if (this.controlePPE.dos_g) {formData.append("dos_g", this.controlePPE.dos_g)}
      if (this.controlePPE.dos_h) {formData.append("dos_h", this.controlePPE.dos_h)}
      if (this.controlePPE.dos_remarque) {formData.append("dos_remarque", this.controlePPE.dos_remarque)}
      if (this.controlePPE.jur_a) {formData.append("jur_a", this.controlePPE.jur_a)}
      if (this.controlePPE.jur_b) {formData.append("jur_b", this.controlePPE.jur_b)}
      if (this.controlePPE.jur_c) {formData.append("jur_c", this.controlePPE.jur_c)}
      if (this.controlePPE.jur_d) {formData.append("jur_d", this.controlePPE.jur_d)}
      if (this.controlePPE.jur_remarque) {formData.append("jur_remarque", this.controlePPE.jur_remarque)}
      if (this.controlePPE.psit_a) {formData.append("psit_a", this.controlePPE.psit_a)}
      if (this.controlePPE.psit_b) {formData.append("psit_b", this.controlePPE.psit_b)}
      if (this.controlePPE.psit_c) {formData.append("psit_c", this.controlePPE.psit_c)}
      if (this.controlePPE.psit_d) {formData.append("psit_d", this.controlePPE.psit_d)}
      if (this.controlePPE.psit_e) {formData.append("psit_e", this.controlePPE.psit_e)}
      if (this.controlePPE.psit_f) {formData.append("psit_f", this.controlePPE.psit_f)}
      if (this.controlePPE.psit_g) {formData.append("psit_g", this.controlePPE.psit_g)}
      if (this.controlePPE.psit_h) {formData.append("psit_h", this.controlePPE.psit_h)}
      if (this.controlePPE.psit_i) {formData.append("psit_i", this.controlePPE.psit_i)}
      if (this.controlePPE.psit_j) {formData.append("psit_j", this.controlePPE.psit_j)}
      if (this.controlePPE.psit_k) {formData.append("psit_k", this.controlePPE.psit_k)}
      if (this.controlePPE.psit_l) {formData.append("psit_l", this.controlePPE.psit_l)}
      if (this.controlePPE.psit_m) {formData.append("psit_m", this.controlePPE.psit_m)}
      if (this.controlePPE.psit_n) {formData.append("psit_n", this.controlePPE.psit_n)}
      if (this.controlePPE.psit_o) {formData.append("psit_o", this.controlePPE.psit_o)}
      if (this.controlePPE.psit_p) {formData.append("psit_p", this.controlePPE.psit_p)}
      if (this.controlePPE.psit_q) {formData.append("psit_q", this.controlePPE.psit_q)}
      if (this.controlePPE.psit_r) {formData.append("psit_r", this.controlePPE.psit_r)}
      if (this.controlePPE.psit_remarque) {formData.append("psit_remarque", this.controlePPE.psit_remarque)}
      if (this.controlePPE.pet_a) {formData.append("pet_a", this.controlePPE.pet_a)}
      if (this.controlePPE.pet_b) {formData.append("pet_b", this.controlePPE.pet_b)}
      if (this.controlePPE.pet_c) {formData.append("pet_c", this.controlePPE.pet_c)}
      if (this.controlePPE.pet_d) {formData.append("pet_d", this.controlePPE.pet_d)}
      if (this.controlePPE.pet_e) {formData.append("pet_e", this.controlePPE.pet_e)}
      if (this.controlePPE.pet_f) {formData.append("pet_f", this.controlePPE.pet_f)}
      if (this.controlePPE.pet_g) {formData.append("pet_g", this.controlePPE.pet_g)}
      if (this.controlePPE.pet_h) {formData.append("pet_h", this.controlePPE.pet_h)}
      if (this.controlePPE.pet_i) {formData.append("pet_i", this.controlePPE.pet_i)}
      if (this.controlePPE.pet_j) {formData.append("pet_j", this.controlePPE.pet_j)}
      if (this.controlePPE.pet_k) {formData.append("pet_k", this.controlePPE.pet_k)}
      if (this.controlePPE.pet_l) {formData.append("pet_l", this.controlePPE.pet_l)}
      if (this.controlePPE.pet_m) {formData.append("pet_m", this.controlePPE.pet_m)}
      if (this.controlePPE.pet_n) {formData.append("pet_n", this.controlePPE.pet_n)}
      if (this.controlePPE.pet_o) {formData.append("pet_o", this.controlePPE.pet_o)}
      if (this.controlePPE.pet_p) {formData.append("pet_p", this.controlePPE.pet_p)}
      if (this.controlePPE.pet_q) {formData.append("pet_q", this.controlePPE.pet_q)}
      if (this.controlePPE.pet_r) {formData.append("pet_r", this.controlePPE.pet_r)}
      if (this.controlePPE.pet_remarque) {formData.append("pet_remarque", this.controlePPE.pet_remarque)}
      if (this.controlePPE.cart_a) {formData.append("cart_a", this.controlePPE.cart_a)}
      if (this.controlePPE.cart_b) {formData.append("cart_b", this.controlePPE.cart_b)}
      if (this.controlePPE.cart_c) {formData.append("cart_c", this.controlePPE.cart_c)}
      if (this.controlePPE.cart_d) {formData.append("cart_d", this.controlePPE.cart_d)}
      if (this.controlePPE.cart_e) {formData.append("cart_e", this.controlePPE.cart_e)}
      if (this.controlePPE.cart_f) {formData.append("cart_f", this.controlePPE.cart_f)}
      if (this.controlePPE.cart_g) {formData.append("cart_g", this.controlePPE.cart_g)}
      if (this.controlePPE.cart_h) {formData.append("cart_h", this.controlePPE.cart_h)}
      if (this.controlePPE.cart_i) {formData.append("cart_i", this.controlePPE.cart_i)}
      if (this.controlePPE.cart_j) {formData.append("cart_j", this.controlePPE.cart_j)}
      if (this.controlePPE.cart_remarque) {formData.append("cart_remarque", this.controlePPE.cart_remarque)}
      if (this.controlePPE.uet_a) {formData.append("uet_a", this.controlePPE.uet_a)}
      if (this.controlePPE.uet_b) {formData.append("uet_b", this.controlePPE.uet_b)}
      if (this.controlePPE.uet_c) {formData.append("uet_c", this.controlePPE.uet_c)}
      if (this.controlePPE.uet_d) {formData.append("uet_d", this.controlePPE.uet_d)}
      if (this.controlePPE.uet_e) {formData.append("uet_e", this.controlePPE.uet_e)}
      if (this.controlePPE.uet_f) {formData.append("uet_f", this.controlePPE.uet_f)}
      if (this.controlePPE.uet_g) {formData.append("uet_g", this.controlePPE.uet_g)}
      if (this.controlePPE.uet_h) {formData.append("uet_h", this.controlePPE.uet_h)}
      if (this.controlePPE.uet_i) {formData.append("uet_i", this.controlePPE.uet_i)}
      if (this.controlePPE.uet_j) {formData.append("uet_j", this.controlePPE.uet_j)}
      if (this.controlePPE.uet_k) {formData.append("uet_k", this.controlePPE.uet_k)}
      if (this.controlePPE.uet_l) {formData.append("uet_l", this.controlePPE.uet_l)}
      if (this.controlePPE.uet_m) {formData.append("uet_m", this.controlePPE.uet_m)}
      if (this.controlePPE.uet_n) {formData.append("uet_n", this.controlePPE.uet_n)}
      if (this.controlePPE.uet_o) {formData.append("uet_o", this.controlePPE.uet_o)}
      if (this.controlePPE.uet_p) {formData.append("uet_p", this.controlePPE.uet_p)}
      if (this.controlePPE.uet_q) {formData.append("uet_q", this.controlePPE.uet_q)}
      if (this.controlePPE.uet_r) {formData.append("uet_r", this.controlePPE.uet_r)}
      if (this.controlePPE.uet_s) {formData.append("uet_s", this.controlePPE.uet_s)}
      if (this.controlePPE.uet_t) {formData.append("uet_t", this.controlePPE.uet_t)}
      if (this.controlePPE.uet_u) {formData.append("uet_u", this.controlePPE.uet_u)}
      if (this.controlePPE.uet_v) {formData.append("uet_v", this.controlePPE.uet_v)}
      if (this.controlePPE.uet_w) {formData.append("uet_w", this.controlePPE.uet_w)}
      if (this.controlePPE.uet_x) {formData.append("uet_x", this.controlePPE.uet_x)}
      if (this.controlePPE.uet_y) {formData.append("uet_y", this.controlePPE.uet_y)}
      if (this.controlePPE.uet_z) {formData.append("uet_z", this.controlePPE.uet_z)}
      if (this.controlePPE.uet_aa) {formData.append("uet_aa", this.controlePPE.uet_aa)}
      if (this.controlePPE.uet_ab) {formData.append("uet_ab", this.controlePPE.uet_ab)}
      if (this.controlePPE.uet_ac) {formData.append("uet_ac", this.controlePPE.uet_ac)}
      if (this.controlePPE.uet_ad) {formData.append("uet_ad", this.controlePPE.uet_ad)}
      if (this.controlePPE.uet_ae) {formData.append("uet_ae", this.controlePPE.uet_ae)}
      if (this.controlePPE.uet_aremarque) {formData.append("uet_aremarque", this.controlePPE.uet_aremarque)}
      if (this.controlePPE.dup_a) {formData.append("dup_a", this.controlePPE.dup_a)}
      if (this.controlePPE.dup_b) {formData.append("dup_b", this.controlePPE.dup_b)}
      if (this.controlePPE.dup_c) {formData.append("dup_c", this.controlePPE.dup_c)}
      if (this.controlePPE.dup_d) {formData.append("dup_d", this.controlePPE.dup_d)}
      if (this.controlePPE.dup_e) {formData.append("dup_e", this.controlePPE.dup_e)}
      if (this.controlePPE.dup_f) {formData.append("dup_f", this.controlePPE.dup_f)}
      if (this.controlePPE.dup_g) {formData.append("dup_g", this.controlePPE.dup_g)}
      if (this.controlePPE.dup_h) {formData.append("dup_h", this.controlePPE.dup_h)}
      if (this.controlePPE.dup_i) {formData.append("dup_i", this.controlePPE.dup_i)}
      if (this.controlePPE.dup_remarque) {formData.append("dup_remarque", this.controlePPE.dup_remarque)}
      if (this.controlePPE.leg_a) {formData.append("leg_a", this.controlePPE.leg_a)}
      if (this.controlePPE.leg_b) {formData.append("leg_b", this.controlePPE.leg_b)}
      if (this.controlePPE.leg_c) {formData.append("leg_c", this.controlePPE.leg_c)}
      if (this.controlePPE.leg_d) {formData.append("leg_d", this.controlePPE.leg_d)}
      if (this.controlePPE.leg_e) {formData.append("leg_e", this.controlePPE.leg_e)}
      if (this.controlePPE.leg_f) {formData.append("leg_f", this.controlePPE.leg_f)}
      if (this.controlePPE.leg_g) {formData.append("leg_g", this.controlePPE.leg_g)}
      if (this.controlePPE.leg_h) {formData.append("leg_h", this.controlePPE.leg_h)}
      if (this.controlePPE.leg_i) {formData.append("leg_i", this.controlePPE.leg_i)}
      if (this.controlePPE.leg_j) {formData.append("leg_j", this.controlePPE.leg_j)}
      if (this.controlePPE.leg_k) {formData.append("leg_k", this.controlePPE.leg_k)}
      if (this.controlePPE.leg_l) {formData.append("leg_l", this.controlePPE.leg_l)}
      if (this.controlePPE.leg_m) {formData.append("leg_m", this.controlePPE.leg_m)}
      if (this.controlePPE.leg_n) {formData.append("leg_n", this.controlePPE.leg_n)}
      if (this.controlePPE.leg_o) {formData.append("leg_o", this.controlePPE.leg_o)}
      if (this.controlePPE.leg_p) {formData.append("leg_p", this.controlePPE.leg_p)}
      if (this.controlePPE.leg_q) {formData.append("leg_q", this.controlePPE.leg_q)}
      if (this.controlePPE.leg_r) {formData.append("leg_r", this.controlePPE.leg_r)}
      if (this.controlePPE.leg_s) {formData.append("leg_s", this.controlePPE.leg_s)}
      if (this.controlePPE.leg_t) {formData.append("leg_t", this.controlePPE.leg_t)}
      if (this.controlePPE.leg_u) {formData.append("leg_u", this.controlePPE.leg_u)}
      if (this.controlePPE.leg_v) {formData.append("leg_v", this.controlePPE.leg_v)}
      if (this.controlePPE.leg_w) {formData.append("leg_w", this.controlePPE.leg_w)}
      if (this.controlePPE.leg_x) {formData.append("leg_x", this.controlePPE.leg_x)}
      if (this.controlePPE.leg_y) {formData.append("leg_y", this.controlePPE.leg_y)}
      if (this.controlePPE.leg_remarque) {formData.append("leg_remarque", this.controlePPE.leg_remarque)}
      if (this.controlePPE.balsurf_a) {formData.append("balsurf_a", this.controlePPE.balsurf_a)}
      if (this.controlePPE.balsurf_b) {formData.append("balsurf_b", this.controlePPE.balsurf_b)}
      if (this.controlePPE.balsurf_c) {formData.append("balsurf_c", this.controlePPE.balsurf_c)}
      if (this.controlePPE.balsurf_d) {formData.append("balsurf_d", this.controlePPE.balsurf_d)}
      if (this.controlePPE.balsurf_remarque) {formData.append("balsurf_remarque", this.controlePPE.balsurf_remarque)}

      this.$http
        .put(
          process.env.VUE_APP_API_URL +
          process.env.VUE_APP_CONTROLE_PPE_ENDPOINT,
          formData,
          {
            withCredentials: true,
            headers: {"Accept": "application/json"}
          }
        )
        .then(response => {
          if (response) {
            this.$root.$emit("ShowMessage", "Le formulaire de contrôle a été mis à jour avec succès")
            this.searchControlePPE();
          }
        })
        .catch(err => {
          handleException(err, this);
        });
    },

    /**
     * get formular operateur
     */
    getFormOperateur() {
      if (typeof this.controlePPE.operateur === "string") {
        this.controlePPE.operateur = this.operateurs_liste.filter(x => x.nom === this.controlePPE.operateur)[0];
      }
    }
  },

  mounted: function() {
    this.searchControlePPE();
    this.searchOperateurs();

    this.affaireReadonly = !checkPermission(process.env.VUE_APP_AFFAIRE_CONTROLE_EDITION) || this.$parent.parentAffaireReadOnly;
  }
};
</script>



