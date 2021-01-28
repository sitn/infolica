<style src="./controlePPE.css" scoped></style>
<template src="./controlePPE.html"></template>


<script>
import {handleException} from '@/services/exceptionsHandler';
import {checkPermission,
        stringifyAutocomplete,
        logAffaireEtape} from '@/services/helper';

const moment = require('moment')

export default {
  name: "ControlePPE",
  props: {
    affaire: Object
  },
  data: () => ({
    affaireReadonly: true,
    check_all: false,
    controlePPE: {},
    controlePPE_all: [],
    controlePPE_dates_liste: [],
    currentControle: null,
    operateurs_liste: [],
    showCancelSaveBtn: true,
    showCreatedControlePPE: false,
    showNewControlePPEBtn: false,
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
            let tmp = response.data;

            if (tmp.length > 0) {
              tmp.forEach(x => {
                if (x.operateur_id) {
                  x.operateur = this.operateurs_liste.filter(y => y.id === x.operateur_id)[0];
                }
                if (x.date) {
                  x.date = moment(x.date, process.env.VUE_APP_DATEFORMAT_WS).format(process.env.VUE_APP_DATEFORMAT_CLIENT);
                }

                x.nom_ = [x.date, x.operateur.nom].join(" - ")
              });
  
              this.controlePPE_all = tmp; // keep in memory all controles PPE
              this.controlePPE_dates_liste = stringifyAutocomplete(tmp, "nom_");
  
              this.controlePPE = this.controlePPE_all[this.controlePPE_all.length - 1]; // only show the last one
              this.currentControle = this.controlePPE.id;
            }
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
            this.$root.$emit("ShowMessage", "Le formulaire de contrôle a été créé avec succès");
            this.showCancelSaveBtn = true;

            //Log edition facture
            logAffaireEtape(this.affaire.id, Number(process.env.VUE_APP_ETAPE_CONTROLE_PPE_ID), "Création d'un nouveau formulaire");

            this.searchControlePPE();
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
      formData.append("gen_1", this.controlePPE.gen_1);
      formData.append("gen_2", this.controlePPE.gen_2);
      formData.append("gen_3", this.controlePPE.gen_3);
      formData.append("gen_4", this.controlePPE.gen_4);
      formData.append("gen_5", this.controlePPE.gen_5);
      formData.append("gen_6", this.controlePPE.gen_6);
      formData.append("gen_7", this.controlePPE.gen_7);
      formData.append("gen_8", this.controlePPE.gen_8);
      formData.append("gen_9", this.controlePPE.gen_9);
      if (this.controlePPE.gen_remarque) {formData.append("gen_remarque", this.controlePPE.gen_remarque)}
      formData.append("dos_a", this.controlePPE.dos_a);
      formData.append("dos_b", this.controlePPE.dos_b);
      formData.append("dos_c", this.controlePPE.dos_c);
      formData.append("dos_d", this.controlePPE.dos_d);
      formData.append("dos_e", this.controlePPE.dos_e);
      formData.append("dos_f", this.controlePPE.dos_f);
      formData.append("dos_g", this.controlePPE.dos_g);
      formData.append("dos_h", this.controlePPE.dos_h);
      if (this.controlePPE.dos_remarque) {formData.append("dos_remarque", this.controlePPE.dos_remarque)}
      formData.append("jur_a", this.controlePPE.jur_a);
      formData.append("jur_b", this.controlePPE.jur_b);
      formData.append("jur_c", this.controlePPE.jur_c);
      formData.append("jur_d", this.controlePPE.jur_d);
      if (this.controlePPE.jur_remarque) {formData.append("jur_remarque", this.controlePPE.jur_remarque)}
      formData.append("psit_a", this.controlePPE.psit_a);
      formData.append("psit_b", this.controlePPE.psit_b);
      formData.append("psit_c", this.controlePPE.psit_c);
      formData.append("psit_d", this.controlePPE.psit_d);
      formData.append("psit_e", this.controlePPE.psit_e);
      formData.append("psit_f", this.controlePPE.psit_f);
      formData.append("psit_g", this.controlePPE.psit_g);
      formData.append("psit_h", this.controlePPE.psit_h);
      formData.append("psit_i", this.controlePPE.psit_i);
      formData.append("psit_j", this.controlePPE.psit_j);
      formData.append("psit_k", this.controlePPE.psit_k);
      formData.append("psit_l", this.controlePPE.psit_l);
      formData.append("psit_m", this.controlePPE.psit_m);
      formData.append("psit_n", this.controlePPE.psit_n);
      formData.append("psit_o", this.controlePPE.psit_o);
      formData.append("psit_p", this.controlePPE.psit_p);
      formData.append("psit_q", this.controlePPE.psit_q);
      formData.append("psit_r", this.controlePPE.psit_r);
      formData.append("psit_s", this.controlePPE.psit_s);
      formData.append("psit_t", this.controlePPE.psit_t);
      formData.append("psit_u", this.controlePPE.psit_u);
      formData.append("psit_v", this.controlePPE.psit_v);
      formData.append("psit_w", this.controlePPE.psit_w);
      formData.append("psit_x", this.controlePPE.psit_x);
      formData.append("psit_y", this.controlePPE.psit_y);
      formData.append("psit_z", this.controlePPE.psit_z);
      if (this.controlePPE.psit_remarque) {formData.append("psit_remarque", this.controlePPE.psit_remarque)}
      formData.append("pet_a", this.controlePPE.pet_a);
      formData.append("pet_b", this.controlePPE.pet_b);
      formData.append("pet_c", this.controlePPE.pet_c);
      formData.append("pet_d", this.controlePPE.pet_d);
      formData.append("pet_e", this.controlePPE.pet_e);
      formData.append("pet_f", this.controlePPE.pet_f);
      formData.append("pet_g", this.controlePPE.pet_g);
      formData.append("pet_h", this.controlePPE.pet_h);
      formData.append("pet_i", this.controlePPE.pet_i);
      formData.append("pet_j", this.controlePPE.pet_j);
      formData.append("pet_k", this.controlePPE.pet_k);
      formData.append("pet_l", this.controlePPE.pet_l);
      formData.append("pet_m", this.controlePPE.pet_m);
      formData.append("pet_n", this.controlePPE.pet_n);
      formData.append("pet_o", this.controlePPE.pet_o);
      formData.append("pet_p", this.controlePPE.pet_p);
      formData.append("pet_q", this.controlePPE.pet_q);
      formData.append("pet_r", this.controlePPE.pet_r);
      if (this.controlePPE.pet_remarque) {formData.append("pet_remarque", this.controlePPE.pet_remarque)}
      formData.append("cart_a", this.controlePPE.cart_a);
      formData.append("cart_b", this.controlePPE.cart_b);
      formData.append("cart_c", this.controlePPE.cart_c);
      formData.append("cart_d", this.controlePPE.cart_d);
      formData.append("cart_e", this.controlePPE.cart_e);
      formData.append("cart_f", this.controlePPE.cart_f);
      formData.append("cart_g", this.controlePPE.cart_g);
      formData.append("cart_h", this.controlePPE.cart_h);
      formData.append("cart_i", this.controlePPE.cart_i);
      formData.append("cart_j", this.controlePPE.cart_j);
      if (this.controlePPE.cart_remarque) {formData.append("cart_remarque", this.controlePPE.cart_remarque)}
      formData.append("uet_a", this.controlePPE.uet_a);
      formData.append("uet_b", this.controlePPE.uet_b);
      formData.append("uet_c", this.controlePPE.uet_c);
      formData.append("uet_d", this.controlePPE.uet_d);
      formData.append("uet_e", this.controlePPE.uet_e);
      formData.append("uet_f", this.controlePPE.uet_f);
      formData.append("uet_g", this.controlePPE.uet_g);
      formData.append("uet_h", this.controlePPE.uet_h);
      formData.append("uet_i", this.controlePPE.uet_i);
      formData.append("uet_j", this.controlePPE.uet_j);
      formData.append("uet_k", this.controlePPE.uet_k);
      formData.append("uet_l", this.controlePPE.uet_l);
      formData.append("uet_m", this.controlePPE.uet_m);
      formData.append("uet_n", this.controlePPE.uet_n);
      formData.append("uet_o", this.controlePPE.uet_o);
      formData.append("uet_p", this.controlePPE.uet_p);
      formData.append("uet_q", this.controlePPE.uet_q);
      formData.append("uet_r", this.controlePPE.uet_r);
      formData.append("uet_s", this.controlePPE.uet_s);
      formData.append("uet_t", this.controlePPE.uet_t);
      formData.append("uet_u", this.controlePPE.uet_u);
      formData.append("uet_v", this.controlePPE.uet_v);
      formData.append("uet_w", this.controlePPE.uet_w);
      formData.append("uet_x", this.controlePPE.uet_x);
      formData.append("uet_y", this.controlePPE.uet_y);
      formData.append("uet_z", this.controlePPE.uet_z);
      formData.append("uet_aa", this.controlePPE.uet_aa);
      formData.append("uet_ab", this.controlePPE.uet_ab);
      formData.append("uet_ac", this.controlePPE.uet_ac);
      formData.append("uet_ad", this.controlePPE.uet_ad);
      formData.append("uet_ae", this.controlePPE.uet_ae);
      if (this.controlePPE.uet_remarque) {formData.append("uet_remarque", this.controlePPE.uet_remarque)}
      formData.append("dup_a", this.controlePPE.dup_a);
      formData.append("dup_b", this.controlePPE.dup_b);
      formData.append("dup_c", this.controlePPE.dup_c);
      formData.append("dup_d", this.controlePPE.dup_d);
      formData.append("dup_e", this.controlePPE.dup_e);
      formData.append("dup_f", this.controlePPE.dup_f);
      formData.append("dup_g", this.controlePPE.dup_g);
      formData.append("dup_h", this.controlePPE.dup_h);
      formData.append("dup_i", this.controlePPE.dup_i);
      if (this.controlePPE.dup_remarque) {formData.append("dup_remarque", this.controlePPE.dup_remarque)}
      formData.append("leg_a", this.controlePPE.leg_a);
      formData.append("leg_b", this.controlePPE.leg_b);
      formData.append("leg_c", this.controlePPE.leg_c);
      formData.append("leg_d", this.controlePPE.leg_d);
      formData.append("leg_e", this.controlePPE.leg_e);
      formData.append("leg_f", this.controlePPE.leg_f);
      formData.append("leg_g", this.controlePPE.leg_g);
      formData.append("leg_h", this.controlePPE.leg_h);
      formData.append("leg_i", this.controlePPE.leg_i);
      formData.append("leg_j", this.controlePPE.leg_j);
      formData.append("leg_k", this.controlePPE.leg_k);
      formData.append("leg_l", this.controlePPE.leg_l);
      formData.append("leg_m", this.controlePPE.leg_m);
      formData.append("leg_n", this.controlePPE.leg_n);
      formData.append("leg_o", this.controlePPE.leg_o);
      formData.append("leg_p", this.controlePPE.leg_p);
      formData.append("leg_q", this.controlePPE.leg_q);
      formData.append("leg_r", this.controlePPE.leg_r);
      formData.append("leg_s", this.controlePPE.leg_s);
      formData.append("leg_t", this.controlePPE.leg_t);
      formData.append("leg_u", this.controlePPE.leg_u);
      formData.append("leg_v", this.controlePPE.leg_v);
      formData.append("leg_w", this.controlePPE.leg_w);
      formData.append("leg_x", this.controlePPE.leg_x);
      formData.append("leg_y", this.controlePPE.leg_y);
      if (this.controlePPE.leg_remarque) {formData.append("leg_remarque", this.controlePPE.leg_remarque)}
      formData.append("balsurf_a", this.controlePPE.balsurf_a);
      formData.append("balsurf_b", this.controlePPE.balsurf_b);
      formData.append("balsurf_c", this.controlePPE.balsurf_c);
      formData.append("balsurf_d", this.controlePPE.balsurf_d);
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
            this.$root.$emit("ShowMessage", "Le formulaire de contrôle a été mis à jour avec succès");
            this.check_all = false;
            this.searchControlePPE();

            //Log edition facture
            logAffaireEtape(this.affaire.id, Number(process.env.VUE_APP_ETAPE_CONTROLE_PPE_ID), "Edition du formulaire");
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
    },

    /**
     * Update view controle formulaire by date
     */
    updateControleByDate(controle_id) {
      this.controlePPE = this.controlePPE_all.filter(x => x.id === controle_id)[0];
      
      // Check si le controle PPE est le plus récent ou non pour afficher ou non les boutons cancel et save
      let controle_id_list = [];
      this.controlePPE_all.forEach(x => controle_id_list.push(x.id));
      if (controle_id === Math.max(...controle_id_list)) {
        this.showCancelSaveBtn = true;
      } else {
        this.showCancelSaveBtn = false;
      }
    },

    /**
     * Update state of all checkboxes of formulaire
     */
    updateCheckboxesState(state) {
      for (const key in this.controlePPE) {
        if (key !== "id" && key !== "date" && key !== "operateur" && key !== "affaire_id" && !key.includes("remarque")) {
          this.controlePPE[key] = state;
        }
      }
    },

    /**
     * init form
     */
    initForm() {
      this.controlePPE = {
        gen_1: false,
        gen_2: false,
        gen_3: false,
        gen_4: false,
        gen_5: false,
        gen_6: false,
        gen_7: false,
        gen_8: false,
        gen_9: false,
        gen_remarque: '',
        dos_a: false,
        dos_b: false,
        dos_c: false,
        dos_d: false,
        dos_e: false,
        dos_f: false,
        dos_g: false,
        dos_h: false,
        dos_remarque: '',
        jur_a: false,
        jur_b: false,
        jur_c: false,
        jur_d: false,
        jur_remarque: '',
        psit_a: false,
        psit_b: false,
        psit_c: false,
        psit_d: false,
        psit_e: false,
        psit_f: false,
        psit_g: false,
        psit_h: false,
        psit_i: false,
        psit_j: false,
        psit_k: false,
        psit_l: false,
        psit_m: false,
        psit_n: false,
        psit_o: false,
        psit_p: false,
        psit_q: false,
        psit_r: false,
        psit_s: false,
        psit_t: false,
        psit_u: false,
        psit_v: false,
        psit_w: false,
        psit_x: false,
        psit_y: false,
        psit_z: false,
        psit_remarque: '',
        pet_a: false,
        pet_b: false,
        pet_c: false,
        pet_d: false,
        pet_e: false,
        pet_f: false,
        pet_g: false,
        pet_h: false,
        pet_i: false,
        pet_j: false,
        pet_k: false,
        pet_l: false,
        pet_m: false,
        pet_n: false,
        pet_o: false,
        pet_p: false,
        pet_q: false,
        pet_r: false,
        pet_remarque: '',
        cart_a: false,
        cart_b: false,
        cart_c: false,
        cart_d: false,
        cart_e: false,
        cart_f: false,
        cart_g: false,
        cart_h: false,
        cart_i: false,
        cart_j: false,
        cart_remarque: '',
        uet_a: false,
        uet_b: false,
        uet_c: false,
        uet_d: false,
        uet_e: false,
        uet_f: false,
        uet_g: false,
        uet_h: false,
        uet_i: false,
        uet_j: false,
        uet_k: false,
        uet_l: false,
        uet_m: false,
        uet_n: false,
        uet_o: false,
        uet_p: false,
        uet_q: false,
        uet_r: false,
        uet_s: false,
        uet_t: false,
        uet_u: false,
        uet_v: false,
        uet_w: false,
        uet_x: false,
        uet_y: false,
        uet_z: false,
        uet_aa: false,
        uet_ab: false,
        uet_ac: false,
        uet_ad: false,
        uet_ae: false,
        uet_remarque: '',
        dup_a: false,
        dup_b: false,
        dup_c: false,
        dup_d: false,
        dup_e: false,
        dup_f: false,
        dup_g: false,
        dup_h: false,
        dup_i: false,
        dup_remarque: '',
        leg_a: false,
        leg_b: false,
        leg_c: false,
        leg_d: false,
        leg_e: false,
        leg_f: false,
        leg_g: false,
        leg_h: false,
        leg_i: false,
        leg_j: false,
        leg_k: false,
        leg_l: false,
        leg_m: false,
        leg_n: false,
        leg_o: false,
        leg_p: false,
        leg_q: false,
        leg_r: false,
        leg_s: false,
        leg_t: false,
        leg_u: false,
        leg_v: false,
        leg_w: false,
        leg_x: false,
        leg_y: false,
        leg_remarque: '',
        balsurf_a: false,
        balsurf_b: false,
        balsurf_c: false,
        balsurf_d: false,
        balsurf_remarque: ''
      }
    }
  },

  mounted: function() {
    this.initForm();
    this.searchControlePPE();
    this.searchOperateurs();

    this.affaireReadonly = !checkPermission(process.env.VUE_APP_AFFAIRE_CONTROLE_EDITION) || this.$parent.parentAffaireReadOnly;
  }
};
</script>



