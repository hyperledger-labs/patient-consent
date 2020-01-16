var m = require("mithril")
var EHR = require("../models/EHR")

module.exports = {
    oninit:
        function(vnode){
            EHR.loadList(vnode.attrs.client_key)
        },
    view: function(vnode) {
        return m(".user-list", EHR.list.map(function(ehr) {
            return m("a.user-list-item", // {href: "/claim/" + claim.clinic_pkey + "/" + claim.claim_id, oncreate: m.route.link},
                "NAME: " + ehr.name +
                "; SURNAME: " + ehr.surname +
                "; ID: " + ehr.id +
                "; CLIENT PKEY: " + ehr.client_pkey +
                "; FIELD 1: " + ehr.field_1 +
                "; FIELD 2: " + ehr.field_2 +
                "; TIMESTAMP: " + ehr.event_time +
                ";"
//                ,
//                m("div"),
//                m("button", {
//                    onclick: function() {
//                        EHR.current.claim_id = claim.id
//                        EHR.current.client_pkey = claim.client_pkey
////                        Claim.current.provided_service = "pills, lab tests"
//                        EHR.current.contract_id = claim.contract_id
//                        EHR.update(vnode.attrs.client_key)
//                    }
//                }, 'Update claim'),
//                m("div"),
//                m("button", {
//                    onclick: function() {
//                        Claim.current.claim_id = claim.id
//                        Claim.current.client_pkey = claim.client_pkey
////                        Claim.current.provided_service = "pills, lab tests"
//                        Claim.current.contract_id = claim.contract_id
//                        Claim.close(vnode.attrs.client_key)
//                    }
//                }, 'Close claim')
            )
        }),
//        m("label.label", "Provided Service"),
//        m("input.input[placeholder=Provided Service]", {
//            oninput: m.withAttr("value", function(value) {Claim.current.provided_service = value}),
//            value: Claim.current.provided_service
//        }),
        m("label.error", EHR.error))
    }
}