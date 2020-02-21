module.exports = function({ hra = "http://trial-rest-api:8000" }) {
    return {

      devServer: {
        host: '0.0.0.0',
        port: 8080,
        proxy: {
          '/api': {
            target: hra,
            headers: {
              "X-real-ip": "0.0.0.0"
            },
            pathRewrite: {
              '^/api' : ''
            }
          }
        }
      }

    }
};