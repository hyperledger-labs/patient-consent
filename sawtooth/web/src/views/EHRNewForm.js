var m = require("mithril")
var EHR = require("../models/EHR")

module.exports = {
//    oninit: function(vnode) {User.load(vnode.attrs.id)},
    view: function(vnode) {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    EHR.register(vnode.attrs.client_key)
                }
            }, [
            m("label.label", "Patient pkey"),
            m("input.input[type=text][placeholder=Patient pkey]", {
                oninput: m.withAttr("value", function(value) {EHR.current.patient_pkey = value}),
                value: EHR.current.patient_pkey
            }),
            m("label.label", "ID"),
            m("input.input[placeholder=ID]", {
                oninput: m.withAttr("value", function(value) {EHR.current.id = value}),
                value: EHR.current.id
            }),
            m("label.label", "Height (cm)"),
            m("input.input[placeholder=Height]", {
                oninput: m.withAttr("value", function(value) {EHR.current.height = value}),
                value: EHR.current.height
            }),
            m("label.label", "Weight (kg)"),
            m("input.input[placeholder=Weight]", {
                oninput: m.withAttr("value", function(value) {EHR.current.weight = value}),
                value: EHR.current.weight
            }),
            m("label.label", "A1C (%): Normal (less than 5.7%), Prediabetes	(5.7% to 6.4%), Diabetes (6.5% or higher)"),
            m("input.input[placeholder=A1C]", {
                oninput: m.withAttr("value", function(value) {EHR.current.A1C = value}),
                value: EHR.current.A1C
            }),
            m("label.label", "Fasting Plasma Glucose - FPG (mg/dl): Normal (less than 100 mg/dl), Prediabetes (100 mg/dl to 125 mg/dl), Diabetes (126 mg/dl or higher)"),
            m("input.input[placeholder=FPG]", {
                oninput: m.withAttr("value", function(value) {EHR.current.FPG = value}),
                value: EHR.current.FPG
            }),
            m("label.label", "Oral Glucose Tolerance Test - OGTT (mg/dl): Normal (less than 140 mg/dl), Prediabetes (140 mg/dl to 199 mg/dl), Diabetes (200 mg/dl or higher)"),
            m("input.input[placeholder=OGTT]", {
                oninput: m.withAttr("value", function(value) {EHR.current.OGTT = value}),
                value: EHR.current.OGTT
            }),
            m("label.label", "Random Plasma Glucose Test - RPGT (mg/dl): Diabetes is diagnosed at blood sugar of greater than or equal to 200 mg/dl"),
            m("input.input[placeholder=RPGT]", {
                oninput: m.withAttr("value", function(value) {EHR.current.RPGT = value}),
                value: EHR.current.RPGT
            }),
            m("button.button[type=submit]", "Register"),
            m("label.error", EHR.error)
        ])
    }
}