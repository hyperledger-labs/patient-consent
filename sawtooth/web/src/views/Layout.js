var m = require("mithril")
//var Client = require("../models/Client")

module.exports = {
//    oninit: Client.loadList,
    view: function(vnode) {
        return m("main.layout", [
            m("nav.menu", [
//                m("a[href='/actions']", {oncreate: m.route.link}, "Actions|"),
//                m("a[href='/clinic_list']", {oncreate: m.route.link}, "Clinics|"),
//                m("a[href='/doctor_list']", {oncreate: m.route.link}, "Doctors|"),
//                m("a[href='/patient_list']", {oncreate: m.route.link}, "Patients|"),
//                m("a[href='/lab_test_list']", {oncreate: m.route.link}, "Lab Tests|"),
//                m("a[href='/lab_test_list/new/']", {oncreate: m.route.link}, "Add Lab Test|"),
//                m("a[href='/pulse_list']", {oncreate: m.route.link}, "Pulse List|"),
//                m("a[href='/pulse_list/new/']", {oncreate: m.route.link}, "Add Pulse|"),
                m("a", {href: "/hospital", oncreate: m.route.link}, "As Hospital|"),
//                m("a", {href: "/doctor", oncreate: m.route.link}, "As Doctor|"),
                m("a", {href: "/patient", oncreate: m.route.link}, "As Patient|"),
                m("a", {href: "/investigator", oncreate: m.route.link}, "As Investigator|"),
//                m("a", {href: "/insurance", oncreate: m.route.link}, "As Insurance"),
            ]),
            m("section", vnode.children),
        ])
    }
}