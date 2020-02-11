var m = require("mithril")
var Client = require("../models/Client")

module.exports = {

    oninit:
        function(vnode){
            Client.loadList()
        }
    ,
    view: function(vnode) {
        return m(".user-list", [
            m("label.label", "Client public key"),
            m("input.input[type=text][placeholder=Client public key][disabled=false]", {
                value: Client.list['patient']
            }),
//            m("a.user-list-item", {href: "/doctor_list/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Doctors List"),
//            m("a.user-list-item", {href: "/investigator_list/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Investigator List"),
//            m("a.user-list-item", {href: "/insurance_list/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Insurance List"),
//            m("a.user-list-item", {href: "/payment_list/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Invoice List"),
            m("a.user-list-item", {href: "/patient/new/", oncreate: m.route.link}, "New Patient"),
            m("a.user-list-item", {href: "/patient_list/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Patients List"),
            m("a.user-list-item", "---"),
            m("a.user-list-item", {href: "/hospital_list/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Hospital List"),
//            m("a.user-list-item", "---"),
//            m("a.user-list-item", {href: "/lab_test_list/new/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Add Lab Test"),
//            m("a.user-list-item", {href: "/lab_test_list/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Lab Test List"),
//            m("a.user-list-item", "---"),
//            m("a.user-list-item", {href: "/pulse_list/new/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Add Pulse"),
//            m("a.user-list-item", {href: "/pulse_list/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Pulse List"),
//            m("a.user-list-item", "---"),
//            m("a.user-list-item", {href: "/contract_list/new/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Add Contract"),
//            m("a.user-list-item", {href: "/contract_list/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Contract List"),
            m("a.user-list-item", "---"),
//            m("a.user-list-item", {href: "/trial_data_list/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Trial Data List"),
//            m("a.user-list-item", {href: "/ehr/new/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Register EHR"),
            m("a.user-list-item", {href: "/ehr_list/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "EHRs List"),
            m("a.user-list-item", "---"),
            m("a.user-list-item", {href: "/inform_consent_request_list/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Inform Consent Requests"),
//            m("a.user-list-item", {href: "/first_visit/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "First Visit"),
//            m("a.user-list-item", {href: "/eat_pills/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Eat Pills"),
//            m("a.user-list-item", {href: "/pass_tests/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Pass Tests"),
//            m("a.user-list-item", {href: "/attend_procedures/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Attend Procedures"),
//            m("a.user-list-item", {href: "/next_visit/?client_key=" + Client.list['patient'], oncreate: m.route.link}, "Next Visit"),
        ])

    }
}