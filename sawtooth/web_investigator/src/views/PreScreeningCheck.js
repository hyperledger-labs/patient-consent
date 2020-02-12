var m = require("mithril")
var EHR = require("../models/EHR")
var Investigator = require("../models/Investigator")

module.exports = {
    oninit:
        function(vnode){
            EHR.screening_data(vnode.attrs.client_key)
        },
    view: function(vnode) {
        return m(".user-list", EHR.sharedDataList.map(function(ehr) {
            return m("a.user-list-item", // {href: "/claim/" + claim.clinic_pkey + "/" + claim.claim_id, oncreate: m.route.link},
                "NAME: " + ehr.name +
                "; SURNAME: " + ehr.surname +
                "; ID: " + ehr.id +
                "; CLIENT PKEY: " + ehr.client_pkey +
                "; Height: " + ehr.height +
                "; Weight: " + ehr.weight +
                "; A1C: " + ehr.A1C +
                "; FPG: " + ehr.FPG +
                "; OGTT: " + ehr.OGTT +
                "; RPGT: " + ehr.RPGT +
                "; TIMESTAMP: " + ehr.event_time +
                ";",
                m("div"),
                m("button", {
                    onclick: function() {
                        Investigator.request_inform_consent(ehr.client_pkey, vnode.attrs.client_key)
                    }
                }, 'Request inform consent'),
//                m("button", {
//                    onclick: function() {
//                        EHR.current.claim_id = claim.id
//                        EHR.current.client_pkey = claim.client_pkey
////                        Claim.current.provided_service = "pills, lab tests"
//                        EHR.current.contract_id = claim.contract_id
//                        EHR.update(vnode.attrs.client_key)
//                    }
//                }, 'Update claim'),
                m("div"),
                m("button", {
                    onclick: function() {
                        Investigator.import_to_trial_data(ehr.id, ehr.client_pkey, vnode.attrs.client_key)
                    }
                }, 'Import to trial data')
                )
            }),
//        m("label.label", "Provided Service"),
//        m("input.input[placeholder=Provided Service]", {
//            oninput: m.withAttr("value", function(value) {Claim.current.provided_service = value}),
//            value: Claim.current.provided_service
//        }),
            m("div"),
            m("label.label", "Inclusion/Exclusion criteria"),
            m("input.input[type=text][placeholder=Example: excl_height_less=2]", {
                oninput: m.withAttr("value", function(value) {EHR.current.incl_excl_criteria = value}),
                value: EHR.current.incl_excl_criteria1
            }),
            m("div"),
            m("button", {
                onclick: function() {
                    EHR.screening_data(vnode.attrs.client_key, EHR.current.incl_excl_criteria)
                }
            }, 'Get Pre-Screening Data (incl. excl. criteria)'),
            m("label.error", EHR.error),
            m("div"),
            m("label.error", Investigator.error)
        )
    }
}