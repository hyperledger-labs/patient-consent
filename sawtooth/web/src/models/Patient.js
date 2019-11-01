var m = require("mithril")

var Patient = {
    list: [],
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