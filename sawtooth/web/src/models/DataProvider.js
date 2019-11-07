var m = require("mithril")

var DataProvider = {
    list: [],
    error: "",
    loadList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/data_providers",
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
            console.log("Get data provider list")
            DataProvider.error = ""
            DataProvider.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            DataProvider.error = e.message
            DataProvider.list = []
        })
    },

    current: {},

    register: function() {
        return m.request({
            method: "POST",
            url: "/api/data_providers",
            data: DataProvider.current,
            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            DataProvider.error = ""
        })
        .catch(function(e) {
            console.log(e)
            DataProvider.error = e.message
        })
    },

    grant_access_to_share_data: function(dataProviderPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/hospitals/grant_access_to_share_data/" + dataProviderPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            DataProvider.error = ""
        })
        .catch(function(e) {
            console.log(e)
            DataProvider.error = e.message
        })
    },

    revoke_access_to_share_data: function(dataProviderPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/hospitals/revoke_access_to_share_data/" + dataProviderPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            DataProvider.error = ""
        })
        .catch(function(e) {
            console.log(e)
            DataProvider.error = e.message
        })
    }

}

module.exports = DataProvider