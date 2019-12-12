var m = require("mithril")

var Patient = {
    list: [],
    informConsentRequestList: [],
    error: "",
    loadList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/patients",
            headers: {
                'ClientKey': clientKey
            }
//            withCredentials: true,
        })
        .then(function(result) {
            Patient.error = ""
            Patient.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            Patient.error = e.message
            Patient.list = []
        })
    },

    inform_consent_request_list: function(clientKey) {   //i.e Investigator
        return m.request({
            method: "GET",
            url: "/api/patients/inform_consent_request_list",
            headers: {
                'ClientKey': clientKey
            }
        })
        .then(function(result) {
            console.log("Get Inform Consent Request List")
            Patient.error = ""
            Patient.informConsentRequestList = result.data
        })
        .catch(function(e) {
            console.log(e)
            Patient.error = e.message
            Patient.informConsentRequestList = []
        })
    },

    sign_inform_consent: function(investigatorPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/patients/sign_inform_consent/" + investigatorPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Patient.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Patient.error = e.message
        })
    },

    decline_inform_consent: function(investigatorPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/patients/decline_inform_consent/" + investigatorPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Patient.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Patient.error = e.message
        })
    },

    current: {},

    register: function() {
        return m.request({
            method: "POST",
            url: "/api/patients",
            data: Patient.current,
            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Patient.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Patient.error = e.message
        })
    }
}

module.exports = Patient