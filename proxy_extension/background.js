var config = {
    mode: "fixed_servers",
    rules: {
        singleProxy: {
            scheme: "https",
            host: "superproxy.zenrows.com",
            port: parseInt(1338)
        },
        bypassList: ["localhost"]
    }
};

chrome.proxy.set({value: config, scope: "regular"}, function() {});

chrome.webRequest.onAuthRequired.addListener(
    function(details) {
        return {
            authCredentials: {
                username: "RtYjSRGy2XmN",
                password: "QEzWBKeexsyq_country-us"
            }
        };
    },
    {urls: ["<all_urls>"]},
    ['blocking']
);
