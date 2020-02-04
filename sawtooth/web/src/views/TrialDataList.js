var m = require("mithril")
var Investigator = require("../models/Investigator")

module.exports = {
    oninit:
        function(vnode){
            Investigator.loadTrialDataList(vnode.attrs.client_key)
        },
    view: function(vnode) {
        return m(".user-list", Investigator.trialDataList.map(function(data) {
            return m("a.user-list-item", // {href: "/claim/" + claim.clinic_pkey + "/" + claim.claim_id, oncreate: m.route.link},
                "ID: " + data.id +
                "; Height: " + data.height +
                "; Weight: " + data.weight +
                "; A1C: " + data.A1C +
                "; FPG: " + data.FPG +
                "; OGTT: " + data.OGTT +
                "; RPGT: " + data.RPGT +
                "; TIMESTAMP: " + data.event_time +
                "; IS ELIGIBLE?: " + data.eligible +
                ";",
                m("div"),
                m("button", {
                    onclick: function() {
                        Investigator.trialData.id = data.id
                        Investigator.trialData.height?Investigator.trialData.height:data.height
                        Investigator.trialData.weight?Investigator.trialData.weight:data.weight
                        Investigator.trialData.A1C?Investigator.trialData.A1C:data.A1C
                        Investigator.trialData.FPG?Investigator.trialData.FPG:data.FPG
                        Investigator.trialData.OGTT?Investigator.trialData.OGTT:data.OGTT
                        Investigator.trialData.RPGT?Investigator.trialData.RPGT:data.RPGT
                        Investigator.update_trial_data(vnode.attrs.client_key)
                    }
                }, 'Update trial data item'),
                m("div"),
                m("button", {
                    onclick: function() {
                        Investigator.trialData.id = data.id
                        Investigator.trialData.eligible = true
                        Investigator.set_eligible(vnode.attrs.client_key)
                    }
                }, 'Set eligible'),
                m("button", {
                    onclick: function() {
                        Investigator.trialData.id = data.id
                        Investigator.trialData.eligible = false
                        Investigator.set_eligible(vnode.attrs.client_key)
                    }
                }, 'Set not eligible')
            )
        }),
        m("label.label", "Height"),
        m("input.input[placeholder=Height]", {
            oninput: m.withAttr("value", function(value) {Investigator.trialData.height = value}),
            value: Investigator.trialData.height
        }),
        m("label.label", "Weight"),
        m("input.input[placeholder=Weight]", {
            oninput: m.withAttr("value", function(value) {Investigator.trialData.weight = value}),
            value: Investigator.trialData.weight
        }),
        m("label.label", "A1C"),
        m("input.input[placeholder=A1C]", {
            oninput: m.withAttr("value", function(value) {Investigator.trialData.A1C = value}),
            value: Investigator.trialData.A1C
        }),
        m("label.label", "FPG"),
        m("input.input[placeholder=FPG]", {
            oninput: m.withAttr("value", function(value) {Investigator.trialData.FPG = value}),
            value: Investigator.trialData.FPG
        }),
        m("label.label", "OGTT"),
        m("input.input[placeholder=OGTT]", {
            oninput: m.withAttr("value", function(value) {Investigator.trialData.OGTT = value}),
            value: Investigator.trialData.OGTT
        }),
        m("label.label", "RPGT"),
        m("input.input[placeholder=RPGT]", {
            oninput: m.withAttr("value", function(value) {Investigator.trialData.RPGT = value}),
            value: Investigator.trialData.RPGT
        }),
        m("label.error", Investigator.error))
    }
}