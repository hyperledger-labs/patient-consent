var m = require("mithril")

var Hospital = {
    list: [],
    error: "",
    loadList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/hospitals",
            headers: {
                'ClientKey': clientKey
            }
//            url: "https://rem-rest-api.herokuapp.com/api/users",
//               url: "http://localhost:8008/state?address=3d804901bbfeb7",
//            withCredentials: true,
//            withCredentials: true,
//            credentials: 'include',
        })
        .then(function(result) {
            console.log("Get hospitals list")
            Hospital.error = ""
            Hospital.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            Hospital.error = e.message
            Hospital.list = []
        })
    },

    current: {},

    register: function() {
        return m.request({
            method: "POST",
            url: "/api/hospitals",
            data: Hospital.current,
            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Hospital.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Hospital.error = e.message
        })
    },

    grant_read_ehr: function(clinicPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/patients/grant_read_ehr/" + clinicPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Hospital.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Hospital.error = e.message
        })
    },

    revoke_read_ehr: function(clinicPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/patients/revoke_read_ehr/" + clinicPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Hospital.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Hospital.error = e.message
        })
    },

    grant_write_ehr: function(clinicPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/patients/grant_write_ehr/" + clinicPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Hospital.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Hospital.error = e.message
        })
    },

    revoke_write_ehr: function(clinicPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/patients/revoke_write_ehr/" + clinicPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Hospital.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Hospital.error = e.message
        })
    }
}

module.exports = Hospital