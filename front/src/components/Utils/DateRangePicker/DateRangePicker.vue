<style src="./dateRangePicker.css" scoped></style>
<template src="./dateRangePicker.html"></template>


<script>

import { disabledDates_fct } from '@/services/helper';

export default {
  name: "DateRangePicker",
  props: {
    dateperiod_start: {
      type: Date,
      default() { return new Date(0) }
    },
    dateperiod_end: {
      type: Date,
      default() { return new Date() }
    },
    showPeriodInfo: {
      type: Boolean,
      default: false
    }
  },
  data: () => {
    return {
      date_from: null,
      date_to: null,
      dateperiod_start_: null,
      dateperiod_end_: null,
    };
  },

  methods: {
    disabledDates(date) {
      if (this.date_from) {
        this.dateperiod_start_ = this.date_from;
      } else {
        this.dateperiod_start_ = this.dateperiod_start;
      }

      if (this.date_to) {
        this.dateperiod_end_ = this.date_to;
      } else {
        this.dateperiod_end_ = this.dateperiod_end;
      }

      return disabledDates_fct(date, this.dateperiod_start_, this.dateperiod_end_);
    },
  },
};

</script>
