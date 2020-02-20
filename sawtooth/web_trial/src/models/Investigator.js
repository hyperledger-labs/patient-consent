var m = require("mithril")

var Investigator = {
    list: [],
    trialDataList: [],
    error: "",
    loadList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/investigators",
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
            console.log("Get investigator list")
            Investigator.error = ""
            Investigator.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            Investigator.error = e.message
            Investigator.list = []
        })
    },

    loadTrialDataList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/investigators/data",
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
            console.log("Get trial data list")
            Investigator.error = ""
            Investigator.trialDataList = result.data
        })
        .catch(function(e) {
            console.log(e)
            Investigator.error = e.message
            Investigator.trialDataList = []
        })
    },

    current: {},

    trialData: {},

    register: function() {
        return m.request({
            method: "POST",
            url: "/api/investigators",
            data: Investigator.current,
            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Investigator.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Investigator.error = e.message
        })
    },

    grant_investigator_access: function(investigatorPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/hospitals/grant_investigator_access/" + investigatorPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Investigator.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Investigator.error = e.message
        })
    },

    revoke_investigator_access: function(investigatorPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/hospitals/revoke_investigator_access/" + investigatorPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Investigator.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Investigator.error = e.message
        })
    },

    request_inform_consent: function(personPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/investigators/request_inform_consent/" + personPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Investigator.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Investigator.error = e.message
        })
    },

    import_to_trial_data: function(id, patient_pkey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/investigators/import_to_trial_data/" + patient_pkey + "/" + id,
            headers: {
                'ClientKey': clientKey
            },
//            data: dataList,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Investigator.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Investigator.error = e.message
        })
    },

//    import_screening_data: function(dataList, clientKey) {
//        return m.request({
//            method: "POST",
//            url: "/api/investigators/import_screening_data",
//            headers: {
//                'ClientKey': clientKey
//            },
//            data: dataList,
//            useBody: true,
////            withCredentials: true,
//        })
//        .then(function(items) {
////            Data.todos.list = items
//            Investigator.error = ""
//        })
//        .catch(function(e) {
//            console.log(e)
//            Investigator.error = e.message
//        })
//    },

    update_trial_data: function(clientKey) {
        return m.request({
            method: "POST",
            url: "/api/investigators/data/update",
            headers: {
                'ClientKey': clientKey
            },
            data: Investigator.trialData,
            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Investigator.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Investigator.error = e.message
        })
    },

    set_eligible: function(clientKey) {
        return m.request({
            method: "POST",
            url: "/api/investigators/data/eligible",
            headers: {
                'ClientKey': clientKey
            },
            data: Investigator.trialData,
            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Investigator.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Investigator.error = e.message
        })
    }

}

module.exports = Investigator